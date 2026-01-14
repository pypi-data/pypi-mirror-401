"""Simplified alert system.

Send alerts to Telegram or webhooks. No classes. No inheritance. No plugin architecture.

Usage:
    payload = AlertPayload(
        job_id="my-job",
        job_name="My Job",
        event_type=AlertEvent.CONFIRMED,
        message="Transaction confirmed!",
    )
    config = AlertConfig(
        telegram_token="...",
        telegram_chat_ids=["123456"],
    )
    await send_alert(payload, config)
"""

from __future__ import annotations

import asyncio
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Coroutine

if TYPE_CHECKING:
    from brawny.telegram import TelegramBot

import httpx

from brawny.logging import get_logger

logger = get_logger(__name__)


class AlertEvent(str, Enum):
    """Alert event types. Aligned with OE2 hook reduction."""

    TRIGGERED = "triggered"
    CONFIRMED = "confirmed"
    FAILED = "failed"


@dataclass
class AlertPayload:
    """Data object for alert content."""

    job_id: str
    job_name: str
    event_type: AlertEvent
    message: str
    parse_mode: str = "Markdown"
    chain_id: int = 1
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AlertConfig:
    """Transport configuration. Passed once, not spread across callsites."""

    telegram_token: str | None = None
    telegram_chat_ids: list[str] = field(default_factory=list)
    webhook_url: str | None = None
    rate_limit_seconds: float = 3.0


# Module-level state for rate limiting only
# NOTE: No module-level httpx.AsyncClient - asyncio objects are not safe to share
# across multiple event loops / loop lifetimes. For low-volume alerts, we create
# a fresh client per request (httpx context manager handles cleanup).
_last_sent: dict[str, datetime] = {}
# Use threading.Lock, not asyncio.Lock - avoids event loop binding issues
_last_sent_lock = threading.Lock()


async def send_alert(payload: AlertPayload, config: AlertConfig) -> None:
    """Send alert to configured destinations. Fire-and-forget."""
    tasks: list[Coroutine[Any, Any, None]] = []

    if config.telegram_token and config.telegram_chat_ids:
        for chat_id in config.telegram_chat_ids:
            if _should_send(payload, "telegram", chat_id, config.rate_limit_seconds):
                tasks.append(_send_telegram(config.telegram_token, chat_id, payload))

    if config.webhook_url:
        if _should_send(payload, "webhook", config.webhook_url, config.rate_limit_seconds):
            tasks.append(_send_webhook(config.webhook_url, payload))

    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                _log_failure(payload, tasks[i], result)


def _should_send(
    payload: AlertPayload,
    dest_type: str,
    destination_id: str,
    limit_seconds: float,
) -> bool:
    """Check rate limit. Key includes dest_type to avoid collisions.

    Key format: job_id:event_type:dest_type:destination_id
    - Multiple chat IDs rate-limited independently
    - Telegram + webhook don't suppress each other
    - dest_type prevents test collisions

    Uses threading.Lock (not asyncio.Lock) to avoid event loop binding issues.
    """
    key = f"{payload.job_id}:{payload.event_type.value}:{dest_type}:{destination_id}"

    with _last_sent_lock:
        now = datetime.utcnow()
        if key in _last_sent:
            if (now - _last_sent[key]).total_seconds() < limit_seconds:
                return False
        _last_sent[key] = now
        return True


async def _send_telegram(token: str, chat_id: str, payload: AlertPayload) -> None:
    """Send message to Telegram. Pure function, no state."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": payload.message,
        "parse_mode": payload.parse_mode,
        "disable_web_page_preview": True,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=data)
        resp.raise_for_status()


async def _send_webhook(url: str, payload: AlertPayload) -> None:
    """Send payload to webhook. Pure function, no state.

    Schema (frozen):
    - job_id: str
    - job_name: str
    - event_type: str (enum value)
    - message: str
    - chain_id: int
    - timestamp: str (ISO8601 UTC)

    Do not add fields without versioning discussion.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            url,
            json={
                "job_id": payload.job_id,
                "job_name": payload.job_name,
                "event_type": payload.event_type.value,
                "message": payload.message,
                "chain_id": payload.chain_id,
                "timestamp": payload.timestamp.isoformat() + "Z",
            },
        )
        resp.raise_for_status()


def _log_failure(payload: AlertPayload, task: Coroutine[Any, Any, None], error: Exception) -> None:
    """Log alert failure with enough context to debug."""
    task_name = task.__qualname__ if hasattr(task, "__qualname__") else str(task)

    if "telegram" in task_name.lower():
        logger.warning(
            "alert_delivery_failed",
            job_id=payload.job_id,
            event_type=payload.event_type.value,
            destination="telegram",
            error=str(error),
        )
    elif "webhook" in task_name.lower():
        logger.warning(
            "alert_delivery_failed",
            job_id=payload.job_id,
            event_type=payload.event_type.value,
            destination="webhook",
            error=str(error),
        )
    else:
        logger.warning(
            "alert_delivery_failed",
            job_id=payload.job_id,
            event_type=payload.event_type.value,
            error=str(error),
        )


# =============================================================================
# Public alert() Function for Job Hooks
# =============================================================================


def alert(
    message: str,
    *,
    to: str | list[str] | None = None,
    parse_mode: str | None = None,
    disable_web_page_preview: bool = True,
    disable_notification: bool = False,
) -> None:
    """Send alert from within a job hook.

    Handles routing resolution, then delegates to TelegramBot.send_message().

    Uses Telegram Bot API parameter names verbatim. No aliases or renaming.
    Refer to https://core.telegram.org/bots/api#sendmessage for parameter docs.

    Args:
        message: Alert text (up to 4096 characters, auto-truncated)
        to: Override routing target (name, raw ID, or list). If None,
            uses job's alert_to config, then global default.
            Note: This is a routing concept, not a Telegram API field.
        parse_mode: "Markdown", "MarkdownV2", "HTML", or None
        disable_web_page_preview: Disable link previews (default True)
        disable_notification: Send without notification sound (default False)

    Resolution order:
        1. `to` parameter (if provided)
        2. Job's alert_to config (if set)
        3. Global default (from config)

    Raises:
        RuntimeError: If called outside a job hook

    Note:
        Unknown chat names are logged and skipped (not raised). Startup
        validation catches typos during normal deployment; runtime errors
        are logged but don't crash hooks.

    Example:
        alert("Harvested successfully")
        alert("Debug info", to="dev", disable_notification=True)
        alert("Check https://etherscan.io/tx/...", disable_web_page_preview=False)
    """
    from brawny._context import get_alert_context
    from brawny.alerts.routing import resolve_targets

    ctx = get_alert_context()
    if ctx is None:
        raise RuntimeError("alert() must be called from within a job hook")

    # Get telegram config and bot from context
    tg_config = getattr(ctx, "telegram_config", None)
    bot = getattr(ctx, "telegram_bot", None)
    if not tg_config or not bot:
        return  # Silent no-op (warned once at startup)

    # Determine target
    if to is not None:
        target = to
    else:
        job_alert_to = getattr(ctx, "job_alert_to", None)
        target = job_alert_to if job_alert_to is not None else None

    # Resolve to chat IDs (unknown names logged + skipped, not raised)
    job_id = getattr(ctx, "job_id", None)
    chat_ids = resolve_targets(
        target,
        tg_config.chats,
        tg_config.default,
        job_id=job_id,
    )

    if not chat_ids:
        return  # No targets configured (or all were invalid)

    # Send to each resolved chat
    for chat_id in chat_ids:
        bot.send_message(
            message,
            chat_id=chat_id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
        )


async def _send_alert_logged(payload: AlertPayload, config: AlertConfig) -> None:
    """Fire-and-forget alert with exception logging."""
    try:
        await send_alert(payload, config)
    except Exception:
        logger.exception("Failed to send alert", job_id=payload.job_id)


# =============================================================================
# Health Alert Sender (distinct rate limiting from job alerts)
# =============================================================================

# Separate rate limiting for health alerts (prevents job alert noise from blocking health)
_health_last_sent: dict[str, datetime] = {}
_health_lock = threading.Lock()

HEALTH_RATE_LIMIT_SECONDS = 1.0  # Min interval between health messages to same chat


def _should_send_health(chat_id: str) -> bool:
    """Check rate limit for health alerts. Uses separate namespace from job alerts."""
    key = f"health:{chat_id}"
    with _health_lock:
        now = datetime.utcnow()
        if key in _health_last_sent:
            if (now - _health_last_sent[key]).total_seconds() < HEALTH_RATE_LIMIT_SECONDS:
                return False
        _health_last_sent[key] = now
        return True


def create_send_health(bot: "TelegramBot") -> "Callable[[str, str], None]":
    """Create a health alert sender bound to a TelegramBot instance.

    Returns a callable that accepts (chat_id, text) kwargs.
    Uses distinct rate limiting from job alerts to prevent cross-blocking.

    Args:
        bot: TelegramBot instance to use for sending

    Returns:
        Function that sends health alerts: fn(chat_id=..., text=...)

    Usage:
        send_fn = create_send_health(telegram_bot)
        send_fn(chat_id="-100...", text="Health alert message")
    """
    def send_health(*, chat_id: str, text: str) -> None:
        """Send a health alert via the standard pipeline.

        Uses distinct rate_limit_key to prevent job alerts from blocking health alerts.
        """
        if not bot.configured:
            return

        if not _should_send_health(chat_id):
            logger.debug(
                "health_alert.rate_limited",
                chat_id=chat_id,
            )
            return

        try:
            bot.send_message(
                text,
                chat_id=chat_id,
                disable_web_page_preview=True,
            )
        except Exception as e:
            logger.warning(
                "health_alert.send_failed",
                chat_id=chat_id,
                error=str(e)[:200],
            )

    return send_health
