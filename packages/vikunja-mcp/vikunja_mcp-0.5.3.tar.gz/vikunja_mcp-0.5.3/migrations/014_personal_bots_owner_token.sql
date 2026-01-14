-- =============================================================================
-- Migration: Add owner_vikunja_token to personal_bots
-- Date: 2026-01-04
-- Bead: solutions-2x6i (Bot Project Sharing Bug)
-- =============================================================================
-- Adds owner_vikunja_token column to enable bot→user project sharing.
-- Bot API tokens can't see users, but owner's JWT token can.
-- We use owner's token to share bot-created projects with owner.
--
-- Run with: psql $DATABASE_URL -f migrations/014_personal_bots_owner_token.sql
-- =============================================================================

BEGIN;

-- Add owner_vikunja_token column (encrypted like bot credentials)
ALTER TABLE personal_bots
    ADD COLUMN IF NOT EXISTS owner_vikunja_token BYTEA;

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (14, 'Add owner_vikunja_token to personal_bots for project sharing')
ON CONFLICT (version) DO NOTHING;

COMMIT;

