# L0: Onboarding Flow

**Status:** Design v2 - Updated January 2026
**Bead:** fa-4mda (was solutions-c33n)
**Last Updated:** 2026-01-08

---

## Onboarding Tiers

This document covers **L0 (Basics)** - the first tier of onboarding.

| Tier | Focus | Goal |
|------|-------|------|
| **L0: Basics** | Vikunja + @eis fundamentals | User can create/complete tasks, knows @eis exists |
| L1: Task Management | Organize with AI | User has working GTD system |
| L2: Productivity | Advanced workflows | AI is user's co-pilot |

See also: `L1_ONBOARDING.md`

---

## Overview

**Two-layer onboarding:**
1. **Vikunja basics** - How to use the task manager (ears off)
2. **@eis enhancement** - How @eis makes things faster/smarter

Most users are new to both. Teaching only @eis leaves users lost when:
- @eis is down
- They're out of credit
- They just want to quickly add a task without AI

### Terminology

| Term | What it is | How we refer to it |
|------|------------|-------------------|
| **Factum Erit** | The service/brand | "Factum Erit" - visible in emails, branding |
| **Vikunja** | The task management UI | "your task manager" |
| **@eis** | The AI assistant | "your AI assistant" |

### Interfaces

Users can interact with @eis through multiple channels:

| Interface | Status | Description |
|-----------|--------|-------------|
| **Vikunja (web)** | ✅ Primary | Create tasks with @eis mentions |
| **Email** | ✅ Primary | Reply to @eis emails, click action links |
| **Slack** | Available | On request - not actively promoted |

Email is a first-class interface. Users can manage tasks entirely through email without ever opening Vikunja.

### Design Principles

1. **Interface-agnostic core** - The learning path works via Vikunja OR email
2. **Learn by doing** - Users type/click/reply, not read walls of text
3. **Progressive disclosure** - Don't overwhelm; unlock features as they learn
4. **@eis is optional** - Everything works without AI; @eis is a power-up
5. **Graduation optional** - Advanced features shown but not required

### Onboarding Paths

**This document describes the Vikunja (web) path.** Email-only onboarding is equally valid:

| Path | Entry Point | Progression |
|------|-------------|-------------|
| **Vikunja** | Signup → Inbox task | This document |
| **Email** | Onboarding email | Reply to email with commands |

The email path sends an onboarding email after signup. Users can reply directly to interact with @eis - they never need to open Vikunja if they prefer email.

---

## Flow Diagram

```
Account Created
      │
      ▼
┌─────────────────────────────────────────────────┐
│ Stage 0: Welcome to Vikunja                     │
│ Your Inbox is where tasks live.                 │
│ Try it: Type "Buy groceries" and press Enter    │
└─────────────────────────────────────────────────┘
      │
      ▼ (user creates a task manually)
      │
┌─────────────────────────────────────────────────┐
│ Stage 1: You created a task!                    │
│ Click the checkbox to complete it.              │
│ That's the basics: create tasks, check off.     │
│                                                 │
│ Now meet your AI assistant...                   │
│ Create a task: @eis !help                       │
└─────────────────────────────────────────────────┘
      │
      ▼ (user runs @eis !help)
      │
┌─────────────────────────────────────────────────┐
│ Stage 2: Try these commands (any order)         │
│ 2a: @eis !w Seattle     (weather - FREE)        │
│ 2b: @eis !bal           (your AI credit - FREE) │
└─────────────────────────────────────────────────┘
      │
      ▼ (both done)
      │
┌─────────────────────────────────────────────────┐
│ Stage 3: AI Power                               │
│ Ask @eis anything:                              │
│ "@eis what should I focus on?"                  │
│                                                 │
│ For task creation, use $$ for better results:   │
│ "@eis $$ plan a birthday party"                 │
└─────────────────────────────────────────────────┘
      │
      ▼ (user tries AI)
      │
┌─────────────────────────────────────────────────┐
│ Stage 4: Pro Mode (optional)                    │
│ Want @eis to watch ALL new tasks?               │
│ Type: @eis !ears on                             │
│                                                 │
│ Or keep ears off and @mention when needed.      │
└─────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────┐
│ ✅ You're all set!                               │
│                                                 │
│ Vikunja basics:                                 │
│ • Type task + Enter = create                    │
│ • Click checkbox = complete                     │
│ • Drag to reorder                               │
│                                                 │
│ @eis commands: (see !help)                      │
│ • @eis !w city    → Weather (FREE)              │
│ • @eis !bal       → Check credit (FREE)         │
│ • @eis !x 42      → Complete task #42           │
│ • @eis !ears on   → Auto-process mode           │
└─────────────────────────────────────────────────┘
```

---

## Stage Details

### Stage 0: Welcome Task (Account Creation)

**Created by:** User provisioning system (signup_workflow.py)
**Location:** User's Inbox

```
Title: 👋 Welcome! Create your first task

Description:
Welcome to Vikunja, your task manager!

**Try it now:** Type something in the task box above (like "Buy groceries")
and press Enter.

That's it - you just created a task! ✓
```

---

### Stage 1: Meet @eis

**Triggered by:** User creates their first manual task
**Creates:** 1 task introducing @eis

```
Title: 🤖 Meet @eis, your AI assistant

Description:
You've got the basics! Now meet @eis.

@eis is an AI assistant that lives in your tasks.
Mention @eis in a task to give it commands.

**Try it:** Create a new task with this text:
@eis !help

This shows everything @eis can do.
```

---

### Stage 2: Core Commands (Parallel)

**Triggered by:** `@eis !help`
**Creates:** 2 tasks (can complete in any order)

**Challenge 2a:**
```
Title: 2️⃣ Try: @eis !w Seattle

Description:
Get weather for any city. FREE - no credit used.

Create a task: @eis !w Seattle
(or try your own city!)
```

**Challenge 2b:**
```
Title: 3️⃣ Try: @eis !bal

Description:
Check your AI credit balance.
You have $1.00 free to start.

Create a task: @eis !bal
```

---

### Stage 3: AI Command

**Triggered by:** Both Stage 2 challenges completed
**Creates:** 1 task

```
Title: 4️⃣ Try AI: Ask @eis anything

Description:
@eis understands natural language.

**For questions (uses ~1-2¢):**
@eis what should I focus on?
@eis summarize my tasks

**For creating tasks (use $$ for best results):**
@eis $$ plan a birthday party
@eis $$ break down "Learn Spanish" into steps

Why $$? The $ prefix controls AI power:
• $   = Quick (Haiku) - good for queries
• $$  = Smart (Sonnet) - good for creating tasks
• $$$ = Best (Opus) - complex planning
```

**Note:** The $ tier (Haiku) cannot create tasks - it can only read and query.
Use $$ or higher for task creation.

---

### Stage 4: Pro Mode (Optional)

**Triggered by:** Any AI command
**Creates:** 1 task

```
Title: 🎓 Optional: Enable Pro Mode

Description:
**Ears Mode** makes @eis listen to ALL new tasks in this project.
No need to type @eis - just describe what you want!

To enable: @eis !ears on
To disable: @eis !ears off

Or keep it off and @mention @eis when you need help.
Both ways work great!
```

---

### Stage 5: Complete

**Triggered by:** `@eis !ears on` OR marking Stage 4 task complete
**Creates:** 1 reference card task

```
Title: ✅ You're ready! (quick reference)

Description:
## Vikunja Basics

| Action | How |
|--------|-----|
| Create task | Type + Enter |
| Complete task | Click checkbox |
| Reorder | Drag and drop |
| Delete | Click task → Delete |

## @eis Commands (FREE)

| Command | What it does |
|---------|--------------|
| `@eis !w city` | Weather for any city |
| `@eis !rss url` | RSS feed items |
| `@eis !x 42` | Complete task #42 |
| `@eis !help` | Full documentation |
| `@eis !h` | Quick cheatsheet |
| `@eis !bal` | Check AI credit |

## @eis AI (uses credit)

| Command | What it does |
|---------|--------------|
| `@eis <question>` | AI answers (Haiku, ~1-2¢) |
| `@eis $$ <request>` | AI creates tasks (Sonnet, ~3-5¢) |

## Pro Features

| Command | What it does |
|---------|--------------|
| `@eis !ears on` | Listen to all tasks |
| `@eis !ears off` | Stop listening |
| `@eis !project add Name` | Create new project |

---

Delete this task when you're ready. Enjoy! 🚀
```

---

## AI Tier Restrictions (fa-qld6)

**Important for onboarding content:**

| Tier | Model | Can Create? | Best For |
|------|-------|-------------|----------|
| `$` | Haiku | ❌ No | Queries, summaries, questions |
| `$$` | Sonnet | ✅ Yes | Task creation, planning |
| `$$$` | Opus | ✅ Yes | Complex analysis |

The $ tier (Haiku) is blocked from:
- `create_task`, `batch_create_tasks`
- `create_project`, `create_label`, `create_bucket`
- `create_view`, `setup_kanban_board`

This prevents Haiku from creating duplicate tasks (known issue).

**Onboarding implication:** When teaching AI task creation, always use `$$`:
- ❌ `@eis plan a party` (defaults to $, can't create)
- ✅ `@eis $$ plan a party` (uses $$, can create)

---

## Disabled Commands (DO NOT INCLUDE)

These were in the original design but are now disabled:

| Command | Status | Reason | Bead |
|---------|--------|--------|------|
| `!s TICKER` | DISABLED | API rate limits | solutions-js3e |
| `!n topic` | DISABLED | Unreliable API | solutions-4sni |

**Do not mention these in onboarding content.**

---

## Implementation Components

### 1. User Onboarding State

Store in PostgreSQL (`factumerit_users` or separate table):

```python
onboarding_state = {
    "stage": 2,                    # Current stage (0-5)
    "completed": ["!w", "!bal"],   # Commands done in current stage
    "started_at": "2026-01-15T10:00:00Z",
    "completed_at": None,          # Set when stage 5 reached
}
```

### 2. Onboarding Triggers

| Event | Condition | Action |
|-------|-----------|--------|
| First manual task | stage=0 | Create "Meet @eis" task, stage=1 |
| `!help` | stage=1 | Delete intro, Create 2a+2b, stage=2 |
| `!w *` | stage=2 | Mark !w done, check if both done |
| `!bal` | stage=2 | Mark !bal done, check if both done |
| Both done | stage=2 | Delete remaining, Create AI task, stage=3 |
| Any AI command | stage=3 | Delete AI task, Create pro mode task, stage=4 |
| `!ears on` OR complete | stage=4 | Delete pro task, Create reference card, stage=5 |

### 3. Modified Files

| File | Changes |
|------|---------|
| `signup_workflow.py` | Update welcome task content |
| `notification_poller.py` | Add `_check_onboarding_progress()` |
| `server.py` | Add onboarding state helpers |
| `keyword_handlers.py` | Trigger progression on command completion |

---

## Edge Cases

### Power User Skip-Ahead

If user runs advanced commands before completing challenges:
- Still execute the command normally
- Delete the corresponding challenge task if it exists
- Update onboarding state

### Task Deletion

If user manually deletes a challenge task:
- Treat as "skipped"
- Don't recreate
- Continue progression

### Re-Running Onboarding

If user wants to restart:
- `@eis !welcome` could recreate missing tasks
- Or show: "You're on stage 3. Type `@eis !help` for command reference."

---

## Success Metrics

Track:
- % of users who complete each stage
- Time between stages
- Drop-off points
- Commands used outside challenges (power users)

---

## Changelog

### v2 (2026-01-08)
- Added Vikunja basics layer (Stage 0: create task manually)
- Removed stock (!s) - disabled due to API rate limits
- Removed news (!n) - disabled due to unreliable API
- Removed @e shortcut mention - buggy (fa-pvnw)
- Added AI tier documentation ($ can't create tasks)
- Changed AI challenge to use $$ explicitly
- Made !ears on optional (can complete by marking task done)
- Updated completion reference card
- Acknowledged Factum Erit as visible brand (was hidden)
- Added email as primary interface alongside Vikunja
- Moved Slack to "available on request" (not actively promoted)

### v1 (2026-01)
- Initial design with !welcome flow
