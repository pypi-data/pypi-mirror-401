"""Transaction intent operations."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from uuid import UUID

from brawny.db.base_new import Database
from brawny.db import queries as Q
from brawny.db import mappers as M
from brawny.model.types import TxIntent, JSONValue
from brawny.model.enums import IntentStatus


def create_intent(
    db: Database,
    intent_id: UUID,
    job_id: str,
    chain_id: int,
    signer_address: str,
    idempotency_key: str,
    to_address: str,
    data: str | None,
    value_wei: str,
    gas_limit: int | None,
    max_fee_per_gas: str | None,
    max_priority_fee_per_gas: str | None,
    min_confirmations: int,
    deadline_ts: datetime | None,
    broadcast_group: str | None = None,
    broadcast_endpoints: list[str] | None = None,
    metadata: dict[str, JSONValue] | None = None,
) -> TxIntent | None:
    """Create a new transaction intent.

    Returns None if idempotency_key already exists (ON CONFLICT DO NOTHING).

    Args:
        metadata: Per-intent context for alerts. Must be JSON-serializable.
    """
    # Validate and serialize metadata
    metadata_json: str | None = None
    if metadata:
        try:
            metadata_json = json.dumps(metadata)
        except TypeError as e:
            raise ValueError(f"intent.metadata must be JSON-serializable: {e}")

    row = db.fetch_one(Q.CREATE_INTENT, {
        "intent_id": str(intent_id),
        "job_id": job_id,
        "chain_id": chain_id,
        "signer_address": signer_address,
        "idempotency_key": idempotency_key,
        "to_address": to_address,
        "data": data,
        "value_wei": value_wei,
        "gas_limit": gas_limit,
        "max_fee_per_gas": max_fee_per_gas,
        "max_priority_fee_per_gas": max_priority_fee_per_gas,
        "min_confirmations": min_confirmations,
        "deadline_ts": deadline_ts,
        "broadcast_group": broadcast_group,
        "broadcast_endpoints_json": json.dumps(broadcast_endpoints) if broadcast_endpoints else None,
        "metadata_json": metadata_json,
    })
    return M.row_to_intent(row) if row else None


def get_intent(db: Database, intent_id: UUID) -> TxIntent | None:
    """Get intent by ID."""
    row = db.fetch_one(Q.GET_INTENT, {"intent_id": str(intent_id)})
    return M.row_to_intent(row) if row else None


def get_intent_by_idempotency_key(
    db: Database,
    chain_id: int,
    signer_address: str,
    idempotency_key: str,
) -> TxIntent | None:
    """Get intent by idempotency key (scoped to chain and signer)."""
    row = db.fetch_one(Q.GET_INTENT_BY_IDEMPOTENCY_KEY, {
        "chain_id": chain_id,
        "signer_address": signer_address.lower(),
        "idempotency_key": idempotency_key,
    })
    return M.row_to_intent(row) if row else None


def claim_next_intent(
    db: Database,
    claim_token: str,
    claimed_by: str | None = None,
) -> TxIntent | None:
    """Claim the next available intent for processing.

    Uses dialect-specific query (FOR UPDATE SKIP LOCKED on Postgres).
    """
    query = Q.CLAIM_NEXT_INTENT[db.dialect]
    row = db.fetch_one(query, {"claim_token": claim_token, "claimed_by": claimed_by})
    return M.row_to_intent(row) if row else None


def update_intent_status(db: Database, intent_id: UUID, status: str) -> bool:
    """Update intent status."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_STATUS, {
        "intent_id": str(intent_id),
        "status": status,
    })
    return count > 0


def update_intent_to_sending(db: Database, intent_id: UUID, claim_token: str) -> bool:
    """Transition intent from claimed to sending (validates claim token)."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_TO_SENDING, {
        "intent_id": str(intent_id),
        "claim_token": claim_token,
    })
    return count > 0


def update_intent_to_pending(db: Database, intent_id: UUID) -> bool:
    """Transition intent to pending (broadcast successful)."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_TO_PENDING, {
        "intent_id": str(intent_id),
    })
    return count > 0


def update_intent_to_confirmed(db: Database, intent_id: UUID) -> bool:
    """Transition intent to confirmed."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_TO_CONFIRMED, {
        "intent_id": str(intent_id),
    })
    return count > 0


def update_intent_to_failed(db: Database, intent_id: UUID) -> bool:
    """Transition intent to failed."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_TO_FAILED, {
        "intent_id": str(intent_id),
    })
    return count > 0


def update_intent_to_reverted(db: Database, intent_id: UUID) -> bool:
    """Transition intent to reverted."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_TO_REVERTED, {
        "intent_id": str(intent_id),
    })
    return count > 0


def set_intent_retry_after(db: Database, intent_id: UUID, retry_after: datetime) -> bool:
    """Set retry_after and increment retry_count."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_RETRY_AFTER, {
        "intent_id": str(intent_id),
        "retry_after": retry_after,
    })
    return count > 0


def release_intent_claim(
    db: Database, intent_id: UUID, claim_token: str, retry_after: datetime | None = None
) -> bool:
    """Release a claimed intent back to created state."""
    count = db.execute_rowcount(Q.RELEASE_INTENT_CLAIM, {
        "intent_id": str(intent_id),
        "claim_token": claim_token,
        "retry_after": retry_after,
    })
    return count > 0


def update_intent_broadcast_binding(
    db: Database,
    intent_id: UUID,
    broadcast_group: str,
    broadcast_endpoints: list[str],
) -> bool:
    """Set the broadcast binding for an intent (RPC endpoints to use)."""
    count = db.execute_rowcount(Q.UPDATE_INTENT_BROADCAST_BINDING, {
        "intent_id": str(intent_id),
        "broadcast_group": broadcast_group,
        "broadcast_endpoints_json": json.dumps(broadcast_endpoints),
    })
    return count > 0


def get_intents_by_status(
    db: Database,
    status: str | list[str],
    chain_id: int | None = None,
    job_id: str | None = None,
    limit: int = 100,
) -> list[TxIntent]:
    """Get intents by status with optional filters."""
    if isinstance(status, str):
        status = [status]

    # Build query dynamically based on filters
    placeholders = ", ".join(f":status_{i}" for i in range(len(status)))
    query = f"SELECT * FROM tx_intents WHERE status IN ({placeholders})"
    params: dict[str, str | int] = {f"status_{i}": s for i, s in enumerate(status)}

    if chain_id is not None:
        query += " AND chain_id = :chain_id"
        params["chain_id"] = chain_id
    if job_id is not None:
        query += " AND job_id = :job_id"
        params["job_id"] = job_id

    query += " ORDER BY created_at ASC LIMIT :limit"
    params["limit"] = limit

    rows = db.fetch_all(query, params)
    return [M.row_to_intent(row) for row in rows]


def get_active_intent_count(db: Database, job_id: str, chain_id: int | None = None) -> int:
    """Get count of active (non-terminal) intents for a job."""
    statuses = [
        IntentStatus.CREATED.value,
        IntentStatus.CLAIMED.value,
        IntentStatus.SENDING.value,
        IntentStatus.PENDING.value,
    ]
    placeholders = ", ".join(f":status_{i}" for i in range(len(statuses)))
    query = f"SELECT COUNT(*) AS count FROM tx_intents WHERE status IN ({placeholders}) AND job_id = :job_id"
    params: dict[str, str | int] = {f"status_{i}": s for i, s in enumerate(statuses)}
    params["job_id"] = job_id

    if chain_id is not None:
        query += " AND chain_id = :chain_id"
        params["chain_id"] = chain_id

    row = db.fetch_one(query, params)
    return int(row["count"]) if row else 0


def get_pending_intent_count(db: Database, chain_id: int | None = None) -> int:
    """Get count of pending intents."""
    statuses = [
        IntentStatus.CREATED.value,
        IntentStatus.CLAIMED.value,
        IntentStatus.SENDING.value,
        IntentStatus.PENDING.value,
    ]
    placeholders = ", ".join(f":status_{i}" for i in range(len(statuses)))
    query = f"SELECT COUNT(*) AS count FROM tx_intents WHERE status IN ({placeholders})"
    params: dict[str, str | int] = {f"status_{i}": s for i, s in enumerate(statuses)}

    if chain_id is not None:
        query += " AND chain_id = :chain_id"
        params["chain_id"] = chain_id

    row = db.fetch_one(query, params)
    return int(row["count"]) if row else 0


def get_backing_off_intent_count(db: Database, chain_id: int | None = None) -> int:
    """Get count of intents in backoff."""
    query = "SELECT COUNT(*) AS count FROM tx_intents WHERE retry_after > CURRENT_TIMESTAMP"
    params: dict[str, int] = {}

    if chain_id is not None:
        query += " AND chain_id = :chain_id"
        params["chain_id"] = chain_id

    row = db.fetch_one(query, params)
    return int(row["count"]) if row else 0


def get_stuck_sending_intents(db: Database, cutoff_time: datetime) -> list[TxIntent]:
    """Get intents stuck in SENDING state."""
    rows = db.fetch_all(Q.GET_STUCK_SENDING_INTENTS, {"cutoff_time": cutoff_time})
    return [M.row_to_intent(row) for row in rows]


def get_stuck_pending_intents(db: Database, cutoff_time: datetime) -> list[TxIntent]:
    """Get intents stuck in PENDING state."""
    rows = db.fetch_all(Q.GET_STUCK_PENDING_INTENTS, {"cutoff_time": cutoff_time})
    return [M.row_to_intent(row) for row in rows]


def delete_old_confirmed_intents(db: Database, cutoff_time: datetime) -> int:
    """Delete old terminal intents."""
    return db.execute_rowcount(Q.DELETE_OLD_CONFIRMED_INTENTS, {"cutoff_time": cutoff_time})


def delete_abandoned_intents(db: Database, cutoff_time: datetime) -> int:
    """Delete old abandoned intents."""
    return db.execute_rowcount(Q.DELETE_ABANDONED_INTENTS, {"cutoff_time": cutoff_time})
