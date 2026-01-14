# AI Workflow Pattern: Multi-Agent Development with Code Review

**Status**: Active
**Created**: 2025-12-24
**Pattern**: Other Agent (Implementation) → Augment (Review + Closer) → Human (Approval)

---

## Overview

This document describes our multi-agent AI development workflow, where different AI agents are used for different phases of development based on their strengths, with Augment serving as the "senior developer" reviewer and closer.

## The Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                   AI Development Workflow                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: SPECIFICATION                                     │
│    Agent: Cursor, Windsurf, Cline, or other                │
│    Output: Specs, documentation, design docs               │
│                                                             │
│  Phase 2: IMPLEMENTATION                                    │
│    Agent: Cursor, Windsurf, Cline, or other                │
│    Output: Code, tests, boilerplate                        │
│    Strength: Speed, well-known patterns                    │
│                                                             │
│  Phase 3: CODE REVIEW                                       │
│    Agent: Augment                                           │
│    Tool: auggie --print "Review this PR: ${link}"          │
│    Strength: Context engine, cross-file reasoning          │
│    Output: Review findings, architectural feedback         │
│                                                             │
│  Phase 4: CLOSER                                            │
│    Agent: Augment                                           │
│    Role: Senior developer                                   │
│    Tasks:                                                   │
│      - Patch issues found in review                        │
│      - Fix integration problems                            │
│      - Ensure architectural consistency                    │
│      - Update downstream call sites                        │
│      - Create rules for future work                        │
│                                                             │
│  Phase 5: APPROVAL                                          │
│    Agent: Human                                             │
│    Tasks: Final review, merge decision, trade-offs         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why This Pattern Works

### Mirrors Real-World Team Dynamics

| Role | Human Team | AI Team |
|------|------------|---------|
| **Junior Developer** | Fast implementation, misses context | Other agents (Cursor, etc.) |
| **Senior Developer** | Code review, architectural guidance | Augment |
| **Tech Lead** | Final approval, strategic decisions | Human |

### Plays to Each Tool's Strengths

**Other Agents Excel At**:
- ✅ Spec writing - Clear, structured documentation
- ✅ Boilerplate code - Standard patterns, well-known implementations
- ✅ Isolated tasks - Single-file changes, well-defined functions
- ✅ Speed - Fast iteration, quick prototypes

**Augment Excels At**:
- ✅ Context-heavy review - Understanding how code fits into larger system
- ✅ Cross-file reasoning - Catching integration issues
- ✅ Architectural consistency - Ensuring patterns match existing code
- ✅ Finding all instances - Catching missed edge cases, all call sites
- ✅ Senior dev perspective - High-level design review

## Implementation

### 1. Setup Augment Code Review

Install Augment CLI:
```bash
npm install -g @augmentcode/auggie
```

### 2. Create Review Rules

Store rules in `.augment/rules/` as Markdown files.

Example: `.augment/rules/matrix-bot-review.md`

```markdown
# Matrix Bot Review Checklist

## Integration
- Doesn't break existing Slack functionality
- All 58 MCP tools properly integrated
- Config changes are backwards compatible

## Security
- Admin commands protected by MATRIX_ADMIN_IDS check
- No hardcoded secrets
- E2EE validation in place
- Input sanitization for user commands

## Consistency
- Matches existing error handling patterns
- Follows established logging conventions
- Response formatting matches Slack bot style
- ECO streak tracking uses existing patterns

## Completeness
- All playful commands implemented
- DM privacy model implemented
- Thinking indicators work
- Reconnection logic handles edge cases
```

### 3. Handoff Protocol

When other agent completes implementation:

```bash
# 1. Other agent commits code
git commit -m "feat: Implement Matrix bot login handler"

# 2. Augment reviews
auggie --print "Review this PR: ${link}" --rules .augment/rules/

# 3. Augment patches issues
# (Use context engine to find all downstream impacts)

# 4. Augment updates rules
# (Add new patterns to prevent future issues)

# 5. Augment commits fixes
git commit -m "fix: Address code review findings"

# 6. Human approves and merges
```

### 4. Measure Effectiveness

Track "Effective Rate" - percentage of findings that are genuinely useful:

| Review | Findings | Useful | Harmless | Wrong | Effective Rate |
|--------|----------|--------|----------|-------|----------------|
| solutions-baft | 12 | 10 | 1 | 1 | 83% |
| solutions-6c21 | 15 | 13 | 2 | 0 | 87% |


## Augment as "Closer" - The Senior Dev Role

The "closer" role is critical in this workflow. Augment acts as the senior developer who:

### Responsibilities

1. **Architectural Review**
   - Does this fit our design patterns?
   - Will this scale?
   - Are there better approaches?
   - What are the trade-offs?

2. **Integration Fixes**
   - Find all downstream call sites that need updates
   - Ensure changes don't break existing functionality
   - Update tests affected by changes
   - Verify configuration changes are safe

3. **Knowledge Transfer**
   - Create rules in `.augment/rules/` for other agents to learn from
   - Document patterns in ADRs
   - Update specs based on learnings
   - Build institutional knowledge

4. **Risk Assessment**
   - What could go wrong?
   - What are the edge cases?
   - What's the blast radius?
   - What security implications exist?

5. **Quality Gate**
   - Prevent issues from reaching production
   - Catch integration problems early
   - Ensure consistency with existing codebase
   - Validate security implementations

### Why Augment is Perfect for This Role

- **Context Engine**: Sees the entire codebase, understands relationships
- **Cross-File Reasoning**: Can find all instances of patterns, all call sites
- **Architectural Awareness**: Understands design patterns across the system
- **Consistency Checking**: Matches existing code style, error handling, logging
- **Completeness**: Finds missed edge cases, forgotten updates

## Iterative Learning Loop

This workflow creates a continuous improvement cycle:

```
Other Agent writes code
    ↓
Augment reviews, finds issues
    ↓
Human creates rules in .augment/rules/
    ↓
Other Agent learns from rules (via prompts)
    ↓
Fewer issues next time
    ↓
Augment focuses on higher-level review
    ↓
Code quality improves over time
```

### Treating Rules as Living Code

From Augment's blog post on code review:

> "Treat rules like living code. If a rule repeatedly misfires, treat it like a bug"

**Process**:
1. Reproduce locally with the same diff/context
2. Decide: refine the rule, add context, whitelist, or accept the finding
3. Ship a small rule change (commit + PR) and canary it to one team
4. Review rules regularly

**Best Practice**: Create a dedicated channel (e.g., `#augment-hypercare`) where engineers flag issues and discuss improvements.

## ROI Calculation

### Time Saved

**Before** (no code review):
- 5 issues slip to production per sprint
- 2 hours debugging each = 10 hours
- Cost: 10 hours × $100/hr = **$1,000**

**After** (Augment review):
- 4 issues caught in review
- 10 minutes to fix each = 40 minutes
- 1 issue slips to production = 2 hours
- Cost: 2.67 hours × $100/hr = **$267**

**Savings**: **$733 per sprint** or **~$19,000 per year**

### Metrics to Track

Post 2-week pilot, gather:
- Number of PRs reviewed (Y)
- Average iterations per PR
- Average reviewer minutes per PR (M)
- Effective Rate (% useful findings)
- Acceptance rate

**Directional math**:
- Minutes saved per PR ≈ reduction in reviewer minutes (X)
- Weekly minutes saved = X × Y
- Weekly hours = (X × Y) / 60
- Weekly $ saved = weekly hours × avg reviewer hourly rate
- Annualize for high-level estimate

## When to Use Which Agent

### Use Other Agents (Cursor, Windsurf, Cline) For:

- ✅ Writing specifications
- ✅ Boilerplate code generation
- ✅ Isolated, well-defined tasks
- ✅ Quick prototypes
- ✅ Standard patterns (CRUD, API endpoints)
- ✅ Single-file changes

### Use Augment For:

- ✅ Code review (context-heavy)
- ✅ Integration tasks (cross-file changes)
- ✅ Architectural decisions
- ✅ Finding all downstream impacts
- ✅ Ensuring consistency with existing code
- ✅ Security review
- ✅ "Closing" implementations (patching issues)

### Use Human For:

- ✅ Final approval and merge decisions
- ✅ Strategic architectural decisions
- ✅ Trade-off evaluation
- ✅ Business logic validation
- ✅ Creating new rules based on review findings

## Example: Matrix Bot Implementation

### Phase 1-2: Other Agent (Implementation)

**Tasks**:
- solutions-3k2u: Add matrix-nio dependency ✓
- solutions-baft: Bot login and connection handler ✓
- solutions-6c21: Message handler and command parser ✓
- solutions-jgy3: Response formatter and sender ✓
- solutions-ui4s: Admin command protection ✓

**Output**: Working implementation, all tests pass

### Phase 3: Augment (Code Review)

**Command**:
```bash
auggie --print "Review Matrix bot implementation in vikunja-slack-bot/" \
  --rules .augment/rules/matrix-bot-review.md
```

**Focus Areas**:
1. Integration with existing Slack bot
2. All 58 MCP tools properly integrated
3. Security implementations (admin protection, E2EE validation)
4. Consistency with existing patterns
5. Error handling and edge cases

**Expected Findings**:
- Missing error handling in reconnection logic
- Inconsistent logging format
- Missed call site in config loader
- Security: Admin check missing in one command
- Performance: Synchronous operation blocking event loop

### Phase 4: Augment (Closer)

**Tasks**:
- Patch all issues found in review
- Update all downstream call sites
- Add missing tests
- Update documentation
- Create rules to prevent future issues

**Output**: Production-ready code

### Phase 5: Human (Approval)

**Tasks**:
- Review Augment's fixes
- Validate trade-offs
- Approve and merge
- Deploy to production

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Augment Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  augment-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Augment CLI
        run: npm install -g @augmentcode/auggie

      - name: Run Augment Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          auggie --print "Review this PR: ${{ github.event.pull_request.html_url }}" \
            --rules .augment/rules/
```

### Conditional Execution

Only run on specific labels or file patterns:

```yaml
- name: Run Augment Review
  if: contains(github.event.pull_request.labels.*.name, 'augment-review')
  # ... rest of step
```

## Best Practices

### 1. Start Small

- Begin with 5-10 high-confidence rules
- Run against 10-20 recent PRs
- Measure Effective Rate
- Iterate and expand

### 2. Keep Reviews Focused

- One concise summary comment
- Only a few high-confidence inline comments per PR
- Avoid overwhelming reviewers

### 3. Make Feedback Visible

- Create dedicated channel for review discussions
- Encourage engineers to flag issues
- Treat rule adjustments like bug fixes

### 4. Canary Rollout

- Start with one team
- Measure and refine
- Expand to other teams once proven

### 5. Review Rules Regularly

- Schedule monthly rule review
- Remove outdated rules
- Add new patterns as codebase evolves

## References

- [Augment Code Review Blog Post](https://www.augmentcode.com/blog/using-the-auggie-cli-for-automated-code-review)
- [Augment CLI Documentation](https://docs.augmentcode.com/cli/overview)
- [GitHub Actions Workflows](https://github.com/augmentcode/review-pr)
- `MATRIX_SECURITY.md` - Security checklist for Matrix bot
- `solutions-frik` - Code review task for Matrix bot

---

**Last Updated**: 2025-12-24
**Pattern Status**: Active, proven effective
**Next Review**: After Matrix bot production deployment

**Goal**: Effective Rate > 80%

If lower, refine rules or prompts.


