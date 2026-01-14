# Factumerit Email Interface: Architecture Explainer

**Target Audience**: Developers working on Factumerit, future maintainers, Ivan (for context recovery)
**Business Impact**: Email becomes a complete parallel interface to Vikunja—users can interact with @eis without ever opening the UI
**Purpose**: This EXPLAINER documents the architecture for email-driven task management, covering both **outbound** (action links) and **inbound** (reply-to-interact) flows.

---

## Email Interface Overview

Factumerit's email interface works in both directions:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FACTUMERIT EMAIL INTERFACE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   OUTBOUND (Action Links)              INBOUND (Reply-to-Interact)          │
│   ─────────────────────                ───────────────────────────          │
│                                                                             │
│   @eis queues project                  User receives email from @eis        │
│        │                                     │                              │
│        ▼                                     ▼                              │
│   Email with signed action links       User hits "Reply" and types          │
│   [Approve] [Cancel] [Snooze]          "What's the weather in Seattle?"     │
│        │                                     │                              │
│        ▼                                     ▼                              │
│   User clicks link                     Resend webhook → /webhooks/resend    │
│        │                                     │                              │
│        ▼                                     ▼                              │
│   /do/{token} validates & executes     Parse reply → route to @eis          │
│        │                                     │                              │
│        ▼                                     ▼                              │
│   Action completed, success page       @eis response sent via email         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Strategic Value**: A user who never opens Vikunja but manages tasks entirely through email is still a productive Factumerit user. This is a differentiator—Vikunja Cloud doesn't have this.

---

## What Problem Does This Solve?

**Simple Definition**: The Email Action Service lets users interact with Vikunja through email links instead of the web UI. Click a link in an email → action happens in Vikunja → done. No login required.

**The Current Limitation**: Factumerit already has an approval queue system for bot-created projects. When @eis creates a project, the user gets a link to approve it. But this link only works if the user is already logged into Vikunja (it reads the JWT from localStorage). Email delivery breaks this assumption—users clicking from email won't have a Vikunja session.

**Why This Matters**:
- Email is push (arrives in inbox), Vikunja UI is pull (user must visit)
- Users can take action from phone, different device, without logging in
- Opens up new interaction patterns: daily digests with "mark done" buttons, reminder snooze links, one-click approvals
- Reduces friction for casual users who don't want another app open

**Strategic Value**: This is a potential differentiator. Vikunja Cloud doesn't have this. A user who never opens Vikunja but manages tasks entirely through email is still a productive Factumerit user.

---

## How It Works: Signed Action Tokens

### The Core Pattern

```
┌──────────────────────────────────────────────────────────────────┐
│  1. EVENT TRIGGERS EMAIL                                         │
│     (project queued, task due, bot notification, etc.)           │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  2. GENERATE SIGNED ACTION URL                                   │
│                                                                  │
│     payload = {                                                  │
│       "a": "approve_project",    // action type                  │
│       "r": 42,                   // resource ID                  │
│       "u": "vikunja:alice",      // user ID                      │
│       "x": 1704153600            // expiration (unix timestamp)  │
│     }                                                            │
│                                                                  │
│     token = base64url(payload) + "." + hmac_sha256(payload, KEY) │
│     url = https://mcp.factumerit.app/do/{token}                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  3. EMAIL DELIVERED                                              │
│                                                                  │
│     Subject: "Your new project is ready"                         │
│     Body: "Click here to create: [Create Project]"               │
│            "Changed your mind? [Cancel]"                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  4. USER CLICKS LINK                                             │
│                                                                  │
│     GET /do/eyJhIjoiYXBwcm92ZS4uLn0.a1b2c3d4                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  5. /do/{token} ENDPOINT VALIDATES & EXECUTES                    │
│                                                                  │
│     a. Decode base64 payload                                     │
│     b. Verify HMAC signature (tamper protection)                 │
│     c. Check expiration timestamp                                │
│     d. Look up user's stored Vikunja token from database         │
│     e. Execute action using user's token                         │
│     f. Return success page (or redirect to Vikunja)              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Why Signed Tokens?

| Approach | Pros | Cons |
|----------|------|------|
| **Session-based (current)** | Simple, uses existing auth | Requires user to be logged in |
| **Magic links (login first)** | Secure | Extra friction, user must login |
| **Signed action tokens** | One-click, no login needed | Requires token management |

Signed tokens win because:
1. **Zero friction**: Click → done. No login page.
2. **Self-contained**: Token carries all info needed to execute action
3. **Secure**: HMAC signature prevents tampering, expiration prevents replay
4. **Auditable**: Can log which token was used, when, from where

---

## Existing Infrastructure We're Building On

### Already Built

| Component | Location | Purpose |
|-----------|----------|---------|
| **Project approval queue** | `server.py:11937` `/project-queue` | Stores pending projects, tracks status |
| **Queue processor page** | `static/project-queue-processor.html` | JS page that creates projects with user's session |
| **Approval links** | `server.py:15020` | Generates `?id={queue_id}` URLs |
| **User token storage** | `personal_bots` table | Stores user's Vikunja JWT for bot operations |
| **Email service** | `email_service.py` | Resend integration, branded templates |
| **Signing key** | `TOKEN_ENCRYPTION_KEY` env var | Fernet key, can derive HMAC key |

### What We Add

| Component | Purpose |
|-----------|---------|
| **Token generator** | `create_action_url(action, user_id, resource_id)` |
| **Action executor endpoint** | `GET /do/{token}` - validates and executes |
| **Action registry** | Maps action types to handler functions |
| **Email templates** | Branded HTML with action buttons |

### Database Tables Involved

```
personal_bots
├── user_id              (e.g., "vikunja:alice")
├── owner_vikunja_token  (encrypted JWT for executing actions)
├── owner_vikunja_user_id (Vikunja numeric user ID)
└── ...

project_creation_queue
├── id                   (queue entry ID, used as resource_id)
├── username             (Vikunja username)
├── status               (pending/processing/complete)
├── projects             (JSONB of project specs)
└── ...

factumerit_users
├── user_id              (e.g., "vikunja:alice")
├── email                (for sending emails)
└── ...
```

---

## Action Types & Handlers

### Initial Actions (MVP)

```python
ACTIONS = {
    # Project queue actions (existing flow, new delivery channel)
    "approve_project": {
        "handler": execute_approve_project,
        "resource": "queue_id",
        "description": "Create queued project(s) in user's account",
    },
    "cancel_project": {
        "handler": execute_cancel_project,
        "resource": "queue_id",
        "description": "Cancel queued project creation request",
    },

    # Task actions (new)
    "complete_task": {
        "handler": execute_complete_task,
        "resource": "task_id",
        "description": "Mark a task as done",
    },
}
```

### Future Actions

```python
    # Reminder actions
    "snooze_task": {
        "handler": execute_snooze_task,
        "resource": "task_id",
        "params": ["days"],  # extra param in token
        "description": "Snooze task reminder by N days",
    },

    # Digest actions
    "view_task": {
        "handler": execute_view_task,
        "resource": "task_id",
        "description": "Redirect to task in Vikunja",
    },

    # Bot notification actions
    "approve_changes": {
        "handler": execute_approve_changes,
        "resource": "change_request_id",
        "description": "Approve bot-suggested changes",
    },

    # Account actions
    "unsubscribe": {
        "handler": execute_unsubscribe,
        "resource": "email_type",
        "description": "Unsubscribe from email type",
    },
```

---

## Token Structure

### Payload Schema

```json
{
  "a": "approve_project",     // action (required)
  "r": 123,                   // resource_id (required)
  "u": "vikunja:alice",       // user_id (required)
  "x": 1704153600,            // expires unix timestamp (required)
  "d": 3                      // extra data (optional, action-specific)
}
```

### URL Format

```
https://mcp.factumerit.app/do/{base64url_payload}.{signature}
```

Example:
```
https://mcp.factumerit.app/do/eyJhIjoiYXBwcm92ZV9wcm9qZWN0IiwiciI6NDIsInUiOiJ2aWt1bmphOmFsaWNlIiwieCI6MTcwNDE1MzYwMH0.a1b2c3d4e5f6
```

### Signature

```python
signature = hmac.new(
    key=derive_key(TOKEN_ENCRYPTION_KEY, b"email-actions"),
    msg=base64url_payload.encode(),
    digestmod=hashlib.sha256
).hexdigest()[:16]  # truncated for shorter URLs
```

Why truncate to 16 chars?
- 64 bits of security is sufficient for short-lived tokens
- Combined with expiration + rate limiting, brute force is impractical
- Shorter URLs are more email-friendly (less likely to wrap/break)

---

## Email Templates

### Branded HTML Structure

```html
<!-- Base template (all emails) -->
<div style="font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto;">
  <!-- Header -->
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">Factumerit</h1>
  </div>

  <!-- Content (varies by email type) -->
  <div style="padding: 30px; background: white;">
    {{ content }}
  </div>

  <!-- Footer -->
  <div style="padding: 20px; background: #f5f5f5; text-align: center; font-size: 12px; color: #666;">
    <p>You're receiving this because you have a Factumerit account.</p>
    <p><a href="{{ unsubscribe_url }}">Unsubscribe</a> from these emails</p>
  </div>
</div>
```

### Email Types

| Type | Trigger | Content |
|------|---------|---------|
| **Welcome** | User signup | Password, "Create your first project" button |
| **Project Ready** | Bot queues project | Project name, Approve/Cancel buttons |
| **Daily Digest** | Scheduled (morning) | Due today list, each with "Done" button |
| **Task Reminder** | Task due soon | Task details, Done/Snooze buttons |
| **Bot Notification** | @eis mentions user | Bot message, action buttons |

---

## Security Model

### Threat Analysis

| Threat | Mitigation |
|--------|------------|
| **Token forgery** | HMAC signature verification |
| **Token replay** | Expiration timestamp (72h default) |
| **Token leakage** | Short expiration, action-specific scope |
| **Brute force** | Rate limiting on /do/ endpoint |
| **Wrong user** | user_id in payload, verified against stored token |
| **Privilege escalation** | Action handlers verify user owns resource |

### Token Lifecycle

```
Generate → Email → Click → Validate → Execute → (optionally mark used)
   │                           │
   │                           └── If invalid: error page
   │
   └── Expires after 72 hours (configurable per action type)
```

### Rate Limiting

```python
# /do/ endpoint rate limits
RATE_LIMITS = {
    "per_ip": "100/hour",      # Prevent scanning from single IP
    "per_user": "50/hour",     # Prevent abuse of single user's tokens
    "global": "10000/hour",    # System-wide protection
}
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (MVP for AI Tinkerers)

**Goal**: Replace Vikunja's welcome email with branded Factumerit email containing password + action link

1. **Token generator function** - `create_action_url()`
2. **/do/{token} endpoint** - validate, look up user token, execute
3. **approve_project handler** - reuse existing queue logic
4. **Welcome email template** - password + "Create first project" button

**Files to create/modify**:
- `src/vikunja_mcp/email_actions.py` (new) - token gen, action registry
- `src/vikunja_mcp/server.py` - add /do/ endpoint
- `src/vikunja_mcp/email_service.py` - add welcome template
- `src/vikunja_mcp/signup_workflow.py` - send welcome email with action link

### Phase 2: Task Actions

1. **complete_task handler**
2. **snooze_task handler** (with days parameter)
3. **Daily digest email** - scheduled job, lists tasks due today with action buttons

### Phase 3: Bot Integration

1. **Modify bot response flow** - option to notify via email instead of/in addition to Vikunja comment
2. **Bot notification email template**
3. **approve_changes handler** for bot-suggested modifications

### Phase 4: User Preferences

1. **Email preferences in factumerit_users** - which emails to receive
2. **Unsubscribe handling** - per email type
3. **Digest frequency settings** - daily/weekly/off

---

## How This Connects to Existing Code

### Current Flow (Vikunja UI Required)

```
@eis request
    → bot queues project (project_creation_queue table)
    → bot posts comment with approve link
    → user clicks link in Vikunja
    → /queue page loads
    → JS reads JWT from localStorage
    → JS calls Vikunja API
    → project created
```

### New Flow (Email, No UI Required)

```
@eis request
    → bot queues project (same table)
    → bot triggers email with signed action link
    → user clicks link in email
    → /do/{token} endpoint
    → server validates token
    → server retrieves user's stored JWT
    → server calls Vikunja API
    → project created
    → success page shown
```

### Key Difference

| Aspect | Current | Email Action |
|--------|---------|--------------|
| **Auth source** | localStorage JWT | Stored JWT in personal_bots table |
| **Execution** | Client-side JS | Server-side Python |
| **Requires login** | Yes | No |
| **Delivery channel** | Vikunja comment | Email |

---

## Testing Strategy

### Unit Tests

```python
def test_token_generation():
    url = create_action_url("approve_project", "vikunja:alice", 42)
    assert "mcp.factumerit.app/do/" in url

def test_token_validation():
    url = create_action_url("approve_project", "vikunja:alice", 42)
    token = url.split("/do/")[1]
    payload = validate_action_token(token)
    assert payload["a"] == "approve_project"
    assert payload["u"] == "vikunja:alice"

def test_expired_token():
    url = create_action_url("approve_project", "vikunja:alice", 42, expires_in=-1)
    token = url.split("/do/")[1]
    with pytest.raises(TokenExpiredError):
        validate_action_token(token)

def test_tampered_token():
    url = create_action_url("approve_project", "vikunja:alice", 42)
    token = url.split("/do/")[1]
    tampered = token[:-1] + "X"  # Change last char
    with pytest.raises(InvalidSignatureError):
        validate_action_token(tampered)
```

### Integration Tests

```python
def test_approve_project_via_email_action():
    # Setup: queue a project
    queue_id = create_test_queue_entry("vikunja:testuser", "Test Project")

    # Generate action URL
    url = create_action_url("approve_project", "vikunja:testuser", queue_id)

    # Simulate click
    response = client.get(url.replace("https://mcp.factumerit.app", ""))

    # Verify project was created
    assert response.status_code == 200
    assert "created" in response.text.lower()

    # Verify queue entry marked complete
    entry = get_queue_entry(queue_id)
    assert entry["status"] == "complete"
```

---

## Configuration

### Environment Variables

```bash
# Existing (already configured)
TOKEN_ENCRYPTION_KEY=...        # Used to derive HMAC key
RESEND_API_KEY=...              # Email sending
VIKUNJA_URL=...                 # Vikunja instance

# New
EMAIL_ACTION_DEFAULT_EXPIRY=259200    # 72 hours in seconds
EMAIL_ACTION_RATE_LIMIT_PER_IP=100    # Per hour
MCP_PUBLIC_URL=https://mcp.factumerit.app  # For generating links
```

### Vikunja Configuration Change

```bash
# On Render: factumerit-vikunja service
VIKUNJA_MAILER_ENABLED=false    # Disable Vikunja's emails
```

---

## Glossary

| Term | Definition |
|------|------------|
| **Action token** | Signed, self-contained URL parameter that authorizes a specific action |
| **HMAC** | Hash-based Message Authentication Code - cryptographic signature |
| **Payload** | JSON data encoded in the token (action, resource, user, expiration) |
| **Resource ID** | The ID of the thing being acted on (queue_id, task_id, etc.) |
| **Stored token** | User's Vikunja JWT saved in personal_bots table during signup |

---

## Related Files

| File | Purpose |
|------|---------|
| `src/vikunja_mcp/server.py` | Main server, will host /do/ endpoint |
| `src/vikunja_mcp/email_service.py` | Resend integration, template rendering |
| `src/vikunja_mcp/signup_workflow.py` | User signup flow, will trigger welcome email |
| `src/vikunja_mcp/bot_provisioning.py` | Stores user tokens we'll use for actions |
| `src/vikunja_mcp/token_broker.py` | Database access, encryption utilities |
| `static/project-queue-processor.html` | Existing queue UI (reference for success pages) |

---

## FAQ

**Q: What if the user's stored token expires?**
A: We store JWT tokens which have long expiry (configured in Vikunja). If expired, action fails gracefully with "Please log in to complete this action" and link to Vikunja.

**Q: Can someone guess/brute-force tokens?**
A: Impractical. 16-char hex signature = 64 bits. At 1000 guesses/second, would take ~585 million years. Plus rate limiting kicks in after 100 attempts/hour.

**Q: What if an email is forwarded?**
A: The action link still works (it's self-contained). But it executes as the original user. This is intentional—delegation is fine for most actions. For sensitive actions, we could add email verification.

**Q: How do we handle action failures?**
A: Show a friendly error page with explanation and "Contact Support" link. Log the failure for debugging. Never expose internal errors.

**Q: Can we revoke a token?**
A: Not directly (they're stateless). But we can: (1) change the signing key (revokes ALL tokens), (2) delete the queue entry (action fails with "not found"), (3) mark user inactive (action fails with "account inactive").

---

---

## Part 2: Inbound Email (Reply-to-Interact)

**Bead**: fa-4mda.1
**Status**: Implemented (Jan 2026)

### What Problem Does Inbound Email Solve?

**Simple Definition**: Users can interact with @eis by simply replying to any email from Factumerit. Type a question, hit send, get an answer back. The AI assistant lives in your inbox.

**In Business Terms**: Think of it like having a personal assistant who monitors a shared email inbox. You don't need to open a special app or remember a website—you just email them like you would a colleague. They read your message, do the work, and email you back.

**The Friction We're Eliminating**:
- **No new app to learn**: Every email client works (Gmail, Outlook, Apple Mail, phone)
- **No login required**: Your email address is your identity
- **No context switching**: Stay in your inbox where you already spend time
- **No special syntax**: Just write naturally, like talking to a person

**Why This Is Strategically Valuable**:

Email is the lowest common denominator of digital communication. *Everyone* has email. Not everyone wants another app, another login, another thing to check. By making @eis available through email, we meet users where they already are.

Consider the personas this unlocks:
- **The email-first executive**: Lives in Outlook, delegates via email, rarely opens task apps
- **The mobile-only user**: Manages everything from phone, apps are friction
- **The casual user**: Tried Vikunja once, never went back—but still gets emails
- **The delegator**: Forwards emails to @eis: "schedule this" or "remind me about this"

**In Finance Terms**: This is like offering a phone-based concierge service instead of only having a web portal. Some customers prefer the portal (Vikunja UI). Some prefer to just call (email). Supporting both maximizes addressable market without forcing anyone to change their workflow.

---

### How Inbound Email Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. USER REPLIES TO EMAIL                                                   │
│                                                                             │
│     To: eis@factumerit.app                                                  │
│     Subject: Re: Welcome to Factumerit!                                     │
│     Body: What's the weather in Seattle?                                    │
│                                                                             │
│           On Jan 8, eis wrote:                                              │
│           > Welcome to Factumerit!                                          │
│           > Your account is ready.                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. RESEND RECEIVES EMAIL                                                   │
│                                                                             │
│     Resend's inbound servers receive the email and send webhook             │
│     POST /webhooks/resend with event type "email.received"                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. WEBHOOK HANDLER PROCESSES                                               │
│                                                                             │
│     a. Verify Svix signature (security)                                     │
│     b. Fetch full email content via Resend API                              │
│     c. Parse reply to extract user's message (strip quoted text)            │
│     d. Look up sender email → Vikunja user                                  │
│     e. Route to CommandParser → KeywordHandlers                             │
│     f. Get response from @eis                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. RESPONSE EMAIL SENT                                                     │
│                                                                             │
│     To: user@example.com                                                    │
│     Subject: Re: Welcome to Factumerit!                                     │
│     In-Reply-To: <original-message-id>   ← Threading header                 │
│     Body: Currently 52°F and cloudy in Seattle...                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Inbound Email Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **Webhook endpoint** | `server.py` `/webhooks/resend` | Receives Resend webhooks |
| **Email handler** | `email_inbound.py` | Orchestrates the flow |
| **Webhook verifier** | `verify_resend_webhook()` | Validates Svix signatures |
| **Email fetcher** | `fetch_email_content()` | Gets body via Resend API |
| **Reply parser** | `parse_reply_text()` | Strips quoted text |
| **User mapper** | `lookup_user_by_email()` | Email → Vikunja user |
| **Response sender** | `send_response_email()` | Sends with threading headers |

---

### Reply Parsing

The parser handles common email client formats:

| Format | Pattern | Example |
|--------|---------|---------|
| Quoted lines | `>` prefix | `> previous message` |
| Gmail | `On ... wrote:` | `On Mon, Jan 8, 2025 at 10:00 AM eis wrote:` |
| Outlook | `From: ... Sent: ...` | `From: eis\nSent: Monday...` |
| Forwarded | `---------- Forwarded` | Gmail forward separator |
| Signatures | `-- ` | Double dash signature delimiter |

**Example Input**:
```
What's the weather in Seattle?

On Mon, Jan 8, 2025 at 10:00 AM eis <eis@factumerit.app> wrote:
> Welcome to Factumerit!
>
> Your account is ready.
```

**Extracted Message**: `What's the weather in Seattle?`

---

### Email Threading

Response emails include proper headers for threading:

```
In-Reply-To: <original-message-id@resend.dev>
References: <original-message-id@resend.dev>
```

This ensures responses appear in the same thread in Gmail, Outlook, Apple Mail, etc.

---

### Inbound Email Security

| Threat | Mitigation |
|--------|------------|
| **Spoofed webhooks** | Svix signature verification (HMAC-SHA256) |
| **Replay attacks** | Timestamp in signature |
| **Spam/abuse** | Sender must be registered user |
| **Rate limiting** | Inherits @eis budget system |
| **Unknown senders** | Ignored (logged for monitoring) |

---

### Inbound Email Configuration

#### Environment Variables

```bash
# Required
RESEND_API_KEY=re_...              # Same key used for sending

# Recommended
RESEND_WEBHOOK_SECRET=whsec_...    # Svix signing secret from Resend dashboard
```

#### Resend Dashboard Setup

1. Go to [Resend Dashboard](https://resend.com/webhooks) → Webhooks
2. Click "Add Webhook"
3. Endpoint URL: `https://mcp.factumerit.app/webhooks/resend`
4. Select event: `email.received`
5. Copy signing secret → `RESEND_WEBHOOK_SECRET`

#### Custom Domain Setup (factumerit.app)

For `eis@factumerit.app` to receive replies, we need to tell the internet "send emails for this address to Resend's servers." This is done via MX (Mail Exchange) records in DNS—the same system that routes email to Gmail or Outlook.

**The Complication**: If factumerit.app already receives email elsewhere (e.g., Google Workspace for hello@factumerit.app), adding Resend's MX record would interfere. MX records work by priority—email goes to the lowest number first.

**Option A: Subdomain (recommended if using existing email)**

Use `eis@reply.factumerit.app` instead of `eis@factumerit.app`:

1. Go to [Resend Dashboard → Domains](https://resend.com/domains)
2. Add subdomain: `reply.factumerit.app`
3. Enable "Receiving" for this subdomain
4. Copy the MX record shown (unique per account)
5. Add to DNS:
   ```
   Type: MX
   Host: reply
   Value: [copy from Resend dashboard]
   Priority: 10
   ```
6. Wait for verification (usually minutes, can take up to 48h)
7. Update `email_service.py` to send from `eis@reply.factumerit.app`

**Option B: Root domain (if not using email elsewhere)**

If factumerit.app doesn't receive email from another service:

1. Resend Dashboard → Domains → factumerit.app → Enable "Receiving"
2. Copy MX record and add to DNS at root (@)
3. Ensure Resend's priority is **lowest** (e.g., 10 if no others exist)

**Option C: Email forwarding (hybrid)**

Keep existing email, forward specific addresses to Resend:
- Configure `eis@factumerit.app` to forward to Resend's SMTP
- More complex but avoids MX record changes

**For development** (no DNS required):
- Use Resend's built-in domain: `<anything>@<team-id>.resend.app`
- Works immediately out of the box

See [Resend Custom Receiving Domains](https://resend.com/docs/dashboard/receiving/custom-domains) for detailed setup.

---

## Next Steps

After reading this explainer:

1. **Review the code locations** mentioned in "Related Files" section
2. **Check the existing queue flow** in `server.py:15001-15041` to see how links are generated today
3. **Look at email_service.py** to understand current Resend integration
4. **Review personal_bots table schema** in token_broker.py to understand stored credentials
5. **Check email_inbound.py** for the inbound email handling implementation

**Outbound Implementation**: Phase 1 (Core Infrastructure) complete
**Inbound Implementation**: Complete (fa-4mda.1)
