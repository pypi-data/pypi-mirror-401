"""Alerts extension with contract handles, ABI resolution, and event decoding.

This extension provides an ergonomic interface for job authors to:
- Interact with contracts in alert hooks
- Decode events from transaction receipts (brownie-compatible)
- Make contract reads
- Format messages with explorer links

Key components:
- AlertContext: Context passed to alert hooks with event access
- ContractHandle: Interface for contract function calls
- EventDict: Brownie-compatible event container
- ABIResolver: Automatic ABI resolution with caching

Formatting helpers (Markdown is the default):
- shorten(hash): "0x1234...5678"
- explorer_link(hash): "[🔗 View on Explorer](url)"
- escape_markdown_v2(text): Escapes special characters

Usage in alert hooks:

    from brawny import Contract
    from brawny.alerts import shorten, explorer_link

    def alert_confirmed(self, ctx: AlertContext) -> str:
        # Get contract handle (brownie-style)
        token = Contract("token")

        # Decode events from receipt (brownie-compatible)
        deposit = ctx.events["Deposit"][0]
        amount = deposit["assets"]

        # Make contract reads
        symbol = token.symbol()
        decimals = token.decimals()

        # Format with explorer links
        tx_link = explorer_link(ctx.receipt.transactionHash.hex())

        return f"Deposited {amount / 10**decimals} {symbol}\\n{tx_link}"
"""

from brawny.alerts.context import AlertContext, JobMetadata
from brawny.alerts.contracts import (
    ContractSystem,
    ContractHandle,
    FunctionCaller,
    ExplicitFunctionCaller,
)
from brawny.alerts.events import (
    EventAccessor,
    DecodedEvent,
    AttributeDict,
    LogEntry,
)
from brawny.alerts.abi_resolver import ABIResolver, ResolvedABI
from brawny.alerts.base import (
    shorten,
    explorer_link,
    escape_markdown_v2,
    get_explorer_url,
    format_tx_link,
    format_address_link,
)
from brawny.alerts.send import (
    AlertEvent,
    AlertPayload,
    AlertConfig,
    send_alert,
    alert,
)
from brawny.alerts.errors import (
    DXError,
    ABINotFoundError,
    ProxyResolutionError,
    StateChangingCallError,
    ReceiptRequiredError,
    EventNotFoundError,
    AmbiguousOverloadError,
    OverloadMatchError,
    FunctionNotFoundError,
    InvalidAddressError,
    EventDecodeError,
    ContractCallError,
    ABICacheError,
)

__all__ = [
    # Context
    "AlertContext",
    "JobMetadata",
    # Contracts
    "ContractHandle",
    "FunctionCaller",
    "ExplicitFunctionCaller",
    "ContractSystem",
    # Events
    "EventAccessor",
    "DecodedEvent",
    "AttributeDict",
    "LogEntry",
    # ABI Resolution
    "ABIResolver",
    "ResolvedABI",
    # Alert System
    "AlertEvent",
    "AlertPayload",
    "AlertConfig",
    "send_alert",
    "alert",
    # Formatting
    "shorten",
    "explorer_link",
    "escape_markdown_v2",
    "get_explorer_url",
    "format_tx_link",
    "format_address_link",
    # Errors
    "DXError",
    "ABINotFoundError",
    "ProxyResolutionError",
    "StateChangingCallError",
    "ReceiptRequiredError",
    "EventNotFoundError",
    "AmbiguousOverloadError",
    "OverloadMatchError",
    "FunctionNotFoundError",
    "InvalidAddressError",
    "EventDecodeError",
    "ContractCallError",
    "ABICacheError",
]
