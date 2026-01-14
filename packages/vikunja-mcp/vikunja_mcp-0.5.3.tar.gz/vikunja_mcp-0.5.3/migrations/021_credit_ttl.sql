-- =============================================================================
-- Migration: Credit TTL Expiration
-- Date: 2026-01-10
-- Bead: fa-i5cv
-- =============================================================================
-- Adds promo credit expiration to user_budgets and TTL to registration tokens.
-- Promo credits expire after a configurable TTL from signup.
--
-- Run with: psql $DATABASE_URL -f migrations/021_credit_ttl.sql
-- =============================================================================

BEGIN;

-- Add promo_expires_at to user_budgets
-- NULL = never expires (paid credit or no TTL on token)
ALTER TABLE user_budgets
ADD COLUMN IF NOT EXISTS promo_expires_at TIMESTAMPTZ DEFAULT NULL;

-- Add ttl_days to registration_tokens
-- NULL = no TTL (credit never expires)
-- >0 = promo credit expires N days after signup
ALTER TABLE registration_tokens
ADD COLUMN IF NOT EXISTS ttl_days INTEGER DEFAULT NULL;

-- Index for finding expired promos (cron job)
CREATE INDEX IF NOT EXISTS idx_user_budgets_promo_expires
    ON user_budgets (promo_expires_at)
    WHERE promo_expires_at IS NOT NULL;

-- Comment for clarity
COMMENT ON COLUMN user_budgets.promo_expires_at IS
    'When promo credit expires. NULL = never expires (paid credit).';
COMMENT ON COLUMN registration_tokens.ttl_days IS
    'Days until promo credit expires after signup. NULL = never expires.';

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (21, 'Credit TTL expiration for promo credits')
ON CONFLICT (version) DO NOTHING;

COMMIT;
