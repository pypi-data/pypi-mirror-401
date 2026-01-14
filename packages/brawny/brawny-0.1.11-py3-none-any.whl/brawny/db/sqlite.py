"""SQLite database implementation for brawny.

SQLite is for development only. Production deployments must use PostgreSQL.

Key differences from PostgreSQL:
- Uses IMMEDIATE transaction mode for nonce reservation (app-level locking)
- Uses deterministic ordering with secondary sort for intent claiming
- No connection pooling (single connection)
- SERIAL becomes INTEGER PRIMARY KEY AUTOINCREMENT
"""

from __future__ import annotations

import json
import re
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
from uuid import UUID

from brawny.db.base import (
    ABICacheEntry,
    BlockHashEntry,
    BlockState,
    Database,
    IsolationLevel,
    ProxyCacheEntry,
)
from brawny.db.circuit_breaker import DatabaseCircuitBreaker
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


def adapt_datetime(dt: datetime) -> str:
    """Adapt datetime to ISO format string for SQLite."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def convert_datetime(val: bytes) -> datetime:
    """Convert ISO format string from SQLite to datetime."""
    s = val.decode("utf-8")
    # Handle various formats
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        # Try parsing without timezone
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


# Register adapters
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("TIMESTAMP", convert_datetime)


class SQLiteDatabase(Database):
    """SQLite implementation of the Database interface.

    Thread-safety: Uses a per-thread connection model with a shared lock
    for transaction isolation.
    """

    def __init__(
        self,
        database_path: str,
        circuit_breaker_failures: int = 5,
        circuit_breaker_seconds: int = 30,
    ) -> None:
        """Initialize SQLite database.

        Args:
            database_path: Path to SQLite database file (or :memory:)
            circuit_breaker_failures: Failures before opening breaker
            circuit_breaker_seconds: Seconds to keep breaker open
        """
        # Remove sqlite:/// prefix if present
        if database_path.startswith("sqlite:///"):
            database_path = database_path[10:]

        self._database_path = database_path
        self._conn: sqlite3.Connection | None = None
        self._lock = threading.RLock()
        self._in_transaction = False
        self._circuit_breaker = DatabaseCircuitBreaker(
            failure_threshold=circuit_breaker_failures,
            open_seconds=circuit_breaker_seconds,
            backend="sqlite",
        )

    @property
    def dialect(self) -> str:
        """Return dialect name for query selection."""
        return "sqlite"

    def connect(self) -> None:
        """Establish database connection."""
        if self._conn is not None:
            return

        # Create directory if needed
        if self._database_path != ":memory:":
            path = Path(self._database_path)
            path.parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(
            self._database_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False,
            timeout=30.0,
        )
        self._conn.row_factory = sqlite3.Row
        # Enable foreign keys
        self._conn.execute("PRAGMA foreign_keys = ON")
        # Use WAL mode for better concurrency
        self._conn.execute("PRAGMA journal_mode = WAL")

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._conn is not None

    def _ensure_connected(self) -> sqlite3.Connection:
        """Ensure connection exists and return it."""
        if self._conn is None:
            raise DatabaseError("Database not connected. Call connect() first.")
        return self._conn

    @contextmanager
    def transaction(
        self, isolation_level: IsolationLevel | None = None
    ) -> Iterator[None]:
        """Context manager for database transactions.

        SQLite supports: DEFERRED, IMMEDIATE, EXCLUSIVE
        We map:
        - SERIALIZABLE -> EXCLUSIVE
        - READ COMMITTED -> IMMEDIATE
        - Others -> DEFERRED
        """
        conn = self._ensure_connected()

        # Map isolation levels to SQLite modes
        if isolation_level == "SERIALIZABLE":
            begin_cmd = "BEGIN EXCLUSIVE"
        elif isolation_level in ("READ COMMITTED", "REPEATABLE READ"):
            begin_cmd = "BEGIN IMMEDIATE"
        else:
            begin_cmd = "BEGIN DEFERRED"

        with self._lock:
            try:
                conn.execute(begin_cmd)
                self._in_transaction = True
                yield
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._in_transaction = False

    def _adapt_sql(self, query: str) -> str:
        """Adapt PostgreSQL-style SQL to SQLite.

        Handles:
        - $1, $2 -> ? (parameter placeholders)
        - SERIAL -> INTEGER (type mapping)
        - NOW() -> CURRENT_TIMESTAMP
        """
        # Replace $N parameters with ?
        query = re.sub(r"\$\d+", "?", query)
        # Replace SERIAL with appropriate SQLite type
        query = query.replace("SERIAL", "INTEGER")
        # Replace NOW() with CURRENT_TIMESTAMP
        query = query.replace("NOW()", "CURRENT_TIMESTAMP")
        return query

    def execute(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> None:
        """Execute a query without returning results."""
        conn = self._ensure_connected()
        query = self._adapt_sql(query)
        self._circuit_breaker.before_call()

        with self._lock:
            cursor = conn.cursor()
            try:
                if params is None:
                    cursor.execute(query)
                elif isinstance(params, dict):
                    cursor.execute(query, params)
                else:
                    cursor.execute(query, params)
                if not self._in_transaction:
                    conn.commit()
                self._circuit_breaker.record_success()
            except sqlite3.Error as e:
                self._circuit_breaker.record_failure(e)
                raise DatabaseError(f"SQLite query failed: {e}") from e
            finally:
                cursor.close()

    def execute_returning(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a query and return all results as dicts."""
        conn = self._ensure_connected()
        query = self._adapt_sql(query)
        self._circuit_breaker.before_call()

        with self._lock:
            cursor = conn.cursor()
            try:
                if params is None:
                    cursor.execute(query)
                elif isinstance(params, dict):
                    cursor.execute(query, params)
                else:
                    cursor.execute(query, params)

                rows = cursor.fetchall()
                if not rows:
                    self._circuit_breaker.record_success()
                    return []

                # Convert Row objects to dicts
                self._circuit_breaker.record_success()
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                self._circuit_breaker.record_failure(e)
                raise DatabaseError(f"SQLite query failed: {e}") from e
            finally:
                cursor.close()

    def execute_one(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Execute a query and return a single result or None."""
        results = self.execute_returning(query, params)
        return results[0] if results else None

    def execute_returning_rowcount(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> int:
        """Execute SQL and return rowcount.

        IMPORTANT: Both sqlite3 and psycopg2 expose cursor.rowcount after execute.
        This method ensures we capture it reliably.
        """
        conn = self._ensure_connected()
        query = self._adapt_sql(query)
        self._circuit_breaker.before_call()

        with self._lock:
            cursor = conn.cursor()
            try:
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                rowcount = cursor.rowcount
                if not self._in_transaction:
                    conn.commit()
                self._circuit_breaker.record_success()
                return rowcount
            except sqlite3.Error as e:
                self._circuit_breaker.record_failure(e)
                raise DatabaseError(f"SQLite query failed: {e}") from e
            finally:
                cursor.close()

    # =========================================================================
    # Block State Operations
    # =========================================================================

    def get_block_state(self, chain_id: int) -> BlockState | None:
        row = self.execute_one(
            "SELECT * FROM block_state WHERE chain_id = ?",
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
            VALUES (?, ?, ?)
            ON CONFLICT(chain_id) DO UPDATE SET
                last_processed_block_number = excluded.last_processed_block_number,
                last_processed_block_hash = excluded.last_processed_block_hash,
                updated_at = CURRENT_TIMESTAMP
            """,
            (chain_id, block_number, block_hash),
        )

    def get_block_hash_at_height(
        self, chain_id: int, block_number: int
    ) -> str | None:
        row = self.execute_one(
            "SELECT block_hash FROM block_hash_history WHERE chain_id = ? AND block_number = ?",
            (chain_id, block_number),
        )
        return row["block_hash"] if row else None

    def insert_block_hash(
        self, chain_id: int, block_number: int, block_hash: str
    ) -> None:
        self.execute(
            """
            INSERT INTO block_hash_history (chain_id, block_number, block_hash)
            VALUES (?, ?, ?)
            ON CONFLICT(chain_id, block_number) DO UPDATE SET
                block_hash = excluded.block_hash,
                inserted_at = CURRENT_TIMESTAMP
            """,
            (chain_id, block_number, block_hash),
        )

    def delete_block_hashes_above(self, chain_id: int, block_number: int) -> int:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM block_hash_history WHERE chain_id = ? AND block_number > ?",
                (chain_id, block_number),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    def delete_block_hash_at_height(self, chain_id: int, block_number: int) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM block_hash_history WHERE chain_id = ? AND block_number = ?",
                (chain_id, block_number),
            )
            deleted = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return deleted

    def cleanup_old_block_hashes(self, chain_id: int, keep_count: int) -> int:
        # Get max block number
        row = self.execute_one(
            "SELECT MAX(block_number) as max_block FROM block_hash_history WHERE chain_id = ?",
            (chain_id,),
        )
        if not row or row["max_block"] is None:
            return 0

        cutoff = row["max_block"] - keep_count + 1
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM block_hash_history WHERE chain_id = ? AND block_number < ?",
                (chain_id, cutoff),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    def get_oldest_block_in_history(self, chain_id: int) -> int | None:
        row = self.execute_one(
            "SELECT MIN(block_number) as min_block FROM block_hash_history WHERE chain_id = ?",
            (chain_id,),
        )
        return row["min_block"] if row else None

    def get_latest_block_in_history(self, chain_id: int) -> int | None:
        row = self.execute_one(
            "SELECT MAX(block_number) as max_block FROM block_hash_history WHERE chain_id = ?",
            (chain_id,),
        )
        return row["max_block"] if row else None

    # =========================================================================
    # Job Operations
    # =========================================================================

    def get_job(self, job_id: str) -> JobConfig | None:
        row = self.execute_one("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        if not row:
            return None
        return self._row_to_job_config(row)

    def get_enabled_jobs(self) -> list[JobConfig]:
        rows = self.execute_returning(
            "SELECT * FROM jobs WHERE enabled = 1 ORDER BY job_id"
        )
        return [self._row_to_job_config(row) for row in rows]

    def list_all_jobs(self) -> list[JobConfig]:
        rows = self.execute_returning("SELECT * FROM jobs ORDER BY job_id")
        return [self._row_to_job_config(row) for row in rows]

    def _row_to_job_config(self, row: dict[str, Any]) -> JobConfig:
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
            VALUES (?, ?, ?, ?)
            ON CONFLICT(job_id) DO UPDATE SET
                job_name = excluded.job_name,
                check_interval_blocks = excluded.check_interval_blocks,
                updated_at = CURRENT_TIMESTAMP
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
                    last_checked_block_number = ?,
                    last_triggered_block_number = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
                """,
                (block_number, block_number, job_id),
            )
        else:
            self.execute(
                """
                UPDATE jobs SET
                    last_checked_block_number = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
                """,
                (block_number, job_id),
            )

    def set_job_enabled(self, job_id: str, enabled: bool) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE jobs SET enabled = ?, updated_at = CURRENT_TIMESTAMP WHERE job_id = ?",
                (enabled, job_id),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def delete_job(self, job_id: str) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            # Delete job_kv entries first (foreign key)
            cursor.execute("DELETE FROM job_kv WHERE job_id = ?", (job_id,))
            cursor.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
            deleted = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return deleted

    def get_job_kv(self, job_id: str, key: str) -> Any | None:
        row = self.execute_one(
            "SELECT value_json FROM job_kv WHERE job_id = ? AND key = ?",
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
            VALUES (?, ?, ?)
            ON CONFLICT(job_id, key) DO UPDATE SET
                value_json = excluded.value_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (job_id, key, value_json),
        )

    def delete_job_kv(self, job_id: str, key: str) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM job_kv WHERE job_id = ? AND key = ?",
                (job_id, key),
            )
            deleted = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return deleted

    # =========================================================================
    # Signer & Nonce Operations
    # =========================================================================

    def get_signer_state(self, chain_id: int, address: str) -> SignerState | None:
        row = self.execute_one(
            "SELECT * FROM signers WHERE chain_id = ? AND signer_address = ?",
            (chain_id, address),
        )
        if not row:
            return None
        return self._row_to_signer_state(row)

    def get_all_signers(self, chain_id: int) -> list[SignerState]:
        rows = self.execute_returning(
            "SELECT * FROM signers WHERE chain_id = ?", (chain_id,)
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
            VALUES (?, ?, ?, ?)
            ON CONFLICT(chain_id, signer_address) DO UPDATE SET
                next_nonce = excluded.next_nonce,
                last_synced_chain_nonce = excluded.last_synced_chain_nonce,
                updated_at = CURRENT_TIMESTAMP
            """,
            (chain_id, address, next_nonce, last_synced_chain_nonce),
        )

    def update_signer_next_nonce(
        self, chain_id: int, address: str, next_nonce: int
    ) -> None:
        self.execute(
            """
            UPDATE signers SET next_nonce = ?, updated_at = CURRENT_TIMESTAMP
            WHERE chain_id = ? AND signer_address = ?
            """,
            (next_nonce, chain_id, address),
        )

    def update_signer_chain_nonce(
        self, chain_id: int, address: str, chain_nonce: int
    ) -> None:
        self.execute(
            """
            UPDATE signers SET last_synced_chain_nonce = ?, updated_at = CURRENT_TIMESTAMP
            WHERE chain_id = ? AND signer_address = ?
            """,
            (chain_nonce, chain_id, address),
        )

    def set_gap_started_at(
        self, chain_id: int, address: str, started_at: datetime
    ) -> None:
        """Record when gap blocking started for a signer."""
        self.execute(
            """
            UPDATE signers SET gap_started_at = ?, updated_at = CURRENT_TIMESTAMP
            WHERE chain_id = ? AND signer_address = ?
            """,
            (started_at.isoformat() if started_at else None, chain_id, address),
        )

    def clear_gap_started_at(self, chain_id: int, address: str) -> None:
        """Clear gap tracking (gap resolved or force reset)."""
        self.execute(
            """
            UPDATE signers SET gap_started_at = NULL, updated_at = CURRENT_TIMESTAMP
            WHERE chain_id = ? AND signer_address = ?
            """,
            (chain_id, address),
        )

    def get_signer_by_alias(self, chain_id: int, alias: str) -> SignerState | None:
        """Get signer by alias. Returns None if not found."""
        row = self.execute_one(
            """
            SELECT * FROM signers
            WHERE chain_id = ? AND alias = ?
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
        conn = self._ensure_connected()
        intent_id_str = str(intent_id) if intent_id else None
        with self._lock:
            try:
                conn.execute("BEGIN IMMEDIATE")
                self._in_transaction = True

                conn.execute(
                    """
                    INSERT INTO signers (chain_id, signer_address, next_nonce, last_synced_chain_nonce)
                    VALUES (?, ?, 0, NULL)
                    ON CONFLICT(chain_id, signer_address) DO NOTHING
                    """,
                    (chain_id, address),
                )

                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT next_nonce FROM signers
                    WHERE chain_id = ? AND signer_address = ?
                    """,
                    (chain_id, address),
                )
                row = cursor.fetchone()
                cursor.close()
                if row is None:
                    raise DatabaseError("Failed to lock signer row")

                db_next_nonce = row["next_nonce"]
                base_nonce = chain_nonce if chain_nonce is not None else db_next_nonce

                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT nonce FROM nonce_reservations
                    WHERE chain_id = ? AND signer_address = ?
                    AND status != ?
                    AND nonce >= ?
                    ORDER BY nonce
                    """,
                    (chain_id, address, NonceStatus.RELEASED.value, base_nonce),
                )
                rows = cursor.fetchall()
                cursor.close()

                candidate = base_nonce
                for res in rows:
                    if res["nonce"] == candidate:
                        candidate += 1
                    elif res["nonce"] > candidate:
                        break

                if candidate - base_nonce > 100:
                    raise DatabaseError(
                        f"Could not find available nonce within 100 slots for signer {address}"
                    )

                conn.execute(
                    """
                    INSERT INTO nonce_reservations (chain_id, signer_address, nonce, status, intent_id)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(chain_id, signer_address, nonce) DO UPDATE SET
                        status = excluded.status,
                        intent_id = excluded.intent_id,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (chain_id, address, candidate, NonceStatus.RESERVED.value, intent_id_str),
                )

                new_next_nonce = max(db_next_nonce, candidate + 1)
                conn.execute(
                    """
                    UPDATE signers SET next_nonce = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE chain_id = ? AND signer_address = ?
                    """,
                    (new_next_nonce, chain_id, address),
                )

                conn.commit()
                return candidate
            except Exception:
                conn.rollback()
                raise
            finally:
                self._in_transaction = False

    def get_nonce_reservation(
        self, chain_id: int, address: str, nonce: int
    ) -> NonceReservation | None:
        row = self.execute_one(
            """
            SELECT * FROM nonce_reservations
            WHERE chain_id = ? AND signer_address = ? AND nonce = ?
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
                WHERE chain_id = ? AND signer_address = ? AND status = ?
                ORDER BY nonce
                """,
                (chain_id, address, status),
            )
        else:
            rows = self.execute_returning(
                """
                SELECT * FROM nonce_reservations
                WHERE chain_id = ? AND signer_address = ?
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
            WHERE chain_id = ? AND signer_address = ? AND nonce < ?
            ORDER BY nonce
            """,
            (chain_id, address, nonce),
        )
        return [self._row_to_nonce_reservation(row) for row in rows]

    def _row_to_nonce_reservation(self, row: dict[str, Any]) -> NonceReservation:
        intent_id = row["intent_id"]
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

    def create_nonce_reservation(
        self,
        chain_id: int,
        address: str,
        nonce: int,
        status: str = "reserved",
        intent_id: UUID | None = None,
    ) -> NonceReservation:
        intent_id_str = str(intent_id) if intent_id else None
        self.execute(
            """
            INSERT INTO nonce_reservations (chain_id, signer_address, nonce, status, intent_id)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(chain_id, signer_address, nonce) DO UPDATE SET
                status = excluded.status,
                intent_id = excluded.intent_id,
                updated_at = CURRENT_TIMESTAMP
            """,
            (chain_id, address, nonce, status, intent_id_str),
        )
        # Fetch and return the reservation
        reservation = self.get_nonce_reservation(chain_id, address, nonce)
        if not reservation:
            raise DatabaseError("Failed to create nonce reservation")
        return reservation

    def update_nonce_reservation_status(
        self,
        chain_id: int,
        address: str,
        nonce: int,
        status: str,
        intent_id: UUID | None = None,
    ) -> bool:
        conn = self._ensure_connected()
        intent_id_str = str(intent_id) if intent_id else None
        with self._lock:
            cursor = conn.cursor()
            if intent_id_str:
                cursor.execute(
                    """
                    UPDATE nonce_reservations SET status = ?, intent_id = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE chain_id = ? AND signer_address = ? AND nonce = ?
                    """,
                    (status, intent_id_str, chain_id, address, nonce),
                )
            else:
                cursor.execute(
                    """
                    UPDATE nonce_reservations SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE chain_id = ? AND signer_address = ? AND nonce = ?
                    """,
                    (status, chain_id, address, nonce),
                )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def release_nonce_reservation(
        self, chain_id: int, address: str, nonce: int
    ) -> bool:
        return self.update_nonce_reservation_status(
            chain_id, address, nonce, "released"
        )

    def cleanup_orphaned_nonces(
        self, chain_id: int, older_than_hours: int = 24
    ) -> int:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    DELETE FROM nonce_reservations
                    WHERE chain_id = ?
                      AND status = 'orphaned'
                      AND updated_at < datetime('now', ? || ' hours')
                    """,
                    (chain_id, f"-{older_than_hours}"),
                )
                deleted = cursor.rowcount
                if not self._in_transaction:
                    conn.commit()
                return deleted
            finally:
                cursor.close()

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
        metadata: dict | None = None,
    ) -> TxIntent | None:
        signer_address = signer_address.lower()
        try:
            self.execute(
                """
                INSERT INTO tx_intents (
                    intent_id, job_id, chain_id, signer_address, idempotency_key,
                    to_address, data, value_wei, gas_limit, max_fee_per_gas,
                    max_priority_fee_per_gas, min_confirmations, deadline_ts,
                    broadcast_group, broadcast_endpoints_json, retry_after, status,
                    metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, 'created', ?)
                """,
                (
                    str(intent_id),
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
                    json.dumps(metadata) if metadata else None,
                ),
            )
            return self.get_intent(intent_id)
        except sqlite3.IntegrityError:
            # Idempotency key already exists
            return None
        except DatabaseError as e:
            if "UNIQUE constraint failed" in str(e):
                return None
            raise

    def get_intent(self, intent_id: UUID) -> TxIntent | None:
        row = self.execute_one(
            "SELECT * FROM tx_intents WHERE intent_id = ?",
            (str(intent_id),),
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
            "SELECT * FROM tx_intents WHERE chain_id = ? AND signer_address = ? AND idempotency_key = ?",
            (chain_id, signer_address.lower(), idempotency_key),
        )
        if not row:
            return None
        return self._row_to_intent(row)

    def _row_to_intent(self, row: dict[str, Any]) -> TxIntent:
        intent_id = row["intent_id"]
        if isinstance(intent_id, str):
            intent_id = UUID(intent_id)
        # Parse metadata_json
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
            retry_after=row["retry_after"],
            retry_count=row.get("retry_count", 0),
            status=IntentStatus(row["status"]),
            claim_token=row["claim_token"],
            claimed_at=row["claimed_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            # Broadcast binding (may be None if not yet broadcast)
            broadcast_group=row.get("broadcast_group"),
            broadcast_endpoints_json=row.get("broadcast_endpoints_json"),
            metadata=metadata,
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

        placeholders = ",".join("?" * len(status))
        query = f"SELECT * FROM tx_intents WHERE status IN ({placeholders})"
        params: list[Any] = list(status)

        if chain_id is not None:
            query += " AND chain_id = ?"
            params.append(chain_id)
        if job_id is not None:
            query += " AND job_id = ?"
            params.append(job_id)

        query += " ORDER BY created_at ASC LIMIT ?"
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
            query += " AND status = ?"
            params.append(status)
        if job_id is not None:
            query += " AND job_id = ?"
            params.append(job_id)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        return self.execute_returning(query, tuple(params))

    def get_active_intent_count(self, job_id: str, chain_id: int | None = None) -> int:
        statuses = [
            IntentStatus.CREATED.value,
            IntentStatus.CLAIMED.value,
            IntentStatus.SENDING.value,
            IntentStatus.PENDING.value,
        ]
        placeholders = ",".join("?" * len(statuses))
        query = f"SELECT COUNT(*) AS count FROM tx_intents WHERE status IN ({placeholders}) AND job_id = ?"
        params: list[Any] = list(statuses)
        params.append(job_id)
        if chain_id is not None:
            query += " AND chain_id = ?"
            params.append(chain_id)
        row = self.execute_one(query, tuple(params))
        return int(row["count"]) if row else 0

    def get_pending_intent_count(self, chain_id: int | None = None) -> int:
        statuses = [
            IntentStatus.CREATED.value,
            IntentStatus.CLAIMED.value,
            IntentStatus.SENDING.value,
            IntentStatus.PENDING.value,
        ]
        placeholders = ",".join("?" * len(statuses))
        query = f"SELECT COUNT(*) AS count FROM tx_intents WHERE status IN ({placeholders})"
        params: list[Any] = list(statuses)
        if chain_id is not None:
            query += " AND chain_id = ?"
            params.append(chain_id)
        row = self.execute_one(query, tuple(params))
        return int(row["count"]) if row else 0

    def get_backing_off_intent_count(self, chain_id: int | None = None) -> int:
        query = "SELECT COUNT(*) AS count FROM tx_intents WHERE retry_after > CURRENT_TIMESTAMP"
        params: list[Any] = []
        if chain_id is not None:
            query += " AND chain_id = ?"
            params.append(chain_id)
        row = self.execute_one(query, tuple(params))
        return int(row["count"]) if row else 0

    def get_oldest_pending_intent_age(self, chain_id: int) -> float | None:
        query = """
            SELECT (julianday('now') - julianday(MIN(created_at))) * 86400 AS age_seconds
            FROM tx_intents
            WHERE chain_id = ?
              AND status IN ('created', 'pending', 'claimed', 'sending')
        """
        result = self.execute_one(query, (chain_id,))
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
            chain_clause = " AND chain_id = ?"
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
        AND updated_at < datetime('now', ? || ' seconds')

        LIMIT ?
        """
        params_with_age = chain_params + [f"-{max_age_seconds}", limit]
        rows = self.execute_returning(query, tuple(params_with_age))
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
        AND updated_at < datetime('now', ? || ' seconds')
        """
        params: list[Any] = [f"-{max_age_seconds}"]
        if chain_id is not None:
            query += " AND chain_id = ?"
            params.append(chain_id)
        query += " ORDER BY updated_at ASC LIMIT ?"
        params.append(limit)
        rows = self.execute_returning(query, tuple(params))
        return [self._row_to_intent(row) for row in rows]

    def claim_next_intent(
        self,
        claim_token: str,
        claimed_by: str | None = None,
    ) -> TxIntent | None:
        """Claim the next available intent for processing.

        SQLite version uses deterministic ordering with immediate lock.
        """
        conn = self._ensure_connected()
        with self._lock:
            # Use IMMEDIATE transaction for claiming
            conn.execute("BEGIN IMMEDIATE")
            try:
                cursor = conn.cursor()
                # Find and claim in one atomic operation
                cursor.execute(
                    """
                    UPDATE tx_intents
                    SET status = 'claimed', claim_token = ?, claimed_at = CURRENT_TIMESTAMP,
                        claimed_by = ?,
                        retry_after = NULL,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE intent_id = (
                        SELECT intent_id FROM tx_intents
                        WHERE status = 'created'
                        AND (deadline_ts IS NULL OR deadline_ts > CURRENT_TIMESTAMP)
                        AND (retry_after IS NULL OR retry_after <= CURRENT_TIMESTAMP)
                        ORDER BY created_at ASC, intent_id ASC
                        LIMIT 1
                    )
                    AND status = 'created'
                    """,
                    (claim_token, claimed_by),
                )

                if cursor.rowcount == 0:
                    conn.rollback()
                    cursor.close()
                    return None

                # Get the claimed intent
                cursor.execute(
                    "SELECT * FROM tx_intents WHERE claim_token = ? AND status = 'claimed'",
                    (claim_token,),
                )
                row = cursor.fetchone()
                conn.commit()
                cursor.close()

                if row:
                    return self._row_to_intent(dict(row))
                return None
            except Exception:
                conn.rollback()
                raise

    def update_intent_status(
        self,
        intent_id: UUID,
        status: str,
        claim_token: str | None = None,
    ) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            if claim_token:
                cursor.execute(
                    """
                    UPDATE tx_intents SET status = ?, claim_token = ?,
                        claimed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                    WHERE intent_id = ?
                    """,
                    (status, claim_token, str(intent_id)),
                )
            else:
                cursor.execute(
                    """
                    UPDATE tx_intents SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE intent_id = ?
                    """,
                    (status, str(intent_id)),
                )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def update_intent_status_if(
        self,
        intent_id: UUID,
        status: str,
        expected_status: str | list[str],
    ) -> bool:
        if isinstance(expected_status, str):
            expected_status = [expected_status]
        placeholders = ",".join("?" * len(expected_status))
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE tx_intents SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE intent_id = ? AND status IN ({placeholders})
                """,
                (status, str(intent_id), *expected_status),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def transition_intent_status(
        self,
        intent_id: UUID,
        from_statuses: list[str],
        to_status: str,
    ) -> tuple[bool, str | None]:
        """Atomic status transition with conditional claim clearing.

        SQLite version: uses BEGIN IMMEDIATE for fewer lock surprises,
        then SELECT + UPDATE with WHERE status guard.
        """
        conn = self._ensure_connected()
        placeholders = ",".join("?" * len(from_statuses))

        with self._lock:
            cursor = conn.cursor()
            started_tx = False
            if not self._in_transaction:
                # BEGIN IMMEDIATE to acquire write lock early
                cursor.execute("BEGIN IMMEDIATE")
                started_tx = True

            try:
                # Get current status (within transaction)
                cursor.execute(
                    "SELECT status FROM tx_intents WHERE intent_id = ?",
                    (str(intent_id),)
                )
                row = cursor.fetchone()
                if not row:
                    if started_tx:
                        conn.rollback()
                    cursor.close()
                    return (False, None)

                old_status = row[0]

                # Check if transition is allowed
                if old_status not in from_statuses:
                    if started_tx:
                        conn.rollback()
                    cursor.close()
                    return (False, None)

                # Clear claim only if leaving 'claimed' (not claimed->claimed)
                should_clear_claim = old_status == "claimed" and to_status != "claimed"

                if should_clear_claim:
                    cursor.execute(
                        f"""
                        UPDATE tx_intents
                        SET status = ?,
                            updated_at = CURRENT_TIMESTAMP,
                            claim_token = NULL,
                            claimed_at = NULL,
                            claimed_by = NULL
                        WHERE intent_id = ? AND status IN ({placeholders})
                        """,
                        (to_status, str(intent_id), *from_statuses),
                    )
                else:
                    cursor.execute(
                        f"""
                        UPDATE tx_intents
                        SET status = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE intent_id = ? AND status IN ({placeholders})
                        """,
                        (to_status, str(intent_id), *from_statuses),
                    )

                if cursor.rowcount == 0:
                    # Lost race - status changed between SELECT and UPDATE
                    if started_tx:
                        conn.rollback()
                    cursor.close()
                    return (False, None)

                if started_tx:
                    conn.commit()
                cursor.close()
                return (True, old_status)

            except Exception:
                if started_tx:
                    conn.rollback()
                cursor.close()
                raise

    def update_intent_signer(self, intent_id: UUID, signer_address: str) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents SET signer_address = ?, updated_at = CURRENT_TIMESTAMP
                WHERE intent_id = ?
                """,
                (signer_address.lower(), str(intent_id)),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def release_intent_claim(self, intent_id: UUID) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents SET status = 'created', claim_token = NULL,
                    claimed_at = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE intent_id = ? AND status = 'claimed'
                """,
                (str(intent_id),),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def release_intent_claim_if_token(self, intent_id: UUID, claim_token: str) -> bool:
        rowcount = self.execute_returning_rowcount(
            """
            UPDATE tx_intents
            SET status = 'created',
                claim_token = NULL,
                claimed_at = NULL,
                claimed_by = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE intent_id = ? AND claim_token = ? AND status = 'claimed'
            """,
            (str(intent_id), claim_token),
        )
        return rowcount == 1

    def clear_intent_claim(self, intent_id: UUID) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents
                SET claim_token = NULL, claimed_at = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE intent_id = ?
                """,
                (str(intent_id),),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def set_intent_retry_after(self, intent_id: UUID, retry_after: datetime | None) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents
                SET retry_after = ?, updated_at = CURRENT_TIMESTAMP
                WHERE intent_id = ?
                """,
                (retry_after, str(intent_id)),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def increment_intent_retry_count(self, intent_id: UUID) -> int:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents
                SET retry_count = retry_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE intent_id = ?
                """,
                (str(intent_id),),
            )
            if cursor.rowcount == 0:
                cursor.close()
                return 0
            cursor.execute(
                "SELECT retry_count FROM tx_intents WHERE intent_id = ?",
                (str(intent_id),),
            )
            row = cursor.fetchone()
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return row[0] if row else 0

    def release_stale_intent_claims(self, max_age_seconds: int) -> int:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents
                SET status = 'created', claim_token = NULL, claimed_at = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE status = 'claimed'
                AND claimed_at < datetime('now', ? || ' seconds')
                AND NOT EXISTS (
                    SELECT 1 FROM tx_attempts WHERE tx_attempts.intent_id = tx_intents.intent_id
                )
                """,
                (f"-{max_age_seconds}",),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    def abandon_intent(self, intent_id: UUID) -> bool:
        return self.update_intent_status(intent_id, "abandoned")

    def get_pending_intents_for_signer(
        self, chain_id: int, address: str
    ) -> list[TxIntent]:
        rows = self.execute_returning(
            """
            SELECT * FROM tx_intents
            WHERE chain_id = ? AND signer_address = ?
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
            WHERE intent_id = ?
            """,
            (str(intent_id),),
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
        replaces_str = str(replaces_attempt_id) if replaces_attempt_id else None
        conn = self._ensure_connected()

        with self._lock:
            try:
                conn.execute("BEGIN IMMEDIATE")
                self._in_transaction = True

                if binding is not None:
                    # First broadcast: check existence + binding state for clear error messages
                    # (The UPDATE's WHERE clause is the true guard; this is for diagnostics)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT broadcast_endpoints_json FROM tx_intents WHERE intent_id = ?",
                        (str(intent_id),),
                    )
                    row = cursor.fetchone()
                    cursor.close()

                    if not row:
                        raise ValueError(f"Intent {intent_id} not found")
                    if row["broadcast_endpoints_json"] is not None:
                        raise ValueError(
                            f"Intent {intent_id} already bound. "
                            f"Cannot rebind — may indicate race condition."
                        )

                    group_name, endpoints = binding
                    # Defensive copy — don't persist a list that might be mutated elsewhere
                    endpoints_snapshot = list(endpoints)

                    rowcount = self.execute_returning_rowcount(
                        """
                        UPDATE tx_intents
                        SET broadcast_group = ?,
                            broadcast_endpoints_json = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE intent_id = ?
                          AND broadcast_endpoints_json IS NULL
                        """,
                        (
                            group_name,
                            json.dumps(endpoints_snapshot),
                            str(intent_id),
                        ),
                    )

                    # Rowcount check guards against TOCTOU race (SELECT passed but UPDATE lost)
                    if rowcount != 1:
                        raise ValueError(
                            f"Binding race condition for intent {intent_id}: "
                            f"another process bound it between SELECT and UPDATE"
                        )

                # Create attempt with broadcast audit fields
                conn.execute(
                    """
                    INSERT INTO tx_attempts (
                        attempt_id, intent_id, nonce, gas_params_json, status,
                        tx_hash, replaces_attempt_id, broadcast_group, endpoint_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(attempt_id),
                        str(intent_id),
                        nonce,
                        gas_params_json,
                        status,
                        tx_hash,
                        replaces_str,
                        broadcast_group,
                        endpoint_url,
                    ),
                )

                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._in_transaction = False

        attempt = self.get_attempt(attempt_id)
        if not attempt:
            raise DatabaseError("Failed to create attempt")
        return attempt

    def get_attempt(self, attempt_id: UUID) -> TxAttempt | None:
        row = self.execute_one(
            "SELECT * FROM tx_attempts WHERE attempt_id = ?",
            (str(attempt_id),),
        )
        if not row:
            return None
        return self._row_to_attempt(row)

    def get_attempts_for_intent(self, intent_id: UUID) -> list[TxAttempt]:
        rows = self.execute_returning(
            "SELECT * FROM tx_attempts WHERE intent_id = ? ORDER BY created_at",
            (str(intent_id),),
        )
        return [self._row_to_attempt(row) for row in rows]

    def get_latest_attempt_for_intent(self, intent_id: UUID) -> TxAttempt | None:
        row = self.execute_one(
            """
            SELECT * FROM tx_attempts WHERE intent_id = ?
            ORDER BY created_at DESC LIMIT 1
            """,
            (str(intent_id),),
        )
        if not row:
            return None
        return self._row_to_attempt(row)

    def get_attempt_by_tx_hash(self, tx_hash: str) -> TxAttempt | None:
        row = self.execute_one(
            "SELECT * FROM tx_attempts WHERE tx_hash = ?",
            (tx_hash,),
        )
        if not row:
            return None
        return self._row_to_attempt(row)

    def _row_to_attempt(self, row: dict[str, Any]) -> TxAttempt:
        attempt_id = row["attempt_id"]
        if isinstance(attempt_id, str):
            attempt_id = UUID(attempt_id)
        intent_id = row["intent_id"]
        if isinstance(intent_id, str):
            intent_id = UUID(intent_id)
        replaces = row["replaces_attempt_id"]
        if replaces and isinstance(replaces, str):
            replaces = UUID(replaces)
        return TxAttempt(
            attempt_id=attempt_id,
            intent_id=intent_id,
            nonce=row["nonce"],
            tx_hash=row["tx_hash"],
            gas_params=GasParams.from_json(row["gas_params_json"]),
            status=AttemptStatus(row["status"]),
            error_code=row["error_code"],
            error_detail=row["error_detail"],
            replaces_attempt_id=replaces,
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
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            # Build dynamic update
            updates = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
            params: list[Any] = [status]

            if tx_hash is not None:
                updates.append("tx_hash = ?")
                params.append(tx_hash)
            if broadcast_block is not None:
                updates.append("broadcast_block = ?")
                params.append(broadcast_block)
            if broadcast_at is not None:
                updates.append("broadcast_at = ?")
                params.append(broadcast_at)
            if included_block is not None:
                updates.append("included_block = ?")
                params.append(included_block)
            if error_code is not None:
                updates.append("error_code = ?")
                params.append(error_code)
            if error_detail is not None:
                updates.append("error_detail = ?")
                params.append(error_detail)

            params.append(str(attempt_id))
            query = f"UPDATE tx_attempts SET {', '.join(updates)} WHERE attempt_id = ?"
            cursor.execute(query, params)
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

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
        conn = self._ensure_connected()

        with self._lock:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO transactions (
                        tx_id, job_id, chain_id, idempotency_key,
                        signer_address, to_address, data, value_wei,
                        min_confirmations, deadline_ts, status,
                        replacement_count, gas_params_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'created', 0, ?)
                    """,
                    (
                        str(tx_id),
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
                if not self._in_transaction:
                    conn.commit()
                cursor.close()
                return self.get_tx(tx_id)
            except sqlite3.IntegrityError:
                # Idempotency key already exists
                cursor.close()
                return None

    def get_tx(self, tx_id: UUID) -> Transaction | None:
        """Get a transaction by ID."""
        row = self.execute_one(
            "SELECT * FROM transactions WHERE tx_id = ?",
            (str(tx_id),),
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
            "SELECT * FROM transactions WHERE chain_id = ? AND signer_address = ? AND idempotency_key = ?",
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
            "SELECT * FROM transactions WHERE current_tx_hash = ?",
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

        if chain_id is not None:
            query += " AND chain_id = ?"
            params.append(chain_id)
        if job_id is not None:
            query += " AND job_id = ?"
            params.append(job_id)

        query += " ORDER BY created_at ASC"
        rows = self.execute_returning(query, tuple(params))
        return [self._row_to_transaction(row) for row in rows]

    def claim_tx(self, claim_token: str) -> Transaction | None:
        """Claim the next CREATED transaction for processing.

        Status remains CREATED while claimed - no "claimed" status.
        """
        conn = self._ensure_connected()
        with self._lock:
            conn.execute("BEGIN IMMEDIATE")
            try:
                cursor = conn.cursor()
                # Find and claim atomically
                cursor.execute(
                    """
                    UPDATE transactions
                    SET claim_token = ?, claimed_at = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE tx_id = (
                        SELECT tx_id FROM transactions
                        WHERE status = 'created'
                        AND claim_token IS NULL
                        AND (deadline_ts IS NULL OR deadline_ts > CURRENT_TIMESTAMP)
                        ORDER BY created_at ASC, tx_id ASC
                        LIMIT 1
                    )
                    AND status = 'created'
                    AND claim_token IS NULL
                    """,
                    (claim_token,),
                )

                if cursor.rowcount == 0:
                    conn.rollback()
                    cursor.close()
                    return None

                # Get the claimed transaction
                cursor.execute(
                    "SELECT * FROM transactions WHERE claim_token = ? AND status = 'created'",
                    (claim_token,),
                )
                row = cursor.fetchone()
                conn.commit()
                cursor.close()

                if row:
                    return self._row_to_transaction(dict(row))
                return None
            except Exception:
                conn.rollback()
                raise

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
        conn = self._ensure_connected()
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

        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE transactions
                SET status = 'broadcast',
                    current_tx_hash = ?,
                    current_nonce = ?,
                    gas_params_json = ?,
                    broadcast_info_json = ?,
                    tx_hash_history = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tx_id = ?
                AND status = 'created'
                """,
                (
                    tx_hash,
                    nonce,
                    gas_params.to_json(),
                    broadcast_info.to_json() if broadcast_info else None,
                    tx_hash_history,
                    str(tx_id),
                ),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

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
        conn = self._ensure_connected()
        now = datetime.now(timezone.utc)

        with self._lock:
            # First, get current state to update history
            cursor = conn.cursor()
            cursor.execute(
                "SELECT current_nonce, tx_hash_history FROM transactions WHERE tx_id = ? AND status = 'broadcast'",
                (str(tx_id),),
            )
            row = cursor.fetchone()
            if not row:
                cursor.close()
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

            cursor.execute(
                """
                UPDATE transactions
                SET current_tx_hash = ?,
                    gas_params_json = ?,
                    tx_hash_history = ?,
                    replacement_count = replacement_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tx_id = ?
                AND status = 'broadcast'
                """,
                (
                    new_tx_hash,
                    gas_params.to_json(),
                    json.dumps(existing_history),
                    str(tx_id),
                ),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def set_tx_confirmed(
        self,
        tx_id: UUID,
        included_block: int,
    ) -> bool:
        """Mark transaction confirmed.

        Sets status=CONFIRMED, included_block, confirmed_at.
        Updates tx_hash_history with outcome.
        """
        conn = self._ensure_connected()
        now = datetime.now(timezone.utc)

        with self._lock:
            # Update history outcome
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tx_hash_history FROM transactions WHERE tx_id = ? AND status = 'broadcast'",
                (str(tx_id),),
            )
            row = cursor.fetchone()
            if not row:
                cursor.close()
                return False

            existing_history = json.loads(row["tx_hash_history"]) if row["tx_hash_history"] else []
            if existing_history:
                existing_history[-1]["outcome"] = "confirmed"

            cursor.execute(
                """
                UPDATE transactions
                SET status = 'confirmed',
                    included_block = ?,
                    confirmed_at = ?,
                    tx_hash_history = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tx_id = ?
                AND status = 'broadcast'
                """,
                (
                    included_block,
                    now,
                    json.dumps(existing_history),
                    str(tx_id),
                ),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

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
        conn = self._ensure_connected()

        # Serialize error_info
        error_info_json = None
        if error_info:
            error_info_json = json.dumps({
                "error_type": error_info.error_type,
                "message": error_info.message,
                "code": error_info.code,
            })

        with self._lock:
            # Get and update history if broadcast
            cursor = conn.cursor()
            cursor.execute(
                "SELECT status, tx_hash_history FROM transactions WHERE tx_id = ? AND status IN ('created', 'broadcast')",
                (str(tx_id),),
            )
            row = cursor.fetchone()
            if not row:
                cursor.close()
                return False

            existing_history = json.loads(row["tx_hash_history"]) if row["tx_hash_history"] else []
            if existing_history and row["status"] == "broadcast":
                existing_history[-1]["outcome"] = "failed"

            cursor.execute(
                """
                UPDATE transactions
                SET status = 'failed',
                    failure_type = ?,
                    error_info_json = ?,
                    tx_hash_history = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE tx_id = ?
                AND status IN ('created', 'broadcast')
                """,
                (
                    failure_type.value,
                    error_info_json,
                    json.dumps(existing_history) if existing_history else None,
                    str(tx_id),
                ),
            )
            updated = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return updated

    def release_stale_tx_claims(self, max_age_seconds: int) -> int:
        """Release claims older than threshold. 0 = release all claims."""
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            if max_age_seconds == 0:
                # Release ALL claims
                cursor.execute(
                    """
                    UPDATE transactions
                    SET claim_token = NULL, claimed_at = NULL,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE status = 'created'
                    AND claim_token IS NOT NULL
                    """
                )
            else:
                cursor.execute(
                    """
                    UPDATE transactions
                    SET claim_token = NULL, claimed_at = NULL,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE status = 'created'
                    AND claim_token IS NOT NULL
                    AND claimed_at < datetime('now', ? || ' seconds')
                    """,
                    (f"-{max_age_seconds}",),
                )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

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
            "SELECT * FROM abi_cache WHERE chain_id = ? AND address = ?",
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
            VALUES (?, ?, ?, ?)
            ON CONFLICT(chain_id, address) DO UPDATE SET
                abi_json = excluded.abi_json,
                source = excluded.source,
                resolved_at = CURRENT_TIMESTAMP
            """,
            (chain_id, address, abi_json, source),
        )

    def clear_cached_abi(self, chain_id: int, address: str) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM abi_cache WHERE chain_id = ? AND address = ?",
                (chain_id, address),
            )
            deleted = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return deleted

    def cleanup_expired_abis(self, max_age_seconds: int) -> int:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM abi_cache
                WHERE resolved_at < datetime('now', ? || ' seconds')
                """,
                (f"-{max_age_seconds}",),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    # =========================================================================
    # Proxy Cache Operations
    # =========================================================================

    def get_cached_proxy(
        self, chain_id: int, proxy_address: str
    ) -> ProxyCacheEntry | None:
        row = self.execute_one(
            "SELECT * FROM proxy_cache WHERE chain_id = ? AND proxy_address = ?",
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
            VALUES (?, ?, ?)
            ON CONFLICT(chain_id, proxy_address) DO UPDATE SET
                implementation_address = excluded.implementation_address,
                resolved_at = CURRENT_TIMESTAMP
            """,
            (chain_id, proxy_address, implementation_address),
        )

    def clear_cached_proxy(self, chain_id: int, proxy_address: str) -> bool:
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM proxy_cache WHERE chain_id = ? AND proxy_address = ?",
                (chain_id, proxy_address),
            )
            deleted = cursor.rowcount > 0
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return deleted

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

        conn = self._ensure_connected()
        placeholders = ",".join("?" * len(statuses))

        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                DELETE FROM tx_intents
                WHERE status IN ({placeholders})
                AND created_at < datetime('now', ? || ' days')
                """,
                (*statuses, f"-{older_than_days}"),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    def get_database_stats(self) -> dict[str, Any]:
        """Get database statistics for health checks."""
        stats: dict[str, Any] = {"type": "sqlite", "path": self._database_path}

        # Count intents by status
        rows = self.execute_returning(
            "SELECT status, COUNT(*) as count FROM tx_intents GROUP BY status"
        )
        stats["intents_by_status"] = {row["status"]: row["count"] for row in rows}

        # Count total jobs
        row = self.execute_one("SELECT COUNT(*) as count FROM jobs")
        stats["total_jobs"] = row["count"] if row else 0

        # Count enabled jobs
        row = self.execute_one("SELECT COUNT(*) as count FROM jobs WHERE enabled = 1")
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

        return stats

    # =========================================================================
    # Reconciliation Operations
    # =========================================================================

    def clear_orphaned_claims(self, chain_id: int, older_than_minutes: int = 2) -> int:
        """Clear claim fields where status != 'claimed' and claim is stale."""
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tx_intents
                SET claim_token = NULL,
                    claimed_at = NULL,
                    claimed_by = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE chain_id = ?
                  AND status != 'claimed'
                  AND claim_token IS NOT NULL
                  AND claimed_at IS NOT NULL
                  AND claimed_at < datetime('now', ? || ' minutes')
                """,
                (chain_id, f"-{older_than_minutes}"),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    def release_orphaned_nonces(self, chain_id: int, older_than_minutes: int = 5) -> int:
        """Release nonces for terminal intents that are stale."""
        # SQLite doesn't support UPDATE...FROM, use subquery
        conn = self._ensure_connected()
        with self._lock:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE nonce_reservations
                SET status = 'released',
                    updated_at = CURRENT_TIMESTAMP
                WHERE chain_id = ?
                  AND status = 'reserved'
                  AND updated_at < datetime('now', ? || ' minutes')
                  AND intent_id IN (
                      SELECT intent_id FROM tx_intents
                      WHERE status IN ('failed', 'abandoned', 'reverted')
                      AND updated_at < datetime('now', ? || ' minutes')
                  )
                """,
                (chain_id, f"-{older_than_minutes}", f"-{older_than_minutes}"),
            )
            count = cursor.rowcount
            if not self._in_transaction:
                conn.commit()
            cursor.close()
            return count

    def count_pending_without_attempts(self, chain_id: int) -> int:
        """Count pending intents with no attempt records (integrity issue)."""
        result = self.execute_one(
            """
            SELECT COUNT(*) as count
            FROM tx_intents ti
            LEFT JOIN tx_attempts ta ON ti.intent_id = ta.intent_id
            WHERE ti.chain_id = ?
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
            WHERE chain_id = ?
              AND status = 'claimed'
              AND claimed_at IS NOT NULL
              AND claimed_at < datetime('now', ? || ' minutes')
            """,
            (chain_id, f"-{older_than_minutes}"),
        )
        return result["count"] if result else 0

    # =========================================================================
    # Invariant Queries (Phase 2)
    # =========================================================================

    def count_stuck_claimed(self, chain_id: int, older_than_minutes: int = 10) -> int:
        """Count intents stuck in CLAIMED status for too long."""
        conn = self._ensure_connected()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM tx_intents
            WHERE chain_id = ?
              AND status = 'claimed'
              AND datetime(claimed_at) < datetime('now', ? || ' minutes')
            """,
            (chain_id, -older_than_minutes),
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def count_orphaned_claims(self, chain_id: int) -> int:
        """Count intents with claim_token set but status != claimed."""
        conn = self._ensure_connected()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM tx_intents
            WHERE chain_id = ?
              AND status != 'claimed'
              AND claim_token IS NOT NULL
            """,
            (chain_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def count_orphaned_nonces(self, chain_id: int) -> int:
        """Count reserved/in_flight nonces for failed/abandoned intents."""
        conn = self._ensure_connected()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM nonce_reservations nr
            JOIN tx_intents ti ON nr.intent_id = ti.intent_id
            WHERE nr.chain_id = ?
              AND nr.status IN ('reserved', 'in_flight')
              AND ti.status IN ('failed', 'abandoned', 'reverted')
            """,
            (chain_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def get_oldest_nonce_gap_age_seconds(self, chain_id: int) -> float:
        """Get age in seconds of the oldest nonce gap.

        Anchors from signers (small table) for efficiency.
        Returns 0 if no gaps or if chain nonce not synced.
        """
        conn = self._ensure_connected()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COALESCE(
                (julianday('now') - julianday(datetime(MIN(nr.created_at)))) * 86400,
                0
            ) AS oldest_gap_seconds
            FROM signers s
            JOIN nonce_reservations nr
              ON nr.chain_id = s.chain_id
             AND nr.signer_address = s.signer_address
            WHERE s.chain_id = ?
              AND s.last_synced_chain_nonce IS NOT NULL
              AND nr.status IN ('reserved', 'in_flight')
              AND nr.nonce < s.last_synced_chain_nonce
            """,
            (chain_id,),
        )
        row = cursor.fetchone()
        return float(row[0]) if row else 0.0
