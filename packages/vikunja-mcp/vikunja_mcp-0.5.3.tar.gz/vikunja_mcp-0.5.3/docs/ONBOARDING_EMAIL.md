# Email Onboarding Path

**Status:** Design Draft
**Bead:** fa-2xrs
**Last Updated:** 2026-01-08

---

## Overview

Email-first onboarding for users who prefer email over web UI. Users can interact with @eis entirely through email replies - no Vikunja login required.

**Key difference from web path:** Users never need to open Vikunja. Everything happens in their inbox.

---

## Why Email-First?

1. **Lower friction** - Reply to email vs. learn new UI
2. **Mobile-friendly** - Works from phone email app
3. **Familiar** - Everyone knows how to reply to email
4. **Async** - Process tasks when convenient
5. **No login** - No password to remember, no session to manage

---

## Current State

The onboarding email (`email_service.py:send_onboarding_email`) currently:
- Sends username/password
- Points to Vikunja login
- Shows example `@eis` task syntax
- Says "Reply to this email" but doesn't explain what happens

**Gap:** The email doesn't teach email-as-interface. It assumes Vikunja is the primary path.

---

## Proposed Email Flow

### Email 1: Welcome (sent on signup)

**Subject:** Welcome to Factumerit, {name}!

**Key changes from current:**
- Lead with "Reply to try @eis" not "Log in to Vikunja"
- Show email commands that work right now
- Make Vikunja login optional/secondary
- Include action links for instant wins

```html
Hi {name},

Welcome to Factumerit! Your AI assistant @eis is ready.

**Try it now - just reply to this email:**

Reply with: !w Seattle
→ Get weather for any city

Reply with: What's on my plate?
→ AI will check your tasks

Reply with: !bal
→ Check your AI credit ($1.00 free)

That's it! @eis reads your replies and responds.

---

**Want more? Try these:**

• "Add task: Buy groceries" → Creates a task
• "!help" → See all commands
• "$$ plan a birthday party" → AI creates a task list

---

**Prefer a web interface?**

You can also use Vikunja, your task manager:

Login: {vikunja_url}
Username: {username}
Password: {password}

Save this email for your credentials.

---

Questions? Just reply. I'm here to help.

— @eis
```

### Email 2: First Response (after first reply)

When user replies for the first time, @eis responds with:
1. The answer to their command
2. A gentle nudge toward next steps

```
[Weather for Seattle: 52°F, cloudy...]

---

Nice! You just used @eis via email.

A few more things you can do:
• Reply "!h" for a quick command cheatsheet
• Reply "What should I focus on?" for AI suggestions
• Or just describe what you need - I'll figure it out

Your replies go directly to @eis. No login needed.
```

### Email 3: Follow-up (optional, after 24-48h of inactivity)

If user hasn't engaged after initial reply:

**Subject:** Quick tip from @eis

```
Hi {name},

Just checking in! Here's a quick tip:

You can manage tasks entirely from your inbox:

• "Add task: Call mom" → Creates a task
• "What's overdue?" → Shows late tasks
• "Complete: Call mom" → Marks it done

Reply anytime. I'm always listening.

— @eis
```

---

## Email Commands Reference

Commands that work via email reply:

| Command | What it does | Example |
|---------|--------------|---------|
| `!w city` | Weather | `!w Tokyo` |
| `!bal` | Check AI credit | `!bal` |
| `!h` | Quick cheatsheet | `!h` |
| `!help` | Full docs | `!help` |
| `Add task: X` | Create task | `Add task: Buy milk` |
| `What's overdue?` | Query tasks | Natural language |
| `$$ request` | AI creates tasks | `$$ plan a trip to Japan` |

**Note:** The `$$` prefix is needed for task creation (same as web).

---

## Action Links

The welcome email can include signed action links for instant wins:

| Action | Link | Description |
|--------|------|-------------|
| Check weather | `/do/{token}` | Pre-filled !w for their city |
| See tasks | `/do/{token}` | Opens task summary |
| Create sample | `/do/{token}` | Creates a demo task |

These use the email action service (`email_actions.py`) - click to execute without login.

---

## Implementation

### Changes to `email_service.py`

1. **Rewrite `send_onboarding_email`:**
   - Lead with email interaction, not Vikunja login
   - Show reply-based commands prominently
   - Make credentials secondary (still included)

2. **Add `send_followup_email`:**
   - Triggered 24-48h after signup if no engagement
   - Gentle reminder with quick tips

### Changes to `email_inbound.py`

1. **Track first reply:**
   - Flag user's first email interaction
   - Include onboarding tips in first response

2. **Add onboarding state:**
   - `email_onboarding_stage`: 0 (new), 1 (first reply), 2 (engaged)
   - Customize responses based on stage

### New: Engagement Tracking

```python
# In factumerit_users or separate table
email_engagement = {
    "first_email_sent": "2026-01-08T10:00:00Z",
    "first_reply_at": None,  # Set on first reply
    "reply_count": 0,
    "last_reply_at": None,
    "followup_sent": False,
}
```

---

## Success Metrics

Track:
- % of users who reply to welcome email
- Time to first reply
- Commands used via email vs web
- Users who never log into Vikunja (email-only)
- Drop-off after welcome email

---

## Edge Cases

### User replies with garbage
- @eis: "I didn't understand that. Try `!help` for commands, or just describe what you need."

### User replies to old email
- Still works - email threading handles context

### User has no tasks yet
- "What's overdue?" → "You don't have any tasks yet. Reply 'Add task: something' to create your first one."

### User exhausts credit
- Show balance warning, explain `!` commands are free

---

## Relationship to Web Onboarding

| Aspect | Web Path (ONBOARDING_FLOW.md) | Email Path (this doc) |
|--------|------------------------------|----------------------|
| Entry | Signup → Inbox task | Signup → Welcome email |
| Interaction | Create tasks in UI | Reply to emails |
| Login required | Yes (for web) | No (email only) |
| Commands | Same | Same |
| AI tiers | Same ($, $$, $$$) | Same |
| Progression | Task-based stages | Reply-based engagement |

Users can switch between paths anytime. The commands are identical.

---

## Open Questions

1. **Should welcome email include password at all?** If we're pushing email-first, credentials are noise.
   - Option A: Include (current) - users can log in if they want
   - Option B: Separate email - "Your Vikunja credentials" sent only if requested
   - **Recommendation:** Keep in welcome email but de-emphasize

2. **Follow-up email timing?**
   - 24h? 48h? Only if no reply?
   - **Recommendation:** 48h, only if no email engagement

3. **Action links in welcome email?**
   - Risk: Complexity, link tracking
   - Benefit: Instant wins without typing
   - **Recommendation:** Start without, add if reply rates are low

---

## Changelog

### v1 (2026-01-08)
- Initial design for email-first onboarding path
