# Vikunja API Token Investigation

**Date:** 2026-01-04  
**Status:** Ready to test  
**Issue:** Bot provisioning fails due to API token creation errors

## Quick Start

### Run the Critical Test (5 minutes)

```bash
cd factumerit/backend/backend
python3 test_html_connect_flow.py --username ivan_test02 --password <password>
```

**This will tell you:**
- ✅ If token creation works → Fix bot provisioning (1-2 hours)
- ❌ If token creation is broken → Use JWT workaround (2-4 hours)

## Background

### The Problem
1. API tokens created via UI return 401 Unauthorized
2. API tokens created via API return "Invalid Data"
3. JWT tokens work fine
4. Bot provisioning is blocked

### The Discovery
Vikunja's HTML OAuth connect flow uses a specific pattern:
1. Fetch `/api/v1/routes` to get available permissions
2. Build full permissions object from routes
3. Create token with complete payload (title + expiry + permissions)

Our bot provisioning uses minimal payload (just title) → "Invalid Data" error

## Test Scripts

### 1. `test_html_connect_flow.py` ⚡ START HERE
Replicates the exact HTML connect flow to test if token creation works.

```bash
python3 test_html_connect_flow.py --username <user> --password <pwd>
```

### 2. `debug_vikunja_tokens.py`
Tests all token creation variations.

```bash
python3 debug_vikunja_tokens.py --username <user> --password <pwd>
```

Optional: Test manually created token from UI:
```bash
python3 debug_vikunja_tokens.py --username <user> --password <pwd> --manual-token tk_abc123...
```

### 3. `inspect_vikunja_db_tokens.py`
Inspects database to see how tokens are stored.

```bash
export VIKUNJA_DB_HOST=localhost
export VIKUNJA_DB_PASSWORD=<password>
python3 inspect_vikunja_db_tokens.py --user-id 33 --show-structure
```

## Documentation

### Main Docs (in `spawn/spawn-solutions/docs/factumerit/`)

1. **097-INVESTIGATION_SUMMARY.md** - Start here
   - Overview of the investigation
   - What we know and what we built
   - Next steps and timeline

2. **097.1-TOKEN_INVESTIGATION_FINDINGS.md** - Detailed analysis
   - Source code insights
   - Theories and hypotheses
   - Action plans for different scenarios

3. **097.2-QUICK_TEST_GUIDE.md** - Step-by-step instructions
   - How to run each test
   - Decision tree
   - Troubleshooting

4. **097-TOKEN_CREATION_ROOT_CAUSE_INVESTIGATION.md** - Original investigation
   - Initial findings
   - Test results
   - Root causes identified

## Decision Tree

```
Run test_html_connect_flow.py
│
├─ ✅ SUCCESS: Token creation works
│  └─ Fix bot provisioning:
│     1. Fetch routes before creating token
│     2. Build full permissions object
│     3. Include expiry date
│     4. Test and deploy
│     Timeline: 1-2 hours
│
└─ ❌ FAILURE: Token creation broken
   │
   Test manually created token from UI
   │
   ├─ ✅ Manual token works
   │  └─ Investigate API endpoint
   │     - Check Vikunja version
   │     - Review nginx config
   │     - Check logs
   │
   └─ ❌ Manual token fails
      └─ Use JWT workaround:
         - Bots login with username/password
         - Store credentials (not tokens)
         - Refresh JWT as needed
         Timeline: 2-4 hours
```

## Expected Fix (if HTML flow works)

Update `src/vikunja_mcp/bot_provisioning.py`:

```python
# Step 2a: Fetch routes
routes_resp = requests.get(
    f"{base_url}/api/v1/routes",
    headers={"Authorization": f"Bearer {jwt_token}"},
    timeout=30
)
routes = routes_resp.json()

# Step 2b: Build permissions
permissions = {}
for group, group_routes in routes.items():
    permissions[group] = list(group_routes.keys())

# Step 2c: Create token with full payload
expiry = datetime.utcnow() + timedelta(days=365)
resp = requests.put(
    f"{base_url}/api/v1/tokens",
    headers={"Authorization": f"Bearer {jwt_token}"},
    json={
        "title": f"Personal Bot Token ({username})",
        "expires_at": expiry.isoformat() + "Z",
        "permissions": permissions
    },
    timeout=30
)
```

## Key Insights

1. **JWT vs API tokens:** Some Vikunja endpoints only accept JWT tokens
2. **Permissions required:** Empty or missing permissions causes "Invalid Data"
3. **HTML flow works:** OAuth connect successfully creates tokens
4. **Our payload is wrong:** We need to match the HTML flow exactly

## Timeline

- **Testing:** 30 minutes
- **Fix (if HTML flow works):** 1-2 hours
- **Workaround (if needed):** 2-4 hours
- **Total:** 2-5 hours to resolution

## References

- [Vikunja Community Discussion](https://community.vikunja.io/t/profile-picture-sync-with-authentik-oauth-oidc-and-api-authentication-for-automated-uploads/3779)
- [Vikunja GitHub](https://github.com/go-vikunja/vikunja)
- [Vikunja API Docs](https://try.vikunja.io/api/v1/docs)

