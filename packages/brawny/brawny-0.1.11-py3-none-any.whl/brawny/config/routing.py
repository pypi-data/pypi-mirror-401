"""RPC group routing helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny.jobs.base import Job


def resolve_default_group(config: "Config") -> str:
    """Resolve the default RPC group.

    Rules:
    - If rpc_default_group is set, use it.
    - If exactly one rpc_group exists, use it.
    - If multiple rpc_groups and no default, raise.
    """
    if config.rpc_default_group:
        return config.rpc_default_group

    if len(config.rpc_groups) == 1:
        return next(iter(config.rpc_groups.keys()))

    if not config.rpc_groups:
        raise ValueError("rpc_groups not configured; set rpc_groups and rpc_default_group")

    raise ValueError("Multiple rpc_groups configured; set rpc_default_group.")


def resolve_job_groups(config: "Config", job: "Job") -> tuple[str, str]:
    """Resolve read/broadcast groups for a job.

    Returns:
        (read_group, broadcast_group)
    """
    read_group = getattr(job, "_read_group", None)
    broadcast_group = getattr(job, "_broadcast_group", None)

    if not config.rpc_groups:
        raise ValueError("rpc_groups not configured; set rpc_groups and rpc_default_group")

    default_group = resolve_default_group(config)
    if read_group is None:
        read_group = default_group
    if broadcast_group is None:
        broadcast_group = default_group

    if read_group not in config.rpc_groups:
        raise ValueError(f"read_group '{read_group}' not found in rpc_groups")
    if broadcast_group not in config.rpc_groups:
        raise ValueError(f"broadcast_group '{broadcast_group}' not found in rpc_groups")

    return read_group, broadcast_group
