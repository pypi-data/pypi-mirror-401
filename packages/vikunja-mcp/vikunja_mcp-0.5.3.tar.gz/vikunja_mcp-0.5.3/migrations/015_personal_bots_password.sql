-- =============================================================================
-- Migration: Add encrypted_password to personal_bots
-- Date: 2026-01-04
-- Bead: solutions-xk9l (JWT Workaround for Broken API Tokens)
-- =============================================================================
-- Adds encrypted_password column to enable JWT-based bot authentication.
-- API tokens are broken in Vikunja (GitHub issue #105), so we use JWT tokens.
-- Bots login with username/password to get JWT tokens instead of API tokens.
--
-- Run with: psql $DATABASE_URL -f migrations/015_personal_bots_password.sql
-- =============================================================================

BEGIN;

-- Add encrypted_password column (Fernet encrypted like other credentials)
ALTER TABLE personal_bots
    ADD COLUMN IF NOT EXISTS encrypted_password BYTEA;

-- Make encrypted_token nullable (transitioning from API tokens to passwords)
-- Old bots use encrypted_token (API tokens - deprecated)
-- New bots use encrypted_password (for JWT auth)
ALTER TABLE personal_bots
    ALTER COLUMN encrypted_token DROP NOT NULL;

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (15, 'Add encrypted_password to personal_bots for JWT authentication')
ON CONFLICT (version) DO NOTHING;

COMMIT;

