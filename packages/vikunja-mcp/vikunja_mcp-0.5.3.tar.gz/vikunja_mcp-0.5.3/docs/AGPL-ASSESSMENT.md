# AGPL License Assessment for Factum Erit / Vikunja Integration

**Date:** 2026-01-06
**Updated:** 2026-01-06 (final verdict after architecture review)
**Status:** ✅ RESOLVED - Clean separation via HTTP middleware
**Bead:** fa-0wb

## Executive Summary

**FINAL VERDICT: Architecture is AGPL-compliant with proper licensing.**

| Component | License | Status |
|-----------|---------|--------|
| Factum Erit Bot | Proprietary | ✅ Stays closed - only makes HTTP calls |
| vikunja-mcp | MIT | ✅ Pure REST API client |
| Vikunja Middleware | **AGPL** | ⚠️ Must release - does direct DB access |
| Vikunja Server | AGPL | ✅ Unmodified official image |

**Key insight**: The "Spinal Tap" middleware runs as a **separate HTTP service**, not imported
into the bot. This creates a clean process boundary that preserves the bot's proprietary status.

| Integration Method | Risk Level | Copyleft Triggered? |
|-------------------|------------|---------------------|
| REST API only (vikunja-mcp) | ✅ Low | No |
| Nginx access policy overlay | ✅ Low | No |
| HTTP call to middleware | ✅ Low | No (for caller) |
| Middleware direct DB access | ✅ Resolved | Yes → release middleware as AGPL |
| Modifying Vikunja source | 🔴 High | Yes (not applicable - unmodified) |

## Architecture Analysis

### Actual Factum Erit Stack (Self-Hosted)

```
┌─────────────────────────────────────────────────────────────┐
│   Factum Erit Bot (Proprietary)                             │
│   (Slack/Matrix handlers, billing, user management)         │
│   server.py: /activate-bot calls middleware via HTTP        │
├─────────────────────────────────────────────────────────────┤
│   vikunja-mcp (MIT)              │                          │
│   Pure HTTP client               │  requests.post(          │
│   httpx → Vikunja API            │    "/internal/share-project")
├──────────────────────────────────┼──────────────────────────┤
│        ↕ HTTP REST API           │   ↕ HTTP POST            │
│                                  │   (separate service)     │
├──────────────────────────────────┴──────────────────────────┤
│                    Docker Container                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  nginx (access policy overlay)                         │ │
│  │  - Blocks /api/v1/register without admin token         │ │
│  │  - Requires token_validated cookie for OIDC callback   │ │
│  │  - Routes /internal/* to middleware                    │ │
│  │  - Proxies other requests to Vikunja                   │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  Middleware (AGPL) ← MUST RELEASE                      │ │
│  │  - /internal/share-project endpoint                    │ │
│  │  - Direct INSERT INTO project_users                    │ │
│  │  - Provides "API+" capabilities                        │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  Vikunja Server (AGPL-3.0) - UNMODIFIED                │ │
│  │  - Running official vikunja/vikunja:latest image       │ │
│  │  - No source code changes                              │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  SQLite: /db/vikunja.db                                │ │
│  │  - Read/written by Vikunja                             │ │
│  │  - Also accessed by middleware (AGPL component)        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key Characteristics

1. **vikunja-mcp** (`vikunja_client.py`): Uses `httpx` for REST API calls ✅
2. **No Vikunja code modified**: Running unmodified official Docker image ✅
3. **nginx overlay**: Adds access control without modifying Vikunja ✅
4. **Bot → Middleware**: HTTP POST, not import (separate processes) ✅
5. **Middleware direct DB access**: Must be released as AGPL ⚠️ → fa-1vxy

## Legal Analysis

### Question 1: Does API usage trigger AGPL copyleft?

**Answer: Generally NO**

The AGPL's network clause applies to the party **running** the AGPL software, not parties **calling** its API. Key sources:

> "AGPL does not extend the GPL in that it makes the Internet count as a form of linking which creates a derivative work... it makes anyone who uses the software via the Internet entitled to its source code. It does not update the 'what counts as a derivative work' algorithm—it updates the 'what counts as distributing the software' algorithm."
> — [Drew DeVault](https://drewdevault.com/2020/07/27/Anti-AGPL-propaganda.html)

> "'Arms-length communication' refers to a software architecture where the AGPL-licensed component is run as a separate, independent process or service, communicating with your proprietary application via standard interfaces (like APIs, command-line calls, or network protocols) rather than direct linking. This separation helps to prevent the AGPL's copyleft from extending to your entire proprietary codebase."
> — [Ithy Guide](https://ithy.com/article/agpl-unmodified-commercial-use-fhaoyrg3)

> "Only modifications to the sync engine or components it directly interacts with (such as its specific MySQL database). Using it via the standard REST APIs requires no disclosure."
> — [Nylas AGPL Clarification](https://github.com/nylas/sync-engine/issues/135)

### Question 2: Can vikunja-mcp be MIT licensed?

**Answer: YES**

vikunja-mcp is an independent work that:
- Contains no Vikunja source code
- Does not link against Vikunja libraries
- Communicates solely via HTTP REST API
- Can work with any Vikunja-compatible API

An API client is not a derivative work of the server it communicates with. The MIT license is appropriate.

### Question 3: What are SaaS/network use considerations?

**Answer: Copyleft applies to the Vikunja operator, not API consumers**

If Factum Erit **runs** a Vikunja instance:
- Must provide source code of any **Vikunja modifications** to users
- Does NOT need to release Factum Erit bot code
- Self-hosted Vikunja without modifications: no disclosure required

If using **hosted Vikunja**:
- The hosting provider bears AGPL obligations
- Factum Erit has no AGPL obligations

### Question 4: Does the nginx access control overlay trigger copyleft?

**Answer: NO** ✅

The nginx configuration acts as a reverse proxy that:
- Blocks certain routes (registration, OIDC callback)
- Requires authentication tokens/cookies
- Forwards allowed traffic unchanged to Vikunja

This is analogous to putting a fence around a building - it doesn't modify the building.
A reverse proxy with access policies is not a "modification" of the proxied software.
Many production deployments use nginx/haproxy/etc. in front of AGPL software without issues.

### Question 5: Does direct database access ("Spinal Tap") trigger copyleft?

**Answer: UNCLEAR** ⚠️ - This is the gray area

The "Spinal Tap" approach directly `INSERT`s into Vikunja's `project_users` table,
bypassing Vikunja's API entirely. This raises questions:

**Arguments that it's safe:**
- The database is data, not software
- Vikunja's code hasn't been modified
- You're just writing data that Vikunja will read
- Similar to importing data via SQL scripts

**Arguments for caution:**
- The Nylas AGPL clarification states: "Only modifications to the sync engine
  **or components it directly interacts with (such as its specific MySQL database)**"
- This suggests the database is considered a "component" of the AGPL software
- Direct DB manipulation creates tighter coupling than API calls
- You're relying on internal schema knowledge, not public API contract

**Key distinction**: The Nylas statement was about what modifications require
disclosure, not about whether database access creates a derivative work. The
intent appears to be: "if you modify Vikunja's database schema, disclose those
changes" rather than "any INSERT makes your code AGPL."

**Practical assessment**: The middleware that does direct DB inserts is not
published as a standalone library (like vikunja-mcp). It's internal infrastructure.
The question is whether this internal middleware must be AGPL-licensed.

## Risk Assessment

### Low Risk Factors

| Factor | Status |
|--------|--------|
| REST API communication (vikunja-mcp) | ✅ Safe |
| vikunja-mcp contains no Vikunja code | ✅ Safe |
| nginx proxy overlay | ✅ Safe |
| Unmodified Vikunja source code | ✅ Safe |
| MIT license for vikunja-mcp | ✅ Appropriate |

### Medium Risk Factors

| Factor | Status |
|--------|--------|
| Direct database INSERT (Spinal Tap) | ⚠️ Gray area |
| Middleware knowledge of Vikunja schema | ⚠️ Tight coupling |

### Potential Concerns

1. **Gray area**: The legal question of "what constitutes a derivative work across network APIs" has not been definitively settled in court. However, the consensus among license experts favors the interpretation that REST API communication does not create derivative works.

2. **Google's conservative stance**: Google bans all AGPL software entirely due to corporate risk aversion. This is a policy choice, not a legal requirement. [Source](https://opensource.google/documentation/reference/using/agpl-policy)

3. **Distributed applications**: Some argue that tightly integrated distributed systems might constitute a single "combined work." The "Spinal Tap" direct database access is closer to this concern than pure API usage.

4. **Database as "component"**: The Nylas clarification explicitly mentions the database as something that "directly interacts" with the AGPL software. While the context was about modifications, it suggests the database isn't entirely separate.

## Recommendations

### Final Decision: Option D - Release Middleware as AGPL

**Chosen approach**: License the middleware under AGPL-3.0 and release publicly.

This is the cleanest solution because:
1. **Bot stays proprietary** - Communicates with middleware over HTTP (separate process)
2. **Full AGPL compliance** - No gray areas or legal uncertainty
3. **Community benefit** - "Vikunja API+" could help other Vikunja users
4. **Simple** - No need to rewrite middleware to use limited API

### Action Items

1. ✅ **vikunja-mcp (MIT)** - No changes required
2. ✅ **nginx overlay** - No changes required
3. ⚠️ **Middleware** - Release as AGPL → See bead fa-1vxy

### Middleware Release Checklist

- [ ] Add AGPL-3.0 LICENSE file to middleware repo
- [ ] Add license header to source files
- [ ] Create public GitHub repo (e.g., `vikunja-api-plus` or `vikunja-middleware`)
- [ ] Document the API endpoints
- [ ] Add attribution to Vikunja project
- [ ] Update this assessment with final repo URL

### Best Practices Going Forward

1. **Never incorporate Vikunja code** into Factum Erit or vikunja-mcp
2. **Keep middleware as separate service** - HTTP boundary preserves bot's proprietary status
3. **Document any Vikunja modifications** if self-hosting with changes
4. **Include attribution** - Credit Vikunja project in middleware and vikunja-mcp

### Architecture Boundary Rules

| If you want to... | Then... |
|-------------------|---------|
| Add new Vikunja API wrapper | Add to vikunja-mcp (MIT) ✅ |
| Add direct DB operation | Add to middleware (AGPL) |
| Add bot business logic | Add to server.py (proprietary) ✅ |
| Call middleware from bot | Use HTTP, never import |

## Comparison with Similar Projects

Many projects successfully use MIT/Apache licenses for API clients of AGPL software:

- MongoDB clients (various licenses) for AGPL MongoDB
- GitLab API clients (various licenses) for AGPL GitLab
- Nextcloud API clients (various licenses) for AGPL Nextcloud

## Legal Disclaimer

This assessment represents technical analysis, not legal advice. The interpretation of AGPL regarding API usage has not been definitively resolved by courts. For specific legal guidance, consult an attorney specializing in open-source licensing.

## References

1. [GNU AGPL-3.0 License Text](https://www.gnu.org/licenses/agpl-3.0.en.html)
2. [Drew DeVault - Anti-AGPL Propaganda](https://drewdevault.com/2020/07/27/Anti-AGPL-propaganda.html)
3. [FOSSA AGPL Guide](https://fossa.com/blog/open-source-software-licenses-101-agpl-license/)
4. [Snyk AGPL Guide](https://snyk.io/learn/agpl-license/)
5. [Nylas AGPL API Clarification](https://github.com/nylas/sync-engine/issues/135)
6. [OSPO AGPL Q&A](https://ospo.co/blog/questions-and-answers-about-the-agpl/)
7. [Google AGPL Policy](https://opensource.google/documentation/reference/using/agpl-policy)
8. [Vikunja License](https://github.com/go-vikunja/vikunja)
