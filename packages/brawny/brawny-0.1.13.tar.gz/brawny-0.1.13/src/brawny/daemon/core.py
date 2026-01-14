"""BrawnyDaemon - Main daemon orchestrator.

Provides the core daemon class that manages all components and threads.
"""

from __future__ import annotations

import asyncio
import itertools
import os
import socket
import threading
import time
from threading import Event, Lock, Thread
from typing import TYPE_CHECKING, Callable

from brawny.alerts.contracts import ContractSystem
from brawny.alerts.health import health_alert
from brawny.alerts.send import create_send_health
from brawny.daemon.context import DaemonContext, DaemonState, RuntimeOverrides
from brawny.daemon.loops import run_monitor, run_worker
from brawny.db import create_database
from brawny.db.migrate import Migrator, verify_critical_schema
from brawny.jobs.discovery import (
    JobDiscoveryFailed,
    JobLoadError,
    auto_discover_jobs,
    discover_jobs,
)
from brawny.jobs.job_validation import validate_all_jobs
from brawny.jobs.registry import get_registry
from brawny.keystore import create_keystore
from brawny.lifecycle import LifecycleDispatcher
from brawny.logging import get_logger
from brawny.metrics import ACTIVE_WORKERS, get_metrics
from brawny.model.enums import IntentStatus
from brawny.model.startup import StartupMessage
from brawny.model.types import BlockInfo
from brawny._rpc import RPCManager
from brawny.scheduler.poller import BlockPoller
from brawny.scheduler.reorg import ReorgDetector
from brawny.scheduler.runner import JobRunner
from brawny.startup import reconcile_pending_intents
from brawny.tx.executor import TxExecutor
from brawny.tx.intent import transition_intent
from brawny.tx.monitor import TxMonitor
from brawny.tx.replacement import TxReplacer
from brawny.validation import validate_job_routing
from brawny.telegram import TelegramBot

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny.config.models import TelegramConfig
    from brawny.db.base import Database
    from brawny.jobs.base import Job
    from brawny.keystore import Keystore


class BrawnyDaemon:
    """Main daemon orchestrator.

    Manages all components, threads, and lifecycle for the brawny daemon.
    """

    def __init__(
        self,
        config: "Config",
        overrides: RuntimeOverrides | None = None,
        extra_modules: list[str] | None = None,
    ) -> None:
        """Initialize the daemon.

        Args:
            config: Application configuration
            overrides: Runtime overrides for dry_run, once, worker_count, etc.
            extra_modules: Additional job modules to discover
        """
        self.config = config
        self.overrides = overrides or RuntimeOverrides()
        self._extra_modules = extra_modules or []
        self._log = get_logger(__name__)

        # Components (initialized in start())
        self._db: Database | None = None
        self._rpc: RPCManager | None = None
        self._keystore: Keystore | None = None
        self._contract_system: ContractSystem | None = None
        self._lifecycle: LifecycleDispatcher | None = None
        self._executor: TxExecutor | None = None
        self._monitor: TxMonitor | None = None
        self._replacer: TxReplacer | None = None
        self._job_runner: JobRunner | None = None
        self._reorg_detector: ReorgDetector | None = None
        self._poller: BlockPoller | None = None

        # Jobs
        self._jobs: dict[str, Job] = {}

        # Telegram (cached instance)
        self._telegram_bot: TelegramBot | None = None

        # Health alerting (initialized in initialize())
        self._health_send_fn: Callable[..., None] | None = None
        self._health_chat_id: str | None = None
        self._health_cooldown: int = 1800

        # Threading
        self._stop = Event()
        self._wakeup_hint = Event()
        self._worker_threads: list[Thread] = []
        self._monitor_thread: Thread | None = None
        self._monitor_stop = Event()

        # Inflight tracking
        self._inflight_lock = Lock()
        self._inflight_count = 0
        self._inflight_zero = Event()
        self._inflight_zero.set()

        # Claim token generation
        self._claim_counter = itertools.count(1)
        self._hostname = socket.gethostname()
        self._pid = os.getpid()

        # Async event loop (owned by daemon, used by runner for async job.check())
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)  # Make it the current loop for this thread
        self._loop_thread_id: int = threading.get_ident()  # Assert ownership

    @property
    def db(self) -> "Database":
        """Get database connection."""
        assert self._db is not None, "Daemon not started"
        return self._db

    @property
    def rpc(self) -> RPCManager:
        """Get RPC manager."""
        assert self._rpc is not None, "Daemon not started"
        return self._rpc

    @property
    def jobs(self) -> dict[str, "Job"]:
        """Get discovered jobs."""
        return self._jobs

    @property
    def keystore(self) -> "Keystore | None":
        """Get keystore (None in dry_run mode)."""
        return self._keystore

    def _check_schema(self) -> None:
        """Verify critical DB schema columns exist. Hard-fail if not."""
        assert self._db is not None

        try:
            verify_critical_schema(self._db)
        except Exception as exc:
            error_msg = str(exc)
            self._log.critical(
                "schema.validation_failed",
                error=error_msg,
                table="tx_intents",
            )
            health_alert(
                component="brawny.startup.schema",
                chain_id=self.config.chain_id,
                error=error_msg,
                level="critical",
                action="Run: brawny migrate",
                db_dialect=self._db.dialect,
                force_send=True,
                send_fn=self._health_send_fn,
                health_chat_id=self._health_chat_id,
            )
            raise SystemExit(f"DB schema mismatch: {error_msg}. Run: brawny migrate") from exc

    def _make_claim_token(self, worker_id: int) -> str:
        """Generate a unique claim token for a worker."""
        return f"{self._hostname}:{self._pid}:{worker_id}:{next(self._claim_counter)}"

    def _make_claimed_by(self, worker_id: int) -> str:
        """Generate a stable claimed_by identifier for a worker."""
        return f"{self._hostname}:{self._pid}:{worker_id}"

    def _inflight_start(self) -> None:
        """Mark an inflight operation starting."""
        with self._inflight_lock:
            self._inflight_count += 1
            self._inflight_zero.clear()

    def _inflight_done(self) -> None:
        """Mark an inflight operation complete."""
        with self._inflight_lock:
            self._inflight_count = max(0, self._inflight_count - 1)
            if self._inflight_count == 0:
                self._inflight_zero.set()

    def _on_intent_created(self, intent_id: str) -> None:
        """Callback when intent is created."""
        self._wakeup_hint.set()

    def _process_block(self, block: BlockInfo) -> None:
        """Process a single block."""
        assert self._job_runner is not None

        self._log.info(
            "block.ingest.start",
            block_number=block.block_number,
        )

        block_result = self._job_runner.process_block(block)

        self._log.info(
            "block.ingest.done",
            block_number=block.block_number,
            jobs_checked=block_result.jobs_checked,
            jobs_triggered=block_result.jobs_triggered,
            intents_created=block_result.intents_created,
        )

    def _discover_jobs(self) -> list[JobLoadError]:
        """Discover and register jobs based on config.

        Returns:
            List of JobLoadError for any modules that failed to load.
        """
        registry = get_registry()
        registry.clear()  # Start fresh to prevent partial state leakage

        if self._extra_modules:
            discovered, errors = discover_jobs(self._extra_modules)
        else:
            discovered, errors = auto_discover_jobs()

        # Log discovery summary
        self._log.info(
            "job.discovery.complete",
            jobs_loaded=len(discovered),
            jobs_failed=len(errors),
        )

        if errors:
            registry.clear()  # Don't leave partial state
            return errors

        self._jobs = {job.job_id: job for job in registry.get_all()}
        return []

    def _validate_jobs(self) -> tuple[dict[str, list[str]], list[str]]:
        """Validate discovered jobs.

        Returns:
            Tuple of (validation_errors, routing_errors)
        """
        validation_errors: dict[str, list[str]] = {}
        routing_errors: list[str] = []

        if self._jobs:
            keystore = self._keystore if not self.overrides.dry_run else None
            validation_errors = validate_all_jobs(self._jobs, keystore=keystore)
            routing_errors = validate_job_routing(self.config, self._jobs)

        return validation_errors, routing_errors

    def _validate_telegram_config(self) -> list[str]:
        """Validate telegram configuration and routing.

        Returns:
            List of validation errors (empty if valid)
        """
        from brawny.alerts.routing import validate_targets
        from brawny.model.errors import ConfigError

        tg = self.config.telegram
        errors: list[str] = []

        # Check if any routing is configured (use truthiness, not is not None)
        has_routing = bool(tg.default) or any(getattr(j, "_alert_to", None) for j in self._jobs.values())

        # Validate all name references
        valid_names = set(tg.chats.keys())

        # Validate default targets
        invalid = validate_targets(tg.default, valid_names)
        for name in invalid:
            errors.append(f"telegram.default references unknown chat '{name}'")

        # Validate each job's alert_to target
        for job_id, job in self._jobs.items():
            target = getattr(job, "_alert_to", None)
            if target is None:
                continue

            invalid = validate_targets(target, valid_names)
            for name in invalid:
                errors.append(
                    f"Job '{job_id}' references unknown telegram chat '{name}'. "
                    f"Valid names: {sorted(valid_names)}"
                )

        if errors:
            for err in errors:
                self._log.error("telegram.routing.invalid", error=err)
            return errors

        # Warn about configuration issues (non-fatal)
        if has_routing and not tg.bot_token:
            self._log.warning(
                "telegram.bot_token_missing",
                message="Jobs use alert_to= or telegram.default is set, but bot_token is missing",
            )
        elif tg.bot_token and not tg.default and not any(getattr(j, "_alert_to", None) for j in self._jobs.values()):
            self._log.warning(
                "telegram.no_default_targets",
                message="bot_token set but no default targets and no jobs use alert_to=",
            )

        return []

    def _reconcile_startup(self) -> None:
        """Reconcile state on startup."""
        assert self._db is not None
        assert self._monitor is not None or self.overrides.dry_run

        # Reconcile nonces
        if self._executor and self._executor.nonce_manager:
            self._log.info("startup.reconcile_nonces")
            self._executor.nonce_manager.reconcile()

        # Recover SENDING intents
        stuck_sending = self._db.get_intents_by_status(
            IntentStatus.SENDING.value,
            chain_id=self.config.chain_id,
        )
        for intent in stuck_sending:
            attempt = self._db.get_latest_attempt_for_intent(intent.intent_id)
            if attempt and attempt.tx_hash:
                transition_intent(
                    self._db,
                    intent.intent_id,
                    IntentStatus.PENDING,
                    "startup_recover_sending",
                    chain_id=self.config.chain_id,
                )
            else:
                # No tx_hash means intent never got broadcast - reset to CREATED
                if attempt and self._executor and self._executor.nonce_manager:
                    from brawny.model.enums import AttemptStatus
                    self._db.update_attempt_status(
                        attempt.attempt_id,
                        AttemptStatus.FAILED.value,
                        error_code="startup_stuck",
                        error_detail="Stuck in SENDING without broadcast",
                    )
                    self._executor.nonce_manager.release(intent.signer_address, attempt.nonce)
                transition_intent(
                    self._db,
                    intent.intent_id,
                    IntentStatus.CREATED,
                    "startup_recover_sending",
                    chain_id=self.config.chain_id,
                )

        if stuck_sending:
            self._log.warning(
                "startup.recover_sending_intents",
                count=len(stuck_sending),
            )

        # Reconcile pending intents
        if self._monitor:
            reconcile_pending_intents(
                self._db,
                self._monitor,
                self.config.chain_id,
                self._log,
            )

    def _start_workers(self) -> None:
        """Start worker threads."""
        if self.overrides.dry_run:
            return

        worker_count = (
            self.overrides.worker_count
            if self.overrides.worker_count is not None
            else self.config.worker_count
        )

        ctx = DaemonContext(
            config=self.config,
            log=self._log,
            db=self._db,
            rpc=self._rpc,
            executor=self._executor,
            monitor=self._monitor,
            replacer=self._replacer,
            nonce_manager=self._executor.nonce_manager if self._executor else None,
            chain_id=self.config.chain_id,
            health_send_fn=self._health_send_fn,
            health_chat_id=self._health_chat_id,
            health_cooldown=self._health_cooldown,
        )
        state = DaemonState(
            make_claim_token=self._make_claim_token,
            make_claimed_by=self._make_claimed_by,
            inflight_inc=self._inflight_start,
            inflight_dec=self._inflight_done,
        )

        for i in range(worker_count):
            t = Thread(
                target=run_worker,
                args=(i, self._stop, self._wakeup_hint, ctx, state, self.overrides.dry_run),
                daemon=True,
            )
            t.start()
            self._worker_threads.append(t)

        # Start monitor thread
        self._monitor_thread = Thread(
            target=run_monitor,
            args=(self._monitor_stop, ctx, self._worker_threads),
            daemon=True,
        )
        self._monitor_thread.start()

        # Initial gauge
        metrics = get_metrics()
        metrics.gauge(ACTIVE_WORKERS).set(
            len(self._worker_threads),
            chain_id=self.config.chain_id,
        )

    def _shutdown(self) -> None:
        """Shutdown the daemon gracefully."""
        self._log.info("daemon.shutdown.start")

        # Signal stop
        self._stop.set()
        self._wakeup_hint.set()
        self._monitor_stop.set()

        # Wait for inflight
        if not self._inflight_zero.is_set():
            self._log.info(
                "shutdown.await_inflight",
                inflight=self._inflight_count,
                grace_seconds=self.config.shutdown_grace_seconds,
            )
        start_wait = time.time()
        self._inflight_zero.wait(timeout=self.config.shutdown_grace_seconds)
        wait_elapsed = time.time() - start_wait
        remaining = max(0.0, self.config.shutdown_grace_seconds - wait_elapsed)

        # Join workers
        for t in self._worker_threads:
            t.join(timeout=remaining)

        # Join monitor
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)

        # Log any threads still alive
        alive = [t for t in self._worker_threads if t.is_alive()]
        if alive:
            self._log.warning("shutdown.threads_still_alive", count=len(alive))

        # Close event loop
        if self._loop and not self._loop.is_closed():
            self._loop.close()

        self._log.info("daemon.shutdown.complete")

    def initialize(
        self,
    ) -> tuple[dict[str, list[str]], list[str], list["StartupMessage"]]:
        """Initialize all components.

        Returns:
            Tuple of (validation_errors, routing_errors, startup_messages) for jobs
        """
        startup_messages: list[StartupMessage] = []

        # Database
        self._db = create_database(
            self.config.database_url,
            pool_size=self.config.database_pool_size,
            pool_max_overflow=self.config.database_pool_max_overflow,
            pool_timeout=self.config.database_pool_timeout_seconds,
            circuit_breaker_failures=self.config.db_circuit_breaker_failures,
            circuit_breaker_seconds=self.config.db_circuit_breaker_seconds,
        )
        self._db.connect()

        # Migrations
        migrator = Migrator(self._db)
        pending = migrator.pending()
        if pending:
            self._log.info("migrations.applying", count=len(pending))
            migrator.migrate()

        # RPC
        self._rpc = RPCManager.from_config(self.config)

        self._log.info(
            "startup.finality_policy",
            chain_id=self.config.chain_id,
            finality_confirmations=self.config.finality_confirmations,
            read_only=True,
        )

        # Keystore (only in live mode)
        if not self.overrides.dry_run:
            self._keystore = create_keystore(
                self.config.keystore_type,
                keystore_path=self.config.keystore_path,
                allowed_signers=[],
            )
            # Make keystore available for signer_address() helper
            from brawny.api import _set_keystore
            _set_keystore(self._keystore)

            # Collect keystore warnings
            startup_messages.extend(self._keystore.get_warnings())

        # Discover jobs
        load_errors = self._discover_jobs()
        if load_errors:
            for err in load_errors:
                self._log.error(
                    "job.module_load_failed",
                    path=err.path,
                    message=err.message,
                    traceback=err.traceback,
                )
            raise JobDiscoveryFailed(load_errors)

        # Sanity check: don't run with zero jobs
        if not self._jobs:
            raise RuntimeError("No jobs discovered - check your jobs directory")

        validation_errors, routing_errors = self._validate_jobs()

        # Validate telegram routing (fails hard on unknown names)
        telegram_errors = self._validate_telegram_config()
        if telegram_errors:
            from brawny.model.errors import ConfigError
            raise ConfigError(
                f"Invalid telegram routing: {len(telegram_errors)} error(s)\n"
                + "\n".join(f"  - {e}" for e in telegram_errors)
            )

        # Cache TelegramBot instance (if configured)
        if self.config.telegram.bot_token:
            self._telegram_bot = TelegramBot(token=self.config.telegram.bot_token)

        # Initialize health alerting
        tg = self.config.telegram
        if tg and tg.health_chat:
            resolved = tg.chats.get(tg.health_chat)
            if resolved:
                self._health_chat_id = resolved
                if self._telegram_bot:
                    self._health_send_fn = create_send_health(self._telegram_bot)
            else:
                # health_chat configured but not found in chats - warn loudly
                self._log.warning(
                    "health_chat_missing",
                    health_chat=tg.health_chat,
                    available_chats=list(tg.chats.keys()),
                )

        if tg:
            self._health_cooldown = tg.health_cooldown_seconds

        # Validate schema (after health is set up so we can alert on failure)
        self._check_schema()

        # Contract system
        self._contract_system = ContractSystem(self._rpc, self.config)

        # Lifecycle
        self._lifecycle = LifecycleDispatcher(
            self._db,
            self._rpc,
            self.config,
            self._jobs,
            contract_system=self._contract_system,
            telegram_bot=self._telegram_bot,
        )

        # TX execution components (only in live mode)
        if self._keystore:
            self._executor = TxExecutor(
                self._db, self._rpc, self._keystore, self.config,
                lifecycle=self._lifecycle,
                jobs=self._jobs,
            )
            self._monitor = TxMonitor(
                self._db, self._rpc, self._executor.nonce_manager, self.config,
                lifecycle=self._lifecycle
            )
            self._replacer = TxReplacer(
                self._db, self._rpc, self._keystore, self._executor.nonce_manager, self.config,
                lifecycle=self._lifecycle
            )

        # Job runner
        self._job_runner = JobRunner(
            self._db,
            self._rpc,
            self.config,
            self._jobs,
            lifecycle=self._lifecycle,
            contract_system=self._contract_system,
            loop=self._loop,
            loop_thread_id=self._loop_thread_id,
        )
        self._job_runner._on_intent_created = self._on_intent_created

        # Reorg detector
        self._reorg_detector = ReorgDetector(
            db=self._db,
            rpc=self._rpc,
            chain_id=self.config.chain_id,
            reorg_depth=self.config.reorg_depth,
            block_hash_history_size=self.config.block_hash_history_size,
            finality_confirmations=self.config.finality_confirmations,
            lifecycle=self._lifecycle,
            health_send_fn=self._health_send_fn,
            health_chat_id=self._health_chat_id,
            health_cooldown=self._health_cooldown,
        )

        # Block poller
        self._poller = BlockPoller(
            self._db, self._rpc, self.config, self._process_block,
            reorg_detector=self._reorg_detector,
            health_send_fn=self._health_send_fn,
            health_chat_id=self._health_chat_id,
            health_cooldown=self._health_cooldown,
        )

        # Register jobs in database
        for job_id, job in self._jobs.items():
            self._db.upsert_job(job_id, job.name, job.check_interval_blocks)

        return validation_errors, routing_errors, startup_messages

    def run(self, blocking: bool = True) -> None:
        """Run the daemon.

        Args:
            blocking: If True, block until shutdown. If False, return immediately.
        """
        assert self._poller is not None, "Daemon not initialized"

        # Startup reconciliation
        self._reconcile_startup()

        # Warm gas cache before workers start (eliminates cold-start race)
        try:
            self._loop.run_until_complete(
                asyncio.wait_for(self._rpc.gas_quote(), timeout=5.0)
            )
            self._log.debug("startup.gas_cache_warmed")
        except Exception as e:
            self._log.warning("startup.gas_cache_warm_failed", error=str(e))

        # Start workers
        self._start_workers()

        try:
            if self.overrides.once:
                # Single iteration mode
                self._poller._poll_once()
            else:
                # Normal polling mode
                try:
                    self._poller.start(blocking=blocking)
                except KeyboardInterrupt:
                    self._log.info("daemon.keyboard_interrupt")
        finally:
            self._shutdown()

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the daemon.

        Signals all components to stop. Called from shutdown handler.

        Args:
            timeout: Timeout for stopping the poller
        """
        # Signal workers and monitor to stop
        self._stop.set()
        self._wakeup_hint.set()
        self._monitor_stop.set()

        if self._poller:
            self._poller.stop(timeout=timeout)
