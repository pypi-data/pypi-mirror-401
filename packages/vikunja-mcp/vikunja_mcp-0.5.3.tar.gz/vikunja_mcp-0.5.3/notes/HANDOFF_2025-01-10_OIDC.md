# Handoff: OIDC Fixes - January 10, 2026

## What Was Done

### 1. Login Loop Fix (DEPLOYED)
- **Problem**: Existing users got stuck in login loop after Google OAuth
- **Root Cause**: JWT `type` claim was 0 (AuthTypeUnknown) instead of 1 (AuthTypeUser)
- **Fix**: Changed `"type": 0` to `"type": 1` in `middleware/main.py:66`
- **Status**: ✅ Deployed and working

### 2. Welcome Task in Wrong Inbox (DEPLOYED)
- **Problem**: New OIDC users didn't see welcome task
- **Root Cause**: Bot service used admin token for API calls, so Stage 4 found bot's Inbox, not user's
- **Fix**: 
  - Middleware now passes `vikunja_jwt` (user's JWT) to bot
  - Bot uses user's JWT for Stage 4 & 6
- **Files Changed**:
  - `vikunja-factumerit/middleware/main.py` - Added `vikunja_jwt` to onboarding payload
  - `factumerit-bot/src/vikunja_mcp/server.py` - Use user JWT instead of admin token
- **Status**: ✅ Pushed, deploying now

### 3. Avatar Shows Old Initial (DEPLOYED)
- **Problem**: After username change, avatar still showed old initial ("U" not "I")
- **Root Cause**: `avatar_provider` in DB was "openid", not "initials" + PWA cache
- **Fix**:
  - `/internal/update-username` now also calls `reset_avatar_to_initials()`
  - Added `/internal/reset-avatar` endpoint
  - Added nginx no-cache headers for `/api/v1/avatar/`
- **Files Changed**:
  - `vikunja-factumerit/middleware/database.py` - Added `reset_avatar_to_initials()`
  - `vikunja-factumerit/middleware/main.py` - Updated endpoint
  - `vikunja-factumerit/nginx.conf` - Added avatar location block
- **Status**: ✅ Pushed, deploying now

### 4. Documentation Updated
- Updated `vikunja-factumerit/middleware/OIDC_MIDDLEWARE_EXPLAINER.md` with 3 new Gotcha sections
- **Status**: ✅ Pushed

## What's Pending

### Test the fixes
User (ivanschneider, id=130) needs to:
1. Wait ~3-4 min for Render deploys
2. Test new user signup flow - should see welcome task in Inbox
3. For existing avatar issue - may need to manually run:
   ```sql
   UPDATE users SET avatar_provider='initials', avatar_file_id=NULL WHERE id=130;
   ```
   Then clear browser cache

### Commits Made
```
vikunja-factumerit:
  e5b668c - fix: JWT type=1 for existing user login
  174a0ff - fix: pass user JWT for OIDC onboarding, add avatar reset
  0dc165c - docs: update OIDC explainer

factumerit-bot:
  5879d17 - fix: use user JWT for OIDC onboarding
```

## Key Files

- `/home/ivanadamin/projects/factumerit/vikunja-factumerit/middleware/main.py` - OIDC callback, JWT generation
- `/home/ivanadamin/projects/factumerit/vikunja-factumerit/middleware/OIDC_MIDDLEWARE_EXPLAINER.md` - Full docs
- `/home/ivanadamin/gt/factumerit/crew/ivan/src/vikunja_mcp/server.py` - Bot's `/internal/complete-oidc-onboarding`
- `/home/ivanadamin/gt/factumerit/crew/ivan/notes/OIDC_LOGIN_LOOP_FIX.md` - Original login loop fix notes
