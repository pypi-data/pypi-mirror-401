-- =============================================================================
-- Migration: Token Usage Table
-- Date: 2025-12-29
-- Bead: solutions-8zly.3
-- =============================================================================
-- Tracks who has used which registration tokens.
-- Prevents duplicate signups with same token.
--
-- Run with: psql $DATABASE_URL -f migrations/009_token_usage.sql
-- =============================================================================

BEGIN;

-- Token usage tracking
CREATE TABLE IF NOT EXISTS token_usage (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL REFERENCES registration_tokens(token) ON DELETE CASCADE,
    user_id TEXT NOT NULL,                     -- Email (Vikunja username)
    used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_user_token UNIQUE (token, user_id)  -- Prevent duplicate signups
);

-- Index for token lookups
CREATE INDEX IF NOT EXISTS idx_token_usage_token
    ON token_usage(token);

-- Index for user lookups
CREATE INDEX IF NOT EXISTS idx_token_usage_user_id
    ON token_usage(user_id);

-- Index for time-based queries
CREATE INDEX IF NOT EXISTS idx_token_usage_used_at
    ON token_usage(used_at);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (9, 'Token usage tracking table')
ON CONFLICT (version) DO NOTHING;

COMMIT;
