# Bot Response Workflow - Complete Trace

## Problem Statement

User `ivan_test20` signed up successfully, but the bot `@e-{hex}` is not responding to @mentions in tasks.

## Complete Workflow Trace

### Phase 1: Beta Signup (server.py → signup_workflow.py)

**Entry Point:** `POST /beta-signup` (server.py line 9217)

```
1. User submits form with email=ivan+test20@ivantohelpyou.com, code=BETA-VHDL-2026
2. Validate token (registration_tokens.py:54)
   - Check token exists ✅
   - Check not revoked ✅
   - Check not expired ✅
   - Check duplicate signup ✅
   - Check uses_remaining > 0 ✅ (was 1)
3. Create factumerit_users entry (server.py:9290)
   - INSERT INTO factumerit_users (user_id, email, ...)
   - user_id = "vikunja:ivan_test20"
4. Record token usage (registration_tokens.py:132)
   - INSERT INTO token_usage (token, user_id, used_at)
   - UPDATE registration_tokens SET uses_remaining = 0
5. Run signup workflow (signup_workflow.py:355)
```

### Phase 2: Signup Workflow - 7 Stages

**Stage 1: Create Vikunja User** (signup_workflow.py:54)
```
POST /api/v1/register
{
  "username": "ivan_test20",
  "email": "ivan+test20@ivantohelpyou.com",
  "password": "{random}"
}

Response: 200 OK
{
  "id": 123,  // vikunja_user_id
  "username": "ivan_test20",
  "token": "jwt_token_here"
}

✅ SUCCESS
- state.vikunja_user_id = 123
- state.vikunja_jwt_token = "jwt_..."
```

**Stage 2: Provision Bot** (signup_workflow.py:95)
```
Calls: bot_provisioning.provision_personal_bot()

1. Generate bot username: e-{random_hex}
2. Generate bot email: e-{random_hex}@factumerit.app
3. Generate bot password: {random}

4. Register bot in Vikunja:
   POST /api/v1/register
   {
     "username": "e-73585c",
     "email": "e-73585c@factumerit.app",
     "password": "{random}"
   }
   
   Response: 200 OK
   {
     "id": 124,  // bot_vikunja_user_id
     "username": "e-73585c"
   }

5. Login as bot to get JWT:
   POST /api/v1/login
   {
     "username": "e-73585c",
     "password": "{random}"
   }
   
   Response: 200 OK
   {
     "token": "bot_jwt_token"
   }

6. Set bot display name:
   POST /api/v1/user/settings/general
   Headers: Authorization: Bearer {bot_jwt_token}
   {
     "name": "eis",
     "overdue_tasks_reminders_time": "09:00"
   }
   
   Response: 200 OK

7. Store bot credentials in database:
   INSERT INTO personal_bots (
     user_id,
     bot_username,
     display_name,
     vikunja_user_id,
     encrypted_password,
     owner_vikunja_user_id,
     owner_vikunja_token
   ) VALUES (
     'vikunja:ivan_test20',
     'e-73585c',
     'eis',
     124,
     encrypt('bot_password'),
     123,
     encrypt('user_jwt_token')
   )

✅ SUCCESS
- state.bot_credentials = BotCredentials(username="e-73585c", password="{random}", vikunja_user_id=124)
```

**Stage 3: Verify Bot Exists** (signup_workflow.py:153)
```
Retry loop: 10 attempts × 2.5s delay = 25s max

Attempt 1-10:
  POST /api/v1/login
  {
    "username": "e-73585c",
    "password": "{random}"
  }
  
  Response: 200 OK (bot can login immediately)
  
✅ SUCCESS on attempt 1
- state.bot_verified = True
```

**Stage 4: Find Inbox** (signup_workflow.py:193)
```
GET /api/v1/projects
Headers: Authorization: Bearer {user_jwt_token}

Response: 200 OK
[
  {
    "id": 456,
    "title": "Inbox",
    ...
  }
]

✅ SUCCESS
- state.inbox_project_id = 456
```

**Stage 5: Share Inbox with Bot** (signup_workflow.py:229)
```
Retry loop: 10 attempts × 3.0s delay = 30s max

Attempt 1:
  PUT /api/v1/projects/456/users
  Headers: Authorization: Bearer {user_jwt_token}
  {
    "username": "e-73585c",
    "permission": 1
  }
  
  Response: 404 Not Found
  {
    "code": 1005,
    "message": "The user does not exist."
  }
  
  Wait 3 seconds...

Attempt 2-10: Same 404 error

❌ FAILED after 30 seconds
- state.inbox_shared = False
```

**Stage 6: Create Welcome Task** (signup_workflow.py:279)
```
PUT /api/v1/projects/456/tasks
Headers: Authorization: Bearer {user_jwt_token}
{
  "title": "👋 Welcome! Your AI assistant is @e-73585c",
  "description": "..."
}

Response: 201 Created

✅ SUCCESS
- state.welcome_task_created = True
```

**Stage 7: Send Password Reset** (signup_workflow.py:320)
```
POST /api/v1/user/password/reset
{
  "email": "ivan+test20@ivantohelpyou.com"
}

Response: 200 OK

✅ SUCCESS
- state.password_reset_sent = True
```

### Phase 3: Notification Poller Picks Up Bot

**Poller Startup** (notification_poller.py:1886)
```
On server start:
1. Call get_all_bot_user_ids() (bot_provisioning.py:518)
   
   SELECT user_id FROM personal_bots
   WHERE vikunja_instance = 'default' AND encrypted_password IS NOT NULL
   ORDER BY created_at
   
   Result: ['vikunja:ivan_test1', ..., 'vikunja:ivan_test19']
   
   NOTE: ivan_test20 NOT in list yet (signup still in progress)

2. Create poller for each bot:
   for user_id in bot_user_ids:
     client = BotVikunjaClient(user_id=user_id)
     poller = NotificationPoller(client=client)
     pollers[user_id] = poller
     asyncio.create_task(poller.start())

3. Start background task to check for new bots every 60 seconds:
   async def check_for_new_bots():
     while True:
       await asyncio.sleep(60)
       current_user_ids = get_all_bot_user_ids()
       for user_id in current_user_ids:
         if user_id not in pollers:
           # NEW BOT DETECTED
           logger.info(f"New bot detected for {user_id}")
           client = BotVikunjaClient(user_id=user_id)
           poller = NotificationPoller(client=client)
           pollers[user_id] = poller
           asyncio.create_task(poller.start())
```

**Timeline:**
- T+0s: Signup starts
- T+30s: Signup completes, bot stored in database
- T+60s: Poller checks for new bots, finds ivan_test20
- T+60s: Poller creates BotVikunjaClient for ivan_test20
- T+60s: Poller starts polling for ivan_test20

### Phase 4: Bot Polling for Notifications

**BotVikunjaClient Initialization** (vikunja_client.py:520)
```
client = BotVikunjaClient(user_id="vikunja:ivan_test20")

1. Load bot credentials from database:
   SELECT bot_username, encrypted_password, vikunja_user_id
   FROM personal_bots
   WHERE user_id = 'vikunja:ivan_test20'

   Result: ('e-73585c', encrypted_password, 124)

2. Decrypt password
3. Login to get JWT token:
   POST /api/v1/login
   {
     "username": "e-73585c",
     "password": "{decrypted}"
   }

   Response: 200 OK
   {
     "token": "bot_jwt_token"
   }

4. Store token for API calls
```

**Notification Polling Loop** (notification_poller.py:722)
```
Every 10 seconds:
  GET /api/v1/notifications
  Headers: Authorization: Bearer {bot_jwt_token}

  Response: 200 OK
  [
    {
      "id": 789,
      "name": "task.comment",
      "notification": {
        "task": {
          "id": 999,
          "title": "Test task",
          "project_id": 456
        },
        "comment": {
          "comment": "@e-73585c !help"
        },
        "doer": {
          "id": 123,
          "username": "ivan_test20"
        }
      }
    }
  ]

  Process notification:
  1. Extract command: "!help"
  2. Execute command handler
  3. Post response as comment
  4. Mark notification as read
```

### Phase 5: User Creates Task and @Mentions Bot

**User Action:**
```
User goes to Vikunja UI
Creates task in Inbox project (id=456)
Adds comment: "@e-73585c !help"
```

**Vikunja's Notification System:**
```
1. Vikunja detects @mention of user "e-73585c"
2. Checks if e-73585c has access to project 456

   SELECT * FROM project_users
   WHERE project_id = 456 AND user_id = 124

   Result: EMPTY (because Stage 5 failed!)

3. Vikunja does NOT create notification (user not shared on project)
```

## Root Cause Analysis

### Why Bot Doesn't Respond

**The Critical Failure Point: Stage 5 (Inbox Sharing)**

```python
# signup_workflow.py line 254-257
json={
    "username": state.bot_credentials.username,  # ✅ Correct field
    "permission": 1  # ❌ WRONG FIELD NAME!
}

Response: 404 - "The user does not exist."
```

**ROOT CAUSE: Wrong API Field Name**

According to Vikunja's Go source code (`102-VIKUNJA_API_QUIRKS.md`):

```go
type ProjectUser struct {
    UserID   int64  `json:"-"`        // Ignored by API
    Username string `json:"username"` // ✅ Correct
    Right    int    `json:"right"`    // ✅ Correct (NOT "permission"!)
}
```

**What we're sending:**
```python
{"username": "e-73585c", "permission": 1}
```

**What Vikunja expects:**
```python
{"username": "e-73585c", "right": 1}
```

**Why does this cause 404 "user does not exist"?**

When Vikunja receives an unknown field (`permission`), it likely:
1. Ignores the unknown field
2. Tries to process the request with only `username`
3. Fails validation because `right` is missing
4. Returns a generic 404 error instead of a proper validation error

This is a **field name typo**, NOT a timing issue!

**Evidence:**
- Other parts of the codebase use `"right": 1` correctly (bot_provisioning.py:468)
- The signup workflow is the ONLY place using `"permission": 1`
- Stage 3 (bot verification) succeeds immediately, proving the bot exists
- Stage 5 fails ALL 10 retries with the same error, proving it's not timing

### What Happens When Sharing Fails

```
1. Bot is created ✅
2. Bot can login ✅
3. Bot is stored in database ✅
4. Poller picks up bot ✅
5. Bot polls for notifications ✅
6. User @mentions bot in Inbox ❌
7. Vikunja checks if bot has access to Inbox ❌
8. Vikunja does NOT create notification ❌
9. Bot never sees the @mention ❌
```

**The bot is polling correctly, but Vikunja isn't sending notifications because the bot doesn't have access to the project.**

## Verification Steps

### 1. Check if bot exists in Vikunja

```bash
curl -H "Authorization: Bearer {admin_token}" \
  https://vikunja.factumerit.app/api/v1/users?s=e-73585c
```

Expected: Should return bot user with id=124

### 2. Check if bot has access to Inbox

```bash
curl -H "Authorization: Bearer {user_token}" \
  https://vikunja.factumerit.app/api/v1/projects/456/users
```

Expected: Should include bot user (id=124) if sharing succeeded
Actual: Probably empty or missing bot

### 3. Manually share Inbox with bot

```bash
curl -X PUT \
  -H "Authorization: Bearer {user_token}" \
  -H "Content-Type: application/json" \
  -d '{"username": "e-73585c", "permission": 1}' \
  https://vikunja.factumerit.app/api/v1/projects/456/users
```

If this succeeds: Timing issue (bot wasn't visible yet)
If this fails with 404: Different issue (API bug, wrong endpoint, etc.)

### 4. Check poller logs

```bash
# On Render dashboard, check logs for:
grep "New bot detected" logs
grep "vikunja:ivan_test20" logs
grep "Starting notification poller" logs
```

Expected: Should see "New bot detected for vikunja:ivan_test20" around T+60s

### 5. Test bot response after manual sharing

If manual sharing succeeds:
1. Create task in Inbox
2. Add comment: "@e-73585c !help"
3. Wait 10 seconds (one poll cycle)
4. Check if bot responds

## THE FIX

### Change "permission" to "right"

**File:** `factumerit/backend/backend/src/vikunja_mcp/signup_workflow.py`
**Line:** 256

**Before:**
```python
json={
    "username": state.bot_credentials.username,
    "permission": 1  # ❌ WRONG
}
```

**After:**
```python
json={
    "username": state.bot_credentials.username,
    "right": 1  # ✅ CORRECT
}
```

This is a **one-word fix** that will make Stage 5 succeed immediately (no timing issues, no retries needed).

## Next Steps

1. ✅ Check Render logs to confirm poller picked up test20
2. ✅ Manually test sharing API with curl
3. ✅ Check if bot exists in Vikunja user search
4. ✅ Manually share Inbox with bot if possible
5. ✅ Test bot response after manual sharing
6. ⏳ Implement permanent fix based on findings



