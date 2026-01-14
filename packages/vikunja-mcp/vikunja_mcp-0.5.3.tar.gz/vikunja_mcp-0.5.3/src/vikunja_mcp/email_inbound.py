"""
Email Inbound Handler for @eis.

Receives inbound emails via Resend webhook and routes them to @eis command processing.
Enables email-as-interface: users can interact with @eis by replying to emails.

Flow:
1. User receives email from @eis (welcome, response, etc.)
2. User replies to email with a question/command
3. Resend receives reply, sends webhook to /webhooks/resend
4. This handler parses email, extracts command, routes to @eis
5. Response sent back via email

Bead: fa-4mda.1
"""

import hashlib
import hmac
import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Optional

import resend

logger = logging.getLogger(__name__)


# =============================================================================
# CONFIGURATION
# =============================================================================

RESEND_WEBHOOK_SECRET = os.environ.get("RESEND_WEBHOOK_SECRET", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class InboundEmail:
    """Parsed inbound email."""
    email_id: str
    from_email: str
    from_name: Optional[str]
    to_email: str
    subject: str
    body_text: str
    body_html: Optional[str]
    in_reply_to: Optional[str]
    message_id: str
    thread_id: Optional[str]


@dataclass
class EmailParseResult:
    """Result of parsing user's message from email."""
    success: bool
    user_message: Optional[str] = None
    error: Optional[str] = None


# =============================================================================
# WEBHOOK VERIFICATION
# =============================================================================

def verify_resend_webhook(payload: bytes, signature: str, timestamp: str, webhook_id: str = "") -> bool:
    """Verify Resend webhook signature using Svix library.

    Resend uses Svix for webhooks. We use the official svix library
    for reliable verification.

    Args:
        payload: Raw request body
        signature: Svix-Signature header value
        timestamp: Svix-Timestamp header value
        webhook_id: Svix-Id header value

    Returns:
        True if signature is valid
    """
    if not RESEND_WEBHOOK_SECRET:
        logger.warning("RESEND_WEBHOOK_SECRET not configured, skipping verification")
        return True  # Allow in dev mode

    try:
        from svix.webhooks import Webhook

        # Svix expects headers as a dict
        headers = {
            "svix-id": webhook_id,
            "svix-signature": signature,
            "svix-timestamp": timestamp,
        }

        wh = Webhook(RESEND_WEBHOOK_SECRET)
        # verify() raises an exception if invalid
        wh.verify(payload, headers)
        return True

    except Exception as e:
        logger.warning(f"Webhook signature verification failed: {e}")
        return False


# =============================================================================
# EMAIL CONTENT EXTRACTION
# =============================================================================

def extract_email_from_webhook(webhook_data: dict) -> Optional[dict]:
    """Extract email content from webhook payload.

    Resend inbound webhooks include the full email content directly
    in the payload - no need to make a separate API call.

    Args:
        webhook_data: Full webhook payload

    Returns:
        Email data dict with text, html, from, to, subject, etc.
    """
    data = webhook_data.get("data", {})

    # The webhook payload contains the email directly
    return {
        "id": data.get("id") or data.get("email_id"),
        "from": data.get("from", ""),
        "to": data.get("to", []),
        "subject": data.get("subject", ""),
        "text": data.get("text", ""),
        "html": data.get("html"),
        "date": data.get("date"),
        "in_reply_to": data.get("inReplyTo") or data.get("in_reply_to"),
        "thread_id": data.get("threadId") or data.get("thread_id"),
        "message_id": data.get("messageId") or data.get("message_id", ""),
    }


# =============================================================================
# EMAIL PARSING
# =============================================================================

def parse_reply_text(body_text: str) -> EmailParseResult:
    """Extract user's message from email reply, stripping quoted content.

    Handles common reply formats:
    - Lines starting with > (quoted)
    - "On <date> <person> wrote:" blocks
    - "From: / Sent: / To:" headers
    - Gmail's reply separator
    - Outlook's reply separator

    Args:
        body_text: Raw email body text

    Returns:
        EmailParseResult with extracted user message
    """
    if not body_text:
        return EmailParseResult(success=False, error="Empty email body")

    lines = body_text.split('\n')
    user_lines = []
    in_quoted_section = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines at the start
        if not user_lines and not stripped:
            continue

        # Detect start of quoted content
        # "On Mon, Jan 8, 2025 at 10:00 AM Person <email> wrote:"
        if re.match(r'^On .+ wrote:$', stripped, re.IGNORECASE):
            break

        # "From: ... Sent: ... To: ..."
        if re.match(r'^From:', stripped, re.IGNORECASE):
            break

        # Gmail separator: "---------- Forwarded message ---------"
        if '---------- Forwarded message' in stripped:
            break

        # Outlook separator: "________________________________"
        if stripped.startswith('_' * 10):
            break

        # Yahoo separator: "--- On ..."
        if stripped.startswith('--- On '):
            break

        # Skip lines starting with > (quoted)
        if stripped.startswith('>'):
            in_quoted_section = True
            continue

        # If we were in a quoted section and hit a non-quoted line,
        # that might be more user content (interspersed replies)
        if in_quoted_section and stripped:
            # Check if this looks like part of the quoted chain
            if re.match(r'^\d{1,2}[:/]\d{2}', stripped):  # Time stamps
                continue
            in_quoted_section = False

        # Add user's line
        user_lines.append(line)

    # Clean up result
    user_message = '\n'.join(user_lines).strip()

    # Remove signature blocks (-- followed by signature)
    sig_match = re.search(r'\n--\s*\n', user_message)
    if sig_match:
        user_message = user_message[:sig_match.start()].strip()

    if not user_message:
        return EmailParseResult(success=False, error="No user message found in reply")

    return EmailParseResult(success=True, user_message=user_message)


def parse_inbound_email(webhook_data: dict, email_content: dict) -> Optional[InboundEmail]:
    """Parse webhook data and email content into InboundEmail.

    Args:
        webhook_data: Data from webhook event
        email_content: Full email from API

    Returns:
        InboundEmail or None on error
    """
    try:
        # Extract from webhook data
        data = webhook_data.get("data", webhook_data)
        email_id = data.get("email_id") or data.get("id")

        # Parse "from" field: "Name <email>" or just "email"
        from_raw = data.get("from", "")
        from_match = re.match(r'^(.+?)\s*<([^>]+)>$', from_raw)
        if from_match:
            from_name = from_match.group(1).strip().strip('"')
            from_email = from_match.group(2)
        else:
            from_name = None
            from_email = from_raw

        # Get "to" (first recipient)
        to_list = data.get("to", [])
        to_email = to_list[0] if to_list else ""

        # Get body from API response
        body_text = email_content.get("text", "") or ""
        body_html = email_content.get("html")

        return InboundEmail(
            email_id=email_id,
            from_email=from_email,
            from_name=from_name,
            to_email=to_email,
            subject=data.get("subject", ""),
            body_text=body_text,
            body_html=body_html,
            in_reply_to=data.get("in_reply_to") or email_content.get("in_reply_to"),
            message_id=data.get("message_id", ""),
            thread_id=data.get("thread_id"),
        )

    except Exception as e:
        logger.exception(f"Failed to parse inbound email: {e}")
        return None


# =============================================================================
# USER MAPPING
# =============================================================================

def lookup_user_by_email(email: str) -> Optional[dict]:
    """Look up Vikunja user by email address.

    Args:
        email: Email address to look up

    Returns:
        dict with user_id, username, or None if not found
    """
    from .token_broker import execute

    try:
        # Check personal_bots table (users with bot setup)
        rows = execute("""
            SELECT user_id, bot_username
            FROM personal_bots
            WHERE user_email = %s
        """, (email,))

        if rows:
            return {
                "user_id": rows[0][0],
                "bot_username": rows[0][1],
                "source": "personal_bots",
            }

        # Check users table directly (via Vikunja DB)
        # Note: This requires access to Vikunja's database
        # For now, return None if not in personal_bots
        logger.info(f"User not found in personal_bots: {email}")
        return None

    except Exception as e:
        logger.exception(f"User lookup failed for {email}: {e}")
        return None


# =============================================================================
# RESPONSE EMAIL
# =============================================================================

def send_response_email(
    to_email: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    in_reply_to: Optional[str] = None,
    references: Optional[str] = None,
) -> bool:
    """Send response email back to user.

    Args:
        to_email: Recipient email
        subject: Email subject (typically "Re: ...")
        body_text: Plain text body
        body_html: HTML body (optional)
        in_reply_to: Message-ID we're replying to (for threading)
        references: References header for threading

    Returns:
        True on success
    """
    if not RESEND_API_KEY:
        logger.error("RESEND_API_KEY not configured")
        return False

    try:
        resend.api_key = RESEND_API_KEY

        email_params = {
            "from": "eis <eis@factumerit.app>",
            "to": [to_email],
            "subject": subject,
            "text": body_text,
        }

        if body_html:
            email_params["html"] = body_html

        # Set headers for threading
        headers = {}
        if in_reply_to:
            headers["In-Reply-To"] = in_reply_to
        if references:
            headers["References"] = references
        elif in_reply_to:
            headers["References"] = in_reply_to

        if headers:
            email_params["headers"] = headers

        response = resend.Emails.send(email_params)
        logger.info(f"Response email sent to {to_email}: {response.get('id')}")
        return True

    except Exception as e:
        logger.exception(f"Failed to send response email to {to_email}: {e}")
        return False


# =============================================================================
# COMMAND PROCESSING
# =============================================================================

async def process_email_command(
    user_message: str,
    user_id: str,
    email: InboundEmail,
) -> tuple[str, bool]:
    """Process user's email message as @eis command.

    Args:
        user_message: Extracted user message from email
        user_id: User ID for budget/context
        email: Full parsed email for context

    Returns:
        Tuple of (response_message, success)
    """
    from .command_parser import CommandParser
    from .keyword_handlers import KeywordHandlers
    from .vikunja_client import BotVikunjaClient

    # Parse command (treat email content as implicit @eis mention)
    parser = CommandParser()
    result = parser.parse(user_message, implicit_mention=True)

    if result.tier == "unknown":
        # Default to natural language processing
        result = parser.parse(f"@eis {user_message}", implicit_mention=False)

    # Execute command
    try:
        client = BotVikunjaClient(user_id=user_id)
        handlers = KeywordHandlers(client)

        if result.tier == "tier3":
            handler = handlers.get_handler(result.handler)
            if handler:
                handler_result = await handler(result.args or {}, user_id=user_id)
                return (handler_result.message, handler_result.success)
            return (f"Unknown command: {result.handler}", False)

        elif result.tier in ("tier1", "tier2", "tier_natural"):
            handler = handlers.get_handler(result.handler)
            if handler:
                handler_result = await handler(
                    result.args or {},
                    user_id=user_id,
                    conversation_context=f"Email from {email.from_email}: {email.subject}",
                )
                return (handler_result.message, handler_result.success)
            return ("Could not process request", False)

        else:
            return (result.error or "Could not understand request", False)

    except Exception as e:
        logger.exception(f"Command processing failed: {e}")
        return (f"Error processing request: {str(e)}", False)


# =============================================================================
# EMAIL ROUTING
# =============================================================================

def load_routing_config() -> dict:
    """Load email routing configuration from YAML file."""
    from pathlib import Path
    import yaml

    # Find project root by looking for pyproject.toml (works in venv too)
    # Start from cwd or fall back to file-based search
    for search_start in [Path.cwd(), Path(__file__).resolve()]:
        current = search_start if search_start.is_dir() else search_start.parent
        while current != current.parent:
            if (current / "pyproject.toml").exists():
                config_path = current / "config" / "email_routing.yaml"
                if config_path.exists():
                    break
            current = current.parent
        else:
            continue
        break
    else:
        # Last resort: try common deployment paths
        for base in [Path("/opt/render/project/src"), Path.cwd()]:
            config_path = base / "config" / "email_routing.yaml"
            if config_path.exists():
                break
        else:
            logger.warning(f"Email routing config not found")
            return {"routes": {"eis": {"action": "eis"}}}  # Default to eis

    if not config_path.exists():
        logger.warning(f"Email routing config not found: {config_path}")
        return {"routes": {"eis": {"action": "eis"}}}  # Default to eis

    try:
        with open(config_path) as f:
            return yaml.safe_load(f) or {"routes": {}}
    except Exception as e:
        logger.exception(f"Failed to load routing config: {e}")
        return {"routes": {"eis": {"action": "eis"}}}


def get_route_for_address(to_email: str) -> dict:
    """Get routing action for a destination email address.

    Args:
        to_email: The "to" address (e.g., eis@factumerit.app)

    Returns:
        Route config dict with 'action' and optional 'destination'
    """
    config = load_routing_config()
    routes = config.get("routes", {})

    # Extract local part (before @)
    local_part = to_email.split("@")[0].lower()

    # Look up route
    if local_part in routes:
        return routes[local_part]

    # Check for default/catch-all
    if "_default" in routes:
        return routes["_default"]

    # No route found - default to drop with warning
    logger.warning(f"No route for {to_email}, dropping")
    return {"action": "drop"}


async def forward_email(
    original_email: 'InboundEmail',
    destination: str,
) -> dict:
    """Forward an email to another address.

    Args:
        original_email: The parsed inbound email
        destination: Email address to forward to

    Returns:
        Result dict
    """
    if not RESEND_API_KEY:
        logger.error("RESEND_API_KEY not configured")
        return {"status": "error", "message": "Email not configured"}

    try:
        resend.api_key = RESEND_API_KEY

        # Build forwarded subject
        subject = original_email.subject
        if not subject.lower().startswith("fwd:"):
            subject = f"Fwd: {subject}"

        # Build forwarded body
        from datetime import datetime
        date_str = datetime.utcnow().strftime("%a, %b %d, %Y at %I:%M %p")
        body = f"""---------- Forwarded message ----------
From: {original_email.from_name or ''} <{original_email.from_email}>
Date: {date_str}
Subject: {original_email.subject}
To: {original_email.to_email}

{original_email.body_text}
"""

        response = resend.Emails.send({
            "from": f"Factumerit <noreply@factumerit.app>",
            "to": [destination],
            "subject": subject,
            "text": body,
            "reply_to": original_email.from_email,
        })

        logger.info(f"Forwarded email to {destination}: {response.get('id')}")
        return {"status": "forwarded", "destination": destination}

    except Exception as e:
        logger.exception(f"Failed to forward email to {destination}: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# MAIN HANDLER
# =============================================================================

async def handle_inbound_email(webhook_data: dict) -> dict:
    """Main handler for inbound email webhook.

    Routes emails based on config/email_routing.yaml:
    - eis: Process with @eis AI assistant
    - forward: Forward to destination email
    - drop: Silently ignore

    Args:
        webhook_data: Webhook payload from Resend

    Returns:
        dict with status and message
    """
    event_type = webhook_data.get("type")

    if event_type != "email.received":
        logger.debug(f"Ignoring event type: {event_type}")
        return {"status": "ignored", "reason": f"Event type {event_type} not handled"}

    data = webhook_data.get("data", {})
    email_id = data.get("email_id") or data.get("id")

    if not email_id:
        return {"status": "error", "message": "No email_id in webhook"}

    logger.info(f"Processing inbound email: {email_id}")

    # Extract email content from webhook payload (no API call needed)
    email_content = extract_email_from_webhook(webhook_data)
    if not email_content:
        return {"status": "error", "message": "Failed to extract email content"}

    # Parse email into structured object
    email = parse_inbound_email(webhook_data, email_content)
    if not email:
        return {"status": "error", "message": "Failed to parse email"}

    logger.info(f"Inbound email from {email.from_email} to {email.to_email}: {email.subject}")

    # Get routing action for this address
    route = get_route_for_address(email.to_email)
    action = route.get("action", "drop")

    logger.info(f"Route for {email.to_email}: {action}")

    # Handle DROP action
    if action == "drop":
        logger.info(f"Dropping email to {email.to_email}")
        return {"status": "dropped", "to": email.to_email}

    # Handle FORWARD action
    if action == "forward":
        destination = route.get("destination")
        if not destination:
            logger.error(f"Forward route for {email.to_email} has no destination")
            return {"status": "error", "message": "Forward destination not configured"}
        return await forward_email(email, destination)

    # Handle EIS action (AI assistant)
    if action == "eis":
        # Look up user
        user = lookup_user_by_email(email.from_email)
        if not user:
            # Unknown sender - could send onboarding email or ignore
            logger.warning(f"Unknown sender: {email.from_email}")
            return {"status": "ignored", "reason": "Unknown sender"}

        # Parse reply to extract user's message
        parse_result = parse_reply_text(email.body_text)
        if not parse_result.success:
            logger.warning(f"Could not parse reply: {parse_result.error}")
            return {"status": "error", "message": parse_result.error}

        logger.info(f"User message: {parse_result.user_message[:100]}...")

        # Process command
        response_message, success = await process_email_command(
            user_message=parse_result.user_message,
            user_id=user["user_id"],
            email=email,
        )

        # Send response email
        subject = email.subject
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"

        send_response_email(
            to_email=email.from_email,
            subject=subject,
            body_text=response_message,
            in_reply_to=email.message_id,
        )

        return {
            "status": "success" if success else "error",
            "message": "Response sent",
            "user_id": user["user_id"],
        }

    # Unknown action
    logger.warning(f"Unknown action '{action}' for {email.to_email}")
    return {"status": "error", "message": f"Unknown action: {action}"}
