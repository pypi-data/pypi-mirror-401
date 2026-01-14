-- Postgres only (SQLite handled in migrator)
ALTER TABLE tx_intents ADD COLUMN IF NOT EXISTS claimed_by VARCHAR(200);

INSERT INTO schema_migrations (version) VALUES ('012')
ON CONFLICT (version) DO NOTHING;
