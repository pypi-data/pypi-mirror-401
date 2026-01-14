-- Migration 011: Add service tracking to factumerit_users
-- 
-- Purpose: Track which users need bot service to avoid unnecessary bot initialization
-- 
-- Bead: solutions-skqu
-- Date: 2026-01-05

-- Add service tracking columns to factumerit_users
ALTER TABLE factumerit_users 
ADD COLUMN IF NOT EXISTS service_needed BOOLEAN DEFAULT FALSE;

ALTER TABLE factumerit_users 
ADD COLUMN IF NOT EXISTS service_requested_at TIMESTAMPTZ;

ALTER TABLE factumerit_users 
ADD COLUMN IF NOT EXISTS service_last_active TIMESTAMPTZ;

ALTER TABLE factumerit_users 
ADD COLUMN IF NOT EXISTS service_reason TEXT;

-- Create index for efficient querying of users needing service
CREATE INDEX IF NOT EXISTS idx_factumerit_users_service_needed 
ON factumerit_users(service_needed) 
WHERE service_needed = TRUE;

-- Backfill: Set service_needed=true for all existing users initially
-- (Conservative approach - they'll be cleaned up by idle timeout)
UPDATE factumerit_users 
SET service_needed = TRUE, 
    service_reason = 'migration_default',
    service_requested_at = NOW()
WHERE service_needed IS NULL OR service_needed = FALSE;

