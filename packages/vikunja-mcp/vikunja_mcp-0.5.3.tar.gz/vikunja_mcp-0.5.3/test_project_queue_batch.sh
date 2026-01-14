#!/bin/bash
# Integration tests for project queue batching
# Bead: solutions-eofy (User Can Create Project - JSON Batch Support)

set -e

DB_URL="postgresql://factumerit:ZR2gEnBwHaABuyZt1HcjJp92vAUvWEfS@dpg-d54tgckhg0os739oddpg-a.oregon-postgres.render.com/matrix_jfmr"

echo "============================================================"
echo "Project Queue Batch Integration Tests"
echo "Bead: solutions-eofy"
echo "============================================================"

# Test 1: Check schema
echo ""
echo "🔍 Test 1: Database Schema"
echo "-----------------------------------------------------------"

RESULT=$(psql "$DB_URL" -t -c "
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'project_creation_queue' 
    AND column_name = 'projects'
")

if [ -n "$RESULT" ]; then
    echo "✅ Column 'projects' exists: $RESULT"
else
    echo "❌ Column 'projects' not found!"
    exit 1
fi

# Test 2: Insert batch
echo ""
echo "🔍 Test 2: Batch Insert"
echo "-----------------------------------------------------------"

QUEUE_ID=$(psql "$DB_URL" -q -t -A -c "
    INSERT INTO project_creation_queue
    (user_id, username, bot_username, projects, status)
    VALUES (
        'vikunja:test_batch',
        'test_batch',
        'eis-test_batch',
        '[
            {\"temp_id\": -1, \"title\": \"Test Marketing\", \"description\": \"\", \"hex_color\": \"\", \"parent_project_id\": 0},
            {\"temp_id\": -2, \"title\": \"Test Campaigns\", \"description\": \"\", \"hex_color\": \"\", \"parent_project_id\": -1},
            {\"temp_id\": -3, \"title\": \"Test Q1 2026\", \"description\": \"\", \"hex_color\": \"\", \"parent_project_id\": -2}
        ]'::jsonb,
        'pending'
    )
    RETURNING id
")

echo "✅ Inserted batch with queue_id=$QUEUE_ID"

# Verify batch
PROJECTS=$(psql "$DB_URL" -t -A -c "
    SELECT jsonb_array_length(projects)
    FROM project_creation_queue
    WHERE id = $QUEUE_ID
")

echo "✅ Fetched batch: $PROJECTS projects"

if [ "$PROJECTS" = "3" ]; then
    echo "✅ Correct number of projects"
else
    echo "❌ Expected 3 projects, got $PROJECTS"
    exit 1
fi

# Check parent references
PARENT_REF=$(psql "$DB_URL" -t -A -c "
    SELECT projects->1->'parent_project_id'
    FROM project_creation_queue
    WHERE id = $QUEUE_ID
")

if [ "$PARENT_REF" = "-1" ]; then
    echo "✅ Parent references preserved correctly"
else
    echo "❌ Parent reference incorrect: $PARENT_REF"
    exit 1
fi

# Cleanup
psql "$DB_URL" -c "DELETE FROM project_creation_queue WHERE id = $QUEUE_ID" > /dev/null
echo "✅ Cleanup complete"

# Test 3: Single mode compatibility
echo ""
echo "🔍 Test 3: Single Mode Compatibility"
echo "-----------------------------------------------------------"

SINGLE_ID=$(psql "$DB_URL" -q -t -A -c "
    INSERT INTO project_creation_queue
    (user_id, username, bot_username, title, description, hex_color, parent_project_id, status)
    VALUES (
        'vikunja:test_single',
        'test_single',
        'eis-test_single',
        'Test Single Project',
        'Description',
        '#00ff00',
        0,
        'pending'
    )
    RETURNING id
")

echo "✅ Inserted single project with queue_id=$SINGLE_ID"

# Verify single mode
TITLE=$(psql "$DB_URL" -t -A -c "
    SELECT title
    FROM project_creation_queue
    WHERE id = $SINGLE_ID
")

PROJECTS_NULL=$(psql "$DB_URL" -t -A -c "
    SELECT projects IS NULL
    FROM project_creation_queue
    WHERE id = $SINGLE_ID
")

if [ "$TITLE" = "Test Single Project" ] && [ "$PROJECTS_NULL" = "t" ]; then
    echo "✅ Single mode works: title='$TITLE', projects=NULL"
else
    echo "❌ Single mode failed"
    exit 1
fi

# Cleanup
psql "$DB_URL" -c "DELETE FROM project_creation_queue WHERE id = $SINGLE_ID" > /dev/null
echo "✅ Cleanup complete"

# Test 4: Mixed query (both modes)
echo ""
echo "🔍 Test 4: Mixed Query (Single + Batch)"
echo "-----------------------------------------------------------"

# Insert both types
BATCH_ID=$(psql "$DB_URL" -q -t -A -c "
    INSERT INTO project_creation_queue
    (user_id, username, bot_username, projects, status)
    VALUES (
        'vikunja:test_mixed',
        'test_mixed',
        'eis-test_mixed',
        '[{\"temp_id\": -1, \"title\": \"Batch Project\", \"description\": \"\", \"hex_color\": \"\", \"parent_project_id\": 0}]'::jsonb,
        'pending'
    )
    RETURNING id
")

SINGLE_ID2=$(psql "$DB_URL" -q -t -A -c "
    INSERT INTO project_creation_queue
    (user_id, username, bot_username, title, status)
    VALUES (
        'vikunja:test_mixed',
        'test_mixed',
        'eis-test_mixed',
        'Single Project',
        'pending'
    )
    RETURNING id
")

# Query both
COUNT=$(psql "$DB_URL" -t -A -c "
    SELECT COUNT(*)
    FROM project_creation_queue
    WHERE username = 'test_mixed' AND status = 'pending'
")

if [ "$COUNT" = "2" ]; then
    echo "✅ Mixed query works: found $COUNT entries"
else
    echo "❌ Expected 2 entries, got $COUNT"
    exit 1
fi

# Cleanup
psql "$DB_URL" -c "DELETE FROM project_creation_queue WHERE username = 'test_mixed'" > /dev/null
echo "✅ Cleanup complete"

echo ""
echo "============================================================"
echo "🎉 All tests passed!"
echo "============================================================"

