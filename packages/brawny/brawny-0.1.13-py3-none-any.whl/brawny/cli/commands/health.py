"""Health check command."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any

import click

from brawny.cli.helpers import get_db, print_json


@click.command()
@click.option("--format", "fmt", default="json", help="Output format (json or text)")
@click.option("--config", "config_path", default=None, help="Path to config.yaml")
def health(fmt: str, config_path: str | None) -> None:
    """Health check endpoint."""
    from brawny.config import Config, get_config
    from brawny._rpc import RPCManager

    try:
        if config_path:
            config = Config.from_yaml(config_path)
            config, _ = config.apply_env_overrides()
        else:
            config = get_config()
    except Exception as e:
        if fmt == "json":
            print_json({"status": "unhealthy", "error": f"Config error: {e}"})
        else:
            click.echo(f"UNHEALTHY: Config error: {e}")
        sys.exit(1)

    db = get_db(config_path)
    result: dict[str, Any] = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {},
    }

    try:
        db_stats = db.get_database_stats()
        result["components"]["database"] = {
            "status": "ok",
            "type": db_stats.get("type", "unknown"),
        }

        try:
            rpc = RPCManager.from_config(config)
            rpc_health = rpc.get_health()
            result["components"]["rpc"] = {
                "status": "ok" if rpc_health["healthy_endpoints"] > 0 else "degraded",
                "healthy_endpoints": rpc_health["healthy_endpoints"],
                "total_endpoints": rpc_health["total_endpoints"],
                "circuit_breaker_open": rpc_health["circuit_breaker_open"],
            }

            try:
                block_number = rpc.get_block_number()
                chain_id = rpc.get_chain_id()
                result["components"]["chain"] = {
                    "chain_id": chain_id,
                    "head_block": block_number,
                }
            except Exception as e:
                result["components"]["chain"] = {
                    "status": "error",
                    "error": str(e)[:100],
                }
                result["status"] = "degraded"
        except Exception as e:
            result["components"]["rpc"] = {
                "status": "error",
                "error": str(e)[:100],
            }
            result["status"] = "degraded"

        block_states = db_stats.get("block_states", [])
        if block_states and "chain" in result["components"]:
            result["components"]["chain"]["last_processed_block"] = block_states[0].get(
                "last_block"
            )

        intents_by_status = db_stats.get("intents_by_status", {})
        result["intents"] = {
            "pending": intents_by_status.get("pending", 0),
            "claimed": intents_by_status.get("claimed", 0),
            "created": intents_by_status.get("created", 0),
        }

    except Exception as e:
        result["status"] = "unhealthy"
        result["error"] = str(e)[:200]
    finally:
        db.close()

    if fmt == "json":
        print_json(result)
    else:
        click.echo(f"Status: {result['status'].upper()}")
        click.echo(f"Timestamp: {result['timestamp']}")
        for name, component in result.get("components", {}).items():
            status = component.get("status", "unknown")
            click.echo(f"  {name}: {status}")

    if result["status"] != "healthy":
        sys.exit(1)


def register(main) -> None:
    main.add_command(health)
