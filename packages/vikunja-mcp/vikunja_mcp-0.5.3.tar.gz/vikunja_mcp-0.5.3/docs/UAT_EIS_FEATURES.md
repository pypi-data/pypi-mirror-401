# @eis User Acceptance Testing (UAT)

**Version:** 2.0
**Date:** January 2026
**Features:** All @eis commands including Capture Mode and One-Click Action Links

---

## Prerequisites

- [ ] Vikunja account with @eis user added to projects
- [ ] Access to https://vikunja.factumerit.app
- [ ] MCP server running at https://mcp.factumerit.app

---

## 1. Info Commands (FREE - No Credit Required)

### 1.1 Weather Command

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Basic weather | `@eis !w Tokyo` | Shows current weather for Tokyo with temp, conditions, humidity | [ ] |
| Weather alias | `@eis !weather Seattle` | Same as !w | [ ] |
| Action bar | (after any !w) | Shows: 🔄 [Refresh] · ✅ [Done] · ⏰ Add `hourly`... | [ ] |
| Refresh link | Click 🔄 [Refresh] | Weather updates, page redirects to task | [ ] |
| Done link | Click ✅ [Done] | Task marked as complete | [ ] |
| With schedule | `@eis !w London hourly` | Creates scheduled task with repeat mode enabled | [ ] |
| Target project | `@eis !w Paris \| Dashboard` | Task created in Dashboard project | [ ] |
| Fuzzy project | `@eis !w Berlin \| dash` | Matches "Dashboard" via fuzzy matching | [ ] |
| Invalid location | `@eis !w xyznonexistent` | Shows error message gracefully | [ ] |

### 1.2 Stock Command (DISABLED FOR LAUNCH)

> **Note:** Stock command disabled due to API rate limits. See solutions-js3e.

### 1.3 News Command (DISABLED FOR LAUNCH)

> **Note:** News command disabled - unreliable API. Use !rss instead. See solutions-4sni.

### 1.4 RSS Command

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Basic RSS | `@eis !rss https://hnrss.org/frontpage` | Shows Hacker News headlines | [ ] |
| Feed alias | `@eis !feed https://xkcd.com/rss.xml` | Same as !rss | [ ] |
| With schedule | `@eis !rss https://hnrss.org/frontpage 6h` | Updates every 6 hours | [ ] |
| Action bar | (after any !rss) | Shows: 🔄 [Refresh] · ✅ [Done] · ⏰ hint | [ ] |
| Invalid URL | `@eis !rss notaurl` | Shows error message gracefully | [ ] |

---

## 2. Action Commands

### 2.1 Complete Command

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Complete single | `@eis !x 42` | Task #42 marked done, command task deleted | [ ] |
| Complete alias | `@eis !complete 42` | Same as !x | [ ] |
| Done alias | `@eis !done 42` | Same as !x | [ ] |
| Multiple tasks | `@eis !x 1 2 3` | Tasks #1, #2, #3 all marked done | [ ] |
| Comma separated | `@eis !x 1,2,3` | Same as above | [ ] |
| Nonexistent task | `@eis !x 999999` | Shows error, task not found | [ ] |

### 2.2 Remind Command (NOT YET IMPLEMENTED)

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Set reminder | `@eis !r 42 / tomorrow 3pm` | Shows "Not yet implemented" message | [ ] |

---

## 3. AI/LLM Commands (Uses Credit)

### 3.1 Natural Language ($ Prefix)

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Simple request | `@eis $ plan a birthday party` | AI generates party planning content | [ ] |
| Medium budget | `@eis $$ write a project proposal` | Uses $$ tier (10 calls max) | [ ] |
| High budget | `@eis $$$ create detailed business plan` | Uses $$$ tier (25 calls max) | [ ] |
| Cost footer | (after any $ command) | Shows cost and balance: "~2¢ \| Balance: $X.XX" | [ ] |
| Refinement | Reply with `@eis add more details` | AI refines previous response | [ ] |

### 3.2 Context Analysis

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Summarize | `@eis $$ 42 / summarize comments` | AI summarizes task #42 comments | [ ] |
| Suggest | `@eis $$ 42 / suggest next steps` | AI suggests actions for task | [ ] |

### 3.3 Natural Language (No Prefix)

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Question | `@eis what's overdue?` | AI uses tools to find overdue tasks | [ ] |
| Create task | `@eis remind me to call mom tomorrow` | Creates task with due date | [ ] |
| Project context | (in specific project) | AI has awareness of current project | [ ] |

---

## 4. Budget Commands

### 4.1 Balance

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Check balance | `@eis !balance` | Shows current credit balance | [ ] |
| Balance alias | `@eis !bal` | Same as !balance | [ ] |
| Credit alias | `@eis !credit` | Same as !balance | [ ] |

### 4.2 Upgrade (on Smart Tasks)

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Upgrade to $$ | `@eis !upgrade $$` | Task budget upgraded to $$ tier | [ ] |
| Upgrade to $$$ | `@eis !upgrade $$$` | Task budget upgraded to $$$ tier | [ ] |

### 4.3 Admin Commands

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Grant self | `@eis !grant $5` | Adds $5 credit to own account | [ ] |
| Grant user | `@eis !grant $10 ivan` | Adds $10 to user "ivan" | [ ] |
| Reset budget | `@eis !reset` | Resets task's LLM counter | [ ] |
| Non-admin grant | (as non-admin) | Shows permission denied error | [ ] |

---

## 5. Meta Commands

### 5.1 Help

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Full help | `@eis !help` | Shows command reference table | [ ] |
| Help alias | `@eis !h` | Same as !help | [ ] |
| Question alias | `@eis !?` | Same as !help | [ ] |
| Topic help | `@eis !help weather` | Shows detailed weather help | [ ] |
| Topic help | `@eis !h stock` | Shows detailed stock help | [ ] |
| Schedule topic | `@eis !help schedule` | Shows schedule options | [ ] |
| Project topic | `@eis !help project` | Shows project syntax help | [ ] |
| Budget topic | `@eis !help budget` | Shows credit/billing info | [ ] |

### 5.2 Find/Cheatsheet

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Cheatsheet | `@eis !find` | Shows common commands quick reference | [ ] |
| Find alias | `@eis !f` | Same as !find | [ ] |
| Cheat alias | `@eis !c` | Same as !find | [ ] |
| With query | `@eis !f overdue` | Filters to relevant commands | [ ] |

---

## 6. Batch Mode (NEW - redesigned)

> **Concept**: Labels = LLM context selectors. Batch mode auto-labels tasks, then processes them together in one LLM call.

### 6.1 Commands

| Test | Command | Expected Result | Pass |
|------|---------|-----------------|------|
| Start batch | `@eis !batch weekly review` | Creates "Weekly Review" task, shows batch ON | [ ] |
| With custom label | `@eis !batch planning --label=plan` | Auto-labels with *plan instead of *batch | [ ] |
| Instance scope | `@eis !batch brain dump --all` | All projects, not just current | [ ] |
| Check status | `@eis !batch status` | Shows count of *batch tasks | [ ] |
| Stop labeling | `@eis !batch off` | Stops auto-labeling, doesn't process | [ ] |
| Process batch | `@eis !batch go` | Processes all *batch tasks in one LLM call | [ ] |
| Process any label | `@eis !batch go *urgent` | Processes all *urgent tasks | [ ] |

### 6.2 Batch Flow

| Test | Steps | Expected Result | Pass |
|------|-------|-----------------|------|
| Full flow | 1. `!batch weekly`<br>2. Create 5 tasks<br>3. `!batch go` | All 5 categorized in one LLM call | [ ] |
| Auto-labeling | Create task while batch ON | Task has *batch label | [ ] |
| Discussion thread | After `!batch go` | Original batch task shows summary | [ ] |
| Follow-up | Comment `@eis $$ advice` on batch task | Gets context from all batch tasks | [ ] |

### 6.3 Label Selection

| Test | Steps | Expected Result | Pass |
|------|-------|-----------------|------|
| Manual label | Label 3 tasks with *review manually | `!batch go *review` processes them | [ ] |
| Mixed sources | Some auto-labeled, some manual | `!batch go` processes all *batch | [ ] |
| Urgent batch | `@eis !batch go *urgent` | Prioritizes/analyzes urgent tasks | [ ] |
| Blocked batch | `@eis !batch go *blocked` | Suggests unblocking strategies | [ ] |

---

## 7. One-Click Action Links (NEW)

### 7.1 Action Bar Components

| Test | Location | Expected Links | Pass |
|------|----------|----------------|------|
| Weather task | After !w command | 🔄 [Refresh] · ✅ [Done] · ⏰ hint | [ ] |
| Stock task | After !s command | 🔄 [Refresh] · ✅ [Done] · ⏰ hint | [ ] |
| News task | After !n command | 🔄 [Refresh] · ✅ [Done] | [ ] |
| RSS task | After !rss command | 🔄 [Refresh] · ✅ [Done] · ⏰ hint | [ ] |
| Scheduled task | After !w Tokyo hourly | 🔄 [Refresh] · ✅ [Done] (no schedule hint) | [ ] |

### 7.2 Link Functionality

| Test | Action | Expected Result | Pass |
|------|--------|-----------------|------|
| Refresh weather | Click 🔄 [Refresh] on weather task | Weather updates, redirects to task | [ ] |
| Refresh stock | Click 🔄 [Refresh] on stock task | Stock updates, redirects to task | [ ] |
| Complete via link | Click ✅ [Done] on any task | Task marked done, redirects to task | [ ] |
| Capture off | Click [Turn off] in capture footer | Capture disabled, redirects to project | [ ] |

### 7.3 Security

| Test | Action | Expected Result | Pass |
|------|--------|-----------------|------|
| Invalid token | Modify token in URL | Returns 401 Unauthorized | [ ] |
| Wrong task ID | Change task ID keeping token | Returns 401 Unauthorized | [ ] |

---

## 8. Status Labels

| Label | Meaning | When Applied | Pass |
|-------|---------|--------------|------|
| ⏳ | Processing | While @eis is working | [ ] |
| 🤖 | Success | After successful processing | [ ] |
| 💬 | Needs Input | When @eis asks a question | [ ] |
| ❌ | Error | When command fails | [ ] |

---

## 9. Edge Cases & Error Handling

| Test | Scenario | Expected Result | Pass |
|------|----------|-----------------|------|
| Empty command | `@eis` (no command) | Treated as natural language or shows help | [ ] |
| Typo tolerance | `@eis !wether Tokyo` | Fuzzy matches to !weather | [ ] |
| Invalid command | `@eis !invalidcmd` | Shows "Unknown command" error | [ ] |
| Project not found | `@eis !w Tokyo \| NonExistent` | Shows available projects to choose | [ ] |
| Multiple project matches | `@eis !w Tokyo \| In` | Shows matching projects as links | [ ] |
| Out of credit | Use $ command with $0.00 balance | Shows "Out of AI credit" message | [ ] |
| API timeout | (simulate slow API) | Shows timeout error gracefully | [ ] |

---

## 10. Integration Tests

### 10.1 End-to-End Flows

| Test | Steps | Expected | Pass |
|------|-------|----------|------|
| Weather → Complete | 1. `@eis !w Tokyo`<br>2. Click ✅ [Done] | Task completed via link | [ ] |
| Ears → Process → Off | 1. `@eis !ears on`<br>2. Create task<br>3. Click [Turn off] | Full ears cycle works | [ ] |
| Stock → Refresh → Schedule | 1. `@eis !s AAPL`<br>2. Refresh<br>3. Create with hourly | Upgrade path works | [ ] |

### 10.2 Concurrent Operations

| Test | Steps | Expected | Pass |
|------|-------|----------|------|
| Multiple ears | Enable ears in 2 projects | Both process independently | [ ] |
| Rapid tasks | Create 5 tasks quickly in ears project | All processed within ~2 minutes | [ ] |

---

## Test Summary

| Category | Total Tests | Passed | Failed |
|----------|-------------|--------|--------|
| Info Commands | 26 | | |
| Action Commands | 7 | | |
| AI/LLM Commands | 10 | | |
| Budget Commands | 8 | | |
| Meta Commands | 12 | | |
| Ears Mode | 11 | | |
| One-Click Links | 9 | | |
| Status Labels | 4 | | |
| Edge Cases | 8 | | |
| Integration | 5 | | |
| **TOTAL** | **100** | | |

---

## Notes

- All `!` commands are FREE (no credit used)
- `$` commands use AI credit (~1-15¢ per request)
- Ears mode only processes tasks created AFTER `!ears on`
- One-click links use secure tokens (HMAC-SHA256)
- Fuzzy matching works for commands and project names

---

## Changelog

- **v2.0** (Jan 2026): Added Ears Mode (renamed from Capture), One-Click Action Links
- **v1.0** (Dec 2025): Initial UAT document
