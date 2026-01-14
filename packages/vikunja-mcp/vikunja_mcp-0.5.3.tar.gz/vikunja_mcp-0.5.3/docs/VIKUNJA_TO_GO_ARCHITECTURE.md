# Vikunja to Go - Ephemeral Bot Access Architecture

**Status**: Architectural proposal (solutions-ih53)  
**Priority**: P1 (solves fundamental trust boundary problem)

---

## The Problem

**Bot with persistent API access to all users' Vikunja = unsolvable trust boundary at scale.**

Even with perfect input sanitization and output escaping:
- Bot compromise → All connected Vikunja instances exposed
- Zero-day exploits in sanitization logic
- Insider threat (bot operator has access to all user data)
- Compliance issues (bot processes user's production data)

**Current architecture**: Bot stores user tokens forever, has permanent read/write access.

---

## The Solution: Ephemeral Bot Access

**"Vikunja to Go" model**: Bot assists with instance creation, then hands off credentials and DELETES its own access.

### Three Phases

```
Phase 1: Bot-Assisted Setup (Trusted)
  User → Matrix Bot → Clones template → Creates temp instance
                   → Helps customize
                   → User reviews preview

Phase 2: Handoff (Trust Boundary)
  User: "looks good, give me the keys"
  Bot → Transfers ownership to user
      → REVOKES its own API token
      → Provides MCP server installation guide
  
Phase 3: User Self-Hosted (Bot never sees this)
  User's local MCP ↔ User's Vikunja instance
```

---

## Implementation Strategy

### Template-Based Provisioning (Simplified)

**No Docker/provisioning infrastructure needed** - just API calls!

1. **Bot maintains template accounts** (bot-owned):
   - `template-software-dev`: Backlog, Sprint, Done projects
   - `template-personal`: Home, Work, Learning projects
   - `template-research`: Papers, Experiments, Notes projects
   - `template-business`: Sales, Marketing, Operations projects

2. **User onboarding flow**:
   ```
   User: "Hey bot, I want to try Vikunja"
   Bot: "Great! What do you work on?"
   User: "Software development"
   Bot: *Exports template-software-dev using export_all_projects*
   Bot: *Creates temporary user account (bot-owned)*
   Bot: *Populates with template content using batch_create_tasks*
   Bot: "Check it out: vikunja.factumerit.app/preview/abc123"
   User: *Reviews in web UI*
   User: "Looks good!"
   ```

3. **Handoff flow**:
   ```
   Bot: "Perfect! Click here to claim: vikunja.factumerit.app/claim?setup_id=abc123"
   User: *Clicks → OAuth login → Creates Vikunja account*
   Auth-bridge:
     - Transfers project ownership to user
     - Creates API token for USER (not bot)
     - Revokes bot's temp token
     - Shows MCP installation instructions
   ```

4. **User self-hosted**:
   ```
   User: *Installs MCP server locally*
   User: *Configures with their own credentials*
   Bot: *No longer has access*
   ```

### Technical Details

**Tools already exist**:
- `export_all_projects()` - Export template content
- `batch_create_tasks()` - Populate temp instance
- `/vikunja-callback` - OAuth endpoint (needs modification)

**New functionality needed**:
- Template account management (create 4-5 templates)
- Temp user creation API (Vikunja admin API)
- Project ownership transfer (Vikunja API)
- Token revocation (Vikunja API)
- MCP installation guide (static page)

---

## Security Benefits

1. **Blast radius = 1**: Bot compromise doesn't expose existing users
2. **Zero persistent access**: Bot credentials are ephemeral (setup only)
3. **User controls trust**: They decide when to "graduate" from bot to self-hosted
4. **Clean separation**: Bot = onboarding tool, MCP = production tool
5. **Compliance-friendly**: Bot never stores/processes user's real work data

---

## Business Model

### Free Tier: "Vikunja Starter Kit" ($0)

**One-time setup assistant** - no persistent access needed!

```
User → Bot helps setup → User exports via Vikunja UI → Done
```

**What user gets**:
1. Bot creates temp instance from template (software dev, personal, research, business)
2. User customizes with bot's help: "add project X", "create tasks for Y"
3. User exports project via Vikunja web UI (built-in export feature!)
4. User imports to their own Vikunja (self-hosted or Vikunja Cloud)
5. Bot deletes temp instance after 24h

**No OAuth needed!** Just temp instance + export instructions.

**Revenue**: $0 (lead generation for paid tiers)

**Key insight**: User can export via Vikunja UI, so bot never needs persistent access!

---

### Pro Tier: "Managed Matrix Bot" ($20-50/month per team)

**Private bot instance for teams** - persistent access is acceptable because team trusts each other.

**What team gets**:
- Private Matrix bot instance (isolated, not multi-tenant)
- Team members connect their Vikunja accounts
- Bot has persistent access to team's shared Vikunja
- Team collaboration features
- Priority support

**Trust model**: Team members already trust each other (same company/project)
- If Alice can prompt inject, she already has access to team's Vikunja anyway
- Bot is just another team member with API access
- Prompt injection risk is team-level, not platform-level

**Revenue**: $20-50/month per team (5-20 users)

---

### Enterprise Tier: "Private Infrastructure" ($500-2000/month)

**Dedicated infrastructure** - full isolation and control.

**What org gets**:
- Dedicated Matrix homeserver (factumerit.yourcompany.com)
- Dedicated bot instance
- Dedicated Vikunja instance
- SSO integration (OIDC/SAML)
- Audit logs
- SLA guarantees
- Custom templates

**Revenue**: $500-2000/month per org (50-500 users)

---

## Migration Path

### Current State (Beta)
- Bot has persistent access to user Vikunja
- Defense-in-depth security (sanitization + escaping)
- Acceptable for trusted beta users (< 10 users)

### Transition
1. **Phase 1**: Launch current architecture for beta (1-2 weeks)
2. **Phase 2**: Build "Vikunja to Go" in parallel (2-3 weeks)
3. **Phase 3**: Migrate beta users to new model
4. **Phase 4**: Full launch with new architecture

### Beta User Communication
```
"You're using the beta architecture where the bot has access to your Vikunja.
We're building a new model where you'll own your data completely.
When ready, we'll help you migrate to self-hosted MCP (5 minutes)."
```

---

## Open Questions

1. **Vikunja user management API**: Can bot create users programmatically?
   - May need admin API access
   - Alternative: Manual user creation, bot just populates

2. **Project ownership transfer**: Does Vikunja API support this?
   - May need to recreate projects in user's account
   - Alternative: Share projects, then user duplicates

3. **Preview without login**: How to show temp instance?
   - Guest link with read-only access?
   - Screenshot/video preview?
   - Temporary credentials?

4. **MCP packaging**: How easy is installation?
   - NPM package for Claude Desktop?
   - Python package for Cline?
   - Docker image for self-hosted?

---

## Related Issues

- **solutions-ih53**: Epic for "Vikunja to Go" architecture
- **solutions-ih53.1**: Phase 1 - Template-based provisioning
- **solutions-ih53.2**: Phase 2 - OAuth handoff and token revocation
- **solutions-3ggz**: Phase 3 - MCP server packaging

---

## References

- `docs/SECURITY-POLICY.md` - Current security model with defense-in-depth
- `docs/SECURITY-ANALYSIS.md` - HTML injection research
- `src/vikunja_mcp/server.py` - export_all_projects, batch_create_tasks tools

