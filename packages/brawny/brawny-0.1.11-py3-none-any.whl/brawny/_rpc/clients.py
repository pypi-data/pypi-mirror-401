"""RPC client management — shared by TxExecutor and JobRunner.

This module provides caching for read RPC clients by group.
Broadcast clients are created per-call from endpoint snapshots (see broadcast.py).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny._rpc.manager import RPCManager


class RPCClients:
    """Manages RPC clients for read operations.

    Caches read clients by group. Broadcast clients are created per-call
    from endpoint snapshots (see broadcast.py).

    Example:
        clients = RPCClients(config)

        # Get cached read client for a group
        public_rpc = clients.get_read_client("public")
        private_rpc = clients.get_read_client("private")

        # Same group = same cached client
        assert clients.get_read_client("public") is public_rpc
    """

    def __init__(self, config: "Config") -> None:
        """Initialize RPC clients manager.

        Args:
            config: Application configuration
        """
        self._config = config
        self._read_clients: dict[str, "RPCManager"] = {}

    def get_read_client(self, group_name: str) -> "RPCManager":
        """Get (cached) read client for a group.

        If the group's client hasn't been created yet, creates it.
        Subsequent calls return the same cached instance.

        Args:
            group_name: Name of the RPC group (e.g., "public", "private")

        Returns:
            RPCManager configured for the group's endpoints

        Raises:
            ValueError: If group not found in config.rpc_groups
        """
        if group_name not in self._read_clients:
            from brawny._rpc.manager import RPCManager

            if group_name not in self._config.rpc_groups:
                raise ValueError(f"RPC group '{group_name}' not found")

            group = self._config.rpc_groups[group_name]
            self._read_clients[group_name] = RPCManager(
                endpoints=group.endpoints,
                timeout_seconds=self._config.rpc_timeout_seconds,
                max_retries=self._config.rpc_max_retries,
                retry_backoff_base=self._config.rpc_retry_backoff_base,
                circuit_breaker_seconds=self._config.rpc_circuit_breaker_seconds,
                rate_limit_per_second=self._config.rpc_rate_limit_per_second,
                rate_limit_burst=self._config.rpc_rate_limit_burst,
                chain_id=self._config.chain_id,
                log_init=False,  # Daemon already logged main RPC init
            )

        return self._read_clients[group_name]

    def get_default_client(self) -> "RPCManager":
        """Get the default read client.

        Uses config.rpc_default_group if set, otherwise requires a single rpc_group.

        Returns:
            RPCManager for the default group

        Raises:
            ValueError: If default group cannot be resolved
        """
        from brawny.config.routing import resolve_default_group

        return self.get_read_client(resolve_default_group(self._config))

    def clear_cache(self) -> None:
        """Clear all cached clients.

        Useful for testing or when config changes require new clients.
        """
        self._read_clients.clear()
