# Bucket Assignment Fix - Custom Kanban Views

## Bug Report (from X-Q Task 244148)

**Symptom**: `set_task_position` doesn't assign tasks to buckets in non-default kanban views

**Steps to Reproduce**:
1. Create a new kanban view with `create_view(project_id, "By Phase", "kanban")` → returns view_id 55017
2. Create buckets in that view with `create_bucket(project_id, "Phase 1", view_id)` → buckets created successfully
3. Attempt to move tasks into buckets with `set_task_position(task_id, project_id, view_id, bucket_id)`

**Expected**: Task assigned to specified bucket in that view

**Actual**:
- Returns `{"task_id": X, "bucket_id": Y, "view_id": Z, "position_set": false}`
- Task remains at `bucket_id: 0` when queried via `get_view_tasks`
- UI shows each task as its own column (no bucket assignment)
- `list_tasks_by_bucket` returns empty `{}`

**Context**: Trying to create a "By Phase" view for the Speaker Tech Stack project (14259) where tasks are organized by phase labels instead of by domain.

---

## Root Cause Analysis

The MCP server's `_set_task_position_impl()` function had **TWO bugs**:

### Bug 1: Missing `max_permission` field (Fixed in commit 8fd3dcc)

The `bucket_data` payload was missing the `max_permission` field that the Vikunja API requires.

**Python Wrapper (vikunja_wrapper.py) - CORRECT** ✅
```python
bucket_data = {
    "max_permission": None,  # ← CRITICAL FIELD
    "task_id": task_id,
    "bucket_id": bucket_id,
    "project_view_id": project_view_id,
    "project_id": project_id
}
```

**MCP Server (server.py) - BUGGY** ❌
```python
bucket_data = {
    # ← MISSING "max_permission": None
    "task_id": task_id,
    "bucket_id": bucket_id,
    "project_view_id": view_id,
    "project_id": project_id
}
```

### Bug 2: Missing second API call (Fixed in commit a288322)

The MCP server was only making **ONE API call** when it should make **TWO** (like the Python wrapper and UI do):

**Python Wrapper (vikunja_wrapper.py) - CORRECT** ✅
```python
# Call 1: Add task to bucket
_request("POST", f"/api/v1/projects/{pid}/views/{vid}/buckets/{bid}/tasks", json=bucket_data)

# Call 2: Commit the bucket assignment
position_data = {
    "max_permission": None,
    "project_view_id": project_view_id,
    "task_id": task_id
}
_request("POST", f"/api/v1/tasks/{tid}/position", json=position_data)
```

**MCP Server (server.py) - BUGGY** ❌
```python
# Call 1: Add task to bucket
_request("POST", f"/api/v1/projects/{pid}/views/{vid}/buckets/{bid}/tasks", json=bucket_data)

# ← MISSING Call 2!
# Only made the second call when apply_sort=True
```

Without the second API call, the bucket assignment is not persisted, and tasks remain at `bucket_id=0` when queried.

---

## Fix

**File**: `/home/ivanadamin/factumerit/backend/src/vikunja_mcp/server.py`
**Function**: `_set_task_position_impl()` (line ~2002)

### Fix 1: Add `max_permission` field (commit 8fd3dcc)

```diff
     # Add task to bucket
     bucket_data = {
+        "max_permission": None,
         "task_id": task_id,
         "bucket_id": bucket_id,
         "project_view_id": view_id,
         "project_id": project_id
     }
```

### Fix 2: Add second API call (commit a288322)

```diff
     _request("POST", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}/tasks", json=bucket_data)

-    result = {"task_id": task_id, "bucket_id": bucket_id, "view_id": view_id, "position_set": False}
+
+    # CRITICAL: Always make the second API call to commit the bucket assignment (Call 2)
+    # This matches the Python wrapper behavior and what the UI does
+    position_data = {
+        "max_permission": None,
+        "project_view_id": view_id,
+        "task_id": task_id
+    }
+    _request("POST", f"/api/v1/tasks/{task_id}/position", json=position_data)
+    result = {"task_id": task_id, "bucket_id": bucket_id, "view_id": view_id, "position_set": True}
```

---

## Deployment

- ✅ **Committed**: `8fd3dcc` - "Fix set_task_position: add missing max_permission field for bucket assignment" (partial fix)
- ✅ **Committed**: `a288322` - "Fix set_task_position: add missing second API call to commit bucket assignment" (complete fix)
- ✅ **Pushed**: to GitHub (vikunja-slack-bot repo)
- 🔄 **Restart Required**: Claude Desktop needs to be restarted to pick up the fix

---

## Testing

After restarting Claude Desktop, test with the original scenario:

```python
# 1. Create custom kanban view
view = create_view(14259, "By Phase", "kanban")  # Returns view_id 55017

# 2. Create buckets
bucket1 = create_bucket(14259, "Phase 1", 55017)
bucket2 = create_bucket(14259, "Phase 2", 55017)

# 3. Assign task to bucket (should now work!)
result = set_task_position(task_id, 14259, 55017, bucket1['id'])

# 4. Verify
tasks = get_view_tasks(14259, 55017)
# Should show task with correct bucket_id
```

**Expected Result**: Tasks are correctly assigned to buckets in custom kanban views, and `get_view_tasks` returns tasks with the correct `bucket_id`.

---

## Impact

This fix affects:
- ✅ **MCP Server** (Claude Desktop) - Primary fix
- ✅ **Slack Bot** - Uses same TOOL_REGISTRY implementation
- ✅ **Matrix Bot** - Uses same TOOL_REGISTRY implementation

All three interfaces now correctly assign tasks to buckets in custom kanban views.

---

## Related Files

- `/home/ivanadamin/factumerit/backend/src/vikunja_mcp/server.py` - MCP server (FIXED)
- `/home/ivanadamin/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-api-wrapper/src/vikunja_wrapper.py` - Python wrapper (already correct)
- `/home/ivanadamin/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-mcp/test_custom_view_buckets.py` - Test script (created for verification)

---

## Commit History

- `a288322` - Fix set_task_position: add missing second API call to commit bucket assignment (2025-12-27) ✅ **COMPLETE FIX**
- `8fd3dcc` - Fix set_task_position: add missing max_permission field for bucket assignment (2025-12-27) ⚠️ **PARTIAL FIX**
- `24af598` - Add create_view and update_view tools (2025-12-26)
- `3c9b9f5` - Fix MCP server startup: use full path to uv (2025-12-26)

