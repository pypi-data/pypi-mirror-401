"""Job configuration and KV store operations."""

from __future__ import annotations

import json
from typing import Any

from brawny.db.base_new import Database
from brawny.db import queries as Q
from brawny.db import mappers as M
from brawny.model.types import JobConfig


def get_job(db: Database, job_id: str) -> JobConfig | None:
    """Get job configuration by ID."""
    row = db.fetch_one(Q.GET_JOB, {"job_id": job_id})
    return M.row_to_job_config(row) if row else None


def get_enabled_jobs(db: Database) -> list[JobConfig]:
    """Get all enabled jobs ordered by job_id."""
    rows = db.fetch_all(Q.GET_ENABLED_JOBS)
    return [M.row_to_job_config(row) for row in rows]


def list_all_jobs(db: Database) -> list[JobConfig]:
    """List all jobs ordered by job_id."""
    rows = db.fetch_all(Q.LIST_ALL_JOBS)
    return [M.row_to_job_config(row) for row in rows]


def upsert_job(
    db: Database,
    job_id: str,
    job_name: str,
    check_interval_blocks: int,
    enabled: bool = True,
) -> None:
    """Upsert job configuration."""
    db.execute(Q.UPSERT_JOB, {
        "job_id": job_id,
        "job_name": job_name,
        "check_interval_blocks": check_interval_blocks,
        "enabled": 1 if enabled else 0,
    })


def set_job_enabled(db: Database, job_id: str, enabled: bool) -> bool:
    """Enable or disable a job."""
    count = db.execute_rowcount(Q.UPDATE_JOB_ENABLED, {
        "job_id": job_id,
        "enabled": 1 if enabled else 0,
    })
    return count > 0


def update_job_checked(
    db: Database, job_id: str, block_number: int, triggered: bool = False
) -> bool:
    """Update job checked state and optionally triggered state."""
    if triggered:
        count = db.execute_rowcount(Q.UPDATE_JOB_TRIGGERED, {
            "job_id": job_id,
            "block_number": block_number,
        })
    else:
        count = db.execute_rowcount(Q.UPDATE_JOB_CHECKED, {
            "job_id": job_id,
            "block_number": block_number,
        })
    return count > 0


def delete_job(db: Database, job_id: str) -> bool:
    """Delete a job configuration."""
    count = db.execute_rowcount(Q.DELETE_JOB, {"job_id": job_id})
    return count > 0


# =============================================================================
# Job KV Store
# =============================================================================


def get_job_kv(db: Database, job_id: str, key: str, default: Any = None) -> Any:
    """Get a value from job KV store."""
    row = db.fetch_one(Q.GET_JOB_KV, {"job_id": job_id, "key": key})
    if row is None:
        return default
    return json.loads(row["value_json"])


def set_job_kv(db: Database, job_id: str, key: str, value: Any) -> None:
    """Set a value in job KV store."""
    db.execute(Q.UPSERT_JOB_KV, {
        "job_id": job_id,
        "key": key,
        "value_json": json.dumps(value),
    })


def delete_job_kv(db: Database, job_id: str, key: str) -> bool:
    """Delete a key from job KV store."""
    count = db.execute_rowcount(Q.DELETE_JOB_KV, {"job_id": job_id, "key": key})
    return count > 0


def delete_all_job_kv(db: Database, job_id: str) -> int:
    """Delete all KV entries for a job."""
    return db.execute_rowcount(Q.DELETE_ALL_JOB_KV, {"job_id": job_id})
