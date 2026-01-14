-- Migration 018: Add 'processing' status for idempotent queue processing
-- Bead: solutions-eofy.1
-- Date: 2026-01-05
--
-- Problem: Users can refresh the queue processor page and create duplicate projects
-- Solution: Add 'processing' status and atomic claim operation
--
-- Flow:
-- 1. Frontend calls /project-queue/claim (not /project-queue)
-- 2. Backend atomically updates pending -> processing and returns those entries
-- 3. Frontend creates projects
-- 4. Frontend marks as complete (processing -> complete)
-- 5. If frontend crashes, entries stay in 'processing' (can be cleaned up later)

-- Update status column comment to document new value
COMMENT ON COLUMN project_creation_queue.status IS 
'Status: pending (queued by bot), processing (claimed by frontend), complete (projects created), failed (error during creation)';

-- Add index for processing status (for cleanup queries)
CREATE INDEX IF NOT EXISTS idx_project_queue_processing 
ON project_creation_queue(status, created_at) 
WHERE status = 'processing';

