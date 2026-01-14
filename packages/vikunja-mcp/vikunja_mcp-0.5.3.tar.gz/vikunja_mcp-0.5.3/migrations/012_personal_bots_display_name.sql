-- =============================================================================
-- Migration: Add display_name to personal_bots
-- Date: 2026-01-03
-- Bead: solutions-a92n
-- =============================================================================
-- Adds display_name column for user-facing bot name.
-- Username is system-generated (eis-{random}), display_name is what users see.
--
-- Run with: psql $DATABASE_URL -f migrations/012_personal_bots_display_name.sql
-- =============================================================================

BEGIN;

-- Add display_name column (default to 'eis')
ALTER TABLE personal_bots
    ADD COLUMN IF NOT EXISTS display_name TEXT NOT NULL DEFAULT 'eis';

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (12, 'Add display_name to personal_bots')
ON CONFLICT (version) DO NOTHING;

COMMIT;
