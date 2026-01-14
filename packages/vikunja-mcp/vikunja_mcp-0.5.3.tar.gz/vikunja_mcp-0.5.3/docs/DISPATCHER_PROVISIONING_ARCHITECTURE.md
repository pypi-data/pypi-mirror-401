# Dispatcher + Provisioning Architecture

## The Insight

Why does bot activation require Vikunja login?

**Current flow:**
1. Registration → creates user + bot credentials
2. Login → user authenticates to Vikunja
3. Activation → shares Inbox with @eis

The only reason for step 2-3 is "share project with bot" - a single DB row.

**Realization:** The bot exists independently. The credentials exist independently. Vikunja is just one frontend to a database.

## The Dispatcher Model

```
User                    Dispatcher              Backend
  │                         │                      │
  │  @eis !help             │                      │
  ├────────────────────────►│                      │
  │                         │  route by user_id    │
  │                         ├─────────────────────►│
  │                         │                      │ (personal bot creds)
  │                         │◄─────────────────────┤
  │◄────────────────────────┤                      │
  │  response               │                      │
```

- **One name** (`@eis`) - users never see ugly bot usernames
- **Many backends** - personal bot credentials provide isolation
- **Any database** - the pattern isn't Vikunja-specific

## Hands-Free Provisioning

Registration creates everything the user needs:

```
Email signup
    │
    ├──► Vikunja user (DB row)
    ├──► Personal bot (credentials table)
    ├──► Inbox project (DB row)
    ├──► Welcome task (DB row)
    └──► Email with credentials
```

No Vikunja API needed. Just DB writes.

## Beyond Tasks: SMCP Integration

SMCP (Supermodel Context Protocol) orchestrates MCP servers:

```
┌─────────────────────────────────────────────────────────┐
│                    SMCP Control Plane                    │
│  Paulina (Registry) │ Naomi (Bus) │ Kathy (Config)      │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────┐       ┌─────────┐       ┌─────────┐
   │ Vikunja │       │ Calendar│       │  CRM    │
   │   MCP   │       │   MCP   │       │   MCP   │
   └─────────┘       └─────────┘       └─────────┘
```

**The same provisioning pattern works for any service:**

```
Email signup
    │
    ├──► Vikunja user + bot
    ├──► Calendar user + credentials
    ├──► CRM user + credentials
    └──► Single email with all credentials
```

One registration. N services. One dispatcher.

## Architecture Layers

### Layer 1: Identity
- User account (email-based)
- Personal bot (credential isolation)
- Service-specific credentials

### Layer 2: Provisioning
- Hands-free: DB writes on registration
- In-app: Activation links for service-specific setup
- Cross-service: Same pattern, different DBs

### Layer 3: Dispatcher
- Single user-facing name (@eis)
- Routes by user identity
- Backend-agnostic

### Layer 4: Orchestration (SMCP)
- Service discovery (Paulina)
- Event routing (Naomi)
- Shared config (Kathy)
- Workflows (Judith)

## Implementation Progression

### Phase 1: Vikunja-Only (Current)
- Registration provisions Vikunja + personal bot
- @eis dispatcher routes to Vikunja
- Activation shares Inbox

### Phase 2: Multi-Database
- Registration provisions multiple DBs
- Same @eis, routes to appropriate backend
- "What's on my calendar?" → Calendar MCP
- "What tasks are due?" → Vikunja MCP

### Phase 3: SMCP Full
- Services discover each other
- Events flow between MCPs
- Workflows span services
- "When I complete a task, update CRM"

## The Abstraction

```
User sees:     @eis
               ────
Dispatcher:    Routes by user_id + intent
               ────
Backend:       Any database with:
               - User identity
               - Credential isolation
               - Data model
```

**The dispatcher doesn't care what's behind it.** It routes requests to the right backend based on:
1. Who's asking (user_id from notification)
2. What they're asking (intent from message)

## Factumerit ID

The natural endpoint: **one identity, many services**.

```
Factumerit ID: ivan@example.com
    │
    ├── Vikunja: tasks, projects, labels
    ├── Calendar: events, schedules
    ├── CRM: contacts, deals
    ├── Docs: files, notes
    └── ...
```

All accessible via `@eis`. All provisioned on registration.

## Key Principles

1. **DB-first provisioning** - Don't depend on app APIs for setup
2. **Credential isolation** - Each user's bot has its own credentials
3. **Single dispatcher** - Users interact with one name
4. **Backend-agnostic** - Same pattern works for any database
5. **SMCP orchestration** - Services communicate through the mesh

## Why This Matters

Traditional SaaS:
- Create account on Service A
- Create account on Service B
- Create account on Service C
- Remember N passwords
- N different UIs

Factumerit:
- One registration
- One password (in email)
- One interface (@eis)
- N services behind the scenes
