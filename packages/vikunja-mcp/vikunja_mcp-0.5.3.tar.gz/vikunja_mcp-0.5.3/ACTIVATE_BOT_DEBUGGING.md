# Activate-Bot Endpoint Debugging Guide

## Problem
The `/activate-bot` endpoint is failing with a 500 error from the middleware:
```
⚠️ Activation Failed
Failed to share Inbox (middleware error: 500)
```

## Architecture

### The Spinal Tap Approach
We bypass Vikunja's buggy API (JWT tokens can't see bot users) by going directly to the database:

```
User clicks activation link
    ↓
/activate-bot endpoint (backend)
    ↓
/internal/share-project (middleware)
    ↓
Direct INSERT into project_users table (PostgreSQL)
```

### Key Components

1. **Backend** (`factumerit/backend/backend/src/vikunja_mcp/server.py`)
   - `/activate-bot` endpoint (line 9507)
   - Reads bot info from `personal_bots` table
   - Calls middleware to share

2. **Middleware** (`factumerit/vikunja-factumerit/middleware/main.py`)
   - `/internal/share-project` endpoint (line 148)
   - Calls `share_project_direct()` function

3. **Database** (`factumerit/vikunja-factumerit/middleware/database.py`)
   - `share_project_direct()` function (line 57)
   - Direct INSERT into `project_users` table

## Debugging Strategy (Working Backwards)

### Phase 1: Smoke Test ✅
**Goal**: Prove database connectivity works

**Changes Made**:
- Modified `/activate-bot` to display database lookup results
- Shows: username, bot_username, bot_vikunja_id, owner_vikunja_id, inbox_id
- Does NOT attempt sharing yet

**Test**:
```bash
python test_activate_bot.py <username>
```

**Expected Result**: HTML page showing all database values

### Phase 2: Test Middleware Directly 🔄
**Goal**: Isolate the 500 error to middleware

**Test**:
```bash
python test_middleware_share.py <project_id> <user_id> <permission>
```

**What to Check**:
1. Does middleware respond at all?
2. What's the actual error message?
3. Is it a database connection issue?
4. Is it a schema mismatch?
5. Is it a missing column?

### Phase 3: Fix the Bug 🎯
**Likely Causes**:
1. **Database connection** - `settings.database_url` not configured
2. **Schema mismatch** - `project_users` table doesn't exist or has different columns
3. **Missing columns** - Table exists but missing `created`/`updated` columns
4. **Permission issue** - Database user doesn't have INSERT permission
5. **Constraint violation** - Foreign key constraint on project_id or user_id

**How to Diagnose**:
```bash
# Check middleware logs
render logs -t factumerit-middleware

# Check database schema
psql $DATABASE_URL -c "\d project_users"

# Test database connection
psql $DATABASE_URL -c "SELECT 1"
```

## Files Modified

### Backend
- `factumerit/backend/backend/src/vikunja_mcp/server.py`
  - Added `_activation_smoke_test_html()` function
  - Commented out sharing logic temporarily
  - Returns smoke test page instead

### Test Scripts
- `factumerit/backend/test_activate_bot.py` - Test full flow
- `factumerit/backend/test_middleware_share.py` - Test middleware only

## How to Test

### Prerequisites
You need access to:
1. **Backend service** - `https://mcp.factumerit.app` (or local)
2. **Middleware service** - `https://vikunja.factumerit.app` (proxies to middleware)
3. **Database** - PostgreSQL with Vikunja schema

### Environment Variables Needed

**Backend** (already configured in Render):
- `DATABASE_URL` - PostgreSQL connection string
- `VIKUNJA_URL` - https://vikunja.factumerit.app
- `TOKEN_ENCRYPTION_KEY` - For decrypting bot credentials

**Middleware** (needs to be configured):
- `database_url` - Same PostgreSQL as backend (Vikunja database)
- `vikunja_url` - http://localhost:3456 or actual Vikunja instance

### Running Tests

#### 1. Smoke Test (Database Read)
```bash
cd factumerit/backend

# Test against production
python test_activate_bot.py <username> https://mcp.factumerit.app

# Test against local
python test_activate_bot.py <username> http://localhost:8000
```

**Expected**: HTML page showing bot info from database

#### 2. Middleware Test (Database Write)
```bash
cd factumerit/backend

# First, get the IDs you need
python test_middleware_share.py --lookup <username>

# Then test the share endpoint
python test_middleware_share.py <project_id> <bot_user_id> 1 https://vikunja.factumerit.app
```

**Expected**: JSON response `{"success": true, "message": "..."}`

#### 3. Check Middleware Logs
```bash
# If middleware is on Render
render logs -t factumerit-middleware

# Look for errors in share_project_direct()
```

### Common Issues

**Issue**: Middleware returns 500 with "database_url not configured"
**Fix**: Add `database_url` env var to middleware service in Render

**Issue**: "relation 'project_users' does not exist"
**Fix**: Middleware is pointing to wrong database (needs Vikunja DB, not token broker DB)

**Issue**: "column 'created' does not exist"
**Fix**: Vikunja schema version mismatch - check table structure

**Issue**: "permission denied for table project_users"
**Fix**: Database user needs INSERT permission on project_users table

## Next Steps

1. ✅ Run smoke test to verify database reads work
2. 🔄 Run middleware test to see actual error
3. 🎯 Fix the root cause based on error
4. ✅ Re-enable sharing logic
5. ✅ Test end-to-end activation

## Related Issues
- **solutions-3v4r**: Debug and fix bot project sharing (IN_PROGRESS)
- **solutions-vykv**: Re-implement deferred bot activation (CLOSED)
- **solutions-gsry**: Onboarding works with bot sharing (BLOCKED)

