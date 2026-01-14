-- =============================================================================
-- Migration: Add owner_vikunja_user_id to personal_bots
-- Date: 2026-01-04
-- Bead: solutions-xk9l.2
-- =============================================================================
-- Adds owner_vikunja_user_id column to enable bot→user project sharing.
-- When bot creates a project, it needs to know owner's Vikunja user ID to share it.
--
-- Run with: psql $DATABASE_URL -f migrations/013_personal_bots_owner_id.sql
-- =============================================================================

BEGIN;

-- Add owner_vikunja_user_id column
ALTER TABLE personal_bots
    ADD COLUMN IF NOT EXISTS owner_vikunja_user_id INTEGER;

-- Add index for lookups (when bot needs to find owner)
CREATE INDEX IF NOT EXISTS idx_personal_bots_owner_id
    ON personal_bots (owner_vikunja_user_id);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (13, 'Add owner_vikunja_user_id to personal_bots for project sharing')
ON CONFLICT (version) DO NOTHING;

COMMIT;

