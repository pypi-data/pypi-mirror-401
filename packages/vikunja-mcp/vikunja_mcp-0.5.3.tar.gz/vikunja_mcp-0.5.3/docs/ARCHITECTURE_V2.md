# Factumerit Platform Architecture v2

**Version**: 2.0
**Date**: 2025-12-27
**Status**: DRAFT - Needs Security Fixes Before Production

---

## Document Status

This document supersedes:
- `analyses/factumerit/25-ARCHITECTURE.md` (2025-12-22) - **OUTDATED** (described Dendrite, now using Synapse)
- `analyses/factumerit/ARCHITECTURE.md` (2025-12-24) - **PARTIALLY CURRENT** (good detail, but missing OAuth bug)

**Key Changes from v1**:
- Switched from Dendrite to Synapse (required for MAS)
- Added Matrix Authentication Service (MAS)
- Documented critical OAuth security bug (solutions-56u9)
- Added failure mode analysis

---

## 1. System Overview

### High-Level Architecture

```
                     INTERNET
    ┌──────────────────────────────────────────────────────────────┐
    │                                                               │
    │   Matrix Federation     Slack API     Claude API    Browser  │
    │   (matrix.org, etc)                                          │
    │                                                               │
    └───────┬────────────────────┬────────────┬────────────┬───────┘
            │                    │            │            │
            ▼                    ▼            ▼            ▼
    ┌──────────────────────────────────────────────────────────────┐
    │                     RENDER PLATFORM                           │
    │                                                               │
    │  ┌─────────────────────┐    ┌────────────────────────────┐  │
    │  │  factumerit-matrix  │    │    vikunja-slack-bot       │  │
    │  │  (srv-...)          │    │    (srv-...)               │  │
    │  │                     │    │                            │  │
    │  │  ┌───────────────┐  │    │  ┌──────────────────────┐  │  │
    │  │  │     nginx     │  │    │  │    MCP Server        │  │  │
    │  │  │   :10000      │  │    │  │    (FastMCP)         │  │  │
    │  │  └───────┬───────┘  │    │  │                      │  │  │
    │  │          │          │    │  │  58 Vikunja Tools    │  │  │
    │  │    ┌─────┴─────┐    │    │  │  Claude AI Parser    │  │  │
    │  │    ▼           ▼    │    │  │  Slack Transport     │  │  │
    │  │  ┌─────┐  ┌──────┐  │    │  │  Matrix Transport    │  │  │
    │  │  │Synapse  │ MAS │  │    │  └──────────┬───────────┘  │  │
    │  │  │:8008 │  │:8080│  │    │             │              │  │
    │  │  └───┬──┘  └──┬──┘  │    │             │              │  │
    │  │      │        │     │    │             │              │  │
    │  └──────┼────────┼─────┘    └─────────────┼──────────────┘  │
    │         │        │                        │                  │
    │         └────┬───┘                        │                  │
    │              │                            │                  │
    │         ┌────▼────────────────────────────▼───────────────┐  │
    │         │            factumerit-db (PostgreSQL)           │  │
    │         │  ┌───────────┐  ┌─────────┐  ┌───────────────┐  │  │
    │         │  │matrix_jfmr│  │   mas   │  │    vikunja    │  │  │
    │         │  │ (Synapse) │  │ (Auth)  │  │   (Tasks)     │  │  │
    │         │  └───────────┘  └─────────┘  └───────────────┘  │  │
    │         └─────────────────────────────────────────────────┘  │
    │                                                               │
    │  ┌────────────────────────────────────────────────────────┐  │
    │  │                   vikunja (srv-...)                     │  │
    │  │  ┌──────────────┐  ┌──────────────────────────────┐    │  │
    │  │  │   Vikunja    │  │   Static OAuth Pages         │    │  │
    │  │  │   :3456      │  │   /slack-connect             │    │  │
    │  │  │              │  │   /matrix-connect            │    │  │
    │  │  └──────────────┘  └──────────────────────────────┘    │  │
    │  └────────────────────────────────────────────────────────┘  │
    │                                                               │
    └──────────────────────────────────────────────────────────────┘
```

### Repository Map

| Repository | Purpose | Key Files |
|------------|---------|-----------|
| `factumerit/backend` | Bot server (MCP, Slack, Matrix) | `src/vikunja_mcp/server.py` |
| `factumerit-matrix` | Synapse + MAS + Element Web | `Dockerfile`, `nginx.conf`, `start.sh` |
| `vikunja-factumerit` | Vikunja config + OAuth pages | `connect.html`, `matrix-connect.html` |
| `spawn-solutions` | Beads, analyses, scripts | `scripts/`, `analyses/factumerit/` |

---

## 2. OAuth Flows

### 2.1 Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         OAUTH CONNECT FLOW                                │
│                                                                           │
│  ┌────────────┐                                                          │
│  │    User    │                                                          │
│  │ (Slack or  │                                                          │
│  │  Matrix)   │                                                          │
│  └─────┬──────┘                                                          │
│        │                                                                  │
│        │ 1. Send message to bot                                          │
│        ▼                                                                  │
│  ┌─────────────────┐                                                     │
│  │ vikunja-slack-bot│                                                    │
│  │                  │                                                    │
│  │ 2. Create nonce  │                                                    │
│  │    (in-memory)   │                                                    │
│  │                  │                                                    │
│  │ 3. Return link   │                                                    │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           │ https://vikunja.factumerit.app/{platform}-connect?state={nonce}
│           ▼                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    vikunja (static pages)                         │   │
│  │                                                                   │   │
│  │  connect.html / matrix-connect.html                               │   │
│  │                                                                   │   │
│  │  4. Check localStorage for existing JWT                           │   │
│  │     ├─ If JWT exists: Skip to step 7                              │   │
│  │     └─ If no JWT: Continue to step 5                              │   │
│  │                                                                   │   │
│  │  5. Open popup to /login (Vikunja OIDC)                          │   │
│  │                                                                   │   │
│  └────────────────────────────────┬──────────────────────────────────┘   │
│                                   │                                      │
│                                   ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                  OIDC Provider (varies by platform)                │  │
│  │                                                                    │  │
│  │  Slack users:  /auth/openid/slack  → Slack OAuth                  │  │
│  │  Matrix users: /auth/openid/factumerit → MAS                      │  │
│  │                                                                    │  │
│  │  6. User authenticates with platform credentials                  │  │
│  │     → JWT stored in localStorage                                   │  │
│  └────────────────────────────────┬───────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                    connect.html (continued)                        │  │
│  │                                                                    │  │
│  │  7. Call Vikunja API with JWT from localStorage:                  │  │
│  │     POST /api/v1/tokens                                           │  │
│  │     → Creates API token (tk_xxx)                                  │  │
│  │                                                                    │  │
│  │  8. Redirect to bot callback with token                           │  │
│  │     https://vikunja-slack-bot.onrender.com/vikunja-callback       │  │
│  │     ?state={nonce}&token=tk_xxx&email={email}                     │  │
│  └────────────────────────────────┬───────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  ┌─────────────────┐                                                     │
│  │ vikunja-slack-bot│                                                    │
│  │                  │                                                    │
│  │ 9. Validate nonce│  ←── SECURITY BUG: Token belongs to                │
│  │    (in-memory)   │      whichever user was logged into browser        │
│  │                  │                                                    │
│  │ 10. Store token  │                                                    │
│  │     for user_id  │                                                    │
│  │                  │                                                    │
│  │ 11. Send DM      │                                                    │
│  │     confirmation │                                                    │
│  └──────────────────┘                                                    │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.2 The Security Bug (solutions-56u9)

**Critical Issue**: OAuth creates tokens under WRONG user account

**Root Cause**:
1. Connect page (`matrix-connect.html`) checks `localStorage.getItem('token')` for existing JWT
2. If ANY user is logged into Vikunja in that browser, the page uses THEIR JWT
3. New API token is created for the already-logged-in user, not the Matrix user
4. Bot stores this token mapped to the Matrix user who clicked the link
5. Matrix user now sees tasks belonging to the browser-logged-in user

**Reproduction**:
1. Admin (i2) logs into vikunja.factumerit.app in browser
2. New user (Latin Trainer) sends message to Matrix bot
3. Latin Trainer clicks OAuth link in SAME browser
4. connect.html finds i2's JWT in localStorage
5. Creates API token for i2
6. Bot stores i2's token under Latin Trainer's Matrix ID
7. Latin Trainer sees i2's 256 tasks!

**Impact**: HIGH - Users see other users' tasks

**Current Workarounds**:
1. Use incognito/private browsing for OAuth
2. Manually create token in Vikunja Settings and use `!vik <token>`
3. Use `!vik disconnect` to clear and reconnect

**Proposed Fixes**:
1. Clear localStorage before starting OAuth flow (breaks existing sessions)
2. Pass user context through entire flow (complex)
3. Add nonce-user verification on API token creation (requires Vikunja changes)
4. Switch to direct API token creation flow (no browser session)

### 2.3 Slack vs Matrix OAuth Comparison

| Aspect | Slack | Matrix |
|--------|-------|--------|
| OIDC Provider | Slack OAuth (`/auth/openid/slack`) | MAS (`/auth/openid/factumerit`) |
| Connect Page | `connect.html` | `matrix-connect.html` |
| Token Prefix | `slack-bot-{nonce}` | `matrix-bot-{nonce}` |
| Working? | Yes (separate browser sessions) | Bug (shared browser sessions) |

---

## 3. Token Types & Storage

### 3.1 Token Type Matrix

| Token | Prefix | Generated By | Stored In | Used For |
|-------|--------|--------------|-----------|----------|
| Matrix Access Token | `syt_` | Element login | Element client | Synapse Client API, Admin API |
| MAS Compatibility Token | `mat_` | `mas manage` CLI | MAS database | Bot login, limited Synapse |
| Vikunja API Token | `tk_` | Vikunja Settings or OAuth | Bot config.yaml | Vikunja API operations |
| Pending Connection Nonce | random | `secrets.token_urlsafe(24)` | Bot in-memory | OAuth flow state |

### 3.2 User Token Storage

**Bot User Tokens** (`/data/config/config.yaml`):
```yaml
users:
  "@i2:matrix.factumerit.app":
    vikunja_token: "tk_xxx"  # Plaintext (!)
    welcomed: true
    model: "haiku"

  "U12345ABC":  # Slack user
    vikunja_token: "tk_yyy"
```

**Security Issues**:
- Tokens stored in plaintext (no encryption at rest)
- File permissions: 644 (should be 600)
- No token rotation mechanism
- No token encryption key in environment

### 3.3 Token Flow Diagram

```
                    MATRIX USER IDENTITY FLOW

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Matrix User   │    │    MAS OIDC     │    │    Vikunja      │
│                 │    │                 │    │                 │
│ @alice:matrix.  │    │ Authenticates   │    │ Creates account │
│ factumerit.app  │    │ Matrix identity │    │ alice@...       │
│                 │    │                 │    │                 │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         │ 1. DM bot            │                      │
         ├──────────────────────►                      │
         │                      │                      │
         │ 2. Click OAuth link  │                      │
         ├─────────────────────────────────────────────►
         │                      │                      │
         │ 3. Login with Matrix │                      │
         ├──────────────────────►                      │
         │                      │                      │
         │     4. OIDC callback │                      │
         │◄─────────────────────┤                      │
         │                      │                      │
         │ 5. Create API token  │                      │
         ├─────────────────────────────────────────────►
         │                      │                      │
         │     6. Token tk_xxx  │                      │
         │◄────────────────────────────────────────────┤
         │                      │                      │
         │ 7. Store mapping:    │                      │
         │    @alice → tk_xxx   │                      │
         │                      │                      │

NOTE: Step 3 is where the BUG occurs - if a different user's
JWT is in localStorage, their identity is used instead.
```

---

## 4. Failure Modes

### 4.1 Known Failure Modes

| Failure Mode | Cause | Impact | Recovery |
|--------------|-------|--------|----------|
| **OAuth token mismatch** | Shared browser session | User sees wrong tasks | `!vik disconnect`, reconnect in incognito |
| **Nonce expired** | Bot restart during OAuth | "Connection request expired" | Click link again |
| **Bot not responding** | E2EE accidentally enabled | Silent failure | Verify E2EE disabled in code |
| **"Token is not active"** | Using `mat_` token for admin API | Admin API fails | Use `syt_` token from Element |
| **Matrix sync timeout** | Slow homeserver, network issues | Missed messages | Bot auto-reconnects |

### 4.2 In-Memory State (Lost on Restart)

The following state is lost when the bot restarts:
- **Pending OAuth connections** (`_pending_connections` dict)
- **Rate limiting counters**
- **ECO streak counters**
- **Cached room DM mappings**

### 4.3 Nonce Expiry Timeline

```
Time →
├────────────────────────────────────────────────────────────────────►
│
│  [0s] User sends message to bot
│       └─ Bot creates nonce (5-minute TTL)
│       └─ Returns OAuth link with nonce
│
│  [30s] User clicks link
│        └─ Nonce valid, OAuth flow starts
│
│  [2m] User completes OIDC login
│       └─ Nonce still valid
│
│  [3m] API token created
│       └─ Callback to bot with nonce
│       └─ Nonce consumed, connection stored
│
│  [5m] Nonce expires (if not used)
│       └─ Automatic cleanup
│
│  [RESTART] Bot restarts
│            └─ ALL nonces lost (in-memory)
│            └─ User must request new link
```

---

## 5. Security Model

### 5.1 Authentication Layers

```
Layer 1: Network (TLS)
│
├─ All traffic encrypted in transit
├─ Render terminates TLS at edge
└─ Internal traffic over private network

Layer 2: Platform Identity
│
├─ Matrix: Synapse authenticates via MAS (OIDC delegation)
├─ Slack: Slack OAuth + signing secret verification
└─ Bot trusts platform-provided user IDs

Layer 3: Admin Authorization
│
├─ ADMIN_IDS environment variable (comma-separated)
├─ Admin commands: !credits, admin_set_user_token, etc.
└─ Implemented in: _is_admin() function

Layer 4: Vikunja Token Scope
│
├─ User's Vikunja token limits what bot can do
├─ Token created with all permissions (via OAuth)
└─ No cross-account access (each user has own token)
```

### 5.2 Secrets Inventory

| Secret | Location | Access |
|--------|----------|--------|
| `MATRIX_PASSWORD` | Render env var | Bot login |
| `ANTHROPIC_API_KEY` | Render env var | Claude API |
| `SLACK_BOT_TOKEN` | Render env var | Slack API |
| `VIKUNJA_TOKEN` | Render env var | Fallback API token |
| `MAS_HOMESERVER_SECRET` | Render env var | Synapse-MAS auth |
| User Vikunja tokens | `/data/config/config.yaml` | Bot config file |

### 5.3 E2EE Status

**Decision**: E2EE disabled for V1

**Implementation**: Hardcoded in `matrix_client.py:58`:
```python
config = AsyncClientConfig(encryption_enabled=False)
```

**Rationale**:
- Bot cannot read encrypted rooms without device verification
- Device verification adds UX friction
- We control the homeserver
- Task data is not highly sensitive

**Risk**: If accidentally enabled, bot silently fails.

---

## 6. Deployment Architecture

### 6.1 Render Services

| Service | Type | Plan | Disk | Port |
|---------|------|------|------|------|
| factumerit-matrix | Web | Starter ($7) | 3GB | 10000 |
| vikunja-slack-bot | Web | Starter ($7) | 1GB | $PORT |
| vikunja | Web | Starter ($7) | 10GB | 3456 |
| factumerit-db | PostgreSQL | Basic ($9) | N/A | 5432 |

**Total**: ~$30-40/month

### 6.2 factumerit-matrix Container

```
┌─────────────────────────────────────────────────────┐
│              Docker Container (Render)               │
│                                                      │
│  ┌─────────────────────────────────────────────────┐│
│  │               supervisord (PID 1)                ││
│  │                                                  ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      ││
│  │  │  nginx   │  │  synapse │  │   mas    │      ││
│  │  │ (pri 100)│  │ (pri 200)│  │ (pri 200)│      ││
│  │  └──────────┘  └──────────┘  └──────────┘      ││
│  │                                                  ││
│  └─────────────────────────────────────────────────┘│
│                                                      │
│  /data/                                              │
│  ├── synapse/                                        │
│  │   ├── homeserver.yaml                            │
│  │   ├── signing.key                                │
│  │   └── media_store/                               │
│  └── mas/                                            │
│      ├── signing_key.pem                            │
│      └── encryption_secret                          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 6.3 vikunja Container

```
┌─────────────────────────────────────────────────────┐
│              Docker Container (Render)               │
│                                                      │
│  ┌─────────────────────────────────────────────────┐│
│  │               nginx (custom config)              ││
│  │                                                  ││
│  │  Static files:                                   ││
│  │  ├── /slack-connect  → connect.html             ││
│  │  ├── /matrix-connect → matrix-connect.html      ││
│  │  └── /*              → Vikunja :3456            ││
│  │                                                  ││
│  └─────────────────────────────────────────────────┘│
│                                                      │
│  ┌─────────────────────────────────────────────────┐│
│  │               Vikunja (:3456)                    ││
│  │                                                  ││
│  │  OIDC Providers:                                 ││
│  │  ├── /auth/openid/slack      (Slack OAuth)      ││
│  │  └── /auth/openid/factumerit (MAS)              ││
│  │                                                  ││
│  └─────────────────────────────────────────────────┘│
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 7. Data Flows

### 7.1 Matrix Message Flow

```
User                Bot                 Claude          Vikunja
 │                   │                    │               │
 │ "what's overdue?" │                    │               │
 │──────────────────►│                    │               │
 │                   │                    │               │
 │                   │ Get user token     │               │
 │                   │ from config.yaml   │               │
 │                   │                    │               │
 │                   │ Parse message      │               │
 │                   │──────────────────► │               │
 │                   │                    │               │
 │                   │ Tool: list_all_tasks               │
 │                   │ filter=overdue     │               │
 │                   │◄───────────────────│               │
 │                   │                    │               │
 │                   │ GET /api/v1/tasks?filter=overdue   │
 │                   │────────────────────────────────────►│
 │                   │                    │               │
 │                   │ [task1, task2, task3]              │
 │                   │◄───────────────────────────────────│
 │                   │                    │               │
 │ "You have 3..."   │                    │               │
 │◄──────────────────│                    │               │
```

### 7.2 ECO Mode (No LLM)

```
User                Bot                 Vikunja
 │                   │                    │
 │ "!oops"           │                    │
 │──────────────────►│                    │
 │                   │                    │
 │                   │ RapidFuzz match:   │
 │                   │ "oops" → "overdue" │
 │                   │ (no Claude call)   │
 │                   │                    │
 │                   │ GET /api/v1/tasks  │
 │                   │────────────────────►│
 │                   │                    │
 │                   │ [tasks...]         │
 │                   │◄───────────────────│
 │                   │                    │
 │ "Overdue tasks:"  │                    │
 │◄──────────────────│                    │
```

---

## 8. Action Items (P0)

### Security Fixes Required

1. **solutions-56u9**: Fix OAuth browser session bug
   - Clear localStorage before OAuth flow, OR
   - Implement server-side user verification

2. **Persistent Nonces**: Store nonces in database/Redis
   - Currently in-memory, lost on restart
   - Users get "expired nonce" after deploys

3. **Token Encryption**: Encrypt user tokens in config.yaml
   - Currently plaintext on disk
   - Use Fernet with key from env var

### Documentation Needed

4. **Archive Outdated Docs**: Red-tag these as superseded:
   - `analyses/factumerit/25-ARCHITECTURE.md` (mentions Dendrite)
   - Any doc describing MAS-less setup

5. **Admin Tooling**: Document/create:
   - User token inspection tool
   - OAuth flow debugging tool
   - Nonce status checker

---

## 9. References

### Internal Docs
- `docs/MATRIX_ADMIN_GUIDE.md` - Admin operations
- `docs/MATRIX_TOKEN_TYPES.md` - Token type reference
- `backend/docs/MATRIX_SECURITY.md` - Security model
- `vikunja-factumerit/OAUTH_CONNECT_FLOW.md` - OAuth flow details

### Related Beads
- solutions-56u9: OAuth security bug (P0)
- solutions-hwgt: This architecture review (P0)
- solutions-3pf7: Validate E2EE disabled
- solutions-w90d: Token encryption

### External
- [Synapse Admin API](https://matrix-org.github.io/synapse/latest/usage/administration/admin_api/)
- [MAS Documentation](https://github.com/matrix-org/matrix-authentication-service)
- [Vikunja API](https://vikunja.io/docs/api/)

---

**Last Updated**: 2025-12-27
**Author**: Claude Code (solutions-hwgt)
