-- =============================================================================
-- Migration: Add user_project_context table for per-instance project context
-- Date: 2025-12-28
-- Bead: solutions-lt0f.1
-- =============================================================================
-- This migration creates the user_project_context table to store project context
-- per-instance instead of per-user. This allows users to have different active
-- projects for different Vikunja instances.
--
-- Before: user_preferences.active_project_id (single project across all instances)
-- After: user_project_context.project_id (one project per instance)
--
-- Run with: psql $DATABASE_URL -f migrations/005_user_project_context.sql
-- =============================================================================

BEGIN;

-- Ensure user_preferences table exists (may have been created manually)
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT PRIMARY KEY,
    active_instance TEXT,
    active_project_id INTEGER,
    active_project_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Per-instance project context
-- This replaces the single active_project_id/name in user_preferences
CREATE TABLE IF NOT EXISTS user_project_context (
    user_id TEXT NOT NULL,
    instance_name TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    project_name TEXT,
    set_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, instance_name)
);

-- Index for common query pattern (get project context for user's active instance)
CREATE INDEX IF NOT EXISTS idx_user_project_context_user ON user_project_context (user_id);

-- Migrate existing project context from user_preferences (if any)
-- Maps to the user's active_instance
INSERT INTO user_project_context (user_id, instance_name, project_id, project_name, set_at)
SELECT
    up.user_id,
    COALESCE(up.active_instance, 'default'),
    up.active_project_id,
    up.active_project_name,
    COALESCE(up.updated_at, NOW())
FROM user_preferences up
WHERE up.active_project_id IS NOT NULL
ON CONFLICT (user_id, instance_name) DO NOTHING;

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (5, 'Add user_project_context table for per-instance project context')
ON CONFLICT (version) DO NOTHING;

COMMIT;

-- =============================================================================
-- Verification queries (run after migration)
-- =============================================================================
-- \dt user_project_context
-- SELECT * FROM user_project_context;
-- SELECT * FROM token_broker_migrations ORDER BY version;
