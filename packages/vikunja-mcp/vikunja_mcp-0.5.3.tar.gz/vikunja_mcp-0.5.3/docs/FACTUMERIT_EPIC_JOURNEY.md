# The Factumerit Epic: From Methodology Science to AI-First Task Management

**A story in 2,270+ commits across 3 repositories, 4 months of research, and 3 weeks of product development**

*For AI Tinkerers - January 2026*

---

## Act 0: The Moon Viewing Festival (September 2025)

It started with writer's block at a Japanese garden.

Seattle, late September 2025. A moon viewing festival—an annual tradition. A poet sat at a table with slips of paper, inviting visitors to write haiku.

**The problem**: All that came to mind was "There once was a man from Nantucket."

**The solution**: Build a program that converts any input into haiku.

But not just any program. **Four programs**, each using a different methodology:

| Method | Approach | Prompt Style |
|--------|----------|--------------|
| **M1** | Immediate | "Don't think, just do it" |
| **M2** | Specification-Driven | "Write all the specs first, then build" |
| **M3** | Test-Driven Development | "Write the tests first, then the code" |
| **M4** | Validated TDD | "Write tests, then BREAK them to prove they detect failures" |

Three local LLM judges (Gemma, Phi, Ollama) scored the outputs. Olympic-style medals.

Then: "Can you do iambic pentameter?" Yes.
Then: "What about limericks?" Full circle. Yes.

**September 30, 2025**: AI Tinkerers Seattle. The demo runs live.

> "You guys chase models. You're like, there's a new model coming out and you try it. I stick with the same model, but I use different methodologies, different prompting methods to try and figure out which one works."

The repo was called `spawn-experiments`. It spawned experiments. Four methods, same task, measured outcomes.

**The magic sauce**: Validated TDD (M4). Write your tests, then break them. Make sure your tests will detect something that's not working. That's production-level code.

But then Claude Code dropped, and for LLM integration tasks, **specifications started winning**.

The question shifted from "How do I write a haiku?" to:

**"How should AI write code?"**

---

## Act I: The Laboratory (September - November 2025)

The moon viewing experiment became a methodology research project.

`spawn-experiments` grew to **431 commits** of pure methodology science. Same problem, four approaches, measured outcomes.

| Method | Approach | Philosophy |
|--------|----------|------------|
| **M1** | Immediate Implementation | "Just build it" |
| **M2** | Full Specification First | "Design before code" |
| **M3** | Test-Driven Development | "Red-Green-Refactor" |
| **M4** | Adaptive TDD | "Match complexity to problem" |

**431 commits** of pure methodology science. Same problem, four approaches, measured outcomes.

The first experiments were humble: LRU caches with TTL, password validators, Roman numeral converters. But patterns emerged:

- **M1 wins for simple tasks** (2-3 minutes, good enough quality)
- **M2 wins for LLM integration** (92/100 avg quality, worth the upfront design)
- **M4 wins for production code** (validated quality with adaptive complexity)

**Key finding**: "When building AI features, specification-driven development consistently outperforms faster methods by 10-18 quality points."

This wasn't just research. It was training data for how to build AI products.

---

## Act I: The Research Foundation (September - November 2025)

While experiments ran in one repo, `spawn-solutions` (1,211 commits) became a **hardware store for software decisions**.

The MPSE framework (Methodology-based Problem-Space Exploration) systematically cataloged:

- **28 algorithm/library comparisons** (Tier 1)
- **14 managed service evaluations** (Tier 3)
- **Open standards discovery** (Tier 2): OpenTelemetry, OAuth/OIDC, PostgreSQL portability

Real discoveries with real business impact:

```
Finding: RapidFuzz is 250x faster than FuzzyWuzzy
Finding: orjson is 3-5x faster than stdlib json
Finding: Method 2 (spec-driven) wins for ALL LLM projects
```

---

## Act II: The Secret Weapon - Augment (September 2025 - ongoing)

While Claude Code executed tasks, **Augment** provided x-ray vision.

### The QRCards Revelation (September 28, 2025)

Strategic analysis assumed QRCards was a "creator economy platform." Augment analyzed the actual codebase and discovered:

> **"QRCards is not primarily a creator economy platform but rather a template library and analytics platform with QR code generation capabilities."**

Key findings from codebase analysis:
- **101 SQLite databases** - not a monolith, a federation
- **75+ Flask endpoints** for template and analytics services
- **DAP Processor** - PDF processing and QR code generation pipeline

The theoretical strategic analyses were transformed into concrete implementation opportunities with specific file paths:

```
Strategic (theoretical): "Implement creator success prediction"
Augment (concrete): "Optimize QR generation in dap_processor/qr/generator.py lines 31-45"
```

### The Division of Labor

By December 25, 2025, tasks were explicitly tagged:

**Augment-tagged** (needs codebase context):
- Security implementations
- Complete onboarding flow testing
- Architecture reviews

**Claude-Code-tagged** (straightforward execution):
- Create onboarding guide
- Create support channels
- Invite beta testers

**The insight**: Different AI tools for different task types. Augment for deep analysis (seat-based cost), Claude Code for execution (token-based cost).

### The Matrix Code Review (December 24, 2025)

Augment reviewed 1,936 lines across 4 files for production deployment:

```
Files Reviewed:
- src/vikunja_mcp/matrix_client.py (469 lines)
- src/vikunja_mcp/matrix_handlers.py (854 lines)
- src/vikunja_mcp/matrix_parser.py (204 lines)
- src/vikunja_mcp/server.py (8409 lines)

Verdict: ✅ APPROVED FOR PRODUCTION
```

This level of codebase-wide analysis—tracing the `TOOL_REGISTRY` pattern across 8,000+ lines—was only possible with full-context AI.

---

## Act III: The Vikunja Selection (November 7, 2025)

Research item **1.131 Project Management** evaluated 8 platforms:

**Lightweight**: WeKan, Vikunja, Focalboard
**Full-featured**: Plane, Taiga, Worklenz
**Enterprise**: OpenProject, Redmine

**Winner: Vikunja** ⭐

Why? Multi-view flexibility (Kanban, List, Calendar, Gantt), hierarchical projects, REST API for automation, active Go+Vue development since 2018. Most importantly: **a platform that could be extended**.

Little did anyone know this research item would become a product.

---

## Act IV: The Beads Revolution (December 10, 2025)

**The day issue tracking got serious.**

```
459655d4 2025-12-10 Initialize beads tracking with Vikunja integration
e6eea089 2025-12-10 Import 206 research items to beads, deprecate YAML tracking
17e28624 2025-12-10 Complete beads audit: import 72 existing research folders, close 41 complete
```

**206 research items** imported in one day. YAML tracking deprecated. Scattered notes became structured issue tracking with:

- Dependencies between issues
- Status tracking (open, in_progress, complete)
- Cross-repo linking
- Vikunja integration for visualization

This was 6 days before the Factumerit Big Bang. The infrastructure was ready.

---

## Act V: The MCP Experiment (December 14, 2025)

**Experiment 1.618** (originally 1.901): Build an MCP server for task management.

Using the methodology science from spawn-experiments, Method 4 (Adaptive TDD) was chosen.

```
Test: MCP server configuration - RED
Impl: MCP server with tool decorators - GREEN
Test: All MCP tools tests written - RED
Impl: All 4 MCP tools - GREEN
```

**Result**: M4 wins, 93/100 quality score.

The experiment proved MCP servers could be built reliably with the right methodology. The vikunja-mcp project was unblocked.

**That same day**: The MCP server grew from 4 tools to 22 tools to cover the full Vikunja wrapper API.

---

## Act VI: The Big Bang (December 16, 2025)

**27 commits in a single day.** The birth of the Slack bot.

```
43cde19 Initial commit: Vikunja Slack bot with Claude API
ca3c0c0 Tool parity: Slack bot now has all 44 tools (was 8)
e2d73fe UX: Thinking indicator + date/time in prompt
4917a2c UX: Rotating Latin thinking messages
1b81461 Feature: Model selection (haiku/sonnet/opus)
e1dc570 Add conversation memory for Slack bot
516b6ea Implement per-user Vikunja tokens for multi-user Slack bot
```

From nothing to a working multi-user Slack bot with:
- Natural language task management
- 44 MCP tools
- Per-user token isolation
- Usage tracking and cost estimation
- Conversation memory

**Why Slack?** Claude.ai's remote MCP had an OAuth bug. The workaround became a feature.

The naming? **"Factum Erit"** — Latin future perfect passive: "It will have been done." Not a promise, but a fait accompli.

---

## Act VII: The December Sprint (December 18-21, 2025)

The Slack bot was working. But mobile access meant more interfaces.

**December 18-19** (21 commits): Multi-instance Vikunja support
- Users could connect personal AND business Vikunja instances
- Instance switching via /connect command
- ICS calendar feeds for Google Calendar sync

**December 20** (26 commits): Zero-LLM-cost operations
- Pattern router bypasses Claude for simple queries
- Slash commands (/today, /overdue, /priority) cost nothing
- ECO mode tracking shows users their savings

**December 21** (16 commits): One-click OAuth connect
- No more manual token pasting
- OAuth callback creates Vikunja accounts automatically
- Welcome DMs guide new users

The bot was becoming a platform.

---

## Act VIII: The Matrix Rabbit Hole (December 22-28, 2025)

**"Why not add Matrix support?"**

Matrix offered: federation, self-hosting, E2EE, open protocol. The Vikunja community was already on Matrix. It seemed perfect.

**December 24-25** (65 commits): Matrix bot implementation
- matrix-nio integration
- RapidFuzz command parser (from research/1.002—the 250x faster fuzzy matching!)
- Synapse homeserver deployment
- Matrix Authentication Service (MAS)

**December 26-27** (71 commits): The authentication nightmare begins
- MAS doesn't return email claims to OIDC clients
- Synapse crashes on MSC4108 config (misleading docs)
- Can't create admin users via API or database

**December 28** (**80 commits**): The darkest day

The MAS email claims bug required:
1. Forking the MAS repository
2. Manually patching the source code
3. Building custom Docker images (15-minute builds)
4. Tracking upstream releases manually

### The 36-Table Problem

To delete a spam user from MAS, you must manually delete from **36 tables** in correct foreign key order:

```sql
-- Partial list (see scripts/matrix-admin.sh for full 36 tables)
DELETE FROM user_sessions WHERE user_id = ...;
DELETE FROM user_passwords WHERE user_id = ...;
DELETE FROM user_emails WHERE user_id = ...;
DELETE FROM user_external_ids WHERE user_id = ...;
-- ... 32 more tables ...
```

**How did we map 36 tables?** Augment. The same x-ray vision that found 101 SQLite databases in QRCards traced the MAS schema across its entire codebase.

---

## Act IX: The Strategic Pivot (December 29, 2025)

After 94 commits fighting Matrix/Synapse/MAS, a decision was made:

**"Defer Matrix/Synapse to reserve. Launch with Vikunja-native @eis instead."**

The numbers were clear:

| Approach | Infrastructure Cost | Engineering Hours | Complexity |
|----------|--------------------|--------------------|------------|
| Matrix-first | $200-300/year | 100-150 hours | High |
| Vikunja-native | $0 | ~20 hours | Low |

**The Matrix Patching Saga** (082-MATRIX_PATCHING_SAGA.md) documented every pain point:
- Manual MAS patches for email claims
- MSC4108 config gotchas requiring source code inspection
- Impossible admin user creation
- 36-table database schema for simple operations

**Key insight**: Vikunja-native @eis mentions could provide 90% of the value with 10% of the complexity.

The Matrix infrastructure wasn't deleted—it was **put in reserve**. If >20% of users requested real-time chat, it could be woken up.

---

## Act X: The OIDC Puzzle (December 29-31, 2025)

**Problem**: Google OIDC lets anyone sign up. We needed invite-only registration.

### The Elegant Solution That Couldn't Work

**Design 103**: nginx + Lua + PostgreSQL

The plan was beautiful:
1. nginx intercepts OIDC callback
2. Lua extracts email from callback URL
3. PostgreSQL query: does user exist?
4. If yes OR valid invite cookie → allow
5. Else → block

**Then came the critical finding** (103.6-CRITICAL_FINDING.md):

> **"Email is NOT available in OIDC callback URL. This is standard OIDC behavior, not an edge case."**

OIDC callbacks only contain `code` and `state`. Email is only available **after** token exchange—which nginx cannot do.

The entire nginx + Lua solution was **fundamentally impossible**.

### The Middleware Proxy Solution

**Option 2**: A FastAPI middleware that acts as an OAuth client:

```
Browser → nginx → Middleware Proxy → Vikunja
```

The middleware:
1. Intercepts callback with `code`
2. **Exchanges code for tokens** (acts as OAuth client)
3. **Decodes ID token** to get email
4. Queries database: user exists?
5. If user exists OR valid invite cookie → proxy to Vikunja
6. Else → 403 Forbidden

**The Three-Check Decision Flow**:
1. **CHECK 1**: Does user exist in database? (VIP or previous user) → Allow
2. **CHECK 2**: Valid invite cookie? (new user registration) → Allow
3. **CHECK 3**: Unauthorized → 403 Forbidden

### The Spinal Tap

December 30, 2025: **Spike to verify SQLite database access**

Discovery: Vikunja uses SQLite at `/db/vikunja.db`

```
b4b0f2c4 2025-12-30 spike(middleware): database access verified - all tests passed ✅
```

The middleware could query user existence directly from Vikunja's SQLite database. A "spinal tap" into the application's data layer, bypassing the API entirely.

**Operational flexibility unlocked**:
- Bulk user imports (bypass API)
- Data migrations and fixes
- Custom workflows outside Vikunja's business logic

---

## Act XI: The Security Pivot (January 3-4, 2026)

**83 commits on January 4th alone.**

User isolation was the concern. In a shared bot architecture, could User A's request accidentally affect User B's data?

**The solution**: Personal bot architecture.

Instead of one bot serving all users:
- Each user gets their own bot instance
- Bot credentials isolated in PostgreSQL with Fernet encryption
- Centralized poller architecture for efficiency
- Lazy bot initialization (bots created on first use)

```
solutions-xk9l: User Isolation Security epic
solutions-xk9l.1: Phase 1 complete
solutions-2x6i: Bot project sharing fixed via owner token flow
```

### The Project Sharing Bug

Vikunja's project sharing API was... surprising:

```
# What the docs said: use user_id
# What actually worked: use username field
# What ALSO failed: username field (sometimes)
# Final solution: Owner Token Flow
```

**4 commits** just to figure out project sharing worked via `username`, not `user_id`, and even then required the owner's JWT token.

---

## Act XII: The Public/Private Split (January 6, 2026)

With a working product, a question emerged: **What can be open-sourced?**

The `vikunja-mcp` core—58 tools for Vikunja task management—was generic. Anyone could use it.

But factumerit-specific code couldn't be published:
- User management and auth flows
- Slack/Matrix bot handlers
- Billing, credits, usage tracking
- Bot provisioning and signup workflows

**Solution**: Tag every function.

```python
# @PUBLIC - Safe for PyPI
@mcp.tool()
def create_task(project_id: int, title: str): ...

# @PRIVATE - Factumerit-specific
def _get_user_vikunja_token(user_id: str): ...
```

An extraction script (`extract_public.py`) generates clean vikunja-mcp releases for PyPI while the private repo contains the full platform.

---

## Epilogue: The Current State (January 7, 2026)

**3 repositories, 2,270+ total commits:**

| Repository | Commits | Purpose |
|------------|---------|---------|
| spawn-experiments | 431 | Methodology research |
| spawn-solutions | 1,211 | Service discovery + beads tracking |
| factumerit | 628 | The product |

**The product:**

- **58 MCP tools** for full Vikunja API access
- **4 interfaces**: Claude Desktop, Claude.ai, Slack bot, Vikunja-native @eis
- **3 authentication flows**: Slack OIDC, Google OIDC (token-gated), API tokens
- **Personal bot architecture** with centralized management
- **ECO mode** for zero-LLM-cost operations

**Commit intensity tells the story:**

```
Dec 10:  --  commits - Beads adoption (206 items imported)
Dec 16:  27 commits - Birth
Dec 20:  26 commits - Slash commands
Dec 24:  37 commits - Matrix begins
Dec 28:  80 commits - Matrix crisis
Dec 29:  --  commits - Strategic pivot
Dec 31:  32 commits - OIDC puzzle
Jan 04:  83 commits - Security pivot
```

---

## The Dead Ends That Taught Everything

### 1. The Matrix Patching Saga (94 commits)

**What we tried**: Matrix/Synapse/MAS for federated chat
**What we learned**:
- MAS email claims require source patching
- 36-table schema for user management
- 15-minute Docker builds
- When you patch your auth service, that's a red flag

**Cost**: 94 commits, ~100 hours
**Value**: Deep OIDC knowledge, strategic clarity

### 2. The nginx + Lua OIDC Gate (Design 103)

**What we tried**: Elegant nginx-layer registration gating
**What we learned**: OIDC callbacks only contain `code` + `state`—email requires application-level token exchange

**Cost**: Full design document, implementation files (all invalidated)
**Value**: Deep OIDC protocol understanding

### 3. The Project Sharing Bug

**What we tried**: Share projects via `user_id`
**What we learned**: Vikunja uses `username`, and even that requires owner JWT token

**Cost**: 4 commits of debugging
**Value**: Vikunja API edge case documentation

---

## Key Learnings for AI Tinkerers

### 1. Research Compounds

The RapidFuzz discovery (research/1.002) saved hours when building the Matrix command parser. The OAuth/OIDC research (2.060) predicted the MAS email claims problem. **Every research item paid dividends.**

### 2. Different AI Tools for Different Tasks

**Augment** = X-ray vision
- See entire codebases (8,000+ line files)
- Trace patterns across modules
- Code reviews, architecture discovery
- Seat-based pricing (use for deep analysis)

**Claude Code** = Task execution
- Clear patterns, straightforward implementation
- Copy-adapt-test workflows
- Token-based pricing (use for volume)

### 3. Methodology Matters

M4 (Adaptive TDD) built the MCP server. M2 (spec-driven) designed the architecture. M1 (immediate) handled quick fixes. **Know which method fits which problem.**

### 4. Pivots Are Features

Matrix wasn't a failure—it's in reserve. The nginx OIDC design taught protocol fundamentals. **Design for pivots, not permanence.**

### 5. Dead Ends Teach

The Matrix Patching Saga (94 commits) taught more about authentication architecture than any tutorial. The nginx OIDC invalidation taught OIDC protocol deeply. **The expensive lessons are the valuable ones.**

### 6. Infrastructure Before Product

Beads adoption (Dec 10) preceded product development (Dec 16) by 6 days. **206 issues imported** meant the tracking system was ready when velocity exploded.

### 7. Trust Models Are Architecture

BYOB (Bring Your Own Bot) emerged from the security pivot. Users run their own MCP servers, connecting to hosted Vikunja. **The trust boundary became a feature.**

---

## The Numbers

| Metric | Value |
|--------|-------|
| Total commits | 2,270+ |
| Research phase | 4 months (Sept-Dec 2025) |
| Product sprint | 3 weeks (Dec 16 - Jan 7) |
| MCP tools | 58 |
| Platforms researched | 8 (PM tools) |
| Methodologies tested | 4 |
| Major pivots | 2 (Matrix deferral, personal bots) |
| Dead ends documented | 3 |
| Interfaces | 4 |
| Beads imported | 206 (Dec 10) |
| Peak commit day | 83 (Jan 4) |
| Price point | $10/month (Dine-In tier) |

---

## What's Next

- **LinkedIn Live demos** with instant provisioning
- **Enterprise SSO** (SAML, SCIM)
- **vikunja-mcp on PyPI** (open source)
- **24/7 support** for Pro/Enterprise tiers

The research continues. The methodology compounds. The product evolves.

**Factum Erit** — It will have been done.

---

*Document generated from analysis of git histories across spawn-experiments, spawn-solutions, and factumerit repositories.*
