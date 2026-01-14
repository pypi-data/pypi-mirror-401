# JWT Bot Authentication - Deployment Checklist

**Date**: 2026-01-04  
**Commit**: 71e53fc  
**Status**: Ready for Production

---

## Pre-Deployment Checklist

- [x] Code committed and pushed to GitHub
- [x] Database migration created (015_personal_bots_password.sql)
- [x] All tests passed locally
- [x] Documentation complete
- [ ] Render deployment triggered
- [ ] Render deployment successful

---

## Deployment Steps

### 1. Verify Render Deployment

Check Render dashboard:
- Service: `vikunja-slack-bot` (or your service name)
- Branch: `main`
- Commit: `71e53fc`
- Status: Should auto-deploy on push

**Manual trigger** (if needed):
```bash
# Via Render dashboard: Deploy > Manual Deploy > Deploy latest commit
```

### 2. Verify Environment Variables

Ensure these are set in Render:
- [x] `DATABASE_URL` - Auto-set by Render
- [x] `VIKUNJA_URL` - https://vikunja.factumerit.app
- [x] `VIKUNJA_ADMIN_TOKEN` - (set in Render dashboard)
- [x] `TOKEN_ENCRYPTION_KEY` - 4JbrMx1r2QfQf7IE2v2iaWEyqvFlq48caoqGtrMyNXU=

### 3. Database Migration (Already Applied)

Migration 015 was already applied to production database:
```bash
# Already done:
# psql $DATABASE_URL -f migrations/015_personal_bots_password.sql
```

Verify:
```bash
psql $DATABASE_URL -c "SELECT version, description FROM token_broker_migrations WHERE version = 15"
```

Expected output:
```
 version |                    description                     
---------+----------------------------------------------------
      15 | Add encrypted_password to personal_bots for JWT authentication
```

---

## Post-Deployment Testing

### Test 1: New User Bot Provisioning

Test with a brand new user:

```bash
# SSH into Render or run locally with production DATABASE_URL
cd factumerit/backend/backend

export DATABASE_URL="<get from Render dashboard>"
export VIKUNJA_URL="https://vikunja.factumerit.app"
export VIKUNJA_ADMIN_TOKEN` - (set in Render dashboard)"
export TOKEN_ENCRYPTION_KEY="4JbrMx1r2QfQf7IE2v2iaWEyqvFlq48caoqGtrMyNXU="

# Test with new user
uv run test_jwt_complete.py
```

Expected: ✅ All tests pass

### Test 2: Setup Beta Users

Provision bots for beta users:

```bash
# Update BETA_USERS in setup_beta_users.py first
# Add @ivan and other beta users

uv run setup_beta_users.py
```

Expected output:
```
✅ Successful: 3
❌ Failed: 0
🎉 All beta users provisioned successfully!
```

### Test 3: Cleanup Test Users

Remove test users created during development:

```bash
# Dry run first
uv run cleanup_test_users.py --dry-run

# Actual cleanup
uv run cleanup_test_users.py
```

---

## Beta User Setup

### Step 1: Identify Beta Users

Current beta users:
- @ivan (user_id: ?)
- User 2 (user_id: ?)
- User 3 (user_id: ?)

**Action needed**: Get actual user IDs from database:
```sql
SELECT user_id, username FROM factumerit_users WHERE username IN ('ivan', 'user2', 'user3');
```

### Step 2: Update setup_beta_users.py

Edit `setup_beta_users.py` and update `BETA_USERS`:
```python
BETA_USERS = [
    {
        "username": "ivan",
        "user_id": "vikunja:ivan",  # Use actual user_id from database
        "display_name": "eis",
    },
    # Add other beta users
]
```

### Step 3: Run Provisioning

```bash
uv run setup_beta_users.py
```

---

## Monitoring

### Check JWT Cache Performance

After 24 hours, check cache statistics:

```python
from vikunja_mcp.bot_jwt_manager import get_cache_stats

stats = get_cache_stats()
print(f"Total cached: {stats['total_cached']}")
print(f"Valid tokens: {stats['valid_tokens']}")
print(f"Expired tokens: {stats['expired_tokens']}")
```

Expected:
- Cache hit rate: >99%
- Valid tokens: Number of active bots
- Expired tokens: 0 (auto-refreshed)

### Check Database

Verify bot credentials are stored:
```sql
SELECT 
    user_id, 
    bot_username, 
    encrypted_password IS NOT NULL as has_password,
    encrypted_token IS NOT NULL as has_token,
    created_at
FROM personal_bots
ORDER BY created_at DESC
LIMIT 10;
```

Expected:
- New bots: `has_password = true`, `has_token = false`
- Old bots: `has_password = false`, `has_token = true` (backward compatible)

---

## Rollback Plan

If issues occur:

### Option 1: Revert Code
```bash
git revert 71e53fc
git push origin main
```

### Option 2: Keep Code, Use Legacy Path
- Existing bots with API tokens continue to work
- New bots can use `VIKUNJA_BOT_TOKEN` env var (deprecated but functional)

---

## Success Criteria

- [ ] Render deployment successful
- [ ] New user can provision bot with JWT
- [ ] Beta users provisioned successfully
- [ ] Test users cleaned up
- [ ] JWT cache working (same token on repeated calls)
- [ ] API calls successful with JWT
- [ ] No errors in Render logs

---

## Next Steps After Deployment

1. Monitor Render logs for 24 hours
2. Check JWT cache statistics
3. Verify beta users can use their bots
4. Document any issues
5. Plan migration of existing bots (optional)

