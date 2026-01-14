"""ABI and proxy cache operations."""

from __future__ import annotations

from brawny.db.base_new import Database, ABICacheEntry, ProxyCacheEntry
from brawny.db import queries as Q
from brawny.db import mappers as M


# =============================================================================
# ABI Cache
# =============================================================================


def get_cached_abi(db: Database, chain_id: int, address: str) -> ABICacheEntry | None:
    """Get cached ABI for a contract address."""
    row = db.fetch_one(Q.GET_ABI_CACHE, {
        "chain_id": chain_id,
        "address": address.lower(),
    })
    return M.row_to_abi_cache(row) if row else None


def set_cached_abi(
    db: Database,
    chain_id: int,
    address: str,
    abi_json: str,
    source: str,
) -> None:
    """Cache an ABI for a contract address.

    Args:
        db: Database instance
        chain_id: Chain ID
        address: Contract address
        abi_json: JSON-encoded ABI
        source: Source of ABI ('etherscan', 'sourcify', 'manual', 'proxy_implementation')
    """
    db.execute(Q.UPSERT_ABI_CACHE, {
        "chain_id": chain_id,
        "address": address.lower(),
        "abi_json": abi_json,
        "source": source,
    })


def clear_cached_abi(db: Database, chain_id: int, address: str) -> bool:
    """Clear cached ABI for a contract address."""
    count = db.execute_rowcount(Q.DELETE_ABI_CACHE, {
        "chain_id": chain_id,
        "address": address.lower(),
    })
    return count > 0


# =============================================================================
# Proxy Cache
# =============================================================================


def get_cached_proxy(
    db: Database, chain_id: int, proxy_address: str
) -> ProxyCacheEntry | None:
    """Get cached proxy implementation address."""
    row = db.fetch_one(Q.GET_PROXY_CACHE, {
        "chain_id": chain_id,
        "proxy_address": proxy_address.lower(),
    })
    return M.row_to_proxy_cache(row) if row else None


def set_cached_proxy(
    db: Database,
    chain_id: int,
    proxy_address: str,
    implementation_address: str,
) -> None:
    """Cache a proxy-to-implementation mapping."""
    db.execute(Q.UPSERT_PROXY_CACHE, {
        "chain_id": chain_id,
        "proxy_address": proxy_address.lower(),
        "implementation_address": implementation_address.lower(),
    })


def clear_cached_proxy(db: Database, chain_id: int, proxy_address: str) -> bool:
    """Clear cached proxy resolution."""
    count = db.execute_rowcount(Q.DELETE_PROXY_CACHE, {
        "chain_id": chain_id,
        "proxy_address": proxy_address.lower(),
    })
    return count > 0
