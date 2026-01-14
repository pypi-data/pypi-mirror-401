"""Row to model mappers for database results.

Centralized conversion from database rows (dicts) to domain models.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from brawny.db.base_new import BlockState, BlockHashEntry, ABICacheEntry, ProxyCacheEntry
from brawny.model.types import (
    JobConfig,
    TxIntent,
    TxAttempt,
    SignerState,
    NonceReservation,
    GasParams,
)
from brawny.model.enums import IntentStatus, AttemptStatus, NonceStatus


def row_to_block_state(row: dict[str, Any]) -> BlockState:
    """Convert database row to BlockState."""
    return BlockState(
        chain_id=row["chain_id"],
        last_processed_block_number=row["last_processed_block_number"],
        last_processed_block_hash=row["last_processed_block_hash"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def row_to_block_hash_entry(row: dict[str, Any]) -> BlockHashEntry:
    """Convert database row to BlockHashEntry."""
    return BlockHashEntry(
        id=row["id"],
        chain_id=row["chain_id"],
        block_number=row["block_number"],
        block_hash=row["block_hash"],
        inserted_at=row["inserted_at"],
    )


def row_to_job_config(row: dict[str, Any]) -> JobConfig:
    """Convert database row to JobConfig."""
    return JobConfig(
        job_id=row["job_id"],
        job_name=row["job_name"],
        enabled=bool(row["enabled"]),
        check_interval_blocks=row["check_interval_blocks"],
        last_checked_block_number=row["last_checked_block_number"],
        last_triggered_block_number=row["last_triggered_block_number"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def row_to_signer_state(row: dict[str, Any]) -> SignerState:
    """Convert database row to SignerState."""
    return SignerState(
        chain_id=row["chain_id"],
        signer_address=row["signer_address"],
        next_nonce=row["next_nonce"],
        last_synced_chain_nonce=row["last_synced_chain_nonce"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        gap_started_at=row.get("gap_started_at"),
        alias=row.get("alias"),
    )


def row_to_nonce_reservation(row: dict[str, Any]) -> NonceReservation:
    """Convert database row to NonceReservation."""
    intent_id = row["intent_id"]
    # Handle string UUIDs (SQLite stores as string)
    if intent_id and isinstance(intent_id, str):
        intent_id = UUID(intent_id)
    return NonceReservation(
        id=row["id"],
        chain_id=row["chain_id"],
        signer_address=row["signer_address"],
        nonce=row["nonce"],
        status=NonceStatus(row["status"]),
        intent_id=intent_id,
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def row_to_intent(row: dict[str, Any]) -> TxIntent:
    """Convert database row to TxIntent."""
    intent_id = row["intent_id"]
    # Handle string UUIDs (SQLite stores as string)
    if isinstance(intent_id, str):
        intent_id = UUID(intent_id)

    # Parse metadata_json once at DB boundary
    metadata_json = row.get("metadata_json")
    metadata = json.loads(metadata_json) if metadata_json else {}

    return TxIntent(
        intent_id=intent_id,
        job_id=row["job_id"],
        chain_id=row["chain_id"],
        signer_address=row["signer_address"],
        idempotency_key=row["idempotency_key"],
        to_address=row["to_address"],
        data=row["data"],
        value_wei=row["value_wei"],
        gas_limit=row["gas_limit"],
        max_fee_per_gas=row["max_fee_per_gas"],
        max_priority_fee_per_gas=row["max_priority_fee_per_gas"],
        min_confirmations=row["min_confirmations"],
        deadline_ts=row["deadline_ts"],
        retry_after=row.get("retry_after"),
        retry_count=row.get("retry_count", 0),
        status=IntentStatus(row["status"]),
        claim_token=row["claim_token"],
        claimed_at=row["claimed_at"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        broadcast_group=row.get("broadcast_group"),
        broadcast_endpoints_json=row.get("broadcast_endpoints_json"),
        metadata=metadata,
    )


def row_to_attempt(row: dict[str, Any]) -> TxAttempt:
    """Convert database row to TxAttempt."""
    attempt_id = row["attempt_id"]
    intent_id = row["intent_id"]
    replaces_attempt_id = row.get("replaces_attempt_id")

    # Handle string UUIDs (SQLite stores as string)
    if isinstance(attempt_id, str):
        attempt_id = UUID(attempt_id)
    if isinstance(intent_id, str):
        intent_id = UUID(intent_id)
    if replaces_attempt_id and isinstance(replaces_attempt_id, str):
        replaces_attempt_id = UUID(replaces_attempt_id)

    return TxAttempt(
        attempt_id=attempt_id,
        intent_id=intent_id,
        nonce=row["nonce"],
        tx_hash=row["tx_hash"],
        gas_params=GasParams.from_json(row["gas_params_json"]),
        status=AttemptStatus(row["status"]),
        error_code=row.get("error_code"),
        error_detail=row.get("error_detail"),
        replaces_attempt_id=replaces_attempt_id,
        broadcast_block=row.get("broadcast_block"),
        broadcast_at=row.get("broadcast_at"),
        included_block=row.get("included_block"),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        broadcast_group=row.get("broadcast_group"),
        endpoint_url=row.get("endpoint_url"),
    )


def row_to_abi_cache(row: dict[str, Any]) -> ABICacheEntry:
    """Convert database row to ABICacheEntry."""
    return ABICacheEntry(
        chain_id=row["chain_id"],
        address=row["address"],
        abi_json=row["abi_json"],
        source=row["source"],
        resolved_at=row["resolved_at"],
    )


def row_to_proxy_cache(row: dict[str, Any]) -> ProxyCacheEntry:
    """Convert database row to ProxyCacheEntry."""
    return ProxyCacheEntry(
        chain_id=row["chain_id"],
        proxy_address=row["proxy_address"],
        implementation_address=row["implementation_address"],
        resolved_at=row["resolved_at"],
    )
