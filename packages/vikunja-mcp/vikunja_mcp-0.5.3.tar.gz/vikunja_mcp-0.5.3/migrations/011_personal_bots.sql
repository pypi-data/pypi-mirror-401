-- =============================================================================
-- Migration: Personal Bots Table
-- Date: 2026-01-03
-- Bead: solutions-xk9l.1
-- =============================================================================
-- Creates storage for personal bot credentials.
-- Each user gets their own @eis-{username} bot for isolation.
--
-- Run with: psql $DATABASE_URL -f migrations/011_personal_bots.sql
-- =============================================================================

BEGIN;

-- Personal bot credentials
-- One row per user, stores their personal bot's encrypted API token
CREATE TABLE IF NOT EXISTS personal_bots (
    user_id TEXT PRIMARY KEY,              -- References factumerit_users.user_id
    bot_username TEXT NOT NULL UNIQUE,     -- @eis-{username}
    vikunja_user_id INTEGER NOT NULL,      -- Bot's Vikunja user ID (for shares)
    encrypted_token BYTEA NOT NULL,        -- Bot's API token (Fernet encrypted)
    vikunja_instance TEXT NOT NULL DEFAULT 'default',  -- Multi-instance support
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,

    -- Foreign key to registered users
    CONSTRAINT fk_personal_bots_user
        FOREIGN KEY (user_id)
        REFERENCES factumerit_users(user_id)
        ON DELETE CASCADE
);

-- Index for bot username lookups (when polling notifications)
CREATE INDEX IF NOT EXISTS idx_personal_bots_username
    ON personal_bots (bot_username);

-- Index for instance filtering (multi-bot polling)
CREATE INDEX IF NOT EXISTS idx_personal_bots_instance
    ON personal_bots (vikunja_instance);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (11, 'Personal bots table for user isolation')
ON CONFLICT (version) DO NOTHING;

COMMIT;
