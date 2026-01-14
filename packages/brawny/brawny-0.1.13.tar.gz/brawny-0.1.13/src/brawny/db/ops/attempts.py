"""Transaction attempt operations."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from brawny.db.base_new import Database
from brawny.db import queries as Q
from brawny.db import mappers as M
from brawny.model.types import TxAttempt, GasParams


def create_attempt(
    db: Database,
    attempt_id: UUID,
    intent_id: UUID,
    nonce: int,
    tx_hash: str | None,
    gas_params: GasParams,
    status: str,
    broadcast_block: int | None = None,
    broadcast_at: datetime | None = None,
    broadcast_group: str | None = None,
    endpoint_url: str | None = None,
) -> TxAttempt | None:
    """Create a new transaction attempt."""
    row = db.fetch_one(Q.CREATE_ATTEMPT, {
        "attempt_id": str(attempt_id),
        "intent_id": str(intent_id),
        "nonce": nonce,
        "tx_hash": tx_hash,
        "gas_params_json": gas_params.to_json(),
        "status": status,
        "broadcast_block": broadcast_block,
        "broadcast_at": broadcast_at,
        "broadcast_group": broadcast_group,
        "endpoint_url": endpoint_url,
    })
    return M.row_to_attempt(row) if row else None


def get_attempt(db: Database, attempt_id: UUID) -> TxAttempt | None:
    """Get attempt by ID."""
    row = db.fetch_one(Q.GET_ATTEMPT, {"attempt_id": str(attempt_id)})
    return M.row_to_attempt(row) if row else None


def get_attempt_by_tx_hash(db: Database, tx_hash: str) -> TxAttempt | None:
    """Get attempt by transaction hash."""
    row = db.fetch_one(Q.GET_ATTEMPT_BY_TX_HASH, {"tx_hash": tx_hash})
    return M.row_to_attempt(row) if row else None


def get_attempts_for_intent(db: Database, intent_id: UUID) -> list[TxAttempt]:
    """Get all attempts for an intent, ordered by created_at DESC."""
    rows = db.fetch_all(Q.GET_ATTEMPTS_FOR_INTENT, {"intent_id": str(intent_id)})
    return [M.row_to_attempt(row) for row in rows]


def get_latest_attempt_for_intent(db: Database, intent_id: UUID) -> TxAttempt | None:
    """Get the most recent attempt for an intent."""
    row = db.fetch_one(Q.GET_LATEST_ATTEMPT_FOR_INTENT, {"intent_id": str(intent_id)})
    return M.row_to_attempt(row) if row else None


def update_attempt_status(db: Database, attempt_id: UUID, status: str) -> bool:
    """Update attempt status."""
    count = db.execute_rowcount(Q.UPDATE_ATTEMPT_STATUS, {
        "attempt_id": str(attempt_id),
        "status": status,
    })
    return count > 0


def update_attempt_included(
    db: Database, attempt_id: UUID, status: str, included_block: int
) -> bool:
    """Update attempt with inclusion info."""
    count = db.execute_rowcount(Q.UPDATE_ATTEMPT_INCLUDED, {
        "attempt_id": str(attempt_id),
        "status": status,
        "included_block": included_block,
    })
    return count > 0


def update_attempt_error(
    db: Database,
    attempt_id: UUID,
    status: str,
    error_code: str | None,
    error_detail: str | None,
) -> bool:
    """Update attempt with error info."""
    count = db.execute_rowcount(Q.UPDATE_ATTEMPT_ERROR, {
        "attempt_id": str(attempt_id),
        "status": status,
        "error_code": error_code,
        "error_detail": error_detail,
    })
    return count > 0


def get_pending_attempts(db: Database, chain_id: int) -> list[TxAttempt]:
    """Get pending attempts for a chain."""
    rows = db.fetch_all(Q.GET_PENDING_ATTEMPTS, {"chain_id": chain_id})
    return [M.row_to_attempt(row) for row in rows]
