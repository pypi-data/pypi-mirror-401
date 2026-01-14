-- brawny transactions table migration
-- Version: 008
-- Description: Add single Transaction model replacing TxIntent + TxAttempt
--
-- This is Phase 1 of the ATTEMPT_MODEL.md simplification:
-- - Single transactions table (no joins)
-- - 4-state TxStatus (created, broadcast, confirmed, failed)
-- - JSON blobs for rarely-queried fields
-- - Append-only tx_hash_history for debugging

-- ============================================================================
-- Transactions - single model for job transaction lifecycle
-- ============================================================================
CREATE TABLE IF NOT EXISTS transactions (
    -- Identity (queryable, indexed)
    tx_id UUID PRIMARY KEY,
    job_id VARCHAR(200) NOT NULL,
    chain_id INTEGER NOT NULL,
    idempotency_key VARCHAR(200) NOT NULL,

    -- Payload (immutable after creation)
    signer_address VARCHAR(42) NOT NULL,
    to_address VARCHAR(42) NOT NULL,
    data TEXT,
    value_wei VARCHAR(78) NOT NULL DEFAULT '0',
    min_confirmations INTEGER NOT NULL DEFAULT 1,
    deadline_ts TIMESTAMP,

    -- Status (queryable)
    status VARCHAR(20) NOT NULL DEFAULT 'created'
        CHECK (status IN ('created', 'broadcast', 'confirmed', 'failed')),
    failure_type VARCHAR(50),

    -- Broadcast state (queryable)
    current_tx_hash VARCHAR(66),
    current_nonce BIGINT,
    replacement_count INTEGER NOT NULL DEFAULT 0,

    -- Worker coordination (queryable)
    claim_token VARCHAR(100),
    claimed_at TIMESTAMP,

    -- Confirmation (queryable)
    included_block BIGINT,
    confirmed_at TIMESTAMP,

    -- Audit (queryable)
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- JSON BLOBS (rarely queried - no indexes)
    gas_params_json TEXT,           -- {"gas_limit": N, "max_fee": N, "priority_fee": N}
    broadcast_info_json TEXT,       -- {"group": str, "endpoints": [...]}
    error_info_json TEXT,           -- ErrorInfo as JSON
    tx_hash_history TEXT            -- Append-only JSON array of TxHashRecord
);

-- Indexes (only on queryable columns)
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_job_status ON transactions(job_id, status);
CREATE INDEX IF NOT EXISTS idx_transactions_signer ON transactions(chain_id, signer_address);
CREATE INDEX IF NOT EXISTS idx_transactions_tx_hash ON transactions(current_tx_hash) WHERE current_tx_hash IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_transactions_created ON transactions(created_at);

-- Idempotency is scoped to (chain_id, signer_address)
CREATE UNIQUE INDEX IF NOT EXISTS uq_transactions_idempotency_scoped
    ON transactions(chain_id, signer_address, idempotency_key);

-- ============================================================================
-- Record this migration
-- ============================================================================
INSERT INTO schema_migrations (version) VALUES ('008');
