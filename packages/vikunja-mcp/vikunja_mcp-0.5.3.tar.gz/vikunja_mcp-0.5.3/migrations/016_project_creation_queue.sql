-- Migration 016: Project Creation Queue
-- Bead: solutions-eofy
-- Date: 2026-01-05
--
-- Queue system for bot-created projects. Instead of bot creating projects
-- directly (which causes permission issues), bot queues project specs here.
-- User's frontend creates projects using their active session token.

CREATE TABLE IF NOT EXISTS project_creation_queue (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,           -- e.g., "vikunja:ivan"
    username TEXT NOT NULL,           -- e.g., "ivan"
    bot_username TEXT NOT NULL,       -- e.g., "e-a1b2c3"
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    hex_color TEXT DEFAULT '',
    parent_project_id INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status TEXT DEFAULT 'pending'     -- pending, complete, failed
);

CREATE INDEX IF NOT EXISTS idx_project_queue_user 
ON project_creation_queue(username) 
WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_project_queue_status 
ON project_creation_queue(status, created_at);

