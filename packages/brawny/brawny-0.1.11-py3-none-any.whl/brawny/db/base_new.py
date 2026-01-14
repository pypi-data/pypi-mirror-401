"""Slim database interface for brawny.

Provides 4 execution primitives + transaction + connect/close.
All domain operations live in db/ops/ modules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterator, Literal


Dialect = Literal["postgres", "sqlite"]
IsolationLevel = Literal["SERIALIZABLE", "READ COMMITTED", "REPEATABLE READ"]


@dataclass
class BlockState:
    """Block processing state."""

    chain_id: int
    last_processed_block_number: int
    last_processed_block_hash: str
    created_at: datetime
    updated_at: datetime


@dataclass
class BlockHashEntry:
    """Block hash history entry for reorg detection."""

    id: int
    chain_id: int
    block_number: int
    block_hash: str
    inserted_at: datetime


@dataclass
class ABICacheEntry:
    """Cached ABI entry."""

    chain_id: int
    address: str
    abi_json: str
    source: str
    resolved_at: datetime


@dataclass
class ProxyCacheEntry:
    """Cached proxy resolution entry."""

    chain_id: int
    proxy_address: str
    implementation_address: str
    resolved_at: datetime


class Database(ABC):
    """Database interface with 4 execution primitives.

    Implementations provide connection management and query execution.
    SQL queries are in db/queries.py, row mapping in db/mappers.py.
    """

    @property
    @abstractmethod
    def dialect(self) -> Dialect:
        """Return dialect name for query selection."""
        ...

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close database connection and cleanup resources."""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if database is connected."""
        ...

    @abstractmethod
    @contextmanager
    def transaction(
        self, isolation_level: IsolationLevel | None = None
    ) -> Iterator[None]:
        """Context manager for database transactions.

        Args:
            isolation_level: Optional isolation level (Postgres only, ignored on SQLite)

        Usage:
            with db.transaction():
                ops.intents.create_intent(db, ...)
                ops.nonces.reserve_nonce(db, ...)

            # For atomic nonce reservation on Postgres
            with db.transaction(isolation_level="SERIALIZABLE"):
                ...
        """
        ...

    @abstractmethod
    def execute(self, query: str, params: dict[str, Any] | None = None) -> None:
        """Execute a query without returning results.

        Args:
            query: SQL with :name placeholders
            params: Dict of parameter values
        """
        ...

    @abstractmethod
    def fetch_one(
        self, query: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Execute a query and return single result or None.

        Args:
            query: SQL with :name placeholders
            params: Dict of parameter values

        Returns:
            Single row as dict, or None if no results
        """
        ...

    @abstractmethod
    def fetch_all(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Execute a query and return all results.

        Args:
            query: SQL with :name placeholders
            params: Dict of parameter values

        Returns:
            List of rows as dicts
        """
        ...

    @abstractmethod
    def execute_rowcount(
        self, query: str, params: dict[str, Any] | None = None
    ) -> int:
        """Execute a query and return affected row count.

        Args:
            query: SQL with :name placeholders
            params: Dict of parameter values

        Returns:
            Number of rows affected
        """
        ...
