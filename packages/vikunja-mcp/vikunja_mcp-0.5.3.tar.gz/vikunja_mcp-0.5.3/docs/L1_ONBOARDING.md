# L1: Task Management Onboarding

**Status:** Design Draft
**Bead:** solutions-c33n
**Date:** January 2026
**Prerequisite:** L0 Complete (user knows @eis commands)

---

## Onboarding Tiers

| Tier | Focus | Goal |
|------|-------|------|
| L0: Commands | Learn @eis syntax | User knows commands work |
| **L1: Task Management** | Organize with AI | User has working GTD system |
| L2: Productivity | Advanced workflows | AI is user's co-pilot |

See also: `ONBOARDING_FLOW.md` (L0)

---

## Overview

L1 teaches users **task management methodology** with @eis as their AI coach. Instead of teaching commands, we teach concepts:

- Inbox as capture point
- Projects as containers
- Processing (Inbox → Projects)
- Review and prioritization
- AI as thought partner

### Terminology

| Term | What it is | How we refer to it |
|------|------------|-------------------|
| **Vikunja** | The task management UI | "your tasks", "your projects" |
| **@eis** | The AI assistant bot | "I", "me", "your assistant" |
| **Inbox** | Default capture project | "your Inbox" |
| **Project** | Container for related tasks | "project" |

### Design Principles

1. **Teach concepts, not commands** - Focus on "why" not "how"
2. **Learn by doing** - Create real projects, not demos
3. **AI as coach** - @eis guides and suggests, user decides
4. **Build real system** - End with working personal productivity setup
5. **Respect existing users** - Don't force structure on power users

---

## Entry Point

User completes L0 and sees:

```
🎯 Ready for the next level?
Type: @eis let's organize my projects
```

Or user can trigger anytime with natural language like:
- `@eis help me get organized`
- `@eis set up my projects`
- `@eis I want to use GTD`

---

## Flow Diagram

```
L0 Complete
     │
     ▼
┌─────────────────────────────────────┐
│ "@eis let's organize my projects"   │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 1. Understand Your Inbox            │
│    "Your Inbox captures quick       │
│     thoughts. Let's try it."        │
│                                     │
│    Challenge: Capture 3 tasks       │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 2. Create Your First Project        │
│    "Projects group related tasks.   │
│     What area of life needs         │
│     organizing?"                    │
│                                     │
│    Challenge: Create a project      │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 3. Process Your Inbox               │
│    "Move tasks to the right place.  │
│     I can help you decide."         │
│                                     │
│    Challenge: Process Inbox → 0     │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 4. Daily Focus                      │
│    "Ask me what needs attention     │
│     today."                         │
│                                     │
│    Challenge: Ask "what's due?"     │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 5. Weekly Review                    │
│    "Review your week with me.       │
│     I'll help you reflect."         │
│                                     │
│    Challenge: Do a weekly review    │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ ✅ L1 Complete                       │
│    You have a working system!       │
│    Keep using it, I'm here to help. │
└─────────────────────────────────────┘
```

---

## Stage Details

### Entry: "Let's organize my projects"

**Triggered by:** Natural language like "organize", "set up", "GTD"
**Creates:** L1 guide task + Stage 1 challenge

**L1 Guide Task (permanent):**
```
Title: 📋 Your Task Management System

Description:
I'll help you set up a simple system to stay organized.

## The Basics

1. **Inbox** - Capture thoughts quickly
2. **Projects** - Group related tasks
3. **Process** - Move Inbox → Projects daily
4. **Review** - Check in weekly

## Your Progress

Complete the challenges to build your system.
Each step creates something real you'll keep using.

---

Current stage: 1 of 5
```

---

### Stage 1: Understand Your Inbox

**Concept:** Inbox is for quick capture. Don't organize yet, just get it out of your head.

**Challenge Task:**
```
Title: 1️⃣ Capture 3 tasks in your Inbox

Description:
Your Inbox is for quick thoughts. Don't worry about
organizing yet - just capture.

Try adding 3 real tasks. Things like:
- "Call dentist"
- "Buy birthday gift for mom"
- "Research vacation spots"

Just type the task title in the box above.
When you have 3+ tasks, type: @eis done capturing
```

**Completion trigger:** User types "@eis done capturing" or Inbox has 3+ tasks
**Validation:** Check Inbox task count

---

### Stage 2: Create Your First Project

**Concept:** Projects group related tasks. Start with life areas.

**Challenge Task:**
```
Title: 2️⃣ Create a project for one area of your life

Description:
Projects help you see related tasks together.

Common starting projects:
- 🏠 Home
- 💼 Work
- 👤 Personal
- 🎯 Goals

Type: @eis create a project called "Home"
(or whatever area you want to organize first)
```

**Completion trigger:** User creates a project (via @eis or Vikunja UI)
**AI behavior:** When user says "create a project called X", use create_project tool

---

### Stage 3: Process Your Inbox

**Concept:** Review Inbox daily. Each task either: do it, move it, or delete it.

**Challenge Task:**
```
Title: 3️⃣ Process your Inbox to zero

Description:
For each task in your Inbox, decide:
- **Do it** (if < 2 minutes)
- **Move it** to a project
- **Delete it** (if not needed)

Try: @eis move "call dentist" to Home

Or ask me: @eis help me process my inbox
I'll go through each task with you.

Goal: Get Inbox to zero tasks.
```

**Completion trigger:** Inbox has 0 tasks
**AI behavior:**
- "move X to Y" → use move_task tool
- "help me process" → iterate through Inbox tasks, ask about each

---

### Stage 4: Daily Focus

**Concept:** Each day, ask what needs attention. Don't try to see everything.

**Challenge Task:**
```
Title: 4️⃣ Ask me what needs attention today

Description:
Instead of scanning all your tasks, just ask me.

Try any of these:
- @eis what's due today?
- @eis what should I focus on?
- @eis what's overdue?

I'll check your tasks and give you a focused list.
```

**Completion trigger:** User asks a "what's due/overdue/focus" question
**AI behavior:** Use list_tasks with filters, summarize priorities

---

### Stage 5: Weekly Review

**Concept:** Weekly check-in to stay on track. Review, reflect, plan.

**Challenge Task:**
```
Title: 5️⃣ Do a weekly review with me

Description:
Once a week, take 15 minutes to:
1. Process Inbox to zero
2. Review each project
3. Check upcoming deadlines
4. Decide next week's priorities

Type: @eis weekly review

I'll guide you through it.
```

**Completion trigger:** User types "weekly review"
**AI behavior:**
1. Check Inbox count, prompt if > 0
2. List projects, ask if each is on track
3. Show tasks due next 7 days
4. Ask user to pick 3 priorities for the week

---

### Completion

**Deletes:** Stage 5 challenge
**Updates:** L1 Guide task

**Updated L1 Guide:**
```
Title: 📋 Your Task Management System ✅

Description:
You have a working system! Here's what you built:

## Your System

✅ **Inbox** - Capture thoughts fast
✅ **Projects** - Organized by life area
✅ **Daily Focus** - Ask me what's due
✅ **Weekly Review** - Stay on track

## Daily Habits

**Morning:** @eis what should I focus on?
**Evening:** Process Inbox to zero

## Weekly Habit

**Sunday:** @eis weekly review

---

## Quick Commands

- "@eis what's due today?"
- "@eis what's overdue?"
- "@eis move X to Project"
- "@eis weekly review"

---

## Ready for more?

When you're ready to level up:
- Labels and filters
- Task breakdown and subtasks
- Recurring tasks
- Project templates

Type: @eis show me advanced features
```

---

## AI Conversation Examples

### Processing Inbox

```
User: @eis help me process my inbox

@eis: Let's process your Inbox! You have 4 tasks.

**1. "Call dentist"**
- Do it now (< 2 min)?
- Move to a project?
- Delete?

What would you like to do with this one?

User: move to Home

@eis: ✅ Moved "Call dentist" to Home

**2. "Research vacation spots"**
What about this one?

User: let's create a Travel project for that

@eis: ✅ Created project "Travel"
✅ Moved "Research vacation spots" to Travel

**3. "Buy milk"**
This seems quick - do it now or move it?

User: I'll do it now, delete it

@eis: ✅ Deleted "Buy milk"

**4. "Learn Spanish"**
This is a big goal! Want to break it down or just move it?

User: move to Personal for now

@eis: ✅ Moved "Learn Spanish" to Personal

🎉 Inbox is at zero! Great job.
```

### Weekly Review

```
User: @eis weekly review

@eis: # Weekly Review 📋

Let's check in on your week!

## 1. Inbox Check
You have 2 tasks in Inbox. Want to process them now?

User: yes

@eis: [processes inbox interactively]

## 2. Project Review

**🏠 Home** (3 tasks, 1 overdue)
- ⚠️ "Fix leaky faucet" was due 2 days ago
- "Call dentist" due tomorrow
- "Organize garage" no due date

Is this project on track?

User: not really, I keep putting off the faucet

@eis: That happens! Options:
1. Schedule a specific time this week
2. Delegate it (hire someone?)
3. Decide it's not a priority right now

What feels right?

User: schedule it for Saturday morning

@eis: ✅ Set "Fix leaky faucet" due Saturday 9am

**💼 Work** (5 tasks, 0 overdue)
All on track! Anything to add?

User: no

@eis: **👤 Personal** (2 tasks)
...

## 3. Next Week

You have 4 tasks due next week.
Pick your top 3 priorities:

1. Fix leaky faucet (Sat)
2. Call dentist (tomorrow)
3. Quarterly report (Thu)
4. Team lunch planning (Fri)

User: 1, 2, 3

@eis: ✅ Great! Your priorities for this week:
1. Call dentist
2. Fix leaky faucet
3. Quarterly report

I'll remind you of these when you ask "what should I focus on?"

Weekly review complete! 🎉
```

---

## Implementation Components

### 1. L1 State Tracking

```yaml
users:
  "vikunja:username":
    l1_onboarding:
      stage: 3                    # Current stage (1-5)
      guide_task_id: 12345        # L1 guide task
      started_at: "2026-01-15"
      completed_at: null
      projects_created: ["Home", "Work"]
      inbox_processed_count: 2
```

### 2. Natural Language Triggers

| User says | Trigger |
|-----------|---------|
| "organize", "set up", "GTD", "get organized" | Start L1 |
| "done capturing", "finished capturing" | Complete Stage 1 |
| "help me process", "process inbox" | Interactive inbox processing |
| "weekly review" | Guided weekly review |
| "what's due", "what's overdue", "focus" | Daily focus query |

### 3. Tool Usage

| Stage | Tools Used |
|-------|------------|
| Stage 1 | list_tasks (count Inbox) |
| Stage 2 | create_project |
| Stage 3 | list_tasks, move_task, delete_task |
| Stage 4 | list_tasks (with filters) |
| Stage 5 | list_tasks, list_projects, update_task |

### 4. Modified Files

| File | Changes |
|------|---------|
| `llm_handlers.py` | Add L1 system prompts, conversational flows |
| `keyword_handlers.py` | Add triggers for L1 stages |
| `server.py` | Add L1 state helpers |

---

## Success Metrics

- % of L0 completers who start L1
- % who complete all 5 stages
- Time to complete L1
- 7-day retention after L1 completion
- Tasks created per week (before/after L1)
- Inbox processing frequency

---

## Future: L2 Productivity

L2 covers advanced workflows for power users:

- **Labels & Filters** - Custom views
- **Task Breakdown** - "@eis break this into subtasks"
- **Recurring Tasks** - Habits and routines
- **Project Templates** - Reusable structures
- **Time Blocking** - Calendar integration
- **Delegation** - Team features

Trigger: `@eis show me advanced features`

---

## Appendix: Full Conversation Flows

### Interactive Inbox Processing

See "Processing Inbox" example above.

Key behaviors:
- One task at a time
- Offer clear options (do/move/delete)
- Create projects on the fly if needed
- Celebrate at zero

### Weekly Review Script

See "Weekly Review" example above.

Key behaviors:
- Start with Inbox check
- Review each project briefly
- Flag overdue items
- Ask about blockers
- Set 3 priorities for next week
- Keep total time ~15 minutes
