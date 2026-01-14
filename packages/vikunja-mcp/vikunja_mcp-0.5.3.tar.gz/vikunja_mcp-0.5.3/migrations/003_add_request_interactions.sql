-- Migration: Add request_interactions table for debugging and analytics
-- Date: 2025-12-28
-- Purpose: Track user commands, results, and execution time to debug issues like "0 tasks"

CREATE TABLE IF NOT EXISTS request_interactions (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,                    -- @user:matrix.factumerit.app
    vikunja_instance TEXT NOT NULL,           -- 'default', 'personal', etc.
    command TEXT NOT NULL,                    -- '\!maybe', '\!stats', '\!test'
    request_type TEXT,                        -- 'filter_command', 'llm_query', 'test'
    filter_applied TEXT,                      -- 'no_due_date', 'overdue', etc.
    results_count INTEGER,                    -- How many tasks/projects returned
    success BOOLEAN NOT NULL,
    error_message TEXT,
    response_preview TEXT,                    -- First 200 chars of response
    execution_time_ms INTEGER,                -- How long it took
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for analysis
CREATE INDEX IF NOT EXISTS idx_interactions_user ON request_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_interactions_time ON request_interactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_interactions_command ON request_interactions(command);
CREATE INDEX IF NOT EXISTS idx_interactions_instance ON request_interactions(vikunja_instance);

-- Retention: Keep 30 days, then archive
COMMENT ON TABLE request_interactions IS 'User interaction log for debugging and analytics. Retention: 30 days.';
