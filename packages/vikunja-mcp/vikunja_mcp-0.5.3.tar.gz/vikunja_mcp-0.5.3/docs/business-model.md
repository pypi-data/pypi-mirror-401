# Factumerit Business Model

## Overview

Factumerit provides AI-enhanced task management through Vikunja integration. The platform uses a **BYOC model** (Bring Your Own Claude): we provide the platform and tools, users bring their own AI.

## The BYOC Pivot

**Why not resell API access?**
- Anthropic ToS requires explicit approval to resell
- Tier limits constrain scaling ($100/mo on Tier 1)
- One-sided terms for commercial use
- Better: users have direct relationship with their AI provider

**The model:**
```
┌─────────────────────────────────────────────────────────────────┐
│  Factumerit Platform: $5/mo                                     │
│  ├── Vikunja hosting (tasks, projects, kanban, gantt)          │
│  ├── !commands (FREE - no LLM needed)                          │
│  ├── MCP server (Claude Desktop integration)                   │
│  └── Bot integration (Slack/Matrix)                            │
└─────────────────────────────────────────────────────────────────┘
                              +
┌─────────────────────────────────────────────────────────────────┐
│  User's AI (BYOC): $20/mo to Anthropic                         │
│  └── Claude Pro/Max subscription                               │
│  └── Claude Desktop + MCP = full power                         │
│  └── Natural language queries, reasoning, planning             │
└─────────────────────────────────────────────────────────────────┘
```

## Command Tiers

### FREE: !commands (No LLM)

Direct Vikunja API calls - no AI required:

| Command | What it does |
|---------|-------------|
| `!inbox` | List inbox tasks |
| `!projects` | List projects |
| `!add <task>` | Create task |
| `!done <id>` | Complete task |
| `!today` | Tasks due today |
| `!week` | Tasks due this week |

These work in Slack, Matrix, or any bot integration.

### $/$$/$$$: AI-Powered (BYOC)

Natural language queries require an LLM:

| Tier | Example | Requires |
|------|---------|----------|
| $ | "What's in my inbox?" | Claude Desktop |
| $$ | "Summarize my week" | Claude Desktop |
| $$$ | "Plan my kitchen remodel" | Claude Desktop |

**Users pay Anthropic directly** via Claude Pro ($20/mo) or Max ($100/mo).

## Platform Subscription

### Pricing

| Duration | Price | Per Day | Use Case |
|----------|-------|---------|----------|
| Weekly | $1.50 | $0.21 | Trip planning, short projects |
| Monthly | $5.00 | $0.17 | Regular users |
| Annual | $50.00 | $0.14 | Power users, ongoing use |

### What's Included

- Full Vikunja access (unlimited tasks, projects)
- !commands via Slack/Matrix (FREE, no LLM)
- MCP server for Claude Desktop
- Template library access

### What's NOT Included

- AI/LLM access (BYOC required)
- We don't bill for AI usage
- No API credits to manage

## B2B Model: AI Concierge

Businesses use Claude Desktop + MCP to serve their customers.

```
┌─────────────────────────────────────────────────────────────────┐
│  BUSINESS (Your Customer)                                       │
│  └── Claude Pro/Max: $20/mo (to Anthropic)                     │
│  └── Factumerit Platform: $X/mo (to us)                        │
│                                                                 │
│  Gets: Claude Desktop + MCP server                              │
│  Can: Create, manage, distribute personalized task lists        │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ "Here's your personalized to-do list"
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  END CUSTOMERS (Business's Customers)                           │
│  └── $0 to Anthropic (no AI needed)                            │
│  └── Bundled in business's service                             │
│                                                                 │
│  Gets: Vikunja account + !commands                              │
│  Can: Manage tasks, get notifications                          │
│  Cannot: AI queries (no Claude Desktop)                        │
└─────────────────────────────────────────────────────────────────┘
```

### B2B Volume Pricing

| Quantity | Platform/seat/mo | Total |
|----------|------------------|-------|
| 10-49 | $4.00 | $40-196/mo |
| 50-99 | $3.50 | $175-347/mo |
| 100+ | $3.00 | $300+/mo |

### Example: Safari Tours

```
Business setup:
  Claude Pro: $20/mo (to Anthropic)
  100 customer licenses: $300/mo (to Factumerit)

Each customer gets:
  - Vikunja account with "Kenya Safari Planner" template
  - !commands via WhatsApp/Slack
  - Business manages their list via Claude Desktop

Business uses Claude to:
  - Create personalized packing lists
  - Set up itinerary reminders
  - Answer customer questions (via their own interface)
```

## Future: Self-Hosted LLM Tier

For users who want AI features without BYOC, we may offer a self-hosted tier:

```
┌─────────────────────────────────────────────────────────────────┐
│  Platform + AI: $10/mo                                          │
│  ├── Everything in base platform                               │
│  ├── AI queries powered by self-hosted model                   │
│  └── Qwen 3 / DeepSeek V3 / Llama 4                           │
└─────────────────────────────────────────────────────────────────┘
```

**Economics:**
- GPU cloud: ~$150-300/mo for decent throughput
- At 100 users: $1.50-3.00/user/mo cost
- At 1000 users: $0.15-0.30/user/mo cost
- Margin improves dramatically with scale

See bead `fa-msco` for evaluation.

## Tax Obligations (WA/Seattle)

| Tax | Rate | Who Pays | Frequency |
|-----|------|----------|-----------|
| WA Sales Tax | 10.55% | Customer | Quarterly remit |
| WA B&O Tax | 1.5% | Business | Quarterly |
| Seattle B&O | ~0.4% | Business | Quarterly |

## Cost Structure

### Fixed Monthly (Infrastructure)

| Item | Cost |
|------|------|
| Render Pro plan | $19 |
| Bot service | $7 |
| Vikunja hosting | $24 |
| Database | $7 |
| Storage | $0.50 |
| **Total** | **~$58** |

### Variable (Per-User)

- No API costs (BYOC model)
- At 100 users: $0.58/user/mo fixed overhead
- At 1000 users: $0.06/user/mo fixed overhead

## Breakeven Analysis

**Subscribers needed to cover infrastructure:**
```
$58 monthly infra / $4.00 net per subscriber = 15 subscribers
```

**With B2B volume (100+ tier):**
```
$58 monthly infra / ~$2.50 net per seat = 24 seats
```

## Revenue Scenarios

### Conservative (Year 1)

| Channel | Volume | Revenue | Margin |
|---------|--------|---------|--------|
| Monthly subs | 50 | $3,000 | $2,400 |
| Annual subs | 20 | $1,000 | $870 |
| B2B (2 partners) | 200 seats | $7,200 | $4,800 |
| **Total** | | **$11,200** | **$8,070** |

Infrastructure: $696/year → **Net: +$7,374**

### Growth (Year 2)

| Channel | Volume | Revenue | Margin |
|---------|--------|---------|--------|
| Monthly subs | 200 | $12,000 | $9,600 |
| Annual subs | 100 | $5,000 | $4,350 |
| B2B (10 partners) | 1000 seats | $36,000 | $24,000 |
| Self-hosted tier | 50 | $6,000 | $3,000 |
| **Total** | | **$59,000** | **$40,950** |

Infrastructure: $696 + $3,600 (GPU) = $4,296/year → **Net: +$36,654**

## What This Changes

### Killed by BYOC Pivot

- ~~API credit system~~ (users bill Anthropic directly)
- ~~Ledger/wallet for API usage~~ (not needed)
- ~~Promo credits as acquisition~~ (give platform time instead)
- ~~Two-meter system~~ (just subscription meter)
- ~~Anthropic reseller relationship~~ (avoided ToS issues)

### Still Relevant

- Platform subscription billing
- User management
- Bot provisioning (!commands)
- MCP server (open source + hosted)
- B2B template distribution
- Credit TTL (for future self-hosted tier)

### New Features Needed

- Claude Desktop setup instructions
- MCP server configuration guide
- Template distribution tool (bead needed)
- B2B customer provisioning workflow

## Implementation Roadmap

Active beads:
- `fa-msco` - Evaluate self-hosted LLM for future tier
- `fa-qfpo` - B2B pricing epic (revised for BYOC)

New beads needed:
- Claude Desktop onboarding guide
- MCP configuration wizard
- Template distribution tool
- B2B provisioning workflow
