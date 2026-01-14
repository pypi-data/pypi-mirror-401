# Test Plan: Queue-Based Project Creation (Bot Mode Only)

**Bead**: solutions-eofy
**Deployed**: 2026-01-05
**Status**: ✅ Code pushed (commit 91f7edd)

---

## Architecture Overview

**Two Code Paths**:
1. **MCP Mode** (`_bot_mode=False`): Claude Desktop → Direct creation (unchanged)
2. **Bot Mode** (`_bot_mode=True`): Vikunja EARS → Queue system (new)

**Routing**: `_create_project_impl()` checks `_bot_mode` context variable

---

## Pre-Test: Deployment Check

1. **Render Deploy Status**: https://dashboard.render.com
   - Wait for "Deploy succeeded" (~2-3 min)

2. **Verify Migrations**:
   ```bash
   psql "$DATABASE_URL" -c "\d project_creation_queue"
   ```
   Expected: Table exists with `projects` JSONB column

---

## Part 1: MCP Regression Tests (Ensure No Breakage)

### Test 1.1: MCP Single Project (Direct Creation)

**Method**: Claude Desktop MCP
**Command**: `"create project MCP Test Single"`

**Expected**:
- ✅ Project created immediately (no queue)
- ✅ Response includes project ID
- ✅ NO processor link in response
- ✅ Project visible in Vikunja immediately

**Verification**:
```sql
-- Should return 0 rows (MCP doesn't use queue)
SELECT * FROM project_creation_queue
WHERE created_at > NOW() - INTERVAL '5 minutes';
```

**Pass/Fail**: ___________

---

### Test 1.2: MCP Hierarchical Projects (Direct Creation)

**Method**: Claude Desktop MCP
**Command**: `"create project Work with subproject Projects"`

**Expected**:
- ✅ Both projects created immediately
- ✅ Parent-child relationship correct
- ✅ NO queue entries
- ✅ Works exactly as before

**Verification**:
- Check Vikunja: Work → Projects hierarchy exists
- Check database: 0 queue entries

**Pass/Fail**: ___________

---

### Test 1.3: MCP List Projects (Existing Functionality)

**Method**: Claude Desktop MCP
**Command**: `"list all my projects"`

**Expected**:
- ✅ Returns project list
- ✅ Includes projects from Test 1.1 and 1.2
- ✅ No errors

**Pass/Fail**: ___________

---

### Test 1.4: MCP Create Task (Existing Functionality)

**Method**: Claude Desktop MCP
**Command**: `"create task 'Test task' in project 'MCP Test Single'"`

**Expected**:
- ✅ Task created successfully
- ✅ No queue involvement
- ✅ Works as before

**Pass/Fail**: ___________

---

## Part 2: Bot Mode Queue Tests (New Functionality)

### Test 2.1: Bot Single Project (Queue)

**Method**: Vikunja EARS (@mention)
**Steps**:
1. Go to Vikunja, open any task
2. Add comment: `@bot create project Bot Test Single`
3. Wait for bot response

**Expected Bot Response**:
```
✅ 1 project queued

Visit this link to create it:
https://mcp.factumerit.app/project-queue-processor

(You'll need to be logged into Vikunja)
```

**Verification Before Clicking Link**:
```sql
-- Should show 1 pending entry
SELECT username, projects, status
FROM project_creation_queue
WHERE status = 'pending'
ORDER BY created_at DESC LIMIT 1;
```

**Action**:
4. Click processor link
5. Verify frontend creates project
6. Verify redirect to Vikunja

**Verification After**:
- ✅ Project "Bot Test Single" exists in Vikunja
- ✅ You own it
- ✅ Bot has write access
- ✅ Queue entry marked complete:
  ```sql
  SELECT status, completed_at
  FROM project_creation_queue
  ORDER BY created_at DESC LIMIT 1;
  ```

**Pass/Fail**: ___________

---

### Test 2.2: Bot Hierarchical Projects (Queue with Temp IDs)

**Method**: Vikunja EARS (@mention)
**Command**: `@bot create Marketing > Campaigns > Q1 2026`

**Expected Bot Response**:
```
✅ 3 projects queued

Visit this link to create them:
https://mcp.factumerit.app/project-queue-processor
```

**Verification Before Clicking**:
```sql
-- Should show JSONB array with 3 projects
SELECT
    username,
    jsonb_array_length(projects) as count,
    projects
FROM project_creation_queue
WHERE status = 'pending'
ORDER BY created_at DESC LIMIT 1;
```

**Expected JSONB Structure**:
```json
[
  {"temp_id": -1, "title": "Marketing", "parent_project_id": 0},
  {"temp_id": -2, "title": "Campaigns", "parent_project_id": -1},
  {"temp_id": -3, "title": "Q1 2026", "parent_project_id": -2}
]
```

**Action**: Click processor link

**Expected Result**:
```
Marketing
└── Campaigns
    └── Q1 2026
```

**Verification**:
- ✅ All 3 projects exist
- ✅ Hierarchy correct (Q1 2026 parent is Campaigns, Campaigns parent is Marketing)
- ✅ You own all 3
- ✅ Bot has access to all 3
- ✅ Queue marked complete

**Pass/Fail**: ___________

---

## Part 3: Edge Cases

### Test 3.1: Empty Queue (Frontend Handling)

**Method**: Direct browser visit
**Action**: Visit https://mcp.factumerit.app/project-queue-processor (when no projects queued)

**Expected**:
- ✅ Message: "No pending projects to create"
- ✅ Redirect to Vikunja after 2 seconds

**Pass/Fail**: ___________

---

### Test 3.2: Not Logged Into Vikunja

**Method**: Logout, then visit processor
**Action**:
1. Logout of Vikunja
2. Visit processor link

**Expected**:
- ✅ Error: "Please log into Vikunja first"
- ✅ Redirect to Vikunja login

**Pass/Fail**: ___________

---

## Summary: Success Criteria

**MCP Regression (Must Pass)**:
- [ ] Test 1.1: Single project direct creation
- [ ] Test 1.2: Hierarchical projects direct creation
- [ ] Test 1.3: List projects works
- [ ] Test 1.4: Create task works
- [ ] **NO queue entries created by MCP**

**Bot Queue (New Feature)**:
- [ ] Test 2.1: Single project queued and created
- [ ] Test 2.2: Hierarchical projects with temp ID resolution
- [ ] Queue entries marked complete
- [ ] User owns all projects
- [ ] Bot has access to all projects

**Edge Cases**:
- [ ] Test 3.1: Empty queue handled gracefully
- [ ] Test 3.2: Login required enforced

**System Health**:
- [ ] No errors in Render logs
- [ ] No errors in browser console
- [ ] Migrations applied successfully

---

## Debugging Commands

**Check Render Logs**:
```bash
# Look for queue flush events
grep "Flushed project queue" logs

# Look for errors
grep "ERROR.*project" logs
```

**Check Database State**:
```sql
-- All queue entries from last hour
SELECT
    id,
    username,
    CASE
        WHEN projects IS NOT NULL THEN jsonb_array_length(projects)
        ELSE 1
    END as count,
    status,
    created_at,
    completed_at
FROM project_creation_queue
WHERE created_at > NOW() - INTERVAL '1 hour'
ORDER BY created_at DESC;

-- Stuck entries (pending > 10 min)
SELECT * FROM project_creation_queue
WHERE status = 'pending'
AND created_at < NOW() - INTERVAL '10 minutes';
```

**Check Browser Console** (F12):
- Network tab: Look for failed API calls
- Console tab: Look for JavaScript errors

---

## Next Steps

**If MCP regression tests pass**:
✅ MCP unchanged, safe to proceed with bot testing

**If bot tests pass**:
- [ ] Mark bead solutions-eofy as complete
- [ ] Document in SUMMARY-2026-01-05.md
- [ ] Test with legacy user @ivan

**If any test fails**:
- [ ] Document failure
- [ ] Check logs and database
- [ ] Create new bead for fix
- [ ] Revert if critical

