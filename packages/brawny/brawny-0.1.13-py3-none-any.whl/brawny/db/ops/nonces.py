"""Signer state and nonce reservation operations."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from brawny.db.base_new import Database
from brawny.db import queries as Q
from brawny.db import mappers as M
from brawny.model.types import SignerState, NonceReservation


# =============================================================================
# Signer State
# =============================================================================


def get_signer(db: Database, chain_id: int, address: str) -> SignerState | None:
    """Get signer state by chain and address."""
    row = db.fetch_one(Q.GET_SIGNER, {"chain_id": chain_id, "address": address.lower()})
    return M.row_to_signer_state(row) if row else None


def get_all_signers(db: Database, chain_id: int) -> list[SignerState]:
    """Get all signers for a chain."""
    rows = db.fetch_all(Q.LIST_SIGNERS, {"chain_id": chain_id})
    return [M.row_to_signer_state(row) for row in rows]


def upsert_signer(
    db: Database,
    chain_id: int,
    address: str,
    next_nonce: int,
    last_synced_chain_nonce: int,
) -> None:
    """Insert or update signer state."""
    db.execute(Q.UPSERT_SIGNER, {
        "chain_id": chain_id,
        "address": address.lower(),
        "next_nonce": next_nonce,
        "last_synced_chain_nonce": last_synced_chain_nonce,
    })


def update_signer_next_nonce(
    db: Database, chain_id: int, address: str, next_nonce: int
) -> bool:
    """Update signer's next nonce value."""
    count = db.execute_rowcount(Q.UPDATE_SIGNER_NEXT_NONCE, {
        "chain_id": chain_id,
        "address": address.lower(),
        "next_nonce": next_nonce,
    })
    return count > 0


def update_signer_chain_nonce(
    db: Database, chain_id: int, address: str, chain_nonce: int
) -> bool:
    """Update signer's last synced chain nonce."""
    count = db.execute_rowcount(Q.UPDATE_SIGNER_CHAIN_NONCE, {
        "chain_id": chain_id,
        "address": address.lower(),
        "chain_nonce": chain_nonce,
    })
    return count > 0


def set_gap_started_at(
    db: Database, chain_id: int, address: str, started_at: datetime
) -> bool:
    """Record when gap blocking started for a signer."""
    count = db.execute_rowcount(Q.SET_GAP_STARTED_AT, {
        "chain_id": chain_id,
        "address": address.lower(),
        "started_at": started_at,
    })
    return count > 0


def clear_gap_started_at(db: Database, chain_id: int, address: str) -> bool:
    """Clear gap blocking timestamp for a signer."""
    count = db.execute_rowcount(Q.CLEAR_GAP_STARTED_AT, {
        "chain_id": chain_id,
        "address": address.lower(),
    })
    return count > 0


def get_signer_by_alias(db: Database, chain_id: int, alias: str) -> SignerState | None:
    """Get signer by alias. Returns None if not found."""
    row = db.fetch_one(Q.GET_SIGNER_BY_ALIAS, {"chain_id": chain_id, "alias": alias})
    return M.row_to_signer_state(row) if row else None


# =============================================================================
# Nonce Reservations
# =============================================================================


def get_nonce_reservation(
    db: Database, chain_id: int, address: str, nonce: int
) -> NonceReservation | None:
    """Get nonce reservation by chain, address, and nonce."""
    row = db.fetch_one(Q.GET_NONCE_RESERVATION, {
        "chain_id": chain_id,
        "address": address.lower(),
        "nonce": nonce,
    })
    return M.row_to_nonce_reservation(row) if row else None


def get_reservations_for_signer(
    db: Database, chain_id: int, address: str, status: str | None = None
) -> list[NonceReservation]:
    """Get all reservations for a signer, optionally filtered by status."""
    if status:
        rows = db.fetch_all(Q.GET_RESERVATIONS_FOR_SIGNER_WITH_STATUS, {
            "chain_id": chain_id,
            "address": address.lower(),
            "status": status,
        })
    else:
        rows = db.fetch_all(Q.GET_RESERVATIONS_FOR_SIGNER, {
            "chain_id": chain_id,
            "address": address.lower(),
        })
    return [M.row_to_nonce_reservation(row) for row in rows]


def get_reservations_below_nonce(
    db: Database, chain_id: int, address: str, nonce: int
) -> list[NonceReservation]:
    """Get reservations below a certain nonce."""
    rows = db.fetch_all(Q.GET_RESERVATIONS_BELOW_NONCE, {
        "chain_id": chain_id,
        "address": address.lower(),
        "nonce": nonce,
    })
    return [M.row_to_nonce_reservation(row) for row in rows]


def get_non_released_reservations(
    db: Database,
    chain_id: int,
    address: str,
    base_nonce: int,
    released_status: str = "released",
) -> list[NonceReservation]:
    """Get non-released reservations at or above base_nonce."""
    rows = db.fetch_all(Q.GET_NON_RELEASED_RESERVATIONS, {
        "chain_id": chain_id,
        "address": address.lower(),
        "base_nonce": base_nonce,
        "released_status": released_status,
    })
    return [M.row_to_nonce_reservation(row) for row in rows]


def upsert_nonce_reservation(
    db: Database,
    chain_id: int,
    address: str,
    nonce: int,
    status: str,
    intent_id: UUID | None = None,
) -> None:
    """Create or update nonce reservation."""
    db.execute(Q.UPSERT_NONCE_RESERVATION, {
        "chain_id": chain_id,
        "address": address.lower(),
        "nonce": nonce,
        "status": status,
        "intent_id": str(intent_id) if intent_id else None,
    })


def update_nonce_reservation_status(
    db: Database,
    chain_id: int,
    address: str,
    nonce: int,
    status: str,
    intent_id: UUID | None = None,
) -> bool:
    """Update nonce reservation status, optionally setting intent_id."""
    if intent_id is not None:
        count = db.execute_rowcount(Q.UPDATE_NONCE_RESERVATION_STATUS_WITH_INTENT, {
            "chain_id": chain_id,
            "address": address.lower(),
            "nonce": nonce,
            "status": status,
            "intent_id": str(intent_id),
        })
    else:
        count = db.execute_rowcount(Q.UPDATE_NONCE_RESERVATION_STATUS, {
            "chain_id": chain_id,
            "address": address.lower(),
            "nonce": nonce,
            "status": status,
        })
    return count > 0


def release_nonce_reservation(
    db: Database, chain_id: int, address: str, nonce: int
) -> bool:
    """Release a nonce reservation (set status to released)."""
    return update_nonce_reservation_status(
        db, chain_id, address, nonce, status="released"
    )


def cleanup_orphaned_nonces(
    db: Database, chain_id: int, hours: int
) -> int:
    """Delete orphaned nonce reservations older than specified hours.

    Note: Uses dialect-specific query due to interval syntax differences.
    """
    query = Q.CLEANUP_ORPHANED_NONCES[db.dialect]
    if db.dialect == "sqlite":
        # SQLite uses datetime offset syntax
        params = {"chain_id": chain_id, "hours_offset": f"-{hours} hours"}
    else:
        # Postgres uses INTERVAL syntax
        params = {"chain_id": chain_id, "hours": hours}
    return db.execute_rowcount(query, params)


# =============================================================================
# Atomic Nonce Reservation
# =============================================================================


def reserve_nonce_atomic(
    db: Database,
    chain_id: int,
    address: str,
    chain_nonce: int | None,
    intent_id: UUID | None = None,
) -> int:
    """Reserve a nonce atomically using proper isolation.

    Uses SERIALIZABLE isolation on Postgres, BEGIN IMMEDIATE on SQLite.
    This is a dialect-specific operation that ensures atomic nonce reservation.

    Steps:
    1. Ensure signer row exists
    2. Lock the signer row (FOR UPDATE on Postgres)
    3. Find the next available nonce (skipping existing reservations)
    4. Create the reservation
    5. Update the signer's next_nonce

    Args:
        db: Database instance
        chain_id: The chain ID
        address: Signer address
        chain_nonce: Current on-chain nonce (from eth_getTransactionCount)
        intent_id: Optional intent ID to associate with reservation

    Returns:
        The reserved nonce

    Raises:
        DatabaseError: If reservation fails or no nonce available within 100 slots
    """
    from brawny.model.errors import DatabaseError

    address = address.lower()
    isolation = "SERIALIZABLE" if db.dialect == "postgres" else None

    with db.transaction(isolation_level=isolation):
        # 1. Ensure signer row exists
        db.execute(Q.ENSURE_SIGNER_EXISTS, {
            "chain_id": chain_id,
            "address": address,
        })

        # 2. Lock the signer row (FOR UPDATE on Postgres, no-op on SQLite)
        lock_query = Q.LOCK_SIGNER_FOR_UPDATE[db.dialect]
        row = db.fetch_one(lock_query, {
            "chain_id": chain_id,
            "address": address,
        })

        if row is None:
            raise DatabaseError("Failed to lock signer row")

        db_next_nonce = row["next_nonce"]
        base_nonce = max(db_next_nonce, chain_nonce or db_next_nonce)

        # 3. Get existing reservations to find gaps
        reservations = get_non_released_reservations(
            db, chain_id, address, base_nonce
        )

        # Find next available nonce (skip existing reservations)
        candidate = base_nonce
        for res in reservations:
            if res.nonce == candidate:
                candidate += 1
            elif res.nonce > candidate:
                break

        if candidate - base_nonce > 100:
            raise DatabaseError(
                f"Could not find available nonce within 100 slots for signer {address}"
            )

        # 4. Create the reservation
        upsert_nonce_reservation(
            db, chain_id, address, candidate, "reserved", intent_id
        )

        # 5. Update signer's next_nonce
        new_next_nonce = candidate + 1
        update_signer_next_nonce(db, chain_id, address, new_next_nonce)

        return candidate
