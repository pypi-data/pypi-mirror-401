-- =============================================================================
-- Migration: Registration Tokens Table
-- Date: 2025-12-29
-- Bead: solutions-8zly.2
-- =============================================================================
-- Creates the registration_tokens table for gated beta access.
-- Tokens like NSA-NORTHWEST-50 control who can sign up.
--
-- Run with: psql $DATABASE_URL -f migrations/008_registration_tokens.sql
-- =============================================================================

BEGIN;

-- Registration tokens for controlled beta access
CREATE TABLE IF NOT EXISTS registration_tokens (
    token TEXT PRIMARY KEY,                    -- e.g., NSA-NORTHWEST-50
    group_id INT,                              -- NULL for Phase 1 (future: REFERENCES groups(id))
    state TEXT NOT NULL DEFAULT 'active',      -- active, exhausted, expired, revoked
    max_uses INT NOT NULL,                     -- e.g., 50
    uses_remaining INT NOT NULL,               -- Decrements on each signup
    expires_at TIMESTAMPTZ,                    -- Optional expiration date
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by TEXT,                           -- Admin user_id who created token
    notes TEXT,                                -- e.g., "NSA Northwest beta cohort"

    CONSTRAINT valid_state CHECK (state IN ('active', 'exhausted', 'expired', 'revoked')),
    CONSTRAINT positive_uses CHECK (max_uses > 0 AND uses_remaining >= 0)
);

-- Index for filtering by state
CREATE INDEX IF NOT EXISTS idx_registration_tokens_state
    ON registration_tokens(state);

-- Index for expiration queries
CREATE INDEX IF NOT EXISTS idx_registration_tokens_expires_at
    ON registration_tokens(expires_at)
    WHERE expires_at IS NOT NULL;

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (8, 'Registration tokens table for gated beta access')
ON CONFLICT (version) DO NOTHING;

COMMIT;
