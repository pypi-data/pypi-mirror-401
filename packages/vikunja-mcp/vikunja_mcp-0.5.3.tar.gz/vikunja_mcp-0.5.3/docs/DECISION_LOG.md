# Factumerit Decision Log

**A catalog of design decisions—large and small—that shaped the product**

*Companion to FACTUMERIT_EPIC_JOURNEY.md*

---

## How to Read This Document

Decisions are organized chronologically, tagged by:
- **[STRATEGIC]** - Major architectural or business direction
- **[TACTICAL]** - Implementation approach within a strategy
- **[PIVOT]** - Changed direction after new information
- **[MICRO]** - Small but consequential choices

Status indicators:
- ✅ Implemented
- 🔄 Superseded (replaced by later decision)
- 💤 Deferred (in reserve)
- ❌ Abandoned (didn't work)

---

## September 2025: Methodology Research

### D-001: Four Methodologies, Not One [STRATEGIC] ✅
**Date**: Sept 2025
**Context**: Building haiku generator at moon viewing festival
**Decision**: Test 4 different AI coding methodologies simultaneously
**Alternatives**: Just use one approach and iterate
**Rationale**: Scientific comparison reveals which method fits which problem
**Outcome**: M4 (Validated TDD) wins for production code, M2 (spec-driven) wins for LLM integration

### D-002: Local LLM Judges [TACTICAL] ✅
**Date**: Sept 2025
**Context**: Need to evaluate methodology outputs
**Decision**: Use Gemma, Phi, Ollama as judges (Olympic medal scoring)
**Alternatives**: Single judge, human evaluation, cloud API
**Rationale**: Multiple local judges = faster iteration, no API costs, consensus scoring
**Outcome**: Reliable scoring mechanism for 431 experiments

---

## November 2025: Platform Selection

### D-003: Vikunja Over 7 Alternatives [STRATEGIC] ✅
**Date**: Nov 7, 2025
**Context**: Need PM tool for project portfolio (research item 1.131)
**Decision**: Vikunja
**Alternatives**: WeKan, Focalboard, Plane, Taiga, Worklenz, OpenProject, Redmine
**Rationale**:
- Multi-view flexibility (Kanban, List, Calendar, Gantt)
- REST API for automation
- Active Go+Vue development
- Self-hostable, $10-15/mo VPS vs $600/yr Trello
**Outcome**: Became the foundation for Factumerit product

---

## December 2025: Infrastructure & Architecture

### D-004: Beads Over YAML Tracking [STRATEGIC] ✅
**Date**: Dec 10, 2025
**Context**: 206 research items scattered in YAML files
**Decision**: Import everything to beads, deprecate YAML
**Alternatives**: Keep improving YAML, use GitHub Issues, use Vikunja directly
**Rationale**: Dependencies, cross-linking, status tracking impossible in YAML
**Outcome**: Infrastructure ready 6 days before product development exploded

### D-005: MCP + Slack Bot, Not MCP Only [TACTICAL] ✅
**Date**: Dec 16, 2025
**Context**: Claude.ai remote MCP had OAuth bug
**Decision**: Build Slack bot as workaround
**Alternatives**: Wait for Claude.ai fix, use only Claude Desktop
**Rationale**: Mobile access needed, workaround becomes feature
**Outcome**: Multi-interface architecture (4 interfaces today)

### D-006: Augment for X-Ray, Claude Code for Execution [STRATEGIC] ✅
**Date**: Dec 25, 2025 (explicit tagging)
**Context**: Different task types need different AI capabilities
**Decision**: Tag tasks by tool—Augment for context-heavy, Claude Code for straightforward
**Alternatives**: Use one tool for everything
**Rationale**:
- Augment sees 8,000+ line files, traces patterns across modules
- Claude Code executes copy-adapt-test workflows efficiently
- Different cost models (seat-based vs token-based)
**Outcome**: 36-table MAS schema mapped, TOOL_REGISTRY pattern traced, efficient task routing

---

## ADR Series (Dec 20-24, 2025)

### ADR-001: Slack as OIDC Provider [TACTICAL] ✅
**Date**: Dec 20, 2025
**Decision**: Use Slack OIDC for Vikunja auth, local admin backup
**Rationale**: Slack workspace already invite-only, zero password management
**Status**: Implemented, later supplemented with Google OIDC

### ADR-013: Slash Command Scoping [MICRO] ✅
**Date**: Dec 20, 2025
**Decision**: Use numbered selection for ambiguous projects
**Rationale**: `/today` might match multiple projects, disambiguation needed

### ADR-014: Quick vs Analytical MCP Tools [TACTICAL] ✅
**Date**: Dec 20, 2025
**Decision**: Separate fast (ECO) commands from LLM-required commands
**Rationale**: `/today`, `/overdue` don't need Claude—save costs

### ADR-015: Connect vs Join Instance Model [TACTICAL] ✅
**Date**: Dec 20, 2025
**Decision**: Users "connect" to existing Vikunja instances, don't "join"
**Rationale**: Supports BYOB (Bring Your Own Bot) model

### ADR-016: One-Click Vikunja Connect [TACTICAL] ✅
**Date**: Dec 20, 2025 (multiple revisions)
**Decision**: OAuth popup + polling, not manual token pasting
**Rationale**: Reduce onboarding friction from 5 steps to 1 click

### ADR-017: Popup+Polling Over Frontend Patch [MICRO] ✅
**Date**: Dec 21, 2025
**Decision**: Custom /slack-connect endpoint with popup, reject patching Vikunja frontend
**Rationale**: No fork maintenance, cleaner architecture

### ADR-018: Launch Lifecycle [TACTICAL] ✅
**Date**: Dec 21, 2025
**Decision**: Define Factum Erit launch phases
**Rationale**: Clear milestones for beta → production

### ADR-019: Matrix Platform Pivot [STRATEGIC] 🔄
**Date**: Dec 22, 2025
**Decision**: Add Matrix as primary chat interface
**Rationale**: Federation, self-hosting, E2EE, open protocol
**Status**: Later deferred (see D-010)

### ADR-020: Shared PostgreSQL Strategy [TACTICAL] 💤
**Date**: Dec 22, 2025
**Decision**: Single PostgreSQL for all services
**Rationale**: Reduce infrastructure complexity
**Status**: Proposed, partially implemented

### ADR-021: Synapse Over Dendrite [TACTICAL] 💤
**Date**: Dec 22, 2025
**Decision**: Use Synapse for Matrix homeserver
**Alternatives**: Dendrite (Go, lighter)
**Rationale**: Synapse more mature, better MAS integration
**Status**: Deferred with Matrix

### ADR-022: Authentik as IdP Bridge [TACTICAL] 💤
**Date**: Dec 22, 2025
**Decision**: Use Authentik to bridge MAS OIDC to Vikunja
**Alternatives**: Zitadel (failed), direct MAS
**Status**: Deferred with Matrix

### ADR-024: Patch MAS for Email Claims [TACTICAL] ❌
**Date**: Dec 23, 2025
**Decision**: Fork and patch MAS source code
**Rationale**: MAS doesn't return email claims (critical bug)
**Status**: Implemented, then abandoned with Matrix deferral
**Learning**: "When you patch your auth service, that's a red flag"

---

## The Matrix Saga & Pivot (Dec 22-29, 2025)

### D-007: Self-Host Matrix on Render [TACTICAL] 💤
**Date**: Dec 22, 2025
**Decision**: Deploy Synapse + MAS on Render
**Outcome**: 94 commits, 36-table schema discovery, 15-minute Docker builds

### D-008: RapidFuzz for Command Parsing [MICRO] ✅
**Date**: Dec 24, 2025
**Decision**: Use RapidFuzz (from research/1.002) for fuzzy command matching
**Rationale**: 250x faster than FuzzyWuzzy
**Outcome**: Research item paid dividends

### D-009: 36-Table Admin Script [TACTICAL] 💤
**Date**: Dec 28, 2025
**Decision**: Write matrix-admin.sh to delete users across 36 MAS tables
**Rationale**: No admin API exists
**Learning**: Deep schema knowledge required for basic operations

### D-010: Defer Matrix to Reserve [PIVOT] ✅
**Date**: Dec 29, 2025
**Context**: 94 commits fighting Matrix/Synapse/MAS
**Decision**: Launch with Vikunja-native @eis instead
**Alternatives**: Push through, find different Matrix hosting
**Rationale**:
- 90% of value with 10% of complexity
- $200-300/year + 100-150 hours saved
- Vikunja API enforces security boundaries
**Outcome**: Matrix in reserve, wake if >20% users request

---

## The OIDC Puzzle (Dec 29-31, 2025)

### D-011: nginx + Lua + PostgreSQL [TACTICAL] ❌
**Date**: Dec 29, 2025
**Context**: Google OIDC lets anyone sign up, need invite-only
**Decision**: Intercept OIDC callback at nginx layer
**Status**: **INVALIDATED** - Email not in callback URL (standard OIDC)
**Learning**: "OIDC is application-level, can't be fully handled at reverse proxy"

### D-012: Middleware Proxy as OAuth Client [PIVOT] ✅
**Date**: Dec 30, 2025
**Context**: nginx solution impossible
**Decision**: FastAPI middleware acts as OAuth client
**Rationale**:
- Exchanges code for tokens (gets email)
- Queries Vikunja SQLite directly ("spinal tap")
- Three-check decision flow
**Outcome**: Token-gated registration working

### D-013: Direct SQLite Access [TACTICAL] ✅
**Date**: Dec 30, 2025
**Decision**: Middleware queries Vikunja's `/db/vikunja.db` directly
**Alternatives**: Only use Vikunja API
**Rationale**:
- User existence check faster than API
- Enables bulk operations
- API doesn't expose everything needed
**Outcome**: Operational flexibility unlocked

---

## Security & Architecture (Jan 2026)

### D-014: Personal Bot Architecture [PIVOT] ✅
**Date**: Jan 3, 2026 (ADR-107)
**Context**: User isolation concern in shared bot
**Decision**: Each user gets own bot instance
**Alternatives**: Shared bot with careful scoping
**Rationale**:
- Complete isolation
- No cross-user data leakage possible
- Centralized poller for efficiency
**Outcome**: 83 commits on Jan 4

### D-015: Fernet Encryption for Bot Credentials [TACTICAL] ✅
**Date**: Jan 3, 2026
**Decision**: Encrypt bot tokens at rest in PostgreSQL
**Rationale**: Defense in depth, token broker pattern

### D-016: Lazy Bot Initialization [MICRO] ✅
**Date**: Jan 3, 2026
**Decision**: Create bots on first use, not at signup
**Rationale**: Avoid provisioning bots for users who never activate

### D-017: Owner Token for Project Sharing [MICRO] ✅
**Date**: Jan 4, 2026
**Context**: Vikunja project sharing API quirks
**Decision**: Use owner's JWT token, not user_id
**Learning**: "Vikunja uses `username` not `user_id`, and requires owner token"

---

## Public/Private Split (Jan 6, 2026)

### D-018: Tag Every Function [TACTICAL] ✅
**Date**: Jan 6, 2026
**Decision**: `# @PUBLIC` and `# @PRIVATE` tags for extraction
**Alternatives**: Separate repos from start, manual curation
**Rationale**: Single codebase, automated extraction for PyPI

### D-019: AGPL for Middleware [STRATEGIC] ✅
**Date**: Jan 6, 2026
**Decision**: Vikunja OIDC middleware must be AGPL (Vikunja is AGPL)
**Rationale**: Middleware queries Vikunja database directly = derivative work

---

## Communication Channel Evolution (Jan 2026)

### D-020: Email as Primary Channel [STRATEGIC] ✅
**Date**: Jan 7, 2026
**Context**: Onboarding friction, user reachability
**Decision**: Use email (via Resend) as primary communication channel
**Alternatives**:
- Slack DM (requires Slack account)
- Matrix (deferred)
- Vikunja comments only (no push notifications)
**Rationale**:
- Universal—everyone has email
- Works across devices without app install
- Password reset, welcome, notifications all via email
- Resend API simple and reliable
**Outcome**: `feat: Email Action Service for onboarding (fa-kwoh)`

### D-021: Email for Password Setup [TACTICAL] ✅
**Date**: Jan 7, 2026
**Decision**: Send password setup link via email, not show in UI
**Alternatives**: Display password in success page, force password creation
**Rationale**:
- More secure (password not visible to shoulder surfers)
- User gets email as proof of delivery
- Standard pattern users understand

---

## Decisions Pending / In Progress

### D-022: Haiku Tier Tool Restrictions [TACTICAL] ✅
**Date**: Jan 7, 2026
**Decision**: Block mutating tools for Haiku tier users
**Rationale**: Haiku less reliable for complex operations, read-only is safer

### D-023: Plugin System [STRATEGIC] 💤
**Date**: Jan 5, 2026
**Decision**: Defer plugin architecture to P2
**Rationale**: Focus on core product, "UAT IS THE NEW DEV"

---

## Meta-Decisions

### M-001: ADRs vs Informal Decisions
**Observation**: ADRs were written Dec 20-24, then stopped
**Reality**: Decisions continued via:
- Beads (solutions-xyz)
- Commit messages
- Doc files (081-MATRIX_DEFERRAL_DECISION.md)
- This decision log
**Learning**: Formal ADRs good for contentious/reversible decisions; informal tracking fine for tactical choices

### M-002: Document Dead Ends
**Decision**: Keep records of failed approaches
**Examples**:
- ADR-024 (MAS patching)
- D-011 (nginx OIDC)
- 82 commits in Matrix saga
**Rationale**: "The expensive lessons are the valuable ones"

---

## Decision Patterns Observed

### 1. Research Compounds
Decisions D-003 (Vikunja), D-008 (RapidFuzz) both leveraged prior research items.

### 2. Workarounds Become Features
D-005 (Slack bot as OAuth workaround) became core multi-interface architecture.

### 3. Pivots Preserve Investment
D-010 (Matrix deferral) didn't delete infrastructure—put in reserve.

### 4. Deep Dives Enable Pivots
Augment x-ray analysis (D-006) enabled both Matrix deep dive AND informed deferral decision.

### 5. Channel Simplification
Slack OIDC → Google OIDC → Email as primary: each step reduced friction.

---

## Statistics

| Category | Count |
|----------|-------|
| Strategic decisions | 8 |
| Tactical decisions | 18 |
| Pivots | 4 |
| Micro decisions | 6 |
| Abandoned | 2 |
| Deferred | 6 |
| Formal ADRs | 13 |

---

*Last updated: January 7, 2026*
