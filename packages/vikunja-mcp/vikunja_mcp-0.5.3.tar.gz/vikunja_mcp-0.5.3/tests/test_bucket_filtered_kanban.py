#\!/usr/bin/env python3
"""
TDD test for bucket-filtered kanban views.

Test Requirements:
1. Create a kanban view with bucket_configuration_mode = "filter"
2. Create buckets with filter queries
3. Verify tasks matching filters appear in correct buckets
4. Verify bucket counts are correct
"""
import requests
import yaml
import json

# Read config
with open('/home/ivanadamin/.vikunja-mcp/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

token = config['instances']['business']['token']
base_url = config['instances']['business']['url']
headers = {"Authorization": f"Bearer {token}"}

project_id = 14259

print("=" * 80)
print("TEST: Bucket-Filtered Kanban View")
print("=" * 80)

# Setup: Get label IDs and count tasks with those labels
print("\n1. SETUP: Count tasks with test labels...")
r = requests.get(f"{base_url}/api/v1/projects/{project_id}/tasks", headers=headers)
all_tasks = r.json()

label_7344_tasks = [t for t in all_tasks if any(l['id'] == 7344 for l in (t.get('labels') or []))]
label_7345_tasks = [t for t in all_tasks if any(l['id'] == 7345 for l in (t.get('labels') or []))]

print(f"   Tasks with label 7344 (⚡ Quick Win): {len(label_7344_tasks)}")
print(f"   Tasks with label 7345 (🧠 Deep Work): {len(label_7345_tasks)}")

if len(label_7344_tasks) == 0 or len(label_7345_tasks) == 0:
    print("   ❌ SETUP FAILED: Need tasks with both labels to test")
    exit(1)

print("   ✅ Setup complete")

# Test 1: Create view with filter mode
print("\n2. TEST: Create kanban view with bucket_configuration_mode='filter'...")
r = requests.put(
    f"{base_url}/api/v1/projects/{project_id}/views",
    headers={**headers, "Content-Type": "application/json"},
    json={
        "title": "TEST Bucket Filtered Kanban",
        "view_kind": "kanban",
        "bucket_configuration_mode": "filter"
    }
)

assert r.status_code in [200, 201], f"Failed to create view: {r.status_code} - {r.text}"
view = r.json()
view_id = view['id']
assert view['bucket_configuration_mode'] == 'filter', "bucket_configuration_mode not set to 'filter'"
print(f"   ✅ Created view {view_id} with filter mode")

# Test 2: Create bucket with filter for label 7344
print("\n3. TEST: Create bucket with filter 'labels in 7344'...")
r = requests.put(
    f"{base_url}/api/v1/projects/{project_id}/views/{view_id}/buckets",
    headers={**headers, "Content-Type": "application/json"},
    json={
        "title": "⚡ Quick Wins",
        "filter": "labels in 7344",
        "position": 100
    }
)

assert r.status_code in [200, 201], f"Failed to create bucket: {r.status_code} - {r.text}"
bucket1 = r.json()
bucket1_id = bucket1['id']
print(f"   ✅ Created bucket {bucket1_id}")

# Test 3: Create bucket with filter for label 7345
print("\n4. TEST: Create bucket with filter 'labels in 7345'...")
r = requests.put(
    f"{base_url}/api/v1/projects/{project_id}/views/{view_id}/buckets",
    headers={**headers, "Content-Type": "application/json"},
    json={
        "title": "🧠 Deep Work",
        "filter": "labels in 7345",
        "position": 200
    }
)

assert r.status_code in [200, 201], f"Failed to create bucket: {r.status_code} - {r.text}"
bucket2 = r.json()
bucket2_id = bucket2['id']
print(f"   ✅ Created bucket {bucket2_id}")

# Test 4: Verify buckets exist
print("\n5. TEST: List buckets and verify filters are stored...")
r = requests.get(
    f"{base_url}/api/v1/projects/{project_id}/views/{view_id}/buckets",
    headers=headers
)

assert r.status_code == 200, f"Failed to list buckets: {r.status_code}"
buckets = r.json()
assert len(buckets) == 2, f"Expected 2 buckets, got {len(buckets)}"

print(f"   Found {len(buckets)} buckets:")
for b in buckets:
    filter_field = b.get('filter', 'NOT PRESENT')
    print(f"     - {b['title']}: filter={filter_field}")

# Test 5: Get tasks in the view
print("\n6. TEST: Get tasks in view and verify they appear in buckets...")
r = requests.get(
    f"{base_url}/api/v1/projects/{project_id}/views/{view_id}/tasks",
    headers=headers
)

assert r.status_code == 200, f"Failed to get tasks: {r.status_code}"
view_tasks = r.json()

print(f"   Tasks in view: {len(view_tasks)}")
print(f"   Expected: {len(label_7344_tasks) + len(label_7345_tasks)} (sum of both labels)")

if len(view_tasks) == 0:
    print("   ❌ FAILED: No tasks in view\!")
    print("\n   Debugging info:")
    print(f"   - View ID: {view_id}")
    print(f"   - Bucket 1 ID: {bucket1_id}")
    print(f"   - Bucket 2 ID: {bucket2_id}")
    print(f"   - Buckets response: {json.dumps(buckets, indent=2)}")
else:
    # Count tasks by bucket
    bucket1_count = len([t for t in view_tasks if t.get('bucket_id') == bucket1_id])
    bucket2_count = len([t for t in view_tasks if t.get('bucket_id') == bucket2_id])
    
    print(f"   Tasks in bucket 1 (Quick Wins): {bucket1_count} (expected: {len(label_7344_tasks)})")
    print(f"   Tasks in bucket 2 (Deep Work): {bucket2_count} (expected: {len(label_7345_tasks)})")
    
    if bucket1_count == len(label_7344_tasks) and bucket2_count == len(label_7345_tasks):
        print("   ✅ PASSED: Tasks correctly filtered into buckets\!")
    else:
        print("   ❌ FAILED: Task counts don't match expected")

# Cleanup
print("\n7. CLEANUP: Delete test view...")
r = requests.delete(
    f"{base_url}/api/v1/projects/{project_id}/views/{view_id}",
    headers=headers
)
assert r.status_code == 200, f"Failed to delete view: {r.status_code}"
print(f"   ✅ Deleted view {view_id}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)

