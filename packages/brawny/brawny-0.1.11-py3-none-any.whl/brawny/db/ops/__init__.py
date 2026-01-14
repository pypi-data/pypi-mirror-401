"""Database operations modules.

Flat function-based operations for each domain:
- blocks: Block state and hash history
- jobs: Job configuration and KV store
- intents: Transaction intents
- attempts: Transaction attempts
- nonces: Signer state and nonce reservations
- cache: ABI and proxy cache

Usage:
    from brawny.db import ops

    # Use functions from specific modules
    state = ops.blocks.get_block_state(db, chain_id)
    job = ops.jobs.get_job(db, job_id)
    intent = ops.intents.create_intent(db, ...)
"""

from __future__ import annotations

from brawny.db.ops import blocks
from brawny.db.ops import jobs
from brawny.db.ops import intents
from brawny.db.ops import attempts
from brawny.db.ops import nonces
from brawny.db.ops import cache

__all__ = ["blocks", "jobs", "intents", "attempts", "nonces", "cache"]
