"""Job runner for evaluating and executing jobs.

Implements the job evaluation logic from SPEC 5.3:
- Evaluate jobs sequentially by job_id
- Run check() with timeout
- Create intents for triggered jobs
- Schedule intents for worker pickup
"""

from __future__ import annotations

import asyncio
import inspect
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from dataclasses import dataclass, field
from functools import lru_cache
from typing import TYPE_CHECKING

from brawny._context import _current_job, _job_ctx, reset_check_block, set_check_block
from brawny._rpc.context import reset_job_context as reset_rpc_job_context
from brawny._rpc.context import set_job_context as set_rpc_job_context
from brawny.jobs.base import Job  # Runtime import for legacy API detection
from brawny.jobs.kv import DatabaseJobKVStore
from brawny.logging import LogEvents, get_logger
from brawny.metrics import (
    INTENTS_CREATED,
    JOB_BUILD_TIMEOUTS,
    JOB_CHECK_SECONDS,
    JOB_CHECK_TIMEOUTS,
    JOBS_TRIGGERED,
    LAST_INTENT_CREATED_TIMESTAMP,
    get_metrics,
)
from brawny.model.contexts import BlockContext, BuildContext, CheckContext
from brawny.model.types import BlockInfo, Trigger

if TYPE_CHECKING:
    from brawny._rpc.clients import RPCClients
    from brawny._rpc.manager import RPCManager
    from brawny.alerts.contracts import ContractSystem
    from brawny.config import Config
    from brawny.db.base import Database
    from brawny.lifecycle import LifecycleDispatcher
    from brawny.model.types import TxIntent, TxIntentSpec

logger = get_logger(__name__)


@lru_cache(maxsize=1024)
def _accepts_ctx(job_class: type, method_name: str) -> bool:
    """Determine if method can safely receive ctx as a positional argument.

    The question: "Can I legally call this method with one positional arg (ctx)?"

    Returns True only if:
    - Method has *args (can always accept one positional), OR
    - First positional param is named 'ctx'

    This prevents accidentally passing ctx to a method like:
        def check(self, foo, ctx):  # Would break if we pass ctx as foo

    Cached by (job_class, method_name) for stability across decorators.
    """
    method = getattr(job_class, method_name)
    sig = inspect.signature(method)

    params = [p for p in sig.parameters.values() if p.name != "self"]

    # If there's *args, one positional is always safe
    if any(p.kind is inspect.Parameter.VAR_POSITIONAL for p in params):
        return True

    positional = [
        p for p in params
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]

    if not positional:
        return False

    # Conservative: only pass ctx if the first positional param is named 'ctx'
    return positional[0].name == "ctx"


@dataclass
class JobResult:
    """Result of running a job check."""

    job_id: str
    triggered: bool = False
    trigger: Trigger | None = None
    intent_created: bool = False
    skipped: bool = False
    error: Exception | None = None


@dataclass
class BlockResult:
    """Result of processing a block."""

    block_number: int
    jobs_checked: int = 0
    jobs_triggered: int = 0
    intents_created: int = 0
    errors: list[str] = field(default_factory=list)


class JobRunner:
    """Job runner for evaluating and executing registered jobs.

    Jobs are evaluated sequentially within a block (deterministic order).
    Multiple workers can process intents concurrently.
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        config: Config,
        jobs: dict[str, Job],
        on_intent_created: Callable[[str], None] | None = None,
        lifecycle: LifecycleDispatcher | None = None,
        contract_system: ContractSystem | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
        loop_thread_id: int | None = None,
    ) -> None:
        """Initialize job runner.

        Args:
            db: Database connection
            rpc: RPC manager (default group client)
            config: Application configuration
            jobs: Dictionary of job_id -> Job instances
            on_intent_created: Callback when intent is created (for worker scheduling)
            loop: Event loop for async job.check() support
            loop_thread_id: Thread ID that owns the loop (for assertion)
        """
        self._db = db
        self._rpc = rpc
        self._config = config
        self._jobs = jobs
        self._chain_id = config.chain_id
        self._on_intent_created = on_intent_created
        self._lifecycle = lifecycle
        self._contract_system = contract_system
        self._loop = loop
        self._loop_thread_id = loop_thread_id

        # RPC clients cache for per-job read routing
        from brawny._rpc.clients import RPCClients
        self._rpc_clients: RPCClients = RPCClients(config)

        # Thread pool for job check timeouts (used for sync jobs only)
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="job_check")
        self._abandoned_executors = 0

    def _recreate_executor_after_timeout(self, operation: str, job_id: str) -> None:
        """Recreate the executor after a timeout to prevent deadlock.

        When a job times out, the worker thread continues running but the future
        is cancelled. With max_workers=1, this blocks all subsequent job operations.
        We recreate the executor to abandon the stuck thread and continue processing.

        Args:
            operation: The operation that timed out ("check" or "build")
            job_id: The job that caused the timeout
        """
        logger.warning(
            "runner.executor_recreated",
            operation=operation,
            job_id=job_id,
            reason="Abandoning stuck thread after timeout",
            abandoned_executors=self._abandoned_executors + 1,
        )
        # Don't wait for the stuck thread - just abandon it
        self._executor.shutdown(wait=False, cancel_futures=True)
        self._abandoned_executors += 1
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="job_check")

    def process_block(self, block: BlockInfo) -> BlockResult:
        """Process a block by evaluating all enabled jobs.

        Jobs are evaluated in job_id order (deterministic).

        Args:
            block: Block information

        Returns:
            BlockResult with processing stats
        """
        result = BlockResult(block_number=block.block_number)

        # Warm gas quote cache at start of block (for executor)
        if self._loop is not None:
            try:
                self._loop.run_until_complete(
                    asyncio.wait_for(self._rpc.gas_quote(), timeout=5.0)
                )
            except Exception as e:
                logger.warning("gas.cache_warm_failed", error=str(e))

        # Get enabled jobs sorted by job_id
        enabled_jobs = self._db.get_enabled_jobs()

        for job_config in enabled_jobs:
            job_id = job_config.job_id

            # Get job instance from registry
            job = self._jobs.get(job_id)
            if job is None:
                # Job in DB but not discovered - skip silently
                # (orphaned jobs are warned about once at startup)
                continue

            # Check interval
            last_checked = job_config.last_checked_block_number
            if last_checked is not None and (block.block_number - last_checked) < job.check_interval_blocks:
                logger.debug(
                    LogEvents.JOB_CHECK_SKIP,
                    job_id=job_id,
                    block_number=block.block_number,
                    last_checked=last_checked,
                    interval=job.check_interval_blocks,
                )
                continue
            backoff_until = self._db.get_job_kv(job_id, "backoff_until_block")
            if isinstance(backoff_until, int) and block.block_number <= backoff_until:
                logger.debug(
                    "job.check_backoff",
                    job_id=job_id,
                    block_number=block.block_number,
                    backoff_until=backoff_until,
                )
                continue

            if job.max_in_flight_intents is not None:
                active_count = self._db.get_active_intent_count(
                    job_id,
                    chain_id=self._chain_id,
                )
                if active_count >= job.max_in_flight_intents:
                    logger.warning(
                        "job.check.backpressure",
                        job_id=job_id,
                        block_number=block.block_number,
                        active_intents=active_count,
                        limit=job.max_in_flight_intents,
                    )
                    self._db.update_job_checked(
                        job_id,
                        block.block_number,
                        triggered=False,
                    )
                    continue

            # Run job check
            job_result = self._run_job_check(job, block)
            result.jobs_checked += 1

            if job_result.error:
                if self._config.job_error_backoff_blocks > 0:
                    self._db.set_job_kv(
                        job_id,
                        "backoff_until_block",
                        block.block_number + self._config.job_error_backoff_blocks,
                    )
                result.errors.append(f"{job_id}: {job_result.error}")
                continue

            # Update last checked
            self._db.update_job_checked(
                job_id,
                block.block_number,
                triggered=job_result.triggered,
            )

            if job_result.triggered and job_result.trigger:
                result.jobs_triggered += 1

                # Create intent if tx required
                if job_result.trigger.tx_required:
                    try:
                        intent, is_new = self._create_intent_for_trigger(
                            job, block, job_result.trigger
                        )
                        if is_new:
                            result.intents_created += 1
                            metrics = get_metrics()
                            metrics.counter(INTENTS_CREATED).inc(
                                chain_id=self._chain_id,
                                job_id=job_id,
                            )
                            metrics.gauge(LAST_INTENT_CREATED_TIMESTAMP).set(
                                time.time(),
                                chain_id=self._chain_id,
                            )
                            if self._lifecycle:
                                self._lifecycle.on_triggered(
                                    job,
                                    job_result.trigger,
                                    block,
                                    intent.intent_id,
                                )
                    except Exception as e:
                        logger.error(
                            "intent.creation_failed",
                            job_id=job_id,
                            error=str(e),
                        )
                        if self._config.job_error_backoff_blocks > 0:
                            self._db.set_job_kv(
                                job_id,
                                "backoff_until_block",
                                block.block_number + self._config.job_error_backoff_blocks,
                            )
                        result.errors.append(f"{job_id} intent: {e}")
                else:
                    if self._lifecycle:
                        self._lifecycle.on_triggered(
                            job,
                            job_result.trigger,
                            block,
                            None,
                        )

        return result

    def _run_job_check(self, job: Job, block: BlockInfo) -> JobResult:
        """Run a job's check method with timeout.

        Supports both sync and async check() methods. Async jobs use the
        daemon's event loop; sync jobs use the thread pool executor.

        Args:
            job: Job instance
            block: Block information

        Returns:
            JobResult with check outcome
        """
        logger.debug(
            LogEvents.JOB_CHECK_START,
            job_id=job.job_id,
            block_number=block.block_number,
        )

        metrics = get_metrics()
        start_time = time.perf_counter()

        # Build check context (phase-specific)
        ctx = self._build_check_context(job, block)

        from brawny.scripting import set_job_context

        try:
            # Use async path if loop is available
            if self._loop is not None and self._loop_thread_id is not None:
                # Assert we're on the correct thread (loop owner)
                assert threading.get_ident() == self._loop_thread_id, \
                    "check_job called from wrong thread"

                trigger = self._loop.run_until_complete(
                    asyncio.wait_for(
                        self._run_check_async(job, block, ctx),
                        timeout=job.check_timeout_seconds,
                    )
                )
            else:
                # Fallback to sync executor (for tests or when no loop provided)
                def _call_with_job_context() -> Trigger | None:
                    ctx_token = _job_ctx.set(ctx)
                    job_token = _current_job.set(job)
                    check_block_token = set_check_block(ctx.block.number)
                    thread_rpc_ctx_token = set_rpc_job_context(job.job_id)
                    set_job_context(True)
                    logger.debug(
                        "check.block_pinned",
                        job_id=job.job_id,
                        block_number=ctx.block.number,
                    )
                    try:
                        # Call with or without ctx based on signature
                        if _accepts_ctx(type(job), "check"):
                            return job.check(ctx)
                        else:
                            return job.check()
                    finally:
                        set_job_context(False)
                        reset_rpc_job_context(thread_rpc_ctx_token)
                        reset_check_block(check_block_token)
                        _job_ctx.reset(ctx_token)
                        _current_job.reset(job_token)

                future = self._executor.submit(_call_with_job_context)
                trigger = future.result(timeout=job.check_timeout_seconds)

            if trigger:
                logger.info(
                    LogEvents.JOB_CHECK_TRIGGERED,
                    job_id=job.job_id,
                    block_number=block.block_number,
                    reason=trigger.reason,
                    tx_required=trigger.tx_required,
                )
                metrics.counter(JOBS_TRIGGERED).inc(
                    chain_id=self._chain_id,
                    job_id=job.job_id,
                )
                return JobResult(
                    job_id=job.job_id,
                    triggered=True,
                    trigger=trigger,
                )
            else:
                return JobResult(job_id=job.job_id, triggered=False)

        except (asyncio.TimeoutError, FuturesTimeout):
            logger.error(
                LogEvents.JOB_CHECK_TIMEOUT,
                job_id=job.job_id,
                block_number=block.block_number,
                timeout=job.check_timeout_seconds,
            )
            metrics.counter(JOB_CHECK_TIMEOUTS).inc(
                chain_id=self._chain_id,
                job_id=job.job_id,
            )
            # Recreate executor to prevent stuck thread from blocking future jobs
            if self._loop is None:
                self._recreate_executor_after_timeout("check", job.job_id)
            return JobResult(
                job_id=job.job_id,
                error=TimeoutError(f"Job check timed out after {job.check_timeout_seconds}s"),
            )

        except Exception as e:
            logger.error(
                "job.check.error",
                job_id=job.job_id,
                block_number=block.block_number,
                error=str(e),
            )
            return JobResult(job_id=job.job_id, error=e)
        finally:
            duration = time.perf_counter() - start_time
            metrics.histogram(JOB_CHECK_SECONDS).observe(
                duration,
                chain_id=self._chain_id,
                job_id=job.job_id,
            )

    async def _run_check_async(self, job: Job, block: BlockInfo, ctx: CheckContext) -> Trigger | None:
        """Run job.check(), handling sync or async."""
        from brawny.scripting import set_job_context

        ctx_token = _job_ctx.set(ctx)
        job_token = _current_job.set(job)
        check_block_token = set_check_block(ctx.block.number)
        async_rpc_ctx_token = set_rpc_job_context(job.job_id)
        set_job_context(True)
        logger.debug(
            "check.block_pinned",
            job_id=job.job_id,
            block_number=ctx.block.number,
        )

        try:
            # Call with or without ctx based on signature
            if _accepts_ctx(type(job), "check"):
                result = job.check(ctx)
            else:
                result = job.check()

            if inspect.isawaitable(result):
                return await result
            return result
        finally:
            set_job_context(False)
            reset_rpc_job_context(async_rpc_ctx_token)
            reset_check_block(check_block_token)
            _job_ctx.reset(ctx_token)
            _current_job.reset(job_token)

    def _build_check_context(self, job: Job, block: BlockInfo) -> CheckContext:
        """Build a CheckContext for job check phase.

        Args:
            job: Job instance
            block: Block information

        Returns:
            CheckContext with block-pinned RPC access and read+write KV
        """
        # Get read RPC client for this job's read_group
        from brawny.alerts.contracts import SimpleContractFactory
        from brawny.config.routing import resolve_job_groups

        read_group, _ = resolve_job_groups(self._config, job)
        rpc = self._rpc_clients.get_read_client(read_group)

        # Build BlockContext (immutable snapshot)
        block_ctx = BlockContext(
            number=block.block_number,
            timestamp=block.timestamp,
            hash=block.block_hash,
            base_fee=0,  # TODO: Get from block if available
            chain_id=block.chain_id,
        )

        # Build ContractFactory
        contracts = SimpleContractFactory(self._contract_system) if self._contract_system else None

        return CheckContext(
            block=block_ctx,
            kv=DatabaseJobKVStore(self._db, job.job_id),
            job_id=job.job_id,
            rpc=rpc,
            logger=logger.bind(job_id=job.job_id, chain_id=block.chain_id),
            contracts=contracts,
            _db=self._db,
        )

    def _build_build_context(
        self, job: Job, block: BlockInfo, trigger: Trigger, signer_address: str
    ) -> BuildContext:
        """Build a BuildContext for job build phase.

        Args:
            job: Job instance
            block: Block information
            trigger: The trigger from check()
            signer_address: Resolved signer address

        Returns:
            BuildContext with trigger, signer, and read-only KV
        """
        from brawny.alerts.contracts import SimpleContractFactory
        from brawny.config.routing import resolve_job_groups

        read_group, _ = resolve_job_groups(self._config, job)
        rpc = self._rpc_clients.get_read_client(read_group)

        # Build BlockContext
        block_ctx = BlockContext(
            number=block.block_number,
            timestamp=block.timestamp,
            hash=block.block_hash,
            base_fee=0,
            chain_id=block.chain_id,
        )

        contracts = SimpleContractFactory(self._contract_system) if self._contract_system else None

        return BuildContext(
            block=block_ctx,
            trigger=trigger,
            job_id=job.job_id,
            signer_address=signer_address,
            rpc=rpc,
            logger=logger.bind(job_id=job.job_id, chain_id=block.chain_id),
            contracts=contracts,
            kv=DatabaseJobKVStore(self._db, job.job_id),  # KVReader (read-only access)
        )

    def _create_intent_for_trigger(
        self,
        job: Job,
        block: BlockInfo,
        trigger: Trigger,
    ) -> tuple[TxIntent, bool]:
        """Create a transaction intent for a triggered job.

        Args:
            job: Job that triggered
            block: Block information
            trigger: Trigger with intent details
        """
        from brawny.tx.intent import create_intent

        # Resolve signer address for build context
        signer_address = job.signer_address

        # Build context for build_tx (phase-specific)
        ctx = self._build_build_context(job, block, trigger, signer_address)

        from brawny.scripting import set_job_context

        def _call_build_with_job_context() -> TxIntentSpec:
            # Set contextvars for implicit context (inside worker thread)
            ctx_token = _job_ctx.set(ctx)
            job_token = _current_job.set(job)
            rpc_ctx_token = set_rpc_job_context(job.job_id)
            set_job_context(True)
            try:
                # Support legacy build_intent(trigger) API:
                # If job has build_intent but didn't override build_tx, use legacy API
                if hasattr(job, "build_intent") and type(job).build_tx is Job.build_tx:
                    return job.build_intent(ctx.trigger)
                # Call with or without ctx based on signature
                if _accepts_ctx(type(job), "build_tx"):
                    return job.build_tx(ctx)
                else:
                    return job.build_tx()
            finally:
                set_job_context(False)
                reset_rpc_job_context(rpc_ctx_token)
                _job_ctx.reset(ctx_token)
                _current_job.reset(job_token)

        # Call job's build_tx method
        try:
            future = self._executor.submit(_call_build_with_job_context)
            spec = future.result(timeout=job.build_timeout_seconds)
        except FuturesTimeout:
            logger.error(
                "job.build.timeout",
                job_id=job.job_id,
                block_number=block.block_number,
                timeout=job.build_timeout_seconds,
            )
            metrics = get_metrics()
            metrics.counter(JOB_BUILD_TIMEOUTS).inc(
                chain_id=self._chain_id,
                job_id=job.job_id,
            )
            # Recreate executor to prevent stuck thread from blocking future jobs
            self._recreate_executor_after_timeout("build", job.job_id)
            raise TimeoutError(f"build_tx timed out after {job.build_timeout_seconds}s")

        # Compute idempotency parts
        idem_parts = list(trigger.idempotency_parts)
        if not idem_parts:
            # Default: use block number as idempotency part
            idem_parts = [block.block_number]

        # Resolve broadcast group and endpoints once at intent creation
        from brawny._rpc.broadcast import get_broadcast_endpoints
        from brawny.config.routing import resolve_job_groups

        _, broadcast_group = resolve_job_groups(self._config, job)
        broadcast_endpoints = get_broadcast_endpoints(self._config, broadcast_group)

        # Create intent with idempotency and broadcast binding
        # trigger.reason is auto-merged into metadata
        intent, is_new = create_intent(
            db=self._db,
            job_id=job.job_id,
            chain_id=self._chain_id,
            spec=spec,
            idem_parts=idem_parts,
            broadcast_group=broadcast_group,
            broadcast_endpoints=broadcast_endpoints,
            trigger=trigger,
        )

        if is_new and self._on_intent_created:
            self._on_intent_created(str(intent.intent_id))

        return intent, is_new

    def close(self) -> None:
        """Shutdown the runner."""
        self._executor.shutdown(wait=True)
