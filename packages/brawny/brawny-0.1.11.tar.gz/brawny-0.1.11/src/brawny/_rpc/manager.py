"""RPC Manager with multi-endpoint failover and health tracking.

Implements OE6 simplification:
- Uses EndpointSelector for health-aware endpoint ordering
- Explicit failover gate: only failover on RPCRetryableError
- Per-attempt metrics (requests, latency, errors, failovers)
- Selector health updates only on transport failures

OE6 Invariants (LOCKED):
1. Failover occurs ONLY on RPCRetryableError (explicit issubclass check)
2. Fatal + Recoverable errors NEVER trigger failover (raise immediately)
3. Per-attempt metrics: requests, latency (success AND failure), errors, failovers
4. Selector health updates ONLY on retryable failures (not Fatal/Recoverable)
5. Selector returns ALL endpoints (unhealthy moved to end, not removed)
"""

from __future__ import annotations

import re
import time
from urllib.parse import urlsplit, urlunsplit
from typing import TYPE_CHECKING, Any

from requests.auth import HTTPBasicAuth
from web3 import Web3
from web3.exceptions import TransactionNotFound

from brawny.logging import LogEvents, get_logger
from brawny.metrics import (
    RPC_ENDPOINT_HEALTH,
    RPC_ERRORS,
    RPC_FAILOVERS,
    RPC_REQUESTS,
    RPC_REQUESTS_BY_JOB,
    RPC_REQUEST_SECONDS,
    get_metrics,
)
from brawny._rpc.context import get_job_context
from brawny.model.errors import (
    SimulationNetworkError,
    SimulationReverted,
)
from brawny._rpc.errors import (
    RPCError,
    RPCFatalError,
    RPCPoolExhaustedError,
    RPCRecoverableError,
    RPCRetryableError,
    classify_error,
    normalize_error_code,
)
from brawny._rpc.selector import EndpointSelector

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny._rpc.gas import GasQuote, GasQuoteCache

logger = get_logger(__name__)

# RPC methods that broadcast transactions (vs read-only)
RPC_BROADCAST_METHODS = {"eth_sendRawTransaction", "eth_sendTransaction"}


def _rpc_category(method: str) -> str:
    """Classify RPC method as 'broadcast' or 'read'."""
    return "broadcast" if method in RPC_BROADCAST_METHODS else "read"


def _rpc_host(url: str, allowed_hosts: frozenset[str] | None = None) -> str:
    """Extract hostname from URL, stripping credentials/path/query.

    Returns 'unknown' if parse fails, 'other' if host not in allowed set.
    This provides cardinality protection for Prometheus metrics.
    """
    try:
        parsed = urlsplit(url)
        host = parsed.hostname or "unknown"
        if parsed.port and parsed.port not in (80, 443):
            host = f"{host}:{parsed.port}"
        # Cardinality guardrail: coerce unknown hosts
        if allowed_hosts and host not in allowed_hosts:
            return "other"
        return host
    except Exception:
        return "unknown"


def _extract_url_auth(url: str) -> tuple[str, HTTPBasicAuth | None]:
    """Extract Basic Auth credentials from URL if present.

    Args:
        url: URL that may contain embedded credentials (https://user:pass@host)

    Returns:
        Tuple of (clean_url, auth) where auth is HTTPBasicAuth if credentials
        were present, None otherwise. The clean_url has credentials removed.

    Example:
        >>> _extract_url_auth("https://guest:secret@eth.example.com/rpc")
        ("https://eth.example.com/rpc", HTTPBasicAuth("guest", "secret"))
    """
    split = urlsplit(url)
    if split.username:
        # Rebuild URL without credentials
        netloc = split.hostname or ""
        if split.port:
            netloc = f"{netloc}:{split.port}"
        clean_url = urlunsplit((split.scheme, netloc, split.path, split.query, split.fragment))
        auth = HTTPBasicAuth(split.username, split.password or "")
        return clean_url, auth
    return url, None


class RPCManager:
    """RPC manager with failover and health tracking.

    Provides a high-level interface for RPC calls with:
    - Automatic retry with exponential backoff
    - Endpoint health tracking via EndpointSelector
    - Explicit failover gate (only on RPCRetryableError)

    OE6 Simplification:
    - Removed circuit breaker (logging-only, no blocking)
    - Removed rate limiter (RPC providers handle this)
    - Uses EndpointSelector for health-aware ordering
    """

    def __init__(
        self,
        endpoints: list[str],
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
        retry_backoff_base: float = 1.0,
        circuit_breaker_seconds: int = 300,
        rate_limit_per_second: float | None = None,
        rate_limit_burst: int | None = None,
        rate_limits: dict[str, dict[str, float | int]] | None = None,
        chain_id: int | None = None,
        gas_refresh_seconds: int = 15,
        log_init: bool = True,
    ) -> None:
        """Initialize RPC manager.

        Args:
            endpoints: List of RPC endpoint URLs
            timeout_seconds: Request timeout
            max_retries: Maximum retry attempts (try up to N different endpoints)
            retry_backoff_base: Base for exponential backoff
            circuit_breaker_seconds: Ignored (kept for backwards compatibility)
            rate_limit_per_second: Ignored (kept for backwards compatibility)
            rate_limit_burst: Ignored (kept for backwards compatibility)
            rate_limits: Ignored (kept for backwards compatibility)
            chain_id: Chain ID for validation
            gas_refresh_seconds: TTL for gas quote cache
            log_init: Whether to log initialization (False for ephemeral broadcast managers)
        """
        if not endpoints:
            raise ValueError("At least one RPC endpoint is required")

        # Use EndpointSelector for health-aware ordering (OE6)
        self._selector = EndpointSelector(endpoints, failure_threshold=3)
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._backoff_base = retry_backoff_base
        self._chain_id = chain_id
        self._gas_refresh_seconds = gas_refresh_seconds
        self._gas_cache: "GasQuoteCache | None" = None
        self._failure_debug_last_ts: dict[tuple[int | None, str, str], float] = {}

        # Create Web3 instances for each endpoint
        # Extract Basic Auth credentials from URLs if present (e.g., https://user:pass@host)
        self._web3_instances: dict[str, Web3] = {}
        for ep in self._selector.endpoints:
            clean_url, auth = _extract_url_auth(ep.url)
            request_kwargs: dict[str, Any] = {"timeout": timeout_seconds}
            if auth:
                request_kwargs["auth"] = auth
            self._web3_instances[ep.url] = Web3(Web3.HTTPProvider(clean_url, request_kwargs=request_kwargs))

        # Build allowed hosts set for metrics cardinality protection
        hosts = []
        for ep in self._selector.endpoints:
            h = _rpc_host(ep.url)  # no allowed_hosts passed - get raw host
            if h not in ("unknown", "other"):
                hosts.append(h)
        self._allowed_hosts = frozenset(hosts)

        if log_init:
            logger.info(
                "rpc.manager.initialized",
                endpoints=len(endpoints),
                timeout=timeout_seconds,
                max_retries=max_retries,
            )

    @classmethod
    def from_config(cls, config: Config) -> RPCManager:
        """Create RPC manager from config.

        Args:
            config: Application configuration

        Returns:
            Configured RPC manager
        """
        from brawny.config.routing import resolve_default_group

        default_group = resolve_default_group(config)
        endpoints = config.rpc_groups[default_group].endpoints
        return cls(
            endpoints=endpoints,
            timeout_seconds=config.rpc_timeout_seconds,
            max_retries=config.rpc_max_retries,
            retry_backoff_base=config.rpc_retry_backoff_base,
            circuit_breaker_seconds=config.rpc_circuit_breaker_seconds,
            rate_limit_per_second=config.rpc_rate_limit_per_second,
            rate_limit_burst=config.rpc_rate_limit_burst,
            rate_limits=config.rpc_rate_limits,
            chain_id=config.chain_id,
            gas_refresh_seconds=config.gas_refresh_seconds,
        )

    @property
    def web3(self) -> Web3:
        """Get Web3 instance for the active (healthiest) endpoint.

        Returns:
            Web3 instance configured for the current best endpoint

        Note:
            This provides direct web3-py API access. For operations with
            automatic retry/failover, use RPCManager methods instead.
        """
        endpoint = self._selector.get_active_endpoint()
        return self._web3_instances[endpoint.url]

    @property
    def gas(self) -> "GasQuoteCache":
        """Gas quote cache (lazy init)."""
        if self._gas_cache is None:
            from brawny._rpc.gas import GasQuoteCache

            self._gas_cache = GasQuoteCache(
                self,
                ttl_seconds=self._gas_refresh_seconds,
            )
        return self._gas_cache

    async def gas_quote(self) -> "GasQuote":
        """Get gas quote (async)."""
        return await self.gas.get_quote()

    def gas_quote_sync(self) -> "GasQuote | None":
        """Get cached gas quote (sync, for executor)."""
        return self.gas.get_quote_sync()

    @staticmethod
    def _safe_endpoint_label(url: str) -> str:
        split = urlsplit(url)
        netloc = split.hostname or ""
        if split.port:
            netloc = f"{netloc}:{split.port}"
        return urlunsplit((split.scheme, netloc, split.path, "", ""))

    def _should_log_failure_debug(self, method: str, endpoint: str) -> bool:
        safe_endpoint = self._safe_endpoint_label(endpoint)
        key = (self._chain_id, method, safe_endpoint)
        now = time.time()
        last = self._failure_debug_last_ts.get(key)
        if last is None or (now - last) >= 60:
            self._failure_debug_last_ts[key] = now
            return True
        return False

    def call(
        self,
        method: str,
        *args: Any,
        timeout: float | None = None,
        block_identifier: int | str = "latest",
    ) -> Any:
        """Execute an RPC call with retry and failover.

        OE6 Invariants:
        1. Failover occurs ONLY on RPCRetryableError (explicit issubclass check)
        2. Fatal + Recoverable errors NEVER trigger failover (raise immediately)
        3. Per-attempt metrics: requests, latency (success AND failure), errors, failovers
        4. Selector health updates ONLY on retryable failures

        Args:
            method: RPC method name (e.g., "eth_blockNumber")
            *args: Method arguments
            timeout: Optional timeout override
            block_identifier: Block identifier for state queries

        Returns:
            RPC response

        Raises:
            RPCFatalError: For non-retryable errors (nonce too low, reverted)
            RPCRecoverableError: For errors that need param changes (underpriced)
            RPCRetryableError: If all retries exhausted
        """
        timeout = timeout or self._timeout
        last_error: Exception | None = None

        # Get metrics provider once outside retry loop
        metrics = get_metrics()
        category = _rpc_category(method)

        # Get ordered endpoints from selector (healthiest first, unhealthy at end)
        ordered_endpoints = self._selector.order_endpoints()
        attempts_to_try = min(self._max_retries, len(ordered_endpoints))

        for attempt, endpoint in enumerate(ordered_endpoints[:attempts_to_try]):
            w3 = self._web3_instances[endpoint.url]
            rpc_host = _rpc_host(endpoint.url, self._allowed_hosts)

            # Count every attempt (OE6: per-attempt metrics)
            metrics.counter(RPC_REQUESTS).inc(
                chain_id=self._chain_id,
                method=method,
                rpc_category=category,
                rpc_host=rpc_host,
            )

            # Job attribution (if context exists) - no rpc_host to avoid cardinality explosion
            job_id = get_job_context()
            if job_id:
                metrics.counter(RPC_REQUESTS_BY_JOB).inc(
                    chain_id=self._chain_id,
                    job_id=job_id,
                    rpc_category=category,
                )

            # Per-attempt timing starts right before execute
            start_time = time.time()
            try:
                result = self._execute_method(w3, method, args, block_identifier)
                latency = time.time() - start_time

                # Record success with selector
                self._selector.record_success(endpoint.url, latency * 1000)

                # Record latency on success
                metrics.histogram(RPC_REQUEST_SECONDS).observe(
                    latency,
                    chain_id=self._chain_id,
                    method=method,
                    rpc_category=category,
                    rpc_host=rpc_host,
                )

                logger.debug(
                    LogEvents.RPC_REQUEST,
                    method=method,
                    endpoint=self._safe_endpoint_label(endpoint.url),
                    latency_ms=round(latency * 1000, 1),
                )

                return result

            except Exception as e:
                latency = time.time() - start_time

                # Record latency on failure too (don't hide slow failures)
                metrics.histogram(RPC_REQUEST_SECONDS).observe(
                    latency,
                    chain_id=self._chain_id,
                    method=method,
                    rpc_category=category,
                    rpc_host=rpc_host,
                )

                # If already an RPCError subclass, preserve it but ensure context
                if isinstance(e, RPCError):
                    if getattr(e, "method", None) is None or getattr(e, "endpoint", None) is None:
                        raise type(e)(str(e), method=method, endpoint=endpoint.url) from e
                    raise

                # Classify using existing infrastructure
                error_class = classify_error(e)
                error_code = normalize_error_code(e)
                include_trace = error_code == "unknown_error" or attempt == attempts_to_try - 1

                if self._should_log_failure_debug(method, endpoint.url):
                    logger.info(
                        "rpc.failure_debug",
                        method=method,
                        endpoint=self._safe_endpoint_label(endpoint.url),
                        timeout_seconds=timeout,
                        attempt=attempt + 1,
                        max_retries=attempts_to_try,
                        elapsed_ms=round(latency * 1000, 1),
                        error_type=type(e).__name__,
                        error_code=error_code,
                    )

                # EXPLICIT FAILOVER GATE (OE6 Invariant #1):
                # Only failover on RPCRetryableError. This prevents future error
                # classes from silently becoming failover triggers.
                if not issubclass(error_class, RPCRetryableError):
                    # Fatal, Recoverable, or any new class: raise immediately, no failover
                    # Don't record failure with selector (not a transport failure)
                    logger.warning(
                        LogEvents.RPC_ERROR,
                        method=method,
                        endpoint=self._safe_endpoint_label(endpoint.url),
                        error=str(e)[:200],
                        error_code=error_code,
                        attempt=attempt + 1,
                        max_retries=attempts_to_try,
                        classified_as=error_class.__name__,
                        exc_info=include_trace,
                    )
                    raise error_class(
                        str(e),
                        code=error_code,
                        endpoint=endpoint.url,
                        method=method,
                    ) from e

                # === RPCRetryableError path: record and maybe failover ===
                # Only record failure with selector for transport errors (OE6 Invariant #4)
                self._selector.record_failure(endpoint.url)

                # Count transport error
                metrics.counter(RPC_ERRORS).inc(
                    chain_id=self._chain_id,
                    method=method,
                    rpc_category=category,
                    rpc_host=rpc_host,
                )

                last_error = e
                is_last = (attempt == attempts_to_try - 1)

                if is_last:
                    logger.warning(
                        LogEvents.RPC_ERROR,
                        method=method,
                        endpoint=self._safe_endpoint_label(endpoint.url),
                        error=str(e)[:200],
                        error_code=error_code,
                        attempt=attempt + 1,
                        max_retries=attempts_to_try,
                        classified_as="RPCRetryableError",
                        exc_info=include_trace,
                    )
                else:
                    # Failover: log and count
                    metrics.counter(RPC_FAILOVERS).inc(
                        chain_id=self._chain_id,
                        method=method,
                    )
                    logger.warning(
                        "rpc.failover",
                        method=method,
                        endpoint=self._safe_endpoint_label(endpoint.url),
                        error=str(e)[:200],
                        error_code=error_code,
                        attempt=attempt + 1,
                        attempts_to_try=attempts_to_try,
                        classified_as="RPCRetryableError",
                    )

                    # Exponential backoff before failover
                    backoff = self._backoff_base * (2 ** attempt)
                    time.sleep(backoff)

        # All retries exhausted
        if not self._selector.has_healthy_endpoint():
            logger.error(LogEvents.RPC_ALL_ENDPOINTS_FAILED)

        raise RPCRetryableError(
            f"All {attempts_to_try} attempts failed: {last_error}",
            code="retries_exhausted",
            method=method,
        )

    def _execute_method(
        self,
        w3: Web3,
        method: str,
        args: tuple,
        block_identifier: int | str,
    ) -> Any:
        """Execute an RPC method on a Web3 instance.

        Args:
            w3: Web3 instance
            method: Method name
            args: Method arguments
            block_identifier: Block for state queries

        Returns:
            Method result
        """
        # Map common method names to Web3 calls
        if method == "eth_blockNumber":
            return w3.eth.block_number
        elif method == "eth_getBlockByNumber":
            block_num = args[0] if args else "latest"
            full_tx = args[1] if len(args) > 1 else False
            return w3.eth.get_block(block_num, full_transactions=full_tx)
        elif method == "eth_getTransactionCount":
            address = args[0]
            block = args[1] if len(args) > 1 else "pending"
            return w3.eth.get_transaction_count(address, block)
        elif method == "eth_getTransactionReceipt":
            tx_hash = args[0]
            try:
                return w3.eth.get_transaction_receipt(tx_hash)
            except TransactionNotFound:
                return None
        elif method == "eth_sendRawTransaction":
            return w3.eth.send_raw_transaction(args[0])
        elif method == "eth_estimateGas":
            return w3.eth.estimate_gas(args[0], block_identifier=block_identifier)
        elif method == "eth_call":
            tx = args[0]
            block = args[1] if len(args) > 1 else block_identifier
            return w3.eth.call(tx, block_identifier=block)
        elif method == "eth_getStorageAt":
            address = args[0]
            slot = args[1]
            block = args[2] if len(args) > 2 else block_identifier
            return w3.eth.get_storage_at(address, slot, block_identifier=block)
        elif method == "eth_chainId":
            return w3.eth.chain_id
        elif method == "eth_gasPrice":
            return w3.eth.gas_price
        elif method == "eth_getBalance":
            address = args[0]
            block = args[1] if len(args) > 1 else block_identifier
            return w3.eth.get_balance(address, block_identifier=block)
        else:
            # Generic RPC call
            return w3.provider.make_request(method, list(args))

    # =========================================================================
    # High-level convenience methods
    # =========================================================================

    def with_retry(self, fn: callable) -> Any:
        """Execute arbitrary web3 operation with retry and failover.

        Use this when you need a web3-py method that isn't wrapped by RPCManager,
        but still want automatic retry and endpoint failover.

        Args:
            fn: Callable that takes a Web3 instance and returns a result.
                Will be called with the healthiest endpoint's Web3 instance.

        Returns:
            Result from fn(web3)

        Raises:
            RPCRetryableError: If all retries exhausted

        Example:
            # Get storage with retry
            storage = rpc.with_retry(lambda w3: w3.eth.get_storage_at(addr, 0))

            # Complex operation with retry
            def get_logs(w3):
                return w3.eth.get_logs({"address": addr, "fromBlock": 0})
            logs = rpc.with_retry(get_logs)
        """
        last_error: Exception | None = None

        # Get ordered endpoints from selector
        ordered_endpoints = self._selector.order_endpoints()
        attempts_to_try = min(self._max_retries, len(ordered_endpoints))

        for attempt, endpoint in enumerate(ordered_endpoints[:attempts_to_try]):
            w3 = self._web3_instances[endpoint.url]

            try:
                start_time = time.time()
                result = fn(w3)
                latency_ms = (time.time() - start_time) * 1000

                self._selector.record_success(endpoint.url, latency_ms)

                logger.debug(
                    "rpc.with_retry.success",
                    endpoint=self._safe_endpoint_label(endpoint.url),
                    latency_ms=round(latency_ms, 1),
                    attempt=attempt + 1,
                )

                return result

            except Exception as e:
                self._selector.record_failure(endpoint.url)

                logger.warning(
                    "rpc.with_retry.error",
                    endpoint=self._safe_endpoint_label(endpoint.url),
                    error=str(e)[:200],
                    attempt=attempt + 1,
                    max_retries=attempts_to_try,
                )

                last_error = e

                # Exponential backoff
                if attempt < attempts_to_try - 1:
                    backoff = self._backoff_base * (2 ** attempt)
                    time.sleep(backoff)

        # All retries exhausted
        raise RPCRetryableError(
            f"with_retry: all {attempts_to_try} attempts failed: {last_error}",
            code="retries_exhausted",
            method="with_retry",
        )

    def get_block_number(self, timeout: float | None = None) -> int:
        """Get current block number."""
        return self.call("eth_blockNumber", timeout=timeout)

    def get_block(
        self,
        block_identifier: int | str = "latest",
        full_transactions: bool = False,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Get block by number or hash."""
        return self.call(
            "eth_getBlockByNumber",
            block_identifier,
            full_transactions,
            timeout=timeout,
        )

    def get_transaction_count(
        self,
        address: str,
        block_identifier: str = "pending",
    ) -> int:
        """Get transaction count (nonce) for address."""
        return self.call("eth_getTransactionCount", address, block_identifier)

    def get_transaction_receipt(self, tx_hash: str) -> dict[str, Any] | None:
        """Get transaction receipt."""
        return self.call("eth_getTransactionReceipt", tx_hash)

    def send_raw_transaction(self, raw_tx: bytes) -> tuple[str, str]:
        """Broadcast a signed transaction.

        Routes through call() to ensure single instrumentation point.
        Metrics are recorded per-attempt in call().

        Returns:
            Tuple of (tx_hash, endpoint_url) — endpoint is best approximation
            (actual endpoint may differ if retry occurred)

        Raises:
            RPCRetryableError: All retries failed
            RPCFatalError: TX rejected (nonce, funds, revert)
            RPCRecoverableError: TX may succeed with different params

        NOTE: RPCManager is group-agnostic. It doesn't know about broadcast groups.
        The broadcast layer wraps errors with group context.
        """
        try:
            result = self.call("eth_sendRawTransaction", raw_tx)

            # Normalize tx_hash
            if hasattr(result, "hex"):
                tx_hash = f"0x{result.hex()}"
            else:
                tx_hash = result if str(result).startswith("0x") else f"0x{result}"

            # Return healthiest endpoint URL (best approximation - actual may differ if retry)
            endpoint = self._selector.get_active_endpoint()
            return tx_hash, endpoint.url

        except RPCRetryableError as e:
            # Convert to RPCPoolExhaustedError for broadcast.py compatibility
            raise RPCPoolExhaustedError(
                f"All {self._max_retries} retries failed",
                endpoints=[ep.url for ep in self._selector.endpoints],
                last_error=e,
            ) from e

    def estimate_gas(
        self,
        tx_params: dict[str, Any],
        block_identifier: int | str = "latest",
    ) -> int:
        """Estimate gas for transaction."""
        return self.call("eth_estimateGas", tx_params, block_identifier=block_identifier)

    def eth_call(
        self,
        tx_params: dict[str, Any],
        block_identifier: int | str = "latest",
    ) -> bytes:
        """Execute eth_call."""
        return self.call("eth_call", tx_params, block_identifier=block_identifier)

    def get_storage_at(
        self,
        address: str,
        slot: str | int,
        block_identifier: int | str = "latest",
    ) -> bytes:
        """Get storage at slot."""
        return self.call("eth_getStorageAt", address, slot, block_identifier=block_identifier)

    def get_chain_id(self) -> int:
        """Get chain ID."""
        return self.call("eth_chainId")

    def get_gas_price(self) -> int:
        """Get current gas price."""
        return self.call("eth_gasPrice")

    def get_base_fee(self, block_identifier: int | str = "latest") -> int:
        """Get base fee from block.

        Returns base fee in wei.
        """
        block = self.get_block(block_identifier)
        base_fee = block.get("baseFeePerGas", 0)
        return int(base_fee) if base_fee else 0

    def get_balance(
        self,
        address: str,
        block_identifier: int | str = "latest",
    ) -> int:
        """Get account balance in wei."""
        return self.call("eth_getBalance", address, block_identifier=block_identifier)

    # =========================================================================
    # Simulation
    # =========================================================================

    def simulate_transaction(
        self,
        tx: dict[str, Any],
        rpc_url: str | None = None,
    ) -> str:
        """Simulate a transaction using eth_call at latest block.

        Args:
            tx: Transaction dict with from, to, data, and optionally value, gas
            rpc_url: Optional override RPC URL. If provided, bypasses the
                RPCManager's failover machinery and calls this URL directly.
                Used for per-job RPC configuration.

        Returns:
            Hex-encoded return data (0x...) on success

        Raises:
            SimulationReverted: Transaction would revert (permanent, don't retry)
            SimulationNetworkError: Network/RPC error (transient, may retry)
        """
        call_params: dict[str, Any] = {
            "from": tx["from"],
            "to": tx["to"],
        }
        if "data" in tx:
            call_params["data"] = tx["data"]
        if "value" in tx:
            call_params["value"] = hex(tx["value"]) if isinstance(tx["value"], int) else tx["value"]
        if "gas" in tx:
            call_params["gas"] = hex(tx["gas"]) if isinstance(tx["gas"], int) else tx["gas"]

        try:
            if rpc_url:
                # Direct call to override RPC (bypasses failover machinery)
                clean_url, auth = _extract_url_auth(rpc_url)
                request_kwargs: dict[str, Any] = {"timeout": 30}
                if auth:
                    request_kwargs["auth"] = auth
                w3 = Web3(Web3.HTTPProvider(clean_url, request_kwargs=request_kwargs))
                result = w3.eth.call(call_params, block_identifier="latest")
            else:
                result = self.eth_call(call_params, block_identifier="latest")
            return result.hex() if isinstance(result, bytes) else result
        except Exception as e:
            revert_reason = self._parse_revert_reason(e)
            if revert_reason:
                raise SimulationReverted(revert_reason) from e
            else:
                raise SimulationNetworkError(str(e)) from e

    def _parse_revert_reason(self, error: Exception) -> str | None:
        """Parse revert reason from RPC error.

        Returns revert reason string if this is a revert, None if network error.

        The key distinction:
        - Reverts are permanent (tx would fail on-chain) -> return reason string
        - Network errors are transient (RPC issues) -> return None

        Detection approach:
        1. Check error codes that indicate execution failure
        2. Look for revert keywords in error message
        3. Try to extract revert data from structured error payloads
        """
        error_str = str(error).lower()

        # Extract error code if present
        error_code = None
        if hasattr(error, "args"):
            for arg in error.args:
                if isinstance(arg, dict):
                    error_code = arg.get("code")
                    if error_code is None:
                        error_code = arg.get("error", {}).get("code")
                if error_code is not None:
                    break

        # Error codes that indicate execution failure (not network issues)
        # -32000: Geth execution error
        # -32015: Parity execution error
        # 3: Geth revert
        revert_error_codes = {-32000, -32015, 3}
        if error_code in revert_error_codes:
            return self._extract_revert_message(error)

        # Keywords that indicate a revert (case-insensitive check already done)
        revert_keywords = [
            "execution reverted",
            "revert",
            "out of gas",
            "insufficient funds",
            "invalid opcode",
            "stack underflow",
            "stack overflow",
        ]
        if any(kw in error_str for kw in revert_keywords):
            return self._extract_revert_message(error)

        # No revert indicators - treat as network error
        return None

    def _extract_revert_message(self, error: Exception) -> str:
        """Extract a human-readable revert message from an error.

        Tries multiple strategies to get the best message possible.
        Returns generic message if no specific reason found.
        """
        error_str = str(error)

        # Strategy 1: "execution reverted: <reason>" pattern
        if "execution reverted:" in error_str.lower():
            idx = error_str.lower().find("execution reverted:")
            return error_str[idx + len("execution reverted:"):].strip() or "execution reverted"

        # Strategy 2: Extract revert data from structured payload
        revert_data = self._extract_revert_data(error)
        if revert_data:
            decoded = self._decode_revert_data(revert_data)
            if decoded:
                return decoded

        # Fallback: truncate error message
        clean_msg = error_str

        # Return first 200 chars of error as fallback
        if len(clean_msg) > 200:
            clean_msg = clean_msg[:200] + "..."
        return clean_msg or "Transaction reverted"

    def _extract_revert_data(self, error: Exception) -> str | None:
        """Extract hex revert data from error if present."""
        if hasattr(error, "args"):
            for arg in error.args:
                if isinstance(arg, dict):
                    # Try common locations for revert data
                    data = arg.get("data")
                    if data is None:
                        data = arg.get("error", {}).get("data")
                    if isinstance(data, dict):
                        data = data.get("data") or data.get("result")
                    if isinstance(data, str) and data.startswith("0x"):
                        return data

        # Also check error string for hex data
        error_str = str(error)
        hex_match = re.search(r"0x[0-9a-fA-F]{8,}", error_str)
        if hex_match:
            return hex_match.group()

        return None

    def _decode_revert_data(self, data: str) -> str | None:
        """Attempt to decode revert data into human-readable format.

        Handles standard Error(string) and Panic(uint256) selectors.
        Returns None if decoding fails (data will be shown as-is).
        """
        if len(data) < 10:
            return None

        selector = data[:10]

        # Error(string) - 0x08c379a0
        if selector == "0x08c379a0" and len(data) >= 138:
            try:
                from eth_abi import decode
                decoded = decode(["string"], bytes.fromhex(data[10:]))
                return decoded[0]
            except Exception:
                pass

        # Panic(uint256) - 0x4e487b71
        if selector == "0x4e487b71" and len(data) >= 74:
            try:
                from eth_abi import decode
                decoded = decode(["uint256"], bytes.fromhex(data[10:]))
                panic_code = decoded[0]
                panic_names = {
                    0x00: "generic panic",
                    0x01: "assertion failed",
                    0x11: "arithmetic overflow",
                    0x12: "division by zero",
                    0x21: "invalid enum value",
                    0x22: "storage encoding error",
                    0x31: "pop on empty array",
                    0x32: "array out of bounds",
                    0x41: "memory allocation error",
                    0x51: "zero function pointer",
                }
                return f"Panic({panic_code:#x}): {panic_names.get(panic_code, 'unknown')}"
            except Exception:
                pass

        # Custom error - return selector + truncated data for debugging
        if len(data) > 74:
            return f"Custom error {selector} ({len(data)//2 - 4} bytes)"
        elif len(data) > 10:
            return f"Custom error {selector}"

        return None

    # =========================================================================
    # Health and diagnostics
    # =========================================================================

    def get_health(self) -> dict[str, Any]:
        """Get health status of all endpoints."""
        endpoints = self._selector.endpoints
        healthy_count = sum(1 for e in endpoints if self._selector.is_healthy(e))
        metrics = get_metrics()
        for endpoint in endpoints:
            split = urlsplit(endpoint.url)
            netloc = split.hostname or ""
            if split.port:
                netloc = f"{netloc}:{split.port}"
            safe_url = urlunsplit((split.scheme, netloc, split.path, "", ""))
            metrics.gauge(RPC_ENDPOINT_HEALTH).set(
                1.0 if self._selector.is_healthy(endpoint) else 0.0,
                endpoint=safe_url or "unknown",
            )
        return {
            "healthy_endpoints": healthy_count,
            "total_endpoints": len(endpoints),
            "all_unhealthy": not self._selector.has_healthy_endpoint(),
            "endpoints": [
                {
                    "url": e.url[:50] + "..." if len(e.url) > 50 else e.url,
                    "healthy": self._selector.is_healthy(e),
                    "latency_ms": round(e.latency_ewma_ms, 1),
                    "consecutive_failures": e.consecutive_failures,
                }
                for e in endpoints
            ],
        }

    def close(self) -> None:
        """Close all connections."""
        # Web3 doesn't have explicit close, but we can clear references
        self._web3_instances.clear()
        logger.info("rpc.manager.closed")
