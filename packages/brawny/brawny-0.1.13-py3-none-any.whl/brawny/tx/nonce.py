"""Centralized nonce manager for transaction execution.

Implements the nonce management strategy from SPEC 8:
- Reserve nonce with SERIALIZABLE isolation
- Nonce status transitions (reserved → in_flight → released/orphaned)
- Reconciliation loop for startup and periodic sync
- SQLite-specific locking for development

Jobs NEVER allocate or set nonces - the nonce manager owns all nonce operations.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator
from uuid import UUID

from web3 import Web3

from brawny.logging import LogEvents, get_logger
from brawny.model.enums import NonceStatus

if TYPE_CHECKING:
    from brawny.db.base import Database
    from brawny.model.types import NonceReservation
    from brawny._rpc.manager import RPCManager

logger = get_logger(__name__)


class NonceManager:
    """Centralized nonce manager for transaction execution.

    Provides atomic nonce reservation with database-backed persistence.
    Handles multiple in-flight nonces per signer to prevent global blocking.

    Thread-safe: Uses database transactions for concurrency control.
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        chain_id: int,
    ) -> None:
        """Initialize nonce manager.

        Args:
            db: Database connection
            rpc: RPC manager for chain state queries
            chain_id: Chain ID for nonce tracking
        """
        self._db = db
        self._rpc = rpc
        self._chain_id = chain_id

    def reserve_nonce(
        self,
        signer_address: str,
        intent_id: UUID | None = None,
    ) -> int:
        """Reserve the next available nonce for a signer.

        Algorithm:
        1. Lock signer row (or create if not exists)
        2. Fetch chain pending nonce
        3. Calculate base nonce as max(chain_nonce, db_next_nonce)
        4. Find next available nonce (skip existing reservations)
        5. Create reservation and update signer's next_nonce

        Args:
            signer_address: Ethereum address of the signer
            intent_id: Optional intent ID to associate with reservation

        Returns:
            The reserved nonce value

        Raises:
            Exception: If reservation fails
        """
        signer_address = signer_address.lower()

        try:
            chain_nonce = self._rpc.get_transaction_count(
                Web3.to_checksum_address(signer_address), block_identifier="pending"
            )
        except Exception as e:
            logger.warning(
                "nonce.chain_fetch_failed",
                signer=signer_address,
                error=str(e),
            )
            chain_nonce = None

        nonce = self._db.reserve_nonce_atomic(
            chain_id=self._chain_id,
            address=signer_address,
            chain_nonce=chain_nonce,
            intent_id=intent_id,
        )

        logger.debug(
            LogEvents.NONCE_RESERVE,
            signer=signer_address,
            nonce=nonce,
            chain_nonce=chain_nonce,
            intent_id=str(intent_id) if intent_id else None,
        )

        return nonce

    def mark_in_flight(
        self,
        signer_address: str,
        nonce: int,
        intent_id: UUID,
    ) -> bool:
        """Mark a nonce reservation as in-flight (after broadcast).

        Args:
            signer_address: Ethereum address of the signer
            nonce: The nonce value
            intent_id: Intent ID to associate

        Returns:
            True if updated successfully
        """
        signer_address = signer_address.lower()
        return self._db.update_nonce_reservation_status(
            chain_id=self._chain_id,
            address=signer_address,
            nonce=nonce,
            status=NonceStatus.IN_FLIGHT.value,
            intent_id=intent_id,
        )

    def release(
        self,
        signer_address: str,
        nonce: int,
    ) -> bool:
        """Release a nonce reservation (after confirm/fail/abandon).

        Args:
            signer_address: Ethereum address of the signer
            nonce: The nonce value

        Returns:
            True if released successfully
        """
        signer_address = signer_address.lower()
        return self._db.release_nonce_reservation(
            self._chain_id, signer_address, nonce
        )

    @contextmanager
    def reserved(
        self,
        signer_address: str,
        intent_id: UUID | None = None,
    ) -> Generator[int, None, None]:
        """Context manager for nonce reservation with automatic release on failure.

        Automatically releases the nonce if an exception occurs within the context.
        On success path, caller is responsible for calling mark_in_flight() to
        transition the nonce to in-flight status.

        Usage:
            with nonce_manager.reserved(signer) as nonce:
                # Build and sign transaction with nonce
                # If exception raised, nonce is automatically released

            # After context, caller should call mark_in_flight() on success

        Args:
            signer_address: Ethereum address of the signer
            intent_id: Optional intent ID to associate with reservation

        Yields:
            Reserved nonce value

        Raises:
            Exception: Re-raises any exception after releasing the nonce
        """
        signer_address = signer_address.lower()
        nonce = self.reserve_nonce(signer_address, intent_id)

        try:
            yield nonce
        except Exception:
            # Release nonce on any exception
            self.release(signer_address, nonce)
            logger.debug(
                "nonce.released_on_error",
                signer=signer_address,
                nonce=nonce,
            )
            raise

    def mark_orphaned(
        self,
        signer_address: str,
        nonce: int,
    ) -> bool:
        """Mark a nonce as orphaned (nonce used but no tx found).

        Args:
            signer_address: Ethereum address of the signer
            nonce: The nonce value

        Returns:
            True if updated successfully
        """
        signer_address = signer_address.lower()
        updated = self._db.update_nonce_reservation_status(
            chain_id=self._chain_id,
            address=signer_address,
            nonce=nonce,
            status=NonceStatus.ORPHANED.value,
        )
        if updated:
            logger.warning(
                LogEvents.NONCE_ORPHANED,
                signer=signer_address,
                nonce=nonce,
            )
        return updated

    def get_reservation(
        self,
        signer_address: str,
        nonce: int,
    ) -> NonceReservation | None:
        """Get a specific nonce reservation.

        Args:
            signer_address: Ethereum address of the signer
            nonce: The nonce value

        Returns:
            Reservation if found, None otherwise
        """
        return self._db.get_nonce_reservation(
            self._chain_id, signer_address.lower(), nonce
        )

    def get_active_reservations(
        self,
        signer_address: str,
    ) -> list[NonceReservation]:
        """Get all active (non-released) reservations for a signer.

        Args:
            signer_address: Ethereum address of the signer

        Returns:
            List of active reservations
        """
        all_reservations = self._db.get_reservations_for_signer(
            self._chain_id, signer_address.lower()
        )
        return [
            r for r in all_reservations
            if r.status not in (NonceStatus.RELEASED,)
        ]

    def reconcile(self, signer_address: str | None = None) -> dict[str, int]:
        """Reconcile nonce reservations with chain state.

        Run at startup and periodically to:
        - Reset next_nonce when gap detected (CRITICAL for recovery)
        - Update signer's synced chain nonce
        - Mark stale reservations as released or orphaned
        - Clean up confirmed/used nonces
        - Release gap reservations (nonces >= chain_nonce with no tx in mempool)

        Args:
            signer_address: Optional specific signer to reconcile.
                           If None, reconciles all signers.

        Returns:
            Dictionary with reconciliation stats
        """
        stats = {
            "signers_checked": 0,
            "nonces_released": 0,
            "nonces_orphaned": 0,
            "orphans_cleaned": 0,
            "next_nonce_reset": 0,
            "gap_reservations_released": 0,
        }

        if signer_address:
            signers = [self._db.get_signer_state(self._chain_id, signer_address.lower())]
            signers = [s for s in signers if s is not None]
        else:
            signers = self._db.get_all_signers(self._chain_id)

        for signer in signers:
            stats["signers_checked"] += 1

            try:
                # Get current chain nonce
                chain_nonce = self._rpc.get_transaction_count(
                    Web3.to_checksum_address(signer.signer_address), block_identifier="pending"
                )

                # Update signer's synced chain nonce
                self._db.update_signer_chain_nonce(
                    self._chain_id, signer.signer_address, chain_nonce
                )

                # CRITICAL FIX: Reset next_nonce when gap detected
                # Without this, reserve_nonce_atomic() keeps returning stale nonces
                if chain_nonce < signer.next_nonce:
                    gap_size = signer.next_nonce - chain_nonce
                    logger.warning(
                        "nonce.gap_reset",
                        signer=signer.signer_address,
                        old_next_nonce=signer.next_nonce,
                        chain_nonce=chain_nonce,
                        gap_size=gap_size,
                    )
                    self._db.update_signer_next_nonce(
                        self._chain_id, signer.signer_address, chain_nonce
                    )
                    stats["next_nonce_reset"] += 1

                    # Release all non-released reservations >= chain_nonce
                    # These are "gap" reservations whose txs are no longer in mempool
                    gap_reservations = self._db.get_reservations_for_signer(
                        self._chain_id, signer.signer_address
                    )
                    for reservation in gap_reservations:
                        if reservation.status == NonceStatus.RELEASED:
                            continue
                        if reservation.nonce >= chain_nonce:
                            # This reservation is in the gap - tx doesn't exist
                            self.release(signer.signer_address, reservation.nonce)
                            stats["gap_reservations_released"] += 1
                            logger.debug(
                                "nonce.gap_reservation_released",
                                signer=signer.signer_address,
                                nonce=reservation.nonce,
                                intent_id=str(reservation.intent_id) if reservation.intent_id else None,
                            )

                # Get stale reservations (nonce < chain_nonce)
                stale_reservations = self._db.get_reservations_below_nonce(
                    self._chain_id, signer.signer_address, chain_nonce
                )

                for reservation in stale_reservations:
                    if reservation.status == NonceStatus.RELEASED:
                        # Already released, skip
                        continue

                    if reservation.intent_id:
                        # Has associated intent - check if confirmed
                        attempt = self._db.get_latest_attempt_for_intent(
                            reservation.intent_id
                        )
                        if attempt and attempt.status.value == "confirmed":
                            # Confirmed - release the reservation
                            self.release(signer.signer_address, reservation.nonce)
                            stats["nonces_released"] += 1
                        else:
                            # Not confirmed but nonce is used - orphaned
                            self.mark_orphaned(signer.signer_address, reservation.nonce)
                            stats["nonces_orphaned"] += 1
                    else:
                        # No intent - just release
                        self.release(signer.signer_address, reservation.nonce)
                        stats["nonces_released"] += 1

                logger.info(
                    LogEvents.NONCE_RECONCILE,
                    signer=signer.signer_address,
                    chain_nonce=chain_nonce,
                    stale_count=len(stale_reservations),
                    next_nonce_was_reset=chain_nonce < signer.next_nonce,
                )

            except Exception as e:
                logger.error(
                    "nonce.reconcile.error",
                    signer=signer.signer_address,
                    error=str(e),
                )

        # Cleanup old orphaned reservations (24+ hours old)
        stats["orphans_cleaned"] = self.cleanup_orphaned()

        return stats

    def cleanup_orphaned(self, older_than_hours: int = 24) -> int:
        """Delete orphaned nonce reservations older than specified hours.

        Orphaned reservations occur when a nonce was used but no transaction
        was found on-chain. These are safe to delete after some time.

        Args:
            older_than_hours: Delete orphans older than this (default: 24h)

        Returns:
            Number of deleted reservations
        """
        deleted = self._db.cleanup_orphaned_nonces(self._chain_id, older_than_hours)
        if deleted > 0:
            logger.info(
                "nonce.orphans_cleaned",
                chain_id=self._chain_id,
                deleted=deleted,
                older_than_hours=older_than_hours,
            )
        return deleted

    def sync_from_chain(self, signer_address: str) -> int:
        """Sync signer state from chain and return current pending nonce.

        Use this during startup or after external transactions.

        Args:
            signer_address: Ethereum address of the signer

        Returns:
            Current pending nonce from chain
        """
        signer_address = signer_address.lower()
        chain_nonce = self._rpc.get_transaction_count(
            Web3.to_checksum_address(signer_address), block_identifier="pending"
        )

        # Upsert signer with chain nonce
        self._db.upsert_signer(
            chain_id=self._chain_id,
            address=signer_address,
            next_nonce=chain_nonce,
            last_synced_chain_nonce=chain_nonce,
        )

        logger.info(
            "nonce.synced_from_chain",
            signer=signer_address,
            chain_nonce=chain_nonce,
        )

        return chain_nonce

    def force_reset(self, signer_address: str) -> int:
        """Force reset nonce state to match chain. Returns new next_nonce.

        USE WITH CAUTION: May cause issues if dropped txs later mine.

        This will:
        - Query current chain pending nonce
        - Reset local next_nonce to match chain
        - Release all reservations with nonce >= chain_pending_nonce
        - Clear gap tracking

        Args:
            signer_address: Ethereum address of the signer

        Returns:
            The new next_nonce (equal to chain pending nonce)
        """
        signer_address = signer_address.lower()
        chain_nonce = self._rpc.get_transaction_count(
            Web3.to_checksum_address(signer_address), block_identifier="pending"
        )

        # Release all reservations at or above chain nonce
        reservations = self._db.get_reservations_for_signer(
            self._chain_id, signer_address
        )
        released_count = 0
        for r in reservations:
            if r.nonce >= chain_nonce and r.status in (
                NonceStatus.RESERVED,
                NonceStatus.IN_FLIGHT,
            ):
                self.release(signer_address, r.nonce)
                released_count += 1

        # Reset next_nonce
        self._db.update_signer_next_nonce(self._chain_id, signer_address, chain_nonce)

        # Clear gap tracking
        self._db.clear_gap_started_at(self._chain_id, signer_address)

        logger.warning(
            "nonce.force_reset",
            signer=signer_address,
            new_next_nonce=chain_nonce,
            released_reservations=released_count,
        )

        return chain_nonce
