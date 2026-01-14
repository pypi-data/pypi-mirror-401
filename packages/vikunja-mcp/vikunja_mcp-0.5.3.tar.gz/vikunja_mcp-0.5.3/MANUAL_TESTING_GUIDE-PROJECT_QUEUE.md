# Manual Testing Guide: Project Queue Batching

**Bead**: solutions-eofy  
**Feature**: JSON Batch Support for Project Queue  
**Date**: 2026-01-05

---

## Prerequisites

1. **Deployed Backend**: Code deployed to Render (auto-deploys on git push)
2. **Database Migration**: Migration 017 applied ✅ (verified by integration tests)
3. **User Accounts**:
   - @ivan (legacy user without personal bot)
   - New test user (with personal bot)
4. **Access**:
   - Claude Desktop with Factumerit MCP server configured
   - Vikunja at vikunja.factumerit.app logged in (in browser)
   - MCP server at mcp.factumerit.app accessible

---

## Test Suite 1: Single Project Creation

### Test 1.1: Basic Single Project

**Steps**:
1. Open Claude Desktop (or use MCP API directly)
2. Ask: `"create project Book Reviews"` (the MCP tool will be called)
3. Wait for response

**Expected Result**:
```
✅ 1 project queued

Visit this link to create it:
https://mcp.factumerit.app/project-queue-processor

(You'll need to be logged into Vikunja)
```

**Verification**:
4. Click the processor link
5. Verify page shows:
   - "Processing 1 project..."
   - Progress indicator
   - Success message
6. Verify redirect to Vikunja
7. In Vikunja, verify:
   - Project "Book Reviews" exists
   - You own the project
   - Bot (@eis-yourname) has write access

**Database Check**:
```sql
SELECT id, username, title, projects, status 
FROM project_creation_queue 
WHERE username = 'yourname' 
ORDER BY created_at DESC LIMIT 1;
```

Expected: `title='Book Reviews'`, `projects=NULL`, `status='complete'`

---

### Test 1.2: Single Project with Description and Color

**Steps**:
1. Send: `"@eis create project 'Personal Goals' with description 'Track my 2026 goals' and color #ff6b6b"`
2. Click processor link

**Expected**:
- Project created with description and custom color
- All metadata preserved

---

## Test Suite 2: Hierarchical Projects

### Test 2.1: Simple Hierarchy (Parent > Child)

**Steps**:
1. Send: `"@eis create project tree: Work > Projects"`
2. Wait for bot response

**Expected Result**:
```
✅ 2 projects queued

Visit this link to create them:
https://mcp.factumerit.app/project-queue-processor
```

**Verification**:
3. Click processor link
4. Verify page shows "Processing 2 projects..."
5. In Vikunja, verify hierarchy:
   ```
   Work
   └── Projects
   ```
6. Verify both projects have bot access

**Database Check**:
```sql
SELECT id, username, projects, status 
FROM project_creation_queue 
WHERE username = 'yourname' 
ORDER BY created_at DESC LIMIT 1;
```

Expected: `projects` is JSONB array with 2 items, `status='complete'`

---

### Test 2.2: Deep Hierarchy (3 Levels)

**Steps**:
1. Send: `"@eis create Marketing > Campaigns > Q1 2026"`
2. Click processor link

**Expected Hierarchy**:
```
Marketing
└── Campaigns
    └── Q1 2026
```

**Verification**:
- All 3 projects created
- Parent-child relationships correct
- No orphaned projects

---

### Test 2.3: Complex Tree (Multiple Branches)

**Steps**:
1. Send: `"@eis create project structure: Company > Engineering > Backend, Company > Engineering > Frontend, Company > Marketing"`
2. Click processor link

**Expected Hierarchy**:
```
Company
├── Engineering
│   ├── Backend
│   └── Frontend
└── Marketing
```

**Critical**: Verify "Engineering" is created only once, not duplicated

---

## Test Suite 3: Multiple Siblings

### Test 3.1: Root-Level Siblings

**Steps**:
1. Send: `"@eis create projects: Work, Personal, Hobbies"`
2. Click processor link

**Expected**:
- 3 projects at root level (no parent)
- All created successfully
- All have bot access

---

## Test Suite 4: Legacy User (@ivan)

### Test 4.1: Legacy User Can Create Projects

**Steps**:
1. Login as @ivan (legacy user)
2. Send: `"@eis create project Test Legacy"`
3. Click processor link

**Expected**:
- ✅ Works without errors
- ✅ No "bot not provisioned" errors
- ✅ Project owned by @ivan
- ✅ Bot has write access

**Critical**: This is the main bug fix - verify it works!

---

## Test Suite 5: Error Handling

### Test 5.1: Not Logged Into Vikunja

**Steps**:
1. Logout of Vikunja
2. Visit processor link

**Expected**:
- Redirect to Vikunja login page
- OR error message: "Please log into Vikunja first"

---

### Test 5.2: No Pending Projects

**Steps**:
1. Visit processor link when queue is empty

**Expected**:
- Message: "No pending projects to create"
- OR redirect to Vikunja

---

### Test 5.3: Broken Parent Reference

**Steps**:
1. Manually insert broken queue entry:
```sql
INSERT INTO project_creation_queue
(user_id, username, bot_username, projects, status)
VALUES (
    'vikunja:testuser',
    'testuser',
    'eis-testuser',
    '[{"temp_id": -1, "title": "Child", "parent_project_id": -99}]'::jsonb,
    'pending'
);
```
2. Visit processor link

**Expected**:
- Project "Child" created at root level (fallback)
- No errors
- Status marked complete

---

## Test Suite 6: Performance & Edge Cases

### Test 6.1: Large Batch (10+ Projects)

**Steps**:
1. Send: `"@eis create 10 projects: P1, P2, P3, P4, P5, P6, P7, P8, P9, P10"`
2. Click processor link

**Expected**:
- All 10 created successfully
- Progress indicator updates
- No timeouts

---

### Test 6.2: Special Characters in Title

**Steps**:
1. Send: `"@eis create project 'Test & <Special> \"Chars\"'"`
2. Click processor link

**Expected**:
- Title sanitized (HTML stripped)
- Project created successfully

---

### Test 6.3: Concurrent Requests

**Steps**:
1. User A creates projects
2. User B creates projects at same time
3. Both click processor links

**Expected**:
- Each user sees only their own queue
- No cross-contamination
- Both succeed

---

## Success Criteria Checklist

- [ ] **Single project creation works**
- [ ] **Hierarchical trees preserve parent-child relationships**
- [ ] **Multiple siblings created correctly**
- [ ] **Legacy user (@ivan) can create projects**
- [ ] **Bot has write access to all created projects**
- [ ] **User owns all created projects**
- [ ] **One trip to processor handles entire batch**
- [ ] **Error handling works (no login, no queue, broken refs)**
- [ ] **Special characters handled correctly**
- [ ] **No duplicate projects in complex trees**

---

## Debugging Tips

### Check Queue Status
```sql
SELECT id, username, title, projects, status, created_at 
FROM project_creation_queue 
WHERE status = 'pending' 
ORDER BY created_at DESC;
```

### Check Recent Completions
```sql
SELECT id, username, 
       CASE 
           WHEN projects IS NOT NULL THEN jsonb_array_length(projects) 
           ELSE 1 
       END as project_count,
       status, created_at, completed_at
FROM project_creation_queue 
WHERE status = 'complete' 
ORDER BY completed_at DESC 
LIMIT 10;
```

### Check Logs (Render)
```bash
# Look for flush events
grep "Flushed project batch" logs

# Look for errors
grep "ERROR" logs | grep "project"
```

---

## Reporting Issues

If any test fails, document:
1. **Test number** (e.g., "Test 2.2 failed")
2. **Steps to reproduce**
3. **Expected vs actual result**
4. **Database state** (queue entry)
5. **Browser console errors** (if frontend issue)
6. **Server logs** (if backend issue)

Create a new bead with prefix "solutions-eofy" for any bugs found.

