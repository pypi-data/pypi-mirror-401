"""Startup reconciliation helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from brawny.model.enums import IntentStatus
from brawny.reconciliation import reconcile_startup, ReconciliationStats
from brawny.tx.monitor import ConfirmationResult

if TYPE_CHECKING:
    from brawny.db.base import Database
    from brawny.tx.monitor import TxMonitor
    import structlog


def reconcile_pending_intents(
    db: Database,
    monitor: TxMonitor,
    chain_id: int,
    logger: "structlog.stdlib.BoundLogger",
) -> int:
    """Reconcile pending intents at startup."""
    pending_intents = db.get_intents_by_status(
        IntentStatus.PENDING.value,
        chain_id=chain_id,
    )
    reconciled = 0
    for intent in pending_intents:
        attempt = db.get_latest_attempt_for_intent(intent.intent_id)
        if not attempt or not attempt.tx_hash:
            continue
        status = monitor.check_confirmation(intent, attempt)
        if status.result == ConfirmationResult.CONFIRMED:
            monitor.handle_confirmed(intent, attempt, status)
            reconciled += 1
        elif status.result == ConfirmationResult.REVERTED:
            monitor.handle_reverted(intent, attempt, status)
            reconciled += 1
        elif status.result == ConfirmationResult.DROPPED:
            monitor.handle_dropped(intent, attempt)
            reconciled += 1

    if reconciled > 0:
        logger.info(
            "startup.reconcile_pending",
            reconciled=reconciled,
        )
    return reconciled


def run_startup_reconciliation(
    db: Database,
    chain_id: int,
    logger: "structlog.stdlib.BoundLogger",
) -> ReconciliationStats:
    """Run general state reconciliation at startup.

    This complements reconcile_pending_intents by handling:
    - Orphaned claims (status != claimed but claim_token set)
    - Orphaned nonces (reserved but intent is terminal)
    - Detecting pending intents without attempts
    - Detecting stale claims

    Args:
        db: Database connection
        chain_id: Chain ID to reconcile
        logger: Logger instance

    Returns:
        Statistics from the reconciliation run
    """
    logger.info("startup.reconciliation_starting", chain_id=chain_id)
    stats = reconcile_startup(db, chain_id)
    logger.info("startup.reconciliation_complete", chain_id=chain_id)
    return stats
