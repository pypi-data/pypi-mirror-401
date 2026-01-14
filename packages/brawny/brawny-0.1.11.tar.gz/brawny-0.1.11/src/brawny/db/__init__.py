"""Database layer with support for PostgreSQL (production) and SQLite (development)."""

from brawny.db.base import (
    ABICacheEntry,
    BlockHashEntry,
    BlockState,
    Database,
    IsolationLevel,
    ProxyCacheEntry,
)
from brawny.db.migrate import Migrator, discover_migrations, get_pending_migrations
try:
    from brawny.db.postgres import PostgresDatabase
except ModuleNotFoundError:
    PostgresDatabase = None  # type: ignore
from brawny.db.sqlite import SQLiteDatabase

__all__ = [
    # Base classes
    "Database",
    "IsolationLevel",
    # Data classes
    "BlockState",
    "BlockHashEntry",
    "ABICacheEntry",
    "ProxyCacheEntry",
    # Implementations
    "SQLiteDatabase",
    "PostgresDatabase",
    # Migration
    "Migrator",
    "discover_migrations",
    "get_pending_migrations",
    # Factory
    "create_database",
]


def create_database(database_url: str, **kwargs: object) -> Database:
    """Factory function to create a database instance based on URL.

    Args:
        database_url: Database connection URL
            - sqlite:///path/to/db.sqlite
            - postgresql://user:pass@host:port/dbname
        **kwargs: Additional arguments passed to the database constructor

    Returns:
        Database instance (SQLiteDatabase or PostgresDatabase)

    Raises:
        ValueError: If database URL scheme is not supported
    """
    circuit_breaker_failures = int(kwargs.pop("circuit_breaker_failures", 5))
    circuit_breaker_seconds = int(kwargs.pop("circuit_breaker_seconds", 30))
    if database_url.startswith("sqlite:///"):
        return SQLiteDatabase(
            database_url,
            circuit_breaker_failures=circuit_breaker_failures,
            circuit_breaker_seconds=circuit_breaker_seconds,
        )
    elif database_url.startswith(("postgresql://", "postgres://")):
        if PostgresDatabase is None:
            raise ValueError(
                "Postgres support requires psycopg and psycopg-pool. "
                "Install with: pip install psycopg[binary] psycopg-pool"
            )
        return PostgresDatabase(  # type: ignore
            database_url,
            circuit_breaker_failures=circuit_breaker_failures,
            circuit_breaker_seconds=circuit_breaker_seconds,
            **kwargs,
        )
    else:
        raise ValueError(
            f"Unsupported database URL: {database_url}. "
            "Must start with 'sqlite:///', 'postgresql://', or 'postgres://'"
        )
