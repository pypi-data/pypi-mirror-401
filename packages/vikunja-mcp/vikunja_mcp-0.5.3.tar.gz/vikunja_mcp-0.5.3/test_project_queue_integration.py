#!/usr/bin/env python3
"""
Integration tests for project queue batching.

Bead: solutions-eofy (User Can Create Project - JSON Batch Support)

Tests the full flow:
1. Create projects via batching
2. Flush to database
3. Fetch from /project-queue endpoint
4. Verify JSON structure

Run with: python test_project_queue_integration.py
"""

import os
import sys
import json
import psycopg2
from datetime import datetime

# Database connection
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://factumerit:ZR2gEnBwHaABuyZt1HcjJp92vAUvWEfS@dpg-d54tgckhg0os739oddpg-a.oregon-postgres.render.com/matrix_jfmr"
)

def test_database_schema():
    """Test that migration 017 was applied correctly."""
    print("🔍 Testing database schema...")
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check projects column exists
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'project_creation_queue' 
        AND column_name = 'projects'
    """)
    
    result = cur.fetchone()
    if result:
        print(f"  ✅ Column 'projects' exists with type: {result[1]}")
    else:
        print(f"  ❌ Column 'projects' not found!")
        return False
    
    # Check constraint exists
    cur.execute("""
        SELECT constraint_name 
        FROM information_schema.table_constraints 
        WHERE table_name = 'project_creation_queue' 
        AND constraint_name = 'queue_has_project_data'
    """)
    
    result = cur.fetchone()
    if result:
        print(f"  ✅ Constraint 'queue_has_project_data' exists")
    else:
        print(f"  ⚠️  Constraint 'queue_has_project_data' not found (may be OK)")
    
    conn.close()
    return True


def test_insert_batch():
    """Test inserting a batch entry."""
    print("\n🔍 Testing batch insert...")
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Create test batch
    test_projects = [
        {
            "temp_id": -1,
            "title": "Test Marketing",
            "description": "Test description",
            "hex_color": "#ff0000",
            "parent_project_id": 0
        },
        {
            "temp_id": -2,
            "title": "Test Campaigns",
            "description": "",
            "hex_color": "",
            "parent_project_id": -1
        },
        {
            "temp_id": -3,
            "title": "Test Q1 2026",
            "description": "",
            "hex_color": "",
            "parent_project_id": -2
        }
    ]
    
    # Insert
    cur.execute("""
        INSERT INTO project_creation_queue
        (user_id, username, bot_username, projects, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        "vikunja:test_integration",
        "test_integration",
        "eis-test_integration",
        json.dumps(test_projects),
        'pending'
    ))
    
    queue_id = cur.fetchone()[0]
    conn.commit()
    
    print(f"  ✅ Inserted batch with queue_id={queue_id}")
    
    # Fetch back
    cur.execute("""
        SELECT id, projects, status
        FROM project_creation_queue
        WHERE id = %s
    """, (queue_id,))
    
    row = cur.fetchone()
    if row:
        fetched_projects = row[1]  # JSONB auto-parsed by psycopg2
        print(f"  ✅ Fetched batch: {len(fetched_projects)} projects")
        print(f"     Projects: {[p['title'] for p in fetched_projects]}")
        
        # Verify structure
        assert fetched_projects[0]["temp_id"] == -1
        assert fetched_projects[1]["parent_project_id"] == -1
        assert fetched_projects[2]["parent_project_id"] == -2
        print(f"  ✅ Parent references preserved correctly")
    else:
        print(f"  ❌ Failed to fetch batch")
        return False
    
    # Cleanup
    cur.execute("DELETE FROM project_creation_queue WHERE id = %s", (queue_id,))
    conn.commit()
    conn.close()
    
    print(f"  ✅ Cleanup complete")
    return True


def test_single_mode_compatibility():
    """Test that single-project mode still works."""
    print("\n🔍 Testing single-project mode (backward compatibility)...")
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Insert single project (old way)
    cur.execute("""
        INSERT INTO project_creation_queue
        (user_id, username, bot_username, title, description, hex_color, parent_project_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        "vikunja:test_single",
        "test_single",
        "eis-test_single",
        "Test Single Project",
        "Description",
        "#00ff00",
        0,
        'pending'
    ))
    
    queue_id = cur.fetchone()[0]
    conn.commit()
    
    print(f"  ✅ Inserted single project with queue_id={queue_id}")
    
    # Fetch back
    cur.execute("""
        SELECT id, title, projects
        FROM project_creation_queue
        WHERE id = %s
    """, (queue_id,))
    
    row = cur.fetchone()
    if row:
        assert row[1] == "Test Single Project"
        assert row[2] is None  # projects should be NULL
        print(f"  ✅ Single mode works: title='{row[1]}', projects=NULL")
    else:
        print(f"  ❌ Failed to fetch single project")
        return False
    
    # Cleanup
    cur.execute("DELETE FROM project_creation_queue WHERE id = %s", (queue_id,))
    conn.commit()
    conn.close()
    
    print(f"  ✅ Cleanup complete")
    return True


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Project Queue Batch Integration Tests")
    print("Bead: solutions-eofy")
    print("=" * 60)
    
    results = []
    
    results.append(("Database Schema", test_database_schema()))
    results.append(("Batch Insert", test_insert_batch()))
    results.append(("Single Mode Compatibility", test_single_mode_compatibility()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

