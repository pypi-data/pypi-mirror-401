-- =============================================================================
-- Migration: Users Table (Registration/Authorization)
-- Date: 2025-12-28
-- =============================================================================
-- Creates a proper users table as source of truth for Factumerit registration.
-- Only populated through official OAuth flow, not !vik commands.
--
-- Run with: psql $DATABASE_URL -f migrations/007_users_table.sql
-- =============================================================================

BEGIN;

-- Registered Factumerit users
-- This is the authoritative source for "is this user allowed to use LLM"
-- Named factumerit_users to avoid collision with Matrix Synapse's users table
CREATE TABLE IF NOT EXISTS factumerit_users (
    user_id TEXT PRIMARY KEY,            -- vikunja:<username> or @user:matrix.example.com
    platform TEXT NOT NULL,              -- 'vikunja', 'matrix', or 'slack'
    email TEXT,                          -- Email from OAuth (optional)
    registered_at TIMESTAMPTZ DEFAULT NOW(),
    registered_via TEXT DEFAULT 'oauth', -- 'oauth', 'admin', 'migration'
    is_active BOOLEAN DEFAULT TRUE,      -- Can be deactivated without deleting
    notes TEXT                           -- Admin notes
);

-- Index for active user lookups
CREATE INDEX IF NOT EXISTS idx_factumerit_users_active
    ON factumerit_users (user_id) WHERE is_active = TRUE;

-- Index for platform filtering
CREATE INDEX IF NOT EXISTS idx_factumerit_users_platform
    ON factumerit_users (platform);

-- Migrate ALL existing users from user_tokens
-- Anyone with a token is a legacy user (before this users table existed)
INSERT INTO factumerit_users (user_id, platform, registered_at, registered_via)
SELECT
    user_id,
    CASE WHEN user_id LIKE '@%:%' THEN 'matrix' ELSE 'slack' END,
    MIN(created_at),
    'migration'
FROM user_tokens
WHERE revoked = FALSE
GROUP BY user_id
ON CONFLICT (user_id) DO NOTHING;

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (7, 'Users table for registration/authorization')
ON CONFLICT (version) DO NOTHING;

COMMIT;
