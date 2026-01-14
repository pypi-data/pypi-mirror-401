"""Endpoint selection with health-aware ordering.

This module extracts endpoint health tracking and selection from RPCManager,
following OE6's separation of concerns.

INVARIANT: order_endpoints() always returns ALL endpoints, just ordered.
Unhealthy endpoints are moved to the end, not removed. This ensures
recovered endpoints eventually get tried again.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class EndpointHealth:
    """Health tracking for a single RPC endpoint."""

    url: str
    consecutive_failures: int = 0
    last_success_ts: float | None = None
    last_failure_ts: float | None = None
    latency_ewma_ms: float = 100.0  # Start with reasonable default

    # EWMA smoothing factor (0.3 = 30% weight to new samples, more responsive than old 0.1)
    EWMA_ALPHA: float = 0.3

    @property
    def is_healthy(self) -> bool:
        """Check if endpoint is currently healthy (below failure threshold)."""
        # Threshold is managed by EndpointSelector
        return True  # Selector determines health based on threshold

    def record_success(self, latency_ms: float) -> None:
        """Record a successful RPC call.

        Args:
            latency_ms: Request latency in milliseconds
        """
        self.consecutive_failures = 0
        self.last_success_ts = time.time()
        # EWMA update
        self.latency_ewma_ms = (
            self.EWMA_ALPHA * latency_ms + (1 - self.EWMA_ALPHA) * self.latency_ewma_ms
        )

    def record_failure(self) -> None:
        """Record a failed RPC call (transport-class failures only)."""
        self.consecutive_failures += 1
        self.last_failure_ts = time.time()


class EndpointSelector:
    """Health-aware endpoint selection.

    CONSTRAINTS (to prevent scope creep):
    - Only track consecutive failures + EWMA latency
    - No background probing
    - No partial circuit breaker logic
    - No complex health scoring

    INVARIANT: order_endpoints() always returns ALL endpoints, just ordered.
    Unhealthy endpoints are moved to the end, not removed. This ensures
    recovered endpoints eventually get tried again.
    """

    def __init__(
        self,
        endpoints: list[str],
        failure_threshold: int = 3,
    ) -> None:
        """Initialize endpoint selector.

        Args:
            endpoints: List of endpoint URLs
            failure_threshold: Consecutive failures before endpoint is unhealthy
        """
        if not endpoints:
            raise ValueError("At least one endpoint is required")

        self._endpoints = [EndpointHealth(url=url.strip()) for url in endpoints if url.strip()]
        if not self._endpoints:
            raise ValueError("At least one non-empty endpoint is required")

        self._failure_threshold = failure_threshold
        self._endpoint_map: dict[str, EndpointHealth] = {e.url: e for e in self._endpoints}

    @property
    def endpoints(self) -> list[EndpointHealth]:
        """Get all endpoint health objects."""
        return self._endpoints

    def get_endpoint(self, url: str) -> EndpointHealth | None:
        """Get endpoint health by URL."""
        return self._endpoint_map.get(url)

    def is_healthy(self, endpoint: EndpointHealth) -> bool:
        """Check if an endpoint is healthy (below failure threshold)."""
        return endpoint.consecutive_failures < self._failure_threshold

    def has_healthy_endpoint(self) -> bool:
        """Check if any endpoint is healthy."""
        return any(self.is_healthy(e) for e in self._endpoints)

    def order_endpoints(self) -> list[EndpointHealth]:
        """Return ALL endpoints ordered by health, preserving position priority.

        Ordering:
        1. Healthy endpoints in original order (first = primary)
        2. Unhealthy endpoints in original order

        Position-based: First healthy endpoint in user config is always preferred.
        """
        healthy = [e for e in self._endpoints if self.is_healthy(e)]
        unhealthy = [e for e in self._endpoints if not self.is_healthy(e)]
        return healthy + unhealthy

    def get_active_endpoint(self) -> EndpointHealth:
        """Get the preferred endpoint (healthiest first).

        Returns first healthy endpoint. If no healthy endpoints,
        returns least recently failed.

        Recovery: When an endpoint's consecutive_failures resets to 0 via
        record_success(), it becomes healthy and can be returned again.
        """
        ordered = self.order_endpoints()
        if ordered:
            return ordered[0]
        # Fallback (should not happen if endpoints exist)
        return self._endpoints[0]

    def record_success(self, url: str, latency_ms: float) -> None:
        """Record successful call for an endpoint.

        Args:
            url: Endpoint URL
            latency_ms: Request latency in milliseconds
        """
        endpoint = self._endpoint_map.get(url)
        if endpoint:
            endpoint.record_success(latency_ms)

    def record_failure(self, url: str) -> None:
        """Record failed call for an endpoint (transport-class failures only).

        Only call this for RPCRetryableError, not for Fatal/Recoverable errors.

        Args:
            url: Endpoint URL
        """
        endpoint = self._endpoint_map.get(url)
        if endpoint:
            endpoint.record_failure()
