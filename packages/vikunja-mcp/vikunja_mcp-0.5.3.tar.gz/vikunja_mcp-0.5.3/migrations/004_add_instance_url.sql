-- =============================================================================
-- Migration: Add instance_url to user_tokens
-- Date: 2025-12-29
-- Bead: solutions-mr8f
-- =============================================================================
-- This migration adds the instance_url column to store the Vikunja base URL
-- for each instance, so the bot knows which URL to use for API calls.
--
-- Before: VIKUNJA_URL env var used for all instances (wrong!)
-- After: Each instance has its own URL stored in PostgreSQL
--
-- Run with: psql $DATABASE_URL -f migrations/004_add_instance_url.sql
-- =============================================================================

BEGIN;

-- Add instance_url column
ALTER TABLE user_tokens
ADD COLUMN IF NOT EXISTS instance_url TEXT;

-- Set default URL for existing rows (from VIKUNJA_URL env var)
-- This will be updated when users reconnect with !vik
UPDATE user_tokens
SET instance_url = 'https://vikunja.factumerit.app'
WHERE instance_url IS NULL;

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (4, 'Add instance_url column to user_tokens')
ON CONFLICT (version) DO NOTHING;

COMMIT;

-- =============================================================================
-- Verification queries (run after migration)
-- =============================================================================
-- \d user_tokens
-- SELECT user_id, vikunja_instance, instance_url FROM user_tokens;

