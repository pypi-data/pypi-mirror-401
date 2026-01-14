"""Templates for brawny init command."""

PYPROJECT_TEMPLATE = """\
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "brawny keeper project"
requires-python = ">=3.10"
dependencies = ["brawny>=0.1.0"]

[tool.setuptools.packages.find]
where = ["."]
include = ["{package_name}*"]
"""

CONFIG_TEMPLATE = """\
# brawny configuration
# See: https://github.com/yearn/brawny#configuration

# Core settings
database_url: sqlite:///data/brawny.db
rpc_groups:
  primary:
    endpoints:
      - ${{RPC_URL}}
rpc_default_group: primary
chain_id: 1

# Keystore configuration
# Options: "file" (preferred) or "env" (least preferred)
keystore_type: file
keystore_path: ~/.brawny/keys

# SQLite requires worker_count: 1. Use PostgreSQL for multi-worker setups.
worker_count: 1

# Prometheus metrics port (default: 9091)
# metrics_port: 9091

# Telegram alerts (optional)
# telegram:
#   bot_token: ${{TELEGRAM_BOT_TOKEN}}
#   chats:
#     ops: "-1001234567890"
#   default: ["ops"]

# Advanced settings (optional)
# advanced:
#   poll_interval_seconds: 1.0
#   reorg_depth: 32
#   default_deadline_seconds: 3600
"""

ENV_EXAMPLE_TEMPLATE = """\
# RPC endpoint (required)
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY

# Keystore password (file keystore mode)
# BRAWNY_KEYSTORE_PASSWORD_WORKER=your-password
# Then import the key:
# brawny accounts import --name worker --private-key 0x...

# Telegram alerts (optional)
# TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
"""

GITIGNORE_TEMPLATE = """\
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/

# brawny
data/
*.db
*.db-journal

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""

INIT_JOBS_TEMPLATE = '"""Job definitions - auto-discovered from ./jobs."""\n'

AGENTS_TEMPLATE = """
# Agent Guide: Build a Compliant brawny Job

This file is meant for user agents that generate new job files. It is a fast, practical spec.

## Golden Rules
- Avoid over-engineering.
- Aim for simplicity and elegance.

## Job File Checklist (Minimal)
- Location: `jobs/<job_name>.py`
- Import `Job` and `job`.
- Add `@job` decorator (omit it to hide a WIP job from discovery/validation).
- Implement `check()` (sync or async).
- If it sends a transaction, implement `build_intent()` (sync).

## Required vs Optional Hooks

### Required
- `check(self) -> Trigger | None` OR `check(self, ctx) -> Trigger | None`
  - Must return `trigger(...)` or `None`.
  - **Implicit style** `def check(self):` - use API helpers (`block`, `kv`, `Contract`, `ctx()`)
  - **Explicit style** `def check(self, ctx):` - ctx passed directly (param MUST be named 'ctx')
  - Can be async: `async def check(self)` or `async def check(self, ctx)`

### Required only for tx jobs
- `build_intent(self, trigger) -> TxIntentSpec`
  - Build calldata and return `intent(...)`.
  - Only called if `trigger.tx_required` is True.

### Optional simulation hook
- `validate_simulation(self, output) -> bool`
  - Return False to fail the intent after a successful simulation.

### Optional alert hooks
- `alert_triggered(self, ctx)` - Called when job triggers
- `alert_confirmed(self, ctx)` - Called after TX confirms (ctx.receipt available)
- `alert_failed(self, ctx)` - Called on failure (ctx.tx can be None for pre-broadcast failures)
  - Return `str`, `(str, parse_mode)`, or `None`.

### Optional lifecycle hooks
- `on_success(self, ctx, receipt, intent, attempt)`
- `on_failure(self, ctx, error, intent, attempt)`  # attempt can be None pre-broadcast

## Job Class Attributes

### Required (auto-derived if not set and @job is used)
- `job_id: str` - Stable identifier (must not change)
- `name: str` - Human-readable name for logs/alerts

### Optional scheduling
- `check_interval_blocks: int = 1` - Min blocks between check() calls
- `check_timeout_seconds: int = 30` - Timeout for check()
- `build_timeout_seconds: int = 10` - Timeout for build_intent()
- `max_in_flight_intents: int | None = None` - Cap on active intents

### Optional gas overrides (all values in wei)
- `max_fee: int | None = None` - Max fee cap for gating/txs (None = no gating)
- `priority_fee: int | None = None` - Tip override for this job

### Optional simulation
- `disable_simulation: bool = False` - Skip pre-broadcast simulation
- `rpc: str | None = None` - Override RPC for simulation

### Broadcast routing (via @job decorator)
Configure broadcast routing using the `@job` decorator:
```python
@job(job_id="arb_exec", rpc_group="flashbots", signer="hot1")
class ArbitrageExecutor(Job):
    ...
```
- `job_id` - Optional override (defaults to snake_case of class name)
- `rpc_group` - Name of RPC group for reads and broadcasts
- `broadcast_group` - Name of RPC group for broadcasts (default: uses rpc_default_group)
- `read_group` - Name of RPC group for read operations (default: uses rpc_default_group)
- `signer` - Name of signer alias (required for tx jobs)

Define RPC groups in config:
```yaml
rpc_groups:
  primary:
    endpoints:
      - https://eth.llamarpc.com
  private:
    endpoints:
      - https://rpc.flashbots.net
      - https://relay.flashbots.net
rpc_default_group: primary
```

### Alert routing
- `@job(alert_to="ops")` - Route alerts to named chat defined in config
- `@job(alert_to=["ops", "dev"])` - Route to multiple chats
- Names must be defined in `telegram.chats` config section
- If not specified, uses `telegram.default` from config

## Core API (What to Use)

### Contract access (brownie-style)
```python
from brawny import Contract
vault = Contract(self.vault_address)  # By address
decimals = vault.decimals()            # View call
data = vault.harvest.encode_input()    # Get calldata
```


### JSON interfaces (brownie-style)
Place ABI JSON files in `./interfaces`, then:
```python
from brawny import interface
token = interface.IERC20("0x1234...")
balance = token.balanceOf("0xabc...")
```

### Job hook helpers (implicit context)
```python
from brawny import trigger, intent, block, gas_ok
return trigger(reason="...", data={...}, idempotency_parts=[block.number])
return intent(signer_address="worker", to_address=addr, data=calldata)
```

### Event access in alert hooks (brownie-compatible)
```python
def alert_confirmed(self, ctx):
    deposit = ctx.events["Deposit"][0]  # First Deposit event
    amount = deposit["amount"]          # Field access
    if "Deposit" in ctx.events:         # Check if event exists
        ...
```

### Other context access
- `ctx()` - Get full CheckContext/BuildContext when using implicit style
- `block.number`, `block.timestamp` - Current block info
- `rpc.*` - RPC manager proxy (e.g., `rpc.get_gas_price()`)
- `gas_ok()` - Check if current gas is below job's max_fee (async)
- `gas_quote()` - Get current base_fee (async)
- `kv.get(key, default=None)`, `kv.set(key, value)` - Persistent KV store (import from brawny)

### Accounts
- Use `intent(signer_address=...)` with a signer alias or address.
- If you set `@job(signer="alias")`, use `self.signer` (alias) or `self.signer_address` (resolved address).
- The signer alias must exist in the accounts directory (`~/.brawny/accounts`).

## Example: Transaction Job

```python
from brawny import Job, job, Contract, trigger, intent, block

@job(signer="worker")
class MyKeeperJob(Job):
    job_id = "my_keeper"
    name = "My Keeper"
    check_interval_blocks = 1
    keeper_address = "0x..."

    def check(self, ctx):
        keeper = Contract(self.keeper_address)
        if keeper.canWork():
            return trigger(
                reason="Keeper can work",
                idempotency_parts=[block.number],
            )
        return None

    def build_intent(self, trig):
        keeper = Contract(self.keeper_address)
        return intent(
            signer_address=self.signer,
            to_address=self.keeper_address,
            data=keeper.work.encode_input(),
        )
```

## Example: Job with Custom Broadcast and Alerts

```python
from brawny import Job, Contract, trigger, intent, explorer_link
from brawny.jobs.registry import job

@job(rpc_group="flashbots", signer="treasury-signer", alert_to="private_ops")
class TreasuryJob(Job):
    \"\"\"Critical treasury operations with dedicated RPC and private alerts.\"\"\"

    name = "Treasury Operations"
    check_interval_blocks = 1
    treasury_address = "0x..."

    def check(self, ctx):
        treasury = Contract(self.treasury_address)
        if treasury.needsRebalance():
            return trigger(reason="Treasury needs rebalancing")
        return None

    def build_intent(self, trig):
        treasury = Contract(self.treasury_address)
        return intent(
            signer_address=self.signer,
            to_address=self.treasury_address,
            data=treasury.rebalance.encode_input(),
        )

    def alert_confirmed(self, ctx):
        if not ctx.tx:
            return None
        return f"Treasury rebalanced: {explorer_link(ctx.tx.hash)}"
```

## Example: Monitor-Only Job (Implicit Context Style)

```python
from brawny import Job, job, Contract, trigger, kv

@job
class MonitorJob(Job):
    job_id = "monitor"
    name = "Monitor"

    def check(self):  # No ctx param - uses implicit context
        value = Contract("0x...").value()
        last = kv.get("last", 0)
        if value > last:
            kv.set("last", value)
            return trigger(
                reason="Value increased",
                data={"value": value},
                tx_required=False,
            )
        return None
```

## Natural-Language -> Job Translation Guide

When a user says:
- **"Check X every block"** -> `check_interval_blocks = 1`
- **"Only run if gas below Y"** -> set `max_fee` (wei) and use `await gas_ok()` in async check()
- **"Use signer Z"** -> `@job(signer="Z")` and use `self.signer` in `intent(...)`
- **"Alert on success/failure"** -> implement `alert_confirmed` / `alert_failed`
- **"Remember last value"** -> use `kv.get/set` (import from brawny)
- **"Use Flashbots"** -> `@job(rpc_group="flashbots")` with flashbots group in config
- **"Send alerts to private channel"** -> `@job(alert_to="private_ops")` with chat in config

## Failure Modes

The `alert_failed` hook provides rich context about what failed and when.

### Failure Classification

**FailureType** (what failed):
- `SIMULATION_REVERTED` - TX would revert on-chain (permanent)
- `SIMULATION_NETWORK_ERROR` - RPC error during simulation (transient)
- `DEADLINE_EXPIRED` - Intent took too long (permanent)
- `SIGNER_FAILED` - Keystore/signer issue
- `NONCE_FAILED` - Couldn't reserve nonce
- `SIGN_FAILED` - Signing error
- `BROADCAST_FAILED` - RPC rejected transaction (transient)
- `TX_REVERTED` - On-chain revert (permanent)
- `NONCE_CONSUMED` - Nonce used by another transaction
- `CHECK_EXCEPTION` - job.check() raised an exception
- `BUILD_TX_EXCEPTION` - job.build_tx() raised an exception
- `UNKNOWN` - Fallback for unexpected failures

**FailureStage** (when it failed):
- `PRE_BROADCAST` - Failed before reaching the chain
- `BROADCAST` - Failed during broadcast
- `POST_BROADCAST` - Failed after broadcast (on-chain)

### AlertContext in alert_failed

```python
# AlertContext fields (all hooks)
ctx.job                  # JobMetadata (id, name)
ctx.trigger              # Trigger that initiated this flow
ctx.chain_id             # Chain ID
ctx.hook                 # HookType enum (TRIGGERED, CONFIRMED, FAILED)
ctx.tx                   # TxInfo | None (hash, nonce, gas params)
ctx.receipt              # TxReceipt | None (only in alert_confirmed)
ctx.block                # BlockInfo | None
ctx.error_info           # ErrorInfo | None (structured, JSON-safe)
ctx.failure_type         # FailureType | None
ctx.failure_stage        # FailureStage | None
ctx.events               # EventDict (only in alert_confirmed)

# AlertContext properties
ctx.is_permanent_failure # True if retrying won't help
ctx.is_transient_failure # True if failure might resolve on retry
ctx.error_message        # Convenience: error_info.message or "unknown"

# AlertContext methods
ctx.explorer_link(hash)  # "[🔗 View](url)" markdown link
ctx.shorten(hex_str)     # "0x1234...abcd"
ctx.has_receipt()        # True if receipt available
ctx.has_error()          # True if error_info available
```

### Example: Handling Failures

```python
from brawny import Job, job
from brawny.model.errors import FailureType

@job
class RobustJob(Job):
    job_id = "robust_job"
    name = "Robust Job"

    def alert_failed(self, ctx):
        # Suppress alerts for transient failures
        if ctx.is_transient_failure:
            return None  # No alert

        # Detailed message for permanent failures
        if ctx.failure_type == FailureType.SIMULATION_REVERTED:
            return f"TX would revert: {ctx.error_message}"
        elif ctx.failure_type == FailureType.TX_REVERTED:
            if not ctx.tx:
                return f"TX reverted on-chain: {ctx.error_message}"
            return f"TX reverted on-chain: {ctx.explorer_link(ctx.tx.hash)}"
        elif ctx.failure_type == FailureType.NONCE_CONSUMED:
            return "Nonce conflict! Check signer activity."
        elif ctx.failure_type == FailureType.CHECK_EXCEPTION:
            return f"check() crashed: {ctx.error_message}"
        elif ctx.failure_type == FailureType.BUILD_TX_EXCEPTION:
            return f"build_intent() crashed: {ctx.error_message}"
        else:
            return f"Failed ({ctx.failure_type.value}): {ctx.error_message}"
```

## Required Output from Agent
When generating a new job file, the agent must provide:
- File path
- Job class name
- `job_id` and `name`
- `check()` implementation
- `build_intent()` if tx required
- Any alert hooks requested
"""

EXAMPLES_TEMPLATE = '''\
"""Example job patterns - NOT registered.

These are reference implementations. To use them:
1. Copy the class to a new file (e.g., my_job.py)
2. Add @job decorator
3. Customize the implementation

Delete this file when you no longer need it.
"""
from brawny import Job, Contract, trigger, kv

# Note: No @job decorator - these are templates only


class MonitorOnlyJob(Job):
    """Monitor-only job - alerts without transactions.

    Use cases:
    - Price deviation alerts
    - Health check monitoring
    - Threshold breach notifications

    Outcome:
    - Creates: Trigger only (no intent, no transaction)
    - Alerts: alert_triggered only
    """

    job_id = "monitor_example"
    name = "Monitor Example"
    check_interval_blocks = 10

    def __init__(self, oracle_address: str, threshold_percent: float = 5.0):
        self.oracle_address = oracle_address
        self.threshold_percent = threshold_percent

    def check(self, ctx):
        """Check if condition is met.

        Returns:
            Trigger with tx_required=False, or None
        """
        oracle = Contract(self.oracle_address)
        price = oracle.latestAnswer() / 1e8

        last_price = kv.get("last_price")
        if last_price is not None:
            change_pct = abs(price - last_price) / last_price * 100
            if change_pct >= self.threshold_percent:
                kv.set("last_price", price)
                return trigger(
                    reason=f"Price changed {change_pct:.2f}%",
                    data={
                        "old_price": last_price,
                        "new_price": price,
                        "change_percent": change_pct,
                    },
                    tx_required=False,  # No transaction needed
                )

        kv.set("last_price", price)
        return None

    def alert_triggered(self, ctx):
        """Format alert message.

        Returns:
            Tuple of (message, parse_mode) or string
        """
        data = {}
        return (
            f"Price alert: {data['old_price']:.2f} -> {data['new_price']:.2f}\\n"
            f"Change: {data['change_percent']:.2f}%",
            "Markdown",
        )
'''

# Monitoring stack templates
DOCKER_COMPOSE_MONITORING_TEMPLATE = """\
# Production-friendly Prometheus + Grafana stack for Brawny
# Usage: docker-compose -f monitoring/docker-compose.yml up -d
#
# Access:
#   Prometheus: http://localhost:9090
#   Grafana:    http://localhost:3000 (admin / admin)
#
# For production, set GF_ADMIN_PASSWORD in environment or .env

services:
  prometheus:
    image: prom/prometheus:v2.48.0
    container_name: brawny-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
    extra_hosts:
      - "host.docker.internal:host-gateway"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:9090/-/ready"]
      interval: 10s
      timeout: 3s
      retries: 3
    restart: unless-stopped

  grafana:
    image: grafana/grafana:10.2.3
    container_name: brawny-grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${{GF_ADMIN_PASSWORD:-admin}}
      - GF_USERS_ALLOW_SIGN_UP=false
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/api/health"]
      interval: 10s
      timeout: 3s
      retries: 3
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
"""

PROMETHEUS_CONFIG_TEMPLATE = """\
# Prometheus configuration for Brawny
#
# Default: scrapes metrics from Brawny on host at localhost:9091
#
# Troubleshooting:
#   macOS/Windows: host.docker.internal:9091 works out of the box
#   Linux: if target is down, replace with your host IP (e.g., 172.17.0.1:9091)
#          or run Brawny in the same Docker network

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'brawny'
    static_configs:
      - targets: ['host.docker.internal:9091']
"""

GRAFANA_DATASOURCE_TEMPLATE = """\
# Auto-provision Prometheus datasource
# UID is stable so dashboards can reference it reliably
apiVersion: 1

datasources:
  - name: Prometheus
    uid: prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
"""

GRAFANA_DASHBOARDS_PROVIDER_TEMPLATE = """\
# Auto-provision dashboards from this directory
apiVersion: 1

providers:
  - name: 'brawny'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /etc/grafana/provisioning/dashboards
"""

GRAFANA_DASHBOARD_TEMPLATE = """\
{
  "annotations": {
    "list": []
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 1,
      "title": "Status",
      "type": "row"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [
            {
              "type": "value",
              "options": {
                "0": {
                  "text": "false"
                },
                "1": {
                  "text": "true"
                }
              }
            }
          ],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "red",
                "value": null
              },
              {
                "color": "green",
                "value": 1
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 0,
        "y": 1
      },
      "id": 2,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "max(up{job=\"brawny\"})",
          "refId": "A"
        }
      ],
      "title": "Brawny Up",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 120
              },
              {
                "color": "red",
                "value": 300
              }
            ]
          },
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 4,
        "y": 1
      },
      "id": 3,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "max(brawny_oldest_pending_intent_age_seconds)",
          "refId": "A"
        }
      ],
      "title": "Oldest Pending Intent",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 10
              },
              {
                "color": "red",
                "value": 50
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 8,
        "y": 1
      },
      "id": 4,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "sum(brawny_pending_intents) or vector(0)",
          "refId": "A"
        }
      ],
      "title": "Pending Intents",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 16,
        "y": 1
      },
      "id": 6,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "sum(brawny_blocks_processed_total) or vector(0)",
          "refId": "A"
        }
      ],
      "title": "Blocks Processed",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 4,
        "w": 4,
        "x": 20,
        "y": 1
      },
      "id": 7,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "sum(brawny_tx_confirmed_total) or vector(0)",
          "refId": "A"
        }
      ],
      "title": "TX Confirmed",
      "type": "stat"
    },
    {
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 5
      },
      "id": 10,
      "title": "Activity",
      "type": "row"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "line"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 120
              },
              {
                "color": "red",
                "value": 300
              }
            ]
          },
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 6
      },
      "id": 11,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "mode": "multi",
          "sort": "none"
        }
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "max(brawny_block_processing_lag_seconds)",
          "legendFormat": "seconds behind chain head",
          "refId": "A"
        }
      ],
      "title": "Block Processing Lag",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "line"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 120
              },
              {
                "color": "red",
                "value": 300
              }
            ]
          },
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 6
      },
      "id": 12,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "mode": "multi",
          "sort": "none"
        }
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "time() - max(brawny_last_tx_confirmed_timestamp)",
          "legendFormat": "seconds since last TX",
          "refId": "B"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "time() - max(brawny_last_intent_created_timestamp)",
          "legendFormat": "seconds since last intent",
          "refId": "C"
        }
      ],
      "title": "Activity Staleness",
      "type": "timeseries"
    },
    {
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 14
      },
      "id": 20,
      "title": "Transactions",
      "type": "row"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 15
      },
      "id": 21,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "mode": "multi",
          "sort": "none"
        }
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "sum(rate(brawny_tx_broadcast_total[5m])) * 60 or vector(0)",
          "legendFormat": "broadcast/min",
          "refId": "A"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "sum(rate(brawny_tx_confirmed_total[5m])) * 60 or vector(0)",
          "legendFormat": "confirmed/min",
          "refId": "B"
        },
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "sum(rate(brawny_tx_failed_total[5m])) * 60 or vector(0)",
          "legendFormat": "failed/min",
          "refId": "C"
        }
      ],
      "title": "TX Throughput",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "prometheus"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "line"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "yellow",
                "value": 120
              },
              {
                "color": "red",
                "value": 300
              }
            ]
          },
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 15
      },
      "id": 22,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "mode": "multi",
          "sort": "none"
        }
      },
      "pluginVersion": "10.2.3",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "expr": "max(brawny_oldest_pending_intent_age_seconds)",
          "legendFormat": "oldest pending age",
          "refId": "A"
        }
      ],
      "title": "Oldest Pending Intent Age",
      "type": "timeseries"
    }
  ],
  "refresh": "10s",
  "schemaVersion": 39,
  "tags": [
    "brawny"
  ],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-1h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "browser",
  "title": "Brawny Overview",
  "uid": "brawny-overview",
  "version": 1,
  "weekStart": ""
}
"""
