"""RPC error types and classification for brawny.

Error classification per SPEC:
- Retryable: Network/RPC issues, should retry with backoff
- Fatal TX: Transaction issues, do not retry with same params
- Recoverable TX: May succeed with different params (e.g., bumped gas)
"""

from __future__ import annotations

from brawny.model.errors import BrawnyError


class RPCError(BrawnyError):
    """Base RPC error."""

    def __init__(
        self,
        message: str,
        code: str | None = None,
        endpoint: str | None = None,
        method: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.endpoint = endpoint
        self.method = method


class RPCRetryableError(RPCError):
    """RPC error that should be retried.

    These are network/infrastructure issues that may resolve
    on retry or with a different endpoint.
    """

    pass


class RPCFatalError(RPCError):
    """Fatal RPC error that should not be retried.

    These are transaction-level errors that won't be fixed
    by retrying with the same parameters.
    """

    pass


class RPCRecoverableError(RPCError):
    """RPC error that may succeed with different parameters.

    Examples: underpriced transactions that need gas bump.
    """

    pass


class RPCPoolExhaustedError(RPCError):
    """All endpoints in a pool failed (internal, group-agnostic).

    This is raised by RPCManager when all endpoints fail during an operation.
    It does not include group context - the caller (broadcast layer) wraps
    this into RPCGroupUnavailableError with group context.
    """

    def __init__(
        self,
        message: str,
        endpoints: list[str],
        last_error: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.endpoints = endpoints
        self.last_error = last_error


class RPCGroupUnavailableError(RPCError):
    """All endpoints in a broadcast group are unavailable (user-facing).

    This is the user-facing error that includes group context. It wraps
    RPCPoolExhaustedError with the group name for logging and diagnostics.
    """

    def __init__(
        self,
        message: str,
        group_name: str | None,
        endpoints: list[str],
        last_error: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.group_name = group_name
        self.endpoints = endpoints
        self.last_error = last_error


# ============================================================================
# Retryable errors (network/infrastructure issues)
# ============================================================================
RETRYABLE_ERROR_CODES = frozenset({
    "timeout",
    "connection_refused",
    "connection_reset",
    "connection_error",
    "rate_limited",           # HTTP 429
    "bad_gateway",            # HTTP 502
    "service_unavailable",    # HTTP 503
    "gateway_timeout",        # HTTP 504
    "internal_error",         # JSON-RPC -32603
    "server_error",           # JSON-RPC -32000 to -32099
    "request_timeout",
    "network_error",
})

# HTTP status codes that indicate retryable errors
RETRYABLE_HTTP_STATUS = frozenset({429, 500, 502, 503, 504})

# JSON-RPC error codes that are retryable
# -32603: Internal error
# -32000 to -32099: Server error (implementation defined)
RETRYABLE_RPC_CODES = frozenset({-32603} | set(range(-32099, -32000 + 1)))


# ============================================================================
# Fatal transaction errors (do not retry with same params)
# ============================================================================
FATAL_TX_ERROR_CODES = frozenset({
    "nonce_too_low",          # Already used nonce
    "insufficient_funds",      # Need more ETH
    "gas_limit_exceeded",      # TX exceeds block gas limit
    "execution_reverted",      # Contract rejected
    "invalid_sender",          # Bad signature
    "invalid_nonce",          # Nonce issues
    "intrinsic_gas_too_low",  # Gas below intrinsic
    "exceeds_block_gas_limit",
    "account_balance_too_low",
    "tx_type_not_supported",
    "max_fee_too_low",
})

# Substrings in error messages that indicate fatal errors
FATAL_TX_SUBSTRINGS = frozenset({
    "nonce too low",
    "insufficient funds",
    "execution reverted",
    "invalid sender",
    "gas limit exceeded",
    "intrinsic gas too low",
    "already known",  # Transaction already in mempool
})


# ============================================================================
# Recoverable transaction errors (may succeed with different params)
# ============================================================================
RECOVERABLE_TX_ERROR_CODES = frozenset({
    "replacement_underpriced",  # Retry with bumped gas
    "transaction_underpriced",  # Base fee too low
    "underpriced",
    "max_priority_fee_too_low",
    "max_fee_per_gas_too_low",
})

# Substrings in error messages that indicate recoverable errors
RECOVERABLE_TX_SUBSTRINGS = frozenset({
    "replacement transaction underpriced",
    "transaction underpriced",
    "max priority fee",
    "max fee per gas",
})


def classify_error(
    error: Exception,
    http_status: int | None = None,
    rpc_code: int | None = None,
) -> type[RPCError]:
    """Classify an error into RPCRetryableError, RPCFatalError, or RPCRecoverableError.

    Args:
        error: The exception to classify
        http_status: HTTP status code if available
        rpc_code: JSON-RPC error code if available

    Returns:
        The appropriate error class
    """
    error_msg = str(error).lower()

    # Check HTTP status first
    if http_status and http_status in RETRYABLE_HTTP_STATUS:
        return RPCRetryableError

    # Check JSON-RPC error code
    if rpc_code and rpc_code in RETRYABLE_RPC_CODES:
        return RPCRetryableError

    # Check for recoverable TX errors (check before fatal)
    for substring in RECOVERABLE_TX_SUBSTRINGS:
        if substring in error_msg:
            return RPCRecoverableError

    # Check for fatal TX errors
    for substring in FATAL_TX_SUBSTRINGS:
        if substring in error_msg:
            return RPCFatalError

    # Check common error patterns
    if "timeout" in error_msg or "timed out" in error_msg:
        return RPCRetryableError
    if "connection" in error_msg:
        return RPCRetryableError
    if "rate limit" in error_msg:
        return RPCRetryableError
    if "reverted" in error_msg:
        return RPCFatalError
    if "nonce" in error_msg and ("low" in error_msg or "invalid" in error_msg):
        return RPCFatalError
    if "insufficient" in error_msg:
        return RPCFatalError

    # Default to retryable for unknown errors
    return RPCRetryableError


def normalize_error_code(error: Exception) -> str:
    """Extract a normalized error code from an exception.

    Args:
        error: The exception to normalize

    Returns:
        Normalized error code string
    """
    error_msg = str(error).lower()

    # Check known patterns
    for code in FATAL_TX_ERROR_CODES:
        if code.replace("_", " ") in error_msg or code.replace("_", "") in error_msg:
            return code

    for code in RECOVERABLE_TX_ERROR_CODES:
        if code.replace("_", " ") in error_msg or code.replace("_", "") in error_msg:
            return code

    for code in RETRYABLE_ERROR_CODES:
        if code.replace("_", " ") in error_msg or code.replace("_", "") in error_msg:
            return code

    # Generic fallback
    return "unknown_error"
