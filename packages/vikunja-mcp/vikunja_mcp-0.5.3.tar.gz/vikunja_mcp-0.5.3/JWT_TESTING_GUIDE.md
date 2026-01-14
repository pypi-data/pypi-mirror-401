# JWT Bot Authentication - Testing Guide

**Quick reference for testing the JWT implementation**

---

## Prerequisites

1. **Database migration applied**:
   ```bash
   psql $DATABASE_URL -f migrations/015_personal_bots_password.sql
   ```

2. **Environment variables set**:
   ```bash
   export DATABASE_URL="postgresql://..."
   export VIKUNJA_URL="https://vikunja.factumerit.app"
   export VIKUNJA_ADMIN_TOKEN="..."  # For bot registration
   ```

---

## Quick Test (5 minutes)

Run the comprehensive test suite:

```bash
cd factumerit/backend/backend
python3 test_jwt_bot_implementation.py --username test_user
```

**Expected output**:
```
🧪 JWT Bot Implementation Test Suite
⏰ Started at: 2026-01-04 ...

======================================================================
TEST 1: Bot Provisioning
======================================================================
📝 Provisioning bot for user: vikunja:test_user
✅ Bot provisioned successfully!
   - Username: @e-abc123
   - Vikunja ID: 42
   - Display Name: test-bot
   - Has Password: True

💾 Storing bot credentials in database...
✅ Credentials stored successfully!

======================================================================
TEST 2: JWT Authentication
======================================================================
🔍 Retrieving bot credentials from database...
✅ Retrieved credentials for: @e-abc123

🔑 Getting JWT token (first time)...
✅ JWT token obtained: v1.eyJhbGciOiJIUzI1NiIsInR5cCI...

🔑 Getting JWT token (second time - should use cache)...
✅ JWT token obtained: v1.eyJhbGciOiJIUzI1NiIsInR5cCI...
✅ Cache working! Same token returned

📊 Cache statistics:
   - Total cached: 1
   - Valid tokens: 1
   - Expired tokens: 0

======================================================================
TEST 3: BotVikunjaClient Operations
======================================================================
🤖 Creating BotVikunjaClient for user: vikunja:test_user
✅ Client created successfully!

📡 Testing API call: GET /api/v1/user
✅ API call successful!
   - Bot username: @e-abc123
   - Bot ID: 42
   - Bot name: test-bot

📡 Testing API call: GET /api/v1/projects
✅ API call successful!
   - Projects found: 3

======================================================================
✅ ALL TESTS PASSED!
======================================================================

🎉 JWT bot implementation is working correctly!
```

---

## Manual Testing

### 1. Test Bot Provisioning

```python
from vikunja_mcp.bot_provisioning import provision_personal_bot, store_bot_credentials

# Provision a bot
credentials = provision_personal_bot("alice", display_name="Alice's Bot")
print(f"Bot: {credentials.username}")
print(f"Has password: {bool(credentials.password)}")

# Store in database
store_bot_credentials("vikunja:alice", credentials)
```

### 2. Test JWT Token Retrieval

```python
from vikunja_mcp.bot_provisioning import get_user_bot_credentials
from vikunja_mcp.bot_jwt_manager import get_bot_jwt, get_cache_stats

# Get credentials
bot_username, bot_password = get_user_bot_credentials("vikunja:alice")
print(f"Bot: {bot_username}")

# Get JWT token
jwt_token = get_bot_jwt(bot_username, bot_password, "https://vikunja.factumerit.app")
print(f"JWT: {jwt_token[:30]}...")

# Check cache
stats = get_cache_stats()
print(f"Cached tokens: {stats['total_cached']}")
```

### 3. Test BotVikunjaClient

```python
from vikunja_mcp.vikunja_client import BotVikunjaClient

# Create client with user_id (JWT auth)
client = BotVikunjaClient(user_id="vikunja:alice")

# Test API calls
user_info = client.get_bot_user()
print(f"Bot: {user_info['username']}")

projects = client.get_projects()
print(f"Projects: {len(projects)}")
```

---

## Troubleshooting

### Error: "No bot credentials found for user"

**Cause**: Bot not provisioned yet  
**Fix**: Run bot provisioning first:
```python
from vikunja_mcp.bot_provisioning import provision_personal_bot, store_bot_credentials
credentials = provision_personal_bot("username", display_name="Bot")
store_bot_credentials("vikunja:username", credentials)
```

### Error: "column encrypted_password does not exist"

**Cause**: Database migration not applied  
**Fix**: Apply migration:
```bash
psql $DATABASE_URL -f migrations/015_personal_bots_password.sql
```

### Error: "401 Unauthorized" on API calls

**Cause**: JWT token expired or invalid  
**Fix**: Clear cache and retry:
```python
from vikunja_mcp.bot_jwt_manager import clear_bot_jwt_cache
clear_bot_jwt_cache()  # Clear all
# or
clear_bot_jwt_cache("@e-abc123")  # Clear specific bot
```

### Error: "BotJWTError: Login failed"

**Cause**: Invalid bot credentials  
**Fix**: Check bot username/password in database:
```sql
SELECT bot_username, encrypted_password IS NOT NULL as has_password
FROM personal_bots
WHERE user_id = 'vikunja:username';
```

---

## Performance Monitoring

### Check JWT Cache Stats

```python
from vikunja_mcp.bot_jwt_manager import get_cache_stats

stats = get_cache_stats()
print(f"Total cached: {stats['total_cached']}")
print(f"Valid tokens: {stats['valid_tokens']}")
print(f"Expired tokens: {stats['expired_tokens']}")
```

### Expected Performance

- **First API call**: ~200-500ms (includes login)
- **Cached calls**: ~50-100ms (no login)
- **Cache hit rate**: >99% (tokens valid for 23 hours)
- **Memory usage**: ~100 bytes per cached token

---

## Next Steps After Testing

1. ✅ All tests pass → Deploy to staging
2. ❌ Tests fail → Check troubleshooting section
3. Monitor JWT cache performance in production
4. Optionally migrate existing bots to JWT (backward compatible)

