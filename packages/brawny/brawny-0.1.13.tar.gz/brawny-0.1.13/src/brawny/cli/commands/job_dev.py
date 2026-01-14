"""Developer utilities for individual jobs."""

from __future__ import annotations

import os
import sys

import click

from brawny.cli.helpers import print_json


@click.group()
def job() -> None:
    """Developer utilities for a single job."""
    pass


@job.command("run")
@click.argument("job_id")
@click.option("--at-block", type=int, help="Run check/build against this block")
@click.option("--dry-run", is_flag=True, help="Run check only (skip build_intent)")
@click.option(
    "--jobs-module",
    "jobs_modules",
    multiple=True,
    help="Additional job module(s) to load",
)
@click.option("--config", "config_path", default="./config.yaml", help="Path to config.yaml")
def job_run(
    job_id: str,
    at_block: int | None,
    dry_run: bool,
    jobs_modules: tuple[str, ...],
    config_path: str,
) -> None:
    """Run check/build for a single job without sending transactions."""
    import time
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

    from brawny._context import _job_ctx, _current_job
    from brawny.config import Config
    from brawny.db import create_database
    from brawny.alerts.contracts import ContractSystem
    from brawny.jobs.kv import DatabaseJobKVStore
    from brawny.jobs.registry import get_registry
    from brawny.jobs.discovery import auto_discover_jobs, discover_jobs
    from brawny.logging import get_logger, setup_logging
    from brawny.model.enums import LogFormat
    from brawny.model.types import BlockInfo, JobContext, idempotency_key
    from brawny._rpc import RPCManager
    from brawny.scripting import set_job_context

    if not config_path or not os.path.exists(config_path):
        click.echo(
            f"Config file is required for job run and was not found: {config_path}",
            err=True,
        )
        sys.exit(1)

    config = Config.from_yaml(config_path)
    config, overrides = config.apply_env_overrides()

    log_level = os.environ.get("BRAWNY_LOG_LEVEL", "INFO")
    setup_logging(log_level, LogFormat.JSON, config.chain_id)
    log = get_logger(__name__)
    log.info(
        "config.loaded",
        path=config_path,
        overrides=overrides,
        config=config.redacted_dict(),
    )

    db = create_database(
        config.database_url,
        pool_size=config.database_pool_size,
        pool_max_overflow=config.database_pool_max_overflow,
        pool_timeout=config.database_pool_timeout_seconds,
        circuit_breaker_failures=config.db_circuit_breaker_failures,
        circuit_breaker_seconds=config.db_circuit_breaker_seconds,
    )
    db.connect()

    try:
        rpc = RPCManager.from_config(config)
        contract_system = ContractSystem(rpc, config)

        modules = list(jobs_modules)
        if modules:
            discover_jobs(modules)
        else:
            auto_discover_jobs()

        registry = get_registry()
        job_obj = registry.get(job_id)
        if job_obj is None:
            click.echo(f"Job '{job_id}' not found. Did you register it?", err=True)
            sys.exit(1)

        if at_block is not None:
            block_number = at_block
        else:
            with ThreadPoolExecutor(max_workers=1, thread_name_prefix="job_dev") as executor:
                number_future = executor.submit(rpc.get_block_number, timeout=5)
                try:
                    block_number = number_future.result(timeout=10)
                except FuturesTimeout:
                    click.echo("Timed out fetching latest block number.", err=True)
                    sys.exit(1)
        block_hash = "0x0"
        timestamp = 0

        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="job_dev") as executor:
            block_future = executor.submit(rpc.get_block, block_number, False, 5)
            try:
                block_data = block_future.result(timeout=10)
            except FuturesTimeout:
                block_data = None

        if block_data:
            block_hash = block_data.get("hash", "")
            if hasattr(block_hash, "hex"):
                block_hash = f"0x{block_hash.hex()}"
            timestamp = block_data.get("timestamp", 0)
        else:
            click.echo(
                f"Warning: timed out loading block {block_number}; using fallback data.",
                err=True,
            )

        block = BlockInfo(
            chain_id=config.chain_id,
            block_number=block_number,
            block_hash=block_hash,
            timestamp=timestamp,
        )

        job_config = db.get_job(job_id)
        ctx = JobContext(
            block=block,
            rpc=rpc,
            logger=log.bind(job_id=job_id),
            state={},
            job_config=job_config,
            kv=DatabaseJobKVStore(db, job_id),
            job_id=job_id,
            contract_system=contract_system,
            hook_name="check",
        )

        def _call_check():
            # Set contextvars for implicit context
            ctx_token = _job_ctx.set(ctx)
            job_token = _current_job.set(job_obj)
            set_job_context(True)
            try:
                return job_obj.check()
            finally:
                set_job_context(False)
                _job_ctx.reset(ctx_token)
                _current_job.reset(job_token)

        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="job_dev") as executor:
            start = time.time()
            future = executor.submit(_call_check)
            try:
                trigger = future.result(timeout=job_obj.check_timeout_seconds)
            except FuturesTimeout:
                click.echo(
                    f"check() timed out after {job_obj.check_timeout_seconds}s",
                    err=True,
                )
                sys.exit(1)

        elapsed = time.time() - start

        if not trigger:
            click.echo(f"No trigger (check completed in {elapsed:.2f}s).")
            return

        idem_parts = list(trigger.idempotency_parts) or [block.block_number]
        idem_key = idempotency_key(job_id, *idem_parts)

        click.echo("\nTrigger:")
        print_json(
            {
                "reason": trigger.reason,
                "tx_required": trigger.tx_required,
                "idempotency_parts": idem_parts,
                "idempotency_key": idem_key,
                "check_seconds": round(elapsed, 3),
            }
        )

        if dry_run or not trigger.tx_required:
            if dry_run:
                click.echo("Dry run enabled; skipping build_intent.")
            return

        ctx_build = JobContext(
            block=block,
            rpc=rpc,
            logger=log.bind(job_id=job_id),
            state={"trigger": trigger},
            job_config=job_config,
            kv=DatabaseJobKVStore(db, job_id),
            job_id=job_id,
            contract_system=contract_system,
            hook_name="build_intent",
        )

        def _call_build():
            # Set contextvars for implicit context
            ctx_token = _job_ctx.set(ctx_build)
            job_token = _current_job.set(job_obj)
            set_job_context(True)
            try:
                return job_obj.build_intent(trigger)
            finally:
                set_job_context(False)
                _job_ctx.reset(ctx_token)
                _current_job.reset(job_token)

        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="job_dev") as executor:
            future = executor.submit(_call_build)
            try:
                spec = future.result(timeout=job_obj.build_timeout_seconds)
            except FuturesTimeout:
                click.echo(
                    f"build_intent() timed out after {job_obj.build_timeout_seconds}s",
                    err=True,
                )
                sys.exit(1)

        click.echo("\nTxIntentSpec:")
        print_json(
            {
                "signer_address": spec.signer_address,
                "to_address": spec.to_address,
                "data": spec.data,
                "value_wei": spec.value_wei,
                "gas_limit": spec.gas_limit,
                "max_fee_per_gas": spec.max_fee_per_gas,
                "max_priority_fee_per_gas": spec.max_priority_fee_per_gas,
                "min_confirmations": spec.min_confirmations,
                "deadline_seconds": spec.deadline_seconds,
            }
        )
    finally:
        db.close()


def register(main) -> None:
    main.add_command(job)
