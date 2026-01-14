#!/usr/bin/env python3
"""
Test bucket assignment in custom kanban views vs default kanban view.

Bug report: set_task_position doesn't assign tasks to buckets in non-default kanban views
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../factumerit/backend/src'))

from vikunja_mcp.server import (
    _connect_instance_impl,
    _create_view_impl,
    _create_bucket_impl,
    _create_task_impl,
    _set_task_position_impl,
    _get_view_tasks_impl,
    _list_buckets_impl,
    _get_task_impl
)

# Get credentials
business_url = os.getenv('VIKUNJA_BUSINESS_URL')
business_token = os.getenv('VIKUNJA_BUSINESS_TOKEN')

if not business_url or not business_token:
    print("❌ Missing VIKUNJA_BUSINESS_URL or VIKUNJA_BUSINESS_TOKEN")
    sys.exit(1)

# Connect
print("Connecting to business instance...")
_connect_instance_impl("business", business_url, business_token)
print("✅ Connected\n")

# Test project (Speaker Tech Stack)
project_id = 14259

print("=" * 80)
print("TEST: Bucket Assignment in Custom Kanban View")
print("=" * 80)

# Step 1: Create a custom kanban view
print("\nStep 1: Create custom kanban view 'Test View'...")
view = _create_view_impl(project_id, "Test View", "kanban")
view_id = view['id']
print(f"✅ Created view ID: {view_id}")

# Step 2: Create buckets in that view
print("\nStep 2: Create buckets...")
bucket1 = _create_bucket_impl(project_id, "Test Bucket 1", view_id)
bucket2 = _create_bucket_impl(project_id, "Test Bucket 2", view_id)
print(f"✅ Created bucket 1: ID {bucket1['id']}")
print(f"✅ Created bucket 2: ID {bucket2['id']}")

# Step 3: Create a test task
print("\nStep 3: Create test task...")
task = _create_task_impl(project_id, "Test Task for Custom View")
task_id = task['id']
print(f"✅ Created task ID: {task_id}")

# Step 4: Assign task to bucket 1
print(f"\nStep 4: Assign task to bucket 1 (ID {bucket1['id']})...")
result = _set_task_position_impl(
    task_id=task_id,
    project_id=project_id,
    view_id=view_id,
    bucket_id=bucket1['id'],
    apply_sort=False
)
print(f"Result: {result}")

# Step 5: Verify assignment
print("\nStep 5: Verify assignment...")

# Check via get_task
task_check = _get_task_impl(task_id)
print(f"Task bucket_id field: {task_check.get('bucket_id')}")

# Check via get_view_tasks
view_tasks = _get_view_tasks_impl(project_id, view_id)
print(f"\nTasks in view {view_id}:")
for t in view_tasks:
    if t['id'] == task_id:
        print(f"  ✅ Found task {task_id}: bucket_id={t.get('bucket_id')}")
        break
else:
    print(f"  ❌ Task {task_id} not found in view tasks")

# Check via list_buckets (which includes task counts)
buckets = _list_buckets_impl(project_id, view_id)
print(f"\nBuckets in view {view_id}:")
for b in buckets:
    print(f"  - {b['title']} (ID {b['id']}): {b.get('count', 0)} tasks")

print("\n" + "=" * 80)
print("ANALYSIS")
print("=" * 80)

if task_check.get('bucket_id') == bucket1['id']:
    print("✅ SUCCESS: Task correctly assigned to bucket!")
elif task_check.get('bucket_id') == 0:
    print("❌ BUG CONFIRMED: Task has bucket_id=0 (not assigned)")
else:
    print(f"⚠️  UNEXPECTED: Task has bucket_id={task_check.get('bucket_id')}")

print("\nCleanup: Please manually delete the 'Test View' and test task from Vikunja UI")
print(f"  - View ID: {view_id}")
print(f"  - Task ID: {task_id}")

