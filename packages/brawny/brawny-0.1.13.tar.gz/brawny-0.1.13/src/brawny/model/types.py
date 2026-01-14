"""Core data types and dataclasses for brawny."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

# JSON-serializable value type for metadata
JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]

# Hook names for type-safe dispatch
HookName = Literal["on_trigger", "on_success", "on_failure"]

from brawny.model.enums import AttemptStatus, IntentStatus, NonceStatus, TxStatus
from brawny.model.errors import FailureType


def to_wei(value: int | float | str) -> int:
    """Convert a value to wei as an integer.

    Safely handles:
    - int: returned as-is
    - float: converted if whole number (e.g., 1e18, 10e18)
    - str: parsed as int first, then as float if needed

    Note on float precision:
        Float64 can only exactly represent integers up to 2^53 (~9e15).
        Wei values (1e18+) exceed this, but common values like 1e18, 10e18,
        1.5e18 convert correctly. For guaranteed precision with unusual
        values, use integer strings: "10000000000000000001"

    Raises:
        ValueError: if value has a fractional part (can't have 0.5 wei)
        TypeError: if value is not int, float, or str

    Examples:
        >>> to_wei(1000000000000000000)
        1000000000000000000
        >>> to_wei(1e18)
        1000000000000000000
        >>> to_wei(10e18)
        10000000000000000000
        >>> to_wei("1000000000000000000")
        1000000000000000000
        >>> to_wei(1.5e18)  # 1.5 * 10^18 is a whole number of wei
        1500000000000000000
        >>> to_wei(1.5)  # Raises ValueError - can't have 0.5 wei
        ValueError: Wei value must be a whole number, got 1.5
    """
    if isinstance(value, int):
        return value

    if isinstance(value, str):
        value = value.strip()
        if not value:
            return 0
        # Try parsing as int first (handles "123", "-456")
        try:
            return int(value)
        except ValueError:
            pass
        # Try parsing as float (handles "1e18", "1.5e18")
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"Cannot parse '{value}' as a number")

    if not isinstance(value, float):
        raise TypeError(f"Expected int, float, or str, got {type(value).__name__}")

    if not math.isfinite(value):
        raise ValueError(f"Invalid wei value: {value} (must be finite)")

    # Check for fractional part using modulo
    # This correctly identifies 1.5 as fractional but 1.5e18 as whole
    remainder = value % 1
    if remainder != 0:
        raise ValueError(
            f"Wei value must be a whole number, got {value} "
            f"(fractional part: {remainder})"
        )

    return int(value)


@dataclass(frozen=True)
class BlockInfo:
    """Information about a specific block."""

    chain_id: int
    block_number: int
    block_hash: str
    timestamp: int

    def __post_init__(self) -> None:
        if not self.block_hash.startswith("0x"):
            object.__setattr__(self, "block_hash", f"0x{self.block_hash}")


@dataclass
class Trigger:
    """Result of a job check indicating action needed.

    Note: trigger.reason is auto-stamped into intent.metadata["reason"].
    Use intent(..., metadata={}) for per-intent context for alerts.
    """

    reason: str
    tx_required: bool = True
    idempotency_parts: list[str | int | bytes] = field(default_factory=list)


@dataclass
class TxIntentSpec:
    """Specification for creating a transaction intent."""

    signer_address: str
    to_address: str
    data: str | None = None
    value_wei: str = "0"
    gas_limit: int | None = None
    max_fee_per_gas: int | None = None
    max_priority_fee_per_gas: int | None = None
    min_confirmations: int = 1
    deadline_seconds: int | None = None
    metadata: dict[str, JSONValue] | None = None  # Per-intent context for alerts


@dataclass
class TxIntent:
    """Persisted transaction intent record."""

    intent_id: UUID
    job_id: str
    chain_id: int
    signer_address: str
    idempotency_key: str
    to_address: str
    data: str | None
    value_wei: str
    gas_limit: int | None
    max_fee_per_gas: str | None
    max_priority_fee_per_gas: str | None
    min_confirmations: int
    deadline_ts: datetime | None
    retry_after: datetime | None
    status: IntentStatus
    claim_token: str | None
    claimed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    retry_count: int = 0

    # Broadcast binding (set on first successful broadcast)
    # These fields preserve the privacy invariant: retries use the SAME endpoints
    broadcast_group: str | None = None
    broadcast_endpoints_json: str | None = None

    # Per-intent context for alerts (parsed dict, not JSON string)
    metadata: dict[str, JSONValue] = field(default_factory=dict)


@dataclass
class GasParams:
    """Gas parameters for a transaction."""

    gas_limit: int
    max_fee_per_gas: int
    max_priority_fee_per_gas: int

    def __post_init__(self) -> None:
        """Validate gas parameters are non-negative."""
        def _coerce_int(value: int | float | str) -> int:
            if isinstance(value, int):
                return value
            if isinstance(value, float):
                return int(value)
            if isinstance(value, str):
                try:
                    return int(value)
                except ValueError:
                    from decimal import Decimal

                    return int(Decimal(value))
            return int(value)

        self.gas_limit = _coerce_int(self.gas_limit)
        self.max_fee_per_gas = _coerce_int(self.max_fee_per_gas)
        self.max_priority_fee_per_gas = _coerce_int(self.max_priority_fee_per_gas)
        if self.gas_limit < 0:
            raise ValueError(f"gas_limit must be non-negative, got {self.gas_limit}")
        if self.max_fee_per_gas < 0:
            raise ValueError(f"max_fee_per_gas must be non-negative, got {self.max_fee_per_gas}")
        if self.max_priority_fee_per_gas < 0:
            raise ValueError(f"max_priority_fee_per_gas must be non-negative, got {self.max_priority_fee_per_gas}")

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps({
            "gas_limit": self.gas_limit,
            "max_fee_per_gas": str(self.max_fee_per_gas),
            "max_priority_fee_per_gas": str(self.max_priority_fee_per_gas),
        })

    @classmethod
    def from_json(cls, data: str) -> GasParams:
        """Deserialize from JSON string."""
        parsed = json.loads(data)
        return cls(
            gas_limit=parsed["gas_limit"],
            max_fee_per_gas=parsed["max_fee_per_gas"],
            max_priority_fee_per_gas=parsed["max_priority_fee_per_gas"],
        )


@dataclass
class TxAttempt:
    """Persisted transaction attempt record."""

    attempt_id: UUID
    intent_id: UUID
    nonce: int
    tx_hash: str | None
    gas_params: GasParams
    status: AttemptStatus
    error_code: str | None
    error_detail: str | None
    replaces_attempt_id: UUID | None
    broadcast_block: int | None
    broadcast_at: datetime | None
    included_block: int | None
    created_at: datetime
    updated_at: datetime

    # Audit trail (which group and endpoint were used for this attempt)
    broadcast_group: str | None = None
    endpoint_url: str | None = None


@dataclass
class BroadcastInfo:
    """Broadcast binding information (privacy invariant).

    Preserves which RPC group/endpoints were used for first broadcast.
    Retries MUST use the same endpoints to prevent privacy leaks.
    """

    group: str | None
    endpoints: list[str] | None

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps({
            "group": self.group,
            "endpoints": self.endpoints,
        })

    @classmethod
    def from_json(cls, data: str | None) -> "BroadcastInfo | None":
        """Deserialize from JSON string."""
        if data is None:
            return None
        parsed = json.loads(data)
        return cls(
            group=parsed.get("group"),
            endpoints=parsed.get("endpoints"),
        )


@dataclass
class TxHashRecord:
    """Record of a single broadcast attempt, stored in tx_hash_history JSON.

    This is append-only archival data for debugging and postmortems.
    NEVER query this in normal flows.
    """

    tx_hash: str
    nonce: int
    broadcast_at: str  # ISO timestamp
    broadcast_block: int | None
    gas_limit: int
    max_fee_per_gas: int
    max_priority_fee_per_gas: int
    reason: str  # "initial", "replacement", "fee_bump"
    outcome: str | None = None  # "confirmed", "replaced", "failed", None (pending)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON serialization."""
        return {
            "tx_hash": self.tx_hash,
            "nonce": self.nonce,
            "broadcast_at": self.broadcast_at,
            "broadcast_block": self.broadcast_block,
            "gas_limit": self.gas_limit,
            "max_fee_per_gas": self.max_fee_per_gas,
            "max_priority_fee_per_gas": self.max_priority_fee_per_gas,
            "reason": self.reason,
            "outcome": self.outcome,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TxHashRecord":
        """Create from dict."""
        return cls(
            tx_hash=data["tx_hash"],
            nonce=data["nonce"],
            broadcast_at=data["broadcast_at"],
            broadcast_block=data.get("broadcast_block"),
            gas_limit=data["gas_limit"],
            max_fee_per_gas=data["max_fee_per_gas"],
            max_priority_fee_per_gas=data["max_priority_fee_per_gas"],
            reason=data["reason"],
            outcome=data.get("outcome"),
        )


@dataclass
class Transaction:
    """Single model representing a job transaction through its full lifecycle.

    IMPORTANT: Transaction is the only durable execution model.
    Do not add attempt tables.

    This replaces the old TxIntent + TxAttempt dual model with a single
    row per transaction. Replacement history is preserved in tx_hash_history
    JSON field (append-only, for debugging only).
    """

    # Identity (queryable)
    tx_id: UUID  # Primary key
    job_id: str
    chain_id: int
    idempotency_key: str  # UNIQUE - prevents duplicates

    # Transaction payload (immutable after creation)
    signer_address: str
    to_address: str
    data: str | None
    value_wei: str
    min_confirmations: int
    deadline_ts: datetime | None

    # Current state (queryable)
    status: TxStatus  # CREATED → BROADCAST → CONFIRMED/FAILED
    failure_type: FailureType | None

    # Broadcast state (queryable)
    current_tx_hash: str | None  # Active tx hash being monitored
    current_nonce: int | None  # Nonce for current broadcast
    replacement_count: int  # 0 = first attempt, 1+ = replacements

    # Worker coordination (queryable)
    claim_token: str | None
    claimed_at: datetime | None

    # Confirmation (queryable)
    included_block: int | None
    confirmed_at: datetime | None

    # Audit (queryable)
    created_at: datetime
    updated_at: datetime

    # --- JSON BLOBS (rarely queried) ---

    # Gas params for current/next attempt
    gas_params_json: str | None = None  # {"gas_limit": N, "max_fee": N, "priority_fee": N}

    # Broadcast binding (privacy invariant)
    broadcast_info_json: str | None = None  # {"group": str, "endpoints": [...]}

    # Error details (debugging only)
    error_info_json: str | None = None  # ErrorInfo as JSON

    # Broadcast history (append-only, debugging only)
    tx_hash_history: str | None = None  # JSON array of TxHashRecord

    @property
    def gas_params(self) -> GasParams | None:
        """Get gas params from JSON."""
        if self.gas_params_json is None:
            return None
        return GasParams.from_json(self.gas_params_json)

    @property
    def broadcast_info(self) -> BroadcastInfo | None:
        """Get broadcast info from JSON."""
        return BroadcastInfo.from_json(self.broadcast_info_json)

    def get_hash_history(self) -> list[TxHashRecord]:
        """Get tx hash history from JSON. For debugging only."""
        if self.tx_hash_history is None:
            return []
        records = json.loads(self.tx_hash_history)
        return [TxHashRecord.from_dict(r) for r in records]


@dataclass
class NonceReservation:
    """Nonce reservation record."""

    id: int
    chain_id: int
    signer_address: str
    nonce: int
    status: NonceStatus
    intent_id: UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass
class SignerState:
    """Signer nonce tracking state."""

    chain_id: int
    signer_address: str
    next_nonce: int
    last_synced_chain_nonce: int | None
    created_at: datetime
    updated_at: datetime
    gap_started_at: datetime | None = None  # When nonce gap blocking started (for alerts)
    alias: str | None = None  # Optional human-readable alias


@dataclass
class JobConfig:
    """Job configuration from database."""

    job_id: str
    job_name: str
    enabled: bool
    check_interval_blocks: int
    last_checked_block_number: int | None
    last_triggered_block_number: int | None
    created_at: datetime
    updated_at: datetime


def idempotency_key(job_id: str, *parts: str | int | bytes) -> str:
    """
    Generate a stable, deterministic idempotency key.

    Format: {job_id}:{hash}

    Rules:
    - bytes are hex-encoded (lowercase, no 0x prefix)
    - ints are decimal string-encoded
    - dicts are sorted by key before serialization
    - hash is SHA256, truncated to 16 hex chars

    Example:
        >>> idempotency_key("vault_deposit", "0xabc...", 42)
        "vault_deposit:a1b2c3d4e5f6g7h8"
    """
    normalized_parts: list[str] = []

    for part in parts:
        if isinstance(part, bytes):
            normalized_parts.append(part.hex())
        elif isinstance(part, int):
            normalized_parts.append(str(part))
        elif isinstance(part, dict):
            normalized_parts.append(json.dumps(part, sort_keys=True, separators=(",", ":")))
        elif isinstance(part, str):
            # Remove 0x prefix if present for consistency
            if part.startswith("0x"):
                normalized_parts.append(part[2:].lower())
            else:
                normalized_parts.append(part)
        else:
            normalized_parts.append(str(part))

    combined = ":".join(normalized_parts)
    hash_bytes = hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]

    return f"{job_id}:{hash_bytes}"
