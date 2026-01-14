"""Startup reconciliation for detecting and repairing inconsistent state.

Phase 1 implementation: runs at startup only.
Phase 2 will add periodic reconciliation after metrics prove stability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from brawny.logging import get_logger
from brawny.metrics import get_metrics

if TYPE_CHECKING:
    from brawny.db.base import Database

logger = get_logger(__name__)


@dataclass
class ReconciliationStats:
    """Statistics from a reconciliation run."""

    orphaned_claims_cleared: int = 0
    orphaned_nonces_released: int = 0
    pending_without_attempts: int = 0
    stale_claims: int = 0


def reconcile_startup(db: Database, chain_id: int) -> ReconciliationStats:
    """Run reconciliation checks at startup.

    Repairs:
    - Orphaned claims (status != claimed but claim_token set, stale)
    - Orphaned nonces (reserved but intent is terminal and stale)

    Detects (logs only, no repair):
    - Pending intents without attempts (data integrity issue)
    - Stale claimed intents (worker may have crashed)

    Args:
        db: Database connection
        chain_id: Chain ID to reconcile

    Returns:
        Statistics from the reconciliation run
    """
    stats = ReconciliationStats()

    # Repair: clear orphaned claims (with time guard)
    stats.orphaned_claims_cleared = db.clear_orphaned_claims(
        chain_id, older_than_minutes=2
    )
    if stats.orphaned_claims_cleared > 0:
        logger.warning(
            "reconciliation.orphaned_claims_cleared",
            count=stats.orphaned_claims_cleared,
            chain_id=chain_id,
        )

    # Repair: release orphaned nonces (with time guard)
    stats.orphaned_nonces_released = db.release_orphaned_nonces(
        chain_id, older_than_minutes=5
    )
    if stats.orphaned_nonces_released > 0:
        logger.warning(
            "reconciliation.orphaned_nonces_released",
            count=stats.orphaned_nonces_released,
            chain_id=chain_id,
        )

    # Detect: pending without attempts (log only - needs investigation)
    stats.pending_without_attempts = db.count_pending_without_attempts(chain_id)
    if stats.pending_without_attempts > 0:
        logger.error(
            "reconciliation.pending_without_attempts",
            count=stats.pending_without_attempts,
            chain_id=chain_id,
            action="manual_investigation_required",
        )

    # Detect: stale claims (log only - may self-recover or need intervention)
    stats.stale_claims = db.count_stale_claims(chain_id, older_than_minutes=10)
    if stats.stale_claims > 0:
        logger.warning(
            "reconciliation.stale_claims",
            count=stats.stale_claims,
            chain_id=chain_id,
        )

    # Emit metrics
    metrics = get_metrics()
    metrics.gauge("brawny_reconciliation_orphaned_claims").set(
        stats.orphaned_claims_cleared, chain_id=chain_id
    )
    metrics.gauge("brawny_reconciliation_orphaned_nonces").set(
        stats.orphaned_nonces_released, chain_id=chain_id
    )
    metrics.gauge("brawny_reconciliation_pending_no_attempts").set(
        stats.pending_without_attempts, chain_id=chain_id
    )
    metrics.gauge("brawny_reconciliation_stale_claims").set(
        stats.stale_claims, chain_id=chain_id
    )

    logger.info("reconciliation.completed", **asdict(stats), chain_id=chain_id)
    return stats
