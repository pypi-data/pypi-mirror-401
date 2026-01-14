-- Migration 017: JSON Batch Support for Project Queue
-- Bead: solutions-eofy
-- Date: 2026-01-05
--
-- Add support for batching multiple projects in one queue entry.
-- When LLM creates hierarchical projects (e.g., "Marketing > Campaigns > Q1 2026"),
-- all projects are batched into a single queue entry with projects as JSON array.
--
-- This allows:
-- - Temp IDs for parent references (e.g., parent_project_id: -1)
-- - Frontend resolves temp IDs to real Vikunja project IDs during creation
-- - One trip to processor page handles entire hierarchy

-- Add projects column for batch mode
ALTER TABLE project_creation_queue 
ADD COLUMN IF NOT EXISTS projects JSONB;

-- Make individual columns nullable (either title OR projects must be set)
ALTER TABLE project_creation_queue 
ALTER COLUMN title DROP NOT NULL;

-- Add constraint: either (title) OR (projects) must be set
ALTER TABLE project_creation_queue
ADD CONSTRAINT check_title_or_projects 
CHECK (
    (title IS NOT NULL AND projects IS NULL) OR 
    (title IS NULL AND projects IS NOT NULL)
);

-- Index for JSONB queries (optional, for future analytics)
CREATE INDEX IF NOT EXISTS idx_project_queue_projects 
ON project_creation_queue USING GIN (projects);

