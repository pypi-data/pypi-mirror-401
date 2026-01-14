# UAT: Focused Filter Tools

**Date**: 2025-12-20
**Deploy**: Render auto-deploy from commit 865b964
**Wait**: ~2-3 min for Render to deploy

---

## Prerequisites

1. Have tasks in Vikunja with various states:
   - Some overdue (due date in past)
   - Some due today
   - Some due this week
   - Some with priority 3+
   - Some with priority 4+
   - Some with no due date
   - Some completed (to verify exclusion)

2. Connected to Factum Erit bot with valid token

---

## Test Cases

### 1. overdue_tasks

**Prompt**: "What's overdue?"

**Expected**:
- Bot calls `overdue_tasks` tool
- Returns only tasks with due date < now
- Does NOT include completed tasks
- Does NOT include tasks with no due date

**Verify**:
- [ ] Only past-due tasks shown
- [ ] Completed tasks excluded
- [ ] Response includes task titles, due dates

---

### 2. due_today

**Prompt**: "What's due today?" or "What should I focus on today?"

**Expected**:
- Bot calls `due_today` tool
- Returns overdue + due today tasks
- Sorted by priority then due date

**Verify**:
- [ ] Overdue tasks included
- [ ] Today's tasks included
- [ ] Tomorrow's tasks excluded
- [ ] High priority shown first

---

### 3. due_this_week

**Prompt**: "What's due this week?"

**Expected**:
- Bot calls `due_this_week` tool
- Returns tasks due in next 7 days + overdue

**Verify**:
- [ ] Tasks due in 1-7 days included
- [ ] Overdue included
- [ ] Tasks due in 8+ days excluded

---

### 4. high_priority_tasks

**Prompt**: "What are my high priority tasks?" or "Show important tasks"

**Expected**:
- Bot calls `high_priority_tasks` tool
- Returns tasks with priority >= 3
- Across all instances

**Verify**:
- [ ] Priority 3, 4, 5 tasks shown
- [ ] Priority 0, 1, 2 tasks excluded
- [ ] Works across multiple Vikunja instances (if configured)

---

### 5. urgent_tasks

**Prompt**: "What's urgent?" or "Show critical tasks"

**Expected**:
- Bot calls `urgent_tasks` tool
- Returns tasks with priority >= 4 only

**Verify**:
- [ ] Only priority 4, 5 tasks shown
- [ ] Priority 3 and below excluded

---

### 6. unscheduled_tasks

**Prompt**: "What tasks have no due date?" or "Show unscheduled tasks"

**Expected**:
- Bot calls `unscheduled_tasks` tool
- Returns tasks with no due date set

**Verify**:
- [ ] Tasks without due dates shown
- [ ] Tasks with dates excluded
- [ ] Useful for backlog review

---

### 7. upcoming_deadlines

**Prompt**: "What's coming up in the next 3 days?" or "Show deadlines for next 5 days"

**Expected**:
- Bot calls `upcoming_deadlines` tool with days parameter
- Returns tasks due in next N days (default 3)
- Does NOT include overdue (unlike due_today)

**Verify**:
- [ ] Default 3 days works
- [ ] Custom days parameter works ("next 5 days")
- [ ] Overdue tasks NOT included
- [ ] Today's tasks included

---

### 8. focus_now

**Prompt**: "What should I work on?" or "What needs my attention?"

**Expected**:
- Bot calls `focus_now` tool
- Returns: high priority (>=3) OR due today/overdue
- Sorted by priority first, then due date

**Verify**:
- [ ] High priority tasks with no date included
- [ ] Low priority but due today included
- [ ] Low priority future tasks excluded
- [ ] Good "what's actionable" view

---

## Performance Check

For each tool, note:
- Response time (should be 2-5 seconds including LLM)
- Token usage shown in response (if enabled)

---

## Edge Cases

### Empty Results
**Prompt**: Test when no tasks match (e.g., nothing overdue)

**Expected**: Graceful message like "No overdue tasks found"

### Large Result Set
**Prompt**: If many tasks match a filter

**Expected**:
- Results should be paginated or truncated
- No timeout errors

### Multi-Instance
**Prompt**: "What's overdue across all my Vikunja instances?"

**Expected**:
- Results grouped by instance
- `by_instance` field in response

---

## Sign-Off

| Tester | Date | Result |
|--------|------|--------|
| | | |

**Notes**:
