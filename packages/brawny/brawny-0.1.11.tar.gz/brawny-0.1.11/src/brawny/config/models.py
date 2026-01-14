"""Configuration models for brawny.

Defines dataclass models for all configuration sections.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from brawny.model.enums import KeystoreType

DEFAULT_BLOCK_HASH_HISTORY_SIZE = 256
DEFAULT_JOB_ERROR_BACKOFF_BLOCKS = 1
DEFAULT_INTENT_RETRY_BACKOFF_SECONDS = 5
DEFAULT_NONCE_RECONCILE_INTERVAL_SECONDS = 300
DEFAULT_STUCK_TX_BLOCKS = 50
DEFAULT_SHUTDOWN_TIMEOUT_SECONDS = 30
DEFAULT_RPC_RETRY_BACKOFF_BASE = 1.0
DEFAULT_RPC_CIRCUIT_BREAKER_SECONDS = 300
DEFAULT_DB_CIRCUIT_BREAKER_FAILURES = 5
DEFAULT_DB_CIRCUIT_BREAKER_SECONDS = 30
DEFAULT_GAS_REFRESH_SECONDS = 15
DEFAULT_FALLBACK_GAS_LIMIT = 500_000
DEFAULT_TELEGRAM_RATE_LIMIT_PER_MINUTE = 20
DEFAULT_ABI_CACHE_TTL_SECONDS = 86400 * 7
DEFAULT_DATABASE_POOL_TIMEOUT_SECONDS = 30.0
DEFAULT_NONCE_GAP_ALERT_SECONDS = 300
DEFAULT_MAX_EXECUTOR_RETRIES = 5
DEFAULT_FINALITY_CONFIRMATIONS = 12


@dataclass
class TelegramConfig:
    """Telegram alert configuration.

    Fields:
        bot_token: Bot token for API calls (None = disabled)
        chats: Named chat targets (e.g., {"ops": "-100...", "dev": "-100..."})
        default: Default targets when job.alert_to not specified
        health_chat: Chat name for daemon health alerts (None = logged only)
        health_cooldown_seconds: Deduplication window for health alerts
    """

    bot_token: str | None = None
    chats: dict[str, str] = field(default_factory=dict)  # name -> chat_id
    default: list[str] = field(default_factory=list)  # Always a list internally
    health_chat: str | None = None  # e.g. "ops" - where daemon health alerts go
    health_cooldown_seconds: int = 1800  # 30 minutes between identical alerts


@dataclass
class RPCGroupConfig:
    """A named collection of RPC endpoints."""

    endpoints: list[str] = field(default_factory=list)  # Canonicalized + deduped at parse time


@dataclass
class AdvancedConfig:
    """
    Advanced options.

    RULE:
    - If this exceeds ~25 fields, something is wrong.
    - New options must justify why they are user-facing at all.
    - AdvancedConfig may only contain tuning parameters, not semantic switches.
      No feature flags or behavior-class booleans (e.g., enable_x/disable_y).
    """

    # Polling
    poll_interval_seconds: float = 1.0
    reorg_depth: int = 32
    finality_confirmations: int = DEFAULT_FINALITY_CONFIRMATIONS

    # Execution
    default_deadline_seconds: int = 3600
    stuck_tx_seconds: int = 300
    max_replacement_attempts: int = 5

    # Gas (gwei)
    gas_limit_multiplier: float = 1.2
    default_priority_fee_gwei: float = 1.5
    max_fee_cap_gwei: float | None = 500.0
    fee_bump_percent: int = 15

    # RPC
    rpc_timeout_seconds: float = 30.0
    rpc_max_retries: int = 3

    # Database pool (Postgres only)
    database_pool_size: int = 5
    database_pool_max_overflow: int = 10

    # Job logs
    log_retention_days: int = 7


@dataclass
class Config:
    """Main configuration for brawny.

    NOTE: Direct construction does NOT validate. Use Config.from_yaml() or
    Config.from_env() for validated configuration, or call .validate() explicitly.
    """

    # Required fields (no defaults) must come first
    database_url: str
    rpc_endpoints: list[str]  # Derived from rpc_groups; not user-facing

    # RPC Groups (for per-job read/broadcast routing)
    rpc_groups: dict[str, RPCGroupConfig]

    # Chain (required)
    chain_id: int

    # RPC default group (optional)
    rpc_default_group: str | None = None

    # Execution
    worker_count: int = 1

    # Advanced (rarely changed)
    advanced: AdvancedConfig | None = None

    # Telegram (canonical form - parsed from telegram: or legacy fields)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)

    # Metrics
    metrics_port: int = 9091

    # Keystore (required)
    keystore_type: KeystoreType = KeystoreType.FILE
    keystore_path: str = "~/.brawny/keys"

    def validate(self) -> None:
        """Validate configuration.

        Raises:
            ConfigError: If validation fails
        """
        from brawny.config.validation import validate_config, validate_advanced_config

        validate_config(self)
        validate_advanced_config(self._advanced_or_default())

    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database."""
        return self.database_url.startswith("sqlite:///")

    @property
    def is_postgres(self) -> bool:
        """Check if using PostgreSQL database."""
        return self.database_url.startswith(("postgresql://", "postgres://"))

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        from brawny.config.parser import from_env as _from_env
        return _from_env()

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        """Load configuration from a YAML file.

        Supports environment variable interpolation using ${VAR}, ${{VAR}}, or ${VAR:-default} syntax.
        """
        from brawny.config.parser import from_yaml as _from_yaml
        return _from_yaml(path)

    def apply_env_overrides(self) -> tuple["Config", list[str]]:
        """Apply environment overrides to the current config."""
        from brawny.config.parser import apply_env_overrides as _apply_env_overrides
        return _apply_env_overrides(self)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def redacted_dict(self) -> dict[str, object]:
        from urllib.parse import urlsplit, urlunsplit

        def _redact_url(value: str) -> str:
            try:
                split = urlsplit(value)
            except Exception:
                return "***"
            netloc = split.netloc
            if "@" in netloc:
                netloc = "***@" + netloc.split("@", 1)[1]
            return urlunsplit((split.scheme, netloc, split.path, "", ""))

        data = self.to_dict()
        redacted: dict[str, object] = {}
        for key, value in data.items():
            if any(word in key.lower() for word in ("token", "secret", "key", "password")):
                redacted[key] = "***"
            elif key == "rpc_endpoints" and isinstance(value, list):
                redacted[key] = [_redact_url(str(v)) for v in value]
            elif key == "rpc_groups" and isinstance(value, dict):
                redacted_groups: dict[str, object] = {}
                for group_name, group_value in value.items():
                    if isinstance(group_value, dict):
                        endpoints = group_value.get("endpoints")
                        if isinstance(endpoints, list):
                            group_value = {
                                **group_value,
                                "endpoints": [_redact_url(str(v)) for v in endpoints],
                            }
                    redacted_groups[group_name] = group_value
                redacted[key] = redacted_groups
            elif key == "rpc_rate_limits" and isinstance(value, dict):
                redacted[key] = {
                    _redact_url(str(endpoint)): limiter for endpoint, limiter in value.items()
                }
            elif key == "telegram" and isinstance(value, dict):
                # Redact bot_token within telegram config
                redacted[key] = {
                    **value,
                    "bot_token": "***" if value.get("bot_token") else None,
                }
            elif isinstance(value, str) and key.endswith("url"):
                redacted[key] = _redact_url(value)
            else:
                redacted[key] = value
        return redacted

    def _advanced_or_default(self) -> AdvancedConfig:
        return self.advanced or AdvancedConfig()

    def _derive_claim_timeout_seconds(self) -> int:
        deadline = self._advanced_or_default().default_deadline_seconds
        return max(60, int(min(300, deadline / 12)))

    @property
    def poll_interval_seconds(self) -> float:
        return self._advanced_or_default().poll_interval_seconds

    @property
    def reorg_depth(self) -> int:
        return self._advanced_or_default().reorg_depth

    @property
    def finality_confirmations(self) -> int:
        return self._advanced_or_default().finality_confirmations

    @property
    def default_deadline_seconds(self) -> int:
        return self._advanced_or_default().default_deadline_seconds

    @property
    def stuck_tx_seconds(self) -> int:
        return self._advanced_or_default().stuck_tx_seconds

    @property
    def max_replacement_attempts(self) -> int:
        return self._advanced_or_default().max_replacement_attempts

    @property
    def gas_limit_multiplier(self) -> float:
        return self._advanced_or_default().gas_limit_multiplier

    @property
    def default_priority_fee_gwei(self) -> float:
        return self._advanced_or_default().default_priority_fee_gwei

    @property
    def max_fee_cap_gwei(self) -> float | None:
        return self._advanced_or_default().max_fee_cap_gwei

    @property
    def fee_bump_percent(self) -> int:
        return self._advanced_or_default().fee_bump_percent

    @property
    def rpc_timeout_seconds(self) -> float:
        return self._advanced_or_default().rpc_timeout_seconds

    @property
    def rpc_max_retries(self) -> int:
        return self._advanced_or_default().rpc_max_retries

    @property
    def database_pool_size(self) -> int:
        return self._advanced_or_default().database_pool_size

    @property
    def database_pool_max_overflow(self) -> int:
        return self._advanced_or_default().database_pool_max_overflow

    @property
    def priority_fee(self) -> int:
        return int(self.default_priority_fee_gwei * 1_000_000_000)

    @property
    def max_fee(self) -> int | None:
        cap = self.max_fee_cap_gwei
        if cap is None:
            return None
        return int(cap * 1_000_000_000)

    @property
    def job_error_backoff_blocks(self) -> int:
        return DEFAULT_JOB_ERROR_BACKOFF_BLOCKS

    @property
    def block_hash_history_size(self) -> int:
        return DEFAULT_BLOCK_HASH_HISTORY_SIZE

    @property
    def deep_reorg_pause(self) -> bool:
        return False

    @property
    def claim_timeout_seconds(self) -> int:
        return self._derive_claim_timeout_seconds()

    @property
    def intent_retry_backoff_seconds(self) -> int:
        return DEFAULT_INTENT_RETRY_BACKOFF_SECONDS

    @property
    def max_executor_retries(self) -> int:
        return DEFAULT_MAX_EXECUTOR_RETRIES

    @property
    def nonce_reconcile_interval_seconds(self) -> int:
        return DEFAULT_NONCE_RECONCILE_INTERVAL_SECONDS

    @property
    def stuck_tx_blocks(self) -> int:
        return DEFAULT_STUCK_TX_BLOCKS

    @property
    def shutdown_timeout_seconds(self) -> int:
        return DEFAULT_SHUTDOWN_TIMEOUT_SECONDS

    @property
    def shutdown_grace_seconds(self) -> int:
        return DEFAULT_SHUTDOWN_TIMEOUT_SECONDS

    @property
    def rpc_retry_backoff_base(self) -> float:
        return DEFAULT_RPC_RETRY_BACKOFF_BASE

    @property
    def rpc_circuit_breaker_seconds(self) -> int:
        return DEFAULT_RPC_CIRCUIT_BREAKER_SECONDS

    @property
    def db_circuit_breaker_failures(self) -> int:
        return DEFAULT_DB_CIRCUIT_BREAKER_FAILURES

    @property
    def db_circuit_breaker_seconds(self) -> int:
        return DEFAULT_DB_CIRCUIT_BREAKER_SECONDS

    @property
    def rpc_rate_limit_per_second(self) -> float | None:
        return None

    @property
    def rpc_rate_limit_burst(self) -> int | None:
        return None

    @property
    def rpc_rate_limits(self) -> dict[str, dict[str, float | int]]:
        return {}

    @property
    def gas_refresh_seconds(self) -> int:
        return DEFAULT_GAS_REFRESH_SECONDS

    @property
    def fallback_gas_limit(self) -> int:
        return DEFAULT_FALLBACK_GAS_LIMIT

    @property
    def telegram_rate_limit_per_minute(self) -> int:
        return DEFAULT_TELEGRAM_RATE_LIMIT_PER_MINUTE

    @property
    def abi_cache_ttl_seconds(self) -> int:
        return DEFAULT_ABI_CACHE_TTL_SECONDS

    @property
    def database_pool_timeout_seconds(self) -> float:
        return DEFAULT_DATABASE_POOL_TIMEOUT_SECONDS

    @property
    def allow_unsafe_nonce_reset(self) -> bool:
        return False

    @property
    def nonce_gap_alert_seconds(self) -> int:
        return DEFAULT_NONCE_GAP_ALERT_SECONDS

    @property
    def brownie_password_fallback(self) -> bool:
        return False

    @property
    def log_retention_days(self) -> int:
        return self._advanced_or_default().log_retention_days
