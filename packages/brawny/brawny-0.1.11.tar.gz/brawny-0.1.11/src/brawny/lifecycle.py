"""Simplified lifecycle dispatcher for job hooks.

Implements 3 lifecycle hooks (on_trigger, on_success, on_failure).
Jobs call alert() explicitly within hooks to send notifications.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any
from uuid import UUID

from brawny.alerts.send import AlertConfig, AlertEvent, AlertPayload
from brawny.jobs.kv import DatabaseJobKVStore, DatabaseJobKVReader
from brawny.logging import LogEvents, get_logger
from brawny.model.contexts import (
    AlertContext,
    BlockContext,
    TriggerContext,
    SuccessContext,
    FailureContext,
)
from brawny.model.errors import (
    ErrorInfo,
    FailureStage,
    FailureType,
    HookType,
    TriggerReason,
)
from brawny.model.events import DecodedEvent
from brawny.model.types import BlockInfo, Trigger, HookName

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny.db.base import Database
    from brawny.jobs.base import Job, TxInfo, TxReceipt, BlockInfo as AlertBlockInfo
    from brawny.model.types import TxAttempt, TxIntent
    from brawny._rpc.manager import RPCManager
    from brawny.alerts.contracts import ContractSystem, SimpleContractFactory
    from brawny.telegram import TelegramBot

logger = get_logger(__name__)


class LifecycleDispatcher:
    """Dispatch job lifecycle hooks.

    Lifecycle Hooks (3):
        - on_trigger: Job check returns Trigger, BEFORE build_tx
        - on_success: Transaction confirmed on-chain
        - on_failure: Any failure (intent may be None for pre-intent failures)

    Jobs call alert() explicitly within hooks to send notifications.
    All hook invocations go through dispatch_hook() for consistent context setup.
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        config: Config,
        jobs: dict[str, Job],
        contract_system: ContractSystem | None = None,
        telegram_bot: "TelegramBot | None" = None,
    ) -> None:
        self._db = db
        self._rpc = rpc
        self._config = config
        self._jobs = jobs
        self._contract_system = contract_system
        self._telegram_bot = telegram_bot
        self._global_alert_config = self._build_global_alert_config()

    # =========================================================================
    # Hook Dispatch (Single Entry Point)
    # =========================================================================

    def dispatch_hook(self, job: Job, hook: HookName, ctx: Any) -> None:
        """Dispatch a lifecycle hook with proper alert context setup.

        All hook invocations must go through this method to ensure
        alert() works correctly within hooks.

        Args:
            job: The job instance
            hook: Hook name ("on_trigger", "on_success", "on_failure")
            ctx: The context to pass to the hook (TriggerContext, SuccessContext, FailureContext)
        """
        from brawny.scripting import set_job_context

        hook_fn = getattr(job, hook, None)
        if hook_fn is None:
            return

        try:
            with self._alert_context(ctx):
                set_job_context(True)
                hook_fn(ctx)
        except Exception as e:
            logger.error(
                f"job.{hook}_crashed",
                job_id=job.job_id,
                error=str(e)[:200],
            )
            if self._has_alert_config():
                self._send_hook_error_alert(job.job_id, hook, e)
        finally:
            set_job_context(False)

    @contextmanager
    def _alert_context(self, ctx: Any):
        """Set alert context for duration of hook execution with token-based reset."""
        from brawny._context import set_alert_context, reset_alert_context

        token = set_alert_context(ctx)
        try:
            yield
        finally:
            reset_alert_context(token)

    # =========================================================================
    # Public API
    # =========================================================================

    def on_triggered(
        self,
        job: Job,
        trigger: Trigger,
        block: BlockInfo,
        intent_id: UUID | None = None,
    ) -> None:
        """Called when job check returns a Trigger. Runs BEFORE build_tx."""
        # Build TriggerContext
        block_ctx = BlockContext(
            number=block.block_number,
            timestamp=block.timestamp,
            hash=block.block_hash,
            base_fee=0,
            chain_id=block.chain_id,
        )
        ctx = TriggerContext(
            trigger=trigger,
            block=block_ctx,
            kv=DatabaseJobKVStore(self._db, job.job_id),
            logger=logger.bind(job_id=job.job_id, chain_id=self._config.chain_id),
            job_id=job.job_id,
            job_name=job.name,
            chain_id=self._config.chain_id,
            alert_config=self._get_alert_config_for_job(job),
            telegram_config=self._config.telegram,
            telegram_bot=self._telegram_bot,
            job_alert_to=getattr(job, "_alert_to", None),
        )
        self.dispatch_hook(job, "on_trigger", ctx)

    def on_submitted(self, intent: TxIntent, attempt: TxAttempt) -> None:
        """Log submission for observability. No job hook."""
        logger.info(
            "tx.submitted",
            intent_id=str(intent.intent_id),
            attempt_id=str(attempt.attempt_id),
            tx_hash=attempt.tx_hash,
            nonce=attempt.nonce,
            job_id=intent.job_id,
            chain_id=self._config.chain_id,
        )

    def on_confirmed(
        self,
        intent: TxIntent,
        attempt: TxAttempt,
        receipt: dict[str, Any],
    ) -> None:
        """Called when transaction is confirmed on-chain."""
        job = self._jobs.get(intent.job_id)
        if not job:
            return

        # Build SuccessContext
        alert_receipt = self._build_alert_receipt(receipt)
        block_ctx = self._to_block_context(self._fetch_block(receipt.get("blockNumber")))
        events = self._decode_receipt_events(alert_receipt) if self._contract_system else None

        ctx = SuccessContext(
            intent=intent,
            receipt=alert_receipt,
            events=events,
            block=block_ctx,
            kv=DatabaseJobKVReader(self._db, job.job_id),
            logger=logger.bind(job_id=job.job_id, chain_id=self._config.chain_id),
            job_id=job.job_id,
            job_name=job.name,
            chain_id=self._config.chain_id,
            alert_config=self._get_alert_config_for_job(job),
            telegram_config=self._config.telegram,
            telegram_bot=self._telegram_bot,
            job_alert_to=getattr(job, "_alert_to", None),
        )
        self.dispatch_hook(job, "on_success", ctx)

    def on_failed(
        self,
        intent: TxIntent,
        attempt: TxAttempt | None,
        error: Exception,
        failure_type: FailureType,
    ) -> None:
        """Called on any terminal failure with intent. Error is required."""
        job = self._jobs.get(intent.job_id)
        if not job:
            return

        # Build FailureContext
        block_ctx = self._to_block_context(self._get_block_for_failed(attempt, None))

        ctx = FailureContext(
            intent=intent,
            attempt=attempt,
            error=error,
            failure_type=failure_type,
            block=block_ctx,
            kv=DatabaseJobKVReader(self._db, job.job_id),
            logger=logger.bind(job_id=job.job_id, chain_id=self._config.chain_id),
            job_id=job.job_id,
            job_name=job.name,
            chain_id=self._config.chain_id,
            alert_config=self._get_alert_config_for_job(job),
            telegram_config=self._config.telegram,
            telegram_bot=self._telegram_bot,
            job_alert_to=getattr(job, "_alert_to", None),
        )
        self.dispatch_hook(job, "on_failure", ctx)

    def on_check_failed(
        self,
        job: Job,
        error: Exception,
        block: BlockInfo,
    ) -> None:
        """Called when job.check() raises an exception. No intent exists."""
        block_ctx = BlockContext(
            number=block.block_number,
            timestamp=block.timestamp,
            hash=block.block_hash,
            base_fee=0,
            chain_id=block.chain_id,
        )
        ctx = FailureContext(
            intent=None,
            attempt=None,
            error=error,
            failure_type=FailureType.CHECK_EXCEPTION,
            block=block_ctx,
            kv=DatabaseJobKVReader(self._db, job.job_id),
            logger=logger.bind(job_id=job.job_id, chain_id=self._config.chain_id),
            job_id=job.job_id,
            job_name=job.name,
            chain_id=self._config.chain_id,
            alert_config=self._get_alert_config_for_job(job),
            telegram_config=self._config.telegram,
            telegram_bot=self._telegram_bot,
            job_alert_to=getattr(job, "_alert_to", None),
        )
        self.dispatch_hook(job, "on_failure", ctx)

    def on_build_tx_failed(
        self,
        job: Job,
        trigger: Trigger,
        error: Exception,
        block: BlockInfo,
    ) -> None:
        """Called when job.build_tx() raises an exception. No intent exists."""
        block_ctx = BlockContext(
            number=block.block_number,
            timestamp=block.timestamp,
            hash=block.block_hash,
            base_fee=0,
            chain_id=block.chain_id,
        )
        ctx = FailureContext(
            intent=None,
            attempt=None,
            error=error,
            failure_type=FailureType.BUILD_TX_EXCEPTION,
            block=block_ctx,
            kv=DatabaseJobKVReader(self._db, job.job_id),
            logger=logger.bind(job_id=job.job_id, chain_id=self._config.chain_id),
            job_id=job.job_id,
            job_name=job.name,
            chain_id=self._config.chain_id,
            alert_config=self._get_alert_config_for_job(job),
            telegram_config=self._config.telegram,
            telegram_bot=self._telegram_bot,
            job_alert_to=getattr(job, "_alert_to", None),
        )
        self.dispatch_hook(job, "on_failure", ctx)

    def on_deep_reorg(
        self, oldest_known: int | None, history_size: int, last_processed: int
    ) -> None:
        """System-level alert for deep reorg. Not job-specific."""
        if not self._has_alert_config():
            return
        message = (
            f"Deep reorg detected. History window is insufficient "
            f"to safely verify the chain.\n"
            f"oldest_known={oldest_known}, history_size={history_size}, "
            f"last_processed={last_processed}"
        )
        payload = AlertPayload(
            job_id="system",
            job_name="Deep Reorg",
            event_type=AlertEvent.FAILED,
            message=message,
            chain_id=self._config.chain_id,
        )
        self._fire_alert(payload, self._global_alert_config)


    def _send_hook_error_alert(self, job_id: str, hook_type: str, error: Exception) -> None:
        """Send fallback error alert when a hook fails."""
        message = f"Alert hook failed for job {job_id}: {error}"
        payload = AlertPayload(
            job_id=job_id,
            job_name=job_id,
            event_type=AlertEvent.FAILED,
            message=message,
            chain_id=self._config.chain_id,
        )
        self._fire_alert(payload, self._global_alert_config)

    def _fire_alert(self, payload: AlertPayload, config: AlertConfig) -> None:
        """Fire alert asynchronously. Fire-and-forget."""
        import asyncio
        from brawny.alerts import send as alerts_send

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(alerts_send.send_alert(payload, config))
        except RuntimeError:
            # No running loop - run synchronously
            asyncio.run(alerts_send.send_alert(payload, config))

    def _build_global_alert_config(self) -> AlertConfig:
        """Build global AlertConfig from application config (legacy compatibility)."""
        # Use new telegram config structure
        tg = self._config.telegram
        chat_ids: list[str] = []

        # Resolve default targets to chat IDs
        if tg.default:
            for name in tg.default:
                if name in tg.chats:
                    chat_ids.append(tg.chats[name])
                elif name.lstrip("-").isdigit():
                    # Raw chat ID
                    chat_ids.append(name)

        return AlertConfig(
            telegram_token=tg.bot_token,
            telegram_chat_ids=chat_ids,
        )

    def _get_alert_config_for_job(self, job: Job) -> AlertConfig:
        """Resolve per-job overrides into job-scoped AlertConfig (legacy compatibility)."""
        job_chat_ids = getattr(job, "telegram_chat_ids", None)
        if job_chat_ids:
            # Job-level targets override global (legacy API)
            return AlertConfig(
                telegram_token=self._config.telegram.bot_token,
                telegram_chat_ids=list(job_chat_ids),
            )
        return self._global_alert_config

    def _has_alert_config(self) -> bool:
        """Check if any alert transport is configured."""
        return bool(
            self._global_alert_config.telegram_token
            and self._global_alert_config.telegram_chat_ids
        )

    # =========================================================================
    # Helpers
    # =========================================================================

    def _build_tx_info(
        self, intent: TxIntent | None, attempt: TxAttempt | None
    ) -> TxInfo | None:
        """Build TxInfo from intent, enrich with attempt if available."""
        if intent is None:
            return None

        from brawny.jobs.base import TxInfo

        # Safe access for optional gas_params
        gp = getattr(attempt, "gas_params", None) if attempt else None

        return TxInfo(
            hash=attempt.tx_hash if attempt else None,
            nonce=attempt.nonce if attempt else None,
            from_address=intent.signer_address,
            to_address=intent.to_address,
            gas_limit=gp.gas_limit if gp else getattr(intent, "gas_limit", 0),
            max_fee_per_gas=gp.max_fee_per_gas if gp else getattr(intent, "max_fee_per_gas", 0),
            max_priority_fee_per_gas=gp.max_priority_fee_per_gas if gp else getattr(intent, "max_priority_fee_per_gas", 0),
        )

    def _build_alert_receipt(self, receipt: dict[str, Any]) -> TxReceipt:
        """Convert raw receipt dict to TxReceipt."""
        from brawny.jobs.base import TxReceipt

        tx_hash = receipt.get("transactionHash")
        if hasattr(tx_hash, "hex"):
            tx_hash = f"0x{tx_hash.hex()}"
        block_hash = receipt.get("blockHash")
        if hasattr(block_hash, "hex"):
            block_hash = f"0x{block_hash.hex()}"
        return TxReceipt(
            transaction_hash=tx_hash,
            block_number=receipt.get("blockNumber"),
            block_hash=block_hash,
            status=receipt.get("status", 1),
            gas_used=receipt.get("gasUsed", 0),
            logs=receipt.get("logs", []),
        )

    def _get_block_for_failed(
        self,
        attempt: TxAttempt | None,
        receipt: dict[str, Any] | None,
    ) -> AlertBlockInfo | None:
        """Determine block for failed alert. Explicit priority."""
        if receipt and "blockNumber" in receipt:
            return self._fetch_block(receipt["blockNumber"])
        if attempt and attempt.broadcast_block:
            return self._fetch_block(attempt.broadcast_block)
        return None

    def _fetch_block(self, block_number: int | None) -> AlertBlockInfo | None:
        """Fetch block info by number."""
        if block_number is None:
            return None
        try:
            block = self._rpc.get_block(block_number)
        except Exception:
            return None
        return self._to_alert_block(
            BlockInfo(
                chain_id=self._config.chain_id,
                block_number=block["number"],
                block_hash=f"0x{block['hash'].hex()}"
                if hasattr(block["hash"], "hex")
                else block["hash"],
                timestamp=block["timestamp"],
            )
        )

    def _model_block_from_number(self, block_number: int) -> BlockInfo | None:
        """Get BlockInfo model from block number."""
        try:
            block = self._rpc.get_block(block_number)
        except Exception:
            return None
        return BlockInfo(
            chain_id=self._config.chain_id,
            block_number=block["number"],
            block_hash=f"0x{block['hash'].hex()}"
            if hasattr(block["hash"], "hex")
            else block["hash"],
            timestamp=block["timestamp"],
        )

    def _to_alert_block(self, block: BlockInfo) -> AlertBlockInfo:
        """Convert model BlockInfo to alert BlockInfo."""
        from brawny.jobs.base import BlockInfo as AlertBlockInfo

        return AlertBlockInfo(
            number=block.block_number,
            hash=block.block_hash,
            timestamp=block.timestamp,
        )

    def _to_block_context(self, alert_block: AlertBlockInfo | None) -> BlockContext:
        """Convert alert BlockInfo to BlockContext."""
        if alert_block is None:
            # Default block context when no block available
            return BlockContext(
                number=0,
                timestamp=0,
                hash="0x0",
                base_fee=0,
                chain_id=self._config.chain_id,
            )
        return BlockContext(
            number=alert_block.number,
            timestamp=alert_block.timestamp,
            hash=alert_block.hash,
            base_fee=0,  # Not always available in alert context
            chain_id=self._config.chain_id,
        )

    def _decode_receipt_events(self, receipt: TxReceipt) -> list[DecodedEvent]:
        """Decode events from receipt using contract system."""
        if self._contract_system is None:
            return []

        try:
            from brawny.alerts.events import decode_logs

            event_dict = decode_logs(
                logs=receipt.logs,
                contract_system=self._contract_system,
            )
            # Convert EventDict to list[DecodedEvent]
            events: list[DecodedEvent] = []
            for event_name, event_item in event_dict.items():
                # event_item is _EventItem
                # Use getattr with fallbacks for robustness
                args_list = getattr(event_item, "_events", None) or []
                addr_list = getattr(event_item, "_addresses", None) or []
                pos_list = getattr(event_item, "pos", None) or []

                for i, args in enumerate(args_list):
                    address = addr_list[i] if i < len(addr_list) else ""
                    log_index = pos_list[i] if i < len(pos_list) else 0

                    events.append(
                        DecodedEvent.create(
                            address=address,
                            event_name=event_name,
                            args=args,
                            log_index=log_index,
                            tx_hash=receipt.transactionHash,
                            block_number=receipt.blockNumber,
                        )
                    )
            return events
        except Exception as e:
            logger.warning("events.decode_failed", error=str(e)[:200])
            return []
