"""Block state and hash history operations."""

from __future__ import annotations

from brawny.db.base_new import Database, BlockState
from brawny.db import queries as Q
from brawny.db import mappers as M


def get_block_state(db: Database, chain_id: int) -> BlockState | None:
    """Get the current block processing state."""
    row = db.fetch_one(Q.GET_BLOCK_STATE, {"chain_id": chain_id})
    return M.row_to_block_state(row) if row else None


def upsert_block_state(
    db: Database, chain_id: int, block_number: int, block_hash: str
) -> None:
    """Update or insert block processing state."""
    db.execute(Q.UPSERT_BLOCK_STATE, {
        "chain_id": chain_id,
        "block_number": block_number,
        "block_hash": block_hash,
    })


def get_block_hash_at_height(
    db: Database, chain_id: int, block_number: int
) -> str | None:
    """Get stored block hash at a specific height."""
    row = db.fetch_one(Q.GET_BLOCK_HASH_AT_HEIGHT, {
        "chain_id": chain_id,
        "block_number": block_number,
    })
    return row["block_hash"] if row else None


def insert_block_hash(
    db: Database, chain_id: int, block_number: int, block_hash: str
) -> None:
    """Insert a block hash into history."""
    db.execute(Q.INSERT_BLOCK_HASH, {
        "chain_id": chain_id,
        "block_number": block_number,
        "block_hash": block_hash,
    })


def delete_block_hashes_above(db: Database, chain_id: int, block_number: int) -> int:
    """Delete block hashes above a certain height (for reorg rewind)."""
    return db.execute_rowcount(Q.DELETE_BLOCK_HASHES_ABOVE, {
        "chain_id": chain_id,
        "block_number": block_number,
    })


def delete_block_hash_at_height(db: Database, chain_id: int, block_number: int) -> bool:
    """Delete a specific block hash (for stale hash cleanup)."""
    count = db.execute_rowcount(Q.DELETE_BLOCK_HASH_AT_HEIGHT, {
        "chain_id": chain_id,
        "block_number": block_number,
    })
    return count > 0


def cleanup_old_block_hashes(db: Database, chain_id: int, keep_count: int) -> int:
    """Delete old block hashes beyond the history window."""
    # Get max block number
    row = db.fetch_one(Q.GET_MAX_BLOCK_IN_HISTORY, {"chain_id": chain_id})
    if not row or row["max_block"] is None:
        return 0

    cutoff = row["max_block"] - keep_count
    return db.execute_rowcount(Q.DELETE_BLOCK_HASHES_BELOW, {
        "chain_id": chain_id,
        "cutoff": cutoff,
    })


def get_oldest_block_in_history(db: Database, chain_id: int) -> int | None:
    """Get the oldest block number in hash history."""
    row = db.fetch_one(Q.GET_OLDEST_BLOCK_IN_HISTORY, {"chain_id": chain_id})
    return row["min_block"] if row else None
