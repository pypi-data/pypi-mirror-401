"""Stuck transaction detection and replacement.

Implements transaction replacement logic from SPEC 9.4:
- Detect stuck transactions based on time and blocks
- Calculate replacement fees with proper bumping
- Create replacement attempts with linked history
- Enforce max replacement attempts and backoff
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import uuid4

from web3 import Web3

from brawny.logging import LogEvents, get_logger
from brawny.metrics import TX_REPLACED, get_metrics
from brawny.model.enums import AttemptStatus, IntentStatus
from brawny.tx.intent import transition_intent
from brawny.tx.utils import normalize_tx_dict
from brawny.model.types import GasParams

if TYPE_CHECKING:
    from brawny.config import Config
    from brawny.db.base import Database
    from brawny.keystore import Keystore
    from brawny.lifecycle import LifecycleDispatcher
    from brawny.model.types import TxAttempt, TxIntent
    from brawny._rpc.manager import RPCManager
    from brawny.tx.nonce import NonceManager

logger = get_logger(__name__)


@dataclass
class ReplacementResult:
    """Result of a replacement attempt."""

    success: bool
    new_attempt: TxAttempt | None = None
    new_tx_hash: str | None = None
    error: str | None = None


class TxReplacer:
    """Handle stuck transaction replacement.

    Implements SPEC 9.4 replacement policy:
    - Same nonce as original attempt
    - Bump both max_fee_per_gas and max_priority_fee_per_gas by fee_bump_percent
    - Link via replaces_attempt_id
    - Mark old attempt as replaced
    - Max max_replacement_attempts before abandoning
    - Double wait time between each replacement attempt
    """

    def __init__(
        self,
        db: Database,
        rpc: RPCManager,
        keystore: Keystore,
        nonce_manager: NonceManager,
        config: Config,
        lifecycle: "LifecycleDispatcher | None" = None,
    ) -> None:
        """Initialize transaction replacer.

        Args:
            db: Database connection
            rpc: RPC manager for chain queries
            keystore: Keystore for transaction signing
            nonce_manager: Nonce manager
            config: Application configuration
        """
        self._db = db
        self._rpc = rpc
        self._keystore = keystore
        self._nonce_manager = nonce_manager
        self._config = config
        self._lifecycle = lifecycle

    def calculate_replacement_fees(self, old_params: GasParams) -> GasParams:
        """Calculate bumped fees for replacement transaction.

        Per Ethereum protocol, replacement must have at least 10% higher fees.
        Uses configured fee_bump_percent (default 15%).

        Args:
            old_params: Previous gas parameters

        Returns:
            New gas parameters with bumped fees
        """
        from brawny.tx.fees import bump_fees

        return bump_fees(
            old_params,
            bump_percent=self._config.fee_bump_percent,
            max_fee_cap=self._config.max_fee,
        )

    def get_replacement_count(self, intent_id) -> int:
        """Get number of replacement attempts for an intent.

        Args:
            intent_id: Intent ID

        Returns:
            Number of attempts that are replacements
        """
        attempts = self._db.get_attempts_for_intent(intent_id)
        return sum(1 for a in attempts if a.replaces_attempt_id is not None)

    def should_replace(self, intent: TxIntent, attempt: TxAttempt) -> bool:
        """Check if a transaction should be replaced.

        Args:
            intent: Transaction intent
            attempt: Current transaction attempt

        Returns:
            True if transaction should be replaced
        """
        if not attempt.broadcast_block or not attempt.tx_hash:
            return False

        # Check max replacements
        replacement_count = self.get_replacement_count(intent.intent_id)
        if replacement_count >= self._config.max_replacement_attempts:
            logger.info(
                "replacement.max_reached",
                intent_id=str(intent.intent_id),
                count=replacement_count,
                max=self._config.max_replacement_attempts,
            )
            return False

        # Check time elapsed using Unix timestamps (no timezone issues)
        import time

        if not attempt.broadcast_at:
            return False

        elapsed_seconds = time.time() - attempt.broadcast_at.timestamp()

        # Double wait time for each replacement attempt
        wait_multiplier = 2 ** replacement_count
        required_wait = self._config.stuck_tx_seconds * wait_multiplier

        if elapsed_seconds < required_wait:
            return False

        # Check if still pending (no receipt)
        receipt = self._rpc.get_transaction_receipt(attempt.tx_hash)
        if receipt is not None:
            # Has receipt - don't replace
            return False

        # Check blocks elapsed
        try:
            current_block = self._rpc.get_block_number()
            blocks_since = current_block - attempt.broadcast_block

            required_blocks = self._config.stuck_tx_blocks * wait_multiplier
            if blocks_since < required_blocks:
                return False
        except Exception:
            pass

        return True

    def replace_transaction(
        self,
        intent: TxIntent,
        attempt: TxAttempt,
    ) -> ReplacementResult:
        """Create a replacement transaction with bumped fees.

        Uses the same nonce as the original attempt but with higher fees.

        Args:
            intent: Transaction intent
            attempt: Current stuck attempt

        Returns:
            ReplacementResult with new attempt if successful
        """
        if attempt.tx_hash:
            try:
                receipt = self._rpc.get_transaction_receipt(attempt.tx_hash)
            except Exception as e:
                logger.warning(
                    "replacement.receipt_check_failed",
                    intent_id=str(intent.intent_id),
                    attempt_id=str(attempt.attempt_id),
                    tx_hash=attempt.tx_hash,
                    error=str(e)[:200],
                )
                receipt = None
            if receipt:
                logger.info(
                    "replacement.skip_confirmed",
                    intent_id=str(intent.intent_id),
                    attempt_id=str(attempt.attempt_id),
                    tx_hash=attempt.tx_hash,
                )
                return ReplacementResult(success=False, error="already_confirmed")

        current_intent = self._db.get_intent(intent.intent_id)
        if current_intent is None or current_intent.status != IntentStatus.PENDING:
            return ReplacementResult(success=False, error="intent_not_pending")

        logger.info(
            "replacement.starting",
            intent_id=str(intent.intent_id),
            attempt_id=str(attempt.attempt_id),
            old_tx_hash=attempt.tx_hash,
            nonce=attempt.nonce,
        )

        # Calculate new gas parameters
        new_gas_params = self.calculate_replacement_fees(attempt.gas_params)

        # Checksum addresses for RPC/signing
        signer_address = Web3.to_checksum_address(intent.signer_address)
        to_address = Web3.to_checksum_address(intent.to_address)

        # Build replacement transaction (same nonce!)
        tx_dict = {
            "nonce": attempt.nonce,  # SAME nonce as original
            "to": to_address,
            "value": intent.value_wei,
            "gas": new_gas_params.gas_limit,
            "maxFeePerGas": new_gas_params.max_fee_per_gas,
            "maxPriorityFeePerGas": new_gas_params.max_priority_fee_per_gas,
            "chainId": intent.chain_id,
            "type": 2,  # EIP-1559
        }

        if intent.data:
            tx_dict["data"] = intent.data

        tx_dict = normalize_tx_dict(tx_dict)

        try:
            # Sign transaction
            signed_tx = self._keystore.sign_transaction(
                tx_dict,
                signer_address,
            )
        except Exception as e:
            logger.error(
                "replacement.sign_failed",
                intent_id=str(intent.intent_id),
                error=str(e)[:200],
            )
            return ReplacementResult(success=False, error=f"Sign failed: {e}")

        # Create new attempt record
        new_attempt_id = uuid4()
        new_attempt = self._db.create_attempt(
            attempt_id=new_attempt_id,
            intent_id=intent.intent_id,
            nonce=attempt.nonce,  # Same nonce
            gas_params_json=new_gas_params.to_json(),
            status=AttemptStatus.SIGNED.value,
            replaces_attempt_id=attempt.attempt_id,
        )

        try:
            # Broadcast replacement
            tx_hash, _endpoint_url = self._rpc.send_raw_transaction(signed_tx.raw_transaction)

            # Update new attempt with tx_hash
            current_block = self._rpc.get_block_number()
            self._db.update_attempt_status(
                new_attempt_id,
                AttemptStatus.BROADCAST.value,
                tx_hash=tx_hash,
                broadcast_block=current_block,
            )

            # Mark old attempt as replaced
            self._db.update_attempt_status(
                attempt.attempt_id,
                AttemptStatus.REPLACED.value,
            )

            logger.info(
                LogEvents.TX_REPLACED,
                intent_id=str(intent.intent_id),
                old_attempt_id=str(attempt.attempt_id),
                new_attempt_id=str(new_attempt_id),
                old_tx_hash=attempt.tx_hash,
                new_tx_hash=tx_hash,
                nonce=attempt.nonce,
                old_max_fee=attempt.gas_params.max_fee_per_gas,
                new_max_fee=new_gas_params.max_fee_per_gas,
            )
            metrics = get_metrics()
            metrics.counter(TX_REPLACED).inc(
                chain_id=intent.chain_id,
                job_id=intent.job_id,
            )

            # Refresh attempt from DB
            new_attempt = self._db.get_attempt(new_attempt_id)
            if self._lifecycle and new_attempt is not None:
                self._lifecycle.on_replaced(intent, new_attempt)

            return ReplacementResult(
                success=True,
                new_attempt=new_attempt,
                new_tx_hash=tx_hash,
            )

        except Exception as e:
            error_str = str(e)

            # Check for specific errors
            if "replacement transaction underpriced" in error_str.lower():
                logger.warning(
                    "replacement.underpriced",
                    intent_id=str(intent.intent_id),
                    error=error_str[:200],
                )
                # Mark as failed, will retry with higher fees
                self._db.update_attempt_status(
                    new_attempt_id,
                    AttemptStatus.FAILED.value,
                    error_code="replacement_underpriced",
                    error_detail=error_str[:500],
                )
                return ReplacementResult(
                    success=False,
                    error="replacement_underpriced",
                )

            logger.error(
                "replacement.broadcast_failed",
                intent_id=str(intent.intent_id),
                error=error_str[:200],
            )

            self._db.update_attempt_status(
                new_attempt_id,
                AttemptStatus.FAILED.value,
                error_code="broadcast_failed",
                error_detail=error_str[:500],
            )

            return ReplacementResult(success=False, error=error_str[:200])

    def abandon_intent(self, intent: TxIntent, attempt: TxAttempt, reason: str) -> None:
        """Abandon an intent after max replacement attempts.

        Args:
            intent: Transaction intent
            attempt: Last attempt
            reason: Reason for abandonment
        """
        # Mark intent as abandoned
        transition_intent(
            self._db,
            intent.intent_id,
            IntentStatus.ABANDONED,
            "max_replacements_exceeded",
            chain_id=self._config.chain_id,
        )

        # Release nonce reservation (checksum address for nonce manager)
        signer_address = Web3.to_checksum_address(intent.signer_address)
        self._nonce_manager.release(signer_address, attempt.nonce)

        if self._lifecycle:
            self._lifecycle.on_failed(
                intent,
                attempt,
                RuntimeError(reason),
            )

        logger.warning(
            LogEvents.TX_ABANDONED,
            intent_id=str(intent.intent_id),
            attempt_id=str(attempt.attempt_id),
            nonce=attempt.nonce,
            reason=reason,
        )

    def process_stuck_transactions(self) -> dict[str, int]:
        """Process all stuck transactions and attempt replacement.

        Single pass through pending intents, checking for stuck transactions
        and attempting replacement where appropriate.

        Returns:
            Dict with counts of actions taken
        """
        results = {
            "checked": 0,
            "replaced": 0,
            "abandoned": 0,
            "errors": 0,
        }

        # Get pending intents
        pending_intents = self._db.get_intents_by_status(
            IntentStatus.PENDING.value,
            chain_id=self._config.chain_id,
        )

        for intent in pending_intents:
            attempt = self._db.get_latest_attempt_for_intent(intent.intent_id)
            if not attempt or not attempt.tx_hash:
                continue

            results["checked"] += 1

            try:
                if self.should_replace(intent, attempt):
                    # Check if we've exceeded max replacements
                    replacement_count = self.get_replacement_count(intent.intent_id)
                    if replacement_count >= self._config.max_replacement_attempts:
                        self.abandon_intent(
                            intent,
                            attempt,
                            f"Max replacement attempts ({self._config.max_replacement_attempts}) exceeded",
                        )
                        results["abandoned"] += 1
                        continue

                    # Attempt replacement
                    result = self.replace_transaction(intent, attempt)
                    if result.success:
                        results["replaced"] += 1
                    else:
                        results["errors"] += 1

            except Exception as e:
                logger.error(
                    "replacement.process_failed",
                    intent_id=str(intent.intent_id),
                    error=str(e)[:200],
                )
                results["errors"] += 1

        if results["replaced"] > 0 or results["abandoned"] > 0:
            logger.info(
                "replacement.batch_complete",
                **results,
            )

        return results
