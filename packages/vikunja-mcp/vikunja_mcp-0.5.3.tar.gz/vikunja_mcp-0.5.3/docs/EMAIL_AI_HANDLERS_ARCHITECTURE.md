# Email AI Handlers Architecture

Design document for multiple AI-powered email addresses on factumerit.app.

**Status:** Draft
**Bead:** fa-14gj
**Last updated:** 2026-01-08

## Overview

The email inbound system currently supports one AI handler (`eis`). This document describes the architecture for supporting multiple AI email handlers with different personas, capabilities, and routing logic.

## Current State

```yaml
# config/email_routing.yaml
routes:
  eis:
    action: eis    # Hardcoded to @eis command processor
```

The `eis` action in `email_inbound.py`:
1. Looks up sender in `personal_bots` table
2. Parses reply text (strips quoted content)
3. Routes to `CommandParser` → `KeywordHandlers`
4. Sends response via Resend

## Proposed Architecture

### Route Configuration

```yaml
routes:
  # AI handlers
  eis:
    action: ai
    handler: eis
    description: Personal AI assistant - full @eis capabilities

  support:
    action: ai
    handler: support
    config:
      escalate_to: help@factumerit.app
      max_turns: 3
    description: Tier 1 support - FAQs, basic help, escalation

  onboard:
    action: ai
    handler: onboard
    config:
      welcome_project: "Getting Started"
    description: New user onboarding assistant

  triage:
    action: ai
    handler: triage
    config:
      labels: [bug, feature, question, urgent]
      route_to: admin@factumerit.app
    description: Categorize and route incoming mail

  digest:
    action: ai
    handler: digest
    config:
      schedule: "daily"
    description: Summarize activity, send reports

  # Non-AI routes
  admin:
    action: forward
    destination: ivan@ivantohelpyou.com
```

### Handler Interface

```python
# src/vikunja_mcp/email_handlers/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class EmailContext:
    """Context passed to AI handlers."""
    email: InboundEmail
    sender_user: Optional[dict]      # From personal_bots lookup
    parsed_message: str              # Reply text, quotes stripped
    config: dict                     # Handler-specific config from YAML
    conversation_history: list       # Previous emails in thread (if any)

@dataclass
class HandlerResult:
    """Result from AI handler."""
    response_text: str               # Plain text response
    response_html: Optional[str]     # HTML response (optional)
    should_respond: bool = True      # False to suppress email response
    forward_to: Optional[str] = None # Escalate/route to another address
    metadata: dict = None            # For logging/analytics

class EmailHandler(ABC):
    """Base class for AI email handlers."""

    @abstractmethod
    async def handle(self, ctx: EmailContext) -> HandlerResult:
        """Process email and return response."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Handler identifier (matches YAML config)."""
        pass
```

### Handler Registry

```python
# src/vikunja_mcp/email_handlers/registry.py

from typing import Dict, Type
from .base import EmailHandler

_handlers: Dict[str, Type[EmailHandler]] = {}

def register(handler_class: Type[EmailHandler]):
    """Decorator to register a handler."""
    _handlers[handler_class.name] = handler_class
    return handler_class

def get_handler(name: str, config: dict) -> EmailHandler:
    """Instantiate handler by name."""
    if name not in _handlers:
        raise ValueError(f"Unknown handler: {name}")
    return _handlers[name](config)
```

### Example Handlers

#### EIS Handler (existing functionality)

```python
# src/vikunja_mcp/email_handlers/eis.py

@register
class EisHandler(EmailHandler):
    name = "eis"

    async def handle(self, ctx: EmailContext) -> HandlerResult:
        if not ctx.sender_user:
            return HandlerResult(
                response_text="I don't recognize your email. Please use Vikunja to set up email access.",
                should_respond=True
            )

        # Existing @eis command processing
        response, success = await process_email_command(
            user_message=ctx.parsed_message,
            user_id=ctx.sender_user["user_id"],
            email=ctx.email,
        )

        return HandlerResult(response_text=response)
```

#### Support Handler

```python
# src/vikunja_mcp/email_handlers/support.py

@register
class SupportHandler(EmailHandler):
    name = "support"

    SYSTEM_PROMPT = """You are a friendly support assistant for Factumerit.
    Answer common questions about task management and the @eis bot.
    If you can't help, say you'll escalate to a human.
    Keep responses brief and helpful."""

    async def handle(self, ctx: EmailContext) -> HandlerResult:
        # Check for escalation triggers
        if self._needs_escalation(ctx.parsed_message):
            return HandlerResult(
                response_text="I'm forwarding this to our team. They'll respond shortly.",
                forward_to=ctx.config.get("escalate_to"),
            )

        # LLM response with support persona
        response = await self._generate_response(ctx)
        return HandlerResult(response_text=response)
```

#### Triage Handler

```python
# src/vikunja_mcp/email_handlers/triage.py

@register
class TriageHandler(EmailHandler):
    name = "triage"

    async def handle(self, ctx: EmailContext) -> HandlerResult:
        # Classify the email
        labels = await self._classify(ctx.parsed_message, ctx.config["labels"])
        priority = await self._assess_priority(ctx.parsed_message)

        # Annotate and forward
        annotated_subject = f"[{','.join(labels)}] {ctx.email.subject}"

        return HandlerResult(
            should_respond=False,  # Don't reply to sender
            forward_to=ctx.config["route_to"],
            metadata={"labels": labels, "priority": priority}
        )
```

### Updated Email Inbound Flow

```python
# email_inbound.py - handle_inbound_email()

async def handle_inbound_email(webhook_data: dict) -> dict:
    # ... existing parsing ...

    route = get_route_for_address(email.to_email)
    action = route.get("action")

    if action == "drop":
        return {"status": "dropped"}

    if action == "forward":
        return await forward_email(email, route["destination"])

    if action == "ai":
        handler_name = route.get("handler")
        handler_config = route.get("config", {})

        # Load handler
        from .email_handlers.registry import get_handler
        handler = get_handler(handler_name, handler_config)

        # Build context
        sender = lookup_user_by_email(email.from_email)
        parsed = parse_reply_text(email.body_text)

        ctx = EmailContext(
            email=email,
            sender_user=sender,
            parsed_message=parsed.user_message if parsed.success else email.body_text,
            config=handler_config,
            conversation_history=[],  # TODO: thread lookup
        )

        # Execute handler
        result = await handler.handle(ctx)

        # Handle forwarding
        if result.forward_to:
            await forward_email(email, result.forward_to)

        # Send response
        if result.should_respond:
            send_response_email(
                to_email=email.from_email,
                subject=f"Re: {email.subject}",
                body_text=result.response_text,
                body_html=result.response_html,
                in_reply_to=email.message_id,
            )

        return {"status": "handled", "handler": handler_name}

    # Legacy: direct action names (backwards compat)
    if action == "eis":
        # ... existing eis handling ...
```

## Authentication & Authorization

### User Lookup Strategy

| Handler | Auth Required | Lookup Method |
|---------|--------------|---------------|
| eis | Yes | `personal_bots` table (existing) |
| support | No | Anonymous OK, but check `users` table for context |
| onboard | No | Create mapping on first contact |
| triage | No | Internal tool, no user context needed |
| digest | Yes | Must be in `personal_bots` |

### Unknown Sender Handling

```python
class SupportHandler(EmailHandler):
    async def handle(self, ctx: EmailContext) -> HandlerResult:
        if ctx.sender_user:
            # Personalized response
            greeting = f"Hi {ctx.sender_user.get('name', 'there')},"
        else:
            # Anonymous but still helpful
            greeting = "Hi,"
```

## Conversation Threading

For multi-turn conversations:

```python
@dataclass
class EmailContext:
    # ...
    conversation_history: list  # Previous exchanges
    thread_id: Optional[str]    # Email thread identifier
    turn_count: int = 0         # How many back-and-forths
```

Thread reconstruction:
1. Use `In-Reply-To` / `References` headers
2. Store in `email_threads` table
3. Limit context window (last N messages)

## Cost & Rate Limiting

```yaml
routes:
  eis:
    action: ai
    handler: eis
    limits:
      daily_emails: 50          # Per-user
      llm_tokens: 10000         # Per-email

  support:
    action: ai
    handler: support
    limits:
      daily_emails: 100         # Higher for support
      llm_tokens: 2000          # Shorter responses
```

## Observability

Each handler invocation logs:
- Handler name
- Sender (hashed)
- Response time
- Token usage
- Forward actions
- Error states

## Migration Path

1. **Phase 1:** Refactor `eis` action to use handler interface (backwards compat)
2. **Phase 2:** Add `support` handler as pilot
3. **Phase 3:** Add remaining handlers based on need

## Open Questions

1. **Shared vs isolated LLM context?** Should handlers share conversation memory?
2. **Handler composition?** Can triage → support pipeline work?
3. **User preferences?** Let users configure which AI emails they can use?
4. **Billing?** How to track/limit usage per handler?

## Related Documents

- [EMAIL_ACTION_SERVICE_EXPLAINER.md](./EMAIL_ACTION_SERVICE_EXPLAINER.md) - User-facing explanation
- [AI_WORKFLOW_PATTERN.md](./AI_WORKFLOW_PATTERN.md) - General AI patterns
- [DISPATCHER_PROVISIONING_ARCHITECTURE.md](./DISPATCHER_PROVISIONING_ARCHITECTURE.md) - Bot provisioning
