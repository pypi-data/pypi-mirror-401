"""RPC management with multi-endpoint failover and health tracking.

OE6 Simplification:
- Uses EndpointSelector for health-aware endpoint ordering
- Explicit failover gate (only on RPCRetryableError)
- Removed circuit breaker and rate limiter (simpler error handling)
"""

from brawny._rpc.errors import (
    RPCError,
    RPCFatalError,
    RPCRecoverableError,
    RPCRetryableError,
    classify_error,
    normalize_error_code,
)
from brawny._rpc.manager import RPCManager
from brawny._rpc.selector import EndpointSelector, EndpointHealth
from brawny._rpc.context import (
    get_job_context,
    reset_job_context,
    set_job_context,
)

__all__ = [
    "RPCManager",
    "EndpointSelector",
    "EndpointHealth",
    "RPCError",
    "RPCFatalError",
    "RPCRecoverableError",
    "RPCRetryableError",
    "classify_error",
    "normalize_error_code",
    "get_job_context",
    "reset_job_context",
    "set_job_context",
]
