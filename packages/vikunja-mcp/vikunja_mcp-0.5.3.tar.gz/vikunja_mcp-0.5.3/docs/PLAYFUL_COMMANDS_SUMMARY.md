# Playful Commands Summary

**Date**: 2025-12-24
**Status**: Documented in V2 Spec
**Related**: MATRIX_TRANSPORT_SPEC_V2.md, VIKUI_SPEC.md

---

## The Playful Command Set

### 🔥 Task Filters (Quick & Fun)

| Old Command | New Playful | Why It's Fun |
|-------------|-------------|--------------|
| `!overdue` | `!oops` | "Oops, I missed these!" |
| `!today` | `!now` | "What's happening NOW?" |
| `!urgent` | `!fire` | 🔥 Fire drill! |
| `!focus` | `!zen` | 🧘 Zen mode, one task |
| `!unscheduled` | `!maybe` | Someday/maybe (GTD) |
| `!priority` | `!vip` | VIP tasks! |
| `!summary` | `!stats` | 📊 Show me the stats |
| `!week` | `!week` | (kept simple) |

### 🔗 Vikunja Connection

| Old Command | New Playful | Why It's Fun |
|-------------|-------------|--------------|
| `!connect` | `!vik` | Short for "Vikunja" |
| `!disconnect` | `!novik` | "No more vik" |
| `!connections` | `!viki` | Plural of "vik" |

### 📚 Knowledge Base (NEW!) - The Vik Family

| Command | Purpose |
|---------|---------|
| `!vikui <name>` | Bind room to knowledge base |
| `!vikui` | Show current binding |
| `!novikui` | Remove binding |
| `!vikuii` | List available knowledge bases |
| `!viktus` | Show all connection status |

---

## The Magic Formula

```
PROJECT (Vikunja)     = STATE (tasks, deadlines, status)
+
VIKUI (RAG)           = CONTENT (docs, notes, knowledge)
+
CLAUDE (LLM)          = INTELLIGENCE (reasoning, actions)
=
🎯 CONTEXT-AWARE AI WORKSPACE
```

---

## Bot Personality

### Traits
- 🎯 **Helpful** - Always ready to assist
- 😄 **Playful** - Fun command names, emoji, gamification
- 🌿 **Eco-conscious** - Celebrates token savings
- 💪 **Motivating** - Positive reinforcement, no judgment
- 🧘 **Zen** - Helps you focus on what matters

### Voice & Tone
- **Casual but professional** - "Oops!" not "ERROR: OVERDUE_TASKS_FOUND"
- **Encouraging** - "No judgment! Let's get these done."
- **Celebratory** - "Keep crushing it! 💪"
- **Focused** - "Block out distractions. This is what matters."

---

## ECO Streak Gamification

**Concept**: Reward users for using efficient `!commands` instead of LLM queries.

**Milestones**:
- 🌱 Streak 5: "You're getting the hang of this!"
- 🌿 Streak 10: "ECO warrior!"
- 🌳 Streak 25: "Token-saving champion!"
- 🏆 Streak 50: "ECO legend! You've saved ~25,000 tokens!"

**Display**:
```
🌿 ECO streak: 12 | ~6,000 tokens saved

🎉 **ECO warrior!**
```

---

## Backward Compatibility

All old command names still work as aliases:
- `!overdue` → `!oops`
- `!today` → `!now`
- `!urgent` → `!fire`
- `!focus` → `!zen`
- `!unscheduled` → `!maybe`
- `!priority` → `!vip`
- `!summary` → `!stats`
- `!connect` → `!vik`
- `!disconnect` → `!novik`
- `!connections` → `!viki`

Users can use whichever they prefer!

---

## User Experience Examples

### Example 1: Quick Task Check

```
Alice: !oops
eis: 😬 **Oops! You have 3 overdue tasks:**

     [#42] Review PR for auth feature
     Due: Dec 20 (4 days ago)
     
     [#58] Update documentation
     Due: Dec 22 (2 days ago)
     
     [#61] Client meeting prep
     Due: Dec 23 (yesterday)
     
     No judgment! Let's get these done. 💪
     
     🌿 ECO streak: 5 | ~2,500 tokens saved
     
     🎉 **You're getting the hang of this!**
```

### Example 2: Focus Mode

```
Bob: !zen
eis: 🧘 **Zen Mode - Your One Focus Task:**

     [#99] Finish Q4 report
     Due: Today at 5pm
     Priority: 5 (urgent)
     
     Block out distractions. This is what matters.
     
     🌿 ECO streak: 12 | ~6,000 tokens saved
     
     🎉 **ECO warrior!**
```

### Example 3: Fire Drill

```
Charlie: !fire
eis: 🔥 **FIRE DRILL! 2 urgent tasks:**

     [#77] Production bug fix
     Due: Today at 2pm (in 3 hours)
     Priority: 5
     
     [#88] Client demo prep
     Due: Tomorrow at 10am
     Priority: 5
     
     Drop everything. These need attention NOW!
     
     🌿 ECO streak: 3 | ~1,500 tokens saved
```

---

## The Complete Vik Family

```
┌─────────────────────────────────────────────────────────────┐
│                    The Vik Family                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STATE (Vikunja Tasks):                                     │
│    !vik       Connect to Vikunja                            │
│    !novik     Disconnect from Vikunja                       │
│    !viki      List Vikunja instances (plural)               │
│                                                             │
│  CONTENT (Knowledge Bases):                                 │
│    !vikui     Connect to knowledge base                     │
│    !novikui   Disconnect from knowledge base                │
│    !vikuii    List knowledge bases (plural)                 │
│                                                             │
│  STATUS (Connection State):                                 │
│    !viktus    Show all connection status                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Linguistic Pattern:**
- **vik** → **viki** (add 'i' for plural)
- **vikui** → **vikuii** (add 'i' for plural)
- **viktus** = Latin passive perfect participle ("having been connected")

---

## Implementation Status

- ✅ **VIKUI_SPEC.md** - Complete RAG architecture documented
- ✅ **MATRIX_TRANSPORT_SPEC_V2.md** - Updated with playful commands
- ✅ **Help text** - Comprehensive `!help` implementation
- ✅ **ECO streak** - Gamification with milestones
- ✅ **Command mapping** - Both playful and legacy names
- ✅ **The Vik Family** - Complete linguistic system
- ⏳ **Implementation** - Ready to code!

---

**Next Steps**: Implement in Matrix bot! 🚀

