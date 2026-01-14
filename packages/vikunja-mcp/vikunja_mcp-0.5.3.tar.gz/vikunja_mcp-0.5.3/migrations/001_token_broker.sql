-- =============================================================================
-- Migration: Token Broker Tables
-- Date: 2025-12-28
-- Bead: solutions-kik7
-- =============================================================================
-- This migration creates the tables for secure token storage with encryption,
-- audit logging, and multi-instance support.
--
-- Run with: psql $DATABASE_URL -f migrations/001_token_broker.sql
-- =============================================================================

BEGIN;

-- User tokens (encrypted at rest)
-- Composite key supports multiple Vikunja instances per user
CREATE TABLE IF NOT EXISTS user_tokens (
    user_id TEXT NOT NULL,              -- @user:matrix.factumerit.app or Slack user ID
    vikunja_instance TEXT NOT NULL DEFAULT 'default', -- Multi-instance support
    encrypted_token BYTEA NOT NULL,     -- Fernet-encrypted Vikunja token
    encryption_version INTEGER DEFAULT 1, -- For key rotation
    expires_at TIMESTAMPTZ NOT NULL,    -- When token expires (from Vikunja)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed_at TIMESTAMPTZ,
    access_count INTEGER DEFAULT 0,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMPTZ,
    revoked_reason TEXT,
    PRIMARY KEY (user_id, vikunja_instance)
);

-- Index for common query pattern (get_user_token lookup)
CREATE INDEX IF NOT EXISTS idx_user_tokens_active ON user_tokens (user_id, vikunja_instance)
    WHERE revoked = FALSE;

-- Index for lookup with revoked check
CREATE INDEX IF NOT EXISTS idx_user_tokens_lookup ON user_tokens (user_id, revoked);

-- Index for expiration queries (background job)
CREATE INDEX IF NOT EXISTS idx_user_tokens_expiring ON user_tokens (expires_at)
    WHERE revoked = FALSE;

-- Comprehensive audit log
CREATE TABLE IF NOT EXISTS token_access_log (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    action TEXT NOT NULL,               -- 'get', 'set', 'revoke', 'migrate'
    purpose TEXT,                       -- '!stats command', 'OAuth callback', etc.
    caller_module TEXT,                 -- 'matrix_handlers', 'slack_handler'
    caller_function TEXT,               -- '_handle_stats', 'vikunja_callback'
    success BOOLEAN NOT NULL,
    error_message TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for audit log analysis
CREATE INDEX IF NOT EXISTS idx_token_access_user ON token_access_log (user_id);
CREATE INDEX IF NOT EXISTS idx_token_access_time ON token_access_log (timestamp);
CREATE INDEX IF NOT EXISTS idx_token_access_action ON token_access_log (action);

-- System tokens (for admin operations)
CREATE TABLE IF NOT EXISTS system_tokens (
    name TEXT PRIMARY KEY,              -- 'waiting_list', 'admin'
    encrypted_token BYTEA NOT NULL,
    purpose TEXT NOT NULL,              -- Why this token exists
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Migration tracking
CREATE TABLE IF NOT EXISTS token_broker_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    description TEXT
);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (1, 'Initial token broker tables')
ON CONFLICT (version) DO NOTHING;

COMMIT;

-- =============================================================================
-- Verification queries (run after migration)
-- =============================================================================
-- \dt user_tokens
-- \dt token_access_log
-- \dt system_tokens
-- SELECT * FROM token_broker_migrations;
