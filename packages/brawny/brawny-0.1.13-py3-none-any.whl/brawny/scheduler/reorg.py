"""Reorg detection and handling.

Implements reorg detection from SPEC 5.2:
- Maintain block_hash_history window
- Compare stored hash at anchor height with chain
- Binary search to find last matching height
- Rewind and reprocess on reorg detection
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Callable

from brawny.alerts.health import health_alert
from brawny.logging import LogEvents, get_logger
from brawny.metrics import REORGS_DETECTED, get_metrics
from brawny.model.enums import AttemptStatus, IntentStatus, NonceStatus
from brawny.tx.intent import transition_intent

if TYPE_CHECKING:
    from brawny.db.base import Database
    from brawny.lifecycle import LifecycleDispatcher
    from brawny._rpc.manager import RPCManager

logger = get_logger(__name__)


@dataclass
class ReorgResult:
    """Result of reorg detection."""

    reorg_detected: bool
    reorg_depth: int = 0
    last_good_height: int | None = None
    intents_reverted: int = 0
    attempts_reverted: int = 0
    rewind_reason: str | None = None
    anchor_height: int | None = None
    anchor_hash_db: str | None = None
    anchor_hash_chain: str | None = None
    history_min_height: int | None = None
    history_max_height: int | None = None
    finality_confirmations: int | None = None
    pause: bool = False
    last_processed: int | None = None


class ReorgDetector:
    """Reorg detector using block hash history comparison.

    Algorithm:
    1. Select anchor height (last_processed - reorg_depth)
    2. Compare stored hash at anchor to current chain hash
    3. If mismatch, binary search for last matching height
    4. Rewind state and handle affected intents
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        chain_id: int,
        reorg_depth: int = 32,
        block_hash_history_size: int = 256,
        finality_confirmations: int = 0,
        lifecycle: "LifecycleDispatcher | None" = None,
        deep_reorg_alert_enabled: bool = True,
        health_send_fn: Callable[..., None] | None = None,
        health_chat_id: str | None = None,
        health_cooldown: int = 1800,
    ) -> None:
        """Initialize reorg detector.

        Args:
            db: Database connection
            rpc: RPC manager
            chain_id: Chain ID
            reorg_depth: Blocks back to check for reorg
            block_hash_history_size: Size of hash history window
        """
        self._db = db
        self._rpc = rpc
        self._chain_id = chain_id
        self._reorg_depth = reorg_depth
        self._history_size = block_hash_history_size
        self._finality_confirmations = max(0, finality_confirmations)
        self._lifecycle = lifecycle
        self._deep_reorg_alert_enabled = deep_reorg_alert_enabled
        self._health_send_fn = health_send_fn
        self._health_chat_id = health_chat_id
        self._health_cooldown = health_cooldown

    def check(self, current_block: int) -> ReorgResult:
        """Check for reorg at the current block height.

        Args:
            current_block: Current block being processed

        Returns:
            ReorgResult with detection status
        """
        # Get block state
        block_state = self._db.get_block_state(self._chain_id)
        if block_state is None:
            return ReorgResult(reorg_detected=False)

        last_processed = block_state.last_processed_block_number
        history_min = self._db.get_oldest_block_in_history(self._chain_id)
        history_max = self._db.get_latest_block_in_history(self._chain_id)

        # Calculate anchor height
        anchor_height = max(0, last_processed - self._reorg_depth)

        # Get stored hash at anchor
        stored_hash = self._db.get_block_hash_at_height(self._chain_id, anchor_height)
        anchor_missing = False
        if stored_hash is None:
            # No history at anchor - check if we have any history
            if history_min is None:
                return ReorgResult(reorg_detected=False)
            if history_max is None or anchor_height > history_max:
                anchor_height = history_min
                stored_hash = self._db.get_block_hash_at_height(self._chain_id, anchor_height)
                if stored_hash is None:
                    return ReorgResult(reorg_detected=False)
                anchor_missing = True
            elif anchor_height >= history_min:
                # Expected history missing -> possible corruption
                logger.error(
                    "reorg.history_missing",
                    anchor_height=anchor_height,
                    history_min=history_min,
                )
                return ReorgResult(
                    reorg_detected=True,
                    reorg_depth=last_processed - history_min + 1,
                    last_good_height=None,
                    rewind_reason="deep_reorg",
                    anchor_height=anchor_height,
                    history_min_height=history_min,
                    history_max_height=history_max,
                    finality_confirmations=self._finality_confirmations,
                    pause=True,
                    last_processed=last_processed,
                )
            else:
                anchor_height = history_min
                stored_hash = self._db.get_block_hash_at_height(self._chain_id, anchor_height)
                if stored_hash is None:
                    return ReorgResult(reorg_detected=False)
                anchor_missing = True
        if not stored_hash.startswith("0x"):
            stored_hash = f"0x{stored_hash}"

        # Get current chain hash at anchor
        try:
            block = self._rpc.get_block(anchor_height)
            if block is None:
                return ReorgResult(reorg_detected=False)

            chain_hash = block.get("hash")
            if chain_hash is None:
                logger.warning(
                    "reorg.missing_block_hash",
                    block_number=anchor_height,
                )
                return ReorgResult(reorg_detected=False)
            if isinstance(chain_hash, bytes):
                chain_hash = chain_hash.hex()
            if not chain_hash.startswith("0x"):
                chain_hash = f"0x{chain_hash}"
        except Exception as e:
            logger.warning(
                "reorg.check_failed",
                anchor_height=anchor_height,
                error=str(e),
            )
            return ReorgResult(reorg_detected=False)

        # Compare hashes
        stored_normalized = stored_hash.lower()
        chain_normalized = chain_hash.lower()

        if stored_normalized == chain_normalized:
            # No reorg
            return ReorgResult(reorg_detected=False)

        # Reorg detected!
        rewind_reason = "missing_history" if anchor_missing else "anchor_mismatch"
        logger.warning(
            LogEvents.BLOCK_REORG_DETECTED,
            anchor_height=anchor_height,
            stored_hash=stored_hash[:18],
            chain_hash=chain_hash[:18],
        )
        metrics = get_metrics()
        metrics.counter(REORGS_DETECTED).inc(
            chain_id=self._chain_id,
        )

        # Find last good height via binary search
        last_good_height = self._find_last_good_height(anchor_height, last_processed)
        oldest = history_min
        if oldest is not None and last_good_height < oldest:
            finality_floor = max(0, last_processed - self._finality_confirmations)
            if anchor_missing and last_good_height < finality_floor:
                logger.error(
                    LogEvents.BLOCK_REORG_DEEP,
                    oldest_known=oldest,
                    history_size=self._history_size,
                )
                if self._lifecycle and self._deep_reorg_alert_enabled:
                    self._lifecycle.on_deep_reorg(oldest, self._history_size, last_processed)
                return ReorgResult(
                    reorg_detected=True,
                    reorg_depth=last_processed - (oldest - 1),
                    last_good_height=None,
                    rewind_reason="deep_reorg",
                    anchor_height=anchor_height,
                    anchor_hash_db=stored_hash,
                    anchor_hash_chain=chain_hash,
                    history_min_height=oldest,
                    history_max_height=history_max,
                    finality_confirmations=self._finality_confirmations,
                    pause=True,
                    last_processed=last_processed,
                )

            logger.warning(
                "reorg.insufficient_history",
                oldest_known=oldest,
                last_good_height=last_good_height,
                history_size=self._history_size,
            )
            last_good_height = oldest

        # Handle impossible state: mismatch at anchor but last_good >= anchor
        # This happens with sparse hash history - delete stale anchor hash
        if rewind_reason == "anchor_mismatch" and last_good_height >= anchor_height:
            logger.warning(
                "reorg.stale_hash_detected",
                anchor_height=anchor_height,
                last_good_height=last_good_height,
                stored_hash=stored_hash[:18],
                chain_hash=chain_hash[:18],
            )
            # Delete the stale hash at anchor and set last_good to anchor - 1
            self._db.delete_block_hash_at_height(self._chain_id, anchor_height)
            last_good_height = anchor_height - 1

        reorg_depth = last_processed - last_good_height

        logger.warning(
            LogEvents.BLOCK_REORG_REWIND,
            last_good_height=last_good_height,
            reorg_depth=reorg_depth,
        )

        return ReorgResult(
            reorg_detected=True,
            reorg_depth=reorg_depth,
            last_good_height=last_good_height,
            rewind_reason=rewind_reason,
            anchor_height=anchor_height,
            anchor_hash_db=stored_hash,
            anchor_hash_chain=chain_hash,
            history_min_height=history_min,
            history_max_height=history_max,
            finality_confirmations=self._finality_confirmations,
            last_processed=last_processed,
        )

    def _find_last_good_height(self, low: int, high: int) -> int:
        """Binary search to find last matching block height.

        Args:
            low: Lower bound (known bad)
            high: Upper bound (known bad)

        Returns:
            Last good block height
        """
        oldest = self._db.get_oldest_block_in_history(self._chain_id)
        if oldest is None:
            return low

        # Start from the known bad anchor and search forward
        # We need to find where the chain diverged
        left = max(oldest, low)
        right = high

        last_good = left - 1  # Assume nothing matches if search fails

        while left <= right:
            mid = (left + right) // 2

            stored = self._db.get_block_hash_at_height(self._chain_id, mid)
            if stored is None:
                # No history here, move right
                left = mid + 1
                continue

            try:
                block = self._rpc.get_block(mid)
                if block is None:
                    left = mid + 1
                    continue

                chain_hash = block["hash"]
                if isinstance(chain_hash, bytes):
                    chain_hash = chain_hash.hex()
                if not chain_hash.startswith("0x"):
                    chain_hash = f"0x{chain_hash}"
            except Exception:
                left = mid + 1
                continue

            if stored.lower() == chain_hash.lower():
                # Match - reorg is after this point
                last_good = mid
                left = mid + 1
            else:
                # Mismatch - reorg is at or before this point
                right = mid - 1

        return last_good
    def rewind(self, reorg_result: ReorgResult) -> ReorgResult:
        """Rewind state using the centralized recovery contract."""
        recovery = ReorgRecovery(
            db=self._db,
            rpc=self._rpc,
            chain_id=self._chain_id,
            lifecycle=self._lifecycle,
            finality_confirmations=self._finality_confirmations,
            health_send_fn=self._health_send_fn,
            health_chat_id=self._health_chat_id,
            health_cooldown=self._health_cooldown,
        )
        return recovery.rewind(reorg_result)

    def handle_deep_reorg(self) -> None:
        """Handle a reorg deeper than our history window.

        This is a critical situation - emit error and rewind to oldest known block.
        """
        oldest = self._db.get_oldest_block_in_history(self._chain_id)

        logger.error(
            LogEvents.BLOCK_REORG_DEEP,
            oldest_known=oldest,
            history_size=self._history_size,
        )

        if oldest is not None:
            recovery = ReorgRecovery(
                db=self._db,
                rpc=self._rpc,
                chain_id=self._chain_id,
                lifecycle=self._lifecycle,
                finality_confirmations=self._finality_confirmations,
                health_send_fn=self._health_send_fn,
                health_chat_id=self._health_chat_id,
                health_cooldown=self._health_cooldown,
            )
            recovery.rewind(
                ReorgResult(
                    reorg_detected=True,
                    reorg_depth=0,
                    last_good_height=oldest,
                    rewind_reason="deep_reorg",
                    history_min_height=oldest,
                    history_max_height=self._db.get_latest_block_in_history(self._chain_id),
                    finality_confirmations=self._finality_confirmations,
                )
            )


class ReorgRecovery:
    """Centralized reorg recovery contract.

    Preconditions:
      - caller holds poller lock
      - no concurrent monitor execution

    Postconditions:
      - last_processed_block <= to_height
      - no confirmed attempt exists above last_processed_block
      - nonce state consistent with attempts
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        chain_id: int,
        lifecycle: "LifecycleDispatcher | None" = None,
        finality_confirmations: int = 0,
        health_send_fn: Callable[..., None] | None = None,
        health_chat_id: str | None = None,
        health_cooldown: int = 1800,
    ) -> None:
        self._db = db
        self._rpc = rpc
        self._chain_id = chain_id
        self._lifecycle = lifecycle
        self._finality_confirmations = max(0, finality_confirmations)
        self._health_send_fn = health_send_fn
        self._health_chat_id = health_chat_id
        self._health_cooldown = health_cooldown

    def rewind(self, reorg_result: ReorgResult) -> ReorgResult:
        """Rewind state to the last good height."""
        to_height = reorg_result.last_good_height
        if to_height is None:
            return reorg_result

        block_state = self._db.get_block_state(self._chain_id)
        if block_state is None:
            raise RuntimeError("reorg.rewind_missing_block_state")
        last_processed = block_state.last_processed_block_number

        deleted_hashes = 0
        intents_reverted = 0
        attempts_reverted = 0
        rewind_hash = None

        if to_height == last_processed:
            reorg_result = replace(reorg_result, last_good_height=to_height)
            self._log_summary(
                reorg_result,
                last_processed_before=last_processed,
                last_processed_after=last_processed,
                deleted_hashes=0,
                intents_reverted=0,
                attempts_reverted=0,
            )
            return replace(
                reorg_result,
                intents_reverted=0,
                attempts_reverted=0,
            )

        try:
            with self._db.transaction():
                deleted_hashes = self._db.delete_block_hashes_above(self._chain_id, to_height)

                rewind_hash = self._db.get_block_hash_at_height(self._chain_id, to_height)
                if rewind_hash is None:
                    try:
                        block = self._rpc.get_block(to_height)
                        if block:
                            rewind_hash = block["hash"]
                            if isinstance(rewind_hash, bytes):
                                rewind_hash = rewind_hash.hex()
                    except Exception:
                        rewind_hash = None

                if rewind_hash is None:
                    logger.warning(
                        "reorg.rewind_hash_missing",
                        to_height=to_height,
                    )
                    rewind_hash = "0x0"

                self._db.upsert_block_state(self._chain_id, to_height, rewind_hash or "0x0")

                intents_reverted, attempts_reverted = self._revert_reorged_intents(to_height)
                self._assert_no_confirmed_above(to_height)
        except Exception as e:
            logger.error(
                "reorg.rewind_failed",
                to_height=to_height,
                error=str(e)[:200],
            )
            health_alert(
                component="brawny.scheduler.reorg",
                chain_id=self._chain_id,
                error=e,
                action="Reorg rewind failed; inspect DB state",
                db_dialect=self._db.dialect,
                send_fn=self._health_send_fn,
                health_chat_id=self._health_chat_id,
                cooldown_seconds=self._health_cooldown,
            )
            raise

        self._log_summary(
            reorg_result,
            last_processed_before=last_processed,
            last_processed_after=to_height,
            deleted_hashes=deleted_hashes,
            intents_reverted=intents_reverted,
            attempts_reverted=attempts_reverted,
        )

        return replace(
            reorg_result,
            reorg_detected=True,
            reorg_depth=max(0, last_processed - to_height),
            last_good_height=to_height,
            intents_reverted=intents_reverted,
            attempts_reverted=attempts_reverted,
            last_processed=last_processed,
        )

    def _revert_reorged_intents(self, to_height: int) -> tuple[int, int]:
        """Revert intents confirmed in blocks above the rewind height."""
        confirmed_intents = self._db.get_intents_by_status(
            IntentStatus.CONFIRMED.value,
            chain_id=self._chain_id,
        )

        intents_reverted = 0
        attempts_reverted = 0
        for intent in confirmed_intents:
            attempts = self._db.get_attempts_for_intent(intent.intent_id)
            if not attempts:
                continue

            confirmed_attempts = [
                a for a in attempts
                if a.status == AttemptStatus.CONFIRMED and a.included_block
                and a.included_block > to_height
            ]
            if not confirmed_attempts:
                continue

            attempt = max(confirmed_attempts, key=lambda a: a.included_block or 0)
            if attempt.included_block and attempt.included_block > to_height:
                transition_intent(
                    self._db,
                    intent.intent_id,
                    IntentStatus.PENDING,
                    "reorg_revert",
                    chain_id=self._chain_id,
                )

                self._db.update_attempt_status(
                    attempt.attempt_id,
                    AttemptStatus.PENDING.value,
                )
                attempts_reverted += 1
                try:
                    signer_address = intent.signer_address.lower()
                    reservation = self._db.get_nonce_reservation(
                        self._chain_id,
                        signer_address,
                        attempt.nonce,
                    )
                    if reservation is None:
                        self._db.create_nonce_reservation(
                            self._chain_id,
                            signer_address,
                            attempt.nonce,
                            status=NonceStatus.IN_FLIGHT.value,
                            intent_id=intent.intent_id,
                        )
                    else:
                        self._db.update_nonce_reservation_status(
                            self._chain_id,
                            signer_address,
                            attempt.nonce,
                            NonceStatus.IN_FLIGHT.value,
                            intent_id=intent.intent_id,
                        )
                except Exception as e:
                    logger.warning(
                        "reorg.nonce_reconcile_failed",
                        intent_id=str(intent.intent_id),
                        nonce=attempt.nonce,
                        error=str(e)[:200],
                    )

                if self._lifecycle:
                    self._lifecycle.on_reorged(intent, attempt, to_height)

                logger.warning(
                    LogEvents.INTENT_REORG,
                    intent_id=str(intent.intent_id),
                    attempt_id=str(attempt.attempt_id),
                    old_block=attempt.included_block,
                    reorg_height=to_height,
                )

                intents_reverted += 1

        return intents_reverted, attempts_reverted

    def _assert_no_confirmed_above(self, to_height: int) -> None:
        confirmed_intents = self._db.get_intents_by_status(
            IntentStatus.CONFIRMED.value,
            chain_id=self._chain_id,
        )
        for intent in confirmed_intents:
            attempts = self._db.get_attempts_for_intent(intent.intent_id)
            for attempt in attempts:
                if (
                    attempt.status == AttemptStatus.CONFIRMED
                    and attempt.included_block
                    and attempt.included_block > to_height
                ):
                    raise RuntimeError(
                        f"reorg.invariant_failed intent={intent.intent_id} included_block={attempt.included_block} to_height={to_height}"
                    )

    def _log_summary(
        self,
        reorg_result: ReorgResult,
        *,
        last_processed_before: int,
        last_processed_after: int,
        deleted_hashes: int,
        intents_reverted: int,
        attempts_reverted: int,
    ) -> None:
        logger.warning(
            "reorg.summary",
            last_processed_before=last_processed_before,
            last_processed_after=last_processed_after,
            anchor_height=reorg_result.anchor_height,
            last_good_height=reorg_result.last_good_height,
            anchor_hash_db=reorg_result.anchor_hash_db,
            anchor_hash_chain=reorg_result.anchor_hash_chain,
            history_min_height=reorg_result.history_min_height,
            history_max_height=reorg_result.history_max_height,
            intents_reverted=intents_reverted,
            attempts_reverted=attempts_reverted,
            deleted_hash_count=deleted_hashes,
            finality_confirmations=self._finality_confirmations,
            rewind_reason=reorg_result.rewind_reason,
        )
