"""PostgreSQL database implementation for brawny.

PostgreSQL is the production database. Features:
- Connection pooling
- SERIALIZABLE isolation for nonce reservation
- FOR UPDATE SKIP LOCKED for intent claiming
- Proper transaction management
"""

from __future__ import annotations

import json
import random
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator
from uuid import UUID

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from brawny.db.base import (
    ABICacheEntry,
    BlockState,
    Database,
    IsolationLevel,
    ProxyCacheEntry,
)
from brawny.db.circuit_breaker import DatabaseCircuitBreaker
from brawny.logging import get_logger
from brawny.model.enums import AttemptStatus, IntentStatus, NonceStatus, TxStatus
from brawny.model.errors import DatabaseError, ErrorInfo, FailureType
from brawny.model.types import (
    BroadcastInfo,
    GasParams,
    JobConfig,
    NonceReservation,
    SignerState,
    Transaction,
    TxAttempt,
    TxHashRecord,
    TxIntent,
)

logger = get_logger(__name__)

# Constants for serialization retry
SERIALIZATION_FAILURE_SQLSTATE = "40001"
MAX_SERIALIZATION_RETRIES = 5
BASE_RETRY_DELAY_MS = 10.0
MAX_RETRY_DELAY_MS = 500.0


def _is_serialization_failure(e: Exception) -> bool:
    """Check if exception is a PostgreSQL serialization failure.

    Walks the exception cause chain to find SQLSTATE 40001.
    """
    for _ in range(3):  # Max depth to prevent infinite loops
        if hasattr(e, "pgcode") and e.pgcode == SERIALIZATION_FAILURE_SQLSTATE:
            return True
        if hasattr(e, "sqlstate") and e.sqlstate == SERIALIZATION_FAILURE_SQLSTATE:
            return True
        if hasattr(e, "__cause__") and e.__cause__ is not None:
            e = e.__cause__
        else:
            break
    return False


def _convert_named_params(query: str, params: dict[str, Any]) -> tuple[str, tuple[Any, ...]]:
    """Convert :name placeholder query to %s positional params for psycopg.

    Args:
        query: SQL query with :name placeholders
        params: Dict of parameter values

    Returns:
        Tuple of (converted_query, positional_params)
    """
    import re
    # Find all :name placeholders (not ::type casts)
    # (?<!:) ensures we don't match the second colon in ::
    pattern = r'(?<!:):([a-zA-Z_][a-zA-Z0-9_]*)(?![a-zA-Z0-9_:])'
    matches = list(re.finditer(pattern, query))

    if not matches:
        return query, ()

    # Build positional params in order of appearance
    positional_params = []
    converted_query = query
    # Process in reverse to maintain string indices
    for match in reversed(matches):
        param_name = match.group(1)
        if param_name not in params:
            raise DatabaseError(f"Missing parameter: {param_name}")
        positional_params.insert(0, params[param_name])
        converted_query = converted_query[:match.start()] + "%s" + converted_query[match.end():]

    return converted_query, tuple(positional_params)


class PostgresDatabase(Database):
    """PostgreSQL implementation of the Database interface.

    Uses psycopg with a synchronous connection pool to avoid
    event-loop conflicts across threads.
    """

    def __init__(
        self,
        database_url: str,
        pool_size: int = 5,
        pool_max_overflow: int = 10,
        pool_timeout: float = 30.0,
        circuit_breaker_failures: int = 5,
        circuit_breaker_seconds: int = 30,
    ) -> None:
        """Initialize PostgreSQL database.

        Args:
            database_url: PostgreSQL connection URL
            pool_size: Minimum pool connections
            pool_max_overflow: Maximum additional connections
            pool_timeout: Connection acquisition timeout
        """
        self._database_url = database_url
        self._pool_size = pool_size
        self._pool_max_size = pool_size + pool_max_overflow
        self._pool_timeout = pool_timeout
        self._pool: ConnectionPool | None = None
        self._isolation_level: IsolationLevel | None = None
        self._local = threading.local()
        self._circuit_breaker = DatabaseCircuitBreaker(
            failure_threshold=circuit_breaker_failures,
            open_seconds=circuit_breaker_seconds,
            backend="postgres",
        )

    @property
    def dialect(self) -> str:
        """Return dialect name for query selection."""
        return "postgres"

    def connect(self) -> None:
        """Establish database connection pool."""
        if self._pool is not None:
            return
        self._pool = ConnectionPool(
            self._database_url,
            min_size=self._pool_size,
            max_size=self._pool_max_size,
            timeout=self._pool_timeout,
        )

    def close(self) -> None:
        """Close database connection pool."""
        if self._pool:
            self._pool.close()
            self._pool = None

    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._pool is not None

    def _ensure_pool(self) -> ConnectionPool:
        """Ensure pool exists and return it."""
        if self._pool is None:
            raise DatabaseError("Database not connected. Call connect() first.")
        return self._pool

    def _get_current_conn(self) -> psycopg.Connection | None:
        return getattr(self._local, "conn", None)

    @contextmanager
    def transaction(
        self, isolation_level: IsolationLevel | None = None
    ) -> Iterator[None]:
        """Context manager for database transactions."""
        if self._get_current_conn() is not None:
            raise DatabaseError("Nested transactions are not supported in PostgresDatabase.")

        pool = self._ensure_pool()
        with pool.connection() as conn:
            conn.row_factory = dict_row
            with conn.transaction():
                if isolation_level:
                    conn.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                self._local.conn = conn
                try:
                    yield
                finally:
                    self._local.conn = None

    def _execute(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> None:
        """Execute a query without returning results."""
        self._circuit_breaker.before_call()
        conn = self._get_current_conn()
        try:
            if conn is not None:
                conn.execute(query, params or ())
                self._circuit_breaker.record_success()
                return

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    if self._isolation_level:
                        conn.execute(f"SET TRANSACTION ISOLATION LEVEL {self._isolation_level}")
                    conn.execute(query, params or ())
            self._circuit_breaker.record_success()
        except psycopg.Error as e:
            self._circuit_breaker.record_failure(e)
            raise DatabaseError(f"Postgres query failed: {e}") from e

    def _fetch_all(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a query and return all results."""
        self._circuit_breaker.before_call()
        conn = self._get_current_conn()
        try:
            if conn is not None:
                result = conn.execute(query, params or ()).fetchall()
                self._circuit_breaker.record_success()
                return result

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    if self._isolation_level:
                        conn.execute(f"SET TRANSACTION ISOLATION LEVEL {self._isolation_level}")
                    result = conn.execute(query, params or ()).fetchall()
            self._circuit_breaker.record_success()
            return result
        except psycopg.Error as e:
            self._circuit_breaker.record_failure(e)
            raise DatabaseError(f"Postgres query failed: {e}") from e

    def _fetch_one(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> dict[str, Any] | None:
        """Execute a query and return a single result."""
        self._circuit_breaker.before_call()
        conn = self._get_current_conn()
        try:
            if conn is not None:
                result = conn.execute(query, params or ()).fetchone()
                self._circuit_breaker.record_success()
                return result

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    if self._isolation_level:
                        conn.execute(f"SET TRANSACTION ISOLATION LEVEL {self._isolation_level}")
                    result = conn.execute(query, params or ()).fetchone()
            self._circuit_breaker.record_success()
            return result
        except psycopg.Error as e:
            self._circuit_breaker.record_failure(e)
            raise DatabaseError(f"Postgres query failed: {e}") from e

    def execute(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> None:
        """Execute a query without returning results."""
        if isinstance(params, dict):
            query, params = _convert_named_params(query, params)
        self._execute(query, params)

    def execute_returning(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a query and return all results as dicts."""
        if isinstance(params, dict):
            query, params = _convert_named_params(query, params)
        return self._fetch_all(query, params)

    def execute_one(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Execute a query and return a single result or None."""
        if isinstance(params, dict):
            query, params = _convert_named_params(query, params)
        return self._fetch_one(query, params)

    def execute_returning_rowcount(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> int:
        """Execute a query and return the number of affected rows."""
        if isinstance(params, dict):
            query, params = _convert_named_params(query, params)

        self._circuit_breaker.before_call()
        conn = self._get_current_conn()
        try:
            if conn is not None:
                cursor = conn.execute(query, params or ())
                self._circuit_breaker.record_success()
                return cursor.rowcount

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    if self._isolation_level:
                        conn.execute(f"SET TRANSACTION ISOLATION LEVEL {self._isolation_level}")
                    cursor = conn.execute(query, params or ())
                    rowcount = cursor.rowcount
            self._circuit_breaker.record_success()
            return rowcount
        except psycopg.Error as e:
            self._circuit_breaker.record_failure(e)
            raise DatabaseError(f"Postgres query failed: {e}") from e

    # =========================================================================
    # Block State Operations
    # =========================================================================

    def get_block_state(self, chain_id: int) -> BlockState | None:
        row = self.execute_one(
            "SELECT * FROM block_state WHERE chain_id = %s",
            (chain_id,),
        )
        if not row:
            return None
        return BlockState(
            chain_id=row["chain_id"],
            last_processed_block_number=row["last_processed_block_number"],
            last_processed_block_hash=row["last_processed_block_hash"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def upsert_block_state(
        self,
        chain_id: int,
        block_number: int,
        block_hash: str,
    ) -> None:
        self.execute(
            """
            INSERT INTO block_state (chain_id, last_processed_block_number, last_processed_block_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT(chain_id) DO UPDATE SET
                last_processed_block_number = EXCLUDED.last_processed_block_number,
                last_processed_block_hash = EXCLUDED.last_processed_block_hash,
                updated_at = NOW()
            """,
            (chain_id, block_number, block_hash),
        )

    def get_block_hash_at_height(
        self, chain_id: int, block_number: int
    ) -> str | None:
        row = self.execute_one(
            "SELECT block_hash FROM block_hash_history WHERE chain_id = %s AND block_number = %s",
            (chain_id, block_number),
        )
        return row["block_hash"] if row else None

    def insert_block_hash(
        self, chain_id: int, block_number: int, block_hash: str
    ) -> None:
        self.execute(
            """
            INSERT INTO block_hash_history (chain_id, block_number, block_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT(chain_id, block_number) DO UPDATE SET
                block_hash = EXCLUDED.block_hash,
                inserted_at = NOW()
            """,
            (chain_id, block_number, block_hash),
        )

    def delete_block_hashes_above(self, chain_id: int, block_number: int) -> int:
        result = self.execute_returning(
            """
            DELETE FROM block_hash_history
            WHERE chain_id = %s AND block_number > %s
            RETURNING id
            """,
            (chain_id, block_number),
        )
        return len(result)

    def delete_block_hash_at_height(self, chain_id: int, block_number: int) -> bool:
        result = self.execute_returning(
            """
            DELETE FROM block_hash_history
            WHERE chain_id = %s AND block_number = %s
            RETURNING id
            """,
            (chain_id, block_number),
        )
        return len(result) > 0

    def cleanup_old_block_hashes(self, chain_id: int, keep_count: int) -> int:
        result = self.execute_returning(
            """
            DELETE FROM block_hash_history
            WHERE chain_id = %s AND block_number < (
                SELECT MAX(block_number) - %s + 1 FROM block_hash_history WHERE chain_id = %s
            )
            RETURNING id
            """,
            (chain_id, keep_count),
        )
        return len(result)

    def get_oldest_block_in_history(self, chain_id: int) -> int | None:
        row = self.execute_one(
            "SELECT MIN(block_number) as min_block FROM block_hash_history WHERE chain_id = %s",
            (chain_id,),
        )
        return row["min_block"] if row else None

    def get_latest_block_in_history(self, chain_id: int) -> int | None:
        row = self.execute_one(
            "SELECT MAX(block_number) as max_block FROM block_hash_history WHERE chain_id = %s",
            (chain_id,),
        )
        return row["max_block"] if row else None

    # =========================================================================
    # Job Operations
    # =========================================================================

    def get_job(self, job_id: str) -> JobConfig | None:
        row = self.execute_one("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
        if not row:
            return None
        return self._row_to_job_config(row)

    def get_enabled_jobs(self) -> list[JobConfig]:
        rows = self.execute_returning(
            "SELECT * FROM jobs WHERE enabled = true ORDER BY job_id"
        )
        return [self._row_to_job_config(row) for row in rows]

    def list_all_jobs(self) -> list[JobConfig]:
        rows = self.execute_returning("SELECT * FROM jobs ORDER BY job_id")
        return [self._row_to_job_config(row) for row in rows]

    def _row_to_job_config(self, row: dict[str, Any]) -> JobConfig:
        return JobConfig(
            job_id=row["job_id"],
            job_name=row["job_name"],
            enabled=row["enabled"],
            check_interval_blocks=row["check_interval_blocks"],
            last_checked_block_number=row["last_checked_block_number"],
            last_triggered_block_number=row["last_triggered_block_number"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def upsert_job(
        self,
        job_id: str,
        job_name: str,
        check_interval_blocks: int,
        enabled: bool = True,
    ) -> None:
        self.execute(
            """
            INSERT INTO jobs (job_id, job_name, check_interval_blocks, enabled)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT(job_id) DO UPDATE SET
                job_name = EXCLUDED.job_name,
                check_interval_blocks = EXCLUDED.check_interval_blocks,
                updated_at = NOW()
            """,
            (job_id, job_name, check_interval_blocks, enabled),
        )

    def update_job_checked(
        self, job_id: str, block_number: int, triggered: bool = False
    ) -> None:
        if triggered:
            self.execute(
                """
                UPDATE jobs SET
                    last_checked_block_number = %s,
                    last_triggered_block_number = %s,
                    updated_at = NOW()
                WHERE job_id = %s
                """,
                (block_number, job_id),
            )
        else:
            self.execute(
                """
                UPDATE jobs SET
                    last_checked_block_number = %s,
                    updated_at = NOW()
                WHERE job_id = %s
                """,
                (block_number, job_id),
            )

    def set_job_enabled(self, job_id: str, enabled: bool) -> bool:
        result = self.execute_returning(
            """
            UPDATE jobs SET enabled = %s, updated_at = NOW()
            WHERE job_id = %s
            RETURNING job_id
            """,
            (enabled, job_id),
        )
        return len(result) > 0

    def delete_job(self, job_id: str) -> bool:
        # Delete job_kv entries first (foreign key)
        self.execute("DELETE FROM job_kv WHERE job_id = %s", (job_id,))
        result = self.execute_returning(
            "DELETE FROM jobs WHERE job_id = %s RETURNING job_id",
            (job_id,),
        )
        return len(result) > 0

    def get_job_kv(self, job_id: str, key: str) -> Any | None:
        row = self.execute_one(
            "SELECT value_json FROM job_kv WHERE job_id = %s AND key = %s",
            (job_id, key),
        )
        if not row:
            return None
        return json.loads(row["value_json"])

    def set_job_kv(self, job_id: str, key: str, value: Any) -> None:
        value_json = json.dumps(value)
        self.execute(
            """
            INSERT INTO job_kv (job_id, key, value_json)
            VALUES (%s, %s, %s)
            ON CONFLICT(job_id, key) DO UPDATE SET
                value_json = EXCLUDED.value_json,
                updated_at = NOW()
            """,
            (job_id, key, value_json),
        )

    def delete_job_kv(self, job_id: str, key: str) -> bool:
        result = self.execute_returning(
            "DELETE FROM job_kv WHERE job_id = %s AND key = %s RETURNING job_id",
            (job_id, key),
        )
        return len(result) > 0

    # =========================================================================
    # Signer & Nonce Operations
    # =========================================================================

    def get_signer_state(self, chain_id: int, address: str) -> SignerState | None:
        row = self.execute_one(
            "SELECT * FROM signers WHERE chain_id = %s AND signer_address = %s",
            (chain_id, address),
        )
        if not row:
            return None
        return self._row_to_signer_state(row)

    def get_all_signers(self, chain_id: int) -> list[SignerState]:
        rows = self.execute_returning(
            "SELECT * FROM signers WHERE chain_id = %s",
            (chain_id,),
        )
        return [self._row_to_signer_state(row) for row in rows]

    def _row_to_signer_state(self, row: dict[str, Any]) -> SignerState:
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

    def upsert_signer(
        self,
        chain_id: int,
        address: str,
        next_nonce: int,
        last_synced_chain_nonce: int | None = None,
    ) -> None:
        self.execute(
            """
            INSERT INTO signers (chain_id, signer_address, next_nonce, last_synced_chain_nonce)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT(chain_id, signer_address) DO UPDATE SET
                next_nonce = EXCLUDED.next_nonce,
                last_synced_chain_nonce = EXCLUDED.last_synced_chain_nonce,
                updated_at = NOW()
            """,
            (chain_id, address, next_nonce, last_synced_chain_nonce),
        )

    def update_signer_next_nonce(
        self, chain_id: int, address: str, next_nonce: int
    ) -> None:
        self.execute(
            """
            UPDATE signers SET next_nonce = %s, updated_at = NOW()
            WHERE chain_id = %s AND signer_address = %s
            """,
            (next_nonce, chain_id, address),
        )

    def update_signer_chain_nonce(
        self, chain_id: int, address: str, chain_nonce: int
    ) -> None:
        self.execute(
            """
            UPDATE signers SET last_synced_chain_nonce = %s, updated_at = NOW()
            WHERE chain_id = %s AND signer_address = %s
            """,
            (chain_nonce, chain_id, address),
        )

    def set_gap_started_at(
        self, chain_id: int, address: str, started_at: datetime
    ) -> None:
        """Record when gap blocking started for a signer."""
        self.execute(
            """
            UPDATE signers SET gap_started_at = %s, updated_at = NOW()
            WHERE chain_id = %s AND signer_address = %s
            """,
            (started_at, chain_id, address),
        )

    def clear_gap_started_at(self, chain_id: int, address: str) -> None:
        """Clear gap tracking (gap resolved or force reset)."""
        self.execute(
            """
            UPDATE signers SET gap_started_at = NULL, updated_at = NOW()
            WHERE chain_id = %s AND signer_address = %s
            """,
            (chain_id, address),
        )

    def get_signer_by_alias(self, chain_id: int, alias: str) -> SignerState | None:
        """Get signer by alias. Returns None if not found."""
        row = self.execute_one(
            """
            SELECT * FROM signers
            WHERE chain_id = %s AND alias = %s
            """,
            (chain_id, alias),
        )
        if not row:
            return None
        return self._row_to_signer_state(row)

    def reserve_nonce_atomic(
        self,
        chain_id: int,
        address: str,
        chain_nonce: int | None,
        intent_id: UUID | None = None,
    ) -> int:
        """Reserve a nonce atomically with serialization conflict retry.

        Uses SERIALIZABLE isolation to prevent race conditions. Retries
        automatically on PostgreSQL serialization failures (40001).

        The inner transaction uses context manager which guarantees
        rollback on exception, making retries safe.

        Args:
            chain_id: The chain ID
            address: Signer address (lowercase)
            chain_nonce: Current on-chain nonce (from eth_getTransactionCount)
            intent_id: Optional intent ID to associate with reservation

        Returns:
            The reserved nonce

        Raises:
            DatabaseError: If reservation fails after all retries
        """
        from brawny.metrics import get_metrics

        last_error: Exception | None = None

        for attempt in range(MAX_SERIALIZATION_RETRIES + 1):
            try:
                return self._reserve_nonce_atomic_inner(
                    chain_id, address, chain_nonce, intent_id
                )
            except Exception as e:
                if not _is_serialization_failure(e):
                    raise

                last_error = e
                get_metrics().counter("brawny_nonce_serialization_retries_total").inc()

                if attempt < MAX_SERIALIZATION_RETRIES:
                    # Exponential backoff with jitter
                    delay_ms = min(BASE_RETRY_DELAY_MS * (2 ** attempt), MAX_RETRY_DELAY_MS)
                    jitter = random.uniform(0, delay_ms * 0.3)
                    time.sleep((delay_ms + jitter) / 1000.0)

                    logger.debug(
                        "nonce.serialization_retry",
                        chain_id=chain_id,
                        address=address,
                        attempt=attempt + 1,
                        delay_ms=delay_ms,
                    )

        # Exhausted retries
        logger.error(
            "nonce.serialization_retries_exhausted",
            chain_id=chain_id,
            address=address,
            max_retries=MAX_SERIALIZATION_RETRIES,
            exc_info=True,
        )
        raise last_error  # type: ignore[misc]

    def _reserve_nonce_atomic_inner(
        self,
        chain_id: int,
        address: str,
        chain_nonce: int | None,
        intent_id: UUID | None,
    ) -> int:
        """Inner implementation - single attempt.

        Uses context manager for transaction which guarantees
        rollback on exception, leaving connection in clean state for retry.
        """
        self._circuit_breaker.before_call()
        pool = self._ensure_pool()

        try:
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    # Use SERIALIZABLE isolation for atomic nonce reservation
                    conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")

                    # Ensure signer row exists
                    conn.execute(
                        """
                        INSERT INTO signers (chain_id, signer_address, next_nonce, last_synced_chain_nonce)
                        VALUES (%s, %s, 0, NULL)
                        ON CONFLICT(chain_id, signer_address) DO NOTHING
                        """,
                        (chain_id, address),
                    )

                    # Lock the signer row
                    row = conn.execute(
                        """
                        SELECT * FROM signers
                        WHERE chain_id = %s AND signer_address = %s
                        FOR UPDATE
                        """,
                        (chain_id, address),
                    ).fetchone()

                    if row is None:
                        raise DatabaseError("Failed to lock signer row")

                    db_next_nonce = row["next_nonce"]
                    base_nonce = chain_nonce if chain_nonce is not None else db_next_nonce

                    # Get existing reservations to find gaps
                    reservations = conn.execute(
                        """
                        SELECT nonce FROM nonce_reservations
                        WHERE chain_id = %s AND signer_address = %s
                        AND status != 'released'
                        AND nonce >= %s
                        ORDER BY nonce
                        """,
                        (chain_id, address, base_nonce),
                    ).fetchall()

                    # Find next available nonce (skip existing reservations)
                    candidate = base_nonce
                    for res in reservations:
                        if res["nonce"] == candidate:
                            candidate += 1
                        elif res["nonce"] > candidate:
                            break

                    if candidate - base_nonce > 100:
                        raise DatabaseError(
                            f"Could not find available nonce within 100 slots for signer {address}"
                        )

                    # Create the reservation
                    conn.execute(
                        """
                        INSERT INTO nonce_reservations (chain_id, signer_address, nonce, status, intent_id)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT(chain_id, signer_address, nonce) DO UPDATE SET
                            status = EXCLUDED.status,
                            intent_id = EXCLUDED.intent_id,
                            updated_at = NOW()
                        """,
                        (chain_id, address, candidate, NonceStatus.RESERVED.value, intent_id),
                    )

                    # Update signer's next_nonce
                    new_next_nonce = max(db_next_nonce, candidate + 1)
                    conn.execute(
                        """
                        UPDATE signers SET next_nonce = %s, updated_at = NOW()
                        WHERE chain_id = %s AND signer_address = %s
                        """,
                        (new_next_nonce, chain_id, address),
                    )

                    self._circuit_breaker.record_success()
                    return candidate

        except DatabaseError:
            self._circuit_breaker.record_failure(None)
            raise
        except Exception as e:
            self._circuit_breaker.record_failure(e)
            raise DatabaseError(f"Nonce reservation failed: {e}") from e

    def get_nonce_reservation(
        self, chain_id: int, address: str, nonce: int
    ) -> NonceReservation | None:
        row = self.execute_one(
            """
            SELECT * FROM nonce_reservations
            WHERE chain_id = %s AND signer_address = %s AND nonce = %s
            """,
            (chain_id, address, nonce),
        )
        if not row:
            return None
        return self._row_to_nonce_reservation(row)

    def get_reservations_for_signer(
        self, chain_id: int, address: str, status: str | None = None
    ) -> list[NonceReservation]:
        if status:
            rows = self.execute_returning(
                """
                SELECT * FROM nonce_reservations
                WHERE chain_id = %s AND signer_address = %s AND status = %s
                ORDER BY nonce
                """,
                (chain_id, address, status),
            )
        else:
            rows = self.execute_returning(
                """
                SELECT * FROM nonce_reservations
                WHERE chain_id = %s AND signer_address = %s
                ORDER BY nonce
                """,
                (chain_id, address),
            )
        return [self._row_to_nonce_reservation(row) for row in rows]

    def get_reservations_below_nonce(
        self, chain_id: int, address: str, nonce: int
    ) -> list[NonceReservation]:
        rows = self.execute_returning(
            """
            SELECT * FROM nonce_reservations
            WHERE chain_id = %s AND signer_address = %s AND nonce < %s
            ORDER BY nonce
            """,
            (chain_id, address, nonce),
        )
        return [self._row_to_nonce_reservation(row) for row in rows]

    def _row_to_nonce_reservation(self, row: dict[str, Any]) -> NonceReservation:
        return NonceReservation(
            id=row["id"],
            chain_id=row["chain_id"],
            signer_address=row["signer_address"],
            nonce=row["nonce"],
            status=NonceStatus(row["status"]),
            intent_id=row["intent_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def create_nonce_reservation(
        self,
        chain_id: int,
        address: str,
        nonce: int,
        status: str = "reserved",
        intent_id: UUID | None = None,
    ) -> NonceReservation:
        row = self.execute_one(
            """
            INSERT INTO nonce_reservations (chain_id, signer_address, nonce, status, intent_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT(chain_id, signer_address, nonce) DO UPDATE SET
                status = EXCLUDED.status,
                intent_id = EXCLUDED.intent_id,
                updated_at = NOW()
            RETURNING *
            """,
            (chain_id, address, nonce, status, intent_id),
        )
        if not row:
            raise DatabaseError("Failed to create nonce reservation")
        return self._row_to_nonce_reservation(row)

    def update_nonce_reservation_status(
        self,
        chain_id: int,
        address: str,
        nonce: int,
        status: str,
        intent_id: UUID | None = None,
    ) -> bool:
        if intent_id:
            result = self.execute_returning(
                """
                UPDATE nonce_reservations SET status = %s, intent_id = %s, updated_at = NOW()
                WHERE chain_id = %s AND signer_address = %s AND nonce = %s
                RETURNING id
                """,
                (status, intent_id, chain_id, address, nonce),
            )
        else:
            result = self.execute_returning(
                """
                UPDATE nonce_reservations SET status = %s, updated_at = NOW()
                WHERE chain_id = %s AND signer_address = %s AND nonce = %s
                RETURNING id
                """,
                (status, chain_id, address, nonce),
            )
        return len(result) > 0

    def release_nonce_reservation(
        self, chain_id: int, address: str, nonce: int
    ) -> bool:
        return self.update_nonce_reservation_status(
            chain_id, address, nonce, "released"
        )

    def cleanup_orphaned_nonces(
        self, chain_id: int, older_than_hours: int = 24
    ) -> int:
        with self._get_connection() as conn:
            result = conn.execute(
                text("""
                    DELETE FROM nonce_reservations
                    WHERE chain_id = :chain_id
                      AND status = 'orphaned'
                      AND updated_at < NOW() - MAKE_INTERVAL(hours => :hours)
                    RETURNING id
                """),
                {"chain_id": chain_id, "hours": older_than_hours},
            )
            return len(result.fetchall())

    # =========================================================================
    # Intent Operations
    # =========================================================================

    def create_intent(
        self,
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
    ) -> TxIntent | None:
        try:
            signer_address = signer_address.lower()
            row = self.execute_one(
                """
                INSERT INTO tx_intents (
                    intent_id, job_id, chain_id, signer_address, idempotency_key,
                    to_address, data, value_wei, gas_limit, max_fee_per_gas,
                    max_priority_fee_per_gas, min_confirmations, deadline_ts,
                    broadcast_group, broadcast_endpoints_json, retry_after, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, 'created')
                ON CONFLICT (chain_id, signer_address, idempotency_key) DO NOTHING
                RETURNING *
                """,
                (
                    intent_id,
                    job_id,
                    chain_id,
                    signer_address,
                    idempotency_key,
                    to_address,
                    data,
                    value_wei,
                    gas_limit,
                    max_fee_per_gas,
                    max_priority_fee_per_gas,
                    min_confirmations,
                    deadline_ts,
                    broadcast_group,
                    json.dumps(broadcast_endpoints) if broadcast_endpoints else None,
                ),
            )
            if row:
                return self._row_to_intent(row)
            return None
        except psycopg.Error as e:
            logger.warning(
                "db.create_intent_failed",
                error=str(e),
                intent_id=str(intent_id),
                idempotency_key=idempotency_key,
                job_id=job_id,
            )
            return None

    def get_intent(self, intent_id: UUID) -> TxIntent | None:
        row = self.execute_one(
            "SELECT * FROM tx_intents WHERE intent_id = %s",
            (intent_id,),
        )
        if not row:
            return None
        return self._row_to_intent(row)

    def get_intent_by_idempotency_key(
        self,
        chain_id: int,
        signer_address: str,
        idempotency_key: str,
    ) -> TxIntent | None:
        row = self.execute_one(
            "SELECT * FROM tx_intents WHERE chain_id = %s AND signer_address = %s AND idempotency_key = %s",
            (chain_id, signer_address.lower(), idempotency_key),
        )
        if not row:
            return None
        return self._row_to_intent(row)

    def _row_to_intent(self, row: dict[str, Any]) -> TxIntent:
        return TxIntent(
            intent_id=row["intent_id"],
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
            # Broadcast binding (may be None if not yet broadcast)
            broadcast_group=row.get("broadcast_group"),
            broadcast_endpoints_json=row.get("broadcast_endpoints_json"),
        )

    def get_intents_by_status(
        self,
        status: str | list[str],
        chain_id: int | None = None,
        job_id: str | None = None,
        limit: int = 100,
    ) -> list[TxIntent]:
        if isinstance(status, str):
            status = [status]

        # Build query dynamically
        query = "SELECT * FROM tx_intents WHERE status = ANY(%s)"
        params: list[Any] = [status]
        param_idx = 2

        if chain_id is not None:
            query += f" AND chain_id = ${param_idx}"
            params.append(chain_id)
            param_idx += 1
        if job_id is not None:
            query += f" AND job_id = ${param_idx}"
            params.append(job_id)
            param_idx += 1

        query += f" ORDER BY created_at ASC LIMIT ${param_idx}"
        params.append(limit)

        rows = self.execute_returning(query, tuple(params))
        return [self._row_to_intent(row) for row in rows]

    def list_intents_filtered(
        self,
        status: str | None = None,
        job_id: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        query = "SELECT * FROM tx_intents WHERE 1=1"
        params: list[Any] = []

        if status is not None:
            query += " AND status = %s"
            params.append(status)
        if job_id is not None:
            query += " AND job_id = %s"
            params.append(job_id)

        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        return self.execute_returning(query, tuple(params))

    def get_active_intent_count(self, job_id: str, chain_id: int | None = None) -> int:
        params: list[Any] = [
            [IntentStatus.CREATED.value,
             IntentStatus.CLAIMED.value,
             IntentStatus.SENDING.value,
             IntentStatus.PENDING.value],
            job_id,
        ]
        query = "SELECT COUNT(*) AS count FROM tx_intents WHERE status = ANY(%s) AND job_id = %s"
        if chain_id is not None:
            query += " AND chain_id = %s"
            params.append(chain_id)
        row = self.execute_one(query, tuple(params))
        return int(row["count"]) if row else 0

    def get_pending_intent_count(self, chain_id: int | None = None) -> int:
        params: list[Any] = [
            [IntentStatus.CREATED.value,
             IntentStatus.CLAIMED.value,
             IntentStatus.SENDING.value,
             IntentStatus.PENDING.value],
        ]
        query = "SELECT COUNT(*) AS count FROM tx_intents WHERE status = ANY(%s)"
        if chain_id is not None:
            query += " AND chain_id = %s"
            params.append(chain_id)
        row = self.execute_one(query, tuple(params))
        return int(row["count"]) if row else 0

    def get_backing_off_intent_count(self, chain_id: int | None = None) -> int:
        query = "SELECT COUNT(*) AS count FROM tx_intents WHERE retry_after > NOW()"
        params: list[Any] = []
        if chain_id is not None:
            query += " AND chain_id = %s"
            params.append(chain_id)
        row = self.execute_one(query, tuple(params))
        return int(row["count"]) if row else 0

    def get_oldest_pending_intent_age(self, chain_id: int) -> float | None:
        query = """
            SELECT EXTRACT(EPOCH FROM (NOW() - MIN(created_at)))::float AS age_seconds
            FROM tx_intents
            WHERE chain_id = %(chain_id)s
              AND status IN ('created', 'pending', 'claimed', 'sending')
        """
        result = self.execute_one(query, {"chain_id": chain_id})
        if result and result.get("age_seconds") is not None:
            return result["age_seconds"]
        return None

    def list_intent_inconsistencies(
        self,
        max_age_seconds: int,
        limit: int = 100,
        chain_id: int | None = None,
    ) -> list[dict[str, Any]]:
        chain_clause = ""
        chain_params: list[Any] = []
        if chain_id is not None:
            chain_clause = " AND chain_id = %s"
            chain_params = [chain_id] * 5

        query = f"""
        SELECT intent_id, status, 'pending_no_attempt' AS reason
        FROM tx_intents
        WHERE status = 'pending'
        {chain_clause}
        AND NOT EXISTS (
            SELECT 1 FROM tx_attempts
            WHERE tx_attempts.intent_id = tx_intents.intent_id
              AND tx_attempts.tx_hash IS NOT NULL
        )

        UNION ALL
        SELECT intent_id, status, 'confirmed_no_confirmed_attempt' AS reason
        FROM tx_intents
        WHERE status = 'confirmed'
        {chain_clause}
        AND NOT EXISTS (
            SELECT 1 FROM tx_attempts
            WHERE tx_attempts.intent_id = tx_intents.intent_id
              AND tx_attempts.status = 'confirmed'
        )

        UNION ALL
        SELECT intent_id, status, 'claimed_missing_claim' AS reason
        FROM tx_intents
        WHERE status = 'claimed'
        {chain_clause}
        AND (claim_token IS NULL OR claimed_at IS NULL)

        UNION ALL
        SELECT intent_id, status, 'nonclaimed_with_claim' AS reason
        FROM tx_intents
        WHERE status != 'claimed'
        {chain_clause}
        AND (claim_token IS NOT NULL OR claimed_at IS NOT NULL)

        UNION ALL
        SELECT intent_id, status, 'sending_stuck' AS reason
        FROM tx_intents
        WHERE status = 'sending'
        {chain_clause}
        AND updated_at < NOW() - INTERVAL '1 second' * %s

        LIMIT %s
        """
        params = chain_params + [max_age_seconds, limit]
        rows = self.execute_returning(query, tuple(params))
        return [dict(row) for row in rows]

    def list_sending_intents_older_than(
        self,
        max_age_seconds: int,
        limit: int = 100,
        chain_id: int | None = None,
    ) -> list[TxIntent]:
        query = """
        SELECT * FROM tx_intents
        WHERE status = 'sending'
        AND updated_at < NOW() - INTERVAL '1 second' * %s
        """
        params: list[Any] = [max_age_seconds]
        if chain_id is not None:
            query += " AND chain_id = %s"
            params.append(chain_id)
        query += " ORDER BY updated_at ASC LIMIT %s"
        params.append(limit)
        rows = self.execute_returning(query, tuple(params))
        return [self._row_to_intent(row) for row in rows]

    def claim_next_intent(
        self,
        claim_token: str,
        claimed_by: str | None = None,
    ) -> TxIntent | None:
        """Claim the next available intent using FOR UPDATE SKIP LOCKED."""
        row = self.execute_one(
            """
            WITH claimed AS (
                SELECT intent_id FROM tx_intents
                WHERE status = 'created'
                AND (deadline_ts IS NULL OR deadline_ts > NOW())
                AND (retry_after IS NULL OR retry_after <= NOW())
                ORDER BY created_at ASC
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            )
            UPDATE tx_intents
            SET status = 'claimed', claim_token = %s, claimed_at = NOW(),
                claimed_by = %s,
                retry_after = NULL, updated_at = NOW()
            WHERE intent_id = (SELECT intent_id FROM claimed)
            RETURNING *
            """,
            (claim_token, claimed_by),
        )
        if row:
            return self._row_to_intent(row)
        return None

    def update_intent_status(
        self,
        intent_id: UUID,
        status: str,
        claim_token: str | None = None,
    ) -> bool:
        if claim_token:
            result = self.execute_returning(
                """
                UPDATE tx_intents SET status = %s, claim_token = %s,
                    claimed_at = NOW(), updated_at = NOW()
                WHERE intent_id = %s
                RETURNING intent_id
                """,
                (status, claim_token, intent_id),
            )
        else:
            result = self.execute_returning(
                """
                UPDATE tx_intents SET status = %s, updated_at = NOW()
                WHERE intent_id = %s
                RETURNING intent_id
                """,
                (status, intent_id),
            )
        return len(result) > 0

    def update_intent_status_if(
        self,
        intent_id: UUID,
        status: str,
        expected_status: str | list[str],
    ) -> bool:
        if isinstance(expected_status, str):
            expected_status = [expected_status]
        result = self.execute_returning(
            """
            UPDATE tx_intents SET status = %s, updated_at = NOW()
            WHERE intent_id = %s AND status = ANY(%s)
            RETURNING intent_id
            """,
            (status, intent_id, expected_status),
        )
        return len(result) > 0

    def transition_intent_status(
        self,
        intent_id: UUID,
        from_statuses: list[str],
        to_status: str,
    ) -> tuple[bool, str | None]:
        """Atomic status transition with conditional claim clearing."""
        # Single UPDATE that:
        # 1. Captures old status via FROM subquery (LIMIT 1 for safety)
        # 2. Only updates if status matches allowed from_statuses
        # 3. Clears claim fields only when old status was 'claimed' AND to_status != 'claimed'
        result = self.execute_returning(
            """
            UPDATE tx_intents ti
            SET
                status = %s,
                updated_at = NOW(),
                claim_token = CASE
                    WHEN old.status = 'claimed' AND %s != 'claimed'
                    THEN NULL ELSE ti.claim_token
                END,
                claimed_at = CASE
                    WHEN old.status = 'claimed' AND %s != 'claimed'
                    THEN NULL ELSE ti.claimed_at
                END,
                claimed_by = CASE
                    WHEN old.status = 'claimed' AND %s != 'claimed'
                    THEN NULL ELSE ti.claimed_by
                END
            FROM (
                SELECT status FROM tx_intents
                WHERE intent_id = %s
                LIMIT 1
            ) old
            WHERE ti.intent_id = %s
              AND ti.status = ANY(%s)
            RETURNING old.status AS old_status
            """,
            (to_status, to_status, to_status, to_status, intent_id, intent_id, from_statuses),
        )

        if result:
            return (True, result[0]["old_status"])
        return (False, None)

    def update_intent_signer(self, intent_id: UUID, signer_address: str) -> bool:
        result = self.execute_returning(
            """
            UPDATE tx_intents SET signer_address = %s, updated_at = NOW()
            WHERE intent_id = %s
            RETURNING intent_id
            """,
            (signer_address.lower(), intent_id),
        )
        return len(result) > 0

    def release_intent_claim(self, intent_id: UUID) -> bool:
        result = self.execute_returning(
            """
            UPDATE tx_intents SET status = 'created', claim_token = NULL,
                claimed_at = NULL, updated_at = NOW()
            WHERE intent_id = %s AND status = 'claimed'
            RETURNING intent_id
            """,
            (intent_id,),
        )
        return len(result) > 0

    def release_intent_claim_if_token(self, intent_id: UUID, claim_token: str) -> bool:
        rowcount = self.execute_returning_rowcount(
            """
            UPDATE tx_intents
            SET status = 'created',
                claim_token = NULL,
                claimed_at = NULL,
                claimed_by = NULL,
                updated_at = NOW()
            WHERE intent_id = %s AND claim_token = %s AND status = 'claimed'
            """,
            (intent_id, claim_token),
        )
        return rowcount == 1

    def clear_intent_claim(self, intent_id: UUID) -> bool:
        result = self.execute_returning(
            """
            UPDATE tx_intents
            SET claim_token = NULL, claimed_at = NULL, updated_at = NOW()
            WHERE intent_id = %s
            RETURNING intent_id
            """,
            (intent_id,),
        )
        return len(result) > 0

    def set_intent_retry_after(self, intent_id: UUID, retry_after: datetime | None) -> bool:
        result = self.execute_returning(
            """
            UPDATE tx_intents
            SET retry_after = %s, updated_at = NOW()
            WHERE intent_id = %s
            RETURNING intent_id
            """,
            (retry_after, intent_id),
        )
        return len(result) > 0

    def increment_intent_retry_count(self, intent_id: UUID) -> int:
        result = self.execute_returning(
            """
            UPDATE tx_intents
            SET retry_count = retry_count + 1, updated_at = NOW()
            WHERE intent_id = %s
            RETURNING retry_count
            """,
            (intent_id,),
        )
        if not result:
            return 0
        return result[0]["retry_count"]

    def release_stale_intent_claims(self, max_age_seconds: int) -> int:
        result = self.execute_returning(
            """
            UPDATE tx_intents
            SET status = 'created', claim_token = NULL, claimed_at = NULL, updated_at = NOW()
            WHERE status = 'claimed'
            AND claimed_at < NOW() - INTERVAL '1 second' * %s
            AND NOT EXISTS (
                SELECT 1 FROM tx_attempts WHERE tx_attempts.intent_id = tx_intents.intent_id
            )
            RETURNING intent_id
            """,
            (max_age_seconds,),
        )
        return len(result)

    def abandon_intent(self, intent_id: UUID) -> bool:
        return self.update_intent_status(intent_id, "abandoned")

    def get_pending_intents_for_signer(
        self, chain_id: int, address: str
    ) -> list[TxIntent]:
        rows = self.execute_returning(
            """
            SELECT * FROM tx_intents
            WHERE chain_id = %s AND signer_address = %s
            AND status IN ('sending', 'pending')
            ORDER BY created_at
            """,
            (chain_id, address),
        )
        return [self._row_to_intent(row) for row in rows]

    # =========================================================================
    # Broadcast Binding Operations
    # =========================================================================

    def get_broadcast_binding(self, intent_id: UUID) -> tuple[str | None, list[str]] | None:
        """Get binding if exists, None for first broadcast.

        Returns:
            Tuple of (group_name or None, endpoints) or None if not bound yet

        Raises:
            ValueError: If binding is corrupt (wrong type, empty)
        """
        row = self.execute_one(
            """
            SELECT broadcast_group, broadcast_endpoints_json
            FROM tx_intents
            WHERE intent_id = %s
            """,
            (intent_id,),
        )

        if not row:
            return None

        has_endpoints = row["broadcast_endpoints_json"] is not None

        # No endpoints → not bound yet
        if not has_endpoints:
            return None

        # Parse and validate endpoints
        endpoints = json.loads(row["broadcast_endpoints_json"])
        if not isinstance(endpoints, list):
            raise ValueError(
                f"Corrupt binding for intent {intent_id}: "
                f"endpoints_json is {type(endpoints).__name__}, expected list"
            )
        if not endpoints:
            raise ValueError(
                f"Corrupt binding for intent {intent_id}: endpoints list is empty"
            )
        if not all(isinstance(ep, str) for ep in endpoints):
            raise ValueError(
                f"Corrupt binding for intent {intent_id}: endpoints contains non-string"
            )

        return row["broadcast_group"], endpoints

    # =========================================================================
    # Attempt Operations
    # =========================================================================

    def create_attempt(
        self,
        attempt_id: UUID,
        intent_id: UUID,
        nonce: int,
        gas_params_json: str,
        status: str = "signed",
        tx_hash: str | None = None,
        replaces_attempt_id: UUID | None = None,
        broadcast_group: str | None = None,
        endpoint_url: str | None = None,
        binding: tuple[str | None, list[str]] | None = None,
    ) -> TxAttempt:
        """Create attempt, optionally setting binding atomically.

        Args:
            binding: If provided (first broadcast), persist binding atomically.
                     Tuple of (group_name or None, endpoints)

        CRITICAL: Uses WHERE broadcast_endpoints_json IS NULL to prevent overwrites.
        """
        with self.transaction(isolation_level=IsolationLevel.SERIALIZABLE):
            if binding is not None:
                # First broadcast: check existence + binding state for clear error messages
                row = self.execute_one(
                    "SELECT broadcast_endpoints_json FROM tx_intents WHERE intent_id = %s FOR UPDATE",
                    (intent_id,),
                )

                if not row:
                    raise ValueError(f"Intent {intent_id} not found")
                if row["broadcast_endpoints_json"] is not None:
                    raise ValueError(
                        f"Intent {intent_id} already bound. "
                        f"Cannot rebind — may indicate race condition."
                    )

                group_name, endpoints = binding
                # Defensive copy
                endpoints_snapshot = list(endpoints)

                # Update with WHERE guard
                updated = self.execute_one(
                    """
                    UPDATE tx_intents
                    SET broadcast_group = %s,
                        broadcast_endpoints_json = %s,
                        updated_at = NOW()
                    WHERE intent_id = %s
                      AND broadcast_endpoints_json IS NULL
                    RETURNING intent_id
                    """,
                    (group_name, json.dumps(endpoints_snapshot), intent_id),
                )

                if not updated:
                    raise ValueError(
                        f"Binding race condition for intent {intent_id}: "
                        f"concurrent update detected"
                    )

            # Create attempt with broadcast audit fields
            row = self.execute_one(
                """
                INSERT INTO tx_attempts (
                    attempt_id, intent_id, nonce, gas_params_json, status,
                    tx_hash, replaces_attempt_id, broadcast_group, endpoint_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    attempt_id,
                    intent_id,
                    nonce,
                    gas_params_json,
                    status,
                    tx_hash,
                    replaces_attempt_id,
                    broadcast_group,
                    endpoint_url,
                ),
            )
            if not row:
                raise DatabaseError("Failed to create attempt")
            return self._row_to_attempt(row)

    def get_attempt(self, attempt_id: UUID) -> TxAttempt | None:
        row = self.execute_one(
            "SELECT * FROM tx_attempts WHERE attempt_id = %s",
            (attempt_id,),
        )
        if not row:
            return None
        return self._row_to_attempt(row)

    def get_attempts_for_intent(self, intent_id: UUID) -> list[TxAttempt]:
        rows = self.execute_returning(
            "SELECT * FROM tx_attempts WHERE intent_id = %s ORDER BY created_at",
            (intent_id,),
        )
        return [self._row_to_attempt(row) for row in rows]

    def get_latest_attempt_for_intent(self, intent_id: UUID) -> TxAttempt | None:
        row = self.execute_one(
            """
            SELECT * FROM tx_attempts WHERE intent_id = %s
            ORDER BY created_at DESC LIMIT 1
            """,
            (intent_id,),
        )
        if not row:
            return None
        return self._row_to_attempt(row)

    def get_attempt_by_tx_hash(self, tx_hash: str) -> TxAttempt | None:
        row = self.execute_one(
            "SELECT * FROM tx_attempts WHERE tx_hash = %s",
            (tx_hash,),
        )
        if not row:
            return None
        return self._row_to_attempt(row)

    def _row_to_attempt(self, row: dict[str, Any]) -> TxAttempt:
        return TxAttempt(
            attempt_id=row["attempt_id"],
            intent_id=row["intent_id"],
            nonce=row["nonce"],
            tx_hash=row["tx_hash"],
            gas_params=GasParams.from_json(row["gas_params_json"]),
            status=AttemptStatus(row["status"]),
            error_code=row["error_code"],
            error_detail=row["error_detail"],
            replaces_attempt_id=row["replaces_attempt_id"],
            broadcast_block=row["broadcast_block"],
            broadcast_at=row.get("broadcast_at"),
            included_block=row.get("included_block"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            # Audit trail (may be None for older attempts)
            broadcast_group=row.get("broadcast_group"),
            endpoint_url=row.get("endpoint_url"),
        )

    def update_attempt_status(
        self,
        attempt_id: UUID,
        status: str,
        tx_hash: str | None = None,
        broadcast_block: int | None = None,
        broadcast_at: datetime | None = None,
        included_block: int | None = None,
        error_code: str | None = None,
        error_detail: str | None = None,
    ) -> bool:
        # Build dynamic update
        updates = ["status = %s", "updated_at = NOW()"]
        params: list[Any] = [status]
        param_idx = 2

        if tx_hash is not None:
            updates.append(f"tx_hash = ${param_idx}")
            params.append(tx_hash)
            param_idx += 1
        if broadcast_block is not None:
            updates.append(f"broadcast_block = ${param_idx}")
            params.append(broadcast_block)
            param_idx += 1
        if broadcast_at is not None:
            updates.append(f"broadcast_at = ${param_idx}")
            params.append(broadcast_at)
            param_idx += 1
        if included_block is not None:
            updates.append(f"included_block = ${param_idx}")
            params.append(included_block)
            param_idx += 1
        if error_code is not None:
            updates.append(f"error_code = ${param_idx}")
            params.append(error_code)
            param_idx += 1
        if error_detail is not None:
            updates.append(f"error_detail = ${param_idx}")
            params.append(error_detail)
            param_idx += 1

        params.append(attempt_id)
        query = f"UPDATE tx_attempts SET {', '.join(updates)} WHERE attempt_id = ${param_idx} RETURNING attempt_id"
        result = self.execute_returning(query, tuple(params))
        return len(result) > 0

    # =========================================================================
    # Transaction Operations (NEW - replaces Intent/Attempt in Phase 2+)
    #
    # IMPORTANT: Transaction is the only durable execution model.
    # Do not add attempt-related methods here.
    # =========================================================================

    def create_tx(
        self,
        tx_id: UUID,
        job_id: str,
        chain_id: int,
        idempotency_key: str,
        signer_address: str,
        to_address: str,
        data: str | None,
        value_wei: str,
        min_confirmations: int,
        deadline_ts: datetime | None,
        gas_params: GasParams | None = None,
    ) -> Transaction | None:
        """Create a new transaction.

        Returns None if idempotency_key already exists (idempotency).
        """
        gas_params_json = gas_params.to_json() if gas_params else None
        try:
            result = self.execute_returning(
                """
                INSERT INTO transactions (
                    tx_id, job_id, chain_id, idempotency_key,
                    signer_address, to_address, data, value_wei,
                    min_confirmations, deadline_ts, status,
                    replacement_count, gas_params_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'created', 0, %s)
                ON CONFLICT (chain_id, signer_address, idempotency_key) DO NOTHING
                RETURNING *
                """,
                (
                    tx_id,
                    job_id,
                    chain_id,
                    idempotency_key,
                    signer_address,
                    to_address,
                    data,
                    value_wei,
                    min_confirmations,
                    deadline_ts,
                    gas_params_json,
                ),
            )
            if not result:
                return None
            return self._row_to_transaction(result[0])
        except psycopg.errors.UniqueViolation:
            return None

    def get_tx(self, tx_id: UUID) -> Transaction | None:
        """Get a transaction by ID."""
        row = self.execute_one(
            "SELECT * FROM transactions WHERE tx_id = %s",
            (tx_id,),
        )
        if not row:
            return None
        return self._row_to_transaction(row)

    def get_tx_by_idempotency_key(
        self,
        chain_id: int,
        signer_address: str,
        idempotency_key: str,
    ) -> Transaction | None:
        """Get a transaction by idempotency key (scoped to chain and signer)."""
        row = self.execute_one(
            "SELECT * FROM transactions WHERE chain_id = %s AND signer_address = %s AND idempotency_key = %s",
            (chain_id, signer_address.lower(), idempotency_key),
        )
        if not row:
            return None
        return self._row_to_transaction(row)

    def get_tx_by_hash(self, tx_hash: str) -> Transaction | None:
        """Get a transaction by current tx hash.

        NOTE: Does NOT search tx_hash_history. Only matches current_tx_hash.
        """
        row = self.execute_one(
            "SELECT * FROM transactions WHERE current_tx_hash = %s",
            (tx_hash,),
        )
        if not row:
            return None
        return self._row_to_transaction(row)

    def list_pending_txs(
        self,
        chain_id: int | None = None,
        job_id: str | None = None,
    ) -> list[Transaction]:
        """List transactions in CREATED or BROADCAST status."""
        query = "SELECT * FROM transactions WHERE status IN ('created', 'broadcast')"
        params: list[Any] = []
        param_idx = 1

        if chain_id is not None:
            query += f" AND chain_id = ${param_idx}"
            params.append(chain_id)
            param_idx += 1
        if job_id is not None:
            query += f" AND job_id = ${param_idx}"
            params.append(job_id)
            param_idx += 1

        query += " ORDER BY created_at ASC"
        rows = self.execute_returning(query, tuple(params) if params else None)
        return [self._row_to_transaction(row) for row in rows]

    def claim_tx(self, claim_token: str) -> Transaction | None:
        """Claim the next CREATED transaction for processing.

        Status remains CREATED while claimed - no "claimed" status.
        Uses FOR UPDATE SKIP LOCKED for non-blocking claim.
        """
        result = self.execute_returning(
            """
            UPDATE transactions
            SET claim_token = %s, claimed_at = NOW(), updated_at = NOW()
            WHERE tx_id = (
                SELECT tx_id FROM transactions
                WHERE status = 'created'
                AND claim_token IS NULL
                AND (deadline_ts IS NULL OR deadline_ts > NOW())
                ORDER BY created_at ASC, tx_id ASC
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            )
            RETURNING *
            """,
            (claim_token,),
        )
        if not result:
            return None
        return self._row_to_transaction(result[0])

    def set_tx_broadcast(
        self,
        tx_id: UUID,
        tx_hash: str,
        nonce: int,
        gas_params: GasParams,
        broadcast_block: int,
        broadcast_info: BroadcastInfo | None = None,
    ) -> bool:
        """Record initial broadcast.

        Sets status=BROADCAST, creates first tx_hash_history record.
        """
        now = datetime.now(timezone.utc)

        # Create first history record
        history_record = TxHashRecord(
            tx_hash=tx_hash,
            nonce=nonce,
            broadcast_at=now.isoformat(),
            broadcast_block=broadcast_block,
            gas_limit=gas_params.gas_limit,
            max_fee_per_gas=gas_params.max_fee_per_gas,
            max_priority_fee_per_gas=gas_params.max_priority_fee_per_gas,
            reason="initial",
            outcome=None,
        )
        tx_hash_history = json.dumps([history_record.to_dict()])

        result = self.execute_returning(
            """
            UPDATE transactions
            SET status = 'broadcast',
                current_tx_hash = %s,
                current_nonce = %s,
                gas_params_json = %s,
                broadcast_info_json = %s,
                tx_hash_history = %s,
                updated_at = NOW()
            WHERE tx_id = %s
            AND status = 'created'
            RETURNING tx_id
            """,
            (
                tx_hash,
                nonce,
                gas_params.to_json(),
                broadcast_info.to_json() if broadcast_info else None,
                tx_hash_history,
                tx_id,
            ),
        )
        return len(result) > 0

    def set_tx_replaced(
        self,
        tx_id: UUID,
        new_tx_hash: str,
        gas_params: GasParams,
        broadcast_block: int,
        reason: str = "fee_bump",
    ) -> bool:
        """Record replacement broadcast.

        Appends to tx_hash_history, updates current_tx_hash, increments
        replacement_count. Status remains BROADCAST.
        """
        now = datetime.now(timezone.utc)

        # First, get current state
        row = self.execute_one(
            "SELECT current_nonce, tx_hash_history FROM transactions WHERE tx_id = %s AND status = 'broadcast'",
            (tx_id,),
        )
        if not row:
            return False

        nonce = row["current_nonce"]
        existing_history = json.loads(row["tx_hash_history"]) if row["tx_hash_history"] else []

        # Mark previous entry as replaced
        if existing_history:
            existing_history[-1]["outcome"] = "replaced"

        # Add new history record
        new_record = TxHashRecord(
            tx_hash=new_tx_hash,
            nonce=nonce,
            broadcast_at=now.isoformat(),
            broadcast_block=broadcast_block,
            gas_limit=gas_params.gas_limit,
            max_fee_per_gas=gas_params.max_fee_per_gas,
            max_priority_fee_per_gas=gas_params.max_priority_fee_per_gas,
            reason=reason,
            outcome=None,
        )
        existing_history.append(new_record.to_dict())

        result = self.execute_returning(
            """
            UPDATE transactions
            SET current_tx_hash = %s,
                gas_params_json = %s,
                tx_hash_history = %s,
                replacement_count = replacement_count + 1,
                updated_at = NOW()
            WHERE tx_id = %s
            AND status = 'broadcast'
            RETURNING tx_id
            """,
            (
                new_tx_hash,
                gas_params.to_json(),
                json.dumps(existing_history),
                tx_id,
            ),
        )
        return len(result) > 0

    def set_tx_confirmed(
        self,
        tx_id: UUID,
        included_block: int,
    ) -> bool:
        """Mark transaction confirmed.

        Sets status=CONFIRMED, included_block, confirmed_at.
        Updates tx_hash_history with outcome.
        """
        now = datetime.now(timezone.utc)

        # Get and update history
        row = self.execute_one(
            "SELECT tx_hash_history FROM transactions WHERE tx_id = %s AND status = 'broadcast'",
            (tx_id,),
        )
        if not row:
            return False

        existing_history = json.loads(row["tx_hash_history"]) if row["tx_hash_history"] else []
        if existing_history:
            existing_history[-1]["outcome"] = "confirmed"

        result = self.execute_returning(
            """
            UPDATE transactions
            SET status = 'confirmed',
                included_block = %s,
                confirmed_at = %s,
                tx_hash_history = %s,
                updated_at = NOW()
            WHERE tx_id = %s
            AND status = 'broadcast'
            RETURNING tx_id
            """,
            (
                included_block,
                now,
                json.dumps(existing_history),
                tx_id,
            ),
        )
        return len(result) > 0

    def set_tx_failed(
        self,
        tx_id: UUID,
        failure_type: FailureType,
        error_info: ErrorInfo | None = None,
    ) -> bool:
        """Mark transaction failed.

        Sets status=FAILED, failure_type, error_info_json.
        Updates tx_hash_history with outcome if applicable.
        """
        # Serialize error_info
        error_info_json = None
        if error_info:
            error_info_json = json.dumps({
                "error_type": error_info.error_type,
                "message": error_info.message,
                "code": error_info.code,
            })

        # Get and update history if broadcast
        row = self.execute_one(
            "SELECT status, tx_hash_history FROM transactions WHERE tx_id = %s AND status IN ('created', 'broadcast')",
            (tx_id,),
        )
        if not row:
            return False

        existing_history = json.loads(row["tx_hash_history"]) if row["tx_hash_history"] else []
        if existing_history and row["status"] == "broadcast":
            existing_history[-1]["outcome"] = "failed"

        result = self.execute_returning(
            """
            UPDATE transactions
            SET status = 'failed',
                failure_type = %s,
                error_info_json = %s,
                tx_hash_history = %s,
                updated_at = NOW()
            WHERE tx_id = %s
            AND status IN ('created', 'broadcast')
            RETURNING tx_id
            """,
            (
                failure_type.value,
                error_info_json,
                json.dumps(existing_history) if existing_history else None,
                tx_id,
            ),
        )
        return len(result) > 0

    def release_stale_tx_claims(self, max_age_seconds: int) -> int:
        """Release claims older than threshold. 0 = release all claims."""
        if max_age_seconds == 0:
            # Release ALL claims
            result = self.execute_returning(
                """
                UPDATE transactions
                SET claim_token = NULL, claimed_at = NULL, updated_at = NOW()
                WHERE status = 'created'
                AND claim_token IS NOT NULL
                RETURNING tx_id
                """
            )
        else:
            result = self.execute_returning(
                """
                UPDATE transactions
                SET claim_token = NULL, claimed_at = NULL, updated_at = NOW()
                WHERE status = 'created'
                AND claim_token IS NOT NULL
                AND claimed_at < NOW() - INTERVAL '%s seconds'
                RETURNING tx_id
                """,
                (max_age_seconds,),
            )
        return len(result)

    def _row_to_transaction(self, row: dict[str, Any]) -> Transaction:
        """Convert database row to Transaction object."""
        tx_id = row["tx_id"]
        if isinstance(tx_id, str):
            tx_id = UUID(tx_id)

        # Parse failure_type if present
        failure_type = None
        if row.get("failure_type"):
            failure_type = FailureType(row["failure_type"])

        return Transaction(
            tx_id=tx_id,
            job_id=row["job_id"],
            chain_id=row["chain_id"],
            idempotency_key=row["idempotency_key"],
            signer_address=row["signer_address"],
            to_address=row["to_address"],
            data=row["data"],
            value_wei=row["value_wei"],
            min_confirmations=row["min_confirmations"],
            deadline_ts=row["deadline_ts"],
            status=TxStatus(row["status"]),
            failure_type=failure_type,
            current_tx_hash=row["current_tx_hash"],
            current_nonce=row["current_nonce"],
            replacement_count=row["replacement_count"],
            claim_token=row["claim_token"],
            claimed_at=row["claimed_at"],
            included_block=row["included_block"],
            confirmed_at=row["confirmed_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            gas_params_json=row["gas_params_json"],
            broadcast_info_json=row["broadcast_info_json"],
            error_info_json=row["error_info_json"],
            tx_hash_history=row["tx_hash_history"],
        )

    # =========================================================================
    # ABI Cache Operations
    # =========================================================================

    def get_cached_abi(self, chain_id: int, address: str) -> ABICacheEntry | None:
        row = self.execute_one(
            "SELECT * FROM abi_cache WHERE chain_id = %s AND address = %s",
            (chain_id, address),
        )
        if not row:
            return None
        return ABICacheEntry(
            chain_id=row["chain_id"],
            address=row["address"],
            abi_json=row["abi_json"],
            source=row["source"],
            resolved_at=row["resolved_at"],
        )

    def set_cached_abi(
        self,
        chain_id: int,
        address: str,
        abi_json: str,
        source: str,
    ) -> None:
        self.execute(
            """
            INSERT INTO abi_cache (chain_id, address, abi_json, source)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT(chain_id, address) DO UPDATE SET
                abi_json = EXCLUDED.abi_json,
                source = EXCLUDED.source,
                resolved_at = NOW()
            """,
            (chain_id, address, abi_json, source),
        )

    def clear_cached_abi(self, chain_id: int, address: str) -> bool:
        result = self.execute_returning(
            "DELETE FROM abi_cache WHERE chain_id = %s AND address = %s RETURNING chain_id",
            (chain_id, address),
        )
        return len(result) > 0

    def cleanup_expired_abis(self, max_age_seconds: int) -> int:
        result = self.execute_returning(
            """
            DELETE FROM abi_cache
            WHERE resolved_at < NOW() - INTERVAL '1 second' * %s
            RETURNING chain_id
            """,
            (max_age_seconds,),
        )
        return len(result)

    # =========================================================================
    # Proxy Cache Operations
    # =========================================================================

    def get_cached_proxy(
        self, chain_id: int, proxy_address: str
    ) -> ProxyCacheEntry | None:
        row = self.execute_one(
            "SELECT * FROM proxy_cache WHERE chain_id = %s AND proxy_address = %s",
            (chain_id, proxy_address),
        )
        if not row:
            return None
        return ProxyCacheEntry(
            chain_id=row["chain_id"],
            proxy_address=row["proxy_address"],
            implementation_address=row["implementation_address"],
            resolved_at=row["resolved_at"],
        )

    def set_cached_proxy(
        self,
        chain_id: int,
        proxy_address: str,
        implementation_address: str,
    ) -> None:
        self.execute(
            """
            INSERT INTO proxy_cache (chain_id, proxy_address, implementation_address)
            VALUES (%s, %s, %s)
            ON CONFLICT(chain_id, proxy_address) DO UPDATE SET
                implementation_address = EXCLUDED.implementation_address,
                resolved_at = NOW()
            """,
            (chain_id, proxy_address, implementation_address),
        )

    def clear_cached_proxy(self, chain_id: int, proxy_address: str) -> bool:
        result = self.execute_returning(
            "DELETE FROM proxy_cache WHERE chain_id = %s AND proxy_address = %s RETURNING chain_id",
            (chain_id, proxy_address),
        )
        return len(result) > 0

    # =========================================================================
    # Cleanup & Maintenance
    # =========================================================================

    def cleanup_old_intents(
        self,
        older_than_days: int,
        statuses: list[str] | None = None,
    ) -> int:
        if statuses is None:
            statuses = ["confirmed", "failed", "abandoned"]

        result = self.execute_returning(
            """
            DELETE FROM tx_intents
            WHERE status = ANY(%s)
            AND created_at < NOW() - INTERVAL '1 day' * %s
            RETURNING intent_id
            """,
            (statuses, older_than_days),
        )
        return len(result)

    def get_database_stats(self) -> dict[str, Any]:
        """Get database statistics for health checks."""
        stats: dict[str, Any] = {"type": "postgresql"}

        # Count intents by status
        rows = self.execute_returning(
            "SELECT status, COUNT(*) as count FROM tx_intents GROUP BY status"
        )
        stats["intents_by_status"] = {row["status"]: row["count"] for row in rows}

        # Count total jobs
        row = self.execute_one("SELECT COUNT(*) as count FROM jobs")
        stats["total_jobs"] = row["count"] if row else 0

        # Count enabled jobs
        row = self.execute_one("SELECT COUNT(*) as count FROM jobs WHERE enabled = true")
        stats["enabled_jobs"] = row["count"] if row else 0

        # Get block state
        rows = self.execute_returning("SELECT * FROM block_state")
        stats["block_states"] = [
            {
                "chain_id": row["chain_id"],
                "last_block": row["last_processed_block_number"],
            }
            for row in rows
        ]

        # Pool statistics if available
        if self._pool:
            stats["pool"] = {
                "size": self._pool.get_size(),
                "free": self._pool.get_idle_size(),
                "min": self._pool.get_min_size(),
                "max": self._pool.get_max_size(),
            }

        return stats

    # =========================================================================
    # Reconciliation Operations
    # =========================================================================

    def clear_orphaned_claims(self, chain_id: int, older_than_minutes: int = 2) -> int:
        """Clear claim fields where status != 'claimed' and claim is stale."""
        result = self.execute_returning(
            """
            UPDATE tx_intents
            SET claim_token = NULL,
                claimed_at = NULL,
                claimed_by = NULL,
                updated_at = NOW()
            WHERE chain_id = %s
              AND status != 'claimed'
              AND claim_token IS NOT NULL
              AND claimed_at IS NOT NULL
              AND claimed_at < NOW() - make_interval(mins => %s)
            RETURNING intent_id
            """,
            (chain_id, older_than_minutes),
        )
        return len(result)

    def release_orphaned_nonces(self, chain_id: int, older_than_minutes: int = 5) -> int:
        """Release nonces for terminal intents that are stale."""
        # Only release 'reserved' (not 'in_flight' - that's scary without receipt check)
        # Guard on both intent.updated_at AND reservation.updated_at for safety
        result = self.execute_returning(
            """
            UPDATE nonce_reservations nr
            SET status = 'released',
                updated_at = NOW()
            FROM tx_intents ti
            WHERE nr.intent_id = ti.intent_id
              AND nr.chain_id = %s
              AND nr.status = 'reserved'
              AND ti.status IN ('failed', 'abandoned', 'reverted')
              AND ti.updated_at < NOW() - make_interval(mins => %s)
              AND nr.updated_at < NOW() - make_interval(mins => %s)
            RETURNING nr.nonce
            """,
            (chain_id, older_than_minutes, older_than_minutes),
        )
        return len(result)

    def count_pending_without_attempts(self, chain_id: int) -> int:
        """Count pending intents with no attempt records (integrity issue)."""
        result = self.execute_one(
            """
            SELECT COUNT(*) as count
            FROM tx_intents ti
            LEFT JOIN tx_attempts ta ON ti.intent_id = ta.intent_id
            WHERE ti.chain_id = %s
              AND ti.status = 'pending'
              AND ta.attempt_id IS NULL
            """,
            (chain_id,),
        )
        return result["count"] if result else 0

    def count_stale_claims(self, chain_id: int, older_than_minutes: int = 10) -> int:
        """Count intents stuck in CLAIMED for too long."""
        result = self.execute_one(
            """
            SELECT COUNT(*) as count
            FROM tx_intents
            WHERE chain_id = %s
              AND status = 'claimed'
              AND claimed_at IS NOT NULL
              AND claimed_at < NOW() - make_interval(mins => %s)
            """,
            (chain_id, older_than_minutes),
        )
        return result["count"] if result else 0

    # =========================================================================
    # Invariant Queries (Phase 2)
    # =========================================================================

    def count_stuck_claimed(self, chain_id: int, older_than_minutes: int = 10) -> int:
        """Count intents stuck in CLAIMED status for too long."""
        row = self.execute_one(
            """
            SELECT COUNT(*) as count
            FROM tx_intents
            WHERE chain_id = %s
              AND status = 'claimed'
              AND claimed_at < NOW() - make_interval(mins => %s)
            """,
            (chain_id, older_than_minutes),
        )
        return row["count"] if row else 0

    def count_orphaned_claims(self, chain_id: int) -> int:
        """Count intents with claim_token set but status != claimed."""
        row = self.execute_one(
            """
            SELECT COUNT(*) as count
            FROM tx_intents
            WHERE chain_id = %s
              AND status != 'claimed'
              AND claim_token IS NOT NULL
            """,
            (chain_id,),
        )
        return row["count"] if row else 0

    def count_orphaned_nonces(self, chain_id: int) -> int:
        """Count reserved/in_flight nonces for failed/abandoned intents."""
        row = self.execute_one(
            """
            SELECT COUNT(*) as count
            FROM nonce_reservations nr
            JOIN tx_intents ti ON nr.intent_id = ti.intent_id
            WHERE nr.chain_id = %s
              AND nr.status IN ('reserved', 'in_flight')
              AND ti.status IN ('failed', 'abandoned', 'reverted')
            """,
            (chain_id,),
        )
        return row["count"] if row else 0

    def get_oldest_nonce_gap_age_seconds(self, chain_id: int) -> float:
        """Get age in seconds of the oldest nonce gap.

        Anchors from signers (small table) for efficiency.
        Returns 0 if no gaps or if chain nonce not synced.
        """
        row = self.execute_one(
            """
            SELECT
                COALESCE(EXTRACT(EPOCH FROM (NOW() - MIN(nr.created_at))), 0) AS oldest_gap_seconds
            FROM signers s
            JOIN nonce_reservations nr
              ON nr.chain_id = s.chain_id
             AND nr.signer_address = s.signer_address
            WHERE s.chain_id = %s
              AND s.last_synced_chain_nonce IS NOT NULL
              AND nr.status IN ('reserved', 'in_flight')
              AND nr.nonce < s.last_synced_chain_nonce
            """,
            (chain_id,),
        )
        return float(row["oldest_gap_seconds"]) if row else 0.0
