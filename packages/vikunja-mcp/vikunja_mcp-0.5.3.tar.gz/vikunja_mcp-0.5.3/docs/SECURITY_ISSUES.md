# Factumerit Security Issues & Failure Modes

**Date**: 2025-12-27
**Status**: PRODUCTION BLOCKERS - Must fix before launch
**Related**: solutions-56u9, solutions-hwgt

---

## Critical Issues (P0)

### 1. OAuth Browser Session Bug (solutions-56u9)

**Severity**: CRITICAL
**Status**: OPEN
**Impact**: Users see other users' tasks

#### Description

The Matrix OAuth connect flow creates Vikunja API tokens under the WRONG user account when browser sessions are shared.

#### Root Cause

```javascript
// matrix-connect.html (line 184-186)
async function checkAuth() {
  const jwt = localStorage.getItem(CONFIG.auth.storageKey);
  if (!jwt) return null;
  // ...
}
```

The connect page checks `localStorage.getItem('token')` for an existing Vikunja JWT. If ANY user is logged into Vikunja in that browser, their JWT is used to create the API token, regardless of which Matrix user clicked the OAuth link.

#### Attack Scenario

1. Admin (i2) logs into vikunja.factumerit.app in Chrome
2. User B (Latin Trainer) sends message to Matrix bot
3. User B clicks OAuth link (opens in SAME Chrome browser)
4. `matrix-connect.html` finds i2's JWT in localStorage
5. Creates API token for i2's Vikunja account
6. Bot stores i2's token under User B's Matrix ID
7. User B now has full access to i2's tasks!

#### Evidence

Incident on 2025-12-27:
- Latin Trainer connected via OAuth
- Saw 256 tasks (i2's task count)
- Should have seen 0 tasks (new user)

#### Workarounds (Temporary)

1. **Use incognito/private browsing** for OAuth flow
2. **Manual token entry**: Create token in Vikunja Settings, use `!vik <token>`
3. **Clear stale connections**: `!vik disconnect` before reconnecting

#### Proposed Fixes

**Option A: Clear localStorage before OAuth (Quick Fix)**
```javascript
// At start of main()
localStorage.removeItem('token');
```
- Pros: Simple, one-line fix
- Cons: Breaks existing browser sessions for that user

**Option B: Pass user context through flow (Proper Fix)**
```javascript
// Embed Matrix user ID in nonce
// Verify at token creation that OIDC user matches expected user
```
- Pros: Correct solution
- Cons: Complex, requires changes to entire flow

**Option C: Server-side token creation**
```javascript
// Bot creates token directly via Vikunja Admin API
// No browser involvement, no session issues
```
- Pros: Eliminates browser session entirely
- Cons: Requires Vikunja admin token, bot has elevated privileges

**Recommended**: Option A for immediate fix, Option C for long-term

---

### 2. Nonces Lost on Restart

**Severity**: HIGH
**Status**: OPEN
**Impact**: Users must re-initiate OAuth after any deploy

#### Description

Pending OAuth connections are stored in-memory:
```python
# server.py line 1112
_pending_connections: dict[str, dict] = {}
```

When the bot restarts (deploy, crash, etc.), all pending connections are lost.

#### User Experience

1. User clicks OAuth link
2. Bot deploys (automatic from git push)
3. User completes OAuth flow
4. Bot returns "Connection request expired or invalid"
5. User must request new link and start over

#### Fix

Store nonces in persistent storage:

**Option A: Database**
```python
# Add to PostgreSQL
CREATE TABLE pending_connections (
    nonce TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL
);
```

**Option B: Redis**
```python
# Use Redis with TTL
redis.setex(f"nonce:{nonce}", 300, json.dumps(data))
```

**Option C: Config file**
```python
# Write to persistent disk (simple, works with Render)
with open("/data/config/pending_connections.yaml", "w") as f:
    yaml.dump(_pending_connections, f)
```

**Recommended**: Option C (simplest, no new dependencies)

---

### 3. Tokens Stored in Plaintext

**Severity**: MEDIUM
**Status**: OPEN
**Impact**: Compromised disk = compromised all user tokens

#### Description

User Vikunja tokens stored in plaintext:
```yaml
# /data/config/config.yaml
users:
  "@alice:matrix.factumerit.app":
    vikunja_token: "tk_xxxxxxxxxxxxxxxxxxxxx"
```

#### Risk

- Anyone with disk access can read all tokens
- Backup leaks expose all user credentials
- No key rotation mechanism

#### Fix

Encrypt tokens at rest:
```python
from cryptography.fernet import Fernet

key = os.environ["TOKEN_ENCRYPTION_KEY"]
fernet = Fernet(key)

def encrypt_token(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()
```

---

## High Priority Issues (P1)

### 4. Rate Limiting Not Implemented

**Severity**: HIGH
**Status**: OPEN (solutions-q5w2)
**Impact**: DoS via command spam, LLM cost exhaustion

#### Description

No rate limiting on Matrix commands. A malicious user can:
- Send thousands of commands per minute
- Exhaust Claude API credits
- Deny service to other users

#### Proposed Limits

| Action | Limit | Window |
|--------|-------|--------|
| Commands per user | 10 | 1 minute |
| Commands per user | 100 | 1 hour |
| LLM requests per user | 5 | 1 minute |

---

### 5. E2EE Silently Breaks Bot

**Severity**: HIGH
**Status**: MITIGATED (hardcoded disabled)
**Impact**: Bot stops responding if E2EE accidentally enabled

#### Description

If `encryption_enabled=True` is set, bot cannot read messages but fails silently.

#### Current Mitigation

E2EE is hardcoded disabled in `matrix_client.py:58`:
```python
config = AsyncClientConfig(encryption_enabled=False)
```

This is defense-in-depth - cannot be accidentally enabled via environment variable.

#### Validation Required

- [ ] Verify E2EE disabled in production logs
- [ ] Add startup check that logs E2EE status
- [ ] Add health endpoint that reports E2EE status

---

## Medium Priority Issues (P2)

### 6. Input Sanitization Missing

**Severity**: MEDIUM
**Status**: OPEN (solutions-2gn5)
**Impact**: XSS in HTML responses, potential injection

#### Vectors

- Task titles with HTML/script tags
- Project names with path traversal
- Prompt injection via task descriptions

#### Fix

```python
import html
def sanitize_input(text: str) -> str:
    return html.escape(text)[:256]
```

---

### 7. No Audit Logging

**Severity**: MEDIUM
**Status**: OPEN (solutions-haxz)
**Impact**: Cannot investigate security incidents

#### Missing

- Admin command usage not logged
- Token operations not logged
- Failed auth attempts not tracked

---

## Failure Mode Matrix

| Mode | Cause | Detection | Recovery |
|------|-------|-----------|----------|
| OAuth token mismatch | Shared browser session | User reports wrong tasks | `!vik disconnect`, incognito |
| Nonce expired | Bot restart | "Connection expired" error | Request new link |
| Bot not responding | E2EE enabled | No responses in logs | Verify E2EE disabled |
| Admin API fails | Wrong token type | "Not server admin" | Use `syt_` token |
| Matrix sync timeout | Network/homeserver | Missed messages | Auto-reconnect |
| LLM timeout | Claude API slow | Response delay | Automatic retry |
| Token exhaustion | No rate limiting | All requests fail | Add rate limits |

---

## Security Checklist (Before Production)

### Must Fix (P0)
- [ ] **solutions-56u9**: Fix OAuth browser session bug
- [ ] Implement persistent nonce storage
- [ ] Add token encryption

### Should Fix (P1)
- [ ] **solutions-q5w2**: Implement rate limiting
- [ ] Validate E2EE disabled on startup
- [ ] Add health check for critical settings

### Nice to Have (P2)
- [ ] **solutions-2gn5**: Input sanitization
- [ ] **solutions-haxz**: Audit logging
- [ ] Pre-commit hooks for secret detection

---

## Incident Response

### If OAuth Bug Exploited

1. **Immediate**: Disable OAuth links (remove from bot responses)
2. **Notify**: Alert affected users via Matrix DM
3. **Investigate**: Check config.yaml for mismatched tokens
4. **Remediate**: Have users disconnect and reconnect properly
5. **Fix**: Deploy OAuth fix (clear localStorage)

### If Tokens Leaked

1. **Rotate**: All users must create new Vikunja tokens
2. **Clear**: Delete config.yaml, redeploy
3. **Notify**: Alert all users to reconnect
4. **Fix**: Implement token encryption

---

## References

- `ARCHITECTURE_V2.md` - System architecture
- `MATRIX_SECURITY.md` - Security model
- solutions-56u9 - OAuth bug bead
- solutions-hwgt - Architecture review bead

---

**Last Updated**: 2025-12-27
**Author**: Claude Code (solutions-hwgt)
