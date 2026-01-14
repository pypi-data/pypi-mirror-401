# Local Development Setup

Run Vikunja + MCP server locally for faster development iteration.

## Quick Start

```bash
cd factumerit/backend/backend

# Start everything
docker-compose -f docker-compose.local.yml up

# In another terminal, run migrations
docker-compose -f docker-compose.local.yml exec mcp-server uv run python -c "from vikunja_mcp.database import init_db; init_db()"
```

**Services:**
- Vikunja: http://localhost:3456
- MCP Server: http://localhost:8000
- PostgreSQL: localhost:5432

## Test Beta Signup

1. **Create a beta token:**
   ```bash
   docker-compose -f docker-compose.local.yml exec postgres psql -U vikunja -d vikunja -c "
   INSERT INTO beta_signup_tokens (registration_code, email, created_at) 
   VALUES ('LOCAL-TEST', NULL, NOW());
   "
   ```

2. **Open signup page:**
   ```
   http://localhost:8000/beta-signup?code=LOCAL-TEST&email=test@example.com
   ```

3. **Watch logs:**
   ```bash
   docker-compose -f docker-compose.local.yml logs -f mcp-server
   ```

## Benefits

✅ **No deployment wait** - Changes reflect immediately with hot reload  
✅ **No rate limits** - Unlimited signups, no Resend quota  
✅ **Direct DB access** - Inspect/modify data easily  
✅ **Vikunja logs** - See both sides of the API  
✅ **Offline work** - No internet needed  

## Testing the Race Condition Fix

```python
# In signup_workflow.py, add artificial delays to test:
def stage_2_provision_bot(self, state):
    logger.info("[Stage 2] Provisioning bot...")
    bot_creds = provision_personal_bot(...)
    
    # Simulate slow database commit
    import time
    time.sleep(5)  # Exaggerate the race condition
    
    return state
```

Then test if Stage 3 verification catches it!

## Database Access

```bash
# Connect to PostgreSQL
docker-compose -f docker-compose.local.yml exec postgres psql -U vikunja -d vikunja

# Check recent signups
SELECT * FROM factumerit_users ORDER BY created_at DESC LIMIT 5;

# Check bot credentials
SELECT * FROM personal_bot_credentials ORDER BY created_at DESC LIMIT 5;

# Clear test data
DELETE FROM factumerit_users WHERE user_id LIKE 'vikunja:test%';
```

## Cleanup

```bash
# Stop services
docker-compose -f docker-compose.local.yml down

# Remove all data (fresh start)
docker-compose -f docker-compose.local.yml down -v
```

## Troubleshooting

**Port conflicts:**
```bash
# Change ports in docker-compose.local.yml:
ports:
  - "5433:5432"  # PostgreSQL
  - "3457:3456"  # Vikunja
  - "8001:8000"  # MCP server
```

**Database migrations:**
```bash
# Run migrations manually
docker-compose -f docker-compose.local.yml exec postgres psql -U vikunja -d vikunja < migrations/001_token_broker.sql
```

**Hot reload not working:**
```bash
# Rebuild the container
docker-compose -f docker-compose.local.yml up --build mcp-server
```

## Production vs Local

| Feature | Production | Local |
|---------|-----------|-------|
| Vikunja URL | vikunja.factumerit.app | localhost:3456 |
| Database | Render PostgreSQL | Local PostgreSQL |
| Emails | Resend (rate limited) | Disabled |
| Rate limiting | Enabled | Disabled |
| Deploy time | 2-5 minutes | Instant |

## Next Steps

Once local dev is working:
1. Test the staged workflow end-to-end
2. Verify bot verification (Stage 3) works
3. Confirm inbox sharing (Stage 5) succeeds
4. Add more test cases
5. Deploy to production with confidence!

