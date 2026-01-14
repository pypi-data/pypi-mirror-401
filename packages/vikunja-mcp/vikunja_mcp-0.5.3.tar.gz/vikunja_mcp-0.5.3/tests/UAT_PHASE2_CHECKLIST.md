# UAT Checklist: Smart Tasks Phase 2

**Date:** 2025-12-30
**Bead:** solutions-hgwx.2
**Tester:** _______________

## Prerequisites

- [ ] Vikunja instance running
- [ ] @eis user account exists
- [ ] Notification poller running (`python -m vikunja_mcp.notification_poller`)

---

## Test 1: Cost Tier Parsing

### 1.1 Tier 1 ($) - Natural Language
Create task with title:
```
@eis $ create a sourdough baking project
```

**Expected:**
- [ ] Task is processed by poller
- [ ] Comment posted with LLM placeholder response
- [ ] Response includes cost footer: `LLM calls: 1/30 ($0.01)`

### 1.2 Tier 1 ($$) - Medium Cost
Create task with title:
```
@eis $$ analyze my project structure
```

**Expected:**
- [ ] Response includes: `LLM calls: 1/150`
- [ ] Cost tier shown as $$

### 1.3 Tier 1 ($$$) - High Cost
Create task with title:
```
@eis $$$ research best practices for API design
```

**Expected:**
- [ ] Response includes: `LLM calls: 1/600`
- [ ] Cost tier shown as $$$

---

## Test 2: Tier 2 - LLM with Task Context

### 2.1 Analyze Existing Task
1. Note the ID of an existing task (e.g., #42)
2. Create task with title:
```
@eis $$ 42 / summarize the description
```

**Expected:**
- [ ] Response mentions task #42
- [ ] Response includes task title
- [ ] Cost footer present

### 2.2 Invalid Task Reference
Create task with title:
```
@eis $$ "Some Task Name" / summarize
```

**Expected:**
- [ ] Error: "Fuzzy search not yet implemented"

---

## Test 3: Budget Management

### 3.1 Upgrade Tier
On a smart task, create comment:
```
@eis !upgrade $$
```

**Expected:**
- [ ] Response: "Upgraded from $ to $$"
- [ ] New limit: 150 calls

### 3.2 Reset Budget
On a smart task with usage, create comment:
```
@eis !reset-budget
```

**Expected:**
- [ ] Response: "Reset budget... Now: 0/X calls"

### 3.3 Reset Alias
```
@eis !reset
```

**Expected:**
- [ ] Same behavior as !reset-budget

---

## Test 4: YAML Frontmatter

### 4.1 Check Metadata in Description
After a $ command succeeds, check task description.

**Expected format:**
```yaml
---
smart_task: true
cost_tier: $
llm_calls_used: 1
llm_calls_limit: 30
total_cost: 0.01
prompt: "original prompt here"
created_at: "2025-12-30T..."
---

[LLM response content here]
```

- [ ] Frontmatter present
- [ ] `smart_task: true` exists
- [ ] `cost_tier` matches command
- [ ] `llm_calls_used` increments
- [ ] Content below frontmatter

---

## Test 5: Budget Warnings

### 5.1 Near Exhaustion Warning
Create a smart task, then manually edit description to set:
```yaml
llm_calls_used: 28
llm_calls_limit: 30
```

Trigger another update.

**Expected:**
- [ ] Footer shows: "2 calls remaining"

### 5.2 Budget Exhaustion
Set `llm_calls_used: 30` in description.

Trigger another update.

**Expected:**
- [ ] Error: "Budget exhausted (30/30 calls, $0.30)"
- [ ] Options shown: !upgrade, !reset-budget, !disable

---

## Test 6: Automated Tests

Run automated UAT script:
```bash
cd ~/factumerit/backend
.venv/bin/python tests/uat_phase2_cost_tiers.py
```

**Expected:**
- [ ] All 44 tests pass
- [ ] Exit code 0

---

## Test Summary

| Test | Pass | Fail | Notes |
|------|------|------|-------|
| 1.1 Tier 1 ($) | | | |
| 1.2 Tier 1 ($$) | | | |
| 1.3 Tier 1 ($$$) | | | |
| 2.1 Tier 2 context | | | |
| 2.2 Fuzzy name error | | | |
| 3.1 !upgrade | | | |
| 3.2 !reset-budget | | | |
| 3.3 !reset alias | | | |
| 4.1 YAML frontmatter | | | |
| 5.1 Near exhaustion | | | |
| 5.2 Exhaustion error | | | |
| 6 Automated script | | | |

**Overall Result:** ☐ PASS / ☐ FAIL

**Sign-off:** _______________ Date: _______________

---

## Notes / Issues Found

```
(Write any issues or observations here)
```
