"""Transaction intent creation and management.

Implements durable intent model from SPEC 6:
- Idempotency via unique key constraint
- Create-or-get semantics for deduplication
- Intents are persisted BEFORE signing/sending

Golden Rule: Persist intent before signing/sending - this is non-negotiable.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from brawny.logging import LogEvents, get_logger
from brawny.metrics import INTENT_TRANSITIONS, get_metrics
from brawny.model.enums import IntentStatus
from brawny.model.types import TxIntent, TxIntentSpec, Trigger, idempotency_key

if TYPE_CHECKING:
    from brawny.db.base import Database

logger = get_logger(__name__)

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    IntentStatus.CREATED.value: {IntentStatus.CLAIMED.value, IntentStatus.SENDING.value},
    IntentStatus.CLAIMED.value: {
        IntentStatus.SENDING.value,
        IntentStatus.CREATED.value,
        IntentStatus.FAILED.value,
        IntentStatus.ABANDONED.value,
    },
    IntentStatus.SENDING.value: {
        IntentStatus.PENDING.value,
        IntentStatus.CREATED.value,
        IntentStatus.FAILED.value,
        IntentStatus.ABANDONED.value,
    },
    IntentStatus.PENDING.value: {
        IntentStatus.CONFIRMED.value,
        IntentStatus.FAILED.value,
        IntentStatus.ABANDONED.value,
    },
    IntentStatus.CONFIRMED.value: {IntentStatus.PENDING.value},  # reorg
    IntentStatus.FAILED.value: set(),      # terminal
    IntentStatus.ABANDONED.value: set(),   # terminal
}


def create_intent(
    db: Database,
    job_id: str,
    chain_id: int,
    spec: TxIntentSpec,
    idem_parts: list[str | int | bytes],
    broadcast_group: str | None = None,
    broadcast_endpoints: list[str] | None = None,
    trigger: Trigger | None = None,
) -> tuple[TxIntent, bool]:
    """Create a new transaction intent with idempotency.

    Implements create-or-get semantics:
    - If intent with same idempotency key exists, return it
    - Otherwise create new intent

    Args:
        db: Database connection
        job_id: Job that triggered this intent
        chain_id: Chain ID for the transaction
        spec: Transaction specification
        idem_parts: Parts to include in idempotency key
        trigger: Trigger that caused this intent (for metadata auto-merge)

    Returns:
        Tuple of (intent, is_new) where is_new is True if newly created
    """
    # Generate idempotency key from job_id and parts
    idem_key = idempotency_key(job_id, *idem_parts)

    # Check for existing intent (scoped to chain + signer)
    existing = db.get_intent_by_idempotency_key(
        chain_id=chain_id,
        signer_address=spec.signer_address.lower(),
        idempotency_key=idem_key,
    )
    if existing:
        logger.info(
            LogEvents.INTENT_DEDUPE,
            job_id=job_id,
            idempotency_key=idem_key,
            chain_id=chain_id,
            signer=spec.signer_address.lower(),
            existing_intent_id=str(existing.intent_id),
            existing_status=existing.status.value,
        )
        return existing, False

    # Calculate deadline if specified
    deadline_ts: datetime | None = None
    if spec.deadline_seconds:
        deadline_ts = datetime.now(timezone.utc) + timedelta(seconds=spec.deadline_seconds)

    # Generate new intent ID
    intent_id = uuid4()

    # Merge trigger.reason into metadata (job metadata wins on key collision)
    # This is immutable - don't mutate spec.metadata
    base = spec.metadata or {}
    if trigger:
        metadata = {"reason": trigger.reason, **base}
    else:
        metadata = base if base else None

    # Create intent in database
    intent = db.create_intent(
        intent_id=intent_id,
        job_id=job_id,
        chain_id=chain_id,
        signer_address=spec.signer_address.lower(),
        idempotency_key=idem_key,
        to_address=spec.to_address.lower(),
        data=spec.data,
        value_wei=spec.value_wei,
        gas_limit=spec.gas_limit,
        max_fee_per_gas=str(spec.max_fee_per_gas) if spec.max_fee_per_gas else None,
        max_priority_fee_per_gas=str(spec.max_priority_fee_per_gas) if spec.max_priority_fee_per_gas else None,
        min_confirmations=spec.min_confirmations,
        deadline_ts=deadline_ts,
        broadcast_group=broadcast_group,
        broadcast_endpoints=broadcast_endpoints,
        metadata=metadata,
    )

    if intent is None:
        # Race condition: another process created it between our check and insert
        # This is expected with idempotency - just get the existing one
        existing = db.get_intent_by_idempotency_key(
            chain_id=chain_id,
            signer_address=spec.signer_address.lower(),
            idempotency_key=idem_key,
        )
        if existing:
            logger.info(
                LogEvents.INTENT_DEDUPE,
                job_id=job_id,
                idempotency_key=idem_key,
                chain_id=chain_id,
                signer=spec.signer_address.lower(),
                existing_intent_id=str(existing.intent_id),
                note="race_condition",
            )
            return existing, False
        else:
            raise RuntimeError(f"Failed to create or find intent with key {idem_key}")

    logger.info(
        LogEvents.INTENT_CREATE,
        intent_id=str(intent.intent_id),
        job_id=job_id,
        idempotency_key=idem_key,
        signer=spec.signer_address,
        to=spec.to_address,
    )

    return intent, True


def get_or_create_intent(
    db: Database,
    job_id: str,
    chain_id: int,
    spec: TxIntentSpec,
    idem_parts: list[str | int | bytes],
    broadcast_group: str | None = None,
    broadcast_endpoints: list[str] | None = None,
) -> TxIntent:
    """Get existing intent by idempotency key or create new one.

    This is the primary API for jobs creating intents.
    Ensures exactly-once semantics via idempotency.

    Args:
        db: Database connection
        job_id: Job that triggered this intent
        chain_id: Chain ID for the transaction
        spec: Transaction specification
        idem_parts: Parts to include in idempotency key

    Returns:
        The intent (existing or newly created)
    """
    intent, _ = create_intent(
        db,
        job_id,
        chain_id,
        spec,
        idem_parts,
        broadcast_group=broadcast_group,
        broadcast_endpoints=broadcast_endpoints,
    )
    return intent


def claim_intent(
    db: Database,
    worker_id: str,
    claimed_by: str | None = None,
) -> TxIntent | None:
    """Claim the next available intent for processing.

    Uses FOR UPDATE SKIP LOCKED (PostgreSQL) or
    IMMEDIATE transaction locking (SQLite) to prevent
    multiple workers from claiming the same intent.

    Args:
        db: Database connection
        worker_id: Unique identifier for this worker

    Returns:
        Claimed intent or None if no intents available
    """
    # Generate unique claim token
    claim_token = f"{worker_id}_{uuid4().hex[:8]}"

    intent = db.claim_next_intent(claim_token, claimed_by=claimed_by)

    if intent:
        logger.info(
            LogEvents.INTENT_CLAIM,
            intent_id=str(intent.intent_id),
            job_id=intent.job_id,
            worker_id=worker_id,
            claim_token=claim_token,
        )

    return intent


def release_claim(db: Database, intent_id: UUID) -> bool:
    """Release an intent claim without processing.

    Use when a worker picks up an intent but cannot process it
    (e.g., during graceful shutdown).

    Args:
        db: Database connection
        intent_id: Intent to release

    Returns:
        True if released successfully
    """
    released = db.release_intent_claim(intent_id)

    if released:
        logger.info(
            LogEvents.INTENT_STATUS,
            intent_id=str(intent_id),
            status="created",
            action="claim_released",
        )

    return released


def update_status(
    db: Database,
    intent_id: UUID,
    status: IntentStatus,
) -> bool:
    """Update intent status.

    Args:
        db: Database connection
        intent_id: Intent to update
        status: New status

    Returns:
        True if updated successfully
    """
    updated = db.update_intent_status(intent_id, status.value)

    if updated:
        logger.info(
            LogEvents.INTENT_STATUS,
            intent_id=str(intent_id),
            status=status.value,
        )

    return updated


def transition_intent(
    db: Database,
    intent_id: UUID,
    to_status: IntentStatus,
    reason: str,
    chain_id: int | None = None,
) -> bool:
    """Transition an intent using the centralized transition map.

    Uses atomic transition that clears claim fields when leaving CLAIMED status.
    """
    allowed_from = [
        from_status
        for from_status, allowed in ALLOWED_TRANSITIONS.items()
        if to_status.value in allowed
    ]

    if not allowed_from:
        logger.error(
            "intent.transition.forbidden",
            intent_id=str(intent_id),
            to_status=to_status.value,
            reason=reason,
        )
        return False

    # Single atomic operation - DB handles claim clearing internally
    success, old_status = db.transition_intent_status(
        intent_id=intent_id,
        from_statuses=allowed_from,
        to_status=to_status.value,
    )

    if success:
        # Emit metrics with ACTUAL previous status
        metrics = get_metrics()
        metrics.counter(INTENT_TRANSITIONS).inc(
            chain_id=chain_id if chain_id is not None else "unknown",
            from_status=old_status if old_status else "unknown",
            to_status=to_status.value,
            reason=reason,
        )
        logger.info(
            "intent.transition",
            intent_id=str(intent_id),
            from_status=old_status,
            to_status=to_status.value,
            reason=reason,
        )
    else:
        logger.debug(
            "intent.transition.skipped",
            intent_id=str(intent_id),
            to_status=to_status.value,
            reason="status_mismatch",
        )

    return success


def abandon_intent(
    db: Database,
    intent_id: UUID,
    reason: str = "abandoned",
    chain_id: int | None = None,
) -> bool:
    """Mark an intent as abandoned.

    Delegates to transition_intent() for validated state transitions.

    Use when:
    - Deadline expired
    - Max replacement attempts exceeded
    - Manual intervention required

    Args:
        db: Database connection
        intent_id: Intent to abandon
        reason: Reason for abandonment
        chain_id: Chain ID for metrics

    Returns:
        True if abandoned successfully
    """
    return transition_intent(
        db, intent_id, IntentStatus.ABANDONED, reason, chain_id=chain_id
    )


def get_pending_for_signer(
    db: Database,
    chain_id: int,
    signer_address: str,
) -> list[TxIntent]:
    """Get all pending intents for a signer.

    Use for startup reconciliation to find in-flight transactions.

    Args:
        db: Database connection
        chain_id: Chain ID
        signer_address: Signer address

    Returns:
        List of pending intents
    """
    return db.get_pending_intents_for_signer(chain_id, signer_address.lower())


def revert_to_pending(
    db: Database,
    intent_id: UUID,
    chain_id: int | None = None,
) -> bool:
    """Revert a confirmed intent to pending status (for reorg handling).

    Delegates to transition_intent() for validated state transitions.
    Called when a confirmed intent's block is invalidated by a reorg.

    Args:
        db: Database connection
        intent_id: Intent to revert
        chain_id: Chain ID for metrics

    Returns:
        True if reverted successfully
    """
    return transition_intent(
        db, intent_id, IntentStatus.PENDING, "reorg_reverted", chain_id=chain_id
    )
