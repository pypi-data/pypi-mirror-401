-- =============================================================================
-- Migration: Pending Connections (OAuth Nonces)
-- Date: 2025-12-28
-- Bead: solutions-fp44
-- =============================================================================
-- Moves OAuth pending connections from YAML file to PostgreSQL.
-- This fixes the issue where pending connections are lost on Render deploys
-- (ephemeral filesystem wipes the YAML file).
--
-- Run with: psql $DATABASE_URL -f migrations/006_pending_connections.sql
-- =============================================================================

BEGIN;

-- Pending OAuth connections (nonces)
-- These are short-lived (5-15 min) entries that map OAuth state to user ID
CREATE TABLE IF NOT EXISTS pending_connections (
    nonce TEXT PRIMARY KEY,              -- Cryptographically secure random string
    user_id TEXT NOT NULL,               -- @user:matrix.example.com or Slack user ID
    platform TEXT NOT NULL DEFAULT 'slack', -- 'slack' or 'matrix'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL      -- When this nonce expires (5-15 min)
);

-- Index for cleanup job (delete expired entries)
CREATE INDEX IF NOT EXISTS idx_pending_connections_expires
    ON pending_connections (expires_at);

-- Index for user lookup (optional, for debugging)
CREATE INDEX IF NOT EXISTS idx_pending_connections_user
    ON pending_connections (user_id);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (6, 'Pending connections table for OAuth nonces')
ON CONFLICT (version) DO NOTHING;

COMMIT;

-- =============================================================================
-- Verification queries (run after migration)
-- =============================================================================
-- \dt pending_connections
-- SELECT * FROM token_broker_migrations WHERE version = 6;
