"""Transaction executor for signing, broadcasting, and monitoring transactions.

Implements the tx execution flow from SPEC 9:
1. Validate deadline
2. Reserve nonce
3. Build tx dict with gas estimation
4. Sign transaction
5. Broadcast transaction
6. Monitor for confirmation
7. Handle replacement for stuck txs

Golden Rule: Intents are persisted BEFORE signing - the executor only
works with already-persisted intents.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Callable
from uuid import UUID, uuid4

from web3 import Web3

from brawny.logging import LogEvents, get_logger
from brawny.tx.utils import normalize_tx_dict
from brawny.metrics import (
    ATTEMPT_WRITE_FAILURES,
    SIMULATION_NETWORK_ERRORS,
    SIMULATION_RETRIES,
    SIMULATION_REVERTED,
    TX_BROADCAST,
    TX_FAILED,
    INTENT_RETRY_ATTEMPTS,
    get_metrics,
)
from brawny.model.enums import AttemptStatus, IntentStatus
from brawny.model.errors import (
    DatabaseError,
    FailureStage,
    FailureType,
    SimulationNetworkError,
    SimulationReverted,
)
from brawny.model.types import GasParams, TxAttempt, TxIntent
from brawny._rpc.context import set_job_context as set_rpc_job_context, reset_job_context as reset_rpc_job_context
from brawny._rpc.errors import RPCError
from brawny.tx.nonce import NonceManager
from brawny.tx.intent import transition_intent
from brawny.utils import ensure_utc, utc_now

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny.db.base import Database
    from brawny.jobs.base import Job
    from brawny.keystore import Keystore
    from brawny.lifecycle import LifecycleDispatcher
    from brawny._rpc.manager import RPCManager

logger = get_logger(__name__)

# Simulation retry settings
MAX_SIMULATION_RETRIES = 2  # Total attempts = 3 (1 initial + 2 retries)


class ExecutionResult(str, Enum):
    """Result of transaction execution."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REVERTED = "reverted"
    DROPPED = "dropped"
    STUCK = "stuck"
    DEADLINE_EXPIRED = "deadline_expired"
    FAILED = "failed"
    BLOCKED = "blocked"  # Signer blocked by nonce gap


@dataclass
class ExecutionOutcome:
    """Outcome of executing an intent."""

    result: ExecutionResult
    intent: TxIntent
    attempt: TxAttempt | None
    tx_hash: str | None = None
    error: Exception | None = None
    block_number: int | None = None
    confirmations: int = 0


class TxExecutor:
    """Transaction executor with full lifecycle management.

    Handles:
    - Gas estimation (EIP-1559)
    - Nonce reservation via NonceManager
    - Transaction signing via Keystore
    - Broadcasting with retry
    - Confirmation monitoring
    - Stuck tx detection and replacement
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        keystore: Keystore,
        config: Config,
        lifecycle: "LifecycleDispatcher | None" = None,
        jobs: dict[str, "Job"] | None = None,
    ) -> None:
        """Initialize transaction executor.

        Args:
            db: Database connection
            rpc: RPC manager for chain operations
            keystore: Keystore for transaction signing
            config: Application configuration
            lifecycle: Optional lifecycle dispatcher for events
            jobs: Optional jobs registry for simulation hooks
        """
        self._db = db
        self._rpc = rpc
        self._keystore = keystore
        self._config = config
        self._nonce_manager = NonceManager(db, rpc, config.chain_id)
        self._lifecycle = lifecycle
        self._jobs = jobs
        self._chain_id = config.chain_id

    @property
    def nonce_manager(self) -> NonceManager:
        """Get the nonce manager."""
        return self._nonce_manager

    # =========================================================================
    # Nonce Gap Detection (Pre-flight check)
    # =========================================================================

    def _check_nonce_gap(
        self, signer_address: str
    ) -> tuple[bool, int | None, float | None]:
        """Check if signer is blocked by a nonce gap.

        Returns (is_blocked, oldest_in_flight_nonce, oldest_age_seconds).

        Checks both RESERVED and IN_FLIGHT records - a gap can exist with either.
        """
        from brawny.model.enums import NonceStatus

        chain_pending = self._rpc.get_transaction_count(signer_address, "pending")

        # Get all active reservations (RESERVED or IN_FLIGHT)
        active = self._nonce_manager.get_active_reservations(signer_address)

        if not active:
            # No reservations = no gap possible
            self._clear_gap_tracking(signer_address)
            return False, None, None

        # Find the lowest nonce we're tracking
        expected_next = min(r.nonce for r in active)

        if chain_pending >= expected_next:
            # No gap - chain has caught up or is ahead
            self._clear_gap_tracking(signer_address)
            return False, None, None

        # Gap exists: chain_pending < expected_next
        # Find oldest IN_FLIGHT for TxReplacer visibility
        from brawny.model.enums import NonceStatus
        in_flight = [r for r in active if r.status == NonceStatus.IN_FLIGHT]
        oldest_nonce = None
        oldest_age = None

        if in_flight:
            oldest = min(in_flight, key=lambda r: r.nonce)
            oldest_nonce = oldest.nonce
            oldest_age = (utc_now() - ensure_utc(oldest.created_at)).total_seconds()

        return True, oldest_nonce, oldest_age

    def _get_gap_duration(self, signer_address: str) -> float:
        """Get how long this signer has been blocked by a nonce gap (persisted in DB)."""
        signer_state = self._db.get_signer_state(self._chain_id, signer_address.lower())

        if signer_state is None:
            return 0.0

        if signer_state.gap_started_at is None:
            # First time seeing gap - record it
            self._db.set_gap_started_at(self._chain_id, signer_address.lower(), utc_now())
            return 0.0

        return (utc_now() - ensure_utc(signer_state.gap_started_at)).total_seconds()

    def _clear_gap_tracking(self, signer_address: str) -> None:
        """Clear gap tracking when gap is resolved or force_reset runs."""
        self._db.clear_gap_started_at(self._chain_id, signer_address.lower())

    def _alert_nonce_gap(
        self,
        signer_address: str,
        duration: float,
        oldest_nonce: int | None,
        oldest_age: float | None,
    ) -> None:
        """Alert on prolonged nonce gap (rate-limited per signer)."""
        if not self._lifecycle:
            return

        context = f"Signer {signer_address} blocked for {duration:.0f}s."
        if oldest_nonce is not None and oldest_age is not None:
            context += f" Oldest IN_FLIGHT: nonce {oldest_nonce} ({oldest_age:.0f}s old)."
        context += f" TxReplacer should recover, or run: brawny signer force-reset {signer_address}"

        self._lifecycle.alert(
            level="warning",
            title=f"Nonce gap blocking signer {signer_address[:10]}...",
            message=context,
        )

    def estimate_gas(
        self,
        intent: TxIntent,
        signer_address: str | None = None,
        to_address: str | None = None,
        job: "Job | None" = None,
    ) -> GasParams:
        """Estimate gas for a transaction intent.

        Uses EIP-1559 gas pricing with cached gas quotes.

        Args:
            intent: Transaction intent
            signer_address: Resolved signer address (optional, uses intent if not provided)
            to_address: Resolved to address (optional, uses intent if not provided)
            job: Job instance for gas overrides (optional)

        Returns:
            Estimated gas parameters

        Raises:
            RetriableExecutionError: If no cached gas quote available
        """
        from brawny.model.errors import RetriableExecutionError

        # Use resolved addresses if provided, otherwise fall back to intent
        from_addr = signer_address or intent.signer_address
        to_addr = to_address or intent.to_address

        # Gas limit
        if intent.gas_limit:
            gas_limit = intent.gas_limit
        else:
            try:
                tx_params = {
                    "from": from_addr,
                    "to": to_addr,
                    "value": int(intent.value_wei),
                }
                if intent.data:
                    tx_params["data"] = intent.data

                estimated = self._rpc.estimate_gas(tx_params)
                gas_limit = int(estimated * self._config.gas_limit_multiplier)
            except Exception as e:
                logger.warning(
                    "gas.estimate_failed",
                    intent_id=str(intent.intent_id),
                    error=str(e),
                )
                gas_limit = self._config.fallback_gas_limit

        # Resolve effective priority_fee (priority: intent > job > config)
        if intent.max_priority_fee_per_gas:
            priority_fee = int(intent.max_priority_fee_per_gas)
        elif job is not None and job.priority_fee is not None:
            priority_fee = int(job.priority_fee)
        else:
            priority_fee = int(self._config.priority_fee)

        # Gas price (EIP-1559)
        if intent.max_fee_per_gas:
            # Explicit in intent - use directly
            max_fee = int(intent.max_fee_per_gas)
        else:
            # Compute from quote (sync cache only)
            quote = self._rpc.gas_quote_sync()

            if quote is None:
                # No cached quote - raise retriable error (don't guess)
                # This should rarely happen (gas_ok warms cache)
                # NOTE: Executor must handle RetriableExecutionError with backoff,
                # not tight-loop retry. See intent_retry_backoff_seconds config.
                raise RetriableExecutionError("No gas quote available, will retry")

            computed_max_fee = int((2 * quote.base_fee) + priority_fee)

            # Apply cap if configured
            effective_max_fee = job.max_fee if job and job.max_fee is not None else self._config.max_fee

            if effective_max_fee is not None:
                max_fee = min(int(effective_max_fee), computed_max_fee)
            else:
                max_fee = computed_max_fee

        return GasParams(
            gas_limit=gas_limit,
            max_fee_per_gas=max_fee,
            max_priority_fee_per_gas=priority_fee,
        )

    def calculate_replacement_fees(self, old_params: GasParams) -> GasParams:
        """Calculate bumped fees for replacement transaction.

        Per Ethereum protocol, replacement must have at least 10% higher fees.
        Uses configured fee_bump_percent (default 15%).

        Args:
            old_params: Previous gas parameters

        Returns:
            New gas parameters with bumped fees
        """
        from brawny.tx.fees import bump_fees

        return bump_fees(
            old_params,
            bump_percent=self._config.fee_bump_percent,
            max_fee_cap=self._config.max_fee,
        )

    def execute(self, intent: TxIntent) -> ExecutionOutcome:
        """Execute a transaction intent.

        Full execution flow:
        1. Validate deadline
        2. Reserve nonce
        3. Estimate gas
        4. Build tx dict
        5. Simulate (unless job opts out)
        6. Sign transaction
        7. Broadcast

        Args:
            intent: Transaction intent to execute

        Returns:
            Execution outcome with result and details
        """
        def _retry_intent(reason: str) -> None:
            """Reset intent to created with exponential backoff, or abandon if max retries exceeded."""
            metrics = get_metrics()
            metrics.counter(INTENT_RETRY_ATTEMPTS).inc(
                chain_id=self._chain_id,
                reason=reason,
            )

            # Atomically increment retry count on intent row
            retry_count = self._db.increment_intent_retry_count(intent.intent_id)

            # Check if max retries exceeded
            if retry_count > self._config.max_executor_retries:
                logger.warning(
                    "intent.max_retries_exceeded",
                    intent_id=str(intent.intent_id),
                    retry_count=retry_count,
                    max_retries=self._config.max_executor_retries,
                    reason=reason,
                )
                transition_intent(
                    self._db,
                    intent.intent_id,
                    IntentStatus.ABANDONED,
                    "max_retries_exceeded",
                    chain_id=self._chain_id,
                )
                if self._lifecycle:
                    self._lifecycle.on_failed(
                        intent, None,
                        RuntimeError(f"Max executor retries ({self._config.max_executor_retries}) exceeded"),
                        failure_type=FailureType.UNKNOWN,
                        failure_stage=FailureStage.PRE_BROADCAST,
                    )
                return

            # Calculate exponential backoff with jitter
            if self._config.intent_retry_backoff_seconds > 0:
                base_backoff = self._config.intent_retry_backoff_seconds * (2 ** (retry_count - 1))
                jitter = random.uniform(0, min(base_backoff * 0.1, 10))  # 10% jitter, max 10s
                backoff_seconds = min(base_backoff + jitter, 300)  # Cap at 5 minutes
                retry_after = datetime.now(timezone.utc) + timedelta(seconds=backoff_seconds)
                self._db.set_intent_retry_after(intent.intent_id, retry_after)
                logger.info(
                    "intent.retry_scheduled",
                    intent_id=str(intent.intent_id),
                    job_id=intent.job_id,
                    retry_count=retry_count,
                    backoff_seconds=round(backoff_seconds, 1),
                    retry_after=retry_after.isoformat(),
                    reason=reason,
                )
            else:
                logger.info(
                    "intent.retry_scheduled",
                    intent_id=str(intent.intent_id),
                    job_id=intent.job_id,
                    retry_count=retry_count,
                    retry_after=None,
                    reason=reason,
                )

            # Transition to CREATED (auto-clears claim via transition_intent)
            if not transition_intent(
                self._db,
                intent.intent_id,
                IntentStatus.CREATED,
                reason,
                chain_id=self._chain_id,
            ):
                logger.warning(
                    "intent.retry_reset_failed",
                    intent_id=str(intent.intent_id),
                    reason=reason,
                )

        # Set RPC job context for metrics attribution
        rpc_ctx_token = set_rpc_job_context(intent.job_id)
        try:
            return self._execute_with_context(intent, _retry_intent)
        finally:
            reset_rpc_job_context(rpc_ctx_token)

    def _execute_with_context(
        self,
        intent: TxIntent,
        _retry_intent: Callable[[str], None],
    ) -> ExecutionOutcome:
        """Execute intent with RPC context already set (internal)."""
        # 0. Resolve signer alias to actual checksum address
        try:
            signer_address = self._keystore.get_address(intent.signer_address)
        except Exception as e:
            logger.error(
                "signer.resolution_failed",
                intent_id=str(intent.intent_id),
                signer=intent.signer_address,
                error=str(e),
            )
            if self._lifecycle:
                self._lifecycle.on_failed(
                    intent, None, e,
                    failure_type=FailureType.SIGNER_FAILED,
                    failure_stage=FailureStage.PRE_BROADCAST,
                    cleanup_trigger=False,
                )
            _retry_intent("signer_resolution_failed")
            return ExecutionOutcome(
                result=ExecutionResult.FAILED,
                intent=intent,
                attempt=None,
                error=e,
            )

        # Update intent with resolved signer address (so monitor can use it)
        if signer_address.lower() != intent.signer_address.lower():
            self._db.update_intent_signer(intent.intent_id, signer_address)
            logger.debug(
                "signer.resolved",
                intent_id=str(intent.intent_id),
                alias=intent.signer_address,
                address=signer_address,
            )

        # Ensure to_address is checksummed
        to_address = Web3.to_checksum_address(intent.to_address)

        # 1. Validate deadline
        if intent.deadline_ts:
            if datetime.now(timezone.utc) > intent.deadline_ts:
                transition_intent(
                    self._db,
                    intent.intent_id,
                    IntentStatus.ABANDONED,
                    "deadline_expired",
                    chain_id=self._chain_id,
                )
                if self._lifecycle:
                    self._lifecycle.on_failed(
                        intent,
                        None,
                        TimeoutError("Intent deadline expired"),
                        failure_type=FailureType.DEADLINE_EXPIRED,
                        failure_stage=FailureStage.PRE_BROADCAST,
                    )
                return ExecutionOutcome(
                    result=ExecutionResult.DEADLINE_EXPIRED,
                    intent=intent,
                    attempt=None,
                    error=TimeoutError("Intent deadline expired"),
                )

        # 1.5 Pre-flight gap check - don't reserve if signer is blocked
        try:
            is_blocked, oldest_nonce, oldest_age = self._check_nonce_gap(signer_address)
        except Exception as e:
            # Fail-safe: if we cannot validate nonce-gap safety, do NOT proceed
            logger.warning(
                "nonce.gap_check_failed",
                intent_id=str(intent.intent_id),
                signer=signer_address,
                error=str(e)[:100],
            )
            _retry_intent("nonce_gap_check_failed")
            return ExecutionOutcome(
                result=ExecutionResult.FAILED,
                intent=intent,
                attempt=None,
                error=e,
            )

        if is_blocked:
            gap_duration = self._get_gap_duration(signer_address)

            logger.warning(
                "nonce.gap_blocked",
                intent_id=str(intent.intent_id),
                job_id=intent.job_id,
                signer=signer_address,
                blocked_duration_seconds=gap_duration,
                oldest_in_flight_nonce=oldest_nonce,
                oldest_in_flight_age_seconds=oldest_age,
            )

            # Check config for unsafe reset mode
            if self._config.allow_unsafe_nonce_reset:
                logger.warning("nonce.unsafe_reset_triggered", signer=signer_address)
                self._nonce_manager.reconcile(signer_address)
                self._clear_gap_tracking(signer_address)
                # Fall through to normal execution
            else:
                # Alert if blocked too long
                if gap_duration > self._config.nonce_gap_alert_seconds:
                    self._alert_nonce_gap(signer_address, gap_duration, oldest_nonce, oldest_age)

                # Return BLOCKED - don't reserve, don't retry immediately
                # Let TxReplacer handle recovery via fee bumping
                return ExecutionOutcome(
                    result=ExecutionResult.BLOCKED,
                    intent=intent,
                    attempt=None,
                    error=RuntimeError(
                        f"Nonce gap detected for {signer_address}, waiting for TxReplacer"
                    ),
                )

        # 2. Reserve nonce
        try:
            nonce = self._nonce_manager.reserve_nonce(
                signer_address,
                intent_id=intent.intent_id,
            )
        except Exception as e:
            logger.error(
                "nonce.reservation_failed",
                intent_id=str(intent.intent_id),
                signer=signer_address,
                error=str(e),
            )
            if self._lifecycle:
                self._lifecycle.on_failed(
                    intent, None, e,
                    failure_type=FailureType.NONCE_FAILED,
                    failure_stage=FailureStage.PRE_BROADCAST,
                    cleanup_trigger=False,
                )
            _retry_intent("nonce_reservation_failed")
            return ExecutionOutcome(
                result=ExecutionResult.FAILED,
                intent=intent,
                attempt=None,
                error=e,
            )

        # NOTE: Gap detection moved to pre-flight check (step 1.5)
        # The pre-flight check returns BLOCKED if there's a nonce gap,
        # allowing TxReplacer to handle recovery instead of auto-abandoning.

        # 3. Estimate gas
        job = self._jobs.get(intent.job_id) if self._jobs else None
        try:
            gas_params = self.estimate_gas(intent, signer_address, to_address, job=job)
        except Exception as e:
            if "RetriableExecutionError" in type(e).__name__ or "No gas quote" in str(e):
                logger.warning(
                    "gas.no_quote_available",
                    intent_id=str(intent.intent_id),
                    job_id=intent.job_id,
                    error=str(e),
                )
                # Release nonce before retry
                self._nonce_manager.release(signer_address, nonce)
                _retry_intent("no_gas_quote")
                return ExecutionOutcome(
                    result=ExecutionResult.FAILED,
                    intent=intent,
                    attempt=None,
                    error=e,
                )
            raise

        # 4. Build tx dict for simulation
        tx_dict = self._build_tx_dict(intent, nonce, gas_params, to_address)
        tx_dict["from"] = signer_address  # Required for simulation

        # 5. Simulation step (runs unless job opts out)
        if job and not getattr(job, "disable_simulation", False):
            try:
                self._simulate_with_retry(job, intent, tx_dict)
            except (SimulationReverted, SimulationNetworkError) as e:
                # Release nonce on simulation failure
                self._nonce_manager.release(signer_address, nonce)
                return self._handle_simulation_failure(job, intent, e)

        # 6. Sign transaction (only if simulation passed)
        try:
            signed_tx = self._keystore.sign_transaction(
                tx_dict,
                signer_address,
            )
        except Exception as e:
            logger.error(
                "tx.sign_failed",
                intent_id=str(intent.intent_id),
                job_id=intent.job_id,
                error=str(e),
            )
            # Release nonce on sign failure
            self._nonce_manager.release(signer_address, nonce)
            if self._lifecycle:
                self._lifecycle.on_failed(
                    intent, None, e,
                    failure_type=FailureType.SIGN_FAILED,
                    failure_stage=FailureStage.PRE_BROADCAST,
                    cleanup_trigger=False,
                )
            _retry_intent("sign_failed")
            return ExecutionOutcome(
                result=ExecutionResult.FAILED,
                intent=intent,
                attempt=None,
                error=e,
            )

        # Warn if priority fee is suspiciously low (< 0.1 gwei)
        if gas_params.max_priority_fee_per_gas < 100_000_000:
            logger.warning(
                "gas.priority_fee_very_low",
                intent_id=str(intent.intent_id),
                job_id=intent.job_id,
                priority_fee_wei=gas_params.max_priority_fee_per_gas,
                priority_fee_gwei=gas_params.max_priority_fee_per_gas / 1e9,
                hint="Transaction may not be included - validators receive almost no tip",
            )

        logger.info(
            LogEvents.TX_SIGN,
            intent_id=str(intent.intent_id),
            job_id=intent.job_id,
            signer=signer_address,
            nonce=nonce,
            gas_limit=gas_params.gas_limit,
            max_fee=gas_params.max_fee_per_gas,
            priority_fee=gas_params.max_priority_fee_per_gas,
        )

        # 7. Broadcast with RPC group routing
        attempt: TxAttempt | None = None
        attempt_id = uuid4()
        tx_hash: str | None = None
        endpoint_url: str | None = None

        try:
            # Update intent status to sending
            if not transition_intent(
                self._db,
                intent.intent_id,
                IntentStatus.SENDING,
                "broadcast_start",
                chain_id=self._chain_id,
            ):
                raise RuntimeError("Intent status not claimable for sending")

            # Check for existing binding (for retry isolation)
            binding = self._db.get_broadcast_binding(intent.intent_id)
            job_id = job.job_id if job else None

            if binding is not None:
                # RETRY: Use persisted endpoints (NEVER current config)
                group_name, endpoints = binding
                is_first_broadcast = False

                # Advisory log if job's config changed
                if job:
                    from brawny.config.routing import resolve_job_groups

                    _, job_broadcast_group = resolve_job_groups(self._config, job)
                    if job_broadcast_group != group_name:
                        logger.warning(
                            "broadcast_group_mismatch",
                            intent_id=str(intent.intent_id),
                            job_id=job_id,
                            persisted_group=group_name,
                            current_job_group=job_broadcast_group,
                        )
            else:
                # FIRST BROADCAST: Resolve group + endpoints from config (no silent fallback)
                if job is None:
                    from brawny.config.routing import resolve_default_group

                    group_name = resolve_default_group(self._config)
                else:
                    from brawny.config.routing import resolve_job_groups

                    _, group_name = resolve_job_groups(self._config, job)
                endpoints = self._config.rpc_groups[group_name].endpoints

                is_first_broadcast = True

            # Broadcast transaction using RPC groups
            from brawny._rpc.broadcast import broadcast_transaction
            from brawny._rpc.errors import RPCGroupUnavailableError

            try:
                tx_hash, endpoint_url = broadcast_transaction(
                    raw_tx=signed_tx.raw_transaction,
                    endpoints=endpoints,
                    group_name=group_name,
                    config=self._config,
                    job_id=job_id,
                )
            except RPCGroupUnavailableError as e:
                logger.error(
                    "broadcast_unavailable",
                    intent_id=str(intent.intent_id),
                    job_id=job_id,
                    broadcast_group=group_name,
                    endpoints=endpoints,
                    error=str(e.last_error) if e.last_error else None,
                )
                raise

            # Create attempt record (+ binding if first broadcast)
            current_block = self._rpc.get_block_number()
            attempt = self._db.create_attempt(
                attempt_id=attempt_id,
                intent_id=intent.intent_id,
                nonce=nonce,
                gas_params_json=gas_params.to_json(),
                status=AttemptStatus.BROADCAST.value,
                tx_hash=tx_hash,
                broadcast_group=group_name,
                endpoint_url=endpoint_url,
                binding=(group_name, endpoints) if is_first_broadcast else None,
            )

            # Update attempt with broadcast block and time
            self._db.update_attempt_status(
                attempt_id,
                AttemptStatus.BROADCAST.value,
                broadcast_block=current_block,
                broadcast_at=datetime.now(timezone.utc),
            )

            # Mark nonce as in-flight
            self._nonce_manager.mark_in_flight(signer_address, nonce, intent.intent_id)

            # Update intent to pending
            if not transition_intent(
                self._db,
                intent.intent_id,
                IntentStatus.PENDING,
                "broadcast_complete",
                chain_id=self._chain_id,
            ):
                raise RuntimeError("Intent status not in sending state")

            logger.info(
                LogEvents.TX_BROADCAST,
                intent_id=str(intent.intent_id),
                job_id=intent.job_id,
                attempt_id=str(attempt_id),
                tx_hash=tx_hash,
                signer=signer_address,
                nonce=nonce,
                broadcast_group=group_name,
                endpoint_url=endpoint_url[:50] if endpoint_url else None,
            )
            metrics = get_metrics()
            metrics.counter(TX_BROADCAST).inc(
                chain_id=self._chain_id,
                job_id=intent.job_id,
            )

            # Refresh attempt
            attempt = self._db.get_attempt(attempt_id)
            if self._lifecycle and attempt is not None:
                self._lifecycle.on_submitted(intent, attempt)

        except (RPCError, DatabaseError, OSError, ValueError, RuntimeError) as e:
            # Expected broadcast-related errors - handle gracefully
            logger.error(
                "tx.broadcast_failed",
                intent_id=str(intent.intent_id),
                job_id=intent.job_id,
                attempt_id=str(attempt_id),
                error=str(e),
            )
            metrics = get_metrics()
            metrics.counter(TX_FAILED).inc(
                chain_id=self._chain_id,
                job_id=intent.job_id,
                reason="broadcast_failed",
            )

            # Create failed attempt record if we haven't yet
            if attempt is None:
                try:
                    attempt = self._db.create_attempt(
                        attempt_id=attempt_id,
                        intent_id=intent.intent_id,
                        nonce=nonce,
                        gas_params_json=gas_params.to_json(),
                        status=AttemptStatus.FAILED.value,
                    )
                except Exception as attempt_error:
                    # Never silently swallow - log with full context for reconstruction
                    # exc_info=True captures attempt_error traceback (current exception)
                    logger.error(
                        "attempt.write_failed",
                        intent_id=str(intent.intent_id),
                        nonce=nonce,
                        tx_hash=tx_hash if "tx_hash" in dir() else None,
                        original_error=str(e),
                        attempt_error=str(attempt_error),
                        attempt_error_type=type(attempt_error).__name__,
                        exc_info=True,
                    )
                    metrics.counter(ATTEMPT_WRITE_FAILURES).inc(stage="broadcast_failure")
                    # Continue with cleanup - attempt is None but we have logs

            if attempt is not None:
                self._db.update_attempt_status(
                    attempt_id,
                    AttemptStatus.FAILED.value,
                    error_code="broadcast_failed",
                    error_detail=str(e)[:500],
                )

            # Release nonce on broadcast failure
            self._nonce_manager.release(signer_address, nonce)

            if self._lifecycle:
                self._lifecycle.on_failed(
                    intent, attempt, e,
                    failure_type=FailureType.BROADCAST_FAILED,
                    failure_stage=FailureStage.BROADCAST,
                    cleanup_trigger=False,
                )
            _retry_intent("broadcast_failed")

            return ExecutionOutcome(
                result=ExecutionResult.FAILED,
                intent=intent,
                attempt=attempt,
                error=e,
            )

        return ExecutionOutcome(
            result=ExecutionResult.PENDING,
            intent=intent,
            attempt=attempt,
            tx_hash=tx_hash,
        )

    def _build_tx_dict(
        self,
        intent: TxIntent,
        nonce: int,
        gas_params: GasParams,
        to_address: str | None = None,
    ) -> dict:
        """Build transaction dictionary for signing.

        Args:
            intent: Transaction intent
            nonce: Nonce to use
            gas_params: Gas parameters
            to_address: Resolved to address (optional, uses intent if not provided)

        Returns:
            Transaction dictionary ready for signing
        """
        tx = {
            "nonce": nonce,
            "to": to_address or intent.to_address,
            "value": intent.value_wei,
            "gas": gas_params.gas_limit,
            "maxFeePerGas": gas_params.max_fee_per_gas,
            "maxPriorityFeePerGas": gas_params.max_priority_fee_per_gas,
            "chainId": intent.chain_id,
            "type": 2,  # EIP-1559
        }

        if intent.data:
            tx["data"] = intent.data

        return normalize_tx_dict(tx)

    # =========================================================================
    # Simulation
    # =========================================================================

    def _simulate_with_retry(
        self,
        job: "Job",
        intent: TxIntent,
        tx: dict,
    ) -> str:
        """Simulate transaction with retry on network errors.

        Args:
            job: Job instance for validation hook
            intent: Transaction intent
            tx: Transaction dict for simulation

        Returns:
            Hex-encoded output on success

        Raises:
            SimulationReverted: Permanent failure (no retry)
            SimulationNetworkError: After all retries exhausted
        """
        last_error: SimulationNetworkError | None = None

        # Resolve per-job RPC override (job.rpc overrides global)
        rpc_url = getattr(job, "rpc", None)

        for attempt in range(MAX_SIMULATION_RETRIES + 1):
            try:
                # Run simulation (uses job RPC if specified)
                output = self._rpc.simulate_transaction(tx, rpc_url=rpc_url)

                # Run job's custom validation (if defined)
                if hasattr(job, "validate_simulation"):
                    if not job.validate_simulation(output):
                        raise SimulationReverted("Job validation rejected")

                # Success
                if attempt > 0:
                    logger.info(
                        "simulation.retry_succeeded",
                        intent_id=str(intent.intent_id),
                        job_id=job.job_id,
                        attempt=attempt + 1,
                    )
                return output

            except SimulationReverted:
                # Permanent failure - don't retry
                raise

            except SimulationNetworkError as e:
                last_error = e
                metrics = get_metrics()

                # Log retry attempt
                if attempt < MAX_SIMULATION_RETRIES:
                    metrics.counter(SIMULATION_RETRIES).inc(
                        chain_id=intent.chain_id,
                        job_id=job.job_id,
                    )
                    logger.warning(
                        "simulation.network_error_retrying",
                        intent_id=str(intent.intent_id),
                        job_id=job.job_id,
                        attempt=attempt + 1,
                        max_attempts=MAX_SIMULATION_RETRIES + 1,
                        error=str(e),
                    )
                else:
                    metrics.counter(SIMULATION_NETWORK_ERRORS).inc(
                        chain_id=intent.chain_id,
                        job_id=job.job_id,
                    )
                    logger.error(
                        "simulation.network_error_exhausted",
                        intent_id=str(intent.intent_id),
                        job_id=job.job_id,
                        attempts=MAX_SIMULATION_RETRIES + 1,
                        error=str(e),
                    )

        # All retries exhausted
        if last_error is None:
            last_error = SimulationNetworkError("Unknown simulation error")
        raise last_error

    def _handle_simulation_failure(
        self,
        job: "Job",
        intent: TxIntent,
        error: SimulationReverted | SimulationNetworkError,
    ) -> ExecutionOutcome:
        """Handle simulation failure - mark intent failed and alert.

        Args:
            job: Job instance
            intent: Transaction intent
            error: Simulation error

        Returns:
            ExecutionOutcome with failure details
        """
        metrics = get_metrics()

        if isinstance(error, SimulationReverted):
            failure_message = f"Simulation reverted: {error.reason}"
            metrics.counter(SIMULATION_REVERTED).inc(
                chain_id=intent.chain_id,
                job_id=job.job_id,
            )
        else:
            failure_message = f"Simulation error: {error}"
            # Note: SIMULATION_NETWORK_ERRORS is already recorded in _simulate_with_retry

        logger.warning(
            "simulation.failed",
            intent_id=str(intent.intent_id),
            job_id=job.job_id,
            error=failure_message,
        )

        # Mark intent as failed in database (transition_intent auto-clears claim)
        transition_intent(
            self._db,
            intent.intent_id,
            IntentStatus.FAILED,
            "simulation_failed",
            chain_id=intent.chain_id,
        )

        # Fire alert
        if self._lifecycle:
            self._lifecycle.on_simulation_failed(job, intent, error)

        return ExecutionOutcome(
            result=ExecutionResult.FAILED,
            intent=intent,
            attempt=None,
            error=error,
        )

    # NOTE: _abandon_stranded_intents() has been removed as part of the
    # nonce policy simplification. Stranded intents are now recovered by
    # TxReplacer via fee bumping, rather than being auto-abandoned.
    # See NONCE.md for the new policy.
