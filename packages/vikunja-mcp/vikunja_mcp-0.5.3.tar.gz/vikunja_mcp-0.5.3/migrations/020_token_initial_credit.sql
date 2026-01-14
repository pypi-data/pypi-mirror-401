-- =============================================================================
-- Migration: Add initial_credit_cents to registration tokens
-- Date: 2025-01-10
-- =============================================================================
-- Adds initial_credit_cents column to registration_tokens to specify how much
-- credit users receive when signing up with a token.
--
-- Run with: psql $DATABASE_URL -f migrations/020_token_initial_credit.sql
-- =============================================================================

BEGIN;

-- Add initial_credit_cents column (default 0 = no automatic credit)
ALTER TABLE registration_tokens
ADD COLUMN IF NOT EXISTS initial_credit_cents INT NOT NULL DEFAULT 0;

-- Add constraint to ensure non-negative values
ALTER TABLE registration_tokens
ADD CONSTRAINT positive_initial_credit CHECK (initial_credit_cents >= 0);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (20, 'Add initial_credit_cents to registration tokens')
ON CONFLICT (version) DO NOTHING;

COMMIT;
