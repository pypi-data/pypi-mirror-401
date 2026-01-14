"""PostgreSQL database implementation.

Slim execution layer with 4 primitives. All business operations live in db/ops/.
Uses connection pooling with psycopg3.
"""

from __future__ import annotations

import re
import threading
from contextlib import contextmanager
from typing import Any, Iterator, Literal

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from brawny.db.base_new import Database, Dialect, IsolationLevel
from brawny.model.errors import DatabaseError


def _rewrite(query: str) -> str:
    """Rewrite :name placeholders to %(name)s for psycopg."""
    # Match :word but not ::type_cast
    return re.sub(r"(?<!:):(\w+)", r"%(\1)s", query)


class PostgresDatabase(Database):
    """PostgreSQL implementation with connection pooling.

    Uses psycopg3 with a synchronous connection pool.
    Queries use :name placeholders (rewritten to %(name)s).
    """

    def __init__(
        self,
        database_url: str,
        pool_size: int = 5,
        pool_max_overflow: int = 10,
        pool_timeout: float = 30.0,
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
        self._local = threading.local()

    @property
    def dialect(self) -> Dialect:
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
        """Get connection from current transaction context."""
        return getattr(self._local, "conn", None)

    @contextmanager
    def transaction(
        self, isolation_level: IsolationLevel | None = None
    ) -> Iterator[None]:
        """Context manager for database transactions.

        Args:
            isolation_level: Optional isolation level (e.g., SERIALIZABLE for nonce reservation)

        Usage:
            with db.transaction():
                ops.intents.create_intent(db, ...)

            with db.transaction(isolation_level="SERIALIZABLE"):
                # Atomic nonce reservation
                ...
        """
        if self._get_current_conn() is not None:
            raise DatabaseError("Nested transactions are not supported")

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

    def execute(self, query: str, params: dict[str, Any] | None = None) -> None:
        """Execute a query without returning results."""
        query = _rewrite(query)
        conn = self._get_current_conn()
        try:
            if conn is not None:
                conn.execute(query, params or {})
                return

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    conn.execute(query, params or {})
        except psycopg.Error as e:
            raise DatabaseError(f"Postgres query failed: {e}") from e

    def fetch_one(
        self, query: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Execute a query and return single result or None."""
        query = _rewrite(query)
        conn = self._get_current_conn()
        try:
            if conn is not None:
                return conn.execute(query, params or {}).fetchone()

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    return conn.execute(query, params or {}).fetchone()
        except psycopg.Error as e:
            raise DatabaseError(f"Postgres query failed: {e}") from e

    def fetch_all(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Execute a query and return all results."""
        query = _rewrite(query)
        conn = self._get_current_conn()
        try:
            if conn is not None:
                return conn.execute(query, params or {}).fetchall()

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    return conn.execute(query, params or {}).fetchall()
        except psycopg.Error as e:
            raise DatabaseError(f"Postgres query failed: {e}") from e

    def execute_rowcount(
        self, query: str, params: dict[str, Any] | None = None
    ) -> int:
        """Execute a query and return affected row count."""
        query = _rewrite(query)
        conn = self._get_current_conn()
        try:
            if conn is not None:
                cur = conn.execute(query, params or {})
                return cur.rowcount

            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.row_factory = dict_row
                with conn.transaction():
                    cur = conn.execute(query, params or {})
                    return cur.rowcount
        except psycopg.Error as e:
            raise DatabaseError(f"Postgres query failed: {e}") from e
