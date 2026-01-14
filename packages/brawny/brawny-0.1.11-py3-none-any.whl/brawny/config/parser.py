"""Configuration parsing for brawny.

Provides functions to load config from YAML files and environment variables.
"""

from __future__ import annotations

import os
import re
from dataclasses import replace

from brawny.model.enums import KeystoreType
from brawny.model.errors import ConfigError

try:
    import yaml
except ImportError:  # pragma: no cover - handled by dependency management
    yaml = None

# Pattern to match ${VAR_NAME}, ${VAR_NAME:-default}, or ${{VAR_NAME}} forms
ENV_VAR_PATTERN = re.compile(r"\$\{\{?([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}?\}")

_ADVANCED_FIELDS = {
    "poll_interval_seconds",
    "reorg_depth",
    "finality_confirmations",
    "default_deadline_seconds",
    "stuck_tx_seconds",
    "max_replacement_attempts",
    "gas_limit_multiplier",
    "default_priority_fee_gwei",
    "max_fee_cap_gwei",
    "fee_bump_percent",
    "rpc_timeout_seconds",
    "rpc_max_retries",
    "database_pool_size",
    "database_pool_max_overflow",
}

_REMOVED_ENV_KEYS = {
    "ALERTS_DX_ENABLED",
    "ALLOWED_SIGNERS",
    "BLOCK_HASH_HISTORY_SIZE",
    "ENABLE_BROWNIE_PASSWORD_FALLBACK",
    "CLAIM_TIMEOUT_SECONDS",
    "DB_CIRCUIT_BREAKER_FAILURES",
    "DB_CIRCUIT_BREAKER_SECONDS",
    "DEEP_REORG_PAUSE",
    "DEEP_REORG_ALERT_ENABLED",
    "ETHERSCAN_API_URL",
    "INTENT_RETRY_BACKOFF_SECONDS",
    "JOB_MODULES",
    "JOBS_PATH",
    "LOG_FORMAT",
    "RPC_CIRCUIT_BREAKER_SECONDS",
    "SHUTDOWN_GRACE_SECONDS",
    "SHUTDOWN_TIMEOUT_SECONDS",
    "MAX_FEE",
    "METRICS_BIND",
    "METRICS_ENABLED",
    "PRIORITY_FEE",
    "SOURCIFY_ENABLED",
    "TELEGRAM_CHAT_IDS",
    "WEBHOOK_URL",
}


def _is_chat_id(s: str) -> bool:
    """Check if string looks like a raw Telegram chat ID."""
    return s.lstrip("-").isdigit()


def _parse_telegram(raw: dict) -> "TelegramConfig":
    """Parse telegram config, handling both old and new formats.

    Normalizes all inputs (strips whitespace) and canonicalizes to TelegramConfig.
    """
    from brawny.config.models import TelegramConfig

    # New format: telegram.bot_token, telegram.chats, telegram.default
    if "telegram" in raw and isinstance(raw["telegram"], dict):
        tg = raw["telegram"]

        # Normalize bot_token
        bot_token = tg.get("bot_token")
        if bot_token:
            bot_token = bot_token.strip()

        # Normalize chats (strip keys and values, validate IDs look numeric)
        raw_chats = tg.get("chats", {})
        chats: dict[str, str] = {}
        for k, v in raw_chats.items():
            if not k or not v:
                continue
            k = k.strip()
            v = str(v).strip()
            if not _is_chat_id(v):
                raise ConfigError(f"telegram.chats.{k} must be a numeric chat ID, got: '{v}'")
            chats[k] = v

        # Normalize default to list, strip each entry
        default = tg.get("default", [])
        if isinstance(default, str):
            default = [default]
        default = [d.strip() for d in default if d and str(d).strip()]

        return TelegramConfig(
            bot_token=bot_token,
            chats=chats,
            default=default,
        )

    # Legacy format: telegram_bot_token, telegram_chat_id
    bot_token = raw.get("telegram_bot_token")
    chat_id = raw.get("telegram_chat_id")

    if bot_token:
        bot_token = str(bot_token).strip()
    if chat_id:
        chat_id = str(chat_id).strip()
        # Validate legacy chat_id is numeric too
        if not _is_chat_id(chat_id):
            raise ConfigError(f"telegram_chat_id must be numeric, got: '{chat_id}'")

    if bot_token or chat_id:
        # Migrate to canonical form
        chats = {"default": chat_id} if chat_id else {}
        default = ["default"] if chat_id else []
        return TelegramConfig(
            bot_token=bot_token,
            chats=chats,
            default=default,
        )

    return TelegramConfig()




def _interpolate_env_vars(
    value: object,
    missing: list[str] | None = None,
    path: str = "",
) -> object:
    """Recursively interpolate ${VAR}, ${VAR:-default}, and ${{VAR}} patterns in config values.

    Supports:
      - ${VAR_NAME} / ${{VAR_NAME}} - replaced with env var value, empty string if not set
      - ${VAR_NAME:-default} / ${{VAR_NAME:-default}} - replaced with env var value, or default if not set

    Args:
        value: Config value (string, list, dict, or primitive)

    Returns:
        Value with environment variables interpolated
    """
    if isinstance(value, str):
        def replacer(match: re.Match[str]) -> str:
            var_name = match.group(1)
            default_val = match.group(2)  # None if no default specified
            env_val = os.environ.get(var_name)
            if env_val is not None:
                return env_val
            if default_val is not None:
                return default_val
            if missing is not None:
                location = path or "<root>"
                missing.append(f"{var_name} (at {location})")
            return ""  # Return empty string for unset vars without default

        result = ENV_VAR_PATTERN.sub(replacer, value)
        # If the entire string was a variable that resolved to empty, return None
        # This allows filtering out empty RPC endpoints
        if result == "" and ENV_VAR_PATTERN.search(value):
            return None
        return result

    elif isinstance(value, list):
        interpolated = [
            _interpolate_env_vars(item, missing, f"{path}[{idx}]")
            for idx, item in enumerate(value)
        ]
        # Filter out None values (unset env vars) and empty strings from lists
        return [v for v in interpolated if v is not None and v != ""]

    elif isinstance(value, dict):
        return {
            k: _interpolate_env_vars(v, missing, f"{path}.{k}" if path else str(k))
            for k, v in value.items()
        }

    else:
        return value


def _get_env(key: str, default: str | None = None, required: bool = False) -> str | None:
    """Get environment variable with BRAWNY_ prefix."""
    full_key = f"BRAWNY_{key}"
    value = os.environ.get(full_key, default)
    if required and not value:
        raise ConfigError(f"Required environment variable {full_key} is not set")
    return value


def _env_is_set(key: str) -> bool:
    return f"BRAWNY_{key}" in os.environ


def _fail_removed_env_vars() -> None:
    removed = [key for key in _REMOVED_ENV_KEYS if _env_is_set(key)]
    if removed:
        raise ConfigError(
            "Removed config options detected in environment: "
            f"{sorted(removed)}. These options no longer exist."
        )


def _get_env_list(key: str, default: list[str] | None = None) -> list[str]:
    """Get comma-separated list from environment variable."""
    value = _get_env(key)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


def _get_env_int(key: str, default: int) -> int:
    """Get integer from environment variable."""
    value = _get_env(key)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"BRAWNY_{key} must be an integer, got: {value}")


def _get_env_float(key: str, default: float) -> float:
    """Get float from environment variable."""
    value = _get_env(key)
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        raise ConfigError(f"BRAWNY_{key} must be a number, got: {value}")


def _parse_env_int(key: str) -> int:
    value = _get_env(key)
    if value is None:
        raise ConfigError(f"Missing env override BRAWNY_{key}")
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"BRAWNY_{key} must be an integer, got: {value}")


def _parse_env_float(key: str) -> float:
    value = _get_env(key)
    if value is None:
        raise ConfigError(f"Missing env override BRAWNY_{key}")
    try:
        return float(value)
    except ValueError:
        raise ConfigError(f"BRAWNY_{key} must be a number, got: {value}")


def from_env() -> "Config":
    """Load configuration from environment variables."""
    from brawny.config.models import AdvancedConfig, Config, RPCGroupConfig
    from brawny.config.validation import canonicalize_endpoint, dedupe_preserve_order, InvalidEndpointError

    _fail_removed_env_vars()

    # Get required values
    database_url = _get_env("DATABASE_URL", required=True)
    if database_url is None:
        raise ConfigError("BRAWNY_DATABASE_URL is required")

    rpc_endpoints = _get_env_list("RPC_ENDPOINTS")
    if not rpc_endpoints:
        raise ConfigError("BRAWNY_RPC_ENDPOINTS is required (comma-separated list)")

    endpoints: list[str] = []
    for i, endpoint in enumerate(rpc_endpoints):
        try:
            endpoints.append(canonicalize_endpoint(endpoint))
        except InvalidEndpointError as e:
            raise ConfigError(f"rpc_endpoints[{i}]: {e}") from e
    endpoints = dedupe_preserve_order(endpoints)

    rpc_default_group = _get_env("RPC_DEFAULT_GROUP") or "primary"

    chain_id = _get_env_int("CHAIN_ID", 1)

    # Parse keystore type
    keystore_type_str = _get_env("KEYSTORE_TYPE", "file")
    try:
        keystore_type = KeystoreType(keystore_type_str)
    except ValueError:
        raise ConfigError(
            f"Invalid keystore type: {keystore_type_str}. "
            f"Must be one of: {', '.join(kt.value for kt in KeystoreType)}"
        )

    advanced_kwargs: dict[str, object] = {}
    if _env_is_set("POLL_INTERVAL_SECONDS"):
        advanced_kwargs["poll_interval_seconds"] = _parse_env_float("POLL_INTERVAL_SECONDS")
    if _env_is_set("REORG_DEPTH"):
        advanced_kwargs["reorg_depth"] = _parse_env_int("REORG_DEPTH")
    if _env_is_set("FINALITY_CONFIRMATIONS"):
        advanced_kwargs["finality_confirmations"] = _parse_env_int("FINALITY_CONFIRMATIONS")
    if _env_is_set("DEFAULT_DEADLINE_SECONDS"):
        advanced_kwargs["default_deadline_seconds"] = _parse_env_int("DEFAULT_DEADLINE_SECONDS")
    if _env_is_set("STUCK_TX_SECONDS"):
        advanced_kwargs["stuck_tx_seconds"] = _parse_env_int("STUCK_TX_SECONDS")
    if _env_is_set("MAX_REPLACEMENT_ATTEMPTS"):
        advanced_kwargs["max_replacement_attempts"] = _parse_env_int("MAX_REPLACEMENT_ATTEMPTS")
    if _env_is_set("GAS_LIMIT_MULTIPLIER"):
        advanced_kwargs["gas_limit_multiplier"] = _parse_env_float("GAS_LIMIT_MULTIPLIER")
    if _env_is_set("DEFAULT_PRIORITY_FEE_GWEI"):
        advanced_kwargs["default_priority_fee_gwei"] = _parse_env_float("DEFAULT_PRIORITY_FEE_GWEI")
    if _env_is_set("MAX_FEE_CAP_GWEI"):
        advanced_kwargs["max_fee_cap_gwei"] = _parse_env_float("MAX_FEE_CAP_GWEI")
    if _env_is_set("FEE_BUMP_PERCENT"):
        advanced_kwargs["fee_bump_percent"] = _parse_env_int("FEE_BUMP_PERCENT")
    if _env_is_set("RPC_TIMEOUT_SECONDS"):
        advanced_kwargs["rpc_timeout_seconds"] = _parse_env_float("RPC_TIMEOUT_SECONDS")
    if _env_is_set("RPC_MAX_RETRIES"):
        advanced_kwargs["rpc_max_retries"] = _parse_env_int("RPC_MAX_RETRIES")
    if _env_is_set("DATABASE_POOL_SIZE"):
        advanced_kwargs["database_pool_size"] = _parse_env_int("DATABASE_POOL_SIZE")
    if _env_is_set("DATABASE_POOL_MAX_OVERFLOW"):
        advanced_kwargs["database_pool_max_overflow"] = _parse_env_int("DATABASE_POOL_MAX_OVERFLOW")


    # Parse telegram config from env (legacy format)
    telegram_config = _parse_telegram({
        "telegram_bot_token": _get_env("TELEGRAM_BOT_TOKEN"),
        "telegram_chat_id": _get_env("TELEGRAM_CHAT_ID"),
    })

    config = Config(
        database_url=database_url,
        rpc_endpoints=endpoints,
        rpc_groups={rpc_default_group: RPCGroupConfig(endpoints=endpoints)},
        rpc_default_group=rpc_default_group,
        chain_id=chain_id,
        worker_count=_get_env_int("WORKER_COUNT", 1),
        advanced=AdvancedConfig(**advanced_kwargs) if advanced_kwargs else None,
        telegram=telegram_config,
        keystore_type=keystore_type,
        keystore_path=_get_env("KEYSTORE_PATH", "~/.brawny/keys") or "~/.brawny/keys",
    )

    config.validate()
    return config


def from_yaml(path: str) -> "Config":
    """Load configuration from a YAML file.

    Supports environment variable interpolation using ${VAR}, ${{VAR}}, or ${VAR:-default} syntax.
    For example:
        rpc_groups:
          primary:
            endpoints:
              - ${RPC_1}
              - ${RPC_2:-http://localhost:8545}
              - ${{RPC_3}}
        rpc_default_group: primary

    Empty/unset variables in lists are automatically filtered out.
    """
    from brawny.config.models import AdvancedConfig, Config, RPCGroupConfig
    from brawny.config.validation import (
        canonicalize_endpoint,
        dedupe_preserve_order,
        InvalidEndpointError,
        validate_no_removed_fields,
    )

    if yaml is None:
        raise ConfigError("PyYAML is required for YAML config support.")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except Exception as e:
        raise ConfigError(f"Failed to read config file {path}: {e}") from e

    if not isinstance(data, dict):
        raise ConfigError("Config file must contain a mapping at the top level.")

    # Interpolate environment variables in all config values
    missing: list[str] = []
    data = _interpolate_env_vars(data, missing)
    if not isinstance(data, dict):
        raise ConfigError("Config interpolation failed.")
    if missing:
        missing_list = ", ".join(sorted(set(missing)))
        raise ConfigError(
            f"Config interpolation failed. Missing environment variables: {missing_list}"
        )

    validate_no_removed_fields(data)

    advanced_data: dict[str, object] = {}
    if "advanced" in data:
        advanced_value = data.pop("advanced")
        if advanced_value is None:
            advanced_value = {}
        if not isinstance(advanced_value, dict):
            raise ConfigError("advanced must be a mapping")
        advanced_data = dict(advanced_value)

    # Parse rpc_groups with canonicalization + deduplication
    rpc_groups_data = data.pop("rpc_groups", {})
    rpc_groups: dict[str, RPCGroupConfig] = {}

    if rpc_groups_data:
        for name, group_data in rpc_groups_data.items():
            if not isinstance(group_data, dict):
                raise ConfigError(f"rpc_groups.{name} must be a mapping")

            endpoints_raw = group_data.get("endpoints", [])
            if not isinstance(endpoints_raw, list):
                raise ConfigError(f"rpc_groups.{name}.endpoints must be a list")

            # Strip → canonicalize → dedupe (once, here)
            # InvalidEndpointError from canonicalize → ConfigError with context
            endpoints = []
            for i, ep in enumerate(endpoints_raw):
                if not isinstance(ep, str):
                    raise ConfigError(f"rpc_groups.{name}.endpoints[{i}] must be string")
                # Skip empty strings (from unset env vars)
                if not ep.strip():
                    continue
                try:
                    canonical = canonicalize_endpoint(ep)
                    endpoints.append(canonical)
                except InvalidEndpointError as e:
                    raise ConfigError(f"rpc_groups.{name}.endpoints[{i}]: {e}") from e

            original_count = len(endpoints)
            endpoints = dedupe_preserve_order(endpoints)
            if len(endpoints) != original_count:
                # Log warning about deduplication (will be logged at config load time)
                import logging
                logging.getLogger(__name__).warning(
                    f"rpc_groups.{name}: removed {original_count - len(endpoints)} "
                    f"duplicate endpoint(s) after canonicalization"
                )

            rpc_groups[name] = RPCGroupConfig(endpoints=endpoints)

    data["rpc_groups"] = rpc_groups

    # Optional default group for routing (may be None)
    data["rpc_default_group"] = data.get("rpc_default_group")

    # Derive rpc_endpoints from default or single group (internal use)
    default_group = data.get("rpc_default_group")
    if default_group and default_group in rpc_groups:
        data["rpc_endpoints"] = rpc_groups[default_group].endpoints
    elif len(rpc_groups) == 1:
        data["rpc_endpoints"] = next(iter(rpc_groups.values())).endpoints
    else:
        data["rpc_endpoints"] = []

    if advanced_data:
        unknown = set(advanced_data.keys()) - _ADVANCED_FIELDS
        if unknown:
            raise ConfigError(f"Unknown advanced config fields: {sorted(unknown)}")
        data["advanced"] = AdvancedConfig(**advanced_data)

    # Parse telegram config (handles both new and legacy formats)
    telegram_config = _parse_telegram(data)
    # Remove raw telegram fields - they've been canonicalized
    data.pop("telegram", None)
    data.pop("telegram_bot_token", None)
    data.pop("telegram_chat_id", None)
    data["telegram"] = telegram_config

    config = Config(**data)
    config.validate()
    return config


def apply_env_overrides(config: "Config") -> tuple["Config", list[str]]:
    """Apply environment overrides to the current config."""
    from brawny.config.models import AdvancedConfig, Config, RPCGroupConfig, TelegramConfig
    from brawny.config.validation import canonicalize_endpoint, dedupe_preserve_order, InvalidEndpointError

    _fail_removed_env_vars()

    overrides: dict[str, object] = {}
    advanced_overrides: dict[str, object] = {}
    overridden: list[str] = []

    mapping = {
        "DATABASE_URL": ("database_url", _get_env),
        "RPC_DEFAULT_GROUP": ("rpc_default_group", _get_env),
        "CHAIN_ID": ("chain_id", _parse_env_int),
        "WORKER_COUNT": ("worker_count", _parse_env_int),
        "KEYSTORE_TYPE": ("keystore_type", _get_env),
        "KEYSTORE_PATH": ("keystore_path", _get_env),
    }

    for env_key, (field_name, parser) in mapping.items():
        if not _env_is_set(env_key):
            continue
        value = parser(env_key)
        if value is None:
            continue
        overrides[field_name] = value
        overridden.append(field_name)

    # Handle telegram env overrides (legacy format)
    telegram_token_override = _get_env("TELEGRAM_BOT_TOKEN") if _env_is_set("TELEGRAM_BOT_TOKEN") else None
    telegram_chat_override = _get_env("TELEGRAM_CHAT_ID") if _env_is_set("TELEGRAM_CHAT_ID") else None
    if telegram_token_override is not None or telegram_chat_override is not None:
        # Build new telegram config merging with existing
        base_telegram = config.telegram
        new_token = telegram_token_override.strip() if telegram_token_override else base_telegram.bot_token
        new_chats = dict(base_telegram.chats)
        new_default = list(base_telegram.default)

        if telegram_chat_override:
            chat_id = telegram_chat_override.strip()
            if not _is_chat_id(chat_id):
                raise ConfigError(f"BRAWNY_TELEGRAM_CHAT_ID must be numeric, got: '{chat_id}'")
            new_chats["default"] = chat_id
            if "default" not in new_default:
                new_default = ["default"] + new_default

        overrides["telegram"] = TelegramConfig(
            bot_token=new_token,
            chats=new_chats,
            default=new_default,
        )
        if telegram_token_override is not None:
            overridden.append("telegram.bot_token")
        if telegram_chat_override is not None:
            overridden.append("telegram.chat_id")

    advanced_mapping = {
        "POLL_INTERVAL_SECONDS": ("poll_interval_seconds", _parse_env_float),
        "REORG_DEPTH": ("reorg_depth", _parse_env_int),
        "FINALITY_CONFIRMATIONS": ("finality_confirmations", _parse_env_int),
        "DEFAULT_DEADLINE_SECONDS": ("default_deadline_seconds", _parse_env_int),
        "STUCK_TX_SECONDS": ("stuck_tx_seconds", _parse_env_int),
        "MAX_REPLACEMENT_ATTEMPTS": ("max_replacement_attempts", _parse_env_int),
        "GAS_LIMIT_MULTIPLIER": ("gas_limit_multiplier", _parse_env_float),
        "DEFAULT_PRIORITY_FEE_GWEI": ("default_priority_fee_gwei", _parse_env_float),
        "MAX_FEE_CAP_GWEI": ("max_fee_cap_gwei", _parse_env_float),
        "FEE_BUMP_PERCENT": ("fee_bump_percent", _parse_env_int),
        "RPC_TIMEOUT_SECONDS": ("rpc_timeout_seconds", _parse_env_float),
        "RPC_MAX_RETRIES": ("rpc_max_retries", _parse_env_int),
        "DATABASE_POOL_SIZE": ("database_pool_size", _parse_env_int),
        "DATABASE_POOL_MAX_OVERFLOW": ("database_pool_max_overflow", _parse_env_int),
    }

    for env_key, (field_name, parser) in advanced_mapping.items():
        if not _env_is_set(env_key):
            continue
        value = parser(env_key)
        advanced_overrides[field_name] = value
        overridden.append(f"advanced.{field_name}")

    rpc_endpoints_override: list[str] | None = None
    if _env_is_set("RPC_ENDPOINTS"):
        raw_endpoints = _get_env_list("RPC_ENDPOINTS")
        endpoints: list[str] = []
        for i, endpoint in enumerate(raw_endpoints):
            try:
                endpoints.append(canonicalize_endpoint(endpoint))
            except InvalidEndpointError as e:
                raise ConfigError(f"rpc_endpoints[{i}]: {e}") from e
        rpc_endpoints_override = dedupe_preserve_order(endpoints)

    if not overrides:
        return config, []

    if "keystore_type" in overrides:
        overrides["keystore_type"] = KeystoreType(str(overrides["keystore_type"]))

    if advanced_overrides:
        base_advanced = config.advanced or AdvancedConfig()
        overrides["advanced"] = replace(base_advanced, **advanced_overrides)

    if rpc_endpoints_override is not None:
        default_group = overrides.get("rpc_default_group") or config.rpc_default_group or "primary"
        overrides["rpc_default_group"] = default_group
        overrides["rpc_endpoints"] = rpc_endpoints_override
        overrides["rpc_groups"] = {default_group: RPCGroupConfig(endpoints=rpc_endpoints_override)}
        overridden.extend(["rpc_endpoints", "rpc_groups"])

    if "rpc_default_group" in overrides:
        default_group = str(overrides["rpc_default_group"])
        if default_group in config.rpc_groups:
            overrides["rpc_endpoints"] = config.rpc_groups[default_group].endpoints

    return replace(config, **overrides), overridden
