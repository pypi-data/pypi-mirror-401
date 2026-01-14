"""SQLite database implementation.

Slim execution layer with 4 primitives. All business operations live in db/ops/.
Uses single connection with WAL mode.

SQLite supports :name placeholders natively with dict params.
"""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from brawny.db.base_new import Database, Dialect, IsolationLevel
from brawny.model.errors import DatabaseError


def _adapt_datetime(dt: datetime) -> str:
    """Adapt datetime to ISO format string for SQLite."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _convert_datetime(val: bytes) -> datetime:
    """Convert ISO format string from SQLite to datetime."""
    s = val.decode("utf-8")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        # Handle format without timezone
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


# Register adapters globally
sqlite3.register_adapter(datetime, _adapt_datetime)
sqlite3.register_converter("TIMESTAMP", _convert_datetime)


def _dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict[str, Any]:
    """Row factory that returns dict rows."""
    cols = [d[0] for d in cursor.description]
    return dict(zip(cols, row))


class SQLiteDatabase(Database):
    """SQLite implementation with single connection.

    Uses WAL mode for better concurrency. Thread safety via lock.
    Queries use :name placeholders natively.
    """

    def __init__(self, database_path: str) -> None:
        """Initialize SQLite database.

        Args:
            database_path: Path to SQLite database file (or :memory:)
        """
        # Remove sqlite:/// prefix if present
        if database_path.startswith("sqlite:///"):
            database_path = database_path[10:]

        self._database_path = database_path
        self._conn: sqlite3.Connection | None = None
        self._lock = threading.RLock()
        self._in_transaction = False

    @property
    def dialect(self) -> Dialect:
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
            isolation_level=None,  # Autocommit mode - we manage transactions manually
        )
        self._conn.row_factory = _dict_factory
        # Enable foreign keys and WAL mode
        self._conn.execute("PRAGMA foreign_keys = ON")
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

        Uses BEGIN IMMEDIATE for write transactions to avoid
        SQLITE_BUSY errors on concurrent writes.

        Args:
            isolation_level: Ignored on SQLite (BEGIN IMMEDIATE provides isolation)
        """
        conn = self._ensure_connected()

        with self._lock:
            if self._in_transaction:
                raise DatabaseError("Nested transactions are not supported")

            try:
                conn.execute("BEGIN IMMEDIATE")
                self._in_transaction = True
                yield
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._in_transaction = False

    def execute(self, query: str, params: dict[str, Any] | None = None) -> None:
        """Execute a query without returning results."""
        conn = self._ensure_connected()
        with self._lock:
            try:
                conn.execute(query, params or {})
                if not self._in_transaction:
                    conn.commit()
            except sqlite3.Error as e:
                raise DatabaseError(f"SQLite query failed: {e}") from e

    def fetch_one(
        self, query: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Execute a query and return single result or None."""
        conn = self._ensure_connected()
        with self._lock:
            try:
                cursor = conn.execute(query, params or {})
                return cursor.fetchone()
            except sqlite3.Error as e:
                raise DatabaseError(f"SQLite query failed: {e}") from e

    def fetch_all(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Execute a query and return all results."""
        conn = self._ensure_connected()
        with self._lock:
            try:
                cursor = conn.execute(query, params or {})
                return cursor.fetchall()
            except sqlite3.Error as e:
                raise DatabaseError(f"SQLite query failed: {e}") from e

    def execute_rowcount(
        self, query: str, params: dict[str, Any] | None = None
    ) -> int:
        """Execute a query and return affected row count."""
        conn = self._ensure_connected()
        with self._lock:
            try:
                cursor = conn.execute(query, params or {})
                if not self._in_transaction:
                    conn.commit()
                return cursor.rowcount
            except sqlite3.Error as e:
                raise DatabaseError(f"SQLite query failed: {e}") from e
