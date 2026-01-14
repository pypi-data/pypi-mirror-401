"""
Vikunja MCP Server (PRIVATE - factumerit)

This is the PRIVATE factumerit server. It contains both:
- Public tools (generic Vikunja operations) → published to PyPI as vikunja-mcp
- Private tools (Slack, Matrix, auth, user management) → NOT published

================================================================================
FUNCTION TAGGING (MANDATORY)
================================================================================

EVERY function MUST have one of these tags on the line BEFORE decorators/def:

    # @PUBLIC         - Generic Vikunja tool, safe for public PyPI release
    # @PUBLIC_HELPER  - Helper function used by public tools
    # @PRIVATE        - Factumerit-specific, never publish

Verify with: python scripts/check_tags.py

Tag as @PUBLIC if ALL criteria are met:
- Generic Vikunja operations (CRUD on tasks, projects, labels, buckets, views)
- No user/multi-tenancy logic (_get_user_*, _set_user_*, user_id params)
- No auth/OAuth flows
- No Slack/Matrix handlers
- No billing/credits/usage tracking
- No factumerit-specific business logic

Tag as @PRIVATE if ANY of these apply:
- slash_* commands (Slack)
- handle_* functions (Slack/Matrix)
- _matrix_* functions
- *_user_* functions (user management)
- oauth_*, auth_*, activate_*, signup_*
- Anything touching user_id, credits, roles, api keys
- HTTP endpoints specific to factumerit (/vikunja-callback, /waiting-list, etc.)

Example:
    # @PUBLIC
    @mcp.tool()
    def list_tasks(...):
        ...

    # @PRIVATE
    def _get_user_credits(user_id: str):
        ...

After adding/modifying tools, run:
    python scripts/check_tags.py     # Verify all functions tagged
    python scripts/extract_public.py # (Optional) Regenerate public server

================================================================================
TOOL CATEGORIES
================================================================================

Public (generic Vikunja):
- Projects: list, get, create, update, delete, export_all_projects
- Tasks: list, get, create, update, complete, delete, set_position, add_label, etc.
- Labels: list, create, delete
- Views: list_views, get_view_tasks, list_tasks_by_bucket, etc.
- Kanban: list_buckets, create_bucket, delete_bucket, sort_bucket
- Relations: create, list
- Batch: batch_create_tasks, batch_update_tasks, batch_set_positions
- Calendar: get_ics_feed, get_calendar_url

Private (factumerit-specific):
- Slack handlers: slash_*, handle_*
- Matrix handlers: _matrix_*
- User management: _get_user_*, _set_user_*
- Auth/OAuth: oauth_*, vikunja_callback
- Billing: credits, usage, limits
- Bot provisioning: activate_bot, signup, waiting_list

================================================================================
CONFIGURATION
================================================================================

- VIKUNJA_URL: Base URL of Vikunja instance (fallback if no instances configured)
- VIKUNJA_TOKEN: API authentication token (fallback if no instances configured)
- ~/.vikunja-mcp/config.yaml: Instance configuration for multi-instance support
"""

import bisect
import contextvars
import logging
import os
import re
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import base64
import hashlib
import markdown
import yaml
from cryptography.fernet import Fernet
from fastmcp import FastMCP
from icalendar import Calendar, Event
from pydantic import Field
import requests

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Configure logger for performance diagnostics
logger = logging.getLogger("vikunja-mcp")
logger.setLevel(logging.DEBUG if os.environ.get("VIKUNJA_DEBUG") else logging.INFO)

# Only add handler if not already configured (avoid duplicate logs)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)

# Performance tracking: set VIKUNJA_PERF=1 to log API call times
PERF_LOGGING = os.environ.get("VIKUNJA_PERF", "").lower() in ("1", "true", "yes")

# Context variable for per-request Vikunja token (used by Slack bot)
# This allows tool impls to use per-user tokens without changing their signatures
_current_vikunja_token: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    '_current_vikunja_token', default=None
)

# Context variable to allow instance token fallback (for MCP/CLI mode)
# SECURITY: Only set this to True for non-user-facing requests (MCP tools, CLI)
# User-facing requests (Matrix, Slack) must NEVER allow fallback to prevent data leaks
_allow_instance_fallback: contextvars.ContextVar[bool] = contextvars.ContextVar(
    '_allow_instance_fallback', default=False
)

# Context variable for current user ID (Matrix/Slack user)
# This allows instance-aware functions to look up user-specific config from PostgreSQL
_current_user_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    '_current_user_id', default=None
)

# Context variable for bot mode (vikunja_chat_with_claude / @eis)
# When True, _request() uses env vars (VIKUNJA_URL + VIKUNJA_BOT_TOKEN) instead of YAML config
# This separates bot operations from MCP multi-instance configuration (solutions-zja1)
_bot_mode: contextvars.ContextVar[bool] = contextvars.ContextVar(
    '_bot_mode', default=False
)

# Context variable for requesting user (who triggered @eis)
# Used to auto-share newly created projects with the requester
_requesting_user: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    '_requesting_user', default=None
)
_requesting_user_id: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar(
    '_requesting_user_id', default=None
)

# Context variables for project queue batching (solutions-eofy)
# Accumulates projects during one LLM turn, flushes at end
_pending_projects: contextvars.ContextVar[Optional[list]] = contextvars.ContextVar(
    '_pending_projects', default=None
)
_next_temp_id: contextvars.ContextVar[int] = contextvars.ContextVar(
    '_next_temp_id', default=-1
)


# @PRIVATE
def mcp_tool_with_fallback(func):
    """Decorator for MCP tools that need instance token fallback.

    MCP/CLI tools don't have per-user authentication, so they need to use
    the instance token from VIKUNJA_TOKEN env var.

    SECURITY: Only use this decorator for MCP tools, never for user-facing handlers.
    """
    import functools

# @PRIVATE
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = _allow_instance_fallback.set(True)
        try:
            return func(*args, **kwargs)
        finally:
            _allow_instance_fallback.reset(token)
    return wrapper


# @PRIVATE
def _reject_queued_project_id(project_id: int, operation: str = "this operation") -> None:
    """Raise error if project_id is a temporary queued ID (negative).

    When projects are queued for user creation, they get temporary negative IDs.
    These IDs cannot be used for subsequent API operations until the user
    actually creates the project.
    """
    if project_id is not None and project_id < 0:
        raise ValueError(
            f"Cannot perform {operation} on queued project (temp_id={project_id}). "
            f"The project has been QUEUED for creation but not yet created. "
            f"The user must click the creation link first. "
            f"Do NOT use the temporary project_id for any subsequent operations. "
            f"Wait for the user to create the project, then use the real project ID."
        )


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

AVAILABLE_MODELS = {
    "haiku": "claude-3-5-haiku-20241022",
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-20250514",
}

DEFAULT_MODEL = os.environ.get("MODEL_DEFAULT", "haiku")  # Default to haiku for cost efficiency

# Model pricing for cost estimation (per million tokens)
MODEL_PRICING = {
    "haiku": {"input": 0.80, "output": 4.00},
    "sonnet": {"input": 3.00, "output": 15.00},
    "opus": {"input": 15.00, "output": 75.00},
}

# Cost thresholds for alerts
COST_ALERT_THRESHOLD = 15.00  # Alert when monthly cost approaches this
CLAUDE_PRO_COST = 20.00  # Monthly cost of Claude Pro subscription

# ============================================================================
# MEMORY CONFIGURATION
# ============================================================================

# Memory strategies available
MEMORY_STRATEGIES = ["none", "rolling"]  # Will add "summarized", "tiered" later

# Default memory settings
DEFAULT_MEMORY_STRATEGY = "rolling"
DEFAULT_MEMORY_WINDOW = 10  # Number of message pairs to keep

# ============================================================================
# KANBAN TEMPLATES
# ============================================================================

KANBAN_TEMPLATES = {
    "gtd": [
        {"title": "📥 Inbox", "position": 10},
        {"title": "⏭️ Next", "position": 20, "limit": 5},
        {"title": "⏸️ Waiting", "position": 30},
        {"title": "💭 Someday", "position": 40},
        {"title": "✅ Done", "position": 50}
    ],
    "sprint": [
        {"title": "📋 Backlog", "position": 10},
        {"title": "📝 To Do", "position": 20},
        {"title": "🚀 In Progress", "position": 30, "limit": 3},
        {"title": "👀 Review", "position": 40, "limit": 2},
        {"title": "✅ Done", "position": 50}
    ],
    "kitchen": [
        {"title": "💡 Idea", "position": 10},
        {"title": "📝 To-Do", "position": 20},
        {"title": "📋 Planned", "position": 30},
        {"title": "🥣 Mise en Place", "position": 40},
        {"title": "🧊 Standby", "position": 50},
        {"title": "🔥 Cooking/Baking", "position": 60},
        {"title": "🎨 Decorating", "position": 70},
        {"title": "📦 Ready", "position": 80},
        {"title": "✅ Done", "position": 90}
    ],
    "payables": [
        {"title": "🤔 Decision Queue", "position": 10},
        {"title": "✅ Approved - Timing Payment", "position": 20},
        {"title": "💰 Paid", "position": 30}
    ],
    "talks": [
        {"title": "💡 Ideas", "position": 10},
        {"title": "📤 Submitted", "position": 20},
        {"title": "✅ Accepted", "position": 30},
        {"title": "📝 Preparing", "position": 40, "limit": 2},
        {"title": "🎤 Delivered", "position": 50}
    ]
}

# ============================================================================
# USAGE LIMITS CONFIGURATION
# ============================================================================

# Default limits (can be overridden per user in config)
DEFAULT_LIFETIME_BUDGET = 1.00  # $ lifetime free tier
DEFAULT_DAILY_BUDGET = 2.00  # $ per day (legacy, superceded by lifetime)
DEFAULT_MONTHLY_BUDGET = 20.00  # $ per month (legacy, superceded by lifetime)
DEFAULT_LIMIT_ACTION = "block"  # "block" when lifetime exhausted

# ============================================================================
# RBAC (Role-Based Access Control)
# ============================================================================

# Role hierarchy (higher index = more permissions)
ROLE_HIERARCHY = ["user", "support", "moderator", "admin", "owner"]

# Role capabilities
ROLE_CAPABILITIES = {
    "user": ["use_bot", "see_own_usage"],
    "support": ["use_bot", "see_own_usage", "view_any_usage"],
    "moderator": ["use_bot", "see_own_usage", "view_any_usage", "set_tier_basic", "set_tier_pro", "suspend_user"],
    "admin": ["use_bot", "see_own_usage", "view_any_usage", "set_tier_basic", "set_tier_pro", "set_tier_unlimited", "suspend_user", "manage_moderators", "add_credits"],
    "owner": ["*"],  # All capabilities
}

# Admin user IDs (migrated to owner role on startup)
# Supports any user ID format: Slack (U0AJNT3KP), Vikunja (vikunja:ivan), Matrix (@user:server)
ADMIN_USER_IDS = set(os.environ.get("ADMIN_USER_IDS", "").split(",")) - {""}


# @PRIVATE
def _get_user_role(user_id: str) -> str:
    """Get user's role from config. Defaults to 'user'."""
    config = _load_config()
    user_roles = config.get("user_roles", {})
    role_info = user_roles.get(user_id, {})
    if isinstance(role_info, dict):
        return role_info.get("role", "user")
    return "user"


# @PRIVATE
def _set_user_role(user_id: str, role: str, granted_by: str) -> dict:
    """Set user's role. Returns success/error dict."""
    if role not in ROLE_HIERARCHY:
        return {"error": f"Invalid role: {role}. Valid roles: {', '.join(ROLE_HIERARCHY)}"}

    config = _load_config()
    if "user_roles" not in config:
        config["user_roles"] = {}

    old_role = _get_user_role(user_id)
    config["user_roles"][user_id] = {
        "role": role,
        "granted_by": granted_by,
        "granted_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_config(config)

    return {
        "user_id": user_id,
        "old_role": old_role,
        "new_role": role,
        "granted_by": granted_by,
        "success": True,
    }


# @PRIVATE
def _has_role(user_id: str, required_role: str) -> bool:
    """Check if user has at least the required role level."""
    user_role = _get_user_role(user_id)
    try:
        user_level = ROLE_HIERARCHY.index(user_role)
        required_level = ROLE_HIERARCHY.index(required_role)
        return user_level >= required_level
    except ValueError:
        return False


# @PRIVATE
def _has_capability(user_id: str, capability: str) -> bool:
    """Check if user has a specific capability."""
    role = _get_user_role(user_id)
    caps = ROLE_CAPABILITIES.get(role, [])
    return "*" in caps or capability in caps


# @PUBLIC_HELPER
def _can_grant_role(granter_id: str, target_role: str) -> bool:
    """Check if granter can grant the target role (must be strictly higher)."""
    granter_role = _get_user_role(granter_id)
    try:
        granter_level = ROLE_HIERARCHY.index(granter_role)
        target_level = ROLE_HIERARCHY.index(target_role)
        # Can only grant roles below your own level
        return granter_level > target_level
    except ValueError:
        return False


# @PRIVATE
def _grant_env_admin_roles() -> None:
    """Grant owner role to users listed in ADMIN_USER_IDS env var (on startup)."""
    if not ADMIN_USER_IDS:
        return

    config = _load_config()
    if "user_roles" not in config:
        config["user_roles"] = {}

    migrated = []
    for admin_id in ADMIN_USER_IDS:
        if admin_id not in config["user_roles"]:
            config["user_roles"][admin_id] = {
                "role": "owner",
                "granted_by": "system:env",
                "granted_at": datetime.now(timezone.utc).isoformat(),
            }
            migrated.append(admin_id)

    if migrated:
        _save_config(config)
        print(f"[RBAC] Granted owner role to {len(migrated)} users from ADMIN_USER_IDS: {migrated}")


# ============================================================================
# API KEY ENCRYPTION (BYOK - Bring Your Own Key)
# ============================================================================

# @PUBLIC_HELPER
def _get_encryption_key() -> bytes:
    """Get or generate encryption key for API key storage.

    Uses VIKUNJA_MCP_ENCRYPTION_KEY env var if set, otherwise derives
    a key from a combination of stable machine identifiers.

    Returns:
        32-byte key suitable for Fernet encryption
    """
    key_from_env = os.environ.get("VIKUNJA_MCP_ENCRYPTION_KEY")
    if key_from_env:
        # Derive 32-byte key from provided value using SHA256
        return base64.urlsafe_b64encode(hashlib.sha256(key_from_env.encode()).digest())

    # Fallback: derive from hostname + config dir (stable per deployment)
    # Not cryptographically ideal but provides obfuscation for stored keys
    import socket
    stable_seed = f"{socket.gethostname()}:{CONFIG_DIR}"
    return base64.urlsafe_b64encode(hashlib.sha256(stable_seed.encode()).digest())


# @PUBLIC_HELPER
def _encrypt_api_key(api_key: str) -> str:
    """Encrypt an API key for storage.

    Args:
        api_key: Plaintext API key (e.g., sk-ant-xxx)

    Returns:
        Base64-encoded encrypted key
    """
    fernet = Fernet(_get_encryption_key())
    return fernet.encrypt(api_key.encode()).decode()


# @PUBLIC_HELPER
def _decrypt_api_key(encrypted: str) -> Optional[str]:
    """Decrypt a stored API key.

    Args:
        encrypted: Base64-encoded encrypted key

    Returns:
        Plaintext API key, or None if decryption fails
    """
    try:
        fernet = Fernet(_get_encryption_key())
        return fernet.decrypt(encrypted.encode()).decode()
    except Exception as e:
        logger.warning(f"Failed to decrypt API key: {e}")
        return None


# @PRIVATE
def _get_user_anthropic_api_key(user_id: str) -> Optional[str]:
    """Get user's stored Anthropic API key if present.

    Args:
        user_id: Slack user ID

    Returns:
        Decrypted API key, or None if not set or decryption fails
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    encrypted = user_config.get("anthropic_api_key_encrypted")
    if not encrypted:
        return None
    return _decrypt_api_key(encrypted)


# @PRIVATE
def _set_user_anthropic_api_key(user_id: str, api_key: str) -> dict:
    """Store encrypted Anthropic API key for user.

    Args:
        user_id: Slack user ID
        api_key: Plaintext API key

    Returns:
        Status dict with success flag and timestamp
    """
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}

    config["users"][user_id]["anthropic_api_key_encrypted"] = _encrypt_api_key(api_key)
    config["users"][user_id]["anthropic_api_key_set_at"] = datetime.now(timezone.utc).isoformat()
    _save_config(config)

    return {
        "success": True,
        "set_at": config["users"][user_id]["anthropic_api_key_set_at"]
    }


# @PRIVATE
def _remove_user_anthropic_api_key(user_id: str) -> dict:
    """Remove user's stored Anthropic API key.

    Args:
        user_id: Slack user ID

    Returns:
        Status dict with success flag
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})

    had_key = "anthropic_api_key_encrypted" in user_config
    if had_key:
        del config["users"][user_id]["anthropic_api_key_encrypted"]
        if "anthropic_api_key_set_at" in config["users"][user_id]:
            del config["users"][user_id]["anthropic_api_key_set_at"]
        _save_config(config)

    return {"success": True, "had_key": had_key}


# @PRIVATE
def _get_user_api_key_status(user_id: str) -> dict:
    """Get status of user's stored API key.

    Args:
        user_id: Slack user ID

    Returns:
        Status dict with has_key, set_at (if set), and using_own_key flags
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})

    has_key = "anthropic_api_key_encrypted" in user_config
    set_at = user_config.get("anthropic_api_key_set_at") if has_key else None

    return {
        "has_key": has_key,
        "set_at": set_at,
        "using_own_key": has_key  # Will use own key for requests
    }


# @PUBLIC_HELPER
def _validate_anthropic_api_key(api_key: str) -> tuple[bool, str]:
    """Validate an Anthropic API key by making a minimal API call.

    Args:
        api_key: API key to validate

    Returns:
        Tuple of (is_valid, message)
    """
    import anthropic

    # Debug logging - show key format without exposing full key
    key_prefix = api_key[:20] if len(api_key) >= 20 else api_key
    key_suffix = api_key[-10:] if len(api_key) >= 10 else ""
    key_length = len(api_key)

    # Show hex representation of first/last few chars to detect hidden characters
    import binascii
    first_bytes = binascii.hexlify(api_key[:10].encode()).decode() if len(api_key) >= 10 else ""
    last_bytes = binascii.hexlify(api_key[-10:].encode()).decode() if len(api_key) >= 10 else ""

    logger.info(f"Validating API key: prefix={key_prefix}... suffix=...{key_suffix} length={key_length}")
    logger.info(f"Key hex (first 10 chars): {first_bytes}")
    logger.info(f"Key hex (last 10 chars): {last_bytes}")

    # Check for common issues
    if '\n' in api_key or '\r' in api_key:
        logger.warning("API key contains newline characters!")
        return False, "API key contains invalid characters (newlines)"
    if ' ' in api_key:
        logger.warning("API key contains spaces!")
        return False, "API key contains invalid characters (spaces)"

    # Check for any non-printable or unusual characters
    unusual_chars = [c for c in api_key if ord(c) < 32 or ord(c) > 126]
    if unusual_chars:
        logger.warning(f"API key contains unusual characters: {[hex(ord(c)) for c in unusual_chars]}")
        return False, "API key contains invalid characters"

    try:
        # First try with raw HTTP request to rule out SDK issues
        import requests
        logger.info("Attempting validation with raw HTTP request...")
        http_response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-5-haiku-20241022",
                "max_tokens": 5,
                "messages": [{"role": "user", "content": "hi"}]
            },
            timeout=10
        )
        logger.info(f"HTTP validation response: status={http_response.status_code}")

        if http_response.status_code == 200:
            logger.info("API key validation successful (HTTP)")
            return True, "API key is valid"
        elif http_response.status_code == 401:
            logger.warning(f"HTTP 401: {http_response.text}")
            return False, "Invalid API key - check the key and try again"
        else:
            logger.error(f"Unexpected HTTP status {http_response.status_code}: {http_response.text}")
            return False, f"Validation error: HTTP {http_response.status_code}"

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e}")
        # Fall back to SDK
        pass

    try:
        logger.info("Attempting validation with Anthropic SDK...")
        client = anthropic.Anthropic(api_key=api_key)
        # Minimal request to validate key
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=5,
            messages=[{"role": "user", "content": "hi"}]
        )
        logger.info("API key validation successful (SDK)")
        return True, "API key is valid"
    except anthropic.AuthenticationError as e:
        logger.warning(f"API key validation failed (AuthenticationError): {e}")
        return False, "Invalid API key - check the key and try again"
    except anthropic.RateLimitError:
        # Key is valid but rate limited - still consider it valid
        logger.info("API key valid but rate limited")
        return True, "API key is valid (rate limited)"
    except Exception as e:
        logger.error(f"API key validation error: {e}", exc_info=True)
        return False, f"Error validating key: {str(e)}"


# @PUBLIC_HELPER
def _is_html(text: str) -> bool:
    """Check if text appears to be HTML (not markdown).

    Simple heuristic: starts with common HTML tags.
    """
    if not text:
        return False
    stripped = text.strip()
    html_starts = ('<p>', '<p ', '<div>', '<div ', '<ul>', '<ol>', '<h1>', '<h2>',
                   '<h3>', '<h4>', '<h5>', '<h6>', '<table>', '<blockquote>', '<!DOCTYPE')
    return stripped.lower().startswith(html_starts)


# @PUBLIC
def md_to_html(text: str) -> str:
    """Convert markdown to HTML for Vikunja descriptions.

    If text is already HTML, returns it unchanged.
    """
    if not text:
        return text
    # If already HTML, don't convert
    if _is_html(text):
        return text
    return markdown.markdown(text)


# @PUBLIC_HELPER
def _sanitize_title(title: str) -> str:
    """Strip HTML tags from title, keeping only plain text.

    Security: Prevents HTML injection in task/project/label titles.
    Titles are displayed in UI and should not contain executable HTML.

    Args:
        title: Raw title string (may contain HTML)

    Returns:
        Sanitized title with HTML tags removed, max 256 chars

    Examples:
        >>> _sanitize_title("<script>alert(1)</script>Test")
        "Test"
        >>> _sanitize_title("<b>Bold Title</b>")
        "Bold Title"
    """
    if not title:
        return title
    # Remove script/style tags AND their content (security-critical)
    title = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', title, flags=re.IGNORECASE | re.DOTALL)
    # Remove all other HTML tags (keep content)
    title = re.sub(r'<[^>]+>', '', title)
    # Limit length (Vikunja has 250 char limit, use 256 for safety)
    return title[:256]


# @PUBLIC_HELPER
def _sanitize_description(desc: str) -> str:
    """Escape HTML entities in description before markdown conversion.

    Security: Prevents second-order HTML injection from Vikunja data.
    Users can inject arbitrary HTML via Vikunja web UI. We must escape
    it before converting markdown to HTML.

    Strategy: Accept markdown from user, escape any HTML in it, then
    convert markdown to HTML safely.

    Args:
        desc: Raw description string (may contain HTML and markdown)

    Returns:
        HTML-escaped description ready for markdown conversion

    Examples:
        >>> _sanitize_description("<script>alert(1)</script>")
        "&lt;script&gt;alert(1)&lt;/script&gt;"
        >>> _sanitize_description("**Bold** <b>HTML</b>")
        "**Bold** &lt;b&gt;HTML&lt;/b&gt;"
    """
    if not desc:
        return desc
    # Escape HTML entities (must be done BEFORE markdown conversion)
    import html
    return html.escape(desc)


# @PUBLIC_HELPER
def _md_to_slack_mrkdwn(text: str) -> str:
    """Convert standard markdown to Slack mrkdwn format.

    Key differences:
    - Bold: **text** → *text*
    - Headers: ## Header → *Header* (Slack has no headers)
    - Links: [text](url) → <url|text>
    """
    if not text:
        return text
    # Convert markdown headers to bold (Slack has no header format)
    # Must be done before **bold** conversion to avoid double-processing
    text = re.sub(r'^#{1,6}\s+(.+)$', r'*\1*', text, flags=re.MULTILINE)
    # Convert **bold** to *bold* (Slack uses single asterisks)
    text = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', text)
    # Convert [text](url) to <url|text>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<\2|\1>', text)
    return text


# ============================================================================
# PROJECT CONFIG MANAGEMENT
# ============================================================================

# Allow override for Render persistent disk via VIKUNJA_MCP_CONFIG_DIR env var
CONFIG_DIR = Path(os.environ.get("VIKUNJA_MCP_CONFIG_DIR", str(Path.home() / ".vikunja-mcp")))
CONFIG_FILE = CONFIG_DIR / "config.yaml"


# @PUBLIC_HELPER
def _load_config() -> dict:
    """Load project config from YAML file."""
    if not CONFIG_FILE.exists():
        return {"projects": {}, "instances": {}, "current_instance": None}
    try:
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f) or {}
            if "projects" not in config:
                config["projects"] = {}
            if "instances" not in config:
                config["instances"] = {}
            return config
    except yaml.YAMLError as e:
        raise ValueError(f"Malformed config file: {e}")


# @PUBLIC_HELPER
def _save_config(config: dict) -> None:
    """Save project config to YAML file (atomic write)."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # Atomic write: write to temp file, then rename
    fd, temp_path = tempfile.mkstemp(dir=CONFIG_DIR, suffix=".yaml")
    try:
        with os.fdopen(fd, "w") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        os.replace(temp_path, CONFIG_FILE)
    except Exception:
        os.unlink(temp_path)
        raise


# @PUBLIC_HELPER
def _deep_merge(base: dict, updates: dict) -> dict:
    """Deep merge updates into base dict."""
    result = base.copy()
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


# ============================================================================
# ECO MODE TRACKING
# ============================================================================

# In-memory ECO streaks (resets on restart, but that's fine for gamification)
_eco_streaks: dict[str, int] = {}
# Estimated tokens saved per slash command (rough average)
_TOKENS_PER_LLM_QUERY = 500


# @PRIVATE
def _increment_eco_streak(user_id: str) -> int:
    """Increment ECO streak for user. Returns new streak count."""
    _eco_streaks[user_id] = _eco_streaks.get(user_id, 0) + 1
    return _eco_streaks[user_id]


# @PRIVATE
def _reset_eco_streak(user_id: str) -> None:
    """Reset ECO streak for user (called when LLM is used)."""
    _eco_streaks[user_id] = 0


# @PRIVATE
def _get_eco_streak(user_id: str) -> int:
    """Get current ECO streak for user."""
    return _eco_streaks.get(user_id, 0)


# @PRIVATE
def _is_usage_footer_enabled(user_id: str) -> bool:
    """Check if usage footer is enabled for user (default: True)."""
    config = _load_config()
    user_prefs = config.get("user_preferences", {}).get(user_id, {})
    return user_prefs.get("show_usage_footer", True)


# @PRIVATE
def _toggle_usage_footer(user_id: str) -> bool:
    """Toggle usage footer for user. Returns new state."""
    config = _load_config()
    if "user_preferences" not in config:
        config["user_preferences"] = {}
    if user_id not in config["user_preferences"]:
        config["user_preferences"][user_id] = {}

    current = config["user_preferences"][user_id].get("show_usage_footer", True)
    config["user_preferences"][user_id]["show_usage_footer"] = not current
    _save_config(config)
    return not current


# @PRIVATE
def _format_eco_footer(user_id: str) -> str:
    """Format ECO mode footer with streak and savings."""
    # Check if user has footer disabled
    if not _is_usage_footer_enabled(user_id):
        return ""

    streak = _get_eco_streak(user_id)
    tokens_saved = streak * _TOKENS_PER_LLM_QUERY

    if streak == 0:
        return ""

    # Streak badges
    if streak >= 10:
        badge = ":evergreen_tree:"  # 10+ = tree
    elif streak >= 5:
        badge = ":seedling:"  # 5+ = seedling
    else:
        badge = ":leaves:"  # 1+ = leaves

    return f"\n{badge} ECO streak: {streak} | ~{tokens_saved:,} tokens saved"


# @PRIVATE
def _format_context_footer(user_id: str) -> str:
    """Format connection/project context footer."""
    instances = _get_instances()
    active_project = None

    # Get active project if set
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    active = user_config.get("active_project")
    if active:
        active_project = active.get("name")
        instance_name = active.get("instance")
    else:
        instance_name = None

    # Format context
    if len(instances) == 1:
        inst_display = list(instances.keys())[0]
    elif instance_name:
        inst_display = instance_name
    else:
        inst_display = "All"

    proj_display = active_project if active_project else "All Projects"

    return f"\n`[{inst_display}: {proj_display}]`"


# ============================================================================
# INSTANCE MANAGEMENT
# ============================================================================

# @PUBLIC_HELPER
def _get_instances() -> dict:
    """Get all configured Vikunja instances.

    Priority order:
    1. Config file instances (~/.vikunja-mcp/config.yaml)
    2. VIKUNJA_INSTANCES env var (JSON array)
    3. VIKUNJA_URL/VIKUNJA_TOKEN env vars as 'default'
    """
    config = _load_config()
    instances = dict(config.get("instances", {}))  # Copy to avoid mutating config

    # Parse VIKUNJA_INSTANCES env var (JSON array of {name, url, token})
    instances_json = os.environ.get("VIKUNJA_INSTANCES", "")
    if instances_json:
        try:
            import json
            instances_list = json.loads(instances_json)
            for inst in instances_list:
                name = inst.get("name", "").strip()
                url = inst.get("url", "").strip()
                token = inst.get("token", "").strip()
                # Only add if not already in config file (config takes precedence)
                if name and url and token and name not in instances:
                    instances[name] = {
                        "url": url.rstrip('/'),
                        "token": token
                    }
        except (json.JSONDecodeError, TypeError):
            pass  # Invalid JSON, skip

    # Always include env var instance as 'default' if set (unless explicitly configured)
    env_url = os.environ.get("VIKUNJA_URL")
    env_token = os.environ.get("VIKUNJA_BOT_TOKEN") or os.environ.get("VIKUNJA_TOKEN")
    if env_url and env_token and "default" not in instances:
        instances["default"] = {
            "url": env_url.rstrip('/'),
            "token": env_token
        }

    return instances


# @PUBLIC_HELPER
def _get_current_instance() -> Optional[str]:
    """Get the name of the currently active instance.

    Priority:
    1. mcp_context.instance (set by set_active_context tool)
    2. current_instance (set by switch_instance or config file)
    3. First configured instance as fallback
    """
    config = _load_config()

    # Check mcp_context FIRST - this is what set_active_context uses (solutions-c8sry)
    # Use `or {}` because YAML null becomes None, and .get() only uses default for missing keys
    mcp_instance = (config.get("mcp_context") or {}).get("instance")
    if mcp_instance:
        return mcp_instance

    # Fall back to current_instance
    current = config.get("current_instance")

    # If no current instance set, check if we have instances configured
    if not current:
        instances = _get_instances()
        if instances:
            # Default to first instance or "default" if it exists
            if "default" in instances:
                return "default"
            return next(iter(instances.keys()))

    return current


# @PUBLIC_HELPER
def _set_current_instance(name: str) -> None:
    """Set the currently active instance."""
    instances = _get_instances()
    if name not in instances:
        available = ", ".join(instances.keys()) if instances else "none configured"
        raise ValueError(f"Instance '{name}' not found. Available: {available}")

    config = _load_config()
    config["current_instance"] = name
    # Also update mcp_context.instance since it has higher priority in _get_current_instance
    if "mcp_context" not in config:
        config["mcp_context"] = {}
    config["mcp_context"]["instance"] = name
    _save_config(config)


# @PUBLIC_HELPER
def _get_instance_config(name: Optional[str] = None) -> tuple[str, str]:
    """Get URL and token for an instance.

    Args:
        name: Instance name, or None for current instance

    Returns:
        Tuple of (url, token)
    """
    if name is None:
        name = _get_current_instance()

    if name is None:
        # Fall back to env vars
        url = os.environ.get("VIKUNJA_URL")
        token = os.environ.get("VIKUNJA_BOT_TOKEN") or os.environ.get("VIKUNJA_TOKEN")  # Optional - user tokens replace this
        if url:
            # URL is required, token is optional (user tokens stored per-user)
            # Strip whitespace from both (solutions-zja1)
            return url.rstrip('/').strip(), (token or "").strip()
        raise ValueError("No instance configured. Set VIKUNJA_URL or configure instances.")

    instances = _get_instances()
    if name not in instances:
        raise ValueError(f"Instance '{name}' not found")

    instance = instances[name]
    url = instance.get("url")
    token = instance.get("token")

    # Support env var references in token (e.g., "${VIKUNJA_CLOUD_TOKEN}")
    if token and token.startswith("${") and token.endswith("}"):
        env_var = token[2:-1]
        token = os.environ.get(env_var)
        if not token:
            raise ValueError(f"Environment variable {env_var} not set for instance '{name}'")

    if not url or not token:
        raise ValueError(f"Instance '{name}' missing url or token")

    return url.rstrip('/'), token


# @PUBLIC_HELPER
def _get_instance_timezone(name: Optional[str] = None) -> Optional[str]:
    """Get timezone for an instance (e.g., 'America/Los_Angeles').

    Returns None if no timezone configured for the instance.
    """
    if name is None:
        name = _get_current_instance()

    if name is None:
        return None

    instances = _get_instances()
    if name not in instances:
        return None

    return instances[name].get("timezone")


# @PUBLIC_HELPER
def _get_instance_token_expires(name: Optional[str] = None) -> Optional[str]:
    """Get token expiration date for an instance (e.g., '2026-11-07').

    Returns None if no expiration date configured.
    """
    if name is None:
        name = _get_current_instance()

    if name is None:
        return None

    instances = _get_instances()
    if name not in instances:
        return None

    return instances[name].get("token_expires")


# @PRIVATE
def _get_user_instance_config(user_id: str) -> tuple[str, str, str]:
    """Get URL and token for a user's active instance.

    This function is user-aware and reads from PostgreSQL for the user's
    active instance and token.

    For Matrix/Slack bot users: Reads URL from PostgreSQL (TODO: solutions-mr8f)
    For MCP users: Reads URL from YAML config

    Args:
        user_id: Matrix/Slack user ID

    Returns:
        Tuple of (instance_name, url, token)

    Raises:
        ValueError: If user has no token configured
    """
    logger.debug(f"[_get_user_instance_config] user_id={user_id}")

    # Get user's active instance from PostgreSQL
    instance = _get_user_instance(user_id)
    if not instance:
        instance = "default"
    logger.debug(f"[_get_user_instance_config] active instance={instance}")

    # Get user's token for that instance from PostgreSQL
    token = _get_user_vikunja_token(user_id)
    if not token:
        logger.error(f"[_get_user_instance_config] No token found for user {user_id}, instance {instance}")
        raise ValueError(f"No Vikunja token configured for user {user_id}")
    logger.debug(f"[_get_user_instance_config] token retrieved (length={len(token)})")

    # Get URL from PostgreSQL (solutions-mr8f)
    from .token_broker import get_user_instance_url
    url = get_user_instance_url(user_id, instance)

    # Fall back to VIKUNJA_URL env var if not set in database
    if not url:
        url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        logger.debug(f"[_get_user_instance_config] url={url} (from VIKUNJA_URL env var fallback)")
    else:
        logger.debug(f"[_get_user_instance_config] url={url} (from PostgreSQL)")

    if not url:
        logger.error(f"[_get_user_instance_config] No URL configured for instance '{instance}'")
        raise ValueError(f"No URL configured for instance '{instance}'")

    logger.debug(f"[_get_user_instance_config] returning: instance={instance}, url={url}, token=***")
    return instance, url.rstrip('/'), token


# @PUBLIC_HELPER
def _get_effective_instance_config() -> tuple[str, str, str]:
    """Get instance config, preferring user context if available.

    This is the main function that tools should call to get instance config.
    It checks for user context (Matrix/Slack) and falls back to YAML config
    for MCP/CLI usage.

    Returns:
        Tuple of (instance_name, url, token)
    """
    user_id = _current_user_id.get()
    if user_id:
        # User context available - use PostgreSQL
        return _get_user_instance_config(user_id)
    else:
        # No user context - use YAML config (MCP/CLI mode)
        instance = _get_current_instance() or "default"
        url, token = _get_instance_config(instance)
        return instance, url, token


# @PUBLIC_HELPER
def _connect_instance(name: str, url: str, token: str, token_expires: str = "", timezone: str = "") -> dict:
    """Connect to a Vikunja instance (add to local config).

    Auto-switches to this instance if no current instance is set.

    Args:
        name: Instance name (e.g., 'personal', 'business')
        url: Base URL of the Vikunja instance
        token: API token
        token_expires: Optional expiration date (YYYY-MM-DD) for tracking
        timezone: Optional timezone for date conversion (e.g., 'America/Los_Angeles')
    """
    config = _load_config()
    if "instances" not in config:
        config["instances"] = {}

    # Check if we should auto-switch (no current instance)
    auto_switched = False
    if not config.get("current_instance"):
        config["current_instance"] = name
        # Also update mcp_context.instance since it has higher priority in _get_current_instance
        if "mcp_context" not in config:
            config["mcp_context"] = {}
        config["mcp_context"]["instance"] = name
        auto_switched = True

    instance_config = {
        "url": url.rstrip('/'),
        "token": token
    }
    if token_expires:
        instance_config["token_expires"] = token_expires
    if timezone:
        instance_config["timezone"] = timezone

    config["instances"][name] = instance_config
    _save_config(config)

    result = {"name": name, "url": url, "connected": True}
    if auto_switched:
        result["switched_to"] = name
        result["note"] = "Auto-switched (first connection)"
    if not token_expires:
        result["hint"] = "If you'd like me to track token expiration, let me know the expiration date (YYYY-MM-DD)"
    else:
        result["token_expires"] = token_expires
    return result


# @PUBLIC_HELPER
def _disconnect_instance(name: str) -> dict:
    """Disconnect from a Vikunja instance (remove from local config only - no data deleted)."""
    config = _load_config()
    instances = config.get("instances", {})

    if name not in instances:
        raise ValueError(f"Instance '{name}' not found")

    del config["instances"][name]

    # If disconnecting current instance, clear current
    if config.get("current_instance") == name:
        config["current_instance"] = None
        # Also clear mcp_context.instance since it has higher priority in _get_current_instance
        if "mcp_context" in config:
            config["mcp_context"]["instance"] = None

    _save_config(config)
    return {"name": name, "disconnected": True}


# @PUBLIC_HELPER
def _rename_instance(old_name: str, new_name: str) -> dict:
    """Rename a Vikunja instance, updating all references."""
    config = _load_config()
    instances = config.get("instances", {})

    if old_name not in instances:
        raise ValueError(f"Instance '{old_name}' not found")

    if new_name in instances:
        raise ValueError(f"Instance '{new_name}' already exists")

    # Copy instance config to new name
    config["instances"][new_name] = config["instances"][old_name]
    del config["instances"][old_name]

    # Update current_instance if needed
    if config.get("current_instance") == old_name:
        config["current_instance"] = new_name
    # Also update mcp_context.instance since it has higher priority in _get_current_instance
    if (config.get("mcp_context") or {}).get("instance") == old_name:
        config["mcp_context"]["instance"] = new_name

    # Update xq section if needed
    if "xq" in config and old_name in config["xq"]:
        config["xq"][new_name] = config["xq"][old_name]
        del config["xq"][old_name]

    # Update projects section - any project with instance: old_name
    if "projects" in config:
        for project_id, project_config in config["projects"].items():
            if project_config.get("instance") == old_name:
                project_config["instance"] = new_name

    _save_config(config)
    return {"old_name": old_name, "new_name": new_name, "renamed": True}


# @PRIVATE
def _list_instances_impl(user_id: str = None) -> dict:
    """List all configured Vikunja instances and user tokens.

    Args:
        user_id: Optional Matrix user ID to show their connected instances
    """
    # Get configured instances (YAML/env)
    instances = _get_instances()
    current = _get_current_instance()

    instance_list = []
    for name, config in instances.items():
        instance_list.append({
            "name": name,
            "url": config.get("url", ""),
            "current": name == current,
            "source": "config"
        })

    # Also get user tokens from PostgreSQL if user_id provided
    if user_id:
        from .token_broker import get_user_instances, get_user_active_instance
        try:
            user_instances = get_user_instances(user_id)
            active_instance = get_user_active_instance(user_id)

            for inst_name in user_instances:
                # Skip if already in list from config
                if any(i["name"] == inst_name for i in instance_list):
                    continue

                instance_list.append({
                    "name": inst_name,
                    "url": "https://vikunja.factumerit.app",  # Default URL
                    "current": inst_name == active_instance,
                    "source": "user_token"
                })
        except Exception as e:
            # Don't fail if token broker unavailable
            pass

    return {
        "instances": instance_list,
        "total": len(instance_list),
        "current": current
    }


# Initialize MCP server
mcp = FastMCP(
    "vikunja",
    instructions="Manage tasks, projects, labels, and kanban boards in Vikunja"
)

# Global reference to centralized poller (for health monitoring)
_centralized_poller = None


# Configuration from environment or instance config
# @PUBLIC
def get_config():
    """Get Vikunja configuration (URL, token) for current instance."""
    return _get_instance_config()


# @PRIVATE
def _get_user_vikunja_token(user_id: str) -> Optional[str]:
    """Get Vikunja API token for a user.

    Phase 2+: Reads from PostgreSQL first, falls back to YAML.
    Returns None if user is not configured (needs onboarding).
    """
    logger.debug(f"[_get_user_vikunja_token] user_id={user_id}")

    # Try PostgreSQL first (token broker)
    try:
        from .token_broker import get_user_token, AuthRequired, TokenBrokerUnavailable

        # Get user's active instance (or default)
        instance = _get_user_instance(user_id) or "default"
        logger.debug(f"[_get_user_vikunja_token] querying instance={instance}")

        token = get_user_token(
            user_id=user_id,
            purpose="get_user_token",
            instance=instance,
            caller="server._get_user_vikunja_token"
        )
        logger.debug(f"[_get_user_vikunja_token] token retrieved from PostgreSQL (length={len(token)})")
        return token
    except AuthRequired as e:
        # User not connected - fall through to YAML check
        logger.debug(f"[_get_user_vikunja_token] AuthRequired: {e}")
        pass
    except TokenBrokerUnavailable as e:
        # Database unavailable - fall back to YAML
        logger.warning(f"[_get_user_vikunja_token] Token broker unavailable, falling back to YAML: {e}")
    except Exception as e:
        logger.error(f"[_get_user_vikunja_token] Token broker error for {user_id}: {e}")

    # Fall back to YAML (legacy - for MCP users only, not Matrix/Slack bot)
    logger.debug(f"[_get_user_vikunja_token] Trying YAML fallback for user {user_id}")
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    token = user_config.get("vikunja_token")
    if token:
        logger.debug(f"[_get_user_vikunja_token] token retrieved from YAML (length={len(token)})")
    else:
        logger.debug(f"[_get_user_vikunja_token] No token found in YAML for user {user_id}")
    return token


# @PRIVATE
def _set_user_vikunja_token(user_id: str, token: str) -> dict:
    """Set Vikunja API token for a user.

    Phase 2 (dual-write): Writes to both YAML and PostgreSQL.
    YAML is primary, PostgreSQL is secondary (for migration).
    """
    # 1. Write to YAML (existing behavior)
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    config["users"][user_id]["vikunja_token"] = token
    _save_config(config)

    # 2. Write to PostgreSQL (token broker - Phase 2 dual-write)
    try:
        from .token_broker import set_user_token, TokenBrokerUnavailable
        from datetime import datetime, timedelta, timezone

        # Vikunja tokens expire after 1 year
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)

        # Get user's active instance (or default)
        instance = _get_user_instance(user_id) or "default"

        # Get URL from VIKUNJA_URL env var (OAuth onboarding - solutions-mr8f)
        instance_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

        set_user_token(
            user_id=user_id,
            token=token,
            source="dual-write",
            expires_at=expires_at,
            instance=instance,
            instance_url=instance_url,
            caller="server._set_user_vikunja_token"
        )
        logger.info(f"Token stored in PostgreSQL for {user_id} at {instance_url}")
    except TokenBrokerUnavailable as e:
        # Token broker not configured yet - continue with YAML only
        logger.warning(f"Token broker unavailable, using YAML only: {e}")
    except Exception as e:
        # Log but don't fail - YAML is still primary during migration
        logger.error(f"Failed to write token to PostgreSQL: {e}")

    return {"user_id": user_id, "vikunja_token_set": True}


# @PRIVATE
def _clear_user_vikunja_token(user_id: str) -> dict:
    """Clear Vikunja API token for a user (allows reconnecting).

    Phase 2 (dual-write): Clears from both YAML and PostgreSQL.
    """
    yaml_cleared = False
    pg_cleared = False

    # 1. Clear from YAML (existing behavior)
    config = _load_config()
    if "users" in config and user_id in config["users"]:
        if "vikunja_token" in config["users"][user_id]:
            del config["users"][user_id]["vikunja_token"]
            _save_config(config)
            yaml_cleared = True

    # 2. Revoke from PostgreSQL (token broker - Phase 2 dual-write)
    try:
        from .token_broker import revoke_user_token, TokenBrokerUnavailable

        pg_cleared = revoke_user_token(
            user_id=user_id,
            reason="user disconnected",
            caller="server._clear_user_vikunja_token"
        )
        if pg_cleared:
            logger.info(f"Token revoked in PostgreSQL for {user_id}")
    except TokenBrokerUnavailable as e:
        logger.warning(f"Token broker unavailable during clear: {e}")
    except Exception as e:
        logger.error(f"Failed to revoke token in PostgreSQL: {e}")

    if yaml_cleared or pg_cleared:
        return {"user_id": user_id, "token_cleared": True}
    return {"user_id": user_id, "token_cleared": False, "reason": "No token found"}


# @PRIVATE
def _get_room_binding(user_id: str, room_id: str) -> str | None:
    """Get user's personal room→project binding.
    
    Args:
        user_id: Matrix user ID (e.g., @user:matrix.org)
        room_id: Matrix room ID (e.g., !abc123:matrix.org)
    
    Returns:
        Project name/ID if bound, None otherwise
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    room_bindings = user_config.get("room_bindings", {})
    return room_bindings.get(room_id)


# @PRIVATE
def _set_room_binding(user_id: str, room_id: str, project: str) -> dict:
    """Set user's personal room→project binding.
    
    Args:
        user_id: Matrix user ID
        room_id: Matrix room ID
        project: Project name or ID to bind
    
    Returns:
        Dict with user_id, room_id, project, and success flag
    """
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    if "room_bindings" not in config["users"][user_id]:
        config["users"][user_id]["room_bindings"] = {}
    
    config["users"][user_id]["room_bindings"][room_id] = project
    _save_config(config)
    
    return {
        "user_id": user_id,
        "room_id": room_id,
        "project": project,
        "success": True
    }


# @PRIVATE
def _remove_room_binding(user_id: str, room_id: str) -> dict:
    """Remove user's personal room→project binding.
    
    Args:
        user_id: Matrix user ID
        room_id: Matrix room ID
    
    Returns:
        Dict with user_id, room_id, removed flag, and previous binding
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    room_bindings = user_config.get("room_bindings", {})
    
    previous = room_bindings.pop(room_id, None)
    
    if previous:
        _save_config(config)
    
    return {
        "user_id": user_id,
        "room_id": room_id,
        "removed": previous is not None,
        "previous_binding": previous
    }


# ============================================================================
# MATRIX USER INSTANCE/PROJECT CONTEXT (per-user persistence)
# ============================================================================

# @PRIVATE
def _get_user_instance(user_id: str) -> str | None:
    """Get user's active Vikunja instance from PostgreSQL.

    Args:
        user_id: Matrix user ID (e.g., @user:matrix.org)

    Returns:
        Instance name if set, None otherwise (uses default)
    """
    from .token_broker import get_user_active_instance
    return get_user_active_instance(user_id)


# @PRIVATE
def _set_user_instance(user_id: str, instance: str) -> dict:
    """Set user's active Vikunja instance in PostgreSQL.

    Args:
        user_id: Matrix user ID
        instance: Instance name to set as active

    Returns:
        Dict with user_id, instance, and success flag
    """
    # Validate instance exists (check both YAML config and user tokens)
    from .token_broker import get_user_instances

    # Get configured instances (YAML)
    configured_instances = _get_instances()

    # Get user's token instances (PostgreSQL)
    user_instances = get_user_instances(user_id)

    # Combine both sources
    all_instances = set(configured_instances.keys()) | set(user_instances)

    if all_instances and instance not in all_instances:
        return {
            "error": f"Instance '{instance}' not found. Available: {', '.join(sorted(all_instances))}"
        }

    # Write to PostgreSQL only
    from .token_broker import set_user_active_instance
    set_user_active_instance(user_id, instance)

    # Clear project context when switching instances (project IDs are instance-specific)
    _clear_user_project(user_id)

    # Get URL (prefer user token instance, fallback to configured)
    url = None
    if instance in configured_instances:
        url = configured_instances[instance].get("url")
    elif instance in user_instances:
        # For user tokens, we don't store URL separately yet
        # TODO: Store URL in user_tokens table
        url = "https://vikunja.factumerit.app"  # Default for now

    return {
        "user_id": user_id,
        "instance": instance,
        "url": url,
        "success": True
    }


# @PRIVATE
def _clear_user_instance(user_id: str) -> dict:
    """Clear user's active instance (revert to default).

    Args:
        user_id: Matrix user ID

    Returns:
        Dict with cleared status
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})

    if "active_instance" in user_config:
        del config["users"][user_id]["active_instance"]
        _save_config(config)
        return {"cleared": True}

    return {"cleared": False, "reason": "No instance was set"}


# @PRIVATE
def _get_user_project(user_id: str) -> dict | None:
    """Get user's active project context from PostgreSQL.

    Args:
        user_id: Matrix user ID

    Returns:
        Dict with project info if set, None otherwise
    """
    from .token_broker import get_user_active_project
    return get_user_active_project(user_id)


# @PRIVATE
def _set_user_project(user_id: str, project_id: int, project_name: str, instance: str = None) -> dict:
    """Set user's active project context in PostgreSQL.

    Args:
        user_id: Matrix user ID
        project_id: Project ID to set as active
        project_name: Project name for display
        instance: Instance name (optional, deprecated - kept for API compatibility)

    Returns:
        Dict with project info and success flag
    """
    from .token_broker import set_user_active_project

    set_user_active_project(user_id, project_id, project_name)

    return {
        "user_id": user_id,
        "project": {
            "id": project_id,
            "name": project_name
        },
        "success": True
    }


# @PRIVATE
def _clear_user_project(user_id: str) -> dict:
    """Clear user's active project context in PostgreSQL.

    Args:
        user_id: Matrix user ID

    Returns:
        Dict with cleared status
    """
    from .token_broker import set_user_active_project, get_user_active_project

    # Check if project was set
    current_project = get_user_active_project(user_id)
    if current_project:
        set_user_active_project(user_id, None)
        return {"cleared": True}

    return {"cleared": False, "reason": "No project was set"}


# @PRIVATE
def _format_user_context(user_id: str) -> str:
    """Format the user's current instance/project context as a footer.

    Args:
        user_id: Matrix user ID

    Returns:
        Formatted context string like "[personal: Kitchen]"
    """
    instances = _get_instances()

    # Get user's active instance
    user_instance = _get_user_instance(user_id)
    if not user_instance:
        # Fall back to default/first instance
        user_instance = _get_current_instance()

    # Get user's active project
    user_project = _get_user_project(user_id)
    project_name = user_project.get("name") if user_project else None

    # Format display
    if len(instances) <= 1:
        # Single instance or no instances configured
        # Use user's active instance if set, otherwise use first configured instance or "default"
        if user_instance:
            inst_display = user_instance
        elif instances:
            inst_display = list(instances.keys())[0]
        else:
            inst_display = "default"
    else:
        inst_display = user_instance or "All"

    proj_display = project_name if project_name else "All Projects"

    return f"`[{inst_display}: {proj_display}]`"


# ============================================================================
# MATRIX FIRST CONTACT / WELCOME TRACKING
# ============================================================================

# @PRIVATE
def _is_first_contact(user_id: str) -> bool:
    """Check if this is the user's first contact with the Matrix bot.

    Args:
        user_id: Matrix user ID (e.g., @user:matrix.org)

    Returns:
        True if user has never been welcomed, False otherwise
    """
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    return not user_config.get("matrix_welcomed", False)


# @PRIVATE
def _mark_user_welcomed(user_id: str) -> None:
    """Mark user as having received the Matrix welcome message.

    Args:
        user_id: Matrix user ID
    """
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}

    config["users"][user_id]["matrix_welcomed"] = True
    config["users"][user_id]["matrix_welcomed_at"] = datetime.now(timezone.utc).isoformat()
    _save_config(config)


# @PRIVATE
def _get_matrix_connect_prompt(user_id: str) -> str:
    """Generate connect prompt for Matrix users without Vikunja token.

    Uses one-click OAuth flow (same as Slack).

    Args:
        user_id: Matrix user ID

    Returns:
        Markdown-formatted connect instructions with one-click link
    """
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    # Create pending connection with nonce (platform auto-detected from user_id)
    nonce = _create_pending_connection(user_id)

    # Build connect URL (use popup flow - proven to work)
    connect_url = f"{vikunja_url}/matrix-connect?state={nonce}"

    return (
        "**Connect your Vikunja account:**\n\n"
        f"[Click here to connect]({connect_url})\n\n"
        "_One-time setup. This will create an API token and link it to your Matrix account._"
    )



# ============================================================================
# PENDING CONNECTION TRACKING (One-click OAuth flow)
# ============================================================================
# Now backed by PostgreSQL instead of YAML file (survives Render deploys)
# Bead: solutions-fp44

from .token_broker import (
    create_pending_connection as _create_pending_connection_pg,
    get_pending_connection as _get_pending_connection_pg,
    delete_pending_connection as _delete_pending_connection_pg,
    cleanup_expired_pending_connections as _cleanup_expired_pending_connections_pg,
)


# @PRIVATE
def _create_pending_connection(user_id: str, platform: str = None) -> str:
    """Create a pending connection for OAuth flow (PostgreSQL-backed).

    Args:
        user_id: User ID initiating the connection (Slack or Matrix)
        platform: Optional platform override. If not provided, auto-detected.

    Returns:
        nonce: Random state parameter to include in OAuth URL
    """
    return _create_pending_connection_pg(user_id, platform)


# @PRIVATE
def _get_pending_connection(nonce: str) -> Optional[dict]:
    """Get pending connection by nonce (PostgreSQL-backed).

    Returns None if nonce is invalid or expired.
    """
    return _get_pending_connection_pg(nonce)


# @PRIVATE
def _delete_pending_connection(nonce: str) -> bool:
    """Delete a pending connection after use (PostgreSQL-backed).

    Returns True if deleted, False if not found.
    """
    return _delete_pending_connection_pg(nonce)


# @PRIVATE
def _cleanup_expired_pending_connections() -> int:
    """Clean up expired pending connections (PostgreSQL-backed).

    Returns number of connections cleaned up.
    """
    return _cleanup_expired_pending_connections_pg()


# @PRIVATE
def _get_connect_prompt(user_id: str) -> str:
    """Generate one-click connect prompt for users without Vikunja token.

    Creates a pending connection and returns a message with the connect URL.
    """
    # Get Vikunja URL from environment
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    # Create pending connection with nonce
    nonce = _create_pending_connection(user_id)

    # Build connect URL
    connect_url = f"{vikunja_url}/slack-connect?state={nonce}"

    return (
        "Welcome to factum erit! Let's connect your Vikunja account.\n\n"
        f"*<{connect_url}|Click here to connect>* (one-time setup)\n\n"
        "_This will securely link your Slack and Vikunja accounts._"
    )


# @PRIVATE
def _get_welcome_message_for_new_user(user_id: str) -> str:
    """Generate welcome message for new workspace members.

    Introduces the bot and prompts them to connect their Vikunja account.
    """
    # Get Vikunja URL from environment
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    # Create pending connection with nonce
    nonce = _create_pending_connection(user_id)

    # Build connect URL
    connect_url = f"{vikunja_url}/slack-connect?state={nonce}"

    return (
        ":wave: *Welcome to Factum Erit!*\n\n"
        "I'm your AI task assistant. I'll help you stay on top of what matters.\n\n"
        "• Ask me anything: \"What's due today?\" or \"Add a task to buy groceries\"\n"
        "• Use slash commands: `/today`, `/week`, `/summary`\n"
        "• Set focus: `/project kitchen` to filter by project\n\n"
        "*Ready? Connect your account:*\n"
        f"*<{connect_url}|Click here to connect>* (one-time setup)\n\n"
        "_Once connected, just message me to get started!_"
    )




# ============================================================================
# ACTIVE PROJECT CONTEXT
# ============================================================================

# @PRIVATE
def _get_active_project_impl(user_id: str) -> dict:
    """Get user's active project context."""
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    active = user_config.get("active_project")

    if active:
        return {
            "active": True,
            "project": active
        }
    return {"active": False}


# @PRIVATE
def _clear_active_project_impl(user_id: str) -> dict:
    """Clear user's active project context."""
    config = _load_config()
    if "users" in config and user_id in config["users"]:
        if "active_project" in config["users"][user_id]:
            del config["users"][user_id]["active_project"]
            _save_config(config)
    return {"cleared": True}


# @PUBLIC_HELPER
def _connect_instance_impl(name: str, url: str, token: str) -> dict:
    """Connect a new Vikunja instance by validating and storing credentials.

    Args:
        name: Instance name (e.g., "personal", "work")
        url: Vikunja instance URL (e.g., "https://vikunja.example.com")
        token: API token from Vikunja Settings > API Tokens

    Returns:
        {success: True, name, url} or {error: str}
    """
    # Normalize URL
    url = url.rstrip("/")
    if not url.startswith("http"):
        url = f"https://{url}"

    # Validate token by making a test API call (use /projects which definitely works)
    try:
        response = requests.request(
            "GET",
            f"{url}/api/v1/projects",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        if response.status_code == 401:
            return {"error": "Invalid token - check your API token in Vikunja Settings"}
        if response.status_code != 200:
            return {"error": f"API error: HTTP {response.status_code}"}

        # Token works - we don't get username from /projects, so just say "connected"
        username = "connected"
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to {url} - check the URL"}
    except Exception as e:
        return {"error": f"Connection failed: {e}"}

    # Store in config
    config = _load_config()
    if "instances" not in config:
        config["instances"] = {}

    config["instances"][name] = {
        "url": url,
        "token": token
    }

    # If this is the first instance, set it as current
    if len(config["instances"]) == 1 or not config.get("current_instance"):
        config["current_instance"] = name
        # Also update mcp_context.instance since it has higher priority in _get_current_instance
        if "mcp_context" not in config:
            config["mcp_context"] = {}
        config["mcp_context"]["instance"] = name

    _save_config(config)

    return {
        "success": True,
        "name": name,
        "url": url,
        "username": username
    }


# @PUBLIC_HELPER
def _disconnect_instance_impl(name: str) -> dict:
    """Disconnect a Vikunja instance by removing it from config.

    Args:
        name: Instance name to remove

    Returns:
        {success: True, name} or {error: str}
    """
    config = _load_config()
    instances = config.get("instances", {})

    if name not in instances:
        available = list(instances.keys()) if instances else []
        if available:
            return {"error": f"Instance '{name}' not found. Available: {', '.join(available)}"}
        return {"error": f"Instance '{name}' not found. No instances configured."}

    # Remove the instance
    del config["instances"][name]

    # If this was the current instance, switch to another or clear
    if config.get("current_instance") == name:
        remaining = list(config["instances"].keys())
        new_current = remaining[0] if remaining else None
        config["current_instance"] = new_current
        # Also update mcp_context.instance since it has higher priority in _get_current_instance
        if "mcp_context" not in config:
            config["mcp_context"] = {}
        config["mcp_context"]["instance"] = new_current

    _save_config(config)

    return {"success": True, "name": name}


# @PUBLIC_HELPER
def _find_projects_by_name(query: str) -> list:
    """Find projects matching query across all instances.

    Returns list of {instance, project_id, name, task_count} sorted by instance then name.
    Uses fuzzy matching (case-insensitive, substring).
    """
    instances = _get_instances()
    matches = []
    query_lower = query.lower()
    errors = []

    for instance_name in instances.keys():
        try:
            # Use _get_instance_config to properly resolve env var tokens
            url, token = _get_instance_config(instance_name)
        except ValueError as e:
            errors.append(f"{instance_name}: {e}")
            continue

        try:
            # Fetch projects from this instance
            response = requests.request(
                "GET",
                f"{url}/api/v1/projects",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
            if response.status_code != 200:
                errors.append(f"{instance_name}: HTTP {response.status_code}")
                continue

            projects = response.json()

            # Recursively search through nested projects
# @PUBLIC
            def search_projects(project_list, parent_path=""):
                for project in project_list:
                    title = project.get("title", "")
                    full_path = f"{parent_path} > {title}" if parent_path else title
                    # Fuzzy match: case-insensitive substring
                    if query_lower in title.lower():
                        matches.append({
                            "instance": instance_name,
                            "project_id": project.get("id"),
                            "name": title,
                            "path": full_path,
                        })
                    # Recurse into child projects
                    children = project.get("child_projects") or []
                    if children:
                        search_projects(children, full_path)

            search_projects(projects)
        except Exception as e:
            errors.append(f"{instance_name}: {type(e).__name__}: {e}")
            continue

    # Log errors for debugging (visible in Render logs)
    if errors:
        import logging
        logging.warning(f"_find_projects_by_name('{query}'): {errors}")

    # Sort by instance, then name
    matches.sort(key=lambda m: (m["instance"], m["name"].lower()))

    # Include errors in result for debugging
    if not matches and errors:
        return [{"_errors": errors}]
    return matches


# @PRIVATE
def _set_active_project_impl(user_id: str, query: str, selection: int = 0) -> dict:
    """Set user's active project by fuzzy name match.

    Args:
        user_id: Slack user ID
        query: Project name to search for (fuzzy match)
        selection: If >0, select the Nth match (1-indexed) when ambiguous

    Returns:
        - {success: True, project: {...}} on unique match or valid selection
        - {ambiguous: True, matches: [...]} when multiple matches found
        - {error: str} on no matches or invalid selection
    """
    matches = _find_projects_by_name(query)

    if not matches:
        return {"error": f"No project found matching '{query}'"}

    # Check for debug errors
    if len(matches) == 1 and "_errors" in matches[0]:
        return {"error": f"No project found matching '{query}'. Debug: {matches[0]['_errors']}"}

    # If selection provided, use it
    if selection > 0:
        if selection > len(matches):
            return {"error": f"Invalid selection {selection}. Only {len(matches)} matches."}
        chosen = matches[selection - 1]
    elif len(matches) == 1:
        # Unique match
        chosen = matches[0]
    else:
        # Ambiguous - return options
        return {
            "ambiguous": True,
            "matches": matches,
            "query": query
        }

    # Save to config
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}

    config["users"][user_id]["active_project"] = {
        "instance": chosen["instance"],
        "project_id": chosen["project_id"],
        "name": chosen["name"]
    }
    _save_config(config)

    return {
        "success": True,
        "project": config["users"][user_id]["active_project"]
    }


# @PRIVATE
def _format_project_for_slack(result: dict) -> str:
    """Format /project command result for Slack."""
    if "error" in result:
        return f":warning: {result['error']}"

    if result.get("cleared"):
        return ":white_check_mark: Active project cleared. Commands will query all projects."

    if result.get("ambiguous"):
        lines = [f"Found '{result['query']}' in multiple places:\n"]
        for i, match in enumerate(result["matches"], 1):
            path = match.get("path", match["name"])
            lines.append(f"{i}. {match['instance']}: {path}")
        lines.append(f"\nUse: `/project {result['query']} 1` or `/project {result['query']} 2`")
        return "\n".join(lines)

    if result.get("success"):
        proj = result["project"]
        return f":white_check_mark: Active project: *{proj['name']}* ({proj['instance']})"

    if result.get("active"):
        proj = result["project"]
        return f"*Active project:* {proj['name']} ({proj['instance']})\n\nUse `/project clear` to query all projects."

    if result.get("active") is False:
        return "No active project set. Commands query all projects.\n\nUse `/project <name>` to focus on a project."

    return ":warning: Unknown result"


# @PUBLIC_HELPER
def _request(method: str, endpoint: str, allow_instance_fallback: bool = False, **kwargs) -> dict:
    """Make authenticated request to Vikunja API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (e.g., /api/v1/tasks)
        allow_instance_fallback: If True, fall back to VIKUNJA_TOKEN env var.
            Default is False for security - user requests MUST have a user token set.
            Only set to True for CLI/MCP usage or system operations.
        **kwargs: Additional arguments passed to requests.request()

    Token resolution:
    1. Context variable _current_vikunja_token (set by auth check for user requests)
    2. Instance token from VIKUNJA_TOKEN env var (ONLY if allow_instance_fallback=True)

    Raises:
        ValueError: If no token is available
    """
    # Get URL and default token from instance config
    # Three modes:
    # 1. User context (Matrix/Slack): Get from PostgreSQL
    # 2. Bot mode (@eis): Get from env vars (VIKUNJA_URL + VIKUNJA_BOT_TOKEN)
    # 3. MCP/CLI mode: Get from YAML config (multi-instance)
    user_id = _current_user_id.get()
    bot_mode = _bot_mode.get()

    if user_id:
        # User context available - get URL from PostgreSQL
        instance_name, base_url, instance_token = _get_user_instance_config(user_id)
        logger.debug(f"[_request] User context: user={user_id}, instance={instance_name}, url={base_url}")
    elif bot_mode:
        # Bot mode (@eis) - use env vars, NOT YAML config (solutions-zja1)
        base_url = os.environ.get("VIKUNJA_URL", "")
        instance_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")
        if base_url:
            base_url = base_url.rstrip('/').strip()
        if instance_token:
            instance_token = instance_token.strip()
        logger.debug(f"[_request] Bot mode: using env vars, url={base_url}")
    else:
        # No user context - use YAML config (MCP/CLI mode)
        base_url, instance_token = _get_instance_config()
        logger.debug(f"[_request] No user context, using YAML config: url={base_url}")

    # Check context var first (per-user token set by auth check)
    token = _current_vikunja_token.get()
    if token:
        logger.debug(f"[_request] Using user token from context var (length={len(token)})")
        # Debug: Log token prefix for solutions-zja1 investigation
        logger.info(f"[_request] Token prefix: {token[:20]}... (total length: {len(token)})")
    else:
        logger.debug(f"[_request] No user token in context var")

    # SECURITY: Only fall back to instance token if explicitly allowed
    # This prevents user requests from accidentally using the admin token
    if not token:
        # Check both parameter AND context var for fallback permission
        fallback_allowed = allow_instance_fallback or _allow_instance_fallback.get()
        if fallback_allowed:
            token = instance_token
            logger.debug(f"Using instance fallback token for {method} {endpoint}")
            # Debug: Log instance token prefix for solutions-zja1 investigation
            logger.info(f"[_request] Instance token prefix: {instance_token[:20] if instance_token else 'None'}... (total length: {len(instance_token) if instance_token else 0})")
        else:
            # Log security event - this should not happen if auth check is working
            logger.warning(
                f"SECURITY: No user token set for {method} {endpoint}. "
                "This may indicate a missing auth check. Rejecting request."
            )
            raise ValueError(
                "No Vikunja token available. Please connect with !vik first."
            )

    if not token:
        raise ValueError("No Vikunja token available")

    full_url = f"{base_url}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Log project-specific requests at INFO level for debugging
    if "/projects/" in endpoint and "/tasks" in endpoint:
        logger.info(f"[_request] {method} {full_url} (params={kwargs.get('params', {})})")
    else:
        logger.debug(f"[_request] {method} {full_url} (params={kwargs.get('params', {})})")

    # Performance tracking
    start_time = time.time()
    response = requests.request(method, full_url, headers=headers, **kwargs)
    elapsed_ms = (time.time() - start_time) * 1000

    # Log project-specific responses at INFO level
    if "/projects/" in endpoint and "/tasks" in endpoint:
        logger.info(f"[_request] Response: {response.status_code} ({elapsed_ms:.0f}ms) - Body length: {len(response.text)}")
    else:
        logger.debug(f"[_request] Response: {response.status_code} ({elapsed_ms:.0f}ms)")

    if PERF_LOGGING:
        logger.info(f"[PERF] {method} {endpoint} → {response.status_code} ({elapsed_ms:.0f}ms)")

    if response.status_code == 401:
        logger.error(f"[_request] 401 Unauthorized: {response.text[:200]}")
        raise ValueError(f"Authentication failed: {response.text}")
    elif response.status_code == 404:
        logger.error(f"[_request] 404 Not Found: {response.text[:200]}")
        raise ValueError(f"Resource not found: {response.text}")
    elif response.status_code >= 400:
        logger.error(f"[_request] {response.status_code} Error: {response.text[:200]}")
        raise ValueError(f"API error ({response.status_code}): {response.text}")

    if method != "DELETE":
        data = response.json()
        if isinstance(data, list):
            logger.debug(f"[_request] Returned {len(data)} items")
        elif isinstance(data, dict):
            logger.debug(f"[_request] Returned dict with keys: {list(data.keys())[:5]}")
        return data
    return {}


# @PUBLIC_HELPER
def _fetch_all_pages(
    method: str,
    endpoint: str,
    per_page: int = 50,
    max_pages: int = 100,
    params: dict = None,
    **kwargs
) -> list:
    """Fetch all pages from a paginated Vikunja API endpoint.

    Vikunja APIs return max 50 items per page (server-side limit).
    This function iterates through all pages until:
    - A page returns fewer items than per_page (last page)
    - An empty page is returned
    - max_pages limit is reached (safety against infinite loops)

    Args:
        method: HTTP method (usually "GET")
        endpoint: API endpoint path
        per_page: Items per page (Vikunja caps at 50)
        max_pages: Safety limit to prevent infinite loops
        params: Query parameters (page will be added/overwritten)
        **kwargs: Additional arguments passed to _request

    Returns:
        List of all items from all pages combined
    """
    all_items = []
    params = dict(params) if params else {}
    params["per_page"] = per_page

    for page in range(1, max_pages + 1):
        params["page"] = page
        try:
            data = _request(method, endpoint, params=params, **kwargs)
        except ValueError as e:
            # Re-raise auth and critical errors
            if "Authentication" in str(e) or "401" in str(e):
                raise
            # Stop on other errors (e.g., page doesn't exist)
            break
        except Exception:
            # Stop on unexpected errors
            break

        if not isinstance(data, list):
            # Unexpected response format
            break

        all_items.extend(data)

        # Stop if we got fewer items than requested (last page)
        if len(data) < per_page:
            break

    return all_items


# Formatters

# @PUBLIC_HELPER
def _format_task(task: dict) -> dict:
    """Format task for MCP response."""
    reminders = task.get("reminders") or []
    return {
        "id": task["id"],
        "title": task["title"],
        "description": task.get("description", ""),
        "done": task.get("done", False),
        "priority": task.get("priority", 0),
        "position": task.get("position"),  # view-specific position (may be None)
        "start_date": task.get("start_date"),
        "end_date": task.get("end_date"),
        "due_date": task.get("due_date"),
        "repeat_after": task.get("repeat_after", 0),  # seconds between repeats (0 = no repeat)
        "repeat_mode": task.get("repeat_mode", 0),  # 0 = from due date, 1 = from completion
        "reminders": [r.get("reminder") for r in reminders],
        "project_id": task.get("project_id") or task.get("list_id", 0),
        "bucket_id": task.get("bucket_id", 0),
        "labels": [{"id": l["id"], "title": l["title"]} for l in (task.get("labels") or [])],
        "assignees": [{"id": a["id"], "username": a.get("username", "")} for a in (task.get("assignees") or [])],
    }


# @PUBLIC_HELPER
def _format_project(project: dict) -> dict:
    """Format project for MCP response."""
    return {
        "id": project["id"],
        "title": project["title"],
        "description": project.get("description", ""),
        "parent_project_id": project.get("parent_project_id", 0),
        "hex_color": project.get("hex_color", ""),
        "is_favorite": project.get("is_favorite", False),
        "position": project.get("position", 0),
    }


# @PUBLIC_HELPER
def _format_label(label: dict) -> dict:
    """Format label for MCP response."""
    return {
        "id": label["id"],
        "title": label["title"],
        "hex_color": label.get("hex_color", ""),
    }


# @PUBLIC_HELPER
def _format_bucket(bucket: dict) -> dict:
    """Format bucket for MCP response."""
    return {
        "id": bucket["id"],
        "title": bucket["title"],
        "project_id": bucket.get("project_id") or bucket.get("list_id", 0),
        "position": bucket.get("position", 0),
        "limit": bucket.get("limit", 0),
    }


# @PUBLIC_HELPER
def _format_view(view: dict) -> dict:
    """Format view for MCP response."""
    result = {
        "id": view["id"],
        "title": view["title"],
        "project_id": view.get("project_id", 0),
        "view_kind": view.get("view_kind", ""),
    }
    # Include filter if present - handle both string and object formats
    # (Vikunja API changed from object to string format)
    if "filter" in view and view["filter"]:
        filter_val = view["filter"]
        if isinstance(filter_val, str):
            # New format: filter is the query string directly
            filter_query = filter_val
        elif isinstance(filter_val, dict):
            # Old format: filter is an object with "filter" key
            filter_query = filter_val.get("filter", "")
        else:
            filter_query = ""
        if filter_query:
            result["filter"] = filter_query
    return result




# @PUBLIC_HELPER
def _format_relation(task_id: int, relation_kind: str, other_task: dict) -> dict:
    """Format task relation for MCP response."""
    return {
        "task_id": task_id,
        "other_task_id": other_task["id"],
        "other_task_title": other_task.get("title", ""),
        "relation_kind": relation_kind,
    }


# ============================================================================
# PROJECT OPERATIONS
# ============================================================================

# @PUBLIC_HELPER
def _list_projects_impl() -> list[dict]:
    # Fetch all pages for projects
    response = _fetch_all_pages("GET", "/api/v1/projects", per_page=50, max_pages=20)
    return [_format_project(p) for p in response]


# @PUBLIC_HELPER
def _get_project_impl(project_id: int) -> dict:
    response = _request("GET", f"/api/v1/projects/{project_id}")
    return _format_project(response)


# @PUBLIC_HELPER
def _create_project_impl(title: str, description: str = "", hex_color: str = "", parent_project_id: int = 0) -> dict:
    """Create a project - routes to queue system for bot mode, direct creation for MCP mode.

    Bead: solutions-eofy

    Bot mode (EARS @mentions): Queue project for user to create with their session token.
    MCP mode (Claude Desktop): Create project directly with user's token (works fine).
    """
    # Check if we're in bot mode (Vikunja EARS) vs MCP mode (Claude Desktop)
    bot_mode = _bot_mode.get()

    if bot_mode:
        # Bot mode: Use queue system (solutions-eofy)
        return _create_project_impl_queue(title, description, hex_color, parent_project_id)
    else:
        # MCP mode: Direct creation (existing behavior)
        return _create_project_impl_direct(title, description, hex_color, parent_project_id)


# @PRIVATE
def _create_project_impl_direct(title: str, description: str = "", hex_color: str = "", parent_project_id: int = 0) -> dict:
    """Direct project creation for MCP mode - user's token, works fine."""
    # Security: Sanitize title (strip HTML)
    data = {"title": _sanitize_title(title)}
    if description:
        data["description"] = description
    if hex_color:
        data["hex_color"] = hex_color
    if parent_project_id:
        data["parent_project_id"] = parent_project_id

    response = _request("PUT", "/api/v1/projects", json=data)
    project = _format_project(response)
    new_project_id = project.get("id")

    shared_with = []

    # Auto-transfer: If bot created this project, clone it to owner's account (solutions-2x6i)
    # DISABLED: Project cloning disabled due to JWT token expiry issues (solutions-eofy)
    # Owner JWT tokens expire after 24 hours, but we only store them once during signup.
    # This causes cloning to fail for users who haven't logged in recently.
    #
    # Alternative approach: Bot creates project and shares it with owner (see fallback sharing below).
    # Owner can access bot-owned projects just fine - they just don't "own" them.
    #
    # TODO: Implement one of these solutions:
    # 1. Store owner credentials (encrypted) and get fresh JWT on demand
    # 2. Implement JWT refresh token flow
    # 3. Accept that projects are bot-owned and shared with users
    requesting_user = _requesting_user.get()
    if False and new_project_id and requesting_user:  # Disabled for now
        try:
            from .project_cloner import clone_project_to_user
            from .bot_provisioning import get_bot_owner_token, get_user_bot_credentials
            from .bot_jwt_manager import get_bot_jwt
            from .token_broker import get_user_token, AuthRequired

            # Get bot's JWT token (to read bot's project)
            # Bot API tokens are broken (Vikunja issue #105), so we use JWT auth
            user_id_for_lookup = f"vikunja:{requesting_user}"
            bot_token = None

            bot_creds = get_user_bot_credentials(user_id_for_lookup)
            if bot_creds:
                bot_username, bot_password = bot_creds
                bot_token = get_bot_jwt(bot_username, bot_password, os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app"))
                logger.info(f"[create_project] Got bot JWT token for {bot_username}")

            # Get user's JWT token (to create project in user's account)
            # First check personal_bots table (stored during signup)
            # Then fall back to token_broker (OIDC-authenticated users)
            user_token = None

            user_token = get_bot_owner_token(user_id_for_lookup)
            if user_token:
                logger.info(f"[create_project] Using owner token from personal_bots for {requesting_user}")
            else:
                # Fall back to OIDC token
                try:
                    user_token = get_user_token(
                        user_id=requesting_user,
                        purpose="clone_bot_project",
                        caller="server._create_project_impl"
                    )
                    logger.info(f"[create_project] Using OIDC token from token_broker for {requesting_user}")
                except AuthRequired as e:
                    logger.info(f"[create_project] User {requesting_user} has no token (not in personal_bots or token_broker), skipping clone: {e}")
                    # Fall through to return bot's project (still works, just not in user's account)

            if bot_token and user_token:
                logger.info(f"[create_project] Cloning bot project {new_project_id} to user {requesting_user}")

                # Clone project from bot's account to user's account
                result = clone_project_to_user(
                    bot_project_id=new_project_id,
                    target_user_token=user_token,
                    bot_token=bot_token,  # Bot's JWT token (not broken API token)
                    parent_project_id=parent_project_id,
                    delete_original=True  # Delete bot's copy after cloning
                )

                if result["success"]:
                    # Return the user's project instead of bot's project
                    user_project_id = result["user_project_id"]
                    logger.info(f"[create_project] Successfully cloned: bot#{new_project_id} → user#{user_project_id}")

                    # Fetch and return the user's project
                    user_project = _request("GET", f"/api/v1/projects/{user_project_id}")
                    return _format_project(user_project)
                else:
                    logger.error(f"[create_project] Clone failed: {result.get('error')}")
                    # Fall through to return bot's project
            else:
                logger.info(f"[create_project] Skipping clone (bot_token={bool(bot_token)}, user_token={bool(user_token)})")
        except AuthRequired as e:
            # User hasn't authenticated - this is expected for users who haven't done OIDC yet
            logger.info(f"[create_project] User {requesting_user} not authenticated, skipping clone: {e}")
        except Exception as e:
            logger.error(f"[create_project] Failed to clone project to user: {e}", exc_info=True)

    # Auto-share: If this is a subproject, inherit users from parent
    if parent_project_id and new_project_id:
        try:
            parent_users = _request("GET", f"/api/v1/projects/{parent_project_id}/users")
            logger.info(f"[create_project] Parent project {parent_project_id} has {len(parent_users)} users: {[u.get('username') for u in parent_users]}")
            for user in parent_users:
                # NOTE: user.get("id") is the RELATION ID, not user ID!
                # The actual user_id is excluded from JSON response (json:"-")
                # We must look up the real user ID by username
                username = user.get("username", "")
                right = user.get("right", 2)  # Preserve their permission level
                if username:
                    try:
                        # Look up real user ID by username
                        user_search = _request("GET", f"/api/v1/users?s={username}")
                        matching = [u for u in user_search if u.get("username", "").lower() == username.lower()]
                        if matching:
                            real_user_id = matching[0]["id"]
                            logger.info(f"[create_project] Inheriting user {username} (real_id={real_user_id}) from parent")
                            _request("PUT", f"/api/v1/projects/{new_project_id}/users", json={
                                "user_id": str(real_user_id),  # Vikunja expects string
                                "right": right
                            })
                            shared_with.append(username)
                        else:
                            logger.warning(f"[create_project] Could not find user {username} via search")
                    except Exception as e:
                        logger.warning(f"[create_project] Failed to inherit user {username}: {e}")
            if shared_with:
                logger.info(f"[create_project] Inherited access from parent: {shared_with}")
        except Exception as e:
            logger.warning(f"[create_project] Failed to inherit users from parent: {e}")

    # Fallback sharing: Share bot's project with requesting user
    # This ensures users can access bot-created projects with admin rights
    # Uses bot's JWT token to share (bot owns the project)
    # Uses requesting_user_id directly (no user search needed - passed from poller)
    requesting_user_id = _requesting_user_id.get()
    if new_project_id and requesting_user_id:
        # Skip if already shared via cloning or parent inheritance
        if not requesting_user or requesting_user.lower() not in [u.lower() for u in shared_with]:
            try:
                from .bot_provisioning import get_user_bot_credentials
                from .bot_jwt_manager import get_bot_jwt
                import httpx

                # Get bot's JWT token (to share the project it owns)
                user_id_for_lookup = f"vikunja:{requesting_user}" if requesting_user else None
                bot_token = None

                if user_id_for_lookup:
                    bot_creds = get_user_bot_credentials(user_id_for_lookup)
                    if bot_creds:
                        bot_username, bot_password = bot_creds
                        bot_token = get_bot_jwt(bot_username, bot_password, os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app"))
                        logger.info(f"[create_project] Got bot JWT token for sharing: {bot_username}")

                if not bot_token:
                    logger.warning(f"[create_project] No personal bot found for {requesting_user} - user may be legacy account created before bot provisioning was added. Projects will be created in shared bot account.")
                else:
                    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

                    # Share project using bot's JWT token (bot owns it)
                    # Use requesting_user (username) - Vikunja API expects "username" field, not "user_id"
                    # See: solutions-2x6i, 111-BOT_PROJECT_SHARING_BUG.md
                    logger.info(f"[create_project] Sharing project {new_project_id} with user {requesting_user}")
                    share_resp = httpx.put(
                        f"{vikunja_url}/api/v1/projects/{new_project_id}/users",
                        headers={"Authorization": f"Bearer {bot_token}"},
                        json={
                            "username": requesting_user,  # Vikunja expects "username", not "user_id"
                            "right": 2  # Admin access
                        },
                        timeout=10
                    )
                    share_resp.raise_for_status()
                    shared_with.append(requesting_user)
                    logger.info(f"[create_project] Successfully shared bot project with {requesting_user}")
            except Exception as e:
                logger.warning(f"[create_project] Failed to auto-share with {requesting_user}: {e}")

    if shared_with:
        project["shared_with"] = shared_with

    return project


# @PRIVATE
def _create_project_impl_queue(title: str, description: str = "", hex_color: str = "", parent_project_id: int = 0) -> dict:
    """Queue project for user-side creation (bot mode only).

    Bead: solutions-eofy, fa-j967 (dedup fix)

    Instead of bot creating the project (which causes permission issues),
    we queue the project spec for the user's frontend to create using their
    active session token. This ensures:
    - User owns the project from the start
    - No token expiry issues (uses active session)
    - Bot gets access (user shares back)

    Supports batching: Multiple create_project calls in one LLM turn are
    batched into a single queue entry with projects as JSON array.

    Deduplication (fa-j967): Checks for existing pending/processing queue entries
    with the same title to prevent duplicate project creation from LLM retries.
    """
    # Security: Sanitize title (strip HTML)
    sanitized_title = _sanitize_title(title)

    # Get user context
    requesting_user = _requesting_user.get()  # e.g., "ivan"
    requesting_user_id = _requesting_user_id.get()  # Numeric ID from bot mode

    if not requesting_user:
        logger.warning("[create_project_queue] No requesting_user, falling back to direct creation")
        return _create_project_impl_direct(sanitized_title, description, hex_color, parent_project_id)

    # Construct user_id for bot_provisioning lookup
    # Bot mode uses "vikunja:username" format
    user_id = f"vikunja:{requesting_user}"

    # Get bot username for sharing back
    from .bot_provisioning import get_user_bot_credentials
    bot_username = None
    bot_creds = get_user_bot_credentials(user_id)
    if bot_creds:
        bot_username, _ = bot_creds

    if not bot_username:
        logger.warning(f"[create_project_queue] No bot found for {requesting_user} (user_id={user_id}), falling back to direct creation")
        return _create_project_impl_direct(sanitized_title, description, hex_color, parent_project_id)

    # === DEDUPLICATION CHECK (fa-j967) ===
    # Check if a project with this title is already pending/processing for this user
    try:
        from .token_broker import execute
        import json

        # Check for exact title match in pending/processing queue entries
        # Also check the batch projects JSONB column for title matches
        existing = execute("""
            SELECT id, status, title, projects
            FROM project_creation_queue
            WHERE username = %s
              AND status IN ('pending', 'processing')
              AND (
                  title = %s
                  OR projects::text ILIKE %s
              )
            ORDER BY created_at DESC
            LIMIT 1
        """, (requesting_user, sanitized_title, f'%"title": "{sanitized_title}"%'))

        if existing:
            queue_id, status, existing_title, existing_projects = existing[0]
            logger.warning(f"[create_project_queue] DEDUP: Project '{sanitized_title}' already {status} in queue (id={queue_id}) for {requesting_user}")

            # Return a clear message that this is a duplicate
            return {
                "id": None,
                "title": sanitized_title,
                "status": "already_queued",
                "message": f"A project named '{sanitized_title}' is already queued for creation. "
                           f"Please click the creation link in the previous message, or wait for it to be processed. "
                           f"Do NOT retry - this will create duplicates.",
                "existing_queue_id": queue_id,
                "existing_status": status
            }
    except Exception as e:
        # Log but don't fail - dedup is best-effort
        logger.warning(f"[create_project_queue] Dedup check failed (continuing): {e}")

    # Also check current batch for duplicates (same LLM turn)
    pending = _pending_projects.get()
    if pending is None:
        # Initialize batch mode for this LLM turn
        pending = []
        _pending_projects.set(pending)
    else:
        # Check if title already in current batch
        for spec in pending:
            if spec.get("title", "").lower() == sanitized_title.lower():
                logger.warning(f"[create_project_queue] DEDUP: Project '{sanitized_title}' already in current batch for {requesting_user}")
                return {
                    "id": spec.get("temp_id"),
                    "title": sanitized_title,
                    "status": "already_in_batch",
                    "message": f"Project '{sanitized_title}' is already queued in this request. No duplicate created."
                }

    # Assign temporary negative ID for parent references
    temp_id = _next_temp_id.get()
    _next_temp_id.set(temp_id - 1)

    # Add to batch
    project_spec = {
        "temp_id": temp_id,
        "title": sanitized_title,
        "description": description,
        "hex_color": hex_color,
        "parent_project_id": parent_project_id
    }
    pending.append(project_spec)

    logger.info(f"[create_project_queue] Queued project '{sanitized_title}' (temp_id={temp_id}) for {requesting_user}")

    # Return with CLEAR messaging that this is QUEUED, not created (fa-j967)
    return {
        "id": temp_id,  # Negative temp ID
        "title": sanitized_title,
        "description": description,
        "hex_color": hex_color,
        "parent_project_id": parent_project_id,
        "status": "queued_for_creation",
        "message": f"Project '{sanitized_title}' has been QUEUED for creation. "
                   f"The user must click the creation link to actually create it. "
                   f"Do NOT tell the user the project has been created - it has only been queued. "
                   f"Do NOT retry if the user says they don't see it - direct them to click the link. "
                   f"IMPORTANT: Do NOT use this temp_id ({temp_id}) for subsequent operations like "
                   f"setup_kanban_board, batch_create_tasks, create_task, etc. - those will FAIL. "
                   f"Wait for the user to create the project and get the real project ID."
    }


# @PRIVATE
def _flush_project_queue() -> Optional[int]:
    """Flush pending projects to database queue (called at end of LLM turn).

    Returns queue entry ID if successful, None otherwise.
    """
    pending = _pending_projects.get()
    if not pending:
        return None  # Nothing to flush

    requesting_user = _requesting_user.get()

    if not requesting_user:
        logger.warning("[flush_project_queue] No requesting_user, cannot flush")
        return None

    # Construct user_id for bot_provisioning lookup
    user_id = f"vikunja:{requesting_user}"

    # Get bot username
    from .bot_provisioning import get_user_bot_credentials
    bot_username = None
    bot_creds = get_user_bot_credentials(user_id)
    if bot_creds:
        bot_username, _ = bot_creds

    if not bot_username:
        logger.warning(f"[flush_project_queue] No bot found for {requesting_user} (user_id={user_id})")
        return None

    try:
        import json
        from .token_broker import execute

        # Insert batch as JSON (using execute helper for PostgreSQL)
        rows = execute("""
            INSERT INTO project_creation_queue
            (user_id, username, bot_username, projects, status)
            VALUES (%s, %s, %s, %s, 'pending')
            RETURNING id
        """, (user_id, requesting_user, bot_username, json.dumps(pending)))

        queue_id = rows[0][0] if rows else None
        if not queue_id:
            logger.error("[flush_project_queue] Failed to get queue ID from insert")
            return None

        logger.info(f"[flush_project_queue] Flushed {len(pending)} projects to queue (id={queue_id}) for {requesting_user}")

        # Clear batch
        _pending_projects.set(None)
        _next_temp_id.set(-1)

        return queue_id
    except Exception as e:
        logger.error(f"[flush_project_queue] Failed to flush batch: {e}", exc_info=True)
        return None


# @PUBLIC_HELPER
def _delete_project_impl(project_id: int) -> dict:
    _request("DELETE", f"/api/v1/projects/{project_id}")
    return {"deleted": True, "project_id": project_id}


# @PUBLIC_HELPER
def _get_project_users_impl(project_id: int) -> dict:
    """Get users with access to a project.

    Note: The Vikunja API returns a relation_id (not user_id) in the 'id' field.
    The actual user_id is excluded from the JSON response. Use username for
    lookups via /api/v1/users?s={username} if you need the real user ID.
    """
    users = _request("GET", f"/api/v1/projects/{project_id}/users")
    return {
        "project_id": project_id,
        "users": [
            {
                "relation_id": u.get("id"),  # NOTE: This is NOT user_id, it's the relation ID
                "username": u.get("username"),
                "name": u.get("name"),
                "right": u.get("right"),  # 0=read, 1=read+write, 2=admin
            }
            for u in users
        ]
    }


# @PUBLIC_HELPER
def _share_project_impl(project_id: int, username: str = "", user_id: int = 0, right: int = 2) -> dict:
    """Share a project with a user by username.

    Args:
        project_id: Project to share
        username: Username to share with (required - Vikunja API uses username)
        user_id: Deprecated - Vikunja API doesn't accept user_id, only username
        right: Permission level (0=read, 1=read+write, 2=admin). Default is admin.

    Returns:
        Success/failure status
    """
    # Vikunja API uses username, not user_id
    if not username:
        return {"error": "Username is required (Vikunja API uses username, not user_id)"}

    # Get requesting user's token for the share call
    # Bot tokens can't share projects - need user's own token
    requesting_user = _requesting_user.get()
    user_token = None
    if requesting_user:
        try:
            from .token_broker import get_user_token
            # User ID format is "vikunja:username" - need to construct it
            token_user_id = f"vikunja:{requesting_user}"
            user_token = get_user_token(
                user_id=token_user_id,
                purpose="share_project",
                caller="server._share_project_impl"
            )
            logger.info(f"[share_project] Got user token for {requesting_user}")
        except Exception as e:
            logger.warning(f"[share_project] Could not get user token: {e}")

    # Add user to project - Vikunja API uses username, not user_id
    try:
        if user_token:
            # Use user's token for sharing (bot token can't share)
            import httpx
            base_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app").rstrip("/")
            resp = httpx.put(
                f"{base_url}/api/v1/projects/{project_id}/users",
                headers={"Authorization": f"Bearer {user_token}"},
                json={"username": username, "right": right},
                timeout=30.0,
            )
            if resp.status_code >= 400:
                return {"error": f"Share failed: {resp.status_code} - {resp.text}"}
            logger.info(f"[share_project] Shared project {project_id} with {username} using user token")
        else:
            # Use bot token - should work now with username
            _request("PUT", f"/api/v1/projects/{project_id}/users", json={
                "username": username,
                "right": right
            })

        right_names = {0: "read", 1: "read+write", 2: "admin"}
        return {
            "success": True,
            "project_id": project_id,
            "user_id": user_id,
            "username": username or requesting_user,
            "right": right_names.get(right, str(right))
        }
    except Exception as e:
        return {"error": f"Failed to share project: {e}"}


# @PRIVATE
def _create_link_share_impl(project_id: int, right: int = 0, name: str = "") -> dict:
    """Create a public link share for a project.

    Args:
        project_id: Project to create share link for
        right: Permission level (0=read-only, 1=read+write, 2=admin). Default is read-only.
        name: Optional name for the share link

    Returns:
        Share info including hash for URL construction
    """
    data = {"right": right}
    if name:
        data["name"] = name

    response = _request("PUT", f"/api/v1/projects/{project_id}/shares", json=data)
    return {
        "id": response.get("id"),
        "hash": response.get("hash"),
        "project_id": project_id,
        "right": right,
        "name": name or response.get("name", ""),
        "url": f"https://vikunja.factumerit.app/share/{response.get('hash')}/auth"
    }


# @PRIVATE
def _get_link_shares_impl(project_id: int) -> list[dict]:
    """Get existing link shares for a project."""
    response = _request("GET", f"/api/v1/projects/{project_id}/shares")
    return [
        {
            "id": s.get("id"),
            "hash": s.get("hash"),
            "right": s.get("right"),
            "name": s.get("name", ""),
            "url": f"https://vikunja.factumerit.app/share/{s.get('hash')}/auth"
        }
        for s in response
    ]


# @PUBLIC_HELPER
def _update_project_impl(project_id: int, title: str = "", description: str = "", hex_color: str = "", parent_project_id: int = -1, position: float = -1) -> dict:
    """Update a project's properties. Use parent_project_id=0 to move to root."""
    # GET current project state (Vikunja API replaces, so we merge)
    current = _request("GET", f"/api/v1/projects/{project_id}")

    # Only update fields that were explicitly provided
    # Security: Sanitize title (strip HTML)
    if title:
        current["title"] = _sanitize_title(title)
    if description:
        current["description"] = description
    if hex_color:
        current["hex_color"] = hex_color
    if parent_project_id >= 0:  # -1 means don't change, 0 means root, >0 means reparent
        current["parent_project_id"] = parent_project_id
    if position >= 0:  # -1 means don't change
        current["position"] = position

    response = _request("POST", f"/api/v1/projects/{project_id}", json=current)
    return _format_project(response)


# @PUBLIC_HELPER
def _export_all_projects_impl() -> dict:
    """Export all projects and their tasks for backup.

    Includes full view/bucket structure and task→bucket assignments
    for proper import with kanban board preservation.
    """
    projects = _request("GET", "/api/v1/projects")

    # Also export all labels (needed for import)
    try:
        labels = _request("GET", "/api/v1/labels")
        formatted_labels = [_format_label(l) for l in labels]
    except Exception:
        formatted_labels = []

    export = {
        "exported_at": datetime.now().isoformat(),
        "vikunja_version": "unknown",
        "project_count": len(projects),
        "label_count": len(formatted_labels),
        "labels": formatted_labels,
        "projects": [],
        "task_count": 0,
        "view_count": 0,
        "bucket_count": 0,
    }

    task_count = 0
    view_count = 0
    bucket_count = 0

    for project in projects:
        project_data = _format_project(project)
        pid = project["id"]

        # Get all tasks including completed
        try:
            tasks = _request("GET", f"/api/v1/projects/{pid}/tasks")
            project_data["tasks"] = [_format_task(t) for t in tasks]
            task_count += len(project_data["tasks"])
        except Exception:
            project_data["tasks"] = []
            project_data["task_error"] = "Failed to fetch tasks"

        # Get views with buckets and task→bucket assignments
        project_data["views"] = []
        project_data["task_bucket_assignments"] = {}  # task_id -> {view_id, bucket_id}

        try:
            views = _request("GET", f"/api/v1/projects/{pid}/views")
            for view in views:
                view_data = _format_view(view)
                view_count += 1

                # For kanban views, get buckets and task assignments
                if view.get("view_kind") == "kanban":
                    view_id = view["id"]
                    try:
                        buckets = _request("GET", f"/api/v1/projects/{pid}/views/{view_id}/buckets")
                        view_data["buckets"] = [_format_bucket(b) for b in buckets]
                        bucket_count += len(buckets)

                        # Get tasks via view endpoint to get bucket assignments
                        # Note: Kanban view returns buckets with nested tasks array
                        try:
                            view_response = _request("GET", f"/api/v1/projects/{pid}/views/{view_id}/tasks")
                            for bucket_item in view_response:
                                bucket_id = bucket_item.get("id")
                                tasks_in_bucket = bucket_item.get("tasks") or []
                                for vt in tasks_in_bucket:
                                    tid = vt.get("id")
                                    if tid and bucket_id:
                                        project_data["task_bucket_assignments"][str(tid)] = {
                                            "view_id": view_id,
                                            "bucket_id": bucket_id,
                                            "position": vt.get("position", 0),
                                        }
                        except Exception:
                            pass  # View tasks fetch failed, continue
                    except Exception:
                        view_data["buckets"] = []

                project_data["views"].append(view_data)
        except Exception:
            project_data["views"] = []
            project_data["view_error"] = "Failed to fetch views"

        export["projects"].append(project_data)

    export["task_count"] = task_count
    export["view_count"] = view_count
    export["bucket_count"] = bucket_count
    return export


# @PUBLIC_HELPER
def _import_from_export_impl(export_data: dict, skip_existing: bool = True) -> dict:
    """Import projects from an export file, preserving bucket assignments.

    Args:
        export_data: Export dict from export_all_projects
        skip_existing: If True, skip projects that already exist (by title)

    Returns:
        Import summary with counts and ID mappings
    """
    result = {
        "success": False,
        "labels_created": 0,
        "projects_created": 0,
        "tasks_created": 0,
        "bucket_assignments": 0,
        "skipped_projects": [],
        "errors": [],
        "label_id_map": {},  # old_id -> new_id
        "project_id_map": {},  # old_id -> new_id
        "task_id_map": {},  # old_id -> new_id
        "bucket_id_map": {},  # old_id -> new_id
        "view_id_map": {},  # old_id -> new_id
    }

    # Get existing projects to check for duplicates
    existing_projects = {}
    if skip_existing:
        try:
            projects = _request("GET", "/api/v1/projects")
            existing_projects = {p["title"]: p["id"] for p in projects}
        except Exception as e:
            result["errors"].append(f"Failed to fetch existing projects: {e}")

    # Get existing labels
    existing_labels = {}
    try:
        labels = _request("GET", "/api/v1/labels")
        existing_labels = {l["title"]: l["id"] for l in labels}
    except Exception:
        pass

    # Step 1: Create labels (or map to existing)
    for label in export_data.get("labels", []):
        old_id = label["id"]
        title = label["title"]

        if title in existing_labels:
            result["label_id_map"][old_id] = existing_labels[title]
        else:
            try:
                new_label = _request("POST", "/api/v1/labels", json={
                    "title": title,
                    "hex_color": label.get("hex_color", ""),
                })
                result["label_id_map"][old_id] = new_label["id"]
                result["labels_created"] += 1
            except Exception as e:
                result["errors"].append(f"Failed to create label '{title}': {e}")

    # Step 2: Create projects (two passes: first root, then children)
    projects = export_data.get("projects", [])

    # First pass: root projects (parent_project_id = 0)
    for proj in projects:
        if proj.get("parent_project_id", 0) != 0:
            continue

        title = proj["title"]
        old_id = proj["id"]

        if title in existing_projects:
            result["project_id_map"][old_id] = existing_projects[title]
            result["skipped_projects"].append(title)
            continue

        try:
            new_proj = _request("POST", "/api/v1/projects", json={
                "title": title,
                "description": proj.get("description", ""),
                "hex_color": proj.get("hex_color", ""),
            })
            result["project_id_map"][old_id] = new_proj["id"]
            result["projects_created"] += 1
            existing_projects[title] = new_proj["id"]
        except Exception as e:
            result["errors"].append(f"Failed to create project '{title}': {e}")

    # Second pass: child projects
    for proj in projects:
        old_parent = proj.get("parent_project_id", 0)
        if old_parent == 0:
            continue

        title = proj["title"]
        old_id = proj["id"]

        if title in existing_projects:
            result["project_id_map"][old_id] = existing_projects[title]
            result["skipped_projects"].append(title)
            continue

        new_parent = result["project_id_map"].get(old_parent, 0)
        try:
            new_proj = _request("POST", "/api/v1/projects", json={
                "title": title,
                "description": proj.get("description", ""),
                "hex_color": proj.get("hex_color", ""),
                "parent_project_id": new_parent,
            })
            result["project_id_map"][old_id] = new_proj["id"]
            result["projects_created"] += 1
        except Exception as e:
            result["errors"].append(f"Failed to create child project '{title}': {e}")

    # Step 3: For each project, create views/buckets and tasks
    for proj in projects:
        old_pid = proj["id"]
        new_pid = result["project_id_map"].get(old_pid)
        if not new_pid:
            continue

        # Skip if this was an existing project (don't modify)
        if proj["title"] in result["skipped_projects"]:
            continue

        # Get the default kanban view that was auto-created
        default_kanban_view_id = None
        try:
            views = _request("GET", f"/api/v1/projects/{new_pid}/views")
            for v in views:
                if v.get("view_kind") == "kanban":
                    default_kanban_view_id = v["id"]
                    break
        except Exception:
            pass

        # Create buckets in the kanban view
        for view in proj.get("views", []):
            if view.get("view_kind") != "kanban":
                continue

            old_view_id = view["id"]
            new_view_id = default_kanban_view_id  # Use default kanban view

            if new_view_id:
                result["view_id_map"][old_view_id] = new_view_id

                # Delete default auto-created buckets first
                try:
                    existing_buckets = _request("GET", f"/api/v1/projects/{new_pid}/views/{new_view_id}/buckets")
                    for eb in existing_buckets:
                        try:
                            _request("DELETE", f"/api/v1/projects/{new_pid}/views/{new_view_id}/buckets/{eb['id']}")
                        except Exception:
                            pass
                except Exception:
                    pass

                # Create buckets from export
                for bucket in view.get("buckets", []):
                    old_bucket_id = bucket["id"]
                    try:
                        new_bucket = _request("PUT", f"/api/v1/projects/{new_pid}/views/{new_view_id}/buckets", json={
                            "title": bucket["title"],
                            "position": bucket.get("position", 0),
                            "limit": bucket.get("limit", 0),
                        })
                        result["bucket_id_map"][old_bucket_id] = new_bucket["id"]
                    except Exception as e:
                        result["errors"].append(f"Failed to create bucket '{bucket['title']}': {e}")

        # Create tasks
        for task in proj.get("tasks", []):
            old_tid = task["id"]
            try:
                # Map label IDs
                new_labels = []
                for label in task.get("labels", []):
                    new_label_id = result["label_id_map"].get(label["id"])
                    if new_label_id:
                        new_labels.append(new_label_id)

                new_task = _request("PUT", f"/api/v1/projects/{new_pid}/tasks", json={
                    "title": task["title"],
                    "description": task.get("description", ""),
                    "done": task.get("done", False),
                    "priority": task.get("priority", 0),
                    "due_date": task.get("due_date"),
                    "start_date": task.get("start_date"),
                    "end_date": task.get("end_date"),
                    "repeat_after": task.get("repeat_after", 0),
                    "repeat_mode": task.get("repeat_mode", 0),
                })
                new_tid = new_task["id"]
                result["task_id_map"][old_tid] = new_tid
                result["tasks_created"] += 1

                # Add labels to task
                for label_id in new_labels:
                    try:
                        _request("PUT", f"/api/v1/tasks/{new_tid}/labels", json={"label_id": label_id})
                    except Exception:
                        pass

            except Exception as e:
                result["errors"].append(f"Failed to create task '{task['title']}': {e}")

        # Assign tasks to buckets using position API
        assignments = proj.get("task_bucket_assignments", {})
        for old_tid_str, assignment in assignments.items():
            old_tid = int(old_tid_str)
            new_tid = result["task_id_map"].get(old_tid)
            if not new_tid:
                continue

            old_view_id = assignment.get("view_id")
            old_bucket_id = assignment.get("bucket_id")
            position = assignment.get("position", 0)

            new_view_id = result["view_id_map"].get(old_view_id)
            new_bucket_id = result["bucket_id_map"].get(old_bucket_id)

            if new_view_id and new_bucket_id:
                try:
                    _request("POST", f"/api/v1/tasks/{new_tid}/position", json={
                        "project_view_id": new_view_id,
                        "bucket_id": new_bucket_id,
                        "position": position,
                    })
                    result["bucket_assignments"] += 1
                except Exception as e:
                    result["errors"].append(f"Failed to assign task {new_tid} to bucket: {e}")

    result["success"] = len(result["errors"]) == 0
    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def import_from_export(
    export_json: str = Field(description="JSON string of export data (from export_all_projects)"),
    skip_existing: bool = Field(default=True, description="Skip projects that already exist by title"),
) -> dict:
    """
    Import projects from an export file, preserving bucket assignments.

    Use this to restore from a backup or migrate between instances.
    The export_json should be the JSON output from export_all_projects.

    Returns import summary with counts of created items and any errors.
    """
    import json
    try:
        export_data = json.loads(export_json)
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON: {e}"}

    return _import_from_export_impl(export_data, skip_existing)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_projects() -> list[dict]:
    """
    List all Vikunja projects.

    Returns projects with IDs, titles, descriptions, and parent relationships.
    Use project IDs when creating tasks or listing tasks.
    """
    return _list_projects_impl()


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_project(
    project_id: int = Field(description="ID of the project to retrieve")
) -> dict:
    """
    Get details of a specific project.

    Returns project ID, title, description, color, and parent project ID.
    """
    return _get_project_impl(project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_project(
    title: str = Field(description="Title of the new project"),
    description: str = Field(default="", description="Optional project description"),
    hex_color: str = Field(default="", description="Color in hex format (e.g., '#3498db')"),
    parent_project_id: int = Field(default=0, description="Parent project ID for nesting (0 = top-level)")
) -> dict:
    """
    Queue a new Vikunja project for creation.

    IMPORTANT: When called from Vikunja bot (@eis), projects are NOT created instantly.
    Instead, they are queued for the user to create. The user will receive a link to
    complete the creation process using their active Vikunja session.

    Returns a queued project spec with status "queued_for_creation".
    The user must click the provided link to finalize creation.

    Use parent_project_id to create nested/child projects.
    Multiple projects created in one turn are batched together.
    """
    return _create_project_impl(title, description, hex_color, parent_project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def delete_project(
    project_id: int = Field(description="ID of the project to delete")
) -> dict:
    """
    Delete a project and all its tasks.

    WARNING: This permanently deletes the project and all contained tasks.
    Returns confirmation of deletion.
    """
    return _delete_project_impl(project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def update_project(
    project_id: int = Field(description="ID of the project to update"),
    title: str = Field(default="", description="New title (empty = keep current)"),
    description: str = Field(default="", description="New description (empty = keep current)"),
    hex_color: str = Field(default="", description="New color in hex format (empty = keep current)"),
    parent_project_id: int = Field(default=-1, description="New parent project ID (-1 = keep current, 0 = move to root, >0 = reparent under that project)"),
    position: float = Field(default=-1, description="Position for ordering (-1 = keep current, lower = earlier in list)")
) -> dict:
    """
    Update a project's properties including its parent (reparenting) and position.

    Use parent_project_id to move projects in the hierarchy:
    - -1: Don't change parent (default)
    - 0: Move to root level (top-level project)
    - >0: Move under the specified parent project

    Use position to reorder projects within their parent:
    - -1: Don't change position (default)
    - Lower values appear first in the list
    - Use list_projects to see current positions

    WARNING: Reparenting has known bugs in Vikunja. Back up first with export_all_projects.
    """
    return _update_project_impl(project_id, title, description, hex_color, parent_project_id, position)


# @PRIVATE
@mcp.tool()
@mcp_tool_with_fallback
def create_link_share(
    project_id: int = Field(description="ID of the project to create share link for"),
    right: int = Field(default=0, description="Permission level: 0=read-only, 1=read+write, 2=admin"),
    name: str = Field(default="", description="Optional name for the share link")
) -> dict:
    """
    Create a public link share for a project.

    Returns the share hash for URL construction.
    URL format: https://vikunja.factumerit.app/share/{hash}/auth
    """
    return _create_link_share_impl(project_id, right, name)


# @PRIVATE
@mcp.tool()
@mcp_tool_with_fallback
def get_link_shares(
    project_id: int = Field(description="ID of the project to get shares for")
) -> dict:
    """
    Get existing link shares for a project.

    Returns list of shares with their hashes and permissions.
    """
    return {"shares": _get_link_shares_impl(project_id)}


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def export_all_projects() -> dict:
    """
    Export all projects and tasks for backup.

    Returns a complete snapshot of all projects with their tasks.
    Use before major restructuring operations.

    Returns: {exported_at, project_count, task_count, projects: [{id, title, ..., tasks: [...]}]}
    """
    return _export_all_projects_impl()


# ============================================================================
# TASK OPERATIONS
# ============================================================================

# @PUBLIC_HELPER
def _list_tasks_impl(project_id: int, include_completed: bool = False, label_filter: str = "") -> list[dict]:
    # Fetch all pages for the project
    response = _fetch_all_pages("GET", f"/api/v1/projects/{project_id}/tasks", per_page=50, max_pages=100)
    tasks = [_format_task(t) for t in response]
    if not include_completed:
        tasks = [t for t in tasks if not t["done"]]
    if label_filter:
        # Filter by label name (case-insensitive partial match)
        label_lower = label_filter.lower()
        tasks = [t for t in tasks if any(label_lower in l["title"].lower() for l in t["labels"])]
    return tasks


# @PUBLIC_HELPER
def _get_task_impl(task_id: int) -> dict:
    response = _request("GET", f"/api/v1/tasks/{task_id}")
    return _format_task(response)


# @PUBLIC_HELPER
def _convert_local_to_utc(date_str: str) -> str:
    """Convert a datetime string from local timezone to UTC.

    If the datetime has no timezone (e.g., '2025-01-06T18:00:00'), treats it
    as the user's local timezone (from instance config) and converts to UTC.

    If already has timezone (ends with Z or has offset), returns as-is.
    Date-only strings (no time) are returned as-is.

    Returns: UTC datetime string (with Z suffix if converted)
    """
    if not date_str:
        return date_str

    # Date-only strings don't need timezone conversion
    if "T" not in date_str:
        return date_str

    # Already has timezone info - return as-is
    if date_str.endswith("Z") or "+" in date_str or date_str.count("-") > 2:
        # Count dashes: 2025-01-06T18:00:00 has 2, 2025-01-06T18:00:00-08:00 has 3
        if "+" in date_str[10:] or date_str[10:].count("-") > 0:
            return date_str
        if date_str.endswith("Z"):
            return date_str

    # No timezone - assume local timezone from config
    local_tz_name = _get_instance_timezone()
    if not local_tz_name:
        # No timezone configured - assume UTC (backward compatible)
        return date_str if date_str.endswith("Z") else date_str + "Z"

    try:
        import pytz
        local_tz = pytz.timezone(local_tz_name)

        # Parse naive datetime
        naive_dt = datetime.fromisoformat(date_str)

        # Localize to user's timezone, then convert to UTC
        local_dt = local_tz.localize(naive_dt)
        utc_dt = local_dt.astimezone(pytz.UTC)

        return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        # Fallback: return as-is with Z suffix
        return date_str if date_str.endswith("Z") else date_str + "Z"


# @PUBLIC_HELPER
def _validate_and_fix_date(date_str: str, field_name: str = "due_date") -> tuple[str, str | None]:
    """Validate date, convert timezone if needed, and auto-correct if in past near year boundary.

    Returns: (corrected_date, warning_message) or (original_date, None)

    Processing steps:
    1. Convert from local timezone to UTC (if datetime has no timezone suffix)
    2. Auto-correct Jan/Feb dates to next year if created in Dec (year boundary fix)
    3. Warn if date is more than 1 day in past
    """
    if not date_str:
        return date_str, None

    # Step 1: Convert local timezone to UTC
    date_str = _convert_local_to_utc(date_str)

    try:
        # Parse the date (handle various ISO formats)
        if "T" in date_str:
            # Full datetime: 2025-01-06T10:00:00Z
            parsed = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            # Date only: 2025-01-06
            parsed = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        # Check if date is in the past
        if parsed < now:
            days_in_past = (now - parsed).days

            # Near year boundary (Jan/Feb date created in Dec): auto-correct
            if parsed.month <= 2 and now.month >= 11 and days_in_past < 365:
                # Likely meant next year
                corrected = parsed.replace(year=parsed.year + 1)
                corrected_str = corrected.strftime("%Y-%m-%dT%H:%M:%SZ") if "T" in date_str else corrected.strftime("%Y-%m-%d")
                warning = f"⚠️ Auto-corrected {field_name} from {date_str[:10]} to {corrected_str[:10]} (assumed next year)"
                return corrected_str, warning

            # Date is in past but not near year boundary - warn only
            if days_in_past > 1:  # More than 1 day in past
                warning = f"⚠️ Warning: {field_name} {date_str[:10]} is {days_in_past} days in the past"
                return date_str, warning

        return date_str, None

    except (ValueError, TypeError):
        # Can't parse date, pass through
        return date_str, None


# @PUBLIC_HELPER
def _create_task_impl(project_id: int, title: str, description: str = "", start_date: str = "", end_date: str = "", due_date: str = "", priority: int = 0, repeat_after: int = 0, repeat_mode: int = 0) -> dict:
    # Guard against queued project IDs (negative temp_id from project queue)
    _reject_queued_project_id(project_id, "create_task")

    # Security: Sanitize title (strip HTML) and description (escape HTML before markdown)
    sanitized_title = _sanitize_title(title)
    data = {"title": sanitized_title}
    warnings = []

    # === DEDUPLICATION CHECK (fa-991k) ===
    # Check for recently created tasks with same title in this project
    # This prevents duplicate task creation from LLM retries/parallel calls
    try:
        from datetime import datetime, timedelta, timezone
        recent_tasks = _request("GET", f"/api/v1/projects/{project_id}/tasks")
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=60)  # Tasks created in last 60 seconds

        for task in recent_tasks:
            # Check title match (case-insensitive)
            if task.get("title", "").lower() == sanitized_title.lower():
                # Check if created recently
                created_str = task.get("created")
                if created_str:
                    try:
                        # Parse ISO format: 2025-01-07T22:30:00Z
                        created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                        if created > cutoff:
                            logger.warning(f"[create_task] DEDUP: Task '{sanitized_title}' already exists (id={task.get('id')}, created {created_str})")
                            return {
                                "id": task.get("id"),
                                "title": task.get("title"),
                                "status": "already_exists",
                                "message": f"A task named '{sanitized_title}' was already created in this project within the last 60 seconds. "
                                           f"Returning existing task instead of creating duplicate.",
                                "_dedup": True
                            }
                    except (ValueError, TypeError):
                        pass  # Can't parse date, skip this task
    except Exception as e:
        # Log but don't fail - dedup is best-effort
        logger.warning(f"[create_task] Dedup check failed (continuing): {e}")

    if description:
        # If already HTML, pass through; otherwise sanitize and convert markdown
        if _is_html(description):
            data["description"] = description
        else:
            data["description"] = md_to_html(_sanitize_description(description))
    if start_date:
        start_date, warn = _validate_and_fix_date(start_date, "start_date")
        data["start_date"] = start_date
        if warn:
            warnings.append(warn)
    if end_date:
        end_date, warn = _validate_and_fix_date(end_date, "end_date")
        data["end_date"] = end_date
        if warn:
            warnings.append(warn)
    if due_date:
        due_date, warn = _validate_and_fix_date(due_date, "due_date")
        data["due_date"] = due_date
        if warn:
            warnings.append(warn)
    if priority:
        data["priority"] = priority
    if repeat_after > 0:
        data["repeat_after"] = repeat_after
        data["repeat_mode"] = repeat_mode

    response = _request("PUT", f"/api/v1/projects/{project_id}/tasks", json=data)
    # Invalidate caches since task list changed
    _invalidate_ics_cache(_get_current_instance())
    _invalidate_task_list_cache()

    result = _format_task(response)
    if warnings:
        result["_warnings"] = warnings
    return result


# @PUBLIC_HELPER
def _update_task_impl(task_id: int, title: str = "", description: str = "", start_date: str = "", end_date: str = "", due_date: str = "", priority: int = -1, repeat_after: int = -1, repeat_mode: int = -1) -> dict:
    # Vikunja API replaces the task, so we must GET first and merge changes
    current = _request("GET", f"/api/v1/tasks/{task_id}")
    warnings = []

    # Only update fields that were explicitly provided
    # Security: Sanitize title (strip HTML) and description (escape HTML before markdown)
    if title:
        current["title"] = _sanitize_title(title)
    if description:
        # If already HTML, pass through; otherwise sanitize and convert markdown
        if _is_html(description):
            current["description"] = description
        else:
            current["description"] = md_to_html(_sanitize_description(description))
    if start_date:
        start_date, warn = _validate_and_fix_date(start_date, "start_date")
        current["start_date"] = start_date
        if warn:
            warnings.append(warn)
    if end_date:
        end_date, warn = _validate_and_fix_date(end_date, "end_date")
        current["end_date"] = end_date
        if warn:
            warnings.append(warn)
    if due_date:
        due_date, warn = _validate_and_fix_date(due_date, "due_date")
        current["due_date"] = due_date
        if warn:
            warnings.append(warn)
    if priority >= 0:
        current["priority"] = priority
    if repeat_after >= 0:
        current["repeat_after"] = repeat_after
    if repeat_mode >= 0:
        current["repeat_mode"] = repeat_mode

    response = _request("POST", f"/api/v1/tasks/{task_id}", json=current)
    # Invalidate caches since task may affect calendar
    _invalidate_ics_cache(_get_current_instance())
    _invalidate_task_list_cache()

    result = _format_task(response)
    if warnings:
        result["_warnings"] = warnings
    return result


# @PUBLIC_HELPER
def _complete_task_impl(task_id: int) -> dict:
    # GET first to preserve other fields
    current = _request("GET", f"/api/v1/tasks/{task_id}")
    current["done"] = True
    response = _request("POST", f"/api/v1/tasks/{task_id}", json=current)
    # Invalidate caches since task status changed
    _invalidate_ics_cache(_get_current_instance())
    _invalidate_task_list_cache()
    return _format_task(response)


# @PUBLIC_HELPER
def _delete_task_impl(task_id: int) -> dict:
    _request("DELETE", f"/api/v1/tasks/{task_id}")
    # Invalidate caches since task removed
    _invalidate_ics_cache(_get_current_instance())
    _invalidate_task_list_cache()
    return {"deleted": True, "task_id": task_id}


# @PUBLIC_HELPER
def _batch_delete_tasks_impl(task_ids: list[int]) -> dict:
    """Delete multiple tasks at once.

    Args:
        task_ids: List of task IDs to delete

    Returns:
        Summary of deleted and failed tasks
    """
    deleted = []
    failed = []
    for task_id in task_ids:
        try:
            _request("DELETE", f"/api/v1/tasks/{task_id}")
            deleted.append(task_id)
        except Exception as e:
            failed.append({"task_id": task_id, "error": str(e)})

    # Invalidate caches once at the end
    if deleted:
        _invalidate_ics_cache(_get_current_instance())
        _invalidate_task_list_cache()

    return {
        "deleted_count": len(deleted),
        "deleted_ids": deleted,
        "failed_count": len(failed),
        "failed": failed if failed else None
    }


# @PUBLIC_HELPER
def _set_task_position_impl(
    task_id: int,
    project_id: int,
    view_id: int,
    bucket_id: int,
    apply_sort: bool = False
) -> dict:
    """
    Move a task to a kanban bucket.

    If apply_sort=True, calculates the correct position based on the bucket's
    sort strategy from project config (instead of just appending).
    """
    # Add task to bucket
    bucket_data = {
        "max_permission": None,
        "task_id": task_id,
        "bucket_id": bucket_id,
        "project_view_id": view_id,
        "project_id": project_id
    }
    _request("POST", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}/tasks", json=bucket_data)


    # CRITICAL: Always make the second API call to commit the bucket assignment (Call 2)
    # This matches the Python wrapper behavior and what the UI does
    # NOTE: bucket_id MUST be included or the assignment doesn't persist!
    position_data = {
        "max_permission": None,
        "project_view_id": view_id,
        "task_id": task_id,
        "bucket_id": bucket_id
    }
    _request("POST", f"/api/v1/tasks/{task_id}/position", json=position_data)
    result = {"task_id": task_id, "bucket_id": bucket_id, "view_id": view_id, "position_set": True}

    if not apply_sort:
        return result

    # Get project config for sort strategy
    config_result = _get_project_config_impl(project_id)
    project_config = config_result.get("config")
    if not project_config:
        return result

    sort_strategy = project_config.get("sort_strategy", {})
    default_strategy = sort_strategy.get("default", "manual")
    bucket_strategies = sort_strategy.get("buckets", {})

    # Get bucket name from bucket_id
    buckets = _list_buckets_impl(project_id, view_id)
    bucket_name = None
    for b in buckets:
        if b["id"] == bucket_id:
            bucket_name = b["title"]
            break

    if not bucket_name:
        return result

    # Get sort strategy for this bucket
    strategy = bucket_strategies.get(bucket_name, default_strategy)
    if strategy == "manual":
        return result

    # Fetch the task to get its sort key value
    task = _get_task_impl(task_id)

    # Fetch existing tasks in bucket with positions
    existing_raw = _get_bucket_tasks_raw(project_id, view_id, bucket_id)
    # Filter out the task we just moved (it's now in the bucket)
    existing_raw = [t for t in existing_raw if t["id"] != task_id]

    # Build sorted list of (sort_key, position) for existing tasks
    existing_sorted = []
    for t in existing_raw:
        key = _get_task_sort_key(t, strategy)
        pos = t.get("position", 0)
        existing_sorted.append((key, pos))
    existing_sorted.sort(key=lambda x: x[0])

    # Get sort key for the moved task
    new_key = _get_task_sort_key(task, strategy)

    # Extract just the sort keys for bisect
    existing_keys = [x[0] for x in existing_sorted]

    # Binary search to find insertion point
    insert_idx = bisect.bisect_left(existing_keys, new_key)

    # Calculate position between neighbors
    if not existing_sorted:
        new_pos = 1000.0
    elif insert_idx == 0:
        first_pos = existing_sorted[0][1]
        new_pos = first_pos / 2 if first_pos > 0 else -1000.0
    elif insert_idx >= len(existing_sorted):
        last_pos = existing_sorted[-1][1]
        new_pos = last_pos + 1000.0
    else:
        prev_pos = existing_sorted[insert_idx - 1][1]
        next_pos = existing_sorted[insert_idx][1]
        new_pos = (prev_pos + next_pos) / 2

    # Set the position
    _set_view_position_impl(task_id, view_id, new_pos)
    result["position_set"] = True
    result["position"] = new_pos

    return result


# @PUBLIC_HELPER
def _add_label_to_task_impl(task_id: int, label_id: int) -> dict:
    _request("PUT", f"/api/v1/tasks/{task_id}/labels", json={"label_id": label_id})
    # Invalidate caches since label may be "calendar"
    _invalidate_ics_cache(_get_current_instance())
    _invalidate_task_list_cache()
    return {"task_id": task_id, "label_id": label_id, "added": True}


# @PUBLIC_HELPER
def _assign_user_impl(task_id: int, user_id: int) -> dict:
    _request("PUT", f"/api/v1/tasks/{task_id}/assignees", json={"user_id": user_id})
    return {"task_id": task_id, "user_id": user_id, "assigned": True}


# @PUBLIC_HELPER
def _unassign_user_impl(task_id: int, user_id: int) -> dict:
    _request("DELETE", f"/api/v1/tasks/{task_id}/assignees/{user_id}")
    return {"task_id": task_id, "user_id": user_id, "unassigned": True}


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_tasks(
    project_id: int = Field(description="ID of the project to list tasks from"),
    include_completed: bool = Field(default=False, description="Whether to include completed tasks"),
    label_filter: str = Field(default="", description="Filter by label name (case-insensitive partial match, e.g., 'Sourdough' or '🍞')")
) -> list[dict]:
    """
    List tasks in a Vikunja project.

    Returns tasks with IDs, titles, descriptions, priorities, due dates, labels, and assignees.
    By default excludes completed tasks. Use include_completed=true to see all.
    Use label_filter to find tasks with specific labels (e.g., label_filter="Sourdough").
    """
    return _list_tasks_impl(project_id, include_completed, label_filter)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_task(
    task_id: int = Field(description="ID of the task to retrieve")
) -> dict:
    """
    Get details of a specific task.

    Returns full task details including labels, assignees, and bucket placement.
    """
    return _get_task_impl(task_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_task(
    project_id: int = Field(description="ID of the project to create the task in"),
    title: str = Field(description="Title of the task"),
    description: str = Field(default="", description="Optional task description"),
    start_date: str = Field(default="", description="Start date in ISO format - for GANTT chart"),
    end_date: str = Field(default="", description="End date in ISO format - for GANTT chart"),
    due_date: str = Field(default="", description="Due date in ISO format - for deadlines/Upcoming view"),
    priority: int = Field(default=0, description="Priority: 0=none, 1=low, 2=medium, 3=high, 4=urgent, 5=critical"),
    repeat_after: int = Field(default=0, description="Repeat interval in seconds (0=no repeat, 86400=daily, 604800=weekly)"),
    repeat_mode: int = Field(default=0, description="0=repeat from due date, 1=repeat from completion date")
) -> dict:
    """
    Create a new task in a Vikunja project.

    Date fields (ISO format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ):
    - start_date + end_date: Required for GANTT chart display
    - due_date: Used for deadlines and "Upcoming" view

    GANTT VISIBILITY: Vikunja Gantt shows DAILY resolution only. Tasks spanning
    hours within a single day appear as tiny bars. For visible Gantt bars, use
    full-day spans: start_date="YYYY-MM-DDT00:00:00Z", end_date="YYYY-MM-DDT23:59:00Z".
    Put actual times in task title if needed (e.g., "Bake pie (2pm-4pm)").
    Override this if precise time tracking is more important than Gantt visibility.

    Priority levels: 0=none, 1=low, 2=medium, 3=high, 4=urgent, 5=critical

    Recurring tasks: Set repeat_after to interval in seconds. Common values:
    - 86400 = daily, 604800 = weekly, 2592000 = ~monthly (30 days)
    repeat_mode: 0 = next due date calculated from original due date
                 1 = next due date calculated from completion date
    """
    return _create_task_impl(project_id, title, description, start_date, end_date, due_date, priority, repeat_after, repeat_mode)


# @PUBLIC_HELPER
def _find_or_create_label(name: str, hex_color: str = "#4caf50") -> int:
    """Find a label by name (case-insensitive) or create it if not found.

    Returns the label ID.
    """
    labels = _list_labels_impl()
    for label in labels:
        if label.get("title", "").lower() == name.lower():
            return label["id"]

    # Label not found, create it
    new_label = _create_label_impl(name, hex_color)
    return new_label["id"]


# @PUBLIC_HELPER
def _add_to_calendar_impl(
    project_id: int,
    title: str,
    due_date: str,
    description: str = "",
    start_date: str = "",
    end_date: str = "",
    label_name: str = "calendar"
) -> dict:
    """Create a task and add the calendar label to it."""
    # Create the task
    task = _create_task_impl(
        project_id=project_id,
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        due_date=due_date
    )

    # Find or create the calendar label
    label_id = _find_or_create_label(label_name)

    # Add label to task
    _add_label_to_task_impl(task["id"], label_id)

    task["calendar_label"] = label_name
    task["added_to_calendar"] = True
    return task


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def add_to_calendar(
    project_id: int = Field(description="ID of the project to create the task in"),
    title: str = Field(description="Title of the calendar event"),
    due_date: str = Field(description="Due date/time in ISO format (YYYY-MM-DDTHH:MM:SSZ)"),
    description: str = Field(default="", description="Optional event description"),
    start_date: str = Field(default="", description="Start date for GANTT (optional)"),
    end_date: str = Field(default="", description="End date for GANTT (optional)"),
    label_name: str = Field(default="calendar", description="Label name to add (default: 'calendar')")
) -> dict:
    """
    Add an event to the calendar by creating a task with the 'calendar' label.

    This creates a task and automatically adds the specified label (default: 'calendar').
    Tasks with this label appear in the ICS calendar feed.

    Use get_calendar_url to get the subscription URL for Google Calendar/Outlook.
    """
    return _add_to_calendar_impl(project_id, title, due_date, description, start_date, end_date, label_name)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def update_task(
    task_id: int = Field(description="ID of the task to update"),
    title: str = Field(default="", description="New title (empty = keep current)"),
    description: str = Field(default="", description="New description (empty = keep current)"),
    start_date: str = Field(default="", description="Start date in ISO format - for GANTT (empty = keep current)"),
    end_date: str = Field(default="", description="End date in ISO format - for GANTT (empty = keep current)"),
    due_date: str = Field(default="", description="Due date in ISO format - for deadlines (empty = keep current)"),
    priority: int = Field(default=-1, description="New priority (-1 = keep current, 0-5 to set)"),
    repeat_after: int = Field(default=-1, description="Repeat interval in seconds (-1=keep, 0=disable, 86400=daily)"),
    repeat_mode: int = Field(default=-1, description="0=from due date, 1=from completion (-1=keep)")
) -> dict:
    """
    Update an existing task.

    Only specified fields are updated. Use empty strings or -1 to keep current values.
    For GANTT chart: set start_date + end_date. For deadlines: set due_date.

    Recurring tasks: Set repeat_after to 0 to disable recurrence, or positive seconds for interval.
    """
    return _update_task_impl(task_id, title, description, start_date, end_date, due_date, priority, repeat_after, repeat_mode)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def complete_task(
    task_id: int = Field(description="ID of the task to mark as complete")
) -> dict:
    """
    Mark a task as complete (done=true).

    Returns the updated task.
    """
    return _complete_task_impl(task_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def delete_task(
    task_id: int = Field(description="ID of the task to delete")
) -> dict:
    """
    Delete a task permanently.

    Returns confirmation of deletion.
    """
    return _delete_task_impl(task_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def set_task_position(
    task_id: int = Field(description="ID of the task to move"),
    project_id: int = Field(description="ID of the project containing the task"),
    view_id: int = Field(description="ID of the kanban view (get from get_kanban_view)"),
    bucket_id: int = Field(description="ID of the target bucket (get from list_buckets)"),
    apply_sort: bool = Field(default=False, description="If true, calculate correct position based on bucket's sort strategy from project config")
) -> dict:
    """
    Move a task to a kanban bucket.

    First use get_kanban_view to get the view_id, then list_buckets to find bucket_id.

    If apply_sort=True, the task will be positioned according to the bucket's
    sort_strategy from project config (e.g., by start_date). Otherwise, it's
    appended to the bucket.
    """
    return _set_task_position_impl(task_id, project_id, view_id, bucket_id, apply_sort)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def add_label_to_task(
    task_id: int = Field(description="ID of the task"),
    label_id: int = Field(description="ID of the label to add (get from list_labels)")
) -> dict:
    """
    Add a label to a task.

    Use list_labels to find available label IDs.
    """
    return _add_label_to_task_impl(task_id, label_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def assign_user(
    task_id: int = Field(description="ID of the task"),
    user_id: int = Field(description="ID of the user to assign")
) -> dict:
    """
    Assign a user to a task.

    Returns confirmation of assignment.
    """
    return _assign_user_impl(task_id, user_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def unassign_user(
    task_id: int = Field(description="ID of the task"),
    user_id: int = Field(description="ID of the user to unassign")
) -> dict:
    """
    Remove a user from a task.

    Returns confirmation of removal.
    """
    return _unassign_user_impl(task_id, user_id)


# @PUBLIC_HELPER
def _format_reminder_input(reminder: str) -> dict:
    """Format a reminder datetime string into API format."""
    return {
        "reminder": reminder,
        "relative_period": 0,
        "relative_to": ""
    }


# @PUBLIC_HELPER
def _set_reminders_impl(task_id: int, reminders: list[str]) -> dict:
    """Set reminders on a task. Replaces all existing reminders."""
    # GET current task to preserve other fields
    current = _request("GET", f"/api/v1/tasks/{task_id}")
    # Convert datetime strings to reminder objects with required fields
    current["reminders"] = [_format_reminder_input(r) for r in reminders]
    response = _request("POST", f"/api/v1/tasks/{task_id}", json=current)
    return _format_task(response)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def set_reminders(
    task_id: int = Field(description="ID of the task"),
    reminders: list[str] = Field(description="List of reminder datetimes in ISO format (e.g., ['2025-12-20T10:00:00Z']). Pass empty list to clear all reminders.")
) -> dict:
    """
    Set reminders on a task.

    Replaces all existing reminders with the provided list.
    Each reminder is an ISO datetime when a notification will be sent.
    Pass an empty list to clear all reminders.

    Example: reminders=["2025-12-19T09:00:00Z", "2025-12-19T13:00:00Z"]
    """
    return _set_reminders_impl(task_id, reminders)


# ============================================================================
# LABEL OPERATIONS
# ============================================================================

# @PUBLIC_HELPER
def _list_labels_impl() -> list[dict]:
    # Fetch all pages for labels
    response = _fetch_all_pages("GET", "/api/v1/labels", per_page=50, max_pages=10)
    return [_format_label(l) for l in response]


# @PUBLIC_HELPER
def _create_label_impl(title: str, hex_color: str) -> dict:
    # Security: Sanitize title (strip HTML)
    data = {"title": _sanitize_title(title), "hex_color": hex_color}
    response = _request("PUT", "/api/v1/labels", json=data)
    return _format_label(response)


# @PUBLIC_HELPER
def _delete_label_impl(label_id: int) -> dict:
    _request("DELETE", f"/api/v1/labels/{label_id}")
    return {"deleted": True, "label_id": label_id}


# @PUBLIC_HELPER
def _analyze_project_dimensions_impl(project_id: int) -> dict:
    """Analyze a project's data to suggest meaningful kanban groupings.

    Returns available labels, priorities in use, assignees, and suggested
    kanban configurations based on the actual data.
    """
    # Validate project exists first
    try:
        project = _request("GET", f"/api/v1/projects/{project_id}")
        project_title = project.get("title", f"Project {project_id}")
    except ValueError as e:
        if "not found" in str(e).lower() or "does not exist" in str(e).lower():
            return {
                "error": f"Project {project_id} not found",
                "project_id": project_id,
                "suggestion": "Use list_projects to find valid project IDs"
            }
        raise

    # Get all tasks for this project
    tasks = _fetch_all_pages("GET", f"/api/v1/projects/{project_id}/tasks", per_page=50, max_pages=100)

    # Get all labels (global, but we'll filter to those used in project)
    all_labels = _fetch_all_pages("GET", "/api/v1/labels", per_page=50, max_pages=10)

    # Analyze dimensions
    labels_in_project = {}
    priorities_in_use = set()
    assignees = {}

    for task in tasks:
        # Track priorities
        priority = task.get("priority", 0)
        if priority > 0:
            priorities_in_use.add(priority)

        # Track labels used in this project
        for label in task.get("labels") or []:
            label_id = label.get("id")
            if label_id not in labels_in_project:
                labels_in_project[label_id] = {
                    "id": label_id,
                    "title": label.get("title", ""),
                    "hex_color": label.get("hex_color", ""),
                    "task_count": 0
                }
            labels_in_project[label_id]["task_count"] += 1

        # Track assignees
        for assignee in task.get("assignees") or []:
            user_id = assignee.get("id")
            username = assignee.get("username", assignee.get("name", f"user_{user_id}"))
            if user_id not in assignees:
                assignees[user_id] = {
                    "id": user_id,
                    "username": username,
                    "task_count": 0
                }
            assignees[user_id]["task_count"] += 1

    # Build suggestions
    suggestions = []

    # Suggest label-based kanban if multiple labels exist
    labels_list = sorted(labels_in_project.values(), key=lambda x: -x["task_count"])
    if len(labels_list) >= 2:
        top_labels = labels_list[:5]  # Top 5 by usage
        suggestions.append({
            "name": "By Label",
            "description": f"Group by labels: {', '.join(l['title'] for l in top_labels)}",
            "bucket_configuration_mode": "filter",
            "buckets": [
                {"title": l["title"], "filter": f"labels in {l['id']}", "task_count": l["task_count"]}
                for l in top_labels
            ]
        })

    # Suggest priority-based kanban if multiple priorities used
    if len(priorities_in_use) >= 2:
        priority_names = {5: "🔥 Urgent (P5)", 4: "High (P4)", 3: "Medium (P3)", 2: "Low (P2)", 1: "Minimal (P1)"}
        sorted_priorities = sorted(priorities_in_use, reverse=True)
        suggestions.append({
            "name": "By Priority",
            "description": f"Group by priority levels: {', '.join(str(p) for p in sorted_priorities)}",
            "bucket_configuration_mode": "filter",
            "buckets": [
                {"title": priority_names.get(p, f"Priority {p}"), "filter": f"priority = {p}"}
                for p in sorted_priorities
            ]
        })

    # Suggest assignee-based kanban if multiple assignees
    assignees_list = sorted(assignees.values(), key=lambda x: -x["task_count"])
    if len(assignees_list) >= 2:
        suggestions.append({
            "name": "By Assignee",
            "description": f"Group by who's responsible: {', '.join(a['username'] for a in assignees_list[:5])}",
            "bucket_configuration_mode": "filter",
            "buckets": [
                {"title": a["username"], "filter": f"assignees in {a['id']}", "task_count": a["task_count"]}
                for a in assignees_list[:5]
            ]
        })

    # Always suggest a status-based option
    suggestions.append({
        "name": "By Status",
        "description": "Traditional workflow: To Do → In Progress → Done",
        "bucket_configuration_mode": "manual",
        "buckets": [
            {"title": "To Do", "filter": None},
            {"title": "In Progress", "filter": None},
            {"title": "Done", "filter": None}
        ],
        "note": "Requires manually dragging tasks between buckets"
    })

    return {
        "project_id": project_id,
        "project_title": project_title,
        "task_count": len(tasks),
        "labels": labels_list,
        "priorities_in_use": sorted(priorities_in_use, reverse=True),
        "assignees": assignees_list,
        "suggested_kanbans": suggestions,
        "recommendation": suggestions[0]["name"] if suggestions else "By Status"
    }


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def analyze_project_dimensions(
    project_id: int = Field(description="Project ID to analyze")
) -> dict:
    """
    Analyze a project's data to discover meaningful grouping dimensions.

    CALL THIS BEFORE creating a kanban view to understand the data.

    Returns:
    - labels: Labels used in this project with task counts
    - priorities_in_use: Priority levels that have tasks
    - assignees: Team members with assigned tasks
    - suggested_kanbans: Ready-to-use kanban configurations based on actual data

    The suggested_kanbans include filter queries you can use directly with
    create_view and create_bucket to build meaningful views.
    """
    return _analyze_project_dimensions_impl(project_id)


# @PRIVATE
def _suggest_filters_impl(project_id: int = None) -> dict:
    """Generate ready-to-use filter queries for creating filtered views.

    Returns filter patterns organized by category with actual label IDs.
    """
    result = {
        "date_filters": [
            {"name": "Overdue", "query": "dueDate < now && done = false",
             "description": "Tasks past their due date"},
            {"name": "Due Today", "query": "dueDate >= now/d && dueDate < now/d+1d && done = false",
             "description": "Tasks due today"},
            {"name": "Due This Week", "query": "dueDate >= now/w && dueDate < now/w+1w && done = false",
             "description": "Tasks due this week"},
            {"name": "Upcoming 3 Days", "query": "dueDate >= now && dueDate < now+3d && done = false",
             "description": "Tasks due in next 3 days"},
            {"name": "No Due Date", "query": "dueDate = null && done = false",
             "description": "Tasks without a deadline"},
        ],
        "priority_filters": [
            {"name": "High Priority", "query": "priority >= 3 && done = false",
             "description": "Priority 3+ (high, urgent, critical)"},
            {"name": "Urgent", "query": "priority >= 4 && done = false",
             "description": "Priority 4+ (urgent, critical)"},
            {"name": "Critical Only", "query": "priority = 5 && done = false",
             "description": "Priority 5 (critical)"},
        ],
        "status_filters": [
            {"name": "Active", "query": "done = false",
             "description": "All incomplete tasks"},
            {"name": "Completed", "query": "done = true",
             "description": "All completed tasks"},
        ],
        "label_filters": [],
        "combined_filters": [
            {"name": "Needs Attention", "query": "(dueDate < now || priority >= 3) && done = false",
             "description": "Overdue OR high priority"},
            {"name": "Quick Wins This Week", "query": "dueDate < now+7d && priority <= 2 && done = false",
             "description": "Low-priority tasks due soon"},
        ],
    }

    # If project specified, add label-based filters with actual IDs
    if project_id:
        try:
            tasks = _fetch_all_pages("GET", f"/api/v1/projects/{project_id}/tasks", per_page=50, max_pages=20)

            # Collect labels used in this project
            labels_seen = {}
            for task in tasks:
                for label in task.get("labels") or []:
                    lid = label.get("id")
                    if lid and lid not in labels_seen:
                        labels_seen[lid] = {
                            "id": lid,
                            "title": label.get("title", ""),
                            "hex_color": label.get("hex_color", "")
                        }

            # Generate filter for each label
            for label in sorted(labels_seen.values(), key=lambda x: x["title"]):
                result["label_filters"].append({
                    "name": f"Label: {label['title']}",
                    "query": f"labels in {label['id']}",
                    "description": f"Tasks with '{label['title']}' label",
                    "label_id": label["id"]
                })

            result["project_id"] = project_id
        except Exception as e:
            result["label_filters_error"] = str(e)

    result["syntax_help"] = {
        "operators": ["=", "!=", "<", ">", "<=", ">=", "in", "like"],
        "combinators": ["&&", "||", "(", ")"],
        "date_math": ["now", "now/d (start of day)", "now/w (start of week)",
                      "now+1d", "now-7d", "now/w+1w"],
        "fields": ["done", "priority", "dueDate", "startDate", "endDate",
                   "labels", "assignees", "percentDone"],
        "docs": "https://vikunja.io/docs/filters/"
    }

    return result


# @PRIVATE
@mcp.tool()
@mcp_tool_with_fallback
def suggest_filters(
    project_id: int = Field(default=None, description="Optional project ID to include label-based filters with actual IDs")
) -> dict:
    """
    Get ready-to-use filter queries for creating filtered views.

    Returns filter patterns organized by category:
    - date_filters: Overdue, due today, this week, upcoming
    - priority_filters: High, urgent, critical
    - status_filters: Active, completed
    - label_filters: Labels used in the project (if project_id provided)
    - combined_filters: Complex patterns (overdue OR high priority)
    - syntax_help: Filter query syntax reference

    Example usage:
    1. Call suggest_filters(project_id=51) to see available filters
    2. Pick a filter query (e.g., "dueDate < now && done = false")
    3. Use with create_view or create_filtered_view

    Returns: {date_filters, priority_filters, label_filters, syntax_help, ...}
    """
    return _suggest_filters_impl(project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_labels() -> list[dict]:
    """
    List all available labels.

    Returns labels with IDs, titles, and colors.
    Use label IDs with add_label_to_task.
    """
    return _list_labels_impl()


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_label(
    title: str = Field(description="Label title"),
    hex_color: str = Field(description="Color in hex format (e.g., '#FF0000' for red)")
) -> dict:
    """
    Create a new label.

    Returns the created label with its assigned ID.
    """
    return _create_label_impl(title, hex_color)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def delete_label(
    label_id: int = Field(description="ID of the label to delete")
) -> dict:
    """
    Delete a label.

    Returns confirmation of deletion.
    """
    return _delete_label_impl(label_id)


# ============================================================================
# VIEW OPERATIONS
# ============================================================================

# @PUBLIC_HELPER
def _list_views_impl(project_id: int) -> list[dict]:
    """List all views for a project (list, kanban, gantt, table)."""
    response = _request("GET", f"/api/v1/projects/{project_id}/views")
    return [_format_view(v) for v in response]


# @PUBLIC_HELPER
def _get_view_tasks_impl(project_id: int, view_id: int) -> list[dict]:
    """Get tasks via a specific view endpoint - returns tasks with bucket info for kanban views."""
    response = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/tasks")
    # Kanban views return buckets with nested tasks
    # List/Gantt views return flat task arrays
    tasks = []
    for item in response:
        if "tasks" in item:
            # This is a bucket - extract tasks with bucket info
            bucket_id = item["id"]
            bucket_title = item["title"]
            for task in (item.get("tasks") or []):
                formatted = _format_task(task)
                formatted["bucket_id"] = bucket_id
                formatted["bucket_title"] = bucket_title
                tasks.append(formatted)
        else:
            # This is a task (non-kanban view)
            tasks.append(_format_task(item))
    return tasks


# @PUBLIC_HELPER
def _list_tasks_by_bucket_impl(project_id: int, view_id: int) -> dict:
    """Get tasks grouped by bucket for kanban views."""
    response = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/tasks")
    buckets = {}
    for item in response:
        if "tasks" in item:
            bucket_name = item["title"]
            buckets[bucket_name] = {
                "bucket_id": item["id"],
                "tasks": [_format_task(t) for t in (item.get("tasks") or [])]
            }
    return buckets


# @PUBLIC_HELPER
def _get_bucket_tasks_raw(project_id: int, view_id: int, bucket_id: int) -> list[dict]:
    """Get raw tasks in a specific bucket (includes position field)."""
    response = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/tasks")
    for item in response:
        if item.get("id") == bucket_id and "tasks" in item:
            return item.get("tasks") or []
    return []


# @PUBLIC_HELPER
def _get_single_sort_key(task: dict, strategy: str):
    """Extract a single sort key from a task dict."""
    if strategy == "start_date":
        return task.get("start_date") or "9999-12-31"
    elif strategy == "due_date":
        return task.get("due_date") or "9999-12-31"
    elif strategy == "end_date":
        return task.get("end_date") or "9999-12-31"
    elif strategy == "priority":
        return -(task.get("priority") or 0)  # Negative for descending (high priority first)
    elif strategy in ("alphabetical", "title"):
        return (task.get("title") or "").lower()
    elif strategy == "created":
        return task.get("id") or 0
    elif strategy == "position":
        return task.get("position") or 0
    return 0


# @PUBLIC_HELPER
def _get_task_sort_key(task: dict, strategy: str, then_by: str = None):
    """Extract sort key(s) from a task dict (API response format).

    Returns a tuple for stable multi-level sorting when then_by is provided.
    """
    primary = _get_single_sort_key(task, strategy)
    if then_by:
        secondary = _get_single_sort_key(task, then_by)
        return (primary, secondary)
    return primary


# @PUBLIC_HELPER
def _get_input_sort_key(task_input: dict, created_task: dict, strategy: str):
    """Extract sort key from task input (used during batch create)."""
    if strategy == "start_date":
        return task_input.get("start_date") or "9999-12-31"
    elif strategy == "due_date":
        return task_input.get("due_date") or "9999-12-31"
    elif strategy == "end_date":
        return task_input.get("end_date") or "9999-12-31"
    elif strategy == "priority":
        return -(task_input.get("priority") or 0)
    elif strategy == "alphabetical":
        return task_input.get("title", "").lower()
    elif strategy == "created":
        return created_task.get("id") or 0
    return 0


# @PUBLIC_HELPER
def _set_view_position_impl(task_id: int, view_id: int, position: float) -> dict:
    """Set a task's position within a specific view (for Gantt ordering, etc.)."""
    response = _request("POST", f"/api/v1/tasks/{task_id}/position", json={
        "project_view_id": view_id,
        "position": position
    })
    return response


# @PUBLIC_HELPER
def _get_kanban_view_impl(project_id: int) -> dict:
    response = _request("GET", f"/api/v1/projects/{project_id}/views")
    kanban_views = [v for v in response if v.get("view_kind") == "kanban"]
    if not kanban_views:
        raise ValueError(f"No kanban view found for project {project_id}")
    return _format_view(kanban_views[0])


# @PUBLIC_HELPER
def _list_buckets_impl(project_id: int, view_id: int) -> list[dict]:
    response = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
    return [_format_bucket(b) for b in response]


# @PUBLIC_HELPER
def _create_bucket_impl(project_id: int, view_id: int, title: str, position: int = 0, limit: int = 0) -> dict:
    data = {"title": title, "position": position, "limit": limit}
    response = _request("PUT", f"/api/v1/projects/{project_id}/views/{view_id}/buckets", json=data)
    return _format_bucket(response)


# @PUBLIC_HELPER
def _delete_bucket_impl(project_id: int, view_id: int, bucket_id: int) -> dict:
    _request("DELETE", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}")
    return {"deleted": True, "bucket_id": bucket_id}


# @PUBLIC_HELPER
def _create_view_impl(project_id: int, title: str, view_kind: str, filter_query: str = None, delete_default_buckets: bool = True) -> dict:
    """Create a new view for a project.

    Args:
        project_id: Project ID
        title: View title
        view_kind: View type (list, kanban, gantt, table)
        filter_query: Optional filter query string
        delete_default_buckets: For kanban views, delete the auto-created
            To-Do/Doing/Done buckets (default True). Set False to keep them.
    """
    # Guard against queued project IDs (negative temp_id from project queue)
    _reject_queued_project_id(project_id, "create_view")

    # Get existing views to determine position for new view (place at end)
    existing_views = _request("GET", f"/api/v1/projects/{project_id}/views")
    max_position = max([v.get("position", 0) for v in existing_views], default=0)

    data = {
        "title": title,
        "view_kind": view_kind,
        "position": max_position + 100  # Place at end with 100-unit spacing
    }

    # CRITICAL: For kanban views, set bucket_configuration_mode to "manual"
    # Without this, Vikunja defaults to "none" which groups by labels,
    # causing each task to appear as its own column instead of in buckets
    if view_kind == "kanban":
        data["bucket_configuration_mode"] = "manual"

    # Add filter if provided (Vikunja expects filter as a string, not an object)
    # Fix: solutions-nwidy / X-Q #250187
    if filter_query:
        data["filter"] = filter_query

    response = _request("PUT", f"/api/v1/projects/{project_id}/views", json=data)
    view_id = response.get("id")

    # For kanban views, Vikunja auto-creates default To-Do/Doing/Done buckets.
    # Delete them if delete_default_buckets is True (default) so user can create custom buckets.
    if view_kind == "kanban" and delete_default_buckets and view_id:
        try:
            buckets = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
            for bucket in buckets:
                bucket_id = bucket.get("id")
                if bucket_id:
                    try:
                        _request("DELETE", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}")
                    except Exception:
                        pass  # Ignore errors deleting individual buckets
        except Exception:
            pass  # Ignore errors listing/deleting buckets

    return _format_view(response)




# @PUBLIC_HELPER
def _delete_view_impl(project_id: int, view_id: int) -> dict:
    """
    Delete a view.
    
    Args:
        project_id: Project ID
        view_id: View ID to delete
    
    Returns:
        Success message
    """
    _request("DELETE", f"/api/v1/projects/{project_id}/views/{view_id}")
    
    return {
        "success": True,
        "message": f"Deleted view {view_id} from project {project_id}"
    }

# @PUBLIC_HELPER
def _update_view_impl(project_id: int, view_id: int, title: str = None, filter_query: str = None) -> dict:
    """Update a view's title and/or filter."""
    data = {}
    
    if title is not None:
        data["title"] = title
    
    # Vikunja expects filter as a string, not an object
    # Fix: solutions-nwidy / X-Q #250187
    if filter_query is not None:
        data["filter"] = filter_query
    
    response = _request("POST", f"/api/v1/projects/{project_id}/views/{view_id}", json=data)
    return _format_view(response)


# @PUBLIC_HELPER
def _setup_kanban_board_impl(
    project_id: int = None,
    project_title: str = None,
    template: str = "gtd",
    custom_buckets: list = None,
    view_title: str = "Kanban",
    delete_default_buckets: bool = True,
    migrate_tasks: dict = None
) -> dict:
    """
    Rapid kanban board setup with templates and task migration.

    This is the ONE tool agents should use for kanban board creation.
    Replaces 26+ API calls with a single tool call.

    Can optionally create the project too (project_title param).
    """
    # Guard against queued project IDs (negative temp_id from project queue)
    _reject_queued_project_id(project_id, "setup_kanban_board")

    project_created = False

    # 1. Create project if project_title provided (and no project_id)
    if project_title and not project_id:
        project_data = {"title": project_title}
        project = _request("PUT", "/api/v1/projects", json=project_data)
        project_id = project["id"]
        project_created = True

    if not project_id:
        raise ValueError("Either project_id or project_title is required")

    # 2. Get or create kanban view
    views = _request("GET", f"/api/v1/projects/{project_id}/views")
    kanban_views = [v for v in views if v.get("view_kind") == "kanban" and v.get("title") == view_title]

    # Track default views/buckets to clean up later
    default_kanban_view_id = None
    if project_created:
        # New projects have a default kanban view we'll want to delete
        default_kanbans = [v for v in views if v.get("view_kind") == "kanban" and v.get("title") != view_title]
        if default_kanbans:
            default_kanban_view_id = default_kanbans[0]["id"]

    if kanban_views:
        view = kanban_views[0]
    else:
        # Create new kanban view with CRITICAL bucket_configuration_mode
        max_position = max([v.get("position", 0) for v in views], default=0)
        view_data = {
            "title": view_title,
            "view_kind": "kanban",
            "bucket_configuration_mode": "manual",  # CRITICAL
            "position": max_position + 100
        }
        view = _request("PUT", f"/api/v1/projects/{project_id}/views", json=view_data)

    view_id = view["id"]

    # 3. Get bucket configuration
    if template == "custom":
        if not custom_buckets:
            raise ValueError("custom_buckets required when template='custom'")
        buckets_config = custom_buckets
    else:
        if template not in KANBAN_TEMPLATES:
            raise ValueError(f"Unknown template: {template}. Available: {list(KANBAN_TEMPLATES.keys())}")
        buckets_config = KANBAN_TEMPLATES[template]

    # 4. Create template buckets (idempotent - reuse existing by title)
    existing_buckets = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
    existing_bucket_map = {b["title"]: b for b in existing_buckets}

    created_buckets = []
    for config in buckets_config:
        bucket_title = config["title"]

        # Idempotency: reuse existing bucket with same title
        if bucket_title in existing_bucket_map:
            bucket = existing_bucket_map[bucket_title]
        else:
            bucket_data = {
                "title": bucket_title,
                "position": config.get("position", 0),
                "limit": config.get("limit", 0)
            }
            bucket = _request("PUT", f"/api/v1/projects/{project_id}/views/{view_id}/buckets", json=bucket_data)

        created_buckets.append({
            "id": bucket["id"],
            "title": bucket["title"],
            "position": bucket.get("position", 0),
            "limit": bucket.get("limit", 0)
        })

    # 5. NOW delete default buckets (after template buckets exist, so we're not deleting the last bucket)
    buckets_deleted = 0
    if delete_default_buckets:
        # Re-fetch to get any buckets created during step 4 (in case of race conditions)
        all_buckets = _request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
        created_bucket_ids = {b["id"] for b in created_buckets}
        for bucket in all_buckets:
            # Delete any bucket we didn't just create (i.e., the defaults like Backlog, Done, etc.)
            if bucket["id"] not in created_bucket_ids:
                try:
                    _request("DELETE", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket['id']}")
                    buckets_deleted += 1
                except Exception:
                    pass  # Ignore errors

    # 6. Delete default kanban view if we created a new project
    if default_kanban_view_id:
        try:
            _request("DELETE", f"/api/v1/projects/{project_id}/views/{default_kanban_view_id}")
        except Exception:
            pass  # Ignore errors

    # 7. Migrate tasks if requested
    tasks_migrated = 0
    migration_summary = {}

    if migrate_tasks:
        # Get all tasks in project
        tasks = _request("GET", f"/api/v1/projects/{project_id}/tasks")

        # Build label→bucket mapping (by title)
        bucket_map = {b["title"]: b["id"] for b in created_buckets}

        for task in tasks:
            task_labels = [label.get("title") for label in task.get("labels", [])]

            # Find matching label→bucket mapping
            for label_title, bucket_title in migrate_tasks.items():
                if label_title in task_labels and bucket_title in bucket_map:
                    bucket_id = bucket_map[bucket_title]

                    # Two-step bucket assignment (CRITICAL for Vikunja API)
                    try:
                        # Step 1: Add to bucket
                        _request("POST",
                                f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}/tasks",
                                json={"task_id": task["id"], "bucket_id": bucket_id,
                                     "project_view_id": view_id, "project_id": project_id})

                        # Step 2: Commit position (bucket_id required for persistence!)
                        _request("POST", f"/api/v1/tasks/{task['id']}/position",
                                json={"project_view_id": view_id, "task_id": task["id"], "bucket_id": bucket_id})

                        tasks_migrated += 1
                        migration_summary[bucket_title] = migration_summary.get(bucket_title, 0) + 1
                    except Exception:
                        # Continue on error
                        pass
                    break  # Only assign to first matching bucket

    result = {
        "view_id": view_id,
        "view_title": view_title,
        "buckets_created": len(created_buckets),
        "buckets": created_buckets,
        "tasks_migrated": tasks_migrated,
        "migration_summary": migration_summary
    }

    if project_created:
        result["project_id"] = project_id
        result["project_created"] = True

    return result


# @PUBLIC_HELPER
def _bulk_relabel_tasks_impl(
    project_id: int,
    task_ids: list[int],
    add_labels: list[str] = None,
    remove_labels: list[str] = None,
    set_labels: list[str] = None
) -> dict:
    """
    Bulk update labels on multiple tasks.
    
    Args:
        project_id: Project ID (for context, labels are global)
        task_ids: List of task IDs to update
        add_labels: Labels to add (by title, will be created if needed)
        remove_labels: Labels to remove (by title)
        set_labels: Replace all labels with this list (by title)
    
    Returns:
        dict with updated_count and details
    """
    if not task_ids:
        return {"updated_count": 0, "details": []}
    
    # Get all labels (labels are global in Vikunja)
    # Note: Labels API is paginated, need to fetch all pages
    all_labels = []
    page = 1
    while True:
        labels_page = _request("GET", f"/api/v1/labels?page={page}")
        if not labels_page:
            break
        all_labels.extend(labels_page)
        page += 1
        # Safety limit
        if page > 100:
            break
    
    label_map = {label["title"]: label["id"] for label in all_labels}
    
    # Create missing labels if needed
    all_label_titles = set()
    if add_labels:
        all_label_titles.update(add_labels)
    if set_labels:
        all_label_titles.update(set_labels)
    
    for title in all_label_titles:
        if title not in label_map:
            # Create label
            new_label = _request("PUT", "/api/v1/labels", json={"title": title, "hex_color": ""})
            label_map[title] = new_label["id"]
    
    # Update each task
    results = []
    for task_id in task_ids:
        try:
            # Get current task labels
            # Note: Vikunja returns null (None) for labels, not missing key, so use `or []`
            task = _request("GET", f"/api/v1/tasks/{task_id}")
            current_label_ids = {label["id"] for label in (task.get("labels") or [])}
            
            # Calculate label changes
            if set_labels is not None:
                # Replace all labels - remove all current, add all new
                labels_to_remove = current_label_ids
                labels_to_add = {label_map[title] for title in set_labels if title in label_map}
            else:
                # Incremental changes
                labels_to_remove = set()
                labels_to_add = set()
                
                if remove_labels:
                    labels_to_remove = {label_map[title] for title in remove_labels if title in label_map}
                
                if add_labels:
                    labels_to_add = {label_map[title] for title in add_labels if title in label_map}
                    # Don't add labels that are already on the task
                    labels_to_add = labels_to_add - current_label_ids
            
            # Apply changes using dedicated endpoints
            for label_id in labels_to_remove:
                if label_id in current_label_ids:
                    _request("DELETE", f"/api/v1/tasks/{task_id}/labels/{label_id}")
            
            for label_id in labels_to_add:
                _request("PUT", f"/api/v1/tasks/{task_id}/labels", json={"label_id": label_id})
            
            final_count = len(current_label_ids - labels_to_remove | labels_to_add)
            results.append({"task_id": task_id, "success": True, "label_count": final_count})
        except Exception as e:
            results.append({"task_id": task_id, "success": False, "error": str(e)})
    
    updated_count = sum(1 for r in results if r["success"])
    return {
        "updated_count": updated_count,
        "total_tasks": len(task_ids),
        "details": results
    }


# @PUBLIC_HELPER
def _bulk_set_task_positions_impl(
    project_id: int,
    view_id: int,
    assignments: list[dict]
) -> dict:
    """
    Bulk assign tasks to buckets in a kanban view.
    
    Args:
        project_id: Project ID
        view_id: View ID
        assignments: List of {task_id, bucket_id, position?} dicts
    
    Returns:
        dict with moved_count, tasks, and errors
    """
    if not assignments:
        return {"moved_count": 0, "tasks": [], "errors": []}
    
    results = []
    errors = []
    
    for assignment in assignments:
        task_id = assignment["task_id"]
        bucket_id = assignment["bucket_id"]
        position = assignment.get("position")
        
        try:
            # Use existing set_task_position implementation to assign bucket
            _set_task_position_impl(
                task_id=task_id,
                project_id=project_id,
                view_id=view_id,
                bucket_id=bucket_id,
                apply_sort=False
            )
            # If position provided, also set the position within the view/bucket
            if position is not None:
                _set_view_position_impl(task_id, view_id, position)
            results.append({"task_id": task_id, "bucket_id": bucket_id, "success": True})
        except Exception as e:
            errors.append({"task_id": task_id, "bucket_id": bucket_id, "error": str(e)})
    
    return {
        "moved_count": len(results),
        "total_assignments": len(assignments),
        "tasks": results,
        "errors": errors
    }


# @PUBLIC_HELPER
def _move_tasks_by_label_to_buckets_impl(
    project_id: int,
    view_id: int,
    label_to_bucket_map: dict[str, int]
) -> dict:
    """
    Move tasks to buckets based on label→bucket mappings.
    
    Args:
        project_id: Project ID
        view_id: View ID
        label_to_bucket_map: Dict mapping label titles to bucket IDs
            e.g., {"🎯 Phase 1: MVP": 39602, "🚀 Phase 2: Content": 39603}
    
    Returns:
        dict with moved_count, by_label breakdown, and errors
    """
    if not label_to_bucket_map:
        return {"moved_count": 0, "by_label": {}, "errors": []}
    
    # Get all labels for ID resolution (labels are global, paginated)
    all_labels = []
    page = 1
    while True:
        labels_page = _request("GET", f"/api/v1/labels?page={page}")
        if not labels_page:
            break
        all_labels.extend(labels_page)
        page += 1
        if page > 100:  # Safety limit
            break
    
    label_id_map = {label["title"]: label["id"] for label in all_labels}
    
    # Get all tasks in the project
    all_tasks = _request("GET", f"/api/v1/projects/{project_id}/tasks")
    
    # Build assignments
    assignments = []
    by_label = {label_title: 0 for label_title in label_to_bucket_map.keys()}
    
    for task in all_tasks:
        task_labels = {label["title"] for label in task.get("labels", [])}
        
        # Check if task has any of the target labels
        for label_title, bucket_id in label_to_bucket_map.items():
            if label_title in task_labels:
                assignments.append({
                    "task_id": task["id"],
                    "bucket_id": bucket_id
                })
                by_label[label_title] += 1
                break  # Only assign to first matching label
    
    # Bulk assign
    result = _bulk_set_task_positions_impl(project_id, view_id, assignments)
    result["by_label"] = by_label
    
    return result



# @PUBLIC_HELPER
def _bulk_create_labels_impl(
    labels: list[dict]
) -> dict:
    """
    Bulk create labels.
    
    Args:
        labels: List of {title: str, hex_color?: str} dicts
    
    Returns:
        dict with created_count, labels, and errors
    """
    if not labels:
        return {"created_count": 0, "labels": [], "errors": []}
    
    # Get existing labels to avoid duplicates (labels are global, paginated)
    existing_labels = []
    page = 1
    while True:
        labels_page = _request("GET", f"/api/v1/labels?page={page}")
        if not labels_page:
            break
        existing_labels.extend(labels_page)
        page += 1
        if page > 100:  # Safety limit
            break
    
    existing_titles = {label["title"] for label in existing_labels}
    
    results = []
    errors = []
    skipped = []
    
    for label_spec in labels:
        title = label_spec.get("title")
        hex_color = label_spec.get("hex_color", "")
        
        if not title:
            errors.append({"title": None, "error": "Title is required"})
            continue
        
        # Skip if already exists
        if title in existing_titles:
            skipped.append({"title": title, "reason": "Already exists"})
            continue
        
        try:
            new_label = _request("PUT", "/api/v1/labels", 
                                json={"title": title, "hex_color": hex_color})
            results.append({
                "id": new_label["id"],
                "title": new_label["title"],
                "hex_color": new_label["hex_color"],
                "success": True
            })
            existing_titles.add(title)  # Track for subsequent labels in same batch
        except Exception as e:
            errors.append({"title": title, "error": str(e)})
    
    return {
        "created_count": len(results),
        "total_requested": len(labels),
        "labels": results,
        "skipped": skipped,
        "errors": errors
    }



# @PUBLIC_HELPER
def _create_filtered_view_impl(
    project_id: int,
    title: str,
    view_kind: str,
    filter_query: str,
    bucket_config_mode: str = "manual"
) -> dict:
    """
    Create a filtered view using saved filter (shows only tasks matching criteria).
    
    Note: Vikunja doesn't support filters on regular views. Instead, this creates
    a "saved filter" which is actually a virtual project that shows filtered tasks.
    The saved filter automatically gets a default view of the specified kind.
    
    Args:
        project_id: Parent project ID (for context, saved filters are cross-project)
        title: Filter/view title
        view_kind: View type ("kanban", "list", "gantt", "table")
        filter_query: Filter query (e.g., 'labels in 7350' or 'priority >= 3')
        bucket_config_mode: "manual" for custom buckets, "none" for auto-grouping
    
    Returns:
        Created saved filter dict (acts as a project)
    """
    # Create saved filter (this creates a virtual project)
    filter_data = {
        "title": title,
        "filters": filter_query
    }
    
    saved_filter = _request("PUT", "/api/v1/filters", json=filter_data)
    
    # The saved filter is now a project - update its default view to the desired kind
    filter_project_id = saved_filter["id"]
    views = _request("GET", f"/api/v1/projects/{filter_project_id}/views")
    
    if views:
        # Update the first view to the desired kind and bucket mode
        default_view = views[0]
        _request("POST", f"/api/v1/projects/{filter_project_id}/views/{default_view['id']}", 
                json={
                    "view_kind": view_kind,
                    "bucket_configuration_mode": bucket_config_mode
                })
    
    return {
        "id": saved_filter["id"],
        "title": saved_filter["title"],
        "is_saved_filter": True,
        "filter": filter_query,
        "view_kind": view_kind
    }



# TODO: This function doesn't work - bucket filters aren't being applied by Vikunja API
# TDD test: /tmp/test_bucket_filtered_kanban.py shows filters aren't stored/applied
# See X-Q task #244154 for details
# Needs investigation: UI test to see correct API structure
# @PUBLIC_HELPER
def _create_bucket_filtered_kanban_impl(
    project_id: int,
    title: str,
    bucket_filters: dict[str, str]
) -> dict:
    """
    Create a kanban view with filter-based buckets (project-scoped).
    
    Each bucket shows only tasks matching its filter within the project.
    
    Args:
        project_id: Project ID
        title: View title
        bucket_filters: Dict mapping bucket titles to filter queries
            e.g., {"Quick Wins": "labels in 7344", "Deep Work": "labels in 7345"}
    
    Returns:
        Created view with buckets
    """
    # Get existing views to position at end
    existing_views = _request("GET", f"/api/v1/projects/{project_id}/views")
    max_position = max([v.get("position", 0) for v in existing_views], default=0)
    
    # Create view with filter-based bucket configuration
    view_data = {
        "title": title,
        "view_kind": "kanban",
        "position": max_position + 100,
        "bucket_configuration_mode": "filter"
    }
    
    new_view = _request("PUT", f"/api/v1/projects/{project_id}/views", json=view_data)
    view_id = new_view["id"]
    
    # Create buckets with filters
    buckets = []
    position = 100
    for bucket_title, filter_query in bucket_filters.items():
        bucket_data = {
            "title": bucket_title,
            "limit": 0,
            "position": position,
            "filter": filter_query
        }
        bucket = _request("PUT", f"/api/v1/projects/{project_id}/views/{view_id}/buckets", 
                         json=bucket_data)
        buckets.append({
            "id": bucket["id"],
            "title": bucket["title"],
            "filter": filter_query
        })
        position += 100
    
    return {
        "id": view_id,
        "title": new_view["title"],
        "view_kind": "kanban",
        "bucket_configuration_mode": "filter",
        "buckets": buckets
    }

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_views(
    project_id: int = Field(description="ID of the project")
) -> list[dict]:
    """
    List all views for a project.

    Returns views with IDs, titles, and view_kind (list, kanban, gantt, table).
    Use view IDs with get_view_tasks to fetch tasks via that view.
    """
    return _list_views_impl(project_id)



# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_view(
    project_id: int = Field(description="ID of the project"),
    title: str = Field(description="View title (e.g., 'High Priority Tasks')"),
    view_kind: str = Field(description="View type: list, kanban, gantt, or table"),
    filter_query: str = Field(default=None, description="Optional filter query (e.g., 'priority >= 3 && done = false')")
) -> dict:
    """
    Create a new view for a project with optional filter.
    
    Filter syntax: SQL-like queries with fields like done, priority, dueDate, assignees.
    Examples: 'done = false', 'priority >= 3 && done = false', 'dueDate < now'
    """
    return _create_view_impl(project_id, title, view_kind, filter_query)




# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def delete_view(
    project_id: int = Field(description="Project ID"),
    view_id: int = Field(description="View ID to delete")
) -> dict:
    """
    Delete a view from a project.
    
    Use this to clean up test views or remove unwanted views.
    
    Example:
    delete_view(project_id=14259, view_id=55019)
    
    Returns: {success: true, message: "..."}
    """
    return _delete_view_impl(project_id, view_id)

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def update_view(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the view to update"),
    title: str = Field(default=None, description="New title (optional)"),
    filter_query: str = Field(default=None, description="New filter query (optional)")
) -> dict:
    """
    Update a view's title and/or filter query.
    
    At least one of title or filter_query must be provided.
    """
    return _update_view_impl(project_id, view_id, title, filter_query)

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_view_tasks(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the view (get from list_views)")
) -> list[dict]:
    """
    Get tasks via a specific view endpoint.

    For kanban views, returns tasks with bucket_id and bucket_title populated.
    For list/gantt views, returns flat task list.
    Use list_tasks_by_bucket for grouped kanban view.
    """
    return _get_view_tasks_impl(project_id, view_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_tasks_by_bucket(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the kanban view (get from list_views)")
) -> dict:
    """
    Get tasks grouped by kanban bucket.

    Returns dict with bucket names as keys, each containing bucket_id and tasks array.
    Use this to understand workflow state without asking user which bucket tasks are in.

    Example response: {"📝 To-Do": {"bucket_id": 123, "tasks": [...]}, "🔥 In Progress": {...}}
    """
    return _list_tasks_by_bucket_impl(project_id, view_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def set_view_position(
    task_id: int = Field(description="ID of the task"),
    view_id: int = Field(description="ID of the view (Gantt, List, etc.)"),
    position: float = Field(description="Position value (lower = earlier in list)")
) -> dict:
    """
    Set a task's position within a specific view.

    Use this to order tasks in Gantt, List, or Table views.
    Position is a float - use increments (e.g., 1000, 2000, 3000) for easy reordering.
    """
    return _set_view_position_impl(task_id, view_id, position)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_kanban_view(
    project_id: int = Field(description="ID of the project")
) -> dict:
    """
    Get the kanban view for a project.

    Returns the view ID needed for bucket operations and task positioning.
    Every project has a default kanban view created automatically.
    """
    return _get_kanban_view_impl(project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_buckets(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the view (get from get_kanban_view)")
) -> list[dict]:
    """
    List all kanban buckets (columns) in a view.

    Returns buckets with IDs, titles, positions, and WIP limits.
    Use bucket IDs with set_task_position to move tasks.
    """
    return _list_buckets_impl(project_id, view_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_bucket(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the view (get from get_kanban_view)"),
    title: str = Field(description="Bucket/column title"),
    position: int = Field(default=0, description="Sort position (0 = first)"),
    limit: int = Field(default=0, description="WIP limit (0 = no limit)")
) -> dict:
    """
    Create a new kanban bucket (column).

    Returns the created bucket with its assigned ID.
    """
    return _create_bucket_impl(project_id, view_id, title, position, limit)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def bulk_relabel_tasks(
    project_id: int = Field(description="Project ID for label resolution"),
    task_ids: list[int] = Field(description="List of task IDs to update"),
    add_labels: list[str] = Field(default=None, description="Labels to add (will be created if needed)"),
    remove_labels: list[str] = Field(default=None, description="Labels to remove"),
    set_labels: list[str] = Field(default=None, description="Replace all labels with this list")
) -> dict:
    """
    Bulk update labels on multiple tasks. Useful for reorganizing task categorization.
    
    You can either:
    - add_labels: Add labels while keeping existing ones
    - remove_labels: Remove specific labels
    - set_labels: Replace ALL labels with a new set
    
    Labels are referenced by title and will be created if they don't exist.
    """
    return _bulk_relabel_tasks_impl(project_id, task_ids, add_labels, remove_labels, set_labels)

    return _create_bucket_impl(project_id, view_id, title, position, limit)




# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def bulk_set_task_positions(
    project_id: int = Field(description="Project ID"),
    view_id: int = Field(description="View ID (kanban view)"),
    assignments: list[dict] = Field(description="List of {task_id: int, bucket_id: int, position?: float}")
) -> dict:
    """
    Bulk assign tasks to buckets in a kanban view. Much faster than individual set_task_position calls.
    
    Example:
    bulk_set_task_positions(
        project_id=14259,
        view_id=55017,
        assignments=[
            {"task_id": 244095, "bucket_id": 39602},
            {"task_id": 244107, "bucket_id": 39603},
            ...
        ]
    )
    
    Returns: {moved_count, total_assignments, tasks: [{task_id, bucket_id, success}], errors: []}
    """
    return _bulk_set_task_positions_impl(project_id, view_id, assignments)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def move_tasks_by_label_to_buckets(
    project_id: int = Field(description="Project ID"),
    view_id: int = Field(description="View ID (kanban view)"),
    label_to_bucket_map: dict = Field(description="Map of label titles to bucket IDs, e.g., {'Phase 1': 39602}")
) -> dict:
    """
    Move tasks to buckets based on their labels. High-level tool for setting up kanban views.
    
    Finds all tasks with each label and moves them to the corresponding bucket.
    Useful for organizing tasks into alternative views (e.g., "By Phase" vs "By Domain").
    
    Example:
    move_tasks_by_label_to_buckets(
        project_id=14259,
        view_id=55017,
        label_to_bucket_map={
            "🎯 Phase 1: MVP": 39602,
            "🚀 Phase 2: Content": 39603,
            "💎 Phase 3: Polish": 39604
        }
    )
    
    Returns: {moved_count, by_label: {"Phase 1": 8, "Phase 2": 5}, errors: []}
    """
    return _move_tasks_by_label_to_buckets_impl(project_id, view_id, label_to_bucket_map)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def setup_kanban_board(
    project_id: int = Field(default=None, description="ID of existing project (or use project_title to create new)"),
    project_title: str = Field(default=None, description="Create new project with this title (alternative to project_id)"),
    template: str = Field(default="gtd", description="Template: gtd, sprint, kitchen, payables, talks, or custom"),
    custom_buckets: list = Field(default=None, description="For template='custom': list of {title, position, limit?}"),
    view_title: str = Field(default="Kanban", description="Name for the kanban view"),
    delete_default_buckets: bool = Field(default=True, description="Delete auto-created Backlog/Done buckets"),
    migrate_tasks: dict = Field(default=None, description="Map label titles to bucket titles for task migration")
) -> dict:
    """
    Rapid kanban board setup with templates and optional task migration.

    Creates a complete kanban board in one call with predefined workflow templates.
    Can also create the project in the same call (use project_title instead of project_id).
    Replaces 26+ API calls with a single tool call.

    Templates:
    - gtd: Getting Things Done (Inbox, Next, Waiting, Someday, Done)
    - sprint: Agile sprint (Backlog, To Do, In Progress, Review, Done)
    - kitchen: Cooking workflow (9 stages from Idea to Done)
    - payables: Finance workflow (Decision Queue, Approved, Paid)
    - talks: Speaking pipeline (Ideas, Submitted, Accepted, Preparing, Delivered)
    - custom: Use custom_buckets parameter

    Examples:
        # Existing project
        setup_kanban_board(project_id=123, template="sprint")

        # New project + board in one call
        setup_kanban_board(project_title="My Recipes", template="kitchen")

    Returns: {view_id, view_title, buckets_created, buckets: [...], project_id?, project_created?}
    """
    return _setup_kanban_board_impl(
        project_id=project_id,
        project_title=project_title,
        template=template,
        custom_buckets=custom_buckets,
        view_title=view_title,
        delete_default_buckets=delete_default_buckets,
        migrate_tasks=migrate_tasks
    )


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def bulk_create_labels(
    labels: list[dict] = Field(description="List of {title: str, hex_color?: str} label specs")
) -> dict:
    """
    Bulk create labels. Useful for setting up a new labeling system.
    
    Skips labels that already exist (by title). hex_color is optional (defaults to empty).
    
    Example:
    bulk_create_labels(
        labels=[
            {"title": "Easy win", "hex_color": "2ECC71"},
            {"title": "Ask for help", "hex_color": "E74C3C"},
            {"title": "Visit the Video Vault", "hex_color": "3498DB"}
        ]
    )
    
    Returns: {created_count, labels: [{id, title, hex_color}], skipped: [], errors: []}
    """
    return _bulk_create_labels_impl(labels)



# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_filtered_view(
    project_id: int = Field(description="Project ID"),
    title: str = Field(description="View title"),
    view_kind: str = Field(description="View type: kanban, list, gantt, or table"),
    filter_query: str = Field(description="Filter query (e.g., 'labels in 7350', 'priority >= 3', 'dueDate < now')"),
    bucket_config_mode: str = Field(default="manual", description="Bucket mode: 'manual' or 'none'")
) -> dict:
    """
    Create a filtered view showing only tasks matching specific criteria.
    
    Useful for creating focused views like:
    - "Quick Wins" (filter: labels in <easy_win_label_id>)
    - "High Priority" (filter: priority >= 4)
    - "This Week" (filter: dueDate >= now/w && dueDate < now/w+1w)
    - "Courses Available" (filter: labels in <course_label_id>)
    
    Filter syntax: https://vikunja.io/docs/filters/
    - Use label IDs, not titles: 'labels in 7350'
    - Combine with &&, ||, parentheses
    - Date math: now, now+1d, now/w, etc.
    
    Example:
    create_filtered_view(
        project_id=14259,
        title="Quick Wins",
        view_kind="kanban",
        filter_query="labels in 7350",
        bucket_config_mode="manual"
    )
    
    Returns: {id, title, view_kind, filter, position}
    """
    return _create_filtered_view_impl(project_id, title, view_kind, filter_query, bucket_config_mode)



# @mcp.tool()  # DISABLED: Bucket filters not working (X-Q #244154)
# @PUBLIC
def create_bucket_filtered_kanban(
    project_id: int = Field(description="Project ID"),
    title: str = Field(description="View title"),
    bucket_filters: dict = Field(description="Dict mapping bucket titles to filter queries")
) -> dict:
    """
    Create a kanban view with filter-based buckets (project-scoped).
    
    Each bucket shows only tasks from THIS PROJECT matching its filter.
    Perfect for template boards where you want filtered views within a project.
    
    Example - Effort-based kanban:
    create_bucket_filtered_kanban(
        project_id=14259,
        title="By Effort",
        bucket_filters={
            "⚡ Quick Wins": "labels in 7344",
            "🧠 Deep Work": "labels in 7345",
            "🆘 Ask for Help": "labels in 7346"
        }
    )
    
    Example - Resource-based kanban:
    create_bucket_filtered_kanban(
        project_id=14259,
        title="By Resource Type",
        bucket_filters={
            "📚 Courses": "labels in 7350",
            "🆓 Free": "labels in 7351",
            "💰 Paid": "labels in 7352"
        }
    )
    
    Returns: {id, title, view_kind, bucket_configuration_mode, buckets: [{id, title, filter}]}
    """
    return _create_bucket_filtered_kanban_impl(project_id, title, bucket_filters)

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def delete_bucket(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the view (get from get_kanban_view)"),
    bucket_id: int = Field(description="ID of the bucket to delete")
) -> dict:
    """
    Delete a kanban bucket (column).

    WARNING: Tasks in this bucket may be moved to another bucket or become unassigned.
    Returns confirmation of deletion.
    """
    return _delete_bucket_impl(project_id, view_id, bucket_id)


# ============================================================================
# RELATION OPERATIONS
# ============================================================================

# @PUBLIC_HELPER
def _create_task_relation_impl(task_id: int, relation_kind: str, other_task_id: int) -> dict:
    data = {"other_task_id": other_task_id, "relation_kind": relation_kind}
    response = _request("PUT", f"/api/v1/tasks/{task_id}/relations", json=data)
    return {"task_id": task_id, "other_task_id": other_task_id, "relation_kind": relation_kind, "created": True}


# @PUBLIC_HELPER
def _list_task_relations_impl(task_id: int) -> list[dict]:
    response = _request("GET", f"/api/v1/tasks/{task_id}")
    relations = []
    related_tasks = response.get("related_tasks") or {}
    for relation_kind, tasks in related_tasks.items():
        if tasks:
            for task in tasks:
                relations.append(_format_relation(task_id, relation_kind, task))
    return relations


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_task_relation(
    task_id: int = Field(description="ID of the source task"),
    relation_kind: str = Field(description="Relation type: 'subtask', 'parenttask', 'related', 'blocking', 'blocked', 'duplicateof', 'duplicates', 'precedes', 'follows', 'copiedfrom', 'copiedto'"),
    other_task_id: int = Field(description="ID of the target task")
) -> dict:
    """
    Create a relation between two tasks.

    Relation types:
    - subtask/parenttask: Parent-child relationship
    - blocking/blocked: Task dependencies
    - related: General association
    - precedes/follows: Sequential ordering
    - duplicateof/duplicates: Duplicate tracking
    """
    return _create_task_relation_impl(task_id, relation_kind, other_task_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_task_relations(
    task_id: int = Field(description="ID of the task")
) -> list[dict]:
    """
    List all relations for a task.

    Returns relations showing how this task connects to other tasks
    (blocking, subtasks, related, etc.).
    """
    return _list_task_relations_impl(task_id)


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

# @PUBLIC_HELPER
def _batch_create_tasks_impl(
    project_id: int,
    tasks: list[dict],
    create_missing_labels: bool = True,
    create_missing_buckets: bool = False,
    use_project_config: bool = True,
    apply_sort: bool = True,
    apply_default_labels: bool = False
) -> dict:
    """
    Create multiple tasks with labels, relations, and bucket positions.

    Task schema:
    {
        "title": str,              # required
        "description": str,        # optional
        "start_date": str,         # optional, ISO format (for GANTT)
        "end_date": str,           # optional, ISO format (for GANTT)
        "due_date": str,           # optional, ISO format (for deadlines)
        "priority": int,           # optional, 0-5
        "labels": list[str],       # optional, label names
        "bucket": str,             # optional, bucket name
        "ref": str,                # optional, local reference for relations
        "blocked_by": list[str],   # optional, refs of blocking tasks
        "blocks": list[str],       # optional, refs this task blocks
        "subtask_of": str,         # optional, ref of parent task
    }

    If use_project_config=True, applies default_bucket from config.
    If apply_default_labels=True (opt-in), applies default_labels from config to tasks without labels.
    If apply_sort=True, auto-positions tasks based on sort_strategy in config.
    """
    # Guard against queued project IDs (negative temp_id from project queue)
    _reject_queued_project_id(project_id, "batch_create_tasks")

    # Load project config if enabled
    project_config = None
    if use_project_config:
        config_result = _get_project_config_impl(project_id)
        project_config = config_result.get("config")

    # Apply config defaults to tasks
    if project_config:
        default_labels = project_config.get("default_labels", [])
        default_bucket = project_config.get("default_bucket", "")

        for task in tasks:
            # Apply default labels only if opt-in and task doesn't specify any
            if apply_default_labels and not task.get("labels") and default_labels:
                task["labels"] = default_labels.copy()
            # Apply default bucket if task doesn't specify one
            if not task.get("bucket") and default_bucket:
                task["bucket"] = default_bucket
    result = {
        "created": 0,
        "tasks": [],
        "labels_created": [],
        "relations_created": 0,
        "errors": []
    }

    # Step 0: Batch dedup - remove duplicate titles within same batch (fa-991k)
    seen_titles = set()
    deduped_tasks = []
    for task in tasks:
        title_lower = task.get("title", "").lower()
        if title_lower in seen_titles:
            if "skipped" not in result:
                result["skipped"] = []
            result["skipped"].append({
                "ref": task.get("ref"),
                "title": task.get("title"),
                "reason": "duplicate_in_batch"
            })
            logger.warning(f"[batch_create_tasks] DEDUP: Skipping duplicate title in batch: '{task.get('title')}'")
        else:
            seen_titles.add(title_lower)
            deduped_tasks.append(task)
    tasks = deduped_tasks

    # Step 1: Fetch existing labels and build name→id map
    existing_labels = _list_labels_impl()
    label_map = {l["title"]: l["id"] for l in existing_labels}

    # Step 2: Find all label names needed
    needed_labels = set()
    for task in tasks:
        for label_name in task.get("labels", []):
            if label_name not in label_map:
                needed_labels.add(label_name)

    # Step 3: Create missing labels if enabled
    if create_missing_labels and needed_labels:
        # Default colors for auto-created labels
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
        for i, label_name in enumerate(needed_labels):
            try:
                new_label = _create_label_impl(label_name, colors[i % len(colors)])
                label_map[label_name] = new_label["id"]
                result["labels_created"].append(label_name)
            except Exception as e:
                result["errors"].append(f"Failed to create label '{label_name}': {str(e)}")

    # Step 4: Fetch kanban view and buckets for bucket positioning
    view_id = None
    bucket_map = {}  # name → id

    # Check if any task needs bucket positioning
    needs_buckets = any(task.get("bucket") for task in tasks)
    if needs_buckets:
        try:
            view = _get_kanban_view_impl(project_id)
            view_id = view["id"]
            existing_buckets = _list_buckets_impl(project_id, view_id)
            bucket_map = {b["title"]: b["id"] for b in existing_buckets}

            # Create missing buckets if enabled
            if create_missing_buckets:
                needed_buckets = set()
                for task in tasks:
                    bucket_name = task.get("bucket")
                    if bucket_name and bucket_name not in bucket_map:
                        needed_buckets.add(bucket_name)

                for i, bucket_name in enumerate(needed_buckets):
                    try:
                        new_bucket = _create_bucket_impl(project_id, view_id, bucket_name, position=len(existing_buckets) + i)
                        bucket_map[bucket_name] = new_bucket["id"]
                    except Exception as e:
                        result["errors"].append(f"Failed to create bucket '{bucket_name}': {str(e)}")
        except Exception as e:
            result["errors"].append(f"Failed to get kanban view: {str(e)}")

    # Step 5: Create all tasks and build ref→id map
    ref_map = {}  # ref → task_id
    created_tasks = []  # list of (task_input, created_task)

    for task_input in tasks:
        try:
            created_task = _create_task_impl(
                project_id=project_id,
                title=task_input["title"],
                description=task_input.get("description", ""),
                start_date=task_input.get("start_date", ""),
                end_date=task_input.get("end_date", ""),
                due_date=task_input.get("due_date", ""),
                priority=task_input.get("priority", 0)
            )

            # Handle dedup case (fa-991k) - task already existed
            if created_task.get("_dedup"):
                if "skipped" not in result:
                    result["skipped"] = []
                result["skipped"].append({
                    "ref": task_input.get("ref"),
                    "id": created_task["id"],
                    "title": created_task["title"],
                    "reason": "duplicate"
                })
                # Still track ref for relations (points to existing task)
                ref = task_input.get("ref")
                if ref:
                    ref_map[ref] = created_task["id"]
                continue

            result["created"] += 1
            result["tasks"].append({
                "ref": task_input.get("ref"),
                "id": created_task["id"],
                "title": created_task["title"]
            })

            # Track ref for relations
            ref = task_input.get("ref")
            if ref:
                ref_map[ref] = created_task["id"]

            created_tasks.append((task_input, created_task))

        except Exception as e:
            result["errors"].append(f"Failed to create task '{task_input.get('title', '?')}': {str(e)}")

    # Step 6: Add labels to tasks
    for task_input, created_task in created_tasks:
        for label_name in task_input.get("labels", []):
            label_id = label_map.get(label_name)
            if label_id:
                try:
                    _add_label_to_task_impl(created_task["id"], label_id)
                except Exception as e:
                    result["errors"].append(f"Failed to add label '{label_name}' to task {created_task['id']}: {str(e)}")
            else:
                result["errors"].append(f"Label '{label_name}' not found for task {created_task['id']}")

    # Step 7: Create relations
    for task_input, created_task in created_tasks:
        task_id = created_task["id"]

        # blocked_by: this task is blocked by other tasks
        for blocker_ref in task_input.get("blocked_by", []):
            blocker_id = ref_map.get(blocker_ref)
            if blocker_id:
                try:
                    _create_task_relation_impl(task_id, "blocked", blocker_id)
                    result["relations_created"] += 1
                except Exception as e:
                    result["errors"].append(f"Failed to create blocked relation for task {task_id}: {str(e)}")
            else:
                result["errors"].append(f"Unknown ref '{blocker_ref}' in blocked_by for task {task_id}")

        # blocks: this task blocks other tasks
        for blocked_ref in task_input.get("blocks", []):
            blocked_id = ref_map.get(blocked_ref)
            if blocked_id:
                try:
                    _create_task_relation_impl(task_id, "blocking", blocked_id)
                    result["relations_created"] += 1
                except Exception as e:
                    result["errors"].append(f"Failed to create blocking relation for task {task_id}: {str(e)}")
            else:
                result["errors"].append(f"Unknown ref '{blocked_ref}' in blocks for task {task_id}")

        # subtask_of: this task is a subtask of another
        parent_ref = task_input.get("subtask_of")
        if parent_ref:
            parent_id = ref_map.get(parent_ref)
            if parent_id:
                try:
                    _create_task_relation_impl(task_id, "parenttask", parent_id)
                    result["relations_created"] += 1
                except Exception as e:
                    result["errors"].append(f"Failed to create subtask relation for task {task_id}: {str(e)}")
            else:
                result["errors"].append(f"Unknown ref '{parent_ref}' in subtask_of for task {task_id}")

    # Step 8: Set bucket positions
    if view_id and bucket_map:
        for task_input, created_task in created_tasks:
            bucket_name = task_input.get("bucket")
            if bucket_name:
                bucket_id = bucket_map.get(bucket_name)
                if bucket_id:
                    try:
                        _set_task_position_impl(created_task["id"], project_id, view_id, bucket_id)
                    except Exception as e:
                        result["errors"].append(f"Failed to set bucket for task {created_task['id']}: {str(e)}")
                else:
                    result["errors"].append(f"Bucket '{bucket_name}' not found for task {created_task['id']}")

    # Step 8.5: Set list view positions so tasks appear in creation order
    # By default, tasks get position 0 which causes random ordering in list views.
    # Set incrementing positions so first-created task appears first.
    if created_tasks:
        try:
            views = _list_views_impl(project_id)
            list_views = [v for v in views if v.get("view_kind") == "list"]

            # For each list view, set positions for all created tasks
            for lv in list_views:
                list_view_id = lv["id"]
                positions = []
                for idx, (task_input, created_task) in enumerate(created_tasks):
                    positions.append({
                        "task_id": created_task["id"],
                        "position": (idx + 1) * 1000  # 1000, 2000, 3000...
                    })

                if positions:
                    try:
                        _batch_set_positions_impl(list_view_id, positions)
                    except Exception as e:
                        result["errors"].append(f"Failed to set list positions for view {list_view_id}: {str(e)}")
        except Exception as e:
            result["errors"].append(f"Failed to set list view positions: {str(e)}")

    # Step 9: Auto-sort tasks based on project config sort_strategy
    # This finds the correct insertion point among existing tasks
    if apply_sort and project_config and view_id:
        sort_strategy = project_config.get("sort_strategy", {})
        default_strategy = sort_strategy.get("default", "manual")
        bucket_strategies = sort_strategy.get("buckets", {})

        # Group newly created tasks by bucket
        tasks_by_bucket = {}  # bucket_name → [(task_input, created_task)]
        for task_input, created_task in created_tasks:
            bucket_name = task_input.get("bucket")
            if bucket_name:
                if bucket_name not in tasks_by_bucket:
                    tasks_by_bucket[bucket_name] = []
                tasks_by_bucket[bucket_name].append((task_input, created_task))

        # Sort and position tasks in each bucket
        for bucket_name, bucket_tasks in tasks_by_bucket.items():
            strategy = bucket_strategies.get(bucket_name, default_strategy)

            if strategy == "manual":
                # Manual: skip auto-sort (bucket position already set in Step 8)
                continue

            bucket_id = bucket_map.get(bucket_name)
            if not bucket_id:
                continue

            # Fetch existing tasks in bucket with positions
            try:
                existing_raw = _get_bucket_tasks_raw(project_id, view_id, bucket_id)
            except Exception as e:
                result["errors"].append(f"Failed to fetch existing tasks in bucket '{bucket_name}': {str(e)}")
                continue

            # Filter out the newly created tasks (they're already in the bucket from Step 8)
            new_task_ids = {created_task["id"] for _, created_task in bucket_tasks}
            existing_raw = [t for t in existing_raw if t["id"] not in new_task_ids]

            # Build sorted list of (sort_key, position) for existing tasks
            existing_sorted = []
            for task in existing_raw:
                key = _get_task_sort_key(task, strategy)
                pos = task.get("position", 0)
                existing_sorted.append((key, pos))
            existing_sorted.sort(key=lambda x: x[0])

            # Extract just the sort keys for bisect
            existing_keys = [x[0] for x in existing_sorted]

            # For each new task, find insertion point and calculate position
            for task_input, created_task in bucket_tasks:
                new_key = _get_input_sort_key(task_input, created_task, strategy)

                # Binary search to find insertion point
                insert_idx = bisect.bisect_left(existing_keys, new_key)

                # Calculate position between neighbors
                if not existing_sorted:
                    # No existing tasks - use standard position
                    new_pos = 1000.0
                elif insert_idx == 0:
                    # Insert at beginning - half of first position
                    first_pos = existing_sorted[0][1]
                    new_pos = first_pos / 2 if first_pos > 0 else -1000.0
                elif insert_idx >= len(existing_sorted):
                    # Insert at end - add gap after last
                    last_pos = existing_sorted[-1][1]
                    new_pos = last_pos + 1000.0
                else:
                    # Insert between two tasks - midpoint
                    prev_pos = existing_sorted[insert_idx - 1][1]
                    next_pos = existing_sorted[insert_idx][1]
                    new_pos = (prev_pos + next_pos) / 2

                try:
                    _set_view_position_impl(created_task["id"], view_id, new_pos)
                except Exception as e:
                    result["errors"].append(f"Failed to set position for task {created_task['id']}: {str(e)}")

                # Insert into existing_sorted for subsequent calculations
                existing_sorted.insert(insert_idx, (new_key, new_pos))
                existing_keys.insert(insert_idx, new_key)

    return result


# @PUBLIC_HELPER
def _setup_project_impl(
    project_id: int,
    buckets: list[str] = None,
    labels: list[dict] = None,
    tasks: list[dict] = None
) -> dict:
    """
    Set up a project with buckets, labels, and tasks in one operation.

    labels schema: [{"name": str, "color": str}]
    tasks schema: same as batch_create_tasks
    """
    # Guard against queued project IDs (negative temp_id from project queue)
    _reject_queued_project_id(project_id, "setup_project")

    buckets = buckets or []
    labels = labels or []
    tasks = tasks or []

    result = {
        "buckets_created": [],
        "labels_created": [],
        "tasks_result": None,
        "errors": []
    }

    # Step 1: Get kanban view
    view_id = None
    if buckets:
        try:
            view = _get_kanban_view_impl(project_id)
            view_id = view["id"]
        except Exception as e:
            result["errors"].append(f"Failed to get kanban view: {str(e)}")
            return result

    # Step 2: Create missing buckets
    if view_id and buckets:
        existing_buckets = _list_buckets_impl(project_id, view_id)
        existing_names = {b["title"] for b in existing_buckets}

        for i, bucket_name in enumerate(buckets):
            if bucket_name not in existing_names:
                try:
                    _create_bucket_impl(project_id, view_id, bucket_name, position=i)
                    result["buckets_created"].append(bucket_name)
                except Exception as e:
                    result["errors"].append(f"Failed to create bucket '{bucket_name}': {str(e)}")

    # Step 3: Create missing labels
    if labels:
        existing_labels = _list_labels_impl()
        existing_label_names = {l["title"] for l in existing_labels}

        for label in labels:
            label_name = label.get("name", "")
            if label_name and label_name not in existing_label_names:
                try:
                    _create_label_impl(label_name, label.get("color", "#3498db"))
                    result["labels_created"].append(label_name)
                except Exception as e:
                    result["errors"].append(f"Failed to create label '{label_name}': {str(e)}")

    # Step 4: Create tasks using batch_create_tasks
    if tasks:
        result["tasks_result"] = _batch_create_tasks_impl(
            project_id=project_id,
            tasks=tasks,
            create_missing_labels=False,  # already done above
            create_missing_buckets=False  # already done above
        )

    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def batch_create_tasks(
    project_id: int = Field(description="ID of the project to create tasks in"),
    tasks: list[dict] = Field(description="List of task objects. Each task: {title: str (required), description: str, start_date: str (ISO, GANTT), end_date: str (ISO, GANTT), due_date: str (ISO, deadline), priority: int (0-5), labels: list[str], bucket: str, ref: str, blocked_by: list[str], blocks: list[str], subtask_of: str}"),
    create_missing_labels: bool = Field(default=True, description="Auto-create labels that don't exist"),
    create_missing_buckets: bool = Field(default=False, description="Auto-create buckets that don't exist"),
    use_project_config: bool = Field(default=True, description="Apply default_bucket from project config"),
    apply_sort: bool = Field(default=True, description="Auto-position tasks based on sort_strategy in project config"),
    apply_default_labels: bool = Field(default=False, description="Apply default_labels from config to tasks without labels (opt-in)")
) -> dict:
    """
    Create multiple tasks at once with labels, relations, and bucket positions.

    Reduces API calls by batching operations. Use 'ref' field to create relations
    between tasks in the same batch. Labels are matched by name (case-sensitive).

    If use_project_config=True, applies default_bucket from config.
    If apply_default_labels=True, applies default_labels from config to tasks without labels.
    If apply_sort=True, auto-positions tasks based on sort_strategy (start_date, due_date, etc.).

    GANTT VISIBILITY: Vikunja Gantt shows DAILY resolution only. For visible bars,
    use full-day spans: start_date="YYYY-MM-DDT00:00:00Z", end_date="YYYY-MM-DDT23:59:00Z".
    Put actual times in task title (e.g., "Bake pie (2pm-4pm)").

    Example:
    tasks=[
        {"title": "Design API (morning)", "ref": "design", "start_date": "2025-01-15T00:00:00Z", "end_date": "2025-01-15T23:59:00Z"},
        {"title": "Implement API", "ref": "impl", "blocked_by": ["design"]},
    ]

    Returns: {created: int, tasks: [{ref, id, title}], labels_created: [], relations_created: int, errors: []}
    """
    return _batch_create_tasks_impl(project_id, tasks, create_missing_labels, create_missing_buckets, use_project_config, apply_sort, apply_default_labels)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def setup_project(
    project_id: int = Field(description="ID of the project to set up"),
    buckets: list[str] = Field(default=[], description="Bucket names to ensure exist (created in order)"),
    labels: list[dict] = Field(default=[], description="Labels to ensure exist: [{name: str, color: str}]"),
    tasks: list[dict] = Field(default=[], description="Tasks to create (same schema as batch_create_tasks)")
) -> dict:
    """
    Set up a project with kanban buckets, labels, and tasks in one operation.

    Higher-level tool that orchestrates bucket creation, label creation, and
    batch task creation. Use this to bootstrap a new project structure.

    Example:
    setup_project(
        project_id=1,
        buckets=["Backlog", "In Progress", "Done"],
        labels=[{"name": "bug", "color": "#e74c3c"}, {"name": "feature", "color": "#3498db"}],
        tasks=[{"title": "First task", "bucket": "Backlog", "labels": ["feature"]}]
    )

    Returns: {buckets_created: [], labels_created: [], tasks_result: {...}, errors: []}
    """
    return _setup_project_impl(project_id, buckets, labels, tasks)


# @PUBLIC_HELPER
def _batch_update_tasks_impl(updates: list[dict]) -> dict:
    """
    Update multiple tasks at once.

    Each update dict must have 'task_id' and any fields to update:
    title, description, start_date, end_date, due_date, priority, reminders
    """
    result = {
        "updated": 0,
        "tasks": [],
        "errors": []
    }

    for update in updates:
        task_id = update.get("task_id")
        if not task_id:
            result["errors"].append("Update missing task_id")
            continue

        try:
            # GET current task to preserve fields
            current = _request("GET", f"/api/v1/tasks/{task_id}")

            # Apply updates
            if "title" in update:
                current["title"] = update["title"]
            if "description" in update:
                current["description"] = md_to_html(update["description"])
            if "start_date" in update:
                current["start_date"] = update["start_date"]
            if "end_date" in update:
                current["end_date"] = update["end_date"]
            if "due_date" in update:
                current["due_date"] = update["due_date"]
            if "priority" in update:
                current["priority"] = update["priority"]
            if "reminders" in update:
                current["reminders"] = [_format_reminder_input(r) for r in update["reminders"]]

            # POST updated task
            response = _request("POST", f"/api/v1/tasks/{task_id}", json=current)
            result["updated"] += 1
            result["tasks"].append({
                "id": task_id,
                "title": response.get("title", "")
            })
        except Exception as e:
            result["errors"].append(f"Failed to update task {task_id}: {str(e)}")

    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def batch_update_tasks(
    updates: list[dict] = Field(description="List of updates. Each: {task_id: int (required), title: str, description: str, start_date: str, end_date: str, due_date: str, priority: int, reminders: list[str]}")
) -> dict:
    """
    Update multiple tasks at once.

    Saves round trips when renaming multiple tasks or setting reminders on several tasks.
    Each update must include task_id and any fields to change.

    Example:
    updates=[
        {"task_id": 123, "title": "New title", "priority": 3},
        {"task_id": 456, "reminders": ["2025-12-20T10:00:00Z"]},
        {"task_id": 789, "due_date": "2025-12-25T17:00:00Z"}
    ]

    Returns: {updated: int, tasks: [{id, title}], errors: []}
    """
    return _batch_update_tasks_impl(updates)


# @PUBLIC_HELPER
def _batch_set_positions_impl(view_id: int, positions: list[dict]) -> dict:
    """
    Set positions for multiple tasks in a view.

    positions: [{task_id: int, position: float}, ...]
    """
    result = {
        "updated": 0,
        "tasks": [],
        "errors": []
    }

    for pos in positions:
        task_id = pos.get("task_id")
        position = pos.get("position")

        if not task_id:
            result["errors"].append("Position entry missing task_id")
            continue
        if position is None:
            result["errors"].append(f"Position entry for task {task_id} missing position")
            continue

        try:
            _set_view_position_impl(task_id, view_id, position)
            result["updated"] += 1
            result["tasks"].append({"task_id": task_id, "position": position})
        except Exception as e:
            result["errors"].append(f"Failed to set position for task {task_id}: {str(e)}")

    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def batch_set_positions(
    view_id: int = Field(description="ID of the view (get from get_kanban_view)"),
    positions: list[dict] = Field(description="List of {task_id: int, position: float}")
) -> dict:
    """
    Set positions for multiple tasks in one call.

    More efficient than calling set_view_position for each task when reordering.

    Example:
    positions=[
        {"task_id": 123, "position": 1000},
        {"task_id": 456, "position": 2000},
        {"task_id": 789, "position": 3000}
    ]

    Returns: {updated: int, tasks: [{task_id, position}], errors: []}
    """
    return _batch_set_positions_impl(view_id, positions)


# @PUBLIC_HELPER
def _sort_bucket_impl(
    project_id: int,
    view_id: int,
    bucket_id: int,
    sort_by: str = None,
    then_by: str = None
) -> dict:
    """
    Re-sort all tasks in a bucket.

    Args:
        project_id: Project ID
        view_id: View ID
        bucket_id: Bucket ID to sort
        sort_by: Primary sort field (overrides config). Options: due_date, start_date,
                 end_date, priority, title, created, position
        then_by: Secondary sort field for ties (e.g., sort by due_date, then by title)

    Fetches all tasks in bucket, sorts by strategy, assigns new positions with gaps.
    """
    result = {
        "sorted": 0,
        "tasks": [],
        "strategy": "manual",
        "then_by": None,
        "errors": []
    }

    # Determine sort strategy
    strategy = sort_by  # Use explicit parameter if provided

    if not strategy:
        # Fall back to project config
        config_result = _get_project_config_impl(project_id)
        project_config = config_result.get("config")
        if not project_config:
            result["errors"].append("No project config found and no sort_by specified")
            return result

        sort_strategy = project_config.get("sort_strategy", {})
        default_strategy = sort_strategy.get("default", "manual")
        bucket_strategies = sort_strategy.get("buckets", {})

        # Get bucket name from bucket_id
        buckets = _list_buckets_impl(project_id, view_id)
        bucket_name = None
        for b in buckets:
            if b["id"] == bucket_id:
                bucket_name = b["title"]
                break

        if not bucket_name:
            result["errors"].append(f"Bucket {bucket_id} not found")
            return result

        strategy = bucket_strategies.get(bucket_name, default_strategy)

    result["strategy"] = strategy
    result["then_by"] = then_by

    if strategy == "manual":
        result["errors"].append("Bucket uses manual sorting - no auto-sort applied. Specify sort_by to override.")
        return result

    # Fetch all tasks in bucket
    tasks_raw = _get_bucket_tasks_raw(project_id, view_id, bucket_id)
    if not tasks_raw:
        return result

    # Sort tasks by strategy (with optional secondary sort)
    sorted_tasks = sorted(tasks_raw, key=lambda t: _get_task_sort_key(t, strategy, then_by))

    # Assign new positions with gaps (1000, 2000, 3000...)
    positions = []
    for i, task in enumerate(sorted_tasks):
        position = (i + 1) * 1000.0
        positions.append({"task_id": task["id"], "position": position})

    # Apply positions in batch
    batch_result = _batch_set_positions_impl(view_id, positions)
    result["sorted"] = batch_result["updated"]
    result["tasks"] = batch_result["tasks"]
    result["errors"].extend(batch_result["errors"])

    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def sort_bucket(
    project_id: int = Field(description="ID of the project"),
    view_id: int = Field(description="ID of the kanban view (get from get_kanban_view)"),
    bucket_id: int = Field(description="ID of the bucket to sort (get from list_buckets)"),
    sort_by: str = Field(default=None, description="Primary sort field: due_date, start_date, end_date, priority, title, created, position. Overrides config if specified."),
    then_by: str = Field(default=None, description="Secondary sort for ties. E.g., sort_by=due_date, then_by=title for alphabetical within same date.")
) -> dict:
    """
    Re-sort all tasks in a bucket with optional two-level sorting.

    Supports two-level sorting for stable ordering:
    - sort_by=due_date, then_by=title → alphabetical within each date
    - sort_by=due_date, then_by=priority → urgent first within each date
    - sort_by=priority, then_by=due_date → urgent first, then by deadline

    If sort_by not specified, uses project config. If config strategy is 'manual',
    no sorting is applied unless sort_by is explicitly provided.

    Returns: {sorted: int, tasks: [{task_id, position}], strategy: str, then_by: str, errors: []}
    """
    return _sort_bucket_impl(project_id, view_id, bucket_id, sort_by, then_by)


# @PUBLIC_HELPER
def _move_task_to_project_impl(task_id: int, target_project_id: int) -> dict:
    """
    Move a task from its current project to a different project.

    Updates the task's project_id field.
    """
    # GET current task
    current = _request("GET", f"/api/v1/tasks/{task_id}")
    old_project_id = current.get("project_id")

    # Update project_id
    current["project_id"] = target_project_id

    # POST updated task
    response = _request("POST", f"/api/v1/tasks/{task_id}", json=current)

    return {
        "task_id": task_id,
        "title": response.get("title", ""),
        "old_project_id": old_project_id,
        "new_project_id": target_project_id,
        "moved": True
    }


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def move_task_to_project(
    task_id: int = Field(description="ID of the task to move"),
    target_project_id: int = Field(description="ID of the project to move the task to")
) -> dict:
    """
    Move a task to a project BY ID. Only use if you have the exact project ID.

    IMPORTANT: If you have a project NAME (like "kitchen" or "inbox"), use
    move_task_to_project_by_name instead - it handles fuzzy matching for you.

    Returns: {task_id, title, old_project_id, new_project_id, moved: true}
    """
    return _move_task_to_project_impl(task_id, target_project_id)


# @PUBLIC_HELPER
def _move_task_to_project_by_name_impl(task_id: int, project_name: str) -> dict:
    """
    Move a task to a project by name (fuzzy match).

    Looks up the project by name, then moves the task.
    Returns error if no match or ambiguous match.
    """
    matches = _find_projects_by_name(project_name)

    if not matches:
        return {"error": f"No project found matching '{project_name}'"}

    if len(matches) > 1:
        # Multiple matches - return options for user to clarify
        options = [f"{m['instance']}: {m['name']} (ID {m['project_id']})" for m in matches[:5]]
        return {
            "error": "ambiguous_project",
            "message": f"Multiple projects match '{project_name}'",
            "options": options,
            "hint": "Please specify more precisely or use move_task_to_project with the exact project ID"
        }

    # Single match - proceed with move
    target = matches[0]
    result = _move_task_to_project_impl(task_id, target["project_id"])
    result["target_project_name"] = target["name"]
    result["target_instance"] = target["instance"]
    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def move_task_to_project_by_name(
    task_id: int = Field(description="ID of the task to move"),
    project_name: str = Field(description="Name of the target project (fuzzy match)")
) -> dict:
    """
    Move a task to a project by name. USE THIS for move requests.

    This is the DEFAULT tool for moving tasks. When user says "move to kitchen"
    or "move to inbox", use this tool with project_name="kitchen" or "inbox".

    Uses fuzzy matching. If ambiguous, returns options for clarification.

    Returns: {task_id, title, old_project_id, new_project_id, target_project_name, moved: true}
    """
    return _move_task_to_project_by_name_impl(task_id, project_name)


# @PUBLIC_HELPER
def _complete_tasks_by_label_impl(project_id: int, label_filter: str) -> dict:
    """Complete all tasks matching a label filter."""
    tasks = _list_tasks_impl(project_id, include_completed=False, label_filter=label_filter)
    result = {"completed": 0, "tasks": [], "errors": []}

    for task in tasks:
        try:
            _complete_task_impl(task["id"])
            result["completed"] += 1
            result["tasks"].append({"id": task["id"], "title": task["title"]})
        except Exception as e:
            result["errors"].append(f"Failed to complete task {task['id']}: {str(e)}")

    return result


# @PUBLIC_HELPER
def _move_tasks_by_label_impl(project_id: int, label_filter: str, view_id: int, bucket_id: int) -> dict:
    """Move all tasks matching a label filter to a bucket."""
    tasks = _list_tasks_impl(project_id, include_completed=False, label_filter=label_filter)
    result = {"moved": 0, "tasks": [], "errors": []}

    for task in tasks:
        try:
            _set_task_position_impl(task["id"], project_id, view_id, bucket_id)
            result["moved"] += 1
            result["tasks"].append({"id": task["id"], "title": task["title"]})
        except Exception as e:
            result["errors"].append(f"Failed to move task {task['id']}: {str(e)}")

    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def complete_tasks_by_label(
    project_id: int = Field(description="ID of the project"),
    label_filter: str = Field(description="Label name to match (case-insensitive partial match)")
) -> dict:
    """
    Complete all tasks matching a label.

    Marks all incomplete tasks with the matching label as done.
    Use after an event to sweep tasks: complete_tasks_by_label(pid, "Sunday Party")

    Returns: {completed: int, tasks: [{id, title}], errors: []}
    """
    return _complete_tasks_by_label_impl(project_id, label_filter)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def move_tasks_by_label(
    project_id: int = Field(description="ID of the project"),
    label_filter: str = Field(description="Label name to match (case-insensitive partial match)"),
    view_id: int = Field(description="ID of the kanban view"),
    bucket_id: int = Field(description="ID of the target bucket")
) -> dict:
    """
    Move all tasks matching a label to a bucket.

    Moves all incomplete tasks with the matching label to the specified kanban bucket.
    Use for workflow transitions: move_tasks_by_label(pid, "Sourdough", vid, done_bucket_id)

    Returns: {moved: int, tasks: [{id, title}], errors: []}
    """
    return _move_tasks_by_label_impl(project_id, label_filter, view_id, bucket_id)


# ============================================================================
# PROJECT CONFIG TOOLS
# ============================================================================

# @PUBLIC_HELPER
def _get_project_config_impl(project_id: int) -> dict:
    """Get configuration for a project."""
    config = _load_config()
    project_config = config["projects"].get(str(project_id))
    return {"project_id": project_id, "config": project_config}


# @PUBLIC_HELPER
def _set_project_config_impl(project_id: int, project_config: dict) -> dict:
    """Set configuration for a project (replaces existing)."""
    config = _load_config()
    created = str(project_id) not in config["projects"]
    config["projects"][str(project_id)] = project_config
    _save_config(config)
    return {"project_id": project_id, "config": project_config, "created": created}


# @PUBLIC_HELPER
def _update_project_config_impl(project_id: int, updates: dict) -> dict:
    """Partially update configuration for a project (deep merge)."""
    config = _load_config()
    existing = config["projects"].get(str(project_id), {})
    merged = _deep_merge(existing, updates)
    config["projects"][str(project_id)] = merged
    _save_config(config)
    return {"project_id": project_id, "config": merged}


# @PUBLIC_HELPER
def _delete_project_config_impl(project_id: int) -> dict:
    """Delete configuration for a project."""
    config = _load_config()
    deleted = str(project_id) in config["projects"]
    if deleted:
        del config["projects"][str(project_id)]
        _save_config(config)
    return {"project_id": project_id, "deleted": deleted}


# @PUBLIC_HELPER
def _list_project_configs_impl() -> dict:
    """List all configured projects."""
    config = _load_config()
    projects = []
    for pid, pconfig in config["projects"].items():
        projects.append({
            "project_id": int(pid),
            "name": pconfig.get("name", f"Project {pid}")
        })
    return {"projects": projects}


# =============================================================================
# PROJECT EARS MODE (solutions-bx4t)
# Powers the !ears command for project-level listening
# DB fields use "capture_*" for backwards compatibility
# =============================================================================

# @PUBLIC_HELPER
def _get_project_ears(project_id: int) -> tuple[bool, str | None]:
    """Check if ears mode (!ears on) is enabled for a project.

    Returns:
        Tuple of (enabled, ears_since_timestamp)
    """
    config = _load_config()
    project_config = config.get("projects", {}).get(str(project_id), {})
    return (
        project_config.get("capture_enabled", False),  # DB field kept for compatibility
        project_config.get("capture_since")  # DB field kept for compatibility
    )


# @PUBLIC_HELPER
def _update_project_ears(project_id: int, enabled: bool):
    """Enable/disable ears mode (!ears on/off) for a project.

    When enabled, records the current timestamp so only tasks created
    after this point are processed.

    Args:
        project_id: Project ID
        enabled: True to enable, False to disable
    """
    config = _load_config()
    if "projects" not in config:
        config["projects"] = {}
    if str(project_id) not in config["projects"]:
        config["projects"][str(project_id)] = {}

    config["projects"][str(project_id)]["capture_enabled"] = enabled  # DB field kept for compatibility

    if enabled:
        # Record when ears mode started (only process tasks after this)
        from datetime import datetime, timezone
        config["projects"][str(project_id)]["capture_since"] = datetime.now(timezone.utc).isoformat()
    else:
        # Clear timestamp when disabled
        config["projects"][str(project_id)].pop("capture_since", None)

    _save_config(config)
    logger.info(f"[EARS] Project #{project_id} ears mode: {'ON' if enabled else 'OFF'}")


# @PUBLIC_HELPER
def _get_ears_enabled_projects() -> list[tuple[int, str]]:
    """Get all projects with ears mode (!ears on) enabled.

    Returns:
        List of (project_id, ears_since_timestamp) tuples
    """
    config = _load_config()
    enabled = []
    for pid, pconfig in config.get("projects", {}).items():
        if pconfig.get("capture_enabled") and pconfig.get("capture_since"):
            enabled.append((int(pid), pconfig["capture_since"]))
    return enabled


# @PUBLIC_HELPER
def _create_from_template_impl(
    project_id: int,
    template: str,
    anchor_time: str,
    labels: list[str] = None,
    title_suffix: str = "",
    bucket: str = None
) -> dict:
    """Create tasks from a project template with a target anchor time."""
    config = _load_config()
    project_config = config["projects"].get(str(project_id))
    if not project_config:
        raise ValueError(f"No config found for project {project_id}")

    templates = project_config.get("templates", {})
    if template not in templates:
        available = list(templates.keys()) if templates else "none"
        raise ValueError(f"Template '{template}' not found. Available: {available}")

    tmpl = templates[template]
    anchor_dt = datetime.fromisoformat(anchor_time.replace("Z", "+00:00"))

    # Build task list with calculated times
    tasks = []
    template_labels = tmpl.get("default_labels", [])
    all_labels = template_labels + (labels or [])

    for task_def in tmpl.get("tasks", []):
        offset_hours = task_def.get("offset_hours", 0)
        duration_hours = task_def.get("duration_hours", 1)

        start_dt = anchor_dt + timedelta(hours=offset_hours)
        end_dt = start_dt + timedelta(hours=duration_hours)

        # Format for Gantt visibility (full day spans)
        start_date = start_dt.strftime("%Y-%m-%dT00:00:00Z")
        end_date = start_dt.strftime("%Y-%m-%dT23:59:00Z")

        title = task_def["title"]
        if title_suffix:
            title = f"{title} {title_suffix}"

        task = {
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "labels": all_labels.copy(),
        }

        if task_def.get("ref"):
            task["ref"] = task_def["ref"]
        if task_def.get("blocked_by"):
            task["blocked_by"] = task_def["blocked_by"]
        if bucket:
            task["bucket"] = bucket

        tasks.append(task)

    # Use batch_create_tasks to create all tasks
    result = _batch_create_tasks_impl(
        project_id=project_id,
        tasks=tasks,
        create_missing_labels=True,
        create_missing_buckets=False
    )

    return result


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_project_config(
    project_id: int = Field(description="ID of the Vikunja project")
) -> dict:
    """
    Get configuration for a project.

    Returns project-specific settings: sort strategy, default labels/bucket, templates, llm_instructions.
    Returns {"project_id": X, "config": null} if no config exists.
    """
    return _get_project_config_impl(project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def set_project_config(
    project_id: int = Field(description="ID of the Vikunja project"),
    config: dict = Field(description="Configuration object: {name, sort_strategy, default_labels, default_bucket, templates, llm_instructions}")
) -> dict:
    """
    Set configuration for a project (replaces existing).

    Config schema:
    - name: Human-readable project name
    - sort_strategy: {default: "manual"|"start_date"|..., buckets: {"Bucket": "strategy"}}
    - default_labels: Labels to auto-apply to new tasks
    - default_bucket: Default bucket for new tasks
    - templates: {name: {description, anchor, default_labels, tasks: [...]}}
    - llm_instructions: Instructions for LLM when working in this project (e.g., "In recipes, use grams instead of cups")

    Returns: {project_id, config, created: bool}
    """
    return _set_project_config_impl(project_id, config)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def update_project_config(
    project_id: int = Field(description="ID of the Vikunja project"),
    updates: dict = Field(description="Fields to update (deep merged with existing)")
) -> dict:
    """
    Partially update configuration for a project.

    Deep merges updates with existing config. Use this to add a template
    or change a sort strategy without replacing the entire config.

    Example: {"sort_strategy": {"buckets": {"New Bucket": "start_date"}}}
    """
    return _update_project_config_impl(project_id, updates)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def delete_project_config(
    project_id: int = Field(description="ID of the Vikunja project")
) -> dict:
    """
    Delete configuration for a project.

    Returns: {project_id, deleted: bool}
    """
    return _delete_project_config_impl(project_id)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_project_configs() -> dict:
    """
    List all configured projects.

    Returns: {projects: [{project_id, name}, ...]}
    """
    return _list_project_configs_impl()


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def create_from_template(
    project_id: int = Field(description="ID of the project to create tasks in"),
    template: str = Field(description="Template name (e.g., 'sourdough')"),
    anchor_time: str = Field(description="ISO datetime for the anchor task (e.g., '2025-12-21T09:00:00Z')"),
    labels: list[str] = Field(default=[], description="Additional labels beyond template defaults"),
    title_suffix: str = Field(default="", description="Append to task titles (e.g., '(Sun party)')"),
    bucket: str = Field(default="", description="Override default bucket placement")
) -> dict:
    """
    Create tasks from a project template with a target anchor time.

    Templates define task sequences with relative timing (offset_hours from anchor).
    The anchor task is the reference point (e.g., "bake" at T+0).

    Example: create_from_template(pid, "sourdough", "2025-12-21T09:00:00Z", labels=["🌟 Sunday Party"])
    → Creates 6 tasks with times calculated backward from 9am bake time

    Returns: {created: int, tasks: [{ref, id, title, start_date}], relations_created: int}
    """
    return _create_from_template_impl(
        project_id, template, anchor_time,
        labels if labels else None,
        title_suffix,
        bucket if bucket else None
    )


# ============================================================================
# INSTANCE MANAGEMENT TOOLS
# ============================================================================

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_instances() -> dict:
    """
    List all configured Vikunja instances.

    Returns: {instances: [{name, url, is_current}, ...], current: str}
    """
    instances = _get_instances()

    # Get current instance - use user context if available
    user_id = _current_user_id.get()
    if user_id:
        current = _get_user_instance(user_id) or "default"
    else:
        current = _get_current_instance()

    return {
        "instances": [
            {
                "name": name,
                "url": inst.get("url"),
                "is_current": name == current
            }
            for name, inst in instances.items()
        ],
        "current": current
    }


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_context() -> dict:
    """
    Get the current Vikunja instance context.

    Returns: {instance: str, url: str}
    """
    # Use effective config which handles user context
    try:
        instance, url, _ = _get_effective_instance_config()
        return {
            "instance": instance,
            "url": url
        }
    except ValueError as e:
        # Check for env var fallback
        url = os.environ.get("VIKUNJA_URL")
        if url:
            return {
                "instance": "default (env)",
                "url": url.rstrip('/')
            }
        return {
            "instance": None,
            "url": None,
            "error": str(e)
        }


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def switch_instance(
    name: str = Field(description="Name of the instance to switch to")
) -> dict:
    """
    Switch to a different Vikunja instance.

    All subsequent operations will use the selected instance's URL and token.

    Returns: {switched_to: str, url: str}
    """
    # Use user context if available, otherwise use YAML config
    user_id = _current_user_id.get()
    if user_id:
        result = _set_user_instance(user_id, name)
        if "error" in result:
            return result
        url = result.get("url", "")
    else:
        _set_current_instance(name)
        url, _ = _get_instance_config(name)

    return {
        "switched_to": name,
        "url": url
    }



# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def check_token_health(
    instance: str = Field(default="", description="Instance name to check (empty = current instance)")
) -> dict:
    """
    Check if the current Vikunja API token is valid and not expired.

    Returns token status, expiration info, and warnings if the token is about to expire.
    Useful for diagnosing authentication issues.

    Returns: {
        instance: str,
        url: str,
        token_valid: bool,
        token_type: str,  # "jwt" or "api_token"
        expires_at: str | null,  # ISO timestamp for JWT tokens
        days_until_expiry: int | null,
        warning: str | null,  # Warning message if expiring soon
        error: str | null  # Error message if invalid
    }
    """
    from datetime import datetime, timezone
    import base64
    import json

    # Get instance config - use user context if available
    try:
        if instance:
            # Specific instance requested - use YAML config
            instance_name = instance
            url, token = _get_instance_config(instance_name)
        else:
            # No instance specified - use effective config (user context or YAML)
            instance_name, url, token = _get_effective_instance_config()
    except Exception as e:
        return {
            "instance": instance or "unknown",
            "error": f"Failed to get instance config: {e}",
            "token_valid": False
        }

    if not instance_name:
        return {
            "error": "No instance selected. Use switch_instance() first.",
            "token_valid": False
        }
    
    if not token:
        return {
            "instance": instance_name,
            "url": url,
            "error": "No token configured for this instance",
            "token_valid": False
        }
    
    result = {
        "instance": instance_name,
        "url": url,
        "token_type": "jwt" if token.startswith("eyJ") else "api_token",
        "expires_at": None,
        "days_until_expiry": None,
        "warning": None,
        "error": None
    }
    
    # Check if JWT token and extract expiration
    if result["token_type"] == "jwt":
        try:
            # Decode JWT payload (second part)
            parts = token.split('.')
            if len(parts) >= 2:
                # Add padding if needed
                payload = parts[1]
                padding = 4 - len(payload) % 4
                if padding != 4:
                    payload += '=' * padding

                decoded = base64.b64decode(payload)
                payload_data = json.loads(decoded)

                if 'exp' in payload_data:
                    exp_timestamp = payload_data['exp']
                    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                    result["expires_at"] = exp_datetime.isoformat()

                    now = datetime.now(timezone.utc)
                    days_left = (exp_datetime - now).days
                    result["days_until_expiry"] = days_left

                    if days_left < 0:
                        result["error"] = f"Token expired {abs(days_left)} days ago on {exp_datetime.strftime('%Y-%m-%d')}"
                        result["token_valid"] = False
                        return result
                    elif days_left <= 7:
                        result["warning"] = f"⚠️ Token expires in {days_left} days on {exp_datetime.strftime('%Y-%m-%d')}. Generate a new token soon!"
                    elif days_left <= 30:
                        result["warning"] = f"Token expires in {days_left} days on {exp_datetime.strftime('%Y-%m-%d')}"
        except Exception as e:
            result["warning"] = f"Could not parse JWT expiration: {e}"
    else:
        # API token - check config for expiration date
        token_expires = _get_instance_token_expires(instance_name)
        if token_expires:
            try:
                exp_date = datetime.strptime(token_expires, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                result["expires_at"] = exp_date.isoformat()

                now = datetime.now(timezone.utc)
                days_left = (exp_date - now).days
                result["days_until_expiry"] = days_left

                if days_left < 0:
                    result["warning"] = f"⚠️ Token may have expired {abs(days_left)} days ago on {token_expires}. Generate a new token!"
                elif days_left <= 7:
                    result["warning"] = f"⚠️ Token expires in {days_left} days on {token_expires}. Generate a new token soon!"
                elif days_left <= 30:
                    result["warning"] = f"Token expires in {days_left} days on {token_expires}"
            except ValueError:
                pass  # Invalid date format, ignore
        else:
            result["note"] = "No expiration date tracked. Use connect_instance with token_expires to enable expiry warnings."

    # Test the token by making an API call
    # Use /api/v1/projects instead of /api/v1/user because API tokens may not have user permission
    try:
        # _request() returns parsed JSON dict on success, raises ValueError on error
        _request("GET", "/api/v1/projects", allow_instance_fallback=True)
        result["token_valid"] = True
    except ValueError as e:
        # _request() raises ValueError for 401, 404, 4xx errors
        result["token_valid"] = False
        if "401" in str(e) or "Authentication failed" in str(e):
            result["error"] = "Token is invalid or has been revoked"
        else:
            result["error"] = f"API error: {e}"
    except Exception as e:
        result["token_valid"] = False
        result["error"] = f"Failed to test token: {e}"
    
    return result

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def admin_connect_instance(
    name: str = Field(description="Name for the instance (e.g., 'cloud', 'factumerit')"),
    url: str = Field(description="Base URL of the Vikunja instance"),
    token: str = Field(description="API token (or env var reference like '${VIKUNJA_CLOUD_TOKEN}')"),
    token_expires: str = Field(default="", description="Optional: Token expiration date (YYYY-MM-DD) for tracking"),
    timezone: str = Field(default="", description="Optional: Timezone for date conversion (e.g., 'America/Los_Angeles')")
) -> dict:
    """
    [ADMIN] Connect to a Vikunja instance with advanced options.

    Adds the instance to your local MCP config. Does not modify the Vikunja server.
    Auto-switches to this instance if it's your first connection.
    Requires admin privileges on current instance (if one exists).

    Optional fields:
    - token_expires: Track when the API token expires (for health check warnings)
    - timezone: Convert naive datetimes to UTC using this timezone

    Returns: {name, url, connected: true, switched_to?: str, hint?: str}
    """
    # Admin check - use current instance
    current = _get_current_instance()
    if current:
        admin_error = _require_admin(current)
        if admin_error:
            return admin_error

    return _connect_instance(name, url, token, token_expires, timezone)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def disconnect_instance(
    name: str = Field(description="Name of the instance to disconnect")
) -> dict:
    """
    [ADMIN] Disconnect from a Vikunja instance.

    Removes the instance from your local MCP config only.
    Does NOT delete any data on the Vikunja server - you can reconnect anytime.
    Requires admin privileges on current instance.

    Returns: {name, disconnected: true}
    """
    # Admin check - use current instance
    current = _get_current_instance()
    if current:
        admin_error = _require_admin(current)
        if admin_error:
            return admin_error

    # Prevent disconnecting the current instance
    if name == current:
        return {"error": "Cannot disconnect the currently active instance. Switch first."}

    return _disconnect_instance(name)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def rename_instance(
    old_name: str = Field(description="Current name of the instance"),
    new_name: str = Field(description="New name for the instance")
) -> dict:
    """
    [ADMIN] Rename a Vikunja instance.

    Updates all references in config (current_instance, xq, projects).
    Requires admin privileges on current instance.

    Returns: {old_name, new_name, renamed: true}
    """
    # Admin check - use current instance
    current = _get_current_instance()
    if current:
        admin_error = _require_admin(current)
        if admin_error:
            return admin_error

    return _rename_instance(old_name, new_name)


# ============================================================================
# PARALLEL FETCH TOOLS
# ============================================================================

# @PUBLIC_HELPER
def _request_for_instance(instance_name: str, method: str, endpoint: str, **kwargs) -> dict:
    """Make request to a specific instance (for parallel fetching)."""
    url, token = _get_instance_config(instance_name)
    full_url = f"{url}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.request(method, full_url, headers=headers, **kwargs)
    if response.status_code >= 400:
        raise ValueError(f"API error ({response.status_code}): {response.text}")
    if method != "DELETE":
        return response.json()
    return {}


# @PUBLIC_HELPER
def _fetch_from_all_instances(method: str, endpoint: str, **kwargs) -> dict[str, any]:
    """Fetch from all configured instances in parallel.

    Returns: {instance_name: response_data, ...}
    Errors are captured as {instance_name: {"error": str}}
    """
    instances = _get_instances()
    results = {}

    if not instances:
        return results  # No instances configured

    with ThreadPoolExecutor(max_workers=len(instances)) as executor:
        futures = {
            executor.submit(_request_for_instance, name, method, endpoint, **kwargs): name
            for name in instances.keys()
        }
        for future in as_completed(futures):
            instance_name = futures[future]
            try:
                results[instance_name] = future.result()
            except Exception as e:
                results[instance_name] = {"error": str(e)}

    return results


# @PUBLIC_HELPER
def _fetch_all_pages_for_instance(
    instance_name: str,
    method: str,
    endpoint: str,
    per_page: int = 50,
    max_pages: int = 100,
    params: dict = None
) -> list:
    """Fetch all pages from a specific instance's paginated endpoint.

    Similar to _fetch_all_pages but for multi-instance context.
    """
    all_items = []
    params = dict(params) if params else {}
    params["per_page"] = per_page

    for page in range(1, max_pages + 1):
        params["page"] = page
        try:
            data = _request_for_instance(instance_name, method, endpoint, params=params)
        except Exception:
            break

        if not isinstance(data, list):
            break

        all_items.extend(data)

        if len(data) < per_page:
            break

    return all_items


# @PUBLIC_HELPER
def _fetch_all_pages_from_all_instances(
    method: str,
    endpoint: str,
    per_page: int = 50,
    max_pages: int = 100,
    params: dict = None
) -> dict[str, list]:
    """Fetch all pages from all instances in parallel.

    Each instance is fetched with full pagination (all pages).
    Returns: {instance_name: [all_items], ...}
    """
    instances = _get_instances()
    results = {}

    if not instances:
        return results  # No instances configured

    with ThreadPoolExecutor(max_workers=len(instances)) as executor:
        futures = {
            executor.submit(
                _fetch_all_pages_for_instance,
                name, method, endpoint, per_page, max_pages, params
            ): name
            for name in instances.keys()
        }
        for future in as_completed(futures):
            instance_name = futures[future]
            try:
                results[instance_name] = future.result()
            except Exception as e:
                results[instance_name] = {"error": str(e)}

    return results


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_all_projects() -> dict:
    """
    List projects from ALL configured Vikunja instances.

    Returns: {projects: [{id, title, instance, ...}, ...], by_instance: {name: count}}
    """
    # Fetch all pages from all instances
    results = _fetch_all_pages_from_all_instances(
        "GET", "/api/v1/projects",
        per_page=50,
        max_pages=20  # Projects usually fewer than tasks
    )

    all_projects = []
    by_instance = {}

    for instance_name, data in results.items():
        if isinstance(data, dict) and "error" in data:
            by_instance[instance_name] = f"error: {data['error']}"
            continue

        by_instance[instance_name] = len(data)
        for project in data:
            all_projects.append({
                "id": project.get("id"),
                "title": project.get("title"),
                "instance": instance_name,
                "description": project.get("description", "")[:100],
            })

    # Sort by title
    all_projects.sort(key=lambda p: p.get("title", "").lower())

    return {
        "projects": all_projects,
        "total": len(all_projects),
        "by_instance": by_instance
    }


# Default limit for task listing
TASK_LIST_LIMIT = 200

# Cache for list_all_tasks results (short TTL for repeated queries)
_task_list_cache: dict = {}
_TASK_LIST_CACHE_TTL_SECONDS = 30  # 30 seconds - balances freshness vs speed


# @PUBLIC_HELPER
def _get_cached_task_list(cache_key: str) -> Optional[dict]:
    """Get cached task list if not expired."""
    if cache_key in _task_list_cache:
        result, timestamp = _task_list_cache[cache_key]
        if time.time() - timestamp < _TASK_LIST_CACHE_TTL_SECONDS:
            return result
        del _task_list_cache[cache_key]
    return None


# @PUBLIC_HELPER
def _set_cached_task_list(cache_key: str, result: dict):
    """Cache task list result."""
    _task_list_cache[cache_key] = (result, time.time())


# @PUBLIC_HELPER
def _invalidate_task_list_cache():
    """Clear task list cache (called on task create/update/delete)."""
    global _task_list_cache
    _task_list_cache = {}


# @PUBLIC_HELPER
def _list_all_tasks_impl(
    filter_due: str = "",
    include_done: bool = False,
    filter: str = "",
    page: int = 0,
    allow_truncated: bool = False,
    due_after: str = "",
    due_before: str = "",
    instance: str = "",
    project_id: int = 0
) -> dict:
    """Implementation for list_all_tasks - testable without decorator."""
    # Check cache first (30s TTL for repeated queries)
    cache_key = f"{filter_due}:{include_done}:{filter}:{page}:{due_after}:{due_before}:{instance}:{project_id}"
    cached = _get_cached_task_list(cache_key)
    if cached:
        cached["cached"] = True
        return cached

    per_page = 50  # Vikunja's actual page limit (ignores higher values)
    params = {}
    if filter:
        params["filter"] = filter

    # Choose endpoint based on whether we're querying a specific project
    # Using project-specific endpoint is more efficient and avoids delegation limits
    if project_id:
        endpoint = f"/api/v1/projects/{project_id}/tasks"
        logger.info(f"[list_all_tasks] Using project-specific endpoint: {endpoint}")
    else:
        endpoint = "/api/v1/tasks/all"
        logger.info(f"[list_all_tasks] Using all-tasks endpoint: {endpoint}")

    # Check if we have configured instances
    instances = _get_instances()

    # Determine instance name for single-instance mode
    # Use the requested instance name, or "default" if not specified
    single_instance_name = instance if instance else "default"

    # Fetch all pages unless specific page requested
    if page > 0:
        params["page"] = page
        params["per_page"] = per_page
        if instances:
            results = _fetch_from_all_instances("GET", endpoint, params=params)
        else:
            # No configured instances - use user token directly
            data = _request("GET", endpoint, params=params)
            results = {single_instance_name: data}
    else:
        # Fetch ALL pages
        if instances:
            # Multi-instance: fetch from all configured instances
            results = _fetch_all_pages_from_all_instances(
                "GET", endpoint,
                per_page=per_page,
                max_pages=100,
                params=params
            )
        else:
            # Single instance: use user token directly
            data = _fetch_all_pages("GET", endpoint, per_page=per_page, max_pages=100, params=params)
            results = {single_instance_name: data}

    all_tasks = []
    by_instance = {}
    hit_limit = False
    high_priority_no_date = 0  # Track tasks with priority >= 3 but no due date
    now = datetime.now(timezone.utc)  # Use UTC for consistent comparison with Vikunja timestamps
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = today_start + timedelta(days=7)

    total_fetched = sum(len(d) if isinstance(d, list) else 0 for d in results.values())
    logger.info(f"[list_all_tasks] QUERY: filter_due={filter_due}, project_id={project_id}, include_done={include_done}")
    logger.info(f"[list_all_tasks] FETCHED: {total_fetched} total tasks from API")
    logger.info(f"[list_all_tasks] TIME: now={now}, today_start={today_start}, today_end={today_start.replace(hour=23, minute=59, second=59)}")

    # Debug: Log raw results for project-specific queries
    if project_id and total_fetched == 0:
        logger.warning(f"[list_all_tasks] No tasks returned for project {project_id}!")
        logger.warning(f"[list_all_tasks] Raw results: {results}")
        logger.warning(f"[list_all_tasks] Endpoint used: {endpoint}")

    for instance_name, data in results.items():
        # Filter by instance if specified
        if instance and instance_name != instance:
            continue

        if isinstance(data, dict) and "error" in data:
            by_instance[instance_name] = f"error: {data['error']}"
            continue

        # Check if we hit the per_page limit
        if len(data) >= per_page:
            hit_limit = True

        instance_count = 0
        for task in data:
            # Skip done tasks unless requested
            if not include_done and task.get("done"):
                logger.debug(f"[list_all_tasks] Skipping done task #{task.get('id')}")
                continue

            # Filter by project if specified
            if project_id and task.get("project_id") != project_id:
                logger.debug(f"[list_all_tasks] Skipping task #{task.get('id')} from project {task.get('project_id')} (want {project_id})")
                continue

            due_date_str = task.get("due_date")
            due_date = None
            if due_date_str and due_date_str != "0001-01-01T00:00:00Z":
                try:
                    due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                except ValueError:
                    pass

            # Count high-priority tasks (>= 3) without due dates for hint
            if not due_date and task.get("priority", 0) >= 3:
                high_priority_no_date += 1

            # Apply due date filter
            # Date filters:
            # - "today" / "due_today" = overdue + due today (actionable items)
            # - "week" / "due_this_week" = overdue + due this week
            # - "overdue" = strictly past due
            # - "no_due_date" = tasks without due date
            # Priority filters:
            # - "priority_5" = priority >= 5
            # - "priority_3_plus" = priority >= 3
            # - "focus" = priority >= 3 AND (overdue OR due today)
            if filter_due in ("today", "due_today"):
                # Include tasks due in the past 24 hours OR future today
                # This handles timezone differences (user may be in PST while server is UTC)
                yesterday_start = today_start - timedelta(days=1)
                today_end = today_start.replace(hour=23, minute=59, second=59)
                if not due_date or due_date < yesterday_start or due_date > today_end:
                    logger.debug(f"[filter_due=today] Skipping task #{task.get('id')}: due_date={due_date}, range={yesterday_start} to {today_end}")
                    continue
                else:
                    logger.debug(f"[filter_due=today] Including task #{task.get('id')}: due_date={due_date}")
            elif filter_due in ("week", "due_this_week"):
                if not due_date or due_date > week_end:
                    continue
            elif filter_due == "overdue":
                if not due_date or due_date >= now:
                    continue
            elif filter_due == "no_due_date":
                # Only tasks WITHOUT a due date
                if due_date:
                    continue
            elif filter_due == "priority_5":
                # Priority 5 only (urgent)
                if task.get("priority", 0) < 5:
                    continue
            elif filter_due == "priority_3_plus":
                # Priority 3 or higher
                if task.get("priority", 0) < 3:
                    continue
            elif filter_due == "focus":
                # Focus mode: high priority (3+) AND (overdue OR due today)
                if task.get("priority", 0) < 3:
                    continue
                today_end = today_start.replace(hour=23, minute=59, second=59)
                if not due_date or due_date > today_end:
                    continue

            # Apply due_after filter (ISO date string like "2025-12-19")
            if due_after:
                if not due_date:
                    continue  # No due date = excluded
                try:
                    after_date = datetime.fromisoformat(due_after.replace("Z", "+00:00"))
                    if len(due_after) == 10:  # Just date, no time
                        after_date = after_date.replace(tzinfo=None)
                        due_date_naive = due_date.replace(tzinfo=None) if due_date.tzinfo else due_date
                        if due_date_naive < after_date:
                            continue
                    elif due_date < after_date:
                        continue
                except ValueError:
                    pass  # Invalid date format, skip filter

            # Apply due_before filter (ISO date string like "2025-12-25")
            if due_before:
                if not due_date:
                    continue  # No due date = excluded
                try:
                    before_date = datetime.fromisoformat(due_before.replace("Z", "+00:00"))
                    if len(due_before) == 10:  # Just date, no time
                        before_date = before_date.replace(tzinfo=None)
                        due_date_naive = due_date.replace(tzinfo=None) if due_date.tzinfo else due_date
                        if due_date_naive >= before_date:
                            continue
                    elif due_date >= before_date:
                        continue
                except ValueError:
                    pass  # Invalid date format, skip filter

            instance_count += 1
            all_tasks.append({
                "id": task.get("id"),
                "title": task.get("title"),
                "instance": instance_name,
                "project_id": task.get("project_id"),
                "due_date": due_date_str if due_date else None,
                "priority": task.get("priority", 0),
                "done": task.get("done", False),
            })

        by_instance[instance_name] = instance_count

    # Sort by due date (nulls last), then priority
# @PUBLIC
    def sort_key(t):
        due = t.get("due_date") or "9999-12-31"
        priority = 5 - t.get("priority", 0)  # Higher priority first
        return (due, priority)

    all_tasks.sort(key=sort_key)

    # Check if we hit the limit - but allow if using date filter (natural narrowing)
    if hit_limit and not allow_truncated and page == 0 and not filter_due:
        return {
            "error": "too_many_results",
            "count": len(all_tasks),
            "message": f"Found {len(all_tasks)}+ tasks (limit: {per_page}/instance). Please narrow your query:",
            "options": [
                "Add date filter: list_all_tasks(filter_due='today')",
                "Add date filter: list_all_tasks(filter_due='week')",
                f"Add filter: list_all_tasks(filter='priority >= 3')",
                f"Request page: list_all_tasks(page=1)",
                "Allow truncated: list_all_tasks(allow_truncated=true)"
            ],
            "by_instance": by_instance
        }

    result = {
        "tasks": all_tasks,
        "total": len(all_tasks),
        "filter_due": filter_due or "all",
        "filter": filter or None,
        "due_after": due_after or None,
        "due_before": due_before or None,
        "page": page if page > 0 else "all",
        "truncated": hit_limit,
        "by_instance": by_instance,
        "cached": False
    }

    # Add hint about high-priority tasks without due dates when using date filters
    if filter_due and high_priority_no_date > 0:
        result["high_priority_no_date"] = high_priority_no_date

    # Cache successful results (not errors)
    _set_cached_task_list(cache_key, result)

    return result


# ============================================================================
# FOCUSED FILTER TOOLS - Simple wrappers for common queries
# These are safe for Slack (bounded, efficient) and can be HTTP endpoints
# ============================================================================

# @PUBLIC_HELPER
def _overdue_tasks_impl(instance: str = "", project_id: int = 0) -> dict:
    """Tasks past their due date, not completed."""
    return _list_all_tasks_impl(filter_due="overdue", instance=instance, project_id=project_id)


# @PUBLIC_HELPER
def _due_today_impl(instance: str = "", project_id: int = 0) -> dict:
    """Tasks due today or overdue. Focus for right now."""
    return _list_all_tasks_impl(filter_due="today", instance=instance, project_id=project_id)


# @PUBLIC_HELPER
def _due_this_week_impl(instance: str = "", project_id: int = 0) -> dict:
    """Tasks due in the next 7 days, including overdue."""
    return _list_all_tasks_impl(filter_due="week", instance=instance, project_id=project_id)


# @PUBLIC_HELPER
def _high_priority_tasks_impl(instance: str = "", project_id: int = 0) -> dict:
    """Open tasks with priority >= 3."""
    return _list_all_tasks_impl(filter="priority >= 3", instance=instance, project_id=project_id, allow_truncated=True)


# @PUBLIC_HELPER
def _urgent_tasks_impl(instance: str = "", project_id: int = 0) -> dict:
    """Open tasks with priority >= 4 (highest priority levels)."""
    return _list_all_tasks_impl(filter="priority >= 4", instance=instance, project_id=project_id, allow_truncated=True)


# @PUBLIC_HELPER
def _unscheduled_tasks_impl(instance: str = "", project_id: int = 0) -> dict:
    """Open tasks without a due date (often forgotten/floating)."""
    # Get all tasks, then filter client-side for no due date
    # Allow truncated since we're doing a focused query
    result = _list_all_tasks_impl(allow_truncated=True, instance=instance, project_id=project_id)
    if "error" in result:
        return result

    # Filter to only tasks without due date (None or sentinel)
    unscheduled = []
    for task in result.get("tasks", []):
        due = task.get("due_date")
        if not due or due == "0001-01-01T00:00:00Z":
            unscheduled.append(task)

    return {
        "tasks": unscheduled,
        "total": len(unscheduled),
        "by_instance": result.get("by_instance", {}),
        "filter": "unscheduled (no due date)"
    }


# @PUBLIC_HELPER
def _upcoming_deadlines_impl(days: int = 3, instance: str = "", project_id: int = 0) -> dict:
    """Tasks due in the next N days (default 3). Does NOT include overdue."""
    from datetime import datetime, timezone, timedelta

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    end_date = (now + timedelta(days=days)).strftime("%Y-%m-%d")

    return _list_all_tasks_impl(due_after=today_str, due_before=end_date, instance=instance, project_id=project_id)


# @PUBLIC_HELPER
def _focus_now_impl(instance: str = "", project_id: int = 0, limit: int = 10) -> dict:
    """Tasks requiring immediate attention: priority >= 4 (high+) OR overdue."""
    from datetime import datetime, timezone

    # Get all open tasks (allow truncated for slash command use)
    result = _list_all_tasks_impl(instance=instance, project_id=project_id, allow_truncated=True)
    if "error" in result:
        return result

    now = datetime.now(timezone.utc)

    focus_tasks = []
    for task in result.get("tasks", []):
        # High priority (>= 4 = high, urgent, critical)?
        if task.get("priority", 0) >= 4:
            focus_tasks.append(task)
            continue

        # Overdue? (strictly past, not just due today)
        due_str = task.get("due_date")
        if due_str and due_str != "0001-01-01T00:00:00Z":
            try:
                due_date = datetime.fromisoformat(due_str.replace("Z", "+00:00"))
                if due_date < now:
                    focus_tasks.append(task)
            except ValueError:
                pass

    # Sort by priority (highest first), then due date
    # @PUBLIC_HELPER
    def sort_key(t):
        priority = 5 - t.get("priority", 0)  # Higher priority first
        due = t.get("due_date") or "9999-12-31"
        return (priority, due)

    focus_tasks.sort(key=sort_key)

    total_matching = len(focus_tasks)

    # Apply limit (0 = no limit)
    if limit > 0 and len(focus_tasks) > limit:
        focus_tasks = focus_tasks[:limit]

    response = {
        "tasks": focus_tasks,
        "total": len(focus_tasks),
        "by_instance": result.get("by_instance", {}),
        "filter": "focus_now (priority >= 4 OR overdue)"
    }

    # Show total_matching if we truncated
    if total_matching > len(focus_tasks):
        response["total_matching"] = total_matching
        response["hint"] = f"Showing top {len(focus_tasks)} of {total_matching}. Use limit=0 for all, or urgent_tasks() for critical-only."

    return response


# @PUBLIC_HELPER
def _task_summary_impl(instance: str = "", project_id: int = 0) -> dict:
    """Lightweight task overview - counts only, no full task details.

    Returns counts for: overdue, due_today, due_this_week, high_priority,
    urgent, unscheduled, plus total and by_instance breakdown.
    """
    from datetime import datetime, timezone, timedelta

    # Fetch all tasks once
    result = _list_all_tasks_impl(allow_truncated=True, instance=instance, project_id=project_id)
    if "error" in result:
        return result

    tasks = result.get("tasks", [])
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    week_end = today_start + timedelta(days=7)

    # Initialize counters
    overdue = 0
    due_today = 0
    due_this_week = 0
    high_priority = 0  # priority >= 3
    urgent = 0  # priority >= 4
    critical = 0  # priority == 5
    unscheduled = 0

    for task in tasks:
        priority = task.get("priority", 0)
        due_str = task.get("due_date")

        # Priority counts
        if priority >= 3:
            high_priority += 1
        if priority >= 4:
            urgent += 1
        if priority == 5:
            critical += 1

        # Due date counts
        if not due_str or due_str == "0001-01-01T00:00:00Z":
            unscheduled += 1
        else:
            try:
                due_date = datetime.fromisoformat(due_str.replace("Z", "+00:00"))
                if due_date < today_start:
                    overdue += 1
                elif due_date <= today_end:
                    due_today += 1
                elif due_date <= week_end:
                    due_this_week += 1
            except ValueError:
                pass

    return {
        "total": len(tasks),
        "overdue": overdue,
        "due_today": due_today,
        "due_this_week": due_this_week,
        "high_priority": high_priority,
        "urgent": urgent,
        "critical": critical,
        "unscheduled": unscheduled,
        "by_instance": result.get("by_instance", {}),
        "note": "Counts only - use specific tools (overdue_tasks, due_today, etc.) for details"
    }


# ============================================================================
# MCP Tools for Focused Task Queries (faster than chat, no LLM tokens)
# ============================================================================

# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def overdue_tasks(
    instance: str = Field(default="", description="Filter to specific instance (e.g., 'personal', 'business'). Empty = all instances.")
) -> dict:
    """
    Get tasks past their due date. FAST - use instead of list_all_tasks:
    - "What's overdue?"
    - "Show me late tasks"
    - "What did I miss?"

    TIP: If user has multiple instances, ask "Which instance - personal, business, or all?"
    before querying to reduce token usage.

    Returns tasks sorted by due date (oldest first).
    """
    return _overdue_tasks_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def due_today(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Get tasks due today + overdue. FAST - use for daily planning:
    - "What's due today?"
    - "What should I work on?"
    - "Today's tasks"

    TIP: If user has multiple instances, ask which one first.

    Returns tasks sorted by priority then due date.
    """
    return _due_today_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def due_this_week(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Get tasks due in the next 7 days + overdue. FAST - weekly planning:
    - "What's due this week?"
    - "Weekly overview"
    - "Upcoming deadlines"

    TIP: If user has multiple instances, ask which one first.
    """
    return _due_this_week_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def high_priority_tasks(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Get tasks with priority >= 3. FAST - important tasks:
    - "What's high priority?"
    - "Important tasks"
    - "Show me priority items"

    Priority scale: 0=none, 1-2=low, 3=medium, 4=high, 5=urgent
    TIP: If user has multiple instances, ask which one first.
    """
    return _high_priority_tasks_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def urgent_tasks(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Get tasks with priority >= 4 (critical only). FAST:
    - "What's urgent?"
    - "Critical tasks"
    - "Top priority"

    TIP: If user has multiple instances, ask which one first.
    """
    return _urgent_tasks_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def unscheduled_tasks(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Get tasks without a due date. FAST - backlog review:
    - "What has no due date?"
    - "Unscheduled tasks"
    - "Floating tasks"

    TIP: If user has multiple instances, ask which one first.
    """
    return _unscheduled_tasks_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def upcoming_deadlines(
    days: int = Field(default=3, description="Number of days to look ahead (default 3)"),
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Get tasks due in the next N days (default 3). Does NOT include overdue.
    FAST - short-term planning:
    - "What's coming up?"
    - "Next 3 days"
    - "Deadlines this week"

    TIP: If user has multiple instances, ask which one first.
    """
    return _upcoming_deadlines_impl(days=days, instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def focus_now(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances."),
    limit: int = Field(default=10, description="Max tasks to return (default 10). Use 0 for all matching tasks.")
) -> dict:
    """
    Get tasks needing immediate attention: priority >= 4 (high+) OR overdue.
    FAST - THE BEST tool for "what should I work on?":
    - "What needs my attention?"
    - "What's actionable?"
    - "Focus mode"

    TIP: If user has multiple instances, ask which one first.

    Returns top tasks sorted by priority then due date. If more tasks match,
    shows total_matching count. Use limit=0 to see all, or urgent_tasks()
    for critical-only items.
    """
    return _focus_now_impl(instance=instance, limit=limit)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def task_summary(
    instance: str = Field(default="", description="Filter to specific instance. Empty = all instances.")
) -> dict:
    """
    Lightweight task overview - COUNTS ONLY, no full task details.
    FASTEST tool for "how many tasks do I have?" / "give me an overview":
    - "How's my task load?"
    - "Quick summary"
    - "How many overdue?"

    TIP: If user has multiple instances, ask which one first to get focused results.

    Returns: {total, overdue, due_today, due_this_week, high_priority, urgent, critical, unscheduled}

    Use specific tools (overdue_tasks, due_today, etc.) to get the actual task details.
    """
    return _task_summary_impl(instance=instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def connect_instance(
    name: str = Field(description="Name for this instance (e.g., 'personal', 'work')"),
    url: str = Field(description="Vikunja instance URL (e.g., 'https://vikunja.example.com')"),
    token: str = Field(description="API token from Vikunja Settings > API Tokens")
) -> dict:
    """
    Connect a new Vikunja instance. Use when user says:
    - "Connect to my Vikunja at..."
    - "Add my personal instance..."
    - "Connect to vikunja.example.com with token..."

    Validates the token before storing. Auto-switches to this instance if it's the first one.
    """
    return _connect_instance_impl(name, url, token)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def set_active_context(
    instance: str = Field(default="", description="Default instance name (e.g., 'personal'). Empty to clear."),
    project_id: int = Field(default=0, description="Default project ID. 0 to clear.")
) -> dict:
    """
    Set default instance and/or project for subsequent queries.
    Persists across tool calls until cleared or changed.

    Use when user says:
    - "Focus on my personal instance"
    - "Switch to the Kitchen project"
    - "Only show me work tasks from now on"

    Clear with empty instance and project_id=0.
    """
    config = _load_config()
    if "mcp_context" not in config:
        config["mcp_context"] = {}

    if instance:
        # Validate instance exists
        instances = _get_instances()
        if instance not in instances:
            return {"error": f"Instance '{instance}' not found. Available: {list(instances.keys())}"}
        config["mcp_context"]["instance"] = instance
    elif "instance" in config["mcp_context"]:
        del config["mcp_context"]["instance"]

    if project_id:
        config["mcp_context"]["project_id"] = project_id
    elif "project_id" in config["mcp_context"]:
        del config["mcp_context"]["project_id"]

    _save_config(config)

    # Return current context (inline to avoid calling decorated function)
    mcp_context = config.get("mcp_context", {})
    instances = _get_instances()
    return {
        "instance": mcp_context.get("instance"),
        "project_id": mcp_context.get("project_id"),
        "available_instances": list(instances.keys()),
        "hint": "Use set_active_context to change defaults, or pass instance= to individual tools."
    }


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def get_active_context() -> dict:
    """
    Get the current default instance and project context.

    Use to check current scope before running queries, or to inform user
    what context is active.

    Returns: {instance: str or null, project_id: int or null, instances: [available list]}
    """
    config = _load_config()
    mcp_context = config.get("mcp_context", {})
    instances = _get_instances()

    return {
        "instance": mcp_context.get("instance"),
        "project_id": mcp_context.get("project_id"),
        "available_instances": list(instances.keys()),
        "hint": "Use set_active_context to change defaults, or pass instance= to individual tools."
    }


# @PUBLIC_HELPER
def _build_share_button_blocks(response_text: str) -> list:
    """Build Slack blocks for ephemeral response (private to user).

    Used for channel @mentions to protect privacy - response shown only to user.
    Share button disabled until Slack Interactivity is configured (solutions-pm0v).
    """
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": response_text
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":lock: _Only visible to you_"
                }
            ]
        }
    ]
    return blocks


# @PUBLIC_HELPER
def _format_tasks_for_slack(result: dict, title: str) -> str:
    """Format task list result as Slack mrkdwn."""
    if "error" in result:
        return f":warning: Error: {result['error']}"

    tasks = result.get("tasks", [])
    if not tasks:
        return f":white_check_mark: {title}: No tasks found"

    lines = [f"*{title}* ({len(tasks)} tasks):\n"]
    for task in tasks[:20]:  # Limit to 20 for readability
        priority = task.get("priority", 0)
        priority_emoji = {5: ":rotating_light:", 4: ":red_circle:", 3: ":large_orange_circle:", 2: ":large_yellow_circle:"}.get(priority, "")
        instance = task.get("instance", "")
        instance_tag = f" [{instance}]" if instance and len(_get_instances()) > 1 else ""
        due = task.get("due_date", "")[:10] if task.get("due_date") else ""
        due_str = f" (due {due})" if due else ""
        lines.append(f"{priority_emoji} {task.get('title', 'Untitled')}{instance_tag}{due_str}")

    if len(tasks) > 20:
        lines.append(f"\n_...and {len(tasks) - 20} more_")

    # Add instance summary if multi-instance
    by_instance = result.get("by_instance", {})
    if len(by_instance) > 1:
        instance_summary = ", ".join(f"{name}: {count}" for name, count in by_instance.items())
        lines.append(f"\n_Instances: {instance_summary}_")

    return "\n".join(lines)


# @PUBLIC_HELPER
def _format_summary_for_slack(result: dict) -> str:
    """Format task summary as Slack mrkdwn."""
    if "error" in result:
        return f":warning: Error: {result['error']}"

    total = result.get("total", 0)
    overdue = result.get("overdue", 0)
    due_today = result.get("due_today", 0)
    due_this_week = result.get("due_this_week", 0)
    critical = result.get("critical", 0)
    urgent = result.get("urgent", 0)
    high_priority = result.get("high_priority", 0)
    unscheduled = result.get("unscheduled", 0)

    lines = [f"*Task Summary* ({total} total)\n"]

    # Time-based
    if overdue:
        lines.append(f":warning: Overdue: {overdue}")
    if due_today:
        lines.append(f":calendar: Due today: {due_today}")
    if due_this_week:
        lines.append(f":date: Due this week: {due_this_week}")

    # Priority-based
    if critical:
        lines.append(f":rotating_light: Critical (P5): {critical}")
    if urgent:
        lines.append(f":red_circle: Urgent (P4+): {urgent}")
    if high_priority:
        lines.append(f":large_orange_circle: High priority (P3+): {high_priority}")

    # Other
    if unscheduled:
        lines.append(f":grey_question: Unscheduled: {unscheduled}")

    # Instance breakdown
    by_instance = result.get("by_instance", {})
    if len(by_instance) > 1:
        instance_summary = ", ".join(f"{name}: {count}" for name, count in by_instance.items())
        lines.append(f"\n_Instances: {instance_summary}_")

    return "\n".join(lines)


# @PUBLIC_HELPER
def _slash_command_multi_instance(user_id: str, impl_func, title: str) -> str:
    """Execute a filter function using multi-instance configuration.

    Multi-instance approach:
    1. Check if instances are configured via _get_instances()
    2. If instances exist, call impl_func directly (uses instance tokens)
    3. If no instances, return error (require instance configuration)
    4. Increment ECO streak and add context/ECO footers
    5. Apply active project filter if set for user
    """
    instances = _get_instances()

    if not instances:
        # No instances configured - error
        return ":x: No Vikunja instances configured. Please configure instances in config.yaml."

    # Increment ECO streak for using slash command
    _increment_eco_streak(user_id)

    # Get user's active project scope (if set)
    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    active_project = user_config.get("active_project")

    # Instances are configured - just call the impl function
    # The impl functions use _list_all_tasks_impl which uses _fetch_all_pages_from_all_instances
    # which reads tokens directly from instance configs via _get_instance_config
    try:
        # Call impl function with project scope if available
        if active_project:
            instance = active_project.get("instance", "")
            project_id = active_project.get("project_id", 0)
            result = impl_func(instance=instance, project_id=project_id)
        else:
            result = impl_func()
        response = _format_tasks_for_slack(result, title)
        # Add context and ECO footers
        response += _format_context_footer(user_id)
        response += _format_eco_footer(user_id)
        return response
    except Exception as e:
        return f":warning: Error: {str(e)}"


# @PUBLIC_HELPER
def _format_instances_for_slack() -> str:
    """Format instance list for /instances slash command."""
    instances = _get_instances()
    current = _get_current_instance()

    if not instances:
        return ":x: No Vikunja instances configured."

    lines = [f"*Configured Instances* ({len(instances)}):\n"]
    for name, config in instances.items():
        url = config.get("url", "")
        is_current = " ← current" if name == current else ""
        lines.append(f"• *{name}*: {url}{is_current}")

    return "\n".join(lines)


# @PUBLIC_HELPER
def _format_help_for_slack(topic: str = "") -> str:
    """Format help message for /help slash command."""
    topic = topic.strip().lower()

    # Detailed help for specific commands
    command_help = {
        "overdue": (
            "*`/overdue`* - Tasks past their due date\n\n"
            "Shows all incomplete tasks where due date < now.\n"
            "Sorted by due date (oldest first), then priority."
        ),
        "today": (
            "*`/today`* - Tasks due today + overdue\n\n"
            "Shows tasks due today AND any overdue tasks.\n"
            "Best for daily planning - what needs attention NOW."
        ),
        "week": (
            "*`/week`* - Tasks due this week\n\n"
            "Shows tasks due in the next 7 days + overdue.\n"
            "Good for weekly planning and sprint reviews."
        ),
        "priority": (
            "*`/priority`* - High priority tasks (3+)\n\n"
            "Shows tasks with priority 3, 4, or 5.\n"
            "Vikunja priority scale: 0=none, 1-2=low, 3=medium, 4=high, 5=urgent"
        ),
        "urgent": (
            "*`/urgent`* - Urgent tasks (priority 4+)\n\n"
            "Shows only priority 4 and 5 tasks.\n"
            "For critical items that need immediate attention."
        ),
        "unscheduled": (
            "*`/unscheduled`* - Tasks without due date\n\n"
            "Shows tasks with no due date set.\n"
            "Useful for backlog review and scheduling floating tasks."
        ),
        "focus": (
            "*`/focus`* - What to work on now\n\n"
            "Shows: high priority (3+) OR due today/overdue.\n"
            "Combines urgency and importance for actionable view."
        ),
        "summary": (
            "*`/summary`* - Quick task counts\n\n"
            "Shows counts: overdue, due today, due this week, priority levels.\n"
            "Fastest overview - no task details, just numbers."
        ),
        "connections": (
            "*`/connections`* - Show connected Vikunja instances\n\n"
            "Lists all your Vikunja connections with URLs.\n"
            "All task commands query ALL connections in parallel."
        ),
        "project": (
            "*`/project`* - Set active project context\n\n"
            "*Usage:*\n"
            "• `/project` - Show current active project\n"
            "• `/project Kitchen` - Set active project (fuzzy match)\n"
            "• `/project Kitchen 2` - Select 2nd match if ambiguous\n"
            "• `/clear` - Clear active project\n\n"
            "_When set, slash commands show only tasks from that project._"
        ),
        "connect": (
            "*`/connect`* - Connect a Vikunja instance\n\n"
            "*Usage:* `/connect <name> <url> <token>`\n\n"
            "*Example:*\n"
            "`/connect personal vikunja.example.com abc123...`\n\n"
            "*Get your token:*\n"
            "1. Log into your Vikunja instance\n"
            "2. Go to Settings > API Tokens\n"
            "3. Create a new token and copy it here\n\n"
            "_Response is always private - your token is never shown._"
        ),
        "disconnect": (
            "*`/disconnect`* - Remove a Vikunja instance\n\n"
            "*Usage:* `/disconnect <name>`\n\n"
            "*Example:* `/disconnect personal`\n\n"
            "_Use `/connections` to see available instances._"
        ),
        "usage": (
            "*`/usage`* - Toggle usage/ECO footer\n\n"
            "*Usage:*\n"
            "• `/usage` - Toggle footer on/off\n"
            "• `/usage on` - Show footer\n"
            "• `/usage off` - Hide footer\n\n"
            "_The footer shows your ECO streak (consecutive slash commands)\n"
            "and estimated token savings vs LLM queries._"
        ),
    }

    if topic and topic in command_help:
        return command_help[topic]

    if topic:
        return f":warning: Unknown command: `{topic}`\n\nType `/help` for all commands."

    # General help
    instances = _get_instances()
    instance_note = f" across {len(instances)} instances" if len(instances) > 1 else ""

    return f"""*Factum Erit Commands*{instance_note}

*Task Filters* (no LLM cost, instant):
• `/overdue` - Tasks past due date
• `/today` - Due today + overdue
• `/week` - Due within 7 days
• `/priority` - Priority 3+ tasks
• `/urgent` - Priority 4+ (critical only)
• `/unscheduled` - No due date set
• `/focus` - High priority OR due today
• `/summary` - Quick counts only (fastest)

*Context*:
• `/project [name]` - Set active project for filtering
• `/clear` - Clear active project
• `/connections` - Show connected Vikunja instances

*Setup* (always private):
• `/connect <name> <url> <token>` - Add Vikunja instance
• `/disconnect <name>` - Remove instance
• `/usage [on|off]` - Toggle ECO footer

• `/help [command]` - Help for specific command

*Chat*: Message me naturally for complex queries!
_"What's overdue in the Kitchen project?"_
_"Create a task to buy groceries, due tomorrow"_"""


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def list_all_tasks(
    filter_due: str = Field(default="", description="Filter: 'today' (overdue+today), 'week' (overdue+week), 'overdue', or empty for all"),
    include_done: bool = Field(default=False, description="Include completed tasks"),
    filter: str = Field(default="", description="Additional Vikunja filter (e.g., 'priority >= 3')"),
    page: int = Field(default=0, description="Page number (0=all pages, 1+=specific page)"),
    allow_truncated: bool = Field(default=False, description="Allow truncated results without error"),
    due_after: str = Field(default="", description="Only tasks due on or after this date (ISO format: YYYY-MM-DD)"),
    due_before: str = Field(default="", description="Only tasks due before this date (ISO format: YYYY-MM-DD)")
) -> dict:
    """
    HEAVY tool for complex task queries. Use QUICK TOOLS FIRST for common queries:

    PREFER THESE QUICK TOOLS (faster, no parameters needed):
    - overdue_tasks() → "What's overdue?"
    - due_today() → "What's due today?" / "What should I work on?"
    - due_this_week() → "What's due this week?"
    - focus_now() → "What needs attention?" / "What's actionable?"
    - high_priority_tasks() → "What's high priority?"
    - urgent_tasks() → "What's urgent/critical?"
    - unscheduled_tasks() → "What has no due date?"

    USE THIS TOOL ONLY FOR:
    - Custom date ranges: due_after="2025-12-19", due_before="2025-12-26"
    - Custom filters: filter="priority >= 3"
    - Including completed tasks: include_done=True
    - Pagination: page=1
    - Queries that need all tasks at once

    Filter meanings:
    - 'today': Overdue + due today
    - 'week': Overdue + due within 7 days
    - 'overdue': Strictly past due only

    Returns: {tasks: [{id, title, instance, project, due_date, priority, ...}], by_instance: {...}}
    """
    return _list_all_tasks_impl(
        filter_due=filter_due,
        include_done=include_done,
        filter=filter,
        page=page,
        allow_truncated=allow_truncated,
        due_after=due_after,
        due_before=due_before
    )


# Default limit for search results - if exceeded, require explicit choice
SEARCH_RESULT_LIMIT = 100


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def search_all(
    query: str = Field(description="Search term to find in task/project titles and descriptions"),
    filter: str = Field(default="", description="Additional Vikunja filter (e.g., '!done', 'priority >= 3')"),
    page: int = Field(default=0, description="Page number (0=all pages, 1+=specific page)"),
    allow_truncated: bool = Field(default=False, description="Allow truncated results without error")
) -> dict:
    """
    Search for tasks and projects across ALL configured Vikunja instances.

    Uses Vikunja's server-side filtering for efficient search.

    If results exceed limit (100), returns error with options:
    - Add filter to narrow results
    - Request specific page
    - Set allow_truncated=true to accept partial results

    Returns: {results: [{type, id, title, instance, ...}, ...], by_instance: {name: count}}
    """
    instances = _get_instances()
    all_results = []
    by_instance = {}
    query_lower = query.lower()
    per_page = 50  # Vikunja's actual page limit

    # Build server-side filter for tasks
    task_filter = f"title ~ \"{query}\" || description ~ \"{query}\""
    if filter:
        task_filter = f"({task_filter}) && ({filter})"

    # Fetch all pages unless specific page requested
    if page > 0:
        params = {"filter": task_filter, "per_page": per_page, "page": page}
        task_results = _fetch_from_all_instances("GET", "/api/v1/tasks/all", params=params)
    else:
        # Fetch ALL pages from ALL instances
        task_results = _fetch_all_pages_from_all_instances(
            "GET", "/api/v1/tasks/all",
            per_page=per_page,
            max_pages=100,
            params={"filter": task_filter}
        )

    # Projects - also paginated (fetch all pages)
    if page > 0:
        project_results = _fetch_from_all_instances("GET", "/api/v1/projects", params={"page": page})
    else:
        project_results = _fetch_all_pages_from_all_instances(
            "GET", "/api/v1/projects",
            per_page=per_page,
            max_pages=20  # Projects usually fewer than tasks
        )

    hit_limit = False
    for instance_name in instances.keys():
        instance_count = 0

        # Search projects (client-side filter)
        projects = project_results.get(instance_name, [])
        if not isinstance(projects, dict) or "error" not in projects:
            for project in projects:
                title = project.get("title", "")
                desc = project.get("description", "")
                if query_lower in title.lower() or query_lower in desc.lower():
                    instance_count += 1
                    all_results.append({
                        "type": "project",
                        "id": project.get("id"),
                        "title": title,
                        "instance": instance_name,
                        "match_in": "title" if query_lower in title.lower() else "description",
                    })

        # Tasks already filtered server-side
        tasks = task_results.get(instance_name, [])
        if not isinstance(tasks, dict) or "error" not in tasks:
            if len(tasks) >= per_page:
                hit_limit = True
            for task in tasks:
                instance_count += 1
                all_results.append({
                    "type": "task",
                    "id": task.get("id"),
                    "title": task.get("title"),
                    "instance": instance_name,
                    "project_id": task.get("project_id"),
                    "done": task.get("done", False),
                })

        by_instance[instance_name] = instance_count

    # Check if we hit the limit and user didn't explicitly allow truncation
    if hit_limit and not allow_truncated and page == 0:
        return {
            "error": "too_many_results",
            "count": len(all_results),
            "query": query,
            "message": f"Found {len(all_results)}+ results (limit: {per_page}/instance). Please narrow your search:",
            "options": [
                f"Add filter: search_all(query='{query}', filter='!done')",
                f"Request page: search_all(query='{query}', page=1)",
                f"Allow truncated: search_all(query='{query}', allow_truncated=true)"
            ],
            "by_instance": by_instance
        }

    return {
        "query": query,
        "filter": filter or None,
        "results": all_results,
        "total": len(all_results),
        "page": page if page > 0 else "all",
        "truncated": hit_limit,
        "by_instance": by_instance
    }


# ============================================================================
# X-Q (EXCHANGE QUEUE) TOOLS
# Human-to-agent task handoff protocol
# "Well X-Q me!" - Steve Martin
# ============================================================================

# @PUBLIC_HELPER
def _get_xq_config() -> dict:
    """Get X-Q project IDs from config."""
    config = _load_config()
    return config.get("xq", {})


# @PUBLIC_HELPER
def _require_admin(instance: str) -> Optional[dict]:
    """Check if instance has admin privileges.

    Returns None if admin, or error dict if not.
    """
    config = _load_config()
    inst_config = config.get("instances", {}).get(instance, {})
    if not inst_config.get("admin", False):
        return {
            "error": "admin_required",
            "message": f"Instance '{instance}' does not have admin privileges",
            "hint": "Set 'admin: true' in config for this instance"
        }
    return None


# @PUBLIC_HELPER
def _get_xq_kanban_view(instance: str, project_id: int) -> dict:
    """Get the Kanban view for an X-Q project.

    Returns: {"view_id": int, "buckets": {title: id, ...}}
    """
    # Get views for project
    views = _request_for_instance(instance, "GET", f"/api/v1/projects/{project_id}/views")

    # Find Kanban view
    kanban_view = None
    for v in views:
        if v.get("view_kind") == "kanban":
            kanban_view = v
            break

    if not kanban_view:
        return {"error": "No Kanban view found in X-Q project"}

    view_id = kanban_view["id"]

    # Get buckets for this view
    buckets = _request_for_instance(instance, "GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
    bucket_map = {b["title"]: b["id"] for b in buckets}

    return {
        "view_id": view_id,
        "buckets": bucket_map,
        "bucket_list": [{"id": b["id"], "title": b["title"]} for b in buckets]
    }


# @PUBLIC_HELPER
def _check_xq_impl(instance: str = "") -> dict:
    """Implementation of check_xq for testing."""
    xq_config = _get_xq_config()
    if not xq_config:
        return {"error": "X-Q not configured. Add 'xq' section to config with project IDs per instance."}

    instances = _get_instances()
    results = {}
    total_pending = 0

    # Filter to specific instance if requested
    check_instances = {instance: instances[instance]} if instance and instance in instances else instances

    for inst_name in check_instances:
        if inst_name not in xq_config:
            continue

        xq_project_id = xq_config[inst_name]

        try:
            # Get tasks from X-Q project
            tasks = _request_for_instance(inst_name, "GET", f"/api/v1/projects/{xq_project_id}/tasks") or []

            # Get Kanban view for bucket info
            kanban_info = _get_xq_kanban_view(inst_name, xq_project_id)
            bucket_id_to_name = {}
            if "bucket_list" in kanban_info:
                bucket_id_to_name = {b["id"]: b["title"] for b in kanban_info["bucket_list"]}

            # Filter to incomplete tasks
            pending_tasks = []
            for task in tasks:
                if task.get("done"):
                    continue

                bucket_name = bucket_id_to_name.get(task.get("bucket_id"), "No bucket")
                pending_tasks.append({
                    "id": task["id"],
                    "title": task["title"],
                    "description": task.get("description", "")[:200] if task.get("description") else "",
                    "created": task.get("created"),
                    "labels": [l["title"] for l in (task.get("labels") or [])],
                    "bucket": bucket_name
                })

            results[inst_name] = {
                "project_id": xq_project_id,
                "pending": pending_tasks,
                "count": len(pending_tasks),
                "buckets": list(bucket_id_to_name.values())
            }
            total_pending += len(pending_tasks)

        except Exception as e:
            results[inst_name] = {"error": str(e)}

    return {
        "total_pending": total_pending,
        "by_instance": results,
        "hint": "Use claim_xq_task(instance, task_id) to start processing a task"
    }


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def check_xq(
    instance: str = Field(default="", description="Instance name (empty=all instances)")
) -> dict:
    """
    Check X-Q (Exchange Queue) for pending items across instances.

    X-Q is the human→agent handoff queue. Files/tasks dropped here
    await processing by the dev agent.

    Returns incomplete tasks that need attention.
    """
    return _check_xq_impl(instance)


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def setup_xq(
    instance: str = Field(description="Instance name to setup X-Q buckets")
) -> dict:
    """
    [ADMIN] Setup X-Q project with proper buckets.

    Requires admin: true on instance config.

    Creates buckets to match X-Q pattern:
    - 📬 Handoff (default bucket for new items)
    - 🔍 Review (dev agent evaluating)
    - ✅ Filed (completed with destination)
    """
    # Admin check
    admin_error = _require_admin(instance)
    if admin_error:
        return admin_error

    xq_config = _get_xq_config()
    if instance not in xq_config:
        return {"error": f"X-Q not configured for instance '{instance}'"}

    xq_project_id = xq_config[instance]
    XQ_BUCKETS = ["📬 Handoff", "🔍 Review", "✅ Filed"]

    try:
        # Get Kanban view
        kanban_info = _get_xq_kanban_view(instance, xq_project_id)
        if "error" in kanban_info:
            return kanban_info

        view_id = kanban_info["view_id"]
        existing_buckets = kanban_info["buckets"]

        created = []
        already_exists = []

        for bucket_name in XQ_BUCKETS:
            if bucket_name in existing_buckets:
                already_exists.append(bucket_name)
            else:
                # Create bucket
                _request_for_instance(instance, "PUT", f"/api/v1/projects/{xq_project_id}/views/{view_id}/buckets", json={
                    "title": bucket_name
                })
                created.append(bucket_name)

        # Set default bucket to Inbox (best effort - may fail on some Vikunja versions)
        inbox_info = _get_xq_kanban_view(instance, xq_project_id)
        inbox_id = inbox_info["buckets"].get("📬 Handoff")
        default_bucket_set = False
        if inbox_id:
            try:
                _request_for_instance(instance, "PUT", f"/api/v1/projects/{xq_project_id}/views/{view_id}", json={
                    "default_bucket_id": inbox_id
                })
                default_bucket_set = True
            except Exception:
                # Some Vikunja versions don't support this - that's ok
                pass

        return {
            "status": "success",
            "instance": instance,
            "project_id": xq_project_id,
            "created": created,
            "already_exists": already_exists,
            "default_bucket_set": default_bucket_set,
            "hint": "X-Q is ready. Drop files as tasks in 📬 Handoff."
        }

    except Exception as e:
        return {"error": str(e)}


# @PUBLIC_HELPER
def _claim_xq_task_impl(instance: str, task_id: int) -> dict:
    """Implementation of claim_xq_task for testing."""
    xq_config = _get_xq_config()
    if instance not in xq_config:
        return {"error": f"X-Q not configured for instance '{instance}'"}

    xq_project_id = xq_config[instance]

    try:
        # Get Kanban view with buckets
        kanban_info = _get_xq_kanban_view(instance, xq_project_id)
        if "error" in kanban_info:
            return {"error": kanban_info["error"], "hint": "Run setup_xq(instance) first"}

        view_id = kanban_info["view_id"]
        review_bucket_id = kanban_info["buckets"].get("🔍 Review")
        if not review_bucket_id:
            return {"error": "No '🔍 Review' bucket found. Run setup_xq(instance) first."}

        # Get task details first
        task = _request_for_instance(instance, "GET", f"/api/v1/tasks/{task_id}")

        # Move to Review bucket via kanban API (not direct task update)
        bucket_data = {
            "task_id": task_id,
            "bucket_id": review_bucket_id,
            "project_view_id": view_id,
            "project_id": xq_project_id
        }
        _request_for_instance(
            instance, "POST",
            f"/api/v1/projects/{xq_project_id}/views/{view_id}/buckets/{review_bucket_id}/tasks",
            json=bucket_data
        )

        return {
            "status": "claimed",
            "task_id": task_id,
            "title": task.get("title"),
            "description": task.get("description"),
            "moved_to": "🔍 Review",
            "instance": instance,
            "hint": "Process the file, then use complete_xq_task(instance, task_id, destination) when done"
        }

    except Exception as e:
        return {"error": str(e)}


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def claim_xq_task(
    instance: str = Field(description="Instance name (cloud, factumerit)"),
    task_id: int = Field(description="Task ID to claim")
) -> dict:
    """
    Claim an X-Q task for processing.

    Moves the task from 📬 Handoff to 🔍 Review bucket,
    indicating the dev agent is evaluating where to file it.
    """
    return _claim_xq_task_impl(instance, task_id)


# @PUBLIC_HELPER
def _complete_xq_task_impl(instance: str, task_id: int, destination: str, notes: str = "") -> dict:
    """Implementation of complete_xq_task for testing."""
    xq_config = _get_xq_config()
    if instance not in xq_config:
        return {"error": f"X-Q not configured for instance '{instance}'"}

    xq_project_id = xq_config[instance]

    try:
        # Get Kanban view with buckets
        kanban_info = _get_xq_kanban_view(instance, xq_project_id)
        if "error" in kanban_info:
            return {"error": kanban_info["error"], "hint": "Run setup_xq(instance) first"}

        view_id = kanban_info["view_id"]
        filed_bucket_id = kanban_info["buckets"].get("✅ Filed")
        if not filed_bucket_id:
            return {"error": "No '✅ Filed' bucket found. Run setup_xq(instance) first."}

        # Get task details
        task = _request_for_instance(instance, "GET", f"/api/v1/tasks/{task_id}")

        # Update description with destination and mark done
        current_desc = task.get("description", "") or ""
        filing_note = f"\n\n---\n**Filed to:** `{destination}`\n**Filed at:** {datetime.now().isoformat()}"
        if notes:
            filing_note += f"\n**Notes:** {notes}"

        _request_for_instance(instance, "POST", f"/api/v1/tasks/{task_id}", json={
            "description": current_desc + filing_note,
            "done": True
        })

        # Move to Filed bucket via kanban API
        bucket_data = {
            "task_id": task_id,
            "bucket_id": filed_bucket_id,
            "project_view_id": view_id,
            "project_id": xq_project_id
        }
        _request_for_instance(
            instance, "POST",
            f"/api/v1/projects/{xq_project_id}/views/{view_id}/buckets/{filed_bucket_id}/tasks",
            json=bucket_data
        )

        return {
            "status": "filed",
            "task_id": task_id,
            "title": task.get("title"),
            "destination": destination,
            "moved_to": "✅ Filed",
            "instance": instance
        }

    except Exception as e:
        return {"error": str(e)}


# @PUBLIC
@mcp.tool()
@mcp_tool_with_fallback
def complete_xq_task(
    instance: str = Field(description="Instance name"),
    task_id: int = Field(description="Task ID"),
    destination: str = Field(description="Where the file was placed (e.g., '/development/projects/smcp/spec.md')"),
    notes: str = Field(default="", description="Optional notes about the filing")
) -> dict:
    """
    Complete an X-Q task after filing.

    Moves the task to ✅ Filed bucket and adds a comment
    documenting where the file was placed.
    """
    return _complete_xq_task_impl(instance, task_id, destination, notes)


# ============================================================================
# TOOL REGISTRY - Single source of truth for all tools
# ============================================================================

TOOL_REGISTRY = {
    # Projects
    "list_projects": {
        "description": "List all Vikunja projects",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _list_projects_impl
    },
    "get_project": {
        "description": "Get details of a specific project",
        "input_schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID"}},
            "required": ["project_id"]
        },
        "impl": _get_project_impl
    },
    "create_project": {
        "description": "Create a project or subproject. IMPORTANT: For subprojects (under an existing project), you MUST first call list_projects to get the parent's ID, then pass it as parent_project_id. Without parent_project_id, creates a top-level project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Project title (e.g., 'Ukulele', 'Surfing')"},
                "description": {"type": "string", "description": "Project description"},
                "hex_color": {"type": "string", "description": "Color in hex format"},
                "parent_project_id": {"type": "integer", "description": "REQUIRED for subprojects. Call list_projects first to find parent ID. Omit or 0 for top-level."}
            },
            "required": ["title"]
        },
        "impl": _create_project_impl
    },
    "update_project": {
        "description": "Update a project's properties",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "title": {"type": "string", "description": "New title"},
                "description": {"type": "string", "description": "New description"},
                "hex_color": {"type": "string", "description": "New color"},
                "parent_project_id": {"type": "integer", "description": "New parent (-1=keep, 0=root, >0=reparent)"}
            },
            "required": ["project_id"]
        },
        "impl": _update_project_impl
    },
    "share_project": {
        "description": "Share a project with a user. Use user_id when available (preferred), fall back to username. Call this after creating projects.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID to share"},
                "user_id": {"type": "integer", "description": "Numeric user ID (preferred - use this when available)"},
                "username": {"type": "string", "description": "Username (fallback if user_id not available)"},
                "right": {"type": "integer", "description": "Permission: 0=read, 1=read+write, 2=admin (default)"}
            },
            "required": ["project_id"]
        },
        "impl": _share_project_impl
    },
    "get_project_users": {
        "description": "Get list of users who have access to a project",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"}
            },
            "required": ["project_id"]
        },
        "impl": _get_project_users_impl
    },
    "delete_project": {
        "description": "Delete a project and all its tasks",
        "input_schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID"}},
            "required": ["project_id"]
        },
        "impl": _delete_project_impl
    },
    "export_all_projects": {
        "description": "Export all projects and tasks for backup",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _export_all_projects_impl
    },

    # Tasks
    "list_tasks": {
        "description": "List tasks in a project",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "include_completed": {"type": "boolean", "description": "Include completed tasks"},
                "label_filter": {"type": "string", "description": "Filter by label name"}
            },
            "required": ["project_id"]
        },
        "impl": _list_tasks_impl
    },
    "get_task": {
        "description": "Get details of a specific task",
        "input_schema": {
            "type": "object",
            "properties": {"task_id": {"type": "integer", "description": "Task ID"}},
            "required": ["task_id"]
        },
        "impl": _get_task_impl
    },
    "create_task": {
        "description": "Create a new TASK inside an existing project. Requires project_id - use list_projects first if you don't know the project ID. Tasks are items within a project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID (REQUIRED - use list_projects to find it)"},
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description (markdown)"},
                "start_date": {"type": "string", "description": "Start date (ISO format)"},
                "end_date": {"type": "string", "description": "End date (ISO format)"},
                "due_date": {"type": "string", "description": "Due date (ISO format)"},
                "priority": {"type": "integer", "description": "Priority 0-5 (5=urgent)"},
                "repeat_after": {"type": "integer", "description": "Repeat interval in seconds (0=no repeat, 86400=daily, 604800=weekly)"},
                "repeat_mode": {"type": "integer", "description": "0=repeat from due date, 1=repeat from completion date"}
            },
            "required": ["project_id", "title"]
        },
        "impl": _create_task_impl
    },
    "update_task": {
        "description": "Update a task's properties",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "title": {"type": "string", "description": "New title"},
                "description": {"type": "string", "description": "New description"},
                "start_date": {"type": "string", "description": "New start date"},
                "end_date": {"type": "string", "description": "New end date"},
                "due_date": {"type": "string", "description": "New due date"},
                "priority": {"type": "integer", "description": "New priority (-1=keep)"},
                "repeat_after": {"type": "integer", "description": "Repeat interval in seconds (-1=keep, 0=no repeat, 86400=daily)"},
                "repeat_mode": {"type": "integer", "description": "0=from due date, 1=from completion (-1=keep)"}
            },
            "required": ["task_id"]
        },
        "impl": _update_task_impl
    },
    "complete_task": {
        "description": "Mark a task as complete",
        "input_schema": {
            "type": "object",
            "properties": {"task_id": {"type": "integer", "description": "Task ID"}},
            "required": ["task_id"]
        },
        "impl": _complete_task_impl
    },
    "delete_task": {
        "description": "Delete a task",
        "input_schema": {
            "type": "object",
            "properties": {"task_id": {"type": "integer", "description": "Task ID"}},
            "required": ["task_id"]
        },
        "impl": _delete_task_impl
    },
    "batch_delete_tasks": {
        "description": "Delete multiple tasks at once. More efficient than calling delete_task repeatedly.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of task IDs to delete"
                }
            },
            "required": ["task_ids"]
        },
        "impl": _batch_delete_tasks_impl
    },
    "set_task_position": {
        "description": "Move a task to a kanban bucket",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"},
                "bucket_id": {"type": "integer", "description": "Target bucket ID"},
                "apply_sort": {"type": "boolean", "description": "Apply sort strategy"}
            },
            "required": ["task_id", "project_id", "view_id", "bucket_id"]
        },
        "impl": _set_task_position_impl
    },
    "add_label_to_task": {
        "description": "Add a label to a task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "label_id": {"type": "integer", "description": "Label ID"}
            },
            "required": ["task_id", "label_id"]
        },
        "impl": _add_label_to_task_impl
    },
    "assign_user": {
        "description": "Assign a user to a task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "user_id": {"type": "integer", "description": "User ID"}
            },
            "required": ["task_id", "user_id"]
        },
        "impl": _assign_user_impl
    },
    "unassign_user": {
        "description": "Remove a user from a task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "user_id": {"type": "integer", "description": "User ID"}
            },
            "required": ["task_id", "user_id"]
        },
        "impl": _unassign_user_impl
    },
    "set_reminders": {
        "description": "Set reminders for a task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "reminders": {"type": "array", "items": {"type": "string"}, "description": "List of ISO datetimes"}
            },
            "required": ["task_id", "reminders"]
        },
        "impl": _set_reminders_impl
    },
    "move_task_to_project": {
        "description": "Move a task to a different project",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "target_project_id": {"type": "integer", "description": "Target project ID"}
            },
            "required": ["task_id", "target_project_id"]
        },
        "impl": _move_task_to_project_impl
    },

    # Focused Filter Tools - Safe for Slack, efficient queries
    "overdue_tasks": {
        "description": "Tasks past their due date, not completed",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _overdue_tasks_impl
    },
    "due_today": {
        "description": "Tasks due today or overdue - your focus for right now",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _due_today_impl
    },
    "due_this_week": {
        "description": "Tasks due in the next 7 days, including overdue",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _due_this_week_impl
    },
    "high_priority_tasks": {
        "description": "Open tasks with priority 3+ across all instances",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _high_priority_tasks_impl
    },
    "urgent_tasks": {
        "description": "Open tasks with priority 4+ (highest priority)",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _urgent_tasks_impl
    },
    "unscheduled_tasks": {
        "description": "Open tasks without a due date (often forgotten)",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _unscheduled_tasks_impl
    },
    "upcoming_deadlines": {
        "description": "Tasks due in the next N days (default 3, excludes overdue)",
        "input_schema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "Number of days to look ahead (default 3)"}
            },
            "required": []
        },
        "impl": _upcoming_deadlines_impl
    },
    "focus_now": {
        "description": "Tasks requiring immediate attention: high priority OR due today/overdue",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _focus_now_impl
    },

    # Labels
    "list_labels": {
        "description": "List all labels",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _list_labels_impl
    },
    "create_label": {
        "description": "Create a new label",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Label title"},
                "hex_color": {"type": "string", "description": "Color in hex format"}
            },
            "required": ["title"]
        },
        "impl": _create_label_impl
    },
    "delete_label": {
        "description": "Delete a label",
        "input_schema": {
            "type": "object",
            "properties": {"label_id": {"type": "integer", "description": "Label ID"}},
            "required": ["label_id"]
        },
        "impl": _delete_label_impl
    },

    # Views
    "list_views": {
        "description": "List views for a project",
        "input_schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID"}},
            "required": ["project_id"]
        },
        "impl": _list_views_impl
    },
    "analyze_project_dimensions": {
        "description": "Analyze project data to discover labels, priorities, assignees and suggest meaningful kanban groupings. CALL THIS BEFORE create_view for kanban.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID to analyze"}
            },
            "required": ["project_id"]
        },
        "impl": _analyze_project_dimensions_impl
    },
    "suggest_filters": {
        "description": "Get ready-to-use filter queries for creating filtered views. Returns date, priority, label, and combined filters with correct syntax. Pass project_id to get label filters with actual IDs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Optional project ID to include label-based filters"}
            },
            "required": []
        },
        "impl": _suggest_filters_impl
    },
    "create_view": {
        "description": "Create a new view for a project. IMPORTANT: For kanban views, first call analyze_project_dimensions to understand the data and choose a meaningful grouping (by label, priority, assignee). Don't duplicate the default kanban - create views that slice data differently. Default buckets (To-Do/Doing/Done) are auto-deleted so you can create custom buckets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "title": {"type": "string", "description": "View title describing the grouping (e.g., 'By Priority', 'By Team Member')"},
                "view_kind": {"type": "string", "description": "View type: list, kanban, gantt, or table"},
                "filter_query": {"type": "string", "description": "Optional filter query (e.g., 'priority >= 3 && done = false')"},
                "delete_default_buckets": {"type": "boolean", "description": "For kanban views, delete auto-created To-Do/Doing/Done buckets (default true)", "default": True}
            },
            "required": ["project_id", "title", "view_kind"]
        },
        "impl": _create_view_impl
    },
    "delete_view": {
        "description": "Delete a view from a project",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID to delete"}
            },
            "required": ["project_id", "view_id"]
        },
        "impl": _delete_view_impl
    },
    "update_view": {
        "description": "Update a view's title and/or filter query",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"},
                "title": {"type": "string", "description": "New title (optional)"},
                "filter_query": {"type": "string", "description": "New filter query (optional, e.g., 'done = false')"}
            },
            "required": ["project_id", "view_id"]
        },
        "impl": _update_view_impl
    },
    "bulk_relabel_tasks": {
        "description": "Bulk update labels on multiple tasks (add, remove, or replace)",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID for label resolution"},
                "task_ids": {"type": "array", "items": {"type": "integer"}, "description": "List of task IDs to update"},
                "add_labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to add (optional)"},
                "remove_labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to remove (optional)"},
                "set_labels": {"type": "array", "items": {"type": "string"}, "description": "Replace all labels (optional)"}
            },
            "required": ["project_id", "task_ids"]
        },
        "impl": _bulk_relabel_tasks_impl
    },
    "bulk_set_task_positions": {
        "description": "Bulk assign tasks to buckets in a kanban view",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID (kanban view)"},
                "assignments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer"},
                            "bucket_id": {"type": "integer"},
                            "position": {"type": "number"}
                        },
                        "required": ["task_id", "bucket_id"]
                    },
                    "description": "List of task→bucket assignments"
                }
            },
            "required": ["project_id", "view_id", "assignments"]
        },
        "impl": _bulk_set_task_positions_impl
    },
    "move_tasks_by_label_to_buckets": {
        "description": "Move tasks to buckets based on label→bucket mappings",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID (kanban view)"},
                "label_to_bucket_map": {
                    "type": "object",
                    "description": "Map of label titles to bucket IDs",
                    "additionalProperties": {"type": "integer"}
                }
            },
            "required": ["project_id", "view_id", "label_to_bucket_map"]
        },
        "impl": _move_tasks_by_label_to_buckets_impl
    },
    "bulk_create_labels": {
        "description": "Bulk create labels (skips existing labels)",
        "input_schema": {
            "type": "object",
            "properties": {
                "labels": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Label title"},
                            "hex_color": {"type": "string", "description": "Hex color (optional, e.g., 'E74C3C')"}
                        },
                        "required": ["title"]
                    },
                    "description": "List of label specifications"
                }
            },
            "required": ["labels"]
        },
        "impl": _bulk_create_labels_impl
    },
    "create_filtered_view": {
        "description": "Create a filtered view (e.g., kanban showing only tasks with specific labels)",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "title": {"type": "string", "description": "View title"},
                "view_kind": {"type": "string", "description": "View type: kanban, list, gantt, or table"},
                "filter_query": {"type": "string", "description": "Filter query (e.g., 'labels in 7350')"},
                "bucket_config_mode": {"type": "string", "description": "Bucket mode: manual or none", "default": "manual"}
            },
            "required": ["project_id", "title", "view_kind", "filter_query"]
        },
        "impl": _create_filtered_view_impl
    },
    # DISABLED: Bucket filters not working in Vikunja API (see X-Q #244154)
    #     "create_bucket_filtered_kanban": {
    #         "description": "Create a kanban view with filter-based buckets (project-scoped)",
    #         "input_schema": {
    #             "type": "object",
    #             "properties": {
    #                 "project_id": {"type": "integer", "description": "Project ID"},
    #                 "title": {"type": "string", "description": "View title"},
    #                 "bucket_filters": {
    #                     "type": "object",
    #                     "description": "Dict mapping bucket titles to filter queries",
    #                     "additionalProperties": {"type": "string"}
    #                 }
    #             },
    #             "required": ["project_id", "title", "bucket_filters"]
    #         },
    #         "impl": _create_bucket_filtered_kanban_impl
    #     },
    "get_view_tasks": {
        "description": "Get tasks from a specific view with positions",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"}
            },
            "required": ["project_id", "view_id"]
        },
        "impl": _get_view_tasks_impl
    },
    "list_tasks_by_bucket": {
        "description": "Get tasks grouped by bucket for a kanban view",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"}
            },
            "required": ["project_id", "view_id"]
        },
        "impl": _list_tasks_by_bucket_impl
    },
    "set_view_position": {
        "description": "Set a task's position within a view",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "view_id": {"type": "integer", "description": "View ID"},
                "position": {"type": "number", "description": "Position value"}
            },
            "required": ["task_id", "view_id", "position"]
        },
        "impl": _set_view_position_impl
    },
    "get_kanban_view": {
        "description": "Get the kanban view for a project",
        "input_schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID"}},
            "required": ["project_id"]
        },
        "impl": _get_kanban_view_impl
    },

    # Buckets
    "list_buckets": {
        "description": "List buckets in a kanban view",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"}
            },
            "required": ["project_id", "view_id"]
        },
        "impl": _list_buckets_impl
    },
    "create_bucket": {
        "description": "Create a new kanban bucket",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"},
                "title": {"type": "string", "description": "Bucket title"},
                "position": {"type": "integer", "description": "Position (left to right)"},
                "limit": {"type": "integer", "description": "WIP limit (0=unlimited)"}
            },
            "required": ["project_id", "view_id", "title"]
        },
        "impl": _create_bucket_impl
    },
    "delete_bucket": {
        "description": "Delete a kanban bucket",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"},
                "bucket_id": {"type": "integer", "description": "Bucket ID"}
            },
            "required": ["project_id", "view_id", "bucket_id"]
        },
        "impl": _delete_bucket_impl
    },
    "sort_bucket": {
        "description": "Sort tasks in a bucket. Supports two-level sorting (sort_by + then_by) for stable ordering.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "view_id": {"type": "integer", "description": "View ID"},
                "bucket_id": {"type": "integer", "description": "Bucket ID"},
                "sort_by": {"type": "string", "description": "Primary sort: due_date, start_date, end_date, priority, title, created, position"},
                "then_by": {"type": "string", "description": "Secondary sort for ties (e.g., due_date+title for alphabetical within date)"}
            },
            "required": ["project_id", "view_id", "bucket_id"]
        },
        "impl": _sort_bucket_impl
    },
    "setup_kanban_board": {
        "description": "Rapid kanban board setup with templates. Creates complete board (and optionally project) in one call. Templates: gtd, sprint, kitchen, payables, talks, custom.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Existing project ID (or use project_title)"},
                "project_title": {"type": "string", "description": "Create new project with this title"},
                "template": {"type": "string", "description": "Template: gtd, sprint, kitchen, payables, talks, custom", "default": "gtd"},
                "custom_buckets": {"type": "array", "description": "For custom: [{title, position, limit?}]"},
                "view_title": {"type": "string", "description": "View title", "default": "Kanban"},
                "delete_default_buckets": {"type": "boolean", "description": "Delete auto-created buckets", "default": True},
                "migrate_tasks": {"type": "object", "description": "Map label titles to bucket titles"}
            },
            "required": []
        },
        "impl": _setup_kanban_board_impl
    },

    # Relations
    "create_task_relation": {
        "description": "Create a relation between tasks",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Source task ID"},
                "relation_kind": {"type": "string", "description": "Relation type (blocked, blocking, related, etc)"},
                "other_task_id": {"type": "integer", "description": "Target task ID"}
            },
            "required": ["task_id", "relation_kind", "other_task_id"]
        },
        "impl": _create_task_relation_impl
    },
    "list_task_relations": {
        "description": "List all relations for a task",
        "input_schema": {
            "type": "object",
            "properties": {"task_id": {"type": "integer", "description": "Task ID"}},
            "required": ["task_id"]
        },
        "impl": _list_task_relations_impl
    },

    # Batch operations
    "batch_create_tasks": {
        "description": "Create multiple tasks with labels and relations",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "tasks": {"type": "array", "items": {"type": "object"}, "description": "List of task objects"},
                "create_missing_labels": {"type": "boolean", "description": "Create labels if missing"},
                "create_missing_buckets": {"type": "boolean", "description": "Create buckets if missing"}
            },
            "required": ["project_id", "tasks"]
        },
        "impl": _batch_create_tasks_impl
    },
    "batch_update_tasks": {
        "description": "Update multiple tasks at once",
        "input_schema": {
            "type": "object",
            "properties": {
                "updates": {"type": "array", "items": {"type": "object"}, "description": "List of {task_id, ...fields}"}
            },
            "required": ["updates"]
        },
        "impl": _batch_update_tasks_impl
    },
    "batch_set_positions": {
        "description": "Set positions for multiple tasks",
        "input_schema": {
            "type": "object",
            "properties": {
                "view_id": {"type": "integer", "description": "View ID"},
                "positions": {"type": "array", "items": {"type": "object"}, "description": "List of {task_id, position}"}
            },
            "required": ["view_id", "positions"]
        },
        "impl": _batch_set_positions_impl
    },
    "setup_project": {
        "description": "Set up buckets and labels for a project",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "buckets": {"type": "array", "items": {"type": "string"}, "description": "Bucket names to create"},
                "labels": {"type": "array", "items": {"type": "string"}, "description": "Label names to create"},
                "tasks": {"type": "array", "items": {"type": "object"}, "description": "Initial tasks"}
            },
            "required": ["project_id"]
        },
        "impl": _setup_project_impl
    },

    # Bulk by label
    "complete_tasks_by_label": {
        "description": "Complete all tasks with a specific label",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "label_filter": {"type": "string", "description": "Label name to match"}
            },
            "required": ["project_id", "label_filter"]
        },
        "impl": _complete_tasks_by_label_impl
    },
    "move_tasks_by_label": {
        "description": "Move all tasks with a label to a bucket",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "label_filter": {"type": "string", "description": "Label name to match"},
                "view_id": {"type": "integer", "description": "View ID"},
                "bucket_id": {"type": "integer", "description": "Target bucket ID"}
            },
            "required": ["project_id", "label_filter", "view_id", "bucket_id"]
        },
        "impl": _move_tasks_by_label_impl
    },

    # Config
    "get_project_config": {
        "description": "Get configuration for a project",
        "input_schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID"}},
            "required": ["project_id"]
        },
        "impl": _get_project_config_impl
    },
    "set_project_config": {
        "description": "Set configuration for a project (replaces existing)",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "project_config": {"type": "object", "description": "Configuration object"}
            },
            "required": ["project_id", "project_config"]
        },
        "impl": _set_project_config_impl
    },
    "update_project_config": {
        "description": "Partially update project configuration (deep merge)",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "updates": {"type": "object", "description": "Fields to update"}
            },
            "required": ["project_id", "updates"]
        },
        "impl": _update_project_config_impl
    },
    "delete_project_config": {
        "description": "Delete configuration for a project",
        "input_schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID"}},
            "required": ["project_id"]
        },
        "impl": _delete_project_config_impl
    },
    "list_project_configs": {
        "description": "List all configured projects",
        "input_schema": {"type": "object", "properties": {}, "required": []},
        "impl": _list_project_configs_impl
    },
    "create_from_template": {
        "description": "Create tasks from a project template",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID"},
                "template": {"type": "string", "description": "Template name"},
                "anchor_time": {"type": "string", "description": "ISO datetime for anchor task"},
                "labels": {"type": "array", "items": {"type": "string"}, "description": "Additional labels"},
                "title_suffix": {"type": "string", "description": "Append to task titles"},
                "bucket": {"type": "string", "description": "Override default bucket"}
            },
            "required": ["project_id", "template", "anchor_time"]
        },
        "impl": _create_from_template_impl
    },
}


# ============================================================================
# HEALTH CHECK (for Render)
# ============================================================================

from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
import secrets
import hashlib
import base64
import json
import urllib.parse

# In-memory storage for OAuth (use Redis/DB for production multi-instance)
_oauth_codes = {}  # code -> {client_id, redirect_uri, code_challenge, expires}
_oauth_tokens = {}  # token -> {client_id, expires}


# @PRIVATE
def _generate_code():
    return secrets.token_urlsafe(32)


# @PRIVATE
def _generate_token():
    return secrets.token_urlsafe(48)


# @PRIVATE
def _verify_pkce(code_verifier: str, code_challenge: str, method: str = "S256") -> bool:
    """Verify PKCE code_verifier against code_challenge."""
    if method == "S256":
        digest = hashlib.sha256(code_verifier.encode()).digest()
        computed = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
        return computed == code_challenge
    elif method == "plain":
        return code_verifier == code_challenge
    return False


# @PRIVATE
@mcp.custom_route("/", methods=["GET"])
async def root_handler(request: Request) -> JSONResponse:
    """Root endpoint - redirect health checks."""
    return JSONResponse({"status": "ok", "service": "factumerit-bot"})


# @PRIVATE
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for Render monitoring."""
    return JSONResponse({"status": "ok"})


# @PRIVATE
@mcp.custom_route("/poller-health", methods=["GET"])
async def poller_health_check(request: Request) -> JSONResponse:
    """Health check endpoint for centralized poller monitoring.

    Returns detailed health metrics about the centralized poller:
    - Bot count
    - Poll cycles completed
    - EARS scans completed
    - Error counts per bot
    - Uptime
    - Last poll/scan times
    """
    global _centralized_poller

    if _centralized_poller is None:
        return JSONResponse({
            "status": "not_running",
            "message": "Centralized poller not initialized"
        })

    try:
        health = _centralized_poller.get_health_status()
        return JSONResponse({
            "status": "ok",
            "poller": health
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)


# @PRIVATE
@mcp.custom_route("/install-success", methods=["GET"])
async def install_success(request: Request) -> HTMLResponse:
    """Success page after Slack app installation."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Installation Successful</title>
    <style>
        body { font-family: -apple-system, sans-serif; max-width: 500px; margin: 80px auto; text-align: center; }
        h1 { color: #2eb67d; }
        p { color: #666; }
    </style>
</head>
<body>
    <h1>Installation Successful!</h1>
    <p>Factum Erit has been installed to your workspace.</p>
    <p>You can close this window and return to Slack.</p>
</body>
</html>"""
    return HTMLResponse(content=html)


# ============================================================================
# WAITING LIST SIGNUP FORM
# ============================================================================

# Configuration for waiting list (creates tasks in @admission-attendant's Vikunja)
WAITING_LIST_TOKEN = os.environ.get("WAITING_LIST_VIKUNJA_TOKEN", "")
WAITING_LIST_PROJECT_ID = int(os.environ.get("WAITING_LIST_PROJECT_ID", "0"))


# @PRIVATE
@mcp.custom_route("/waiting-list", methods=["GET"])
async def waiting_list_form(request: Request) -> HTMLResponse:
    """Render the waiting list signup form."""
    source = request.query_params.get("source", "direct")
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Join the Waiting List - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a2e;
            margin-top: 0;
            font-size: 24px;
        }}
        p {{ color: #666; line-height: 1.6; }}
        label {{
            display: block;
            margin-bottom: 6px;
            font-weight: 500;
            color: #333;
        }}
        input, textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 16px;
        }}
        input:focus, textarea:focus {{
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }}
        button {{
            width: 100%;
            padding: 14px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        button:hover {{ background: #4f46e5; }}
        .optional {{ color: #999; font-weight: normal; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Join the Waiting List</h1>
        <p>Be among the first to try Factumerit - AI-powered task management that works where you already are.</p>
        <form method="POST" action="/waiting-list">
            <input type="hidden" name="source" value="{source}">

            <label for="email">Email address</label>
            <input type="email" id="email" name="email" required placeholder="you@example.com">

            <label for="name">Name <span class="optional">(optional)</span></label>
            <input type="text" id="name" name="name" placeholder="Your name">

            <label for="message">What interests you about Factumerit? <span class="optional">(optional)</span></label>
            <textarea id="message" name="message" rows="3" placeholder="Tell us about your use case..."></textarea>

            <button type="submit">Join Waiting List</button>
        </form>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html)


# @PRIVATE
@mcp.custom_route("/waiting-list", methods=["POST"])
async def waiting_list_submit(request: Request) -> HTMLResponse:
    """Handle waiting list form submission - create task in Vikunja."""
    # Parse form data
    form = await request.form()
    email = form.get("email", "").strip()
    name = form.get("name", "").strip()
    message = form.get("message", "").strip()
    source = form.get("source", "direct").strip()

    # Validate email
    if not email or "@" not in email:
        return HTMLResponse(
            content=_waiting_list_error_html("Please provide a valid email address."),
            status_code=400
        )

    # Check configuration
    if not WAITING_LIST_TOKEN or not WAITING_LIST_PROJECT_ID:
        logger.error("Waiting list not configured: missing WAITING_LIST_VIKUNJA_TOKEN or WAITING_LIST_PROJECT_ID")
        return HTMLResponse(
            content=_waiting_list_error_html("Waiting list temporarily unavailable. Please try again later."),
            status_code=500
        )

    # Build task title and description (HTML for Vikunja)
    # Escape user input to prevent XSS
    from html import escape
    safe_name = escape(name) if name else ""
    safe_email = escape(email)
    safe_source = escape(source)
    safe_message = escape(message) if message else ""

    task_title = f"{safe_email}" + (f" ({safe_name})" if safe_name else "")
    description_parts = []
    if safe_name:
        description_parts.append(f"<b>Name:</b> {safe_name}")
    description_parts.append(f"<b>Email:</b> {safe_email}")
    description_parts.append(f"<b>Source:</b> {safe_source}")
    if safe_message:
        description_parts.append(f"<br><b>Message:</b><br>{safe_message}")
    description_parts.append(f"<hr><i>Submitted: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</i>")
    task_description = "<br>".join(description_parts)

    # Create task in Vikunja
    try:
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        resp = requests.put(
            f"{vikunja_url}/api/v1/projects/{WAITING_LIST_PROJECT_ID}/tasks",
            headers={
                "Authorization": f"Bearer {WAITING_LIST_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "title": task_title,
                "description": task_description,
            },
            timeout=10,
        )
        resp.raise_for_status()
        logger.info(f"Waiting list signup: {email} (source: {source})")
    except Exception as e:
        logger.error(f"Failed to create waiting list task: {e}")
        return HTMLResponse(
            content=_waiting_list_error_html("Something went wrong. Please try again later."),
            status_code=500
        )

    return HTMLResponse(content=_waiting_list_success_html())


# @PRIVATE
def _waiting_list_success_html() -> str:
    """Success page after waiting list signup."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>You're on the list! - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 80px auto;
            padding: 20px;
            text-align: center;
        }
        .emoji { font-size: 48px; margin-bottom: 16px; }
        h1 { color: #059669; margin-bottom: 8px; }
        p { color: #666; line-height: 1.6; }
        a { color: #6366f1; }
    </style>
</head>
<body>
    <div class="emoji">🎉</div>
    <h1>You're on the list!</h1>
    <p>Thanks for your interest in Factumerit. We'll reach out soon with early access details.</p>
    <p><a href="https://factumerit.app">← Back to Factumerit</a></p>
</body>
</html>"""


# @PRIVATE
def _waiting_list_error_html(message: str) -> str:
    """Error page for waiting list signup failures."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Oops - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 80px auto;
            padding: 20px;
            text-align: center;
        }}
        h1 {{ color: #dc2626; }}
        p {{ color: #666; }}
        a {{ color: #6366f1; }}
    </style>
</head>
<body>
    <h1>Oops!</h1>
    <p>{message}</p>
    <p><a href="/waiting-list">← Try again</a></p>
</body>
</html>"""


# ============================================================================
# BETA SIGNUP (Gated access with registration tokens)
# ============================================================================
# Bead: solutions-ltye

# @PRIVATE
@mcp.custom_route("/beta-signup", methods=["GET"])
async def beta_signup_form(request: Request) -> HTMLResponse:
    """Render the beta signup form or auto-validate if code provided.

    Simplified flow:
    - If ?code=X in URL → validate immediately → show Google/Password choice
    - If no code → show code entry form (edge case)
    """
    from starlette.responses import HTMLResponse

    # If code provided in URL, validate and skip to choice page
    prefill_code = request.query_params.get("code", "").strip().upper()

    if prefill_code:
        # Auto-validate the code
        from .registration_tokens import (
            validate_registration_token,
            TokenNotFoundError,
            TokenExhaustedError,
            TokenExpiredError,
            TokenRevokedError,
        )

        try:
            # Validate with placeholder - actual identity comes from OAuth/password form
            token_data = validate_registration_token(prefill_code, user_id="pending")
            logger.info(f"Beta signup: Token {prefill_code} auto-validated from URL")

            # Store validated code in cookie and show choice page
            initial_credit_cents = token_data.get("initial_credit_cents", 0)
            ttl_days = token_data.get("ttl_days")
            serializer = _get_cookie_serializer()
            signup_state = serializer.dumps({
                "code": prefill_code,
                "initial_credit_cents": initial_credit_cents,
                "ttl_days": ttl_days,
                "validated_at": time.time(),
            })

            response = HTMLResponse(content=_signup_choice_html(), status_code=200)
            response.set_cookie(
                key="signup_state",
                value=signup_state,
                max_age=600,
                httponly=True,
                secure=True,
                samesite="lax",
                path="/",
            )
            return response

        except (TokenNotFoundError, TokenExhaustedError, TokenExpiredError, TokenRevokedError) as e:
            # Invalid code - show error with option to try again
            error_msg = {
                TokenNotFoundError: "Invalid registration code.",
                TokenExhaustedError: "This code has reached its usage limit.",
                TokenExpiredError: "This registration code has expired.",
                TokenRevokedError: "This code is no longer valid.",
            }.get(type(e), "Invalid registration code.")
            return HTMLResponse(
                content=_beta_signup_error_html(error_msg),
                status_code=400
            )

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Sign Up - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 420px;
            margin: 60px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 40px 32px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .logo {{ font-size: 48px; margin-bottom: 8px; text-align: center; }}
        h1 {{
            color: #1a1a2e;
            margin: 0 0 8px;
            font-size: 24px;
            text-align: center;
        }}
        .subtitle {{ color: #666; text-align: center; margin-bottom: 24px; }}
        label {{
            display: block;
            margin-bottom: 6px;
            font-weight: 500;
            color: #333;
        }}
        input {{
            width: 100%;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        input:focus {{
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }}
        .code-input {{
            font-family: monospace;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-align: center;
            font-size: 18px;
        }}
        button {{
            width: 100%;
            padding: 14px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            margin-top: 16px;
        }}
        button:hover {{ background: #4f46e5; }}
        .hint {{ font-size: 13px; color: #888; text-align: center; }}
        .login-link {{ text-align: center; margin-top: 20px; font-size: 14px; color: #666; }}
        .login-link a {{ color: #6366f1; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">✨</div>
        <h1>Create Your Account</h1>
        <p class="subtitle">Enter your registration code to get started</p>
        <form method="POST" action="/beta-signup">
            <label for="code">Registration Code</label>
            <input type="text" id="code" name="code" required
                   class="code-input" placeholder="CODE-HERE"
                   value="{prefill_code}" pattern="[A-Za-z0-9-]+"
                   title="Registration codes are letters, numbers, and hyphens"
                   autocomplete="off" autocapitalize="characters">
            <p class="hint">From your signup link or event organizer</p>
            <button type="submit">Continue</button>
        </form>
        <p class="login-link">Already have an account? <a href="https://vikunja.factumerit.app/login">Sign in</a></p>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html)


# @PRIVATE
@mcp.custom_route("/beta-signup", methods=["POST"])
async def beta_signup_submit(request: Request) -> HTMLResponse:
    """Handle manual code entry (edge case when no URL param).

    Validates code and shows auth method choice.
    """
    from starlette.responses import HTMLResponse

    # Parse form data - only code needed
    form = await request.form()
    code = form.get("code", "").strip().upper()

    if not code:
        return HTMLResponse(
            content=_beta_signup_error_html("Registration code is required."),
            status_code=400
        )

    # Import registration token validation
    from .registration_tokens import (
        validate_registration_token,
        TokenNotFoundError,
        TokenExhaustedError,
        TokenExpiredError,
        TokenRevokedError,
    )

    # Validate token
    try:
        token_data = validate_registration_token(code, user_id="pending")
        logger.info(f"Beta signup POST: Token {code} validated")
    except TokenNotFoundError:
        return HTMLResponse(
            content=_beta_signup_error_html("Invalid registration code. Please check and try again."),
            status_code=400
        )
    except TokenExhaustedError:
        return HTMLResponse(
            content=_beta_signup_error_html("This registration code has reached its usage limit."),
            status_code=400
        )
    except TokenExpiredError:
        return HTMLResponse(
            content=_beta_signup_error_html("This registration code has expired."),
            status_code=400
        )
    except TokenRevokedError:
        return HTMLResponse(
            content=_beta_signup_error_html("This registration code is no longer valid."),
            status_code=400
        )

    # Store validated state in cookie (code only, no email yet)
    initial_credit_cents = token_data.get("initial_credit_cents", 0)
    ttl_days = token_data.get("ttl_days")
    serializer = _get_cookie_serializer()
    signup_state = serializer.dumps({
        "code": code,
        "initial_credit_cents": initial_credit_cents,
        "ttl_days": ttl_days,
        "validated_at": time.time(),
    })

    # Return auth method choice page with cookie
    response = HTMLResponse(content=_signup_choice_html(), status_code=200)
    response.set_cookie(
        key="signup_state",
        value=signup_state,
        max_age=600,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return response


# @PRIVATE
@mcp.custom_route("/signup-password", methods=["GET"])
async def signup_password_form(request: Request) -> HTMLResponse:
    """Show email/password signup form.

    Registration code already validated, stored in cookie.
    Now collect email and password.
    """
    from starlette.responses import HTMLResponse

    # Verify signup state cookie exists
    signup_cookie = request.cookies.get("signup_state")
    if not signup_cookie:
        return HTMLResponse(
            content=_beta_signup_error_html("Session expired. Please start over."),
            status_code=400
        )

    try:
        serializer = _get_cookie_serializer()
        serializer.loads(signup_cookie, max_age=600)  # Just validate, don't need data
    except Exception:
        return HTMLResponse(
            content=_beta_signup_error_html("Session expired. Please start over."),
            status_code=400
        )

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Create Account - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 420px;
            margin: 60px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 40px 32px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 { color: #1a1a2e; margin: 0 0 8px; font-size: 24px; text-align: center; }
        .subtitle { color: #666; text-align: center; margin-bottom: 24px; font-size: 14px; }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 500;
            color: #333;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 16px;
        }
        input:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        button {
            width: 100%;
            padding: 14px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #4f46e5; }
        .optional { color: #999; font-weight: normal; font-size: 13px; }
        .back-link { text-align: center; margin-top: 16px; font-size: 14px; }
        .back-link a { color: #6366f1; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Create Your Account</h1>
        <p class="subtitle">Enter your email to get started</p>
        <form method="POST" action="/signup-password">
            <label for="email">Email address</label>
            <input type="email" id="email" name="email" required placeholder="you@example.com" autofocus>

            <label for="name">Name <span class="optional">(optional)</span></label>
            <input type="text" id="name" name="name" placeholder="Your name">

            <button type="submit">Create Account</button>
        </form>
        <p class="back-link"><a href="/beta-signup">← Back to sign in options</a></p>
    </div>
</body>
</html>"""

    return HTMLResponse(content=html)


# @PRIVATE
@mcp.custom_route("/signup-password", methods=["POST"])
async def signup_password(request: Request) -> HTMLResponse:
    """Complete signup with password authentication.

    Reads code from cookie, email/name from form. Creates Vikunja account.
    """
    from starlette.responses import HTMLResponse
    from html import escape

    # Read and validate signup state cookie (has code, not email)
    signup_cookie = request.cookies.get("signup_state")
    if not signup_cookie:
        return HTMLResponse(
            content=_beta_signup_error_html("Session expired. Please start over."),
            status_code=400
        )

    try:
        serializer = _get_cookie_serializer()
        signup_data = serializer.loads(signup_cookie, max_age=600)
    except Exception as e:
        logger.warning(f"Signup-password: Invalid cookie: {e}")
        return HTMLResponse(
            content=_beta_signup_error_html("Session expired or invalid. Please start over."),
            status_code=400
        )

    code = signup_data["code"]
    initial_credit_cents = signup_data.get("initial_credit_cents", 0)
    ttl_days = signup_data.get("ttl_days")

    # Get email/name from form
    form = await request.form()
    email = form.get("email", "").strip().lower()
    name = form.get("name", "").strip()

    if not email or "@" not in email:
        return HTMLResponse(
            content=_beta_signup_error_html("Please provide a valid email address."),
            status_code=400
        )

    # Register user in factumerit_users table
    username = email.split("@")[0].replace(".", "_").replace("+", "_")[:50]
    user_id = f"vikunja:{username}"
    try:
        from .token_broker import register_user
        register_user(user_id, platform="vikunja", email=email, registered_via="beta_signup")
        logger.info(f"Signup-password: User {user_id} registered in factumerit_users table")
    except Exception as e:
        logger.error(f"Signup-password: Failed to register user: {e}")
        return HTMLResponse(
            content=_beta_signup_error_html("Account setup failed. Please contact support."),
            status_code=500
        )

    # Create wallet with initial credit from token
    try:
        from .budget_service import ensure_user_budget
        ensure_user_budget(user_id, initial_credit_cents=initial_credit_cents, promo_ttl_days=ttl_days)
        ttl_note = f" (expires in {ttl_days} days)" if ttl_days else ""
        logger.info(f"Signup-password: Wallet created for {user_id} with ${initial_credit_cents/100:.2f} credit{ttl_note}")
    except Exception as e:
        logger.error(f"Signup-password: Failed to create wallet: {e}")
        # Non-fatal - wallet can be created later on first API call

    # Record token usage
    from .registration_tokens import record_token_usage
    try:
        record_token_usage(code, email)
        logger.info(f"Signup-password: Token usage recorded for {code}/{email}")
    except Exception as e:
        logger.error(f"Signup-password: Failed to record token usage: {e}")
        return HTMLResponse(
            content=_beta_signup_error_html("Failed to record signup. Please contact support."),
            status_code=500
        )

    # Run signup workflow with generated password
    from .signup_workflow import SignupWorkflow
    import secrets

    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    password = secrets.token_urlsafe(12)

    workflow = SignupWorkflow(vikunja_url)

    try:
        state = workflow.run_full_workflow(
            email=email,
            username=username,
            registration_code=code,
            password=password
        )
    except Exception as e:
        logger.error(f"Signup-password: Workflow failed: {e}")
        return HTMLResponse(
            content=_beta_signup_error_html(
                "Account partially created. You should receive a password reset email. "
                "If not, please contact support with your email address."
            ),
            status_code=500
        )

    # Store bot credentials if provisioned
    if state.bot_credentials:
        try:
            from .bot_provisioning import store_bot_credentials
            store_bot_credentials(
                user_id,
                state.bot_credentials,
                owner_vikunja_user_id=state.vikunja_user_id,
                owner_vikunja_token=state.vikunja_jwt_token
            )
            logger.info(f"Signup-password: Bot credentials stored for {user_id}")
        except Exception as e:
            logger.warning(f"Signup-password: Failed to store bot credentials: {e}")

    # Clear signup cookie and show success page
    safe_email = escape(email)
    bot_username = state.bot_credentials.username if state.bot_credentials else None
    response = HTMLResponse(content=_beta_signup_success_html(safe_email, vikunja_url, bot_username))
    response.delete_cookie("signup_state", path="/")
    return response


# @PRIVATE
@mcp.custom_route("/signup-google", methods=["GET"])
async def signup_google(request: Request):
    """Complete signup with Google authentication.

    Auto-redirects to Google OAuth. Email/name come from Google, not from form.
    Cookie carries registration code for post-OAuth onboarding.
    Bead: fa-8g1r
    """
    from starlette.responses import HTMLResponse

    # Read and validate signup state cookie (contains code, not email)
    signup_cookie = request.cookies.get("signup_state")
    if not signup_cookie:
        return HTMLResponse(
            content=_beta_signup_error_html("Session expired. Please start over."),
            status_code=400
        )

    try:
        serializer = _get_cookie_serializer()
        signup_data = serializer.loads(signup_cookie, max_age=600)
    except Exception as e:
        logger.warning(f"Signup-google: Invalid cookie: {e}")
        return HTMLResponse(
            content=_beta_signup_error_html("Session expired or invalid. Please start over."),
            status_code=400
        )

    code = signup_data["code"]
    initial_credit_cents = signup_data.get("initial_credit_cents", 0)
    ttl_days = signup_data.get("ttl_days")

    logger.info(f"Signup-google: Setting up OIDC redirect for code {code}")

    # Generate token_validated cookie for nginx OIDC gating
    # Email will come from Google OAuth, not from form
    token_cookie_serializer = _get_cookie_serializer()
    token_validated_value = token_cookie_serializer.dumps({
        "validated": True,
        "token": code,
        "initial_credit_cents": initial_credit_cents,
        "ttl_days": ttl_days,
        "timestamp": time.time(),
    })

    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    login_url = f"{vikunja_url}/login?redirectToProvider=true"

    # Auto-redirect page - no email to display since Google provides it
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Redirecting to Google - Factumerit</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .card {{ background: white; padding: 40px; border-radius: 16px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; }}
        h2 {{ margin: 0 0 16px; color: #333; }}
        .spinner {{ width: 40px; height: 40px; border: 3px solid #e0e0e0; border-top-color: #4285f4; border-radius: 50%; animation: spin 1s linear infinite; margin: 20px auto; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        .note {{ font-size: 14px; color: #666; margin-bottom: 8px; }}
        .fallback {{ margin-top: 16px; font-size: 12px; color: #999; }}
        .fallback a {{ color: #4285f4; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>Connecting to Google...</h2>
        <div class="spinner"></div>
        <p class="note">You'll sign in with your Google account</p>
        <p class="fallback">Not redirecting? <a href="{login_url}">Click here</a></p>
    </div>
    <script>
        setTimeout(function() {{
            window.location.href = "{login_url}";
        }}, 500);
    </script>
</body>
</html>"""

    response = HTMLResponse(content=html, status_code=200)

    # Set token_validated cookie for nginx to allow OIDC registration
    response.set_cookie(
        key="token_validated",
        value=token_validated_value,
        max_age=300,
        httponly=True,
        secure=True,
        samesite="lax",
        domain=".factumerit.app",
        path="/",
    )

    return response


# @PRIVATE
def _signup_choice_html() -> str:
    """Auth method choice page after code validation."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create Account - Factumerit</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 420px;
            margin: 60px auto;
            padding: 20px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 40px 32px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .logo { font-size: 48px; margin-bottom: 8px; }
        h1 { font-size: 24px; margin: 0 0 8px; color: #1a1a1a; }
        .subtitle { color: #666; margin-bottom: 28px; font-size: 15px; }
        .success-badge {
            display: inline-block;
            background: #d4edda;
            color: #155724;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 24px;
        }
        .divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
            color: #999;
            font-size: 13px;
        }
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid #e5e5e5;
        }
        .divider span { padding: 0 12px; }
        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            padding: 14px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            border: none;
        }
        .btn-google {
            background: #4285f4;
            color: white;
        }
        .btn-google:hover { background: #3367d6; }
        .btn-password {
            background: #f5f5f5;
            color: #333;
            border: 1px solid #ddd;
        }
        .btn-password:hover { background: #e8e8e8; }
        .btn svg { width: 20px; height: 20px; }
        .option {
            margin-bottom: 12px;
        }
        .option-desc {
            margin-top: 6px;
            font-size: 12px;
            color: #888;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">&#10024;</div>
        <h1>Choose How to Sign In</h1>
        <div class="success-badge">&#10003; Code accepted</div>

        <div class="option">
            <a href="/signup-google" class="btn btn-google">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#fff"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#fff"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#fff"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#fff"/>
                </svg>
                Continue with Google
            </a>
            <p class="option-desc">Recommended - quick and secure</p>
        </div>

        <div class="divider"><span>or</span></div>

        <div class="option">
            <a href="/signup-password" class="btn btn-password">
                Continue with Email
            </a>
            <p class="option-desc">Create account with email &amp; password</p>
        </div>
    </div>
</body>
</html>"""


# @PRIVATE
def _signup_google_page_html(vikunja_url: str, bot_url: str, code: str, email: str) -> str:
    """Popup-based Google OIDC signup page.

    Opens Vikunja OIDC in popup, waits for completion, runs onboarding.
    Bead: fa-8g1r
    """
    from html import escape
    safe_code = escape(code)
    safe_email = escape(email)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In with Google - Factumerit</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 420px;
            margin: 60px auto;
            padding: 20px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 40px 32px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .logo {{ font-size: 48px; margin-bottom: 8px; }}
        h1 {{ font-size: 24px; margin: 0 0 8px; color: #1a1a1a; }}
        .subtitle {{ color: #666; margin-bottom: 24px; font-size: 14px; }}
        .status {{
            padding: 16px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 14px;
            line-height: 1.5;
        }}
        .status.pending {{ background: #fff3cd; color: #856404; }}
        .status.success {{ background: #d4edda; color: #155724; }}
        .status.error {{ background: #f8d7da; color: #721c24; }}
        .spinner {{
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #ccc;
            border-top-color: #333;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: #4285f4;
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 16px;
            transition: background 0.2s;
        }}
        .btn:hover {{ background: #3367d6; }}
        .btn:disabled {{ background: #ccc; cursor: not-allowed; }}
        .help {{ margin-top: 24px; font-size: 13px; color: #666; }}
        .help a {{ color: #6366f1; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">&#128640;</div>
        <h1>Signing in with Google</h1>
        <p class="subtitle">{safe_email}</p>

        <div id="status" class="status pending">
            <span class="spinner"></span>Opening Google sign-in...
        </div>

        <button id="retry-btn" class="btn" style="display: none;" onclick="startLogin()">
            Try Again
        </button>

        <div class="help" id="help" style="display: none;">
            <p>Popup blocked? <a href="#" onclick="startLogin(); return false;">Click here</a> to try again.</p>
        </div>
    </div>

    <script>
        const CONFIG = {{
            vikunjaUrl: '{vikunja_url}',
            botUrl: '{bot_url}',
            registrationToken: '{safe_code}',
            email: '{safe_email}',
            oidcPath: '/auth/openid/google',
            pollIntervalMs: 1500,
            pollTimeoutMs: 300000
        }};

        const statusEl = document.getElementById('status');
        const retryBtn = document.getElementById('retry-btn');
        const helpEl = document.getElementById('help');

        let popup = null;
        let pollInterval = null;

        function showStatus(msg, type = 'pending') {{
            const spinner = type === 'pending' ? '<span class="spinner"></span>' : '';
            statusEl.innerHTML = spinner + msg;
            statusEl.className = 'status ' + type;
        }}

        function showError(msg) {{
            showStatus(msg, 'error');
            retryBtn.style.display = 'inline-flex';
            helpEl.style.display = 'block';
        }}

        function showSuccess(msg) {{
            showStatus(msg, 'success');
        }}

        async function checkAuth() {{
            const jwt = localStorage.getItem('token');
            if (!jwt) return null;
            try {{
                const resp = await fetch(CONFIG.vikunjaUrl + '/api/v1/user', {{
                    headers: {{ 'Authorization': 'Bearer ' + jwt }}
                }});
                if (!resp.ok) {{
                    localStorage.removeItem('token');
                    return null;
                }}
                return await resp.json();
            }} catch (e) {{
                localStorage.removeItem('token');
                return null;
            }}
        }}

        async function runOnboarding(user, jwt) {{
            showStatus('Setting up your account...');
            try {{
                const resp = await fetch(CONFIG.botUrl + '/oidc-onboard', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        jwt: jwt,
                        email: user.email || CONFIG.email,
                        username: user.username,
                        registration_token: CONFIG.registrationToken
                    }})
                }});
                const data = await resp.json();
                if (!resp.ok) console.error('Onboarding failed:', data);
                return data;
            }} catch (e) {{
                console.error('Onboarding error:', e);
                return {{ success: false, error: e.message }};
            }}
        }}

        async function completeRegistration(user) {{
            const jwt = localStorage.getItem('token');
            const result = await runOnboarding(user, jwt);
            if (result && result.existing_user) {{
                showSuccess('Welcome back! Redirecting to your account...');
            }} else {{
                showSuccess('Account created! Redirecting...');
            }}
            setTimeout(() => {{
                window.location.href = CONFIG.vikunjaUrl + '/';
            }}, 1500);
        }}

        function startLogin() {{
            retryBtn.style.display = 'none';
            showStatus('Opening Google sign-in...');
            localStorage.removeItem('token');

            popup = window.open(
                CONFIG.vikunjaUrl + CONFIG.oidcPath,
                'auth-popup',
                'width=500,height=650,menubar=no,toolbar=no'
            );

            if (!popup || popup.closed) {{
                showError('Popup was blocked. Please allow popups for this site.');
                return;
            }}

            const startTime = Date.now();
            pollInterval = setInterval(async () => {{
                if (Date.now() - startTime > CONFIG.pollTimeoutMs) {{
                    clearInterval(pollInterval);
                    showError('Sign-in timed out. Please try again.');
                    return;
                }}
                if (popup.closed) {{
                    const user = await checkAuth();
                    if (!user) {{
                        clearInterval(pollInterval);
                        showError('Sign-in cancelled. Click below to try again.');
                        return;
                    }}
                }}
                const user = await checkAuth();
                if (user) {{
                    clearInterval(pollInterval);
                    if (popup && !popup.closed) popup.close();
                    await completeRegistration(user);
                }}
            }}, CONFIG.pollIntervalMs);

            showStatus('Waiting for Google sign-in...');
            helpEl.style.display = 'block';
        }}

        startLogin();
    </script>
</body>
</html>"""


# @PRIVATE
def _beta_signup_success_html(email: str, vikunja_url: str, bot_username: str = None) -> str:
    """Success page after beta signup."""

    # Bot info section (if bot was provisioned)
    bot_info_html = ""
    if bot_username:
        bot_info_html = """
    <div class="next-steps" style="background: #fef3c7; border-left: 4px solid #f59e0b;">
        <h3>🤖 Your AI Assistant</h3>
        <p>Mention <strong style="font-family: monospace; color: #0284c7;">@eis</strong> in any task to get AI help.</p>
        <p style="font-size: 14px; margin-top: 12px;"><strong>⚡ One more step:</strong> After logging in, check your Inbox for a welcome task with an activation link. Click it to connect your bot!</p>
    </div>
"""
    else:
        # Bot provisioning failed - show manual setup instructions
        bot_info_html = f"""
    <div class="next-steps" style="background: #fef3c7; border-left: 4px solid #f59e0b;">
        <h3>⚠️ AI Assistant Setup (Manual Step Required)</h3>
        <p style="font-size: 14px; margin-bottom: 12px;">Your AI assistant couldn't be set up automatically. You can enable it manually:</p>
        <ol style="font-size: 14px; text-align: left; line-height: 1.8;">
            <li>Log in to <a href="{vikunja_url}" style="color: #0284c7;">Vikunja</a></li>
            <li>Go to <strong>Settings → API Tokens</strong></li>
            <li>Click <strong>"Create new token"</strong></li>
            <li>Copy the token and contact support to link it to your bot</li>
        </ol>
        <p style="font-size: 13px; color: #92400e; margin-top: 12px;">
            <em>We're working on automating this step. For now, you can still use Vikunja normally!</em>
        </p>
    </div>
"""

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Factumerit!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 80px auto;
            padding: 20px;
            text-align: center;
        }}
        .emoji {{ font-size: 48px; margin-bottom: 16px; }}
        h1 {{ color: #059669; margin-bottom: 8px; }}
        p {{ color: #666; line-height: 1.6; }}
        .email {{ font-weight: 600; color: #333; }}
        .button {{
            display: inline-block;
            margin-top: 20px;
            padding: 14px 28px;
            background: #6366f1;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
        }}
        .button:hover {{ background: #4f46e5; }}
        .next-steps {{
            text-align: left;
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 24px;
        }}
        .next-steps h3 {{ margin-top: 0; }}
        .next-steps ol {{ padding-left: 20px; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="emoji">✅</div>
    <h1>Account Created!</h1>
    <p>Account created for <span class="email">{email}</span></p>

    <div class="next-steps">
        <h3>Check Your Email</h3>
        <p style="margin-bottom: 12px;">We sent your login credentials to:</p>
        <p style="font-size: 18px; font-weight: 600; color: #333; margin: 16px 0;">{email}</p>
        <p style="font-size: 14px; color: #666;">
            Your password is in the email. Can't find it? Check your spam folder.
        </p>
    </div>

{bot_info_html}
    <a href="{vikunja_url}" class="button">Go to Login</a>
</body>
</html>"""


# @PRIVATE
def _beta_signup_error_html(message: str) -> str:
    """Error page for beta signup failures."""
    import html
    escaped_message = html.escape(message)
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Signup Error - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 80px auto;
            padding: 20px;
            text-align: center;
        }}
        h1 {{ color: #dc2626; }}
        p {{ color: #666; }}
        a {{ color: #6366f1; }}
    </style>
</head>
<body>
    <h1>Signup Error</h1>
    <p>{escaped_message}</p>
    <p><a href="/beta-signup">← Try again</a></p>
</body>
</html>"""


# ============================================================================
# BOT ACTIVATION (Deferred bot sharing after signup)
# ============================================================================
# Bead: solutions-vykv
#
# Flow:
# 1. User signs up → bot provisioned but NOT shared with Inbox
# 2. User logs in → sees welcome task with activation link
# 3. User clicks link → /activate-bot shares Inbox with bot
# 4. Bot can now monitor Inbox and respond to @mentions
#
# Why deferred?
# - Avoids database replication race conditions during signup
# - User can retry if activation fails
# - Easier to debug sharing issues in isolation


# @PRIVATE
def _create_api_token_for_user(owner_jwt: str, vikunja_url: str) -> str | None:
    """Create a Vikunja API token for Claude Desktop using the owner's JWT.

    Returns the API token string, or None if creation fails.
    """
    from datetime import datetime, timedelta

    try:
        # First, get available permissions from /api/v1/routes
        routes_resp = requests.get(
            f"{vikunja_url}/api/v1/routes",
            headers={"Authorization": f"Bearer {owner_jwt}"},
            timeout=30
        )
        routes_resp.raise_for_status()
        routes = routes_resp.json()

        # Build permissions dict from available routes (all permissions)
        permissions = {}
        for group, group_routes in routes.items():
            if isinstance(group_routes, dict):
                permissions[group] = list(group_routes.keys())

        # Set expiry to 1 year
        expiry_date = datetime.now() + timedelta(days=365)
        token_title = f"Claude Desktop ({datetime.now().strftime('%Y-%m-%d')})"

        # Vikunja API uses PUT for token creation
        token_resp = requests.put(
            f"{vikunja_url}/api/v1/tokens",
            headers={"Authorization": f"Bearer {owner_jwt}"},
            json={
                "title": token_title,
                "expires_at": expiry_date.isoformat() + "Z",
                "permissions": permissions
            },
            timeout=30
        )
        token_resp.raise_for_status()
        token_data = token_resp.json()
        return token_data.get("token")

    except Exception as e:
        logger.error(f"Failed to create API token: {e}")
        return None


# @PRIVATE
def _create_welcome_task(
    vikunja_url: str,
    inbox_id: int,
) -> bool:
    """Create a welcome task in the user's Inbox pointing to setup email.

    Uses VIKUNJA_BOT_TOKEN (@eis bot credentials) since the Inbox was just
    shared with @eis. The API token is NOT included here for security -
    it's only in the email.

    Returns True if task was created successfully.
    """
    # Simple welcome message - token is in the email for security
    description = """<h2>🎉 Your AI assistant is ready!</h2>

<p>Check your email for <strong>Claude Desktop setup instructions</strong> with your personal API token.</p>

<p>Once connected, you can ask Claude things like:</p>
<ul>
<li><em>"What's on my todo list?"</em></li>
<li><em>"Add a task to buy groceries tomorrow"</em></li>
<li><em>"What are my high priority tasks?"</em></li>
</ul>

<hr>

<p>📖 <a href="https://github.com/ivantohelpyou/vikunja-mcp">Full documentation</a></p>
"""

    try:
        logger.info(f"Creating welcome task in Inbox {inbox_id} via middleware...")

        task_resp = requests.post(
            f"{vikunja_url}/internal/create-task",
            json={
                "project_id": inbox_id,
                "title": "🎉 Your AI assistant is ready!",
                "description": description,
                "priority": 3,  # High priority so it's visible
            },
            timeout=30
        )

        if task_resp.status_code >= 400:
            logger.error(f"Task creation HTTP {task_resp.status_code}: {task_resp.text[:500]}")

        task_resp.raise_for_status()
        result = task_resp.json()
        logger.info(f"Created welcome task {result.get('task_id')} in Inbox {inbox_id}")
        return True

    except requests.exceptions.HTTPError as e:
        resp_text = e.response.text[:500] if e.response else 'no response body'
        logger.error(f"Failed to create welcome task: {e} - Response: {resp_text}")
        return False
    except Exception as e:
        logger.error(f"Failed to create welcome task (unexpected): {e}")
        return False


# @PRIVATE
@mcp.custom_route("/activate-bot", methods=["GET"])
async def activate_bot(request: Request) -> HTMLResponse:
    """Activate AI assistant for a user - shares Inbox with bot.

    This endpoint is called from the welcome task activation link.
    It handles bot-to-Inbox sharing with retries to handle database replication lag.
    """
    from starlette.responses import HTMLResponse
    import time

    username = request.query_params.get("user", "").strip()

    if not username:
        return HTMLResponse(
            content=_activation_error_html("Missing user parameter."),
            status_code=400
        )

    user_id = f"vikunja:{username}"

    # Get bot credentials (username + password for JWT login)
    try:
        from .bot_provisioning import get_user_bot_credentials, get_bot_owner_token
        logger.info(f"Bot activation: Looking up bot credentials for {user_id}")
        bot_creds_tuple = get_user_bot_credentials(user_id)

        if not bot_creds_tuple:
            logger.error(f"Bot activation: No bot found in database for {user_id}")
            return HTMLResponse(
                content=_activation_error_html("Bot not found. Please contact support."),
                status_code=404
            )

        bot_username, bot_password = bot_creds_tuple  # (username, password) tuple
        logger.info(f"Bot activation: Found bot {bot_username} for {user_id}")
    except Exception as e:
        logger.error(f"Bot activation: Failed to get bot credentials for {user_id}: {e}")
        return HTMLResponse(
            content=_activation_error_html(f"Failed to retrieve bot credentials: {str(e)}"),
            status_code=500
        )

    # Get bot and owner Vikunja user IDs from database
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    try:
        from .bot_provisioning import get_user_bot_vikunja_id, get_bot_owner_vikunja_id, get_bot_owner_token

        # Get bot's Vikunja user ID
        bot_vikunja_id = get_user_bot_vikunja_id(user_id)
        if not bot_vikunja_id:
            logger.error(f"Bot activation: No bot found for {user_id}")
            return HTMLResponse(
                content=_activation_error_html("Bot not found. Please contact support."),
                status_code=404
            )

        # Get owner's Vikunja user ID
        owner_vikunja_id = get_bot_owner_vikunja_id(user_id)

        # Get owner's JWT token
        owner_jwt = get_bot_owner_token(user_id)
        if not owner_jwt:
            logger.error(f"Bot activation: No owner JWT token found for {user_id}")
            return HTMLResponse(
                content=_activation_error_html("Owner token not found. Please contact support."),
                status_code=404
            )

        logger.info(f"Bot activation: bot_id={bot_vikunja_id}, owner_id={owner_vikunja_id}")

    except Exception as e:
        logger.error(f"Bot activation: Failed to get bot metadata: {e}")
        return HTMLResponse(
            content=_activation_error_html(f"Failed to retrieve bot metadata: {str(e)}"),
            status_code=500
        )

    # Find owner's Inbox using their JWT token
    inbox_id = None
    try:
        logger.info(f"Bot activation: Getting owner's projects to find Inbox")
        projects_resp = requests.get(
            f"{vikunja_url}/api/v1/projects",
            headers={"Authorization": f"Bearer {owner_jwt}"},
            timeout=10
        )

        if projects_resp.status_code == 200:
            projects = projects_resp.json()
            inbox = next((p for p in projects if p.get("title") == "Inbox"), None)

            if inbox:
                inbox_id = inbox.get("id")
                logger.info(f"Bot activation: Found Inbox (id={inbox_id})")
            else:
                logger.error(f"Bot activation: No Inbox found in projects")
        else:
            logger.error(f"Bot activation: Failed to get projects: {projects_resp.status_code}")
    except Exception as e:
        logger.error(f"Bot activation: Exception getting projects: {e}")

    if not inbox_id:
        return HTMLResponse(
            content=_activation_error_html("Could not find Inbox. Please contact support."),
            status_code=404
        )

    # Dispatcher model: Share Inbox with @eis (central bot), not personal bot
    # Users @mention @eis, personal bot credentials used behind the scenes
    # Look up @eis user ID first
    eis_vikunja_id = None
    try:
        logger.info(f"Bot activation: Looking up @eis user ID")
        users_resp = requests.get(
            f"{vikunja_url}/api/v1/users",
            headers={"Authorization": f"Bearer {owner_jwt}"},
            params={"s": "eis"},
            timeout=10
        )
        if users_resp.status_code == 200:
            users = users_resp.json()
            eis_user = next((u for u in users if u.get("username") == "eis"), None)
            if eis_user:
                eis_vikunja_id = eis_user.get("id")
                logger.info(f"Bot activation: Found @eis user (id={eis_vikunja_id})")
            else:
                logger.warning(f"Bot activation: @eis user not found in search results")
        else:
            logger.warning(f"Bot activation: Failed to search users: {users_resp.status_code}")
    except Exception as e:
        logger.warning(f"Bot activation: Failed to look up @eis: {e}")

    if not eis_vikunja_id:
        logger.error(f"Bot activation: Could not find @eis user ID")
        return HTMLResponse(
            content=_activation_error_html("Could not find @eis bot. Please contact support."),
            status_code=500
        )

    # Share Inbox with @eis via middleware (spinal tap: direct DB INSERT)
    try:
        logger.info(f"Bot activation: Sharing project {inbox_id} with @eis (id={eis_vikunja_id}) via middleware")

        share_resp = requests.post(
            f"{vikunja_url}/internal/share-project",
            json={
                "project_id": inbox_id,
                "user_id": eis_vikunja_id,  # Share with @eis for dispatcher model
                "permission": 1  # Read & Write (0=read, 1=read/write, 2=admin)
            },
            timeout=10
        )

        logger.info(f"Bot activation: Middleware response {share_resp.status_code}: {share_resp.text[:500]}")

        if share_resp.status_code == 200:
            logger.info(f"Bot activation: ✓ SUCCESS! Inbox shared with @eis via middleware")

            # Generate API token for Claude Desktop and send config email + create task
            api_token = _create_api_token_for_user(owner_jwt, vikunja_url)
            if api_token:
                logger.info(f"Bot activation: Created API token for {user_id}")

                # Send Claude config email (bypasses WAF, permanent reference)
                from .bot_provisioning import get_user_email
                from .email_service import send_claude_config_email
                user_email = get_user_email(user_id)
                if user_email:
                    email_result = send_claude_config_email(
                        to_email=user_email,
                        api_token=api_token,
                        vikunja_url=vikunja_url,
                        user_name=username,
                    )
                    if email_result.success:
                        logger.info(f"Bot activation: Sent Claude config email to {user_email}")
                    else:
                        logger.warning(f"Bot activation: Failed to send config email: {email_result.error}")
                else:
                    logger.warning(f"Bot activation: No email found for {user_id}, skipping config email")

                # Also create welcome task pointing to the email
                task_created = _create_welcome_task(vikunja_url, inbox_id)
                if task_created:
                    logger.info(f"Bot activation: Created welcome task")
                else:
                    logger.warning(f"Bot activation: Failed to create welcome task (non-fatal)")
            else:
                logger.warning(f"Bot activation: Failed to create API token (non-fatal)")

            return HTMLResponse(
                content=_activation_success_html(bot_username),
                status_code=200
            )
        else:
            logger.error(f"Bot activation: Middleware sharing failed: {share_resp.status_code} - {share_resp.text}")
            return HTMLResponse(
                content=_activation_error_html(f"Failed to share Inbox (middleware error: {share_resp.status_code})"),
                status_code=500
            )

    except Exception as e:
        logger.error(f"Bot activation: Exception calling middleware: {e}")
        return HTMLResponse(
            content=_activation_error_html(f"Failed to activate bot: {str(e)}"),
            status_code=500
        )


# @PRIVATE
def _activation_smoke_test_html(username: str, bot_username: str, bot_vikunja_id: int, owner_vikunja_id: int, inbox_id: int) -> str:
    """Smoke test page showing database lookup results."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Smoke Test - Bot Activation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 80px auto;
            padding: 20px;
        }}
        .emoji {{ font-size: 48px; margin-bottom: 16px; text-align: center; }}
        h1 {{ color: #059669; margin-bottom: 8px; text-align: center; }}
        .subtitle {{ color: #666; text-align: center; margin-bottom: 32px; }}
        .data-table {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .data-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #ddd;
        }}
        .data-row:last-child {{ border-bottom: none; }}
        .data-label {{
            font-weight: 600;
            color: #333;
        }}
        .data-value {{
            font-family: monospace;
            color: #0284c7;
            background: #e0f2fe;
            padding: 4px 12px;
            border-radius: 4px;
        }}
        .success-badge {{
            background: #059669;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin: 20px auto;
            text-align: center;
        }}
        .note {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 16px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .note strong {{ color: #92400e; }}
    </style>
</head>
<body>
    <div class="emoji">🔬</div>
    <h1>Smoke Test Passed!</h1>
    <p class="subtitle">Database connectivity verified</p>

    <div class="success-badge">✓ Database Lookup Successful</div>

    <div class="data-table">
        <div class="data-row">
            <span class="data-label">Username:</span>
            <span class="data-value">{username}</span>
        </div>
        <div class="data-row">
            <span class="data-label">Bot Username:</span>
            <span class="data-value">@{bot_username}</span>
        </div>
        <div class="data-row">
            <span class="data-label">Bot Vikunja ID:</span>
            <span class="data-value">{bot_vikunja_id}</span>
        </div>
        <div class="data-row">
            <span class="data-label">Owner Vikunja ID:</span>
            <span class="data-value">{owner_vikunja_id}</span>
        </div>
        <div class="data-row">
            <span class="data-label">Inbox Project ID:</span>
            <span class="data-value">{inbox_id}</span>
        </div>
    </div>

    <div class="note">
        <strong>⚠️ Note:</strong> This is a smoke test. The actual sharing operation is currently disabled.
        All data shown above was successfully retrieved from the database, proving connectivity works.
    </div>

    <p style="text-align: center; color: #666; margin-top: 32px;">
        Next step: Test the middleware /internal/share-project endpoint
    </p>
</body>
</html>"""


# @PRIVATE
def _activation_success_html(bot_username: str) -> str:
    """Minimal success page after bot activation.

    Full instructions are in the welcome task - this page just confirms success.
    """
    return """<!DOCTYPE html>
<html>
<head>
    <title>Activated!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            text-align: center;
        }
        .emoji { font-size: 64px; margin-bottom: 16px; }
        h1 { color: #059669; margin-bottom: 8px; }
        p { color: #666; }
    </style>
</head>
<body>
    <div class="emoji">✓</div>
    <h1>Activated!</h1>
    <p>Check your <strong>Inbox</strong> for setup instructions.</p>
    <p style="font-size: 13px; color: #9ca3af; margin-top: 20px;">
        You can close this tab.
    </p>
</body>
</html>"""


# @PRIVATE
def _activation_error_html(message: str) -> str:
    """Error page for bot activation failures."""
    import html
    escaped_message = html.escape(message)
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Activation Error - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 80px auto;
            padding: 20px;
            text-align: center;
        }}
        .emoji {{ font-size: 48px; margin-bottom: 16px; }}
        h1 {{ color: #dc2626; margin-bottom: 8px; }}
        p {{ color: #666; line-height: 1.6; }}
        .error-message {{
            background: #fee2e2;
            border-left: 4px solid #dc2626;
            padding: 16px;
            border-radius: 8px;
            margin: 24px 0;
            text-align: left;
        }}
        .button {{
            display: inline-block;
            margin-top: 20px;
            padding: 14px 28px;
            background: #6366f1;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
        }}
        .button:hover {{ background: #4f46e5; }}
    </style>
</head>
<body>
    <div class="emoji">⚠️</div>
    <h1>Activation Failed</h1>
    <div class="error-message">
        <p>{escaped_message}</p>
    </div>
    <p>Please try again or contact support at <a href="mailto:support@factumerit.app">support@factumerit.app</a></p>
    <a href="javascript:location.reload()" class="button">Try Again</a>
</body>
</html>"""


# ============================================================================
# GOOGLE OIDC TOKEN-GATED REGISTRATION
# ============================================================================
# Bead: solutions-l0u9.10
# Design doc: docs/factumerit/094-GOOGLE_OIDC_TOKEN_GATING.md
#
# Flow:
# 1. User visits /auth-register?token=XXX
# 2. Bot validates token, sets signed cookie
# 3. Redirect to vikunja.factumerit.app/login
# 4. User clicks "Login with Google"
# 5. Google redirects to callback → nginx checks for cookie
# 6. Cookie present → account created; missing → 403 blocked

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Cookie signing secret (must be set in environment)
COOKIE_SIGNING_SECRET = os.environ.get("COOKIE_SIGNING_SECRET", "")

# Initialize serializer lazily (only if secret is set)
_cookie_serializer: URLSafeTimedSerializer | None = None


# @PRIVATE
def _get_cookie_serializer() -> URLSafeTimedSerializer:
    """Get or create the cookie serializer."""
    global _cookie_serializer
    if _cookie_serializer is None:
        if not COOKIE_SIGNING_SECRET:
            raise RuntimeError("COOKIE_SIGNING_SECRET not set - cannot sign cookies")
        _cookie_serializer = URLSafeTimedSerializer(COOKIE_SIGNING_SECRET)
    return _cookie_serializer


# @PRIVATE
@mcp.custom_route("/auth-register", methods=["GET"])
async def auth_register(request: Request):
    """Token-gated registration endpoint for Google OIDC flow.

    Validates registration token and sets a signed cookie that nginx
    checks before allowing the OIDC callback to proceed.

    Query params:
        token: Registration token (e.g., NSA-NORTHWEST-50)

    Returns:
        Redirect to Vikunja login page with cookie set
    """
    from starlette.responses import RedirectResponse, HTMLResponse

    token = request.query_params.get("token", "").strip().upper()

    # Validate token is provided
    if not token:
        return HTMLResponse(
            content=_auth_register_error_html("Registration code is required."),
            status_code=400
        )

    # Check if cookie signing is configured
    if not COOKIE_SIGNING_SECRET:
        logger.error("COOKIE_SIGNING_SECRET not set - auth-register disabled")
        return HTMLResponse(
            content=_auth_register_error_html("Registration system not configured. Please contact support."),
            status_code=500
        )

    # Import registration token validation
    from .registration_tokens import (
        validate_registration_token,
        record_token_usage,
        TokenNotFoundError,
        TokenExhaustedError,
        TokenExpiredError,
        TokenRevokedError,
    )

    try:
        # Validate the token (using a placeholder user_id for now)
        # Note: We don't know the user's email yet - they haven't logged in with Google
        # We'll use "pending" as placeholder; duplicate check will happen on account creation
        token_data = validate_registration_token(token, user_id="pending-oidc")

        # Token is valid - generate signed cookie value
        serializer = _get_cookie_serializer()
        cookie_value = serializer.dumps({
            "validated": True,
            "token": token,
            "timestamp": time.time(),
        })

        # Record token usage eagerly (before redirect)
        # This ensures the token count is decremented even if user abandons flow
        record_token_usage(token, user_id="pending-oidc")

        logger.info(f"Auth-register: Token '{token}' validated, showing registration page")

        # Return HTML page that handles popup-based OIDC flow with onboarding
        # Bead: fa-8g1r (Welcome message missing for Google Login users)
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        bot_url = os.environ.get("BOT_URL", "https://mcp.factumerit.app")

        html_content = _auth_register_page_html(vikunja_url, bot_url, token, cookie_value)
        response = HTMLResponse(content=html_content, status_code=200)

        # Set cookie with domain for cross-subdomain access
        # Domain must be .factumerit.app to work across subdomains
        response.set_cookie(
            key="token_validated",
            value=cookie_value,
            max_age=300,  # 5 minutes
            httponly=True,
            secure=True,
            samesite="lax",
            domain=".factumerit.app",
            path="/",
        )

        return response

    except TokenNotFoundError:
        return HTMLResponse(
            content=_auth_register_error_html(f"Registration code '{token}' not found."),
            status_code=404
        )
    except TokenExhaustedError:
        return HTMLResponse(
            content=_auth_register_error_html(f"Registration code '{token}' has been fully used."),
            status_code=403
        )
    except TokenExpiredError as e:
        return HTMLResponse(
            content=_auth_register_error_html(str(e)),
            status_code=403
        )
    except TokenRevokedError:
        return HTMLResponse(
            content=_auth_register_error_html(f"Registration code '{token}' has been revoked."),
            status_code=403
        )
    except Exception as e:
        logger.error(f"Auth-register error: {e}", exc_info=True)
        return HTMLResponse(
            content=_auth_register_error_html("An error occurred. Please try again."),
            status_code=500
        )


# @PRIVATE
def _auth_register_error_html(message: str) -> str:
    """Generate error page HTML for auth-register."""
    from html import escape
    escaped_message = escape(message)
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Registration Error - Factumerit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 480px;
            margin: 40px auto;
            padding: 20px;
            text-align: center;
        }}
        h1 {{ color: #dc2626; }}
        p {{ color: #666; line-height: 1.6; }}
        a {{ color: #6366f1; }}
        .help {{
            margin-top: 24px;
            padding: 16px;
            background: #f5f5f5;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <h1>Registration Error</h1>
    <p>{escaped_message}</p>
    <div class="help">
        <p>Need help? Contact your administrator for a valid registration code.</p>
        <p>Or try <a href="/beta-signup">password-based signup</a> instead.</p>
    </div>
</body>
</html>"""


# @PRIVATE
def _auth_register_page_html(vikunja_url: str, bot_url: str, token: str, cookie_value: str) -> str:
    """Generate HTML page for OIDC registration with popup flow.

    This page opens Vikunja login in a popup, waits for successful login,
    then calls /oidc-onboard to complete onboarding before redirecting.

    Bead: fa-8g1r (Welcome message missing for Google Login users)
    """
    from html import escape
    escaped_token = escape(token)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up - Factumerit</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 420px;
            margin: 60px auto;
            padding: 20px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 40px 32px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .logo {{
            font-size: 48px;
            margin-bottom: 8px;
        }}
        h1 {{
            font-size: 24px;
            margin: 0 0 8px;
            color: #1a1a1a;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 24px;
            font-size: 14px;
        }}
        .status {{
            padding: 16px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 14px;
            line-height: 1.5;
        }}
        .status.pending {{ background: #fff3cd; color: #856404; }}
        .status.success {{ background: #d4edda; color: #155724; }}
        .status.error {{ background: #f8d7da; color: #721c24; }}
        .spinner {{
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #ccc;
            border-top-color: #333;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: #4285f4;
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 16px;
            transition: background 0.2s;
        }}
        .btn:hover {{ background: #3367d6; }}
        .btn:disabled {{ background: #ccc; cursor: not-allowed; }}
        .btn svg {{
            width: 20px;
            height: 20px;
        }}
        .help {{
            margin-top: 24px;
            font-size: 13px;
            color: #666;
        }}
        .help a {{ color: #6366f1; }}
        .checkmark {{
            font-size: 48px;
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">&#128640;</div>
        <h1>Welcome to Factumerit</h1>
        <p class="subtitle">Your AI-powered task assistant</p>

        <div id="status" class="status pending" style="display: none;"></div>

        <button id="google-btn" class="btn" onclick="startLogin()">
            <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Continue with Google
        </button>

        <div class="help" id="help" style="display: none;">
            <p>Popup blocked? <a href="#" onclick="startLogin(); return false;">Click here</a> to try again.</p>
        </div>
    </div>

    <script>
        const CONFIG = {{
            vikunjaUrl: '{vikunja_url}',
            botUrl: '{bot_url}',
            registrationToken: '{escaped_token}',
            oidcPath: '/auth/openid/google',
            pollIntervalMs: 1500,
            pollTimeoutMs: 300000  // 5 minutes
        }};

        const statusEl = document.getElementById('status');
        const googleBtn = document.getElementById('google-btn');
        const helpEl = document.getElementById('help');

        let popup = null;
        let pollInterval = null;

        function showStatus(msg, type = 'pending') {{
            const spinner = type === 'pending' ? '<span class="spinner"></span>' : '';
            statusEl.innerHTML = spinner + msg;
            statusEl.className = 'status ' + type;
            statusEl.style.display = 'block';
        }}

        function showError(msg) {{
            showStatus(msg, 'error');
            googleBtn.disabled = false;
            googleBtn.textContent = 'Try Again';
            helpEl.style.display = 'block';
        }}

        function showSuccess(msg) {{
            showStatus(msg, 'success');
        }}

        // Check if user is logged in to Vikunja
        async function checkAuth() {{
            const jwt = localStorage.getItem('token');
            if (!jwt) return null;

            try {{
                const resp = await fetch(CONFIG.vikunjaUrl + '/api/v1/user', {{
                    headers: {{ 'Authorization': 'Bearer ' + jwt }}
                }});
                if (!resp.ok) {{
                    localStorage.removeItem('token');
                    return null;
                }}
                return await resp.json();
            }} catch (e) {{
                localStorage.removeItem('token');
                return null;
            }}
        }}

        // Run onboarding via bot endpoint
        async function runOnboarding(user, jwt) {{
            showStatus('Setting up your account...');

            try {{
                const resp = await fetch(CONFIG.botUrl + '/oidc-onboard', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        jwt: jwt,
                        email: user.email,
                        username: user.username,
                        registration_token: CONFIG.registrationToken
                    }})
                }});

                const data = await resp.json();

                if (!resp.ok) {{
                    console.error('Onboarding failed:', data);
                    // Continue anyway - user account exists
                }}

                return data;
            }} catch (e) {{
                console.error('Onboarding error:', e);
                // Continue anyway - user account exists
                return {{ success: false, error: e.message }};
            }}
        }}

        // Complete the registration flow
        async function completeRegistration(user) {{
            const jwt = localStorage.getItem('token');

            // Run onboarding
            const result = await runOnboarding(user, jwt);

            // Success! Show appropriate message based on whether user already existed
            if (result && result.existing_user) {{
                showSuccess('Welcome back! Redirecting to your account...');
            }} else {{
                showSuccess('Account created! Redirecting...');
            }}

            // Redirect to Vikunja dashboard
            setTimeout(() => {{
                window.location.href = CONFIG.vikunjaUrl + '/';
            }}, 1500);
        }}

        // Start Google login flow
        function startLogin() {{
            googleBtn.disabled = true;
            showStatus('Opening login window...');

            // Clear any existing session to prevent account mixups
            localStorage.removeItem('token');

            // Open Vikunja OIDC login in popup
            popup = window.open(
                CONFIG.vikunjaUrl + CONFIG.oidcPath,
                'auth-popup',
                'width=500,height=650,menubar=no,toolbar=no'
            );

            if (!popup || popup.closed) {{
                showError('Popup was blocked. Please allow popups for this site.');
                return;
            }}

            // Start polling for auth completion
            const startTime = Date.now();
            pollInterval = setInterval(async () => {{
                // Check timeout
                if (Date.now() - startTime > CONFIG.pollTimeoutMs) {{
                    clearInterval(pollInterval);
                    showError('Login timed out. Please try again.');
                    return;
                }}

                // Check if popup closed without completing
                if (popup.closed) {{
                    const user = await checkAuth();
                    if (!user) {{
                        clearInterval(pollInterval);
                        showError('Login cancelled. Click below to try again.');
                        return;
                    }}
                }}

                // Check for successful login
                const user = await checkAuth();
                if (user) {{
                    clearInterval(pollInterval);
                    if (popup && !popup.closed) popup.close();
                    await completeRegistration(user);
                }}
            }}, CONFIG.pollIntervalMs);

            showStatus('Waiting for login...');
            helpEl.style.display = 'block';
        }}

        // Auto-start on page load
        startLogin();
    </script>
</body>
</html>"""


# @PRIVATE
@mcp.custom_route("/oidc-onboard", methods=["POST"])
async def oidc_onboard(request: Request):
    """Complete onboarding for OIDC-registered users.

    Called by the registration page after user completes Google OIDC login.
    Runs the same onboarding stages as email registration.

    Bead: fa-8g1r (Welcome message missing for Google Login users)

    Expected JSON body:
        jwt: Vikunja JWT token (from localStorage after OIDC login)
        api_token: API token created by auth-bridge flow (optional)
        email: User's email (from Vikunja /user endpoint)
        username: User's Vikunja username
        registration_token: The registration token that was used

    Returns:
        JSON with success status and onboarding results
    """
    from starlette.responses import JSONResponse

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    jwt_token = body.get("jwt", "")
    email = body.get("email", "")
    username = body.get("username", "")
    registration_token = body.get("registration_token", "")

    if not jwt_token or not email or not username:
        return JSONResponse(
            {"error": "Missing required fields: jwt, email, username"},
            status_code=400
        )

    logger.info(f"[OIDC-onboard] Starting onboarding for {email} (username: {username})")

    try:
        # Get user ID from Vikunja to verify JWT is valid
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        user_resp = requests.get(
            f"{vikunja_url}/api/v1/user",
            headers={"Authorization": f"Bearer {jwt_token}"},
            timeout=10
        )

        if user_resp.status_code != 200:
            logger.warning(f"[OIDC-onboard] Invalid JWT for {email}: {user_resp.status_code}")
            return JSONResponse(
                {"error": "Invalid JWT token"},
                status_code=401
            )

        user_data = user_resp.json()
        vikunja_user_id = user_data.get("id")
        verified_username = user_data.get("username")
        verified_email = user_data.get("email", email)

        logger.info(f"[OIDC-onboard] Verified user: id={vikunja_user_id}, username={verified_username}")

        # Check if user already exists - don't waste registration token
        user_id = f"vikunja:{verified_username}"
        from .token_broker import is_registered_user
        if is_registered_user(user_id):
            logger.info(f"[OIDC-onboard] User {user_id} already exists - returning existing account message")
            return JSONResponse({
                "success": True,
                "existing_user": True,
                "message": "Welcome back! You already have an account.",
                "user_id": user_id,
            })

        # Register NEW user in factumerit_users table
        try:
            from .token_broker import register_user
            register_user(user_id, platform="vikunja", email=verified_email, registered_via="oidc")
            logger.info(f"[OIDC-onboard] User {user_id} registered in factumerit_users table")
        except Exception as e:
            logger.warning(f"[OIDC-onboard] Failed to register user: {e}")

        # Create wallet with initial credit from token
        try:
            from .registration_tokens import get_token_stats, TokenNotFoundError
            from .budget_service import ensure_user_budget

            initial_credit_cents = 0
            ttl_days = None
            if registration_token:
                try:
                    token_stats = get_token_stats(registration_token)
                    initial_credit_cents = token_stats.get("initial_credit_cents", 0)
                    ttl_days = token_stats.get("ttl_days")
                except TokenNotFoundError:
                    logger.warning(f"[OIDC-onboard] Token {registration_token} not found for credit lookup")

            ensure_user_budget(user_id, initial_credit_cents=initial_credit_cents, promo_ttl_days=ttl_days)
            ttl_note = f" (expires in {ttl_days} days)" if ttl_days else ""
            logger.info(f"[OIDC-onboard] Wallet created for {user_id} with ${initial_credit_cents/100:.2f} credit{ttl_note}")
        except Exception as e:
            logger.error(f"[OIDC-onboard] Failed to create wallet: {e}")
            # Non-fatal - wallet can be created later on first API call

        # Create SignupState for running workflow stages
        from .signup_workflow import SignupState, SignupWorkflow

        workflow = SignupWorkflow(vikunja_url)

        state = SignupState(
            email=verified_email,
            username=verified_username,
            registration_code=registration_token,
            vikunja_user_id=vikunja_user_id,
            vikunja_jwt_token=jwt_token,
        )

        # Stage 2: Provision bot (non-fatal)
        state = workflow.stage_2_provision_bot(state)

        # Stage 3: Verify bot exists (non-fatal, but required for stage 5)
        state = workflow.stage_3_verify_bot(state, max_retries=10, retry_delay=2.5)

        # Stage 4: Find Inbox (non-fatal)
        state = workflow.stage_4_find_inbox(state)

        # Stage 5: Skip sharing - deferred to activation like email flow
        logger.info(f"[OIDC-onboard] Skipping Inbox sharing - deferred to activation endpoint")

        # Stage 6: Create welcome task with activation link (non-fatal)
        state = workflow.stage_6_create_welcome_task(state)

        # Stage 7: Send Google welcome email (same content as password email, minus credentials)
        from .email_service import send_google_welcome_email
        user_name = user_data.get("name") or verified_username
        email_result = send_google_welcome_email(
            to_email=verified_email,
            user_name=user_name,
        )
        if email_result.success:
            logger.info(f"[OIDC-onboard] Welcome email sent to {verified_email}")
            state.password_reset_sent = True  # Reuse field for tracking
        else:
            logger.warning(f"[OIDC-onboard] Failed to send welcome email: {email_result.error}")

        logger.info(f"[OIDC-onboard] ✓ Onboarding complete for {verified_email}")
        logger.info(f"    Bot provisioned: {'✓' if state.bot_credentials else '✗'}")
        logger.info(f"    Bot verified: {'✓' if state.bot_verified else '✗'}")
        logger.info(f"    Inbox found: {'✓' if state.inbox_project_id else '✗'}")
        logger.info(f"    Welcome task: {'✓' if state.welcome_task_created else '✗'}")

        return JSONResponse({
            "success": True,
            "onboarding": {
                "bot_provisioned": state.bot_credentials is not None,
                "bot_verified": state.bot_verified,
                "inbox_found": state.inbox_project_id is not None,
                "welcome_task_created": state.welcome_task_created,
                "email_sent": state.password_reset_sent,
            }
        })

    except Exception as e:
        logger.error(f"[OIDC-onboard] Error for {email}: {e}", exc_info=True)
        return JSONResponse(
            {"error": f"Onboarding failed: {str(e)}"},
            status_code=500
        )


# ============================================================================
# WORKSPACE SWITCHER (Multi-account support)
# ============================================================================
# Bead: fa-bh42 (Multi-account workspaces)

# @PRIVATE
@mcp.custom_route("/my-workspaces", methods=["GET"])
async def my_workspaces(request: Request):
    """Show workspace switcher for users with multiple linked accounts.

    Requires authenticated session. Shows all workspaces linked to the
    user's Google identity and allows switching between them.
    """
    from starlette.responses import HTMLResponse, RedirectResponse
    from .token_broker import get_user_workspaces, get_canonical_email, execute

    # Get current user from Vikunja session (JWT in localStorage doesn't help here)
    # We'll use the email from query param or cookie
    email = request.query_params.get("email", "").strip()

    if not email:
        # Try to get from cookie
        serializer = _get_cookie_serializer()
        try:
            signup_state = serializer.loads(request.cookies.get("signup_state", ""))
            # Check if we have stored email from recent signup
            if "email" in signup_state:
                email = signup_state["email"]
        except Exception:
            pass

    if not email:
        # No email context - show a form to enter email
        return HTMLResponse(content=_workspaces_lookup_html(), status_code=200)

    # Get canonical email and lookup workspaces
    canonical = get_canonical_email(email)
    workspaces = get_user_workspaces(canonical)

    if not workspaces:
        return HTMLResponse(
            content=_workspaces_empty_html(canonical),
            status_code=200
        )

    return HTMLResponse(
        content=_workspaces_list_html(canonical, workspaces),
        status_code=200
    )


# @PRIVATE
def _workspaces_lookup_html() -> str:
    """HTML for workspace lookup form."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>My Workspaces - Factum Erit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 { color: #1a1a2e; margin-bottom: 8px; }
        p { color: #666; }
        input[type="email"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            margin: 16px 0;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover { background: #5558e3; }
    </style>
</head>
<body>
    <div class="card">
        <h1>My Workspaces</h1>
        <p>Enter your email to see your linked workspaces.</p>
        <form method="GET" action="/my-workspaces">
            <input type="email" name="email" placeholder="your@email.com" required autofocus>
            <button type="submit">Look Up Workspaces</button>
        </form>
    </div>
</body>
</html>"""


# @PRIVATE
def _workspaces_empty_html(email: str) -> str:
    """HTML when no workspaces found."""
    from html import escape
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>No Workspaces - Factum Erit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        h1 {{ color: #1a1a2e; }}
        p {{ color: #666; }}
        .email {{ font-weight: bold; color: #333; }}
        a {{ color: #6366f1; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>No Workspaces Found</h1>
        <p>No workspaces are linked to <span class="email">{escape(email)}</span>.</p>
        <p style="margin-top: 24px;">
            <a href="/my-workspaces">← Try a different email</a>
        </p>
    </div>
</body>
</html>"""


# @PRIVATE
def _workspaces_list_html(email: str, workspaces: list) -> str:
    """HTML showing list of workspaces."""
    from html import escape
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    workspace_items = ""
    for ws in workspaces:
        primary_badge = '<span class="badge primary">Primary</span>' if ws["is_primary"] else ""
        username = ws["user_id"].replace("vikunja:", "")
        workspace_items += f"""
        <div class="workspace">
            <div class="workspace-info">
                <div class="workspace-name">{escape(ws["workspace_name"])} {primary_badge}</div>
                <div class="workspace-user">@{escape(username)}</div>
            </div>
            <a href="{vikunja_url}/user/login?username={escape(username)}" class="btn-switch">
                Switch
            </a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>My Workspaces - Factum Erit</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #1a1a2e; margin-bottom: 8px; }}
        .subtitle {{ color: #666; margin-bottom: 24px; }}
        .workspace {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px;
            border: 1px solid #eee;
            border-radius: 8px;
            margin-bottom: 12px;
        }}
        .workspace:hover {{ border-color: #6366f1; }}
        .workspace-name {{
            font-weight: 600;
            color: #333;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .workspace-user {{
            font-size: 14px;
            color: #666;
            margin-top: 4px;
        }}
        .badge {{
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 500;
        }}
        .badge.primary {{
            background: #e0e7ff;
            color: #4338ca;
        }}
        .btn-switch {{
            padding: 8px 16px;
            background: #f5f5f5;
            color: #333;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
        }}
        .btn-switch:hover {{
            background: #6366f1;
            color: white;
        }}
        .footer {{
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #eee;
            font-size: 14px;
            color: #666;
        }}
        .footer a {{ color: #6366f1; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>My Workspaces</h1>
        <p class="subtitle">Linked to {escape(email)}</p>

        {workspace_items}

        <div class="footer">
            <p>Switching workspaces will log you into that Vikunja account.</p>
            <p style="margin-top: 12px;"><a href="/my-workspaces">← Look up different email</a></p>
        </div>
    </div>
</body>
</html>"""


# @PRIVATE
@mcp.custom_route("/internal/complete-oidc-onboarding", methods=["POST"])
async def complete_oidc_onboarding(request: Request):
    """Complete onboarding for OIDC users - called by vikunja middleware.

    This endpoint is called by the vikunja OIDC middleware after a successful
    Google login. The middleware passes user_id directly from its database access,
    so we don't need admin API access to search users.

    Steps:
    1. Receive user_id from middleware (no API search needed)
    2. Update their username to the name from signup
    3. Provision the @eis bot
    4. Create welcome task
    5. Send welcome email

    Bead: fa-8g1r (Welcome message missing for Google Login users)

    Expected JSON body:
        email: User's email (from token_validated cookie)
        name: User's name (from token_validated cookie)
        registration_token: The registration token that was used
        secret: Shared secret for authentication
        vikunja_user_id: User's Vikunja ID (from middleware DB lookup)
        vikunja_username: User's current username (from middleware DB lookup)

    Returns:
        JSON with success status and onboarding results
    """
    from starlette.responses import JSONResponse

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    email = body.get("email", "")
    name = body.get("name", "")
    registration_token = body.get("registration_token", "")
    secret = body.get("secret", "")
    vikunja_user_id = body.get("vikunja_user_id")  # From middleware DB lookup
    current_username = body.get("vikunja_username", "")  # From middleware DB lookup
    user_jwt = body.get("vikunja_jwt", "")  # User's JWT for API calls (to access their Inbox)

    # Validate shared secret (use cookie signing secret)
    expected_secret = os.environ.get("COOKIE_SIGNING_SECRET", "")
    if not secret or secret != expected_secret:
        logger.warning(f"[OIDC-complete] Invalid secret for {email}")
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    if not email:
        return JSONResponse(
            {"error": "Missing required field: email"},
            status_code=400
        )

    if not vikunja_user_id:
        return JSONResponse(
            {"error": "Missing required field: vikunja_user_id"},
            status_code=400
        )

    logger.info(f"[OIDC-complete] Starting onboarding for {email} (name: {name}, user_id: {vikunja_user_id})")

    try:
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        admin_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")

        logger.info(f"[OIDC-complete] Found user: id={vikunja_user_id}, username={current_username}")

        # Update username if name was provided and current username is auto-generated
        new_username = current_username
        if name and _is_auto_generated_username(current_username):
            # Generate a clean username from the name
            new_username = _generate_username_from_name(name, email)
            if new_username != current_username:
                # Use spinal tap endpoint (middleware direct DB access)
                # Bot token can't update users via API, but middleware can via SQLite
                update_resp = requests.post(
                    f"{vikunja_url}/internal/update-username",
                    json={"user_id": vikunja_user_id, "new_username": new_username},
                    timeout=10
                )
                if update_resp.status_code == 200:
                    result = update_resp.json()
                    logger.info(f"[OIDC-complete] Updated username via spinal tap: {result.get('old_username')} -> {result.get('new_username')}")
                else:
                    logger.warning(f"[OIDC-complete] Failed to update username via spinal tap: {update_resp.status_code} - {update_resp.text[:200]}")
                    new_username = current_username  # Keep old username

        # Create SignupState for running workflow stages
        from .signup_workflow import SignupState, SignupWorkflow

        workflow = SignupWorkflow(vikunja_url)

        # Use user's JWT if provided (for accessing their Inbox), otherwise fall back to admin token
        # User JWT is generated by middleware and passed here so we can create tasks in the user's Inbox
        api_token = user_jwt if user_jwt else admin_token
        if user_jwt:
            logger.info(f"[OIDC-complete] Using user JWT for API calls (will access user's Inbox)")
        else:
            logger.warning(f"[OIDC-complete] No user JWT provided, using admin token (will access bot's Inbox)")

        state = SignupState(
            email=email,
            username=new_username,
            registration_code=registration_token,
            vikunja_user_id=vikunja_user_id,
            vikunja_jwt_token=api_token,  # Use user's JWT to access their Inbox
        )

        # OIDC users need factumerit_users record before bot provisioning
        # (password signup creates this in a different flow)
        from .token_broker import register_user
        user_id = f"vikunja:{new_username}"
        if register_user(user_id, platform="vikunja", email=email, registered_via="oidc"):
            logger.info(f"[OIDC-complete] Registered factumerit user: {user_id}")
        else:
            logger.warning(f"[OIDC-complete] Failed to register factumerit user: {user_id}")

        # Create wallet with initial credit from token
        try:
            from .registration_tokens import get_token_stats, TokenNotFoundError
            from .budget_service import ensure_user_budget

            initial_credit_cents = 0
            ttl_days = None  # None = never expires
            if registration_token:
                try:
                    token_stats = get_token_stats(registration_token)
                    initial_credit_cents = token_stats.get("initial_credit_cents", 0)
                    ttl_days = token_stats.get("ttl_days")
                except TokenNotFoundError:
                    logger.warning(f"[OIDC-complete] Token {registration_token} not found for credit lookup")

            ensure_user_budget(user_id, initial_credit_cents=initial_credit_cents, promo_ttl_days=ttl_days)
            logger.info(f"[OIDC-complete] Wallet created for {user_id} with ${initial_credit_cents/100:.2f} credit")
        except Exception as e:
            logger.error(f"[OIDC-complete] Failed to create wallet: {e}")
            # Non-fatal - wallet can be created later on first API call

        # Stage 2: Provision bot (non-fatal)
        state = workflow.stage_2_provision_bot(state)

        # Stage 3: Verify bot exists (non-fatal, but required for stage 5)
        state = workflow.stage_3_verify_bot(state, max_retries=10, retry_delay=2.5)

        # Stage 4: Find Inbox (non-fatal)
        state = workflow.stage_4_find_inbox(state)

        # Stage 5: Skip sharing - deferred to activation like email flow
        logger.info(f"[OIDC-complete] Skipping Inbox sharing - deferred to activation endpoint")

        # Stage 6: Create welcome task with activation link (non-fatal)
        state = workflow.stage_6_create_welcome_task(state)

        # Stage 7: Send Google welcome email
        from .email_service import send_onboarding_email
        display_name = name or new_username
        email_result = send_onboarding_email(
            to_email=email,
            username=new_username,
            password=None,
            user_name=display_name,
            auth_method="google",
        )
        if email_result.success:
            logger.info(f"[OIDC-complete] Welcome email sent to {email}")
            state.password_reset_sent = True
        else:
            logger.warning(f"[OIDC-complete] Failed to send welcome email: {email_result.error}")

        logger.info(f"[OIDC-complete] ✓ Onboarding complete for {email}")
        logger.info(f"    Username: {new_username}")
        logger.info(f"    Bot provisioned: {'✓' if state.bot_credentials else '✗'}")
        logger.info(f"    Bot verified: {'✓' if state.bot_verified else '✗'}")
        logger.info(f"    Inbox found: {'✓' if state.inbox_project_id else '✗'}")
        logger.info(f"    Welcome task: {'✓' if state.welcome_task_created else '✗'}")
        logger.info(f"    Email sent: {'✓' if state.password_reset_sent else '✗'}")

        return JSONResponse({
            "success": True,
            "onboarding": {
                "username": new_username,
                "bot_provisioned": state.bot_credentials is not None,
                "bot_verified": state.bot_verified,
                "inbox_found": state.inbox_project_id is not None,
                "welcome_task_created": state.welcome_task_created,
                "email_sent": state.password_reset_sent,
            }
        })

    except Exception as e:
        logger.error(f"[OIDC-complete] Error for {email}: {e}", exc_info=True)
        return JSONResponse(
            {"error": f"Onboarding failed: {str(e)}"},
            status_code=500
        )


# @PRIVATE
def _is_auto_generated_username(username: str) -> bool:
    """Check if username looks auto-generated (e.g., 'humbly-artistic-antelope')."""
    if not username:
        return True
    # Vikunja generates usernames like "adjective-adjective-animal"
    parts = username.split("-")
    if len(parts) >= 2:
        # Check if it looks like an auto-generated pattern
        # These are typically lowercase words separated by hyphens
        if all(part.isalpha() and part.islower() for part in parts):
            return True
    return False


# @PRIVATE
def _generate_username_from_name(name: str, email: str) -> str:
    """Generate a clean username from name, falling back to email prefix."""
    import re

    # Try to use the name first
    if name:
        # Convert to lowercase, replace spaces with nothing, remove non-alphanumeric
        clean = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
        if len(clean) >= 3:
            return clean[:20]  # Limit length

    # Fall back to email prefix
    prefix = email.split("@")[0]
    clean = re.sub(r'[^a-zA-Z0-9]', '', prefix.lower())
    return clean[:20] if clean else "user"


# ============================================================================
# VIKUNJA OAUTH CALLBACK (One-click connect flow)
# ============================================================================

# @PRIVATE
@mcp.custom_route("/vikunja-callback", methods=["GET"])
async def vikunja_callback(request: Request):
    """Callback endpoint for Vikunja one-click OAuth connection.

    Called by auth-bridge after user completes OAuth and token is created.

    Query params:
        state: Nonce from pending connection (maps to Slack user ID)
        token: Vikunja API token (created by auth-bridge)
        email: User's email (optional, for logging)

    Returns:
        HTML success page or error page
    """
    from starlette.responses import HTMLResponse

    state = request.query_params.get("state")
    token = request.query_params.get("token")
    email = request.query_params.get("email", "")

    # Validate required params
    if not state or not token:
        logger.warning(f"Vikunja callback missing params: state={bool(state)}, token={bool(token)}")
        return HTMLResponse(
            content=_callback_error_html("Missing required parameters. Please try connecting again."),
            status_code=400
        )

    # Validate state (nonce) and get user ID
    pending = _get_pending_connection(state)
    if not pending:
        logger.warning(f"Vikunja callback invalid/expired state: {state[:8]}...")
        return HTMLResponse(
            content=_callback_error_html(
                "Connection request expired or invalid. "
                "This can happen if the bot restarted. "
                "Please send a message to the bot to get a fresh connection link."
            ),
            status_code=400
        )

    # Get user ID and platform from pending connection
    user_id = pending.get("user_id") or pending.get("slack_user_id")  # Backward compat
    platform = pending.get("platform", "slack")  # Default to slack for old connections

    # Validate token format (basic check)
    if not token.startswith("tk_"):
        logger.warning(f"Vikunja callback invalid token format for {platform} user {user_id}")
        return HTMLResponse(
            content=_callback_error_html("Invalid token format. Please try connecting again."),
            status_code=400
        )

    # Check if user is already registered (OAuth callback only for existing users)
    # New users must go through beta-signup with a registration token first
    from .token_broker import is_registered_user
    if not is_registered_user(user_id):
        logger.warning(f"OAuth callback for unregistered user {user_id} - blocking")
        return HTMLResponse(
            content=_callback_error_html(
                "You need to sign up first. "
                "Please use a registration link to create your account, "
                "then you can connect via OAuth."
            ),
            status_code=403
        )

    # Store token for user (they're already registered)
    _set_user_vikunja_token(user_id, token)
    token_preview = token[:10] + "..." if len(token) > 10 else token
    logger.info(f"Vikunja token set for {platform} user {user_id} (email: {email}): {token_preview}")

    # Clean up pending connection
    _delete_pending_connection(state)

    # Notify user based on platform (best effort)
    try:
        if platform == "slack":
            slack_app, _ = _get_slack_app()
            if slack_app:
                slack_app.client.chat_postMessage(
                    channel=user_id,  # DM the user
                    text=(
                        ":white_check_mark: *Connected!*\n\n"
                        "You're all set. Try:\n"
                        "• \"Add a task: Buy groceries tomorrow\"\n"
                        "• `/today` for today's tasks\n"
                        "• `/summary` for the big picture\n\n"
                        "_Or just tell me what's on your mind._"
                    )
                )
                logger.info(f"Sent connection success DM to Slack user {user_id}")
        elif platform == "matrix":
            # Send Matrix DM via matrix_client
            from .matrix_client import get_matrix_bot_instance
            matrix_bot = get_matrix_bot_instance()
            if matrix_bot:
                dm_room_id = await matrix_bot._get_or_create_dm(user_id)
                if dm_room_id:
                    await matrix_bot._send_message(
                        dm_room_id,
                        (
                            "✅ **Connected!**\n\n"
                            "You're all set. Try:\n"
                            "• \"Add a task: Buy groceries tomorrow\"\n"
                            "• `!today` for today's tasks\n"
                            "• `!summary` for the big picture\n\n"
                            "_Or just tell me what's on your mind._"
                        )
                    )
                    logger.info(f"Sent connection success DM to Matrix user {user_id}")
    except Exception as e:
        logger.warning(f"Failed to send {platform} notification to {user_id}: {e}")

    # Redirect to Vikunja dashboard (success!)
    from starlette.responses import RedirectResponse
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    return RedirectResponse(url=f"{vikunja_url}/", status_code=303)


# @PRIVATE
def _callback_success_html(platform: str = "slack") -> str:
    """Generate success HTML page for callback.
    
    Args:
        platform: "slack" or "matrix" - determines return message
    """
    return_to = "Slack" if platform == "slack" else "Element"
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Connected to Vikunja</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .card {{
            background: white;
            padding: 48px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 400px;
        }}
        .checkmark {{
            font-size: 64px;
            margin-bottom: 16px;
        }}
        h1 {{
            margin: 0 0 16px;
            color: #1a1a1a;
        }}
        p {{
            color: #666;
            margin: 0;
            line-height: 1.6;
        }}
        .close-hint {{
            margin-top: 24px;
            font-size: 14px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="checkmark">✅</div>
        <h1>Connected!</h1>
        <p>Your Vikunja account is now linked to the {platform.title()} bot.</p>
        <p class="close-hint">You can close this tab and return to {return_to}.</p>
    </div>
    <script>
        // Auto-close after 3 seconds (if opened as popup)
        setTimeout(() => {{ window.close(); }}, 3000);
    </script>
</body>
</html>"""


# @PRIVATE
def _callback_error_html(message: str) -> str:
    """Generate error HTML page for callback."""
    import html
    escaped_message = html.escape(message)
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Connection Failed</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }}
        .card {{
            background: white;
            padding: 48px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            max-width: 400px;
        }}
        .icon {{
            font-size: 64px;
            margin-bottom: 16px;
        }}
        h1 {{
            margin: 0 0 16px;
            color: #c0392b;
        }}
        p {{
            color: #666;
            margin: 0;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">❌</div>
        <h1>Connection Failed</h1>
        <p>{escaped_message}</p>
    </div>
</body>
</html>"""


# ============================================================================
# ICS CALENDAR HTTP ENDPOINT
# ============================================================================

# Cache for parsed calendar instances (parsed once on first access)
_calendar_instances_cache: Optional[dict] = None

# Cache for ICS feed content with TTL (instance+label -> (content, timestamp))
_ics_feed_cache: dict = {}
_ICS_CACHE_TTL_SECONDS = 300  # 5 minutes


# @PRIVATE
def _get_cached_ics_feed(instance: str, label: str) -> Optional[str]:
    """Get cached ICS feed if not expired."""
    cache_key = f"{instance}:{label}"
    if cache_key in _ics_feed_cache:
        content, timestamp = _ics_feed_cache[cache_key]
        if time.time() - timestamp < _ICS_CACHE_TTL_SECONDS:
            return content
        # Expired, remove from cache
        del _ics_feed_cache[cache_key]
    return None


# @PRIVATE
def _set_cached_ics_feed(instance: str, label: str, content: str):
    """Cache ICS feed content."""
    cache_key = f"{instance}:{label}"
    _ics_feed_cache[cache_key] = (content, time.time())


# @PRIVATE
def _invalidate_ics_cache(instance: Optional[str] = None):
    """Invalidate ICS cache for an instance or all instances.

    Called when tasks are created/updated/deleted to ensure
    calendar feeds reflect latest data.
    """
    global _ics_feed_cache
    if instance:
        # Clear only entries for this instance
        keys_to_remove = [k for k in _ics_feed_cache if k.startswith(f"{instance}:")]
        for k in keys_to_remove:
            del _ics_feed_cache[k]
    else:
        # Clear all cached feeds
        _ics_feed_cache = {}


# @PRIVATE
def _get_calendar_instances() -> dict:
    """Get calendar instance configurations from environment.

    Parses VIKUNJA_INSTANCES JSON env var for multi-instance support.
    Falls back to VIKUNJA_URL/VIKUNJA_TOKEN for single-instance mode.

    Returns:
        Dict mapping instance name to {url, token, calendar_token}
    """
    global _calendar_instances_cache

    # Return cached result if available
    if _calendar_instances_cache is not None:
        return _calendar_instances_cache

    instances = {}

    # Try multi-instance config first
    instances_json = os.environ.get("VIKUNJA_INSTANCES", "")
    if instances_json:
        try:
            instances_list = json.loads(instances_json)
            for inst in instances_list:
                name = inst.get("name", "").strip()
                url = inst.get("url", "").strip()
                token = inst.get("token", "").strip()
                if name and url and token:
                    calendar_token = hashlib.sha256(token.encode()).hexdigest()[:16]
                    instances[name] = {
                        "url": url,
                        "token": token,
                        "calendar_token": calendar_token
                    }
        except (json.JSONDecodeError, TypeError):
            pass  # Fall through to single-instance mode

    # Fall back to single-instance mode
    if not instances:
        url = os.environ.get("VIKUNJA_URL", "")
        token = os.environ.get("VIKUNJA_BOT_TOKEN") or os.environ.get("VIKUNJA_TOKEN", "")
        if url and token:
            calendar_token = hashlib.sha256(token.encode()).hexdigest()[:16]
            instances["default"] = {
                "url": url,
                "token": token,
                "calendar_token": calendar_token
            }

    _calendar_instances_cache = instances
    return instances


# @PRIVATE
def _clear_calendar_instances_cache():
    """Clear the calendar instances cache (for testing)."""
    global _calendar_instances_cache
    _calendar_instances_cache = None


# @PRIVATE
def _get_calendar_token(instance: Optional[str] = None) -> str:
    """Generate calendar feed token for an instance.

    Args:
        instance: Instance name. If None, uses default/first instance.

    Returns:
        16-char hex token derived from instance's API token.
    """
    instances = _get_calendar_instances()

    if not instances:
        return ""

    if instance and instance in instances:
        return instances[instance]["calendar_token"]

    # For backward compatibility, return first/default instance token
    if "default" in instances:
        return instances["default"]["calendar_token"]

    # Return first available instance
    first_instance = next(iter(instances.values()), None)
    return first_instance["calendar_token"] if first_instance else ""


# @PRIVATE
def _validate_calendar_request(instance: str, token: str) -> Optional[dict]:
    """Validate a calendar request and return instance config if valid.

    Args:
        instance: Instance name from URL
        token: Token from URL

    Returns:
        Instance config dict if valid, None if invalid
    """
    instances = _get_calendar_instances()

    if instance not in instances:
        return None

    inst_config = instances[instance]
    if inst_config["calendar_token"] != token:
        return None

    return inst_config


# @PRIVATE
@mcp.custom_route("/calendar/{instance}/{token}.ics", methods=["GET"])
async def calendar_ics_feed_multi(request: Request):
    """ICS calendar feed endpoint for multi-instance support.

    URL: /calendar/{instance}/{token}.ics?label=calendar

    - instance: Instance name (e.g., "personal", "business")
    - token: Security token for that instance
    - label: Filter tasks by this label (default: "calendar")

    Returns: ICS file with text/calendar content type
    """
    from starlette.responses import Response

    instance = request.path_params.get("instance", "")
    url_token = request.path_params.get("token", "")

    # Validate instance and token
    inst_config = _validate_calendar_request(instance, url_token)
    if not inst_config:
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid instance or token"},
            status_code=401
        )

    # Get label from query params
    label = request.query_params.get("label", "calendar")

    # Check cache first
    ics_content = _get_cached_ics_feed(instance, label)
    if not ics_content:
        # Generate ICS using instance-specific credentials
        ics_content = _get_ics_feed_impl(label=label, instance=instance)
        _set_cached_ics_feed(instance, label, ics_content)

    # Return with calendar content type
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": f'attachment; filename="{instance}-{label}.ics"'
        }
    )


# @PRIVATE
@mcp.custom_route("/calendar/{token}.ics", methods=["GET"])
async def calendar_ics_feed(request: Request):
    """ICS calendar feed endpoint (backward compatible single-instance).

    URL: /calendar/{token}.ics?label=calendar

    - token: Security token derived from Vikunja credentials
    - label: Filter tasks by this label (default: "calendar")

    Returns: ICS file with text/calendar content type
    """
    from starlette.responses import Response

    url_token = request.path_params.get("token", "")

    # Find which instance this token belongs to
    instances = _get_calendar_instances()
    matched_instance = None

    for name, config in instances.items():
        if config["calendar_token"] == url_token:
            matched_instance = name
            break

    if not matched_instance:
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid calendar token"},
            status_code=401
        )

    # Get label from query params
    label = request.query_params.get("label", "calendar")

    # Check cache first
    ics_content = _get_cached_ics_feed(matched_instance, label)
    if not ics_content:
        # Generate ICS
        ics_content = _get_ics_feed_impl(label=label, instance=matched_instance)
        _set_cached_ics_feed(matched_instance, label, ics_content)

    # Return with calendar content type
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": f'attachment; filename="{label}.ics"'
        }
    )


# ============================================================================
# SMART TASK REFRESH ENDPOINT
# ============================================================================


# @PRIVATE
def _generate_refresh_token(task_id: int) -> str:
    """Generate a secure refresh token for a task.

    Token is derived from task_id + bot token, so it's:
    - Unique per task
    - Only valid if you know the bot token
    - URL-safe (hex encoding)
    """
    bot_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")
    return hashlib.sha256(f"{task_id}:{bot_token}".encode()).hexdigest()[:12]


# @PRIVATE
def _verify_refresh_token(task_id: int, token: str) -> bool:
    """Verify a refresh token is valid for a task."""
    expected = _generate_refresh_token(task_id)
    return token == expected


# @PRIVATE
def _generate_action_token(action: str, *ids: int) -> str:
    """Generate a secure token for one-click action links.

    Token is derived from action + ids + bot token, so it's:
    - Unique per action and context
    - Only valid if you know the bot token
    - URL-safe (hex encoding)

    Args:
        action: Action name (e.g., "complete", "ears-off")
        *ids: Context IDs (task_id, project_id, etc.)

    Returns:
        12-character hex token
    """
    bot_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")
    data = f"{action}:{':'.join(str(i) for i in ids)}:{bot_token}"
    return hashlib.sha256(data.encode()).hexdigest()[:12]


# @PRIVATE
def _verify_action_token(action: str, token: str, *ids: int) -> bool:
    """Verify an action token is valid."""
    expected = _generate_action_token(action, *ids)
    return token == expected


# @PRIVATE
@mcp.custom_route("/refresh/{task_id}/{token}", methods=["GET"])
async def refresh_smart_task(request: Request):
    """Refresh a smart task (weather/stock/news) and redirect to Vikunja.

    URL: /refresh/{task_id}/{token}

    - task_id: The task ID to refresh
    - token: Security token derived from task_id + bot_token

    On success: Refreshes the task content and redirects to the task in Vikunja.
    On error: Returns JSON error message.
    """
    from starlette.responses import RedirectResponse
    import asyncio

    task_id_str = request.path_params.get("task_id", "")
    url_token = request.path_params.get("token", "")

    # Validate task_id
    try:
        task_id = int(task_id_str)
    except (ValueError, TypeError):
        return JSONResponse(
            {"error": "invalid_task_id", "message": "Task ID must be a number"},
            status_code=400
        )

    # Validate token
    if not _verify_refresh_token(task_id, url_token):
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid or expired refresh token"},
            status_code=401
        )

    # Get the task and extract metadata
    from .vikunja_client import BotVikunjaClient, VikunjaAPIError
    from .metadata_manager import MetadataManager
    from .keyword_handlers import KeywordHandlers

    try:
        client = BotVikunjaClient()
        task = client.get_task(task_id)
    except VikunjaAPIError as e:
        return JSONResponse(
            {"error": "task_not_found", "message": f"Task #{task_id} not found: {e}"},
            status_code=404
        )

    # Extract metadata to find keyword and handler_args
    description = task.get("description", "")
    metadata, content = MetadataManager.extract(description)

    if not metadata or not metadata.keyword:
        return JSONResponse(
            {"error": "not_smart_task", "message": "Task is not a refreshable smart task"},
            status_code=400
        )

    keyword = metadata.keyword
    handler_args = metadata.handler_args or {}

    # Execute the appropriate handler
    handlers = KeywordHandlers(client)
    handler_method = handlers.get_handler(f"{keyword}_handler")

    if not handler_method:
        return JSONResponse(
            {"error": "unknown_keyword", "message": f"Unknown keyword: {keyword}"},
            status_code=400
        )

    try:
        result = await handler_method(handler_args)
    except Exception as e:
        return JSONResponse(
            {"error": "handler_error", "message": f"Refresh failed: {e}"},
            status_code=500
        )

    if not result.success:
        return JSONResponse(
            {"error": "refresh_failed", "message": result.message},
            status_code=500
        )

    # Update the task with new content, preserving metadata and action bar
    try:
        mcp_url = os.environ.get("MCP_URL", "https://mcp.factumerit.app")

        # Build action bar
        refresh_token = _generate_refresh_token(task_id)
        complete_token = _generate_action_token("complete", task_id)
        action_parts = [
            f"🔄 [Refresh]({mcp_url}/refresh/{task_id}/{refresh_token})",
            f"✅ [Done]({mcp_url}/complete/{task_id}/{complete_token})",
        ]
        # Add schedule hint if no schedule
        if not metadata.schedule and keyword in ("weather", "stock", "rss"):
            action_parts.append("⏰ Add `hourly` or `6h` to auto-update")
        action_bar = " · ".join(action_parts)

        # Add action bar to message
        message_with_actions = f"{result.message}\n\n{action_bar}"
        html_content = markdown.markdown(message_with_actions, extensions=['fenced_code', 'tables'])

        # Always preserve metadata (keyword, handler_args, schedule)
        new_metadata = MetadataManager.create_initial(
            cost_tier=metadata.cost_tier or "$",
            prompt="",  # No prompt for refresh
            keyword=keyword,
            handler_args=handler_args,
        )
        if metadata.schedule:
            new_metadata.schedule = metadata.schedule
        html_description = MetadataManager.format_html(new_metadata, html_content)

        client.update_task(task_id, description=html_description)
    except VikunjaAPIError as e:
        return JSONResponse(
            {"error": "update_failed", "message": f"Could not update task: {e}"},
            status_code=500
        )

    # Redirect to the task in Vikunja
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    redirect_url = f"{vikunja_url}/tasks/{task_id}"

    return RedirectResponse(url=redirect_url, status_code=302)


# @PUBLIC
@mcp.custom_route("/move/{task_id}/{project_id}/{token}", methods=["GET"])
async def move_task_to_project(request: Request):
    """Move a task to a different project and redirect to Vikunja.

    URL: /move/{task_id}/{project_id}/{token}

    - task_id: The task ID to move
    - project_id: The target project ID
    - token: Security token derived from task_id + project_id + bot_token

    On success: Moves the task and redirects to the task in Vikunja.
    On error: Returns JSON error message.
    """
    from starlette.responses import RedirectResponse

    task_id_str = request.path_params.get("task_id", "")
    project_id_str = request.path_params.get("project_id", "")
    url_token = request.path_params.get("token", "")

    # Validate task_id and project_id
    try:
        task_id = int(task_id_str)
        project_id = int(project_id_str)
    except (ValueError, TypeError):
        return JSONResponse(
            {"error": "invalid_ids", "message": "Task ID and Project ID must be numbers"},
            status_code=400
        )

    # Validate token
    bot_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")
    expected_token = hashlib.sha256(f"{task_id}:{project_id}:{bot_token}".encode()).hexdigest()[:12]
    if url_token != expected_token:
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid or expired move token"},
            status_code=401
        )

    # Move the task
    from .vikunja_client import BotVikunjaClient, VikunjaAPIError

    try:
        client = BotVikunjaClient()

        # Get current task
        task = client.get_task(task_id)
        if not task:
            return JSONResponse(
                {"error": "task_not_found", "message": f"Task #{task_id} not found"},
                status_code=404
            )

        # Clean description: remove "Move to:" links after successful move
        description = task.get("description", "")
        if description and "📁" in description:
            import re
            # Remove the move links section (📁 Move to: ...)
            # Pattern: ---\n📁 **Move to:** ... to end of that line
            description = re.sub(r'\n*---\n*📁 \*?\*?Move to:\*?\*?[^\n]*\n*', '', description)
            # Also remove standalone move links without ---
            description = re.sub(r'\n*📁 \*?\*?Move to:\*?\*?[^\n]*\n*', '', description)
            description = description.rstrip()

        # Update task with new project_id and cleaned description
        task["project_id"] = project_id
        client.update_task(task_id, project_id=project_id, description=description)

        logger.info(f"Moved task #{task_id} to project #{project_id}")

    except VikunjaAPIError as e:
        return JSONResponse(
            {"error": "move_failed", "message": f"Could not move task: {e}"},
            status_code=500
        )

    # Redirect to the task in Vikunja
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    redirect_url = f"{vikunja_url}/tasks/{task_id}"

    return RedirectResponse(url=redirect_url, status_code=302)


# @PRIVATE
@mcp.custom_route("/complete/{task_id}/{token}", methods=["GET"])
async def complete_task_action(request: Request):
    """Complete a task via one-click link and redirect to Vikunja.

    URL: /complete/{task_id}/{token}

    - task_id: The task ID to complete
    - token: Security token derived from "complete" + task_id + bot_token

    On success: Marks task as done and redirects to the task in Vikunja.
    On error: Returns JSON error message.

    Bead: solutions-50da
    """
    from starlette.responses import RedirectResponse
    from .vikunja_client import BotVikunjaClient, VikunjaAPIError

    task_id_str = request.path_params.get("task_id", "")
    url_token = request.path_params.get("token", "")

    # Validate task_id
    try:
        task_id = int(task_id_str)
    except (ValueError, TypeError):
        return JSONResponse(
            {"error": "invalid_task_id", "message": "Task ID must be a number"},
            status_code=400
        )

    # Validate token
    if not _verify_action_token("complete", url_token, task_id):
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid or expired action token"},
            status_code=401
        )

    # Complete the task
    try:
        client = BotVikunjaClient()
        task = client.get_task(task_id)
        if not task:
            return JSONResponse(
                {"error": "task_not_found", "message": f"Task #{task_id} not found"},
                status_code=404
            )

        # Mark as done
        client.update_task(task_id, done=True)
        logger.info(f"[ACTION] Completed task #{task_id} via one-click link")

    except VikunjaAPIError as e:
        return JSONResponse(
            {"error": "complete_failed", "message": f"Could not complete task: {e}"},
            status_code=500
        )

    # Redirect to the task in Vikunja
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    redirect_url = f"{vikunja_url}/tasks/{task_id}"

    return RedirectResponse(url=redirect_url, status_code=302)


# @PRIVATE
@mcp.custom_route("/remove/{task_id}/{token}", methods=["GET"])
async def remove_task_action(request: Request):
    """Remove (DELETE) a task via one-click link.

    URL: /remove/{task_id}/{token}

    - task_id: The task ID to remove
    - token: Security token derived from "remove" + task_id + bot_token

    On success: Deletes the task and redirects to Vikunja project.
    On error: Returns JSON error message.

    Bead: solutions-nzo3
    """
    from starlette.responses import RedirectResponse
    from .vikunja_client import BotVikunjaClient, VikunjaAPIError

    task_id_str = request.path_params.get("task_id", "")
    url_token = request.path_params.get("token", "")

    # Validate task_id
    try:
        task_id = int(task_id_str)
    except (ValueError, TypeError):
        return JSONResponse(
            {"error": "invalid_task_id", "message": "Task ID must be a number"},
            status_code=400
        )

    # Validate token
    if not _verify_action_token("remove", url_token, task_id):
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid or expired action token"},
            status_code=401
        )

    # Get project_id before deleting (for redirect)
    project_id = None
    try:
        client = BotVikunjaClient()
        task = client.get_task(task_id)
        if task:
            project_id = task.get("project_id")

            # If task has repeat mode, disable it first
            if task.get("repeat_after", 0) > 0:
                client.update_task(task_id, repeat_after=0, repeat_mode=0)

            # Delete the task
            client.delete_task(task_id)
            logger.info(f"[ACTION] Removed task #{task_id} via one-click link")
        else:
            return JSONResponse(
                {"error": "task_not_found", "message": f"Task #{task_id} not found"},
                status_code=404
            )

    except VikunjaAPIError as e:
        return JSONResponse(
            {"error": "remove_failed", "message": f"Could not remove task: {e}"},
            status_code=500
        )

    # Redirect to the project in Vikunja (task is deleted, can't redirect to it)
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    if project_id:
        redirect_url = f"{vikunja_url}/projects/{project_id}"
    else:
        redirect_url = vikunja_url

    return RedirectResponse(url=redirect_url, status_code=302)


# @PRIVATE
@mcp.custom_route("/set-schedule/{task_id}/{schedule}/{token}", methods=["GET"])
async def set_schedule_action(request: Request):
    """Set or change schedule for a task via one-click link.

    URL: /set-schedule/{task_id}/{schedule}/{token}

    - task_id: The task ID to update
    - schedule: Schedule string (hourly, 6h, 12h, daily, off)
    - token: Security token derived from "schedule-{schedule}" + task_id + bot_token

    On success: Updates task schedule and redirects to Vikunja task.
    On error: Returns JSON error message.

    Bead: solutions-n5aa
    """
    from starlette.responses import RedirectResponse
    from .vikunja_client import BotVikunjaClient, VikunjaAPIError
    from .task_scheduler import get_task_scheduler
    from .metadata_manager import MetadataManager

    task_id_str = request.path_params.get("task_id", "")
    schedule = request.path_params.get("schedule", "")
    url_token = request.path_params.get("token", "")

    # Validate task_id
    try:
        task_id = int(task_id_str)
    except (ValueError, TypeError):
        return JSONResponse(
            {"error": "invalid_task_id", "message": "Task ID must be a number"},
            status_code=400
        )

    # Validate schedule
    valid_schedules = ["hourly", "6h", "12h", "daily", "off"]
    if schedule not in valid_schedules:
        return JSONResponse(
            {"error": "invalid_schedule", "message": f"Invalid schedule. Use: {', '.join(valid_schedules)}"},
            status_code=400
        )

    # Validate token
    if not _verify_action_token(f"schedule-{schedule}", url_token, task_id):
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid or expired action token"},
            status_code=401
        )

    # Schedule to seconds mapping
    schedule_seconds = {
        "hourly": 3600,
        "6h": 21600,
        "12h": 43200,
        "daily": 86400,
        "off": 0,
    }

    try:
        client = BotVikunjaClient()
        task = client.get_task(task_id)
        if not task:
            return JSONResponse(
                {"error": "task_not_found", "message": f"Task #{task_id} not found"},
                status_code=404
            )

        # Update Vikunja repeat_after
        repeat_after = schedule_seconds.get(schedule, 0)
        client.update_task(
            task_id,
            repeat_after=repeat_after,
            repeat_mode=0 if repeat_after > 0 else 0,
        )

        # Update metadata in description
        description = task.get("description", "")
        metadata, content = MetadataManager.extract(description)
        if metadata:
            metadata.schedule = schedule if schedule != "off" else None
            new_description = MetadataManager.format_html(metadata, content)
            client.update_task(task_id, description=new_description)

        # Update task scheduler
        scheduler = get_task_scheduler(client)
        if schedule == "off":
            scheduler.remove_task(task_id)
            logger.info(f"[ACTION] Disabled schedule for task #{task_id}")
        else:
            # Get keyword from metadata
            keyword = metadata.keyword if metadata else "weather"
            handler_args = metadata.handler_args if metadata else {}
            scheduler.add_task(
                task_id=task_id,
                keyword=keyword,
                schedule=schedule,
                args=handler_args,
            )
            logger.info(f"[ACTION] Set schedule to '{schedule}' for task #{task_id}")

    except VikunjaAPIError as e:
        return JSONResponse(
            {"error": "schedule_failed", "message": f"Could not update schedule: {e}"},
            status_code=500
        )

    # Redirect to the task in Vikunja
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    redirect_url = f"{vikunja_url}/tasks/{task_id}"

    return RedirectResponse(url=redirect_url, status_code=302)


# @PRIVATE
@mcp.custom_route("/ears-off/{project_id}/{token}", methods=["GET"])
@mcp.custom_route("/capture-off/{project_id}/{token}", methods=["GET"])  # Backwards compat
async def ears_off_action(request: Request):
    """Disable ears mode (!ears off) for a project via one-click link.

    URL: /ears-off/{project_id}/{token} (preferred)
    URL: /capture-off/{project_id}/{token} (backwards compatibility)

    - project_id: The project ID to disable ears mode for
    - token: Security token derived from "ears-off" + project_id + bot_token

    On success: Disables ears mode and redirects to the project in Vikunja.
    On error: Returns JSON error message.

    Bead: solutions-bx4t
    """
    from starlette.responses import RedirectResponse

    project_id_str = request.path_params.get("project_id", "")
    url_token = request.path_params.get("token", "")

    # Validate project_id
    try:
        project_id = int(project_id_str)
    except (ValueError, TypeError):
        return JSONResponse(
            {"error": "invalid_project_id", "message": "Project ID must be a number"},
            status_code=400
        )

    # Validate token (accept both ears-off and capture-off for backwards compat)
    if not (_verify_action_token("ears-off", url_token, project_id) or
            _verify_action_token("capture-off", url_token, project_id)):
        return JSONResponse(
            {"error": "invalid_token", "message": "Invalid or expired action token"},
            status_code=401
        )

    # Disable ears mode
    _update_project_ears(project_id, enabled=False)
    logger.info(f"[EARS] Disabled ears mode for project #{project_id} via one-click link")

    # Update service_needed flags for all users (solutions-skqu)
    # Since we don't know which user clicked the link, check all users with service_needed=true
    try:
        from .bot_provisioning import get_users_needing_service, set_service_needed

        users_needing_service = get_users_needing_service()
        ears_projects = _get_ears_enabled_projects()

        # If no more EARS projects exist, disable service for all users
        if not ears_projects:
            for user_id in users_needing_service:
                set_service_needed(user_id, needed=False)
                logger.info(f"[EARS] Disabled service for {user_id} (no EARS projects)")
    except Exception as e:
        logger.error(f"[EARS] Failed to update service_needed flags: {e}")
        # Don't fail the whole operation

    # Redirect to the project in Vikunja
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    redirect_url = f"{vikunja_url}/projects/{project_id}"

    return RedirectResponse(url=redirect_url, status_code=302)


# @PRIVATE
@mcp.custom_route("/project-queue", methods=["GET"])
async def get_project_queue(request: Request):
    """Get pending projects from queue for current user.

    Bead: solutions-eofy

    Returns pending queue entries for the authenticated user.
    Frontend uses this to create projects with user's session token.
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Missing or invalid Authorization header"}, status_code=401)

    token = auth_header[7:]  # Remove "Bearer " prefix

    # Verify token and get username
    try:
        import httpx
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        resp = httpx.get(
            f"{vikunja_url}/api/v1/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        resp.raise_for_status()
        user_data = resp.json()
        username = user_data.get("username")

        if not username:
            return JSONResponse({"error": "Could not determine username"}, status_code=401)

        # Fetch pending queue entries
        from .token_broker import execute
        rows = execute("""
            SELECT id, user_id, username, bot_username, title, description,
                   hex_color, parent_project_id, projects, created_at
            FROM project_creation_queue
            WHERE username = %s AND status = 'pending'
            ORDER BY created_at ASC
        """, (username,))

        entries = []
        for row in rows:
            entry = {
                "id": row[0],
                "user_id": row[1],
                "username": row[2],
                "bot_username": row[3],
                "created_at": row[9].isoformat() if row[9] else None
            }

            # Check if batch mode (projects JSONB) or single mode (title)
            if row[8]:  # projects column (JSONB - already parsed by psycopg)
                entry["projects"] = row[8]
            else:  # single mode
                entry["title"] = row[4]
                entry["description"] = row[5]
                entry["hex_color"] = row[6]
                entry["parent_project_id"] = row[7]

            entries.append(entry)

        return JSONResponse(entries)

    except Exception as e:
        logger.error(f"[get_project_queue] Error: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)




# @PRIVATE
@mcp.custom_route("/project-queue/claim", methods=["POST"])
async def claim_project_queue(request: Request):
    """Atomically claim pending queue entries for processing.

    Bead: solutions-eofy.1

    This endpoint provides idempotent queue processing:
    1. Atomically updates pending -> processing
    2. Returns claimed entries
    3. Frontend creates projects
    4. Frontend calls /complete to mark as done

    This prevents duplicate project creation if user refreshes the page.
    """
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Missing or invalid Authorization header"}, status_code=401)

    token = auth_header[7:]  # Remove "Bearer " prefix

    # Verify token and get username
    try:
        import httpx
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        resp = httpx.get(
            f"{vikunja_url}/api/v1/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        resp.raise_for_status()
        user_data = resp.json()
        username = user_data.get("username")

        if not username:
            return JSONResponse({"error": "Could not determine username"}, status_code=401)

        # Atomically claim pending entries (UPDATE ... RETURNING pattern)
        from .token_broker import execute
        rows = execute("""
            UPDATE project_creation_queue
            SET status = 'processing'
            WHERE id IN (
                SELECT id FROM project_creation_queue
                WHERE username = %s AND status = 'pending'
                ORDER BY created_at ASC
                FOR UPDATE SKIP LOCKED
            )
            RETURNING id, user_id, username, bot_username, title, description,
                      hex_color, parent_project_id, projects, created_at
        """, (username,))

        entries = []
        for row in rows:
            entry = {
                "id": row[0],
                "user_id": row[1],
                "username": row[2],
                "bot_username": row[3],
                "created_at": row[9].isoformat() if row[9] else None
            }

            # Check if batch mode (projects JSONB) or single mode (title)
            if row[8]:  # projects column (JSONB - already parsed by psycopg)
                entry["projects"] = row[8]
            else:  # single mode
                entry["title"] = row[4]
                entry["description"] = row[5]
                entry["hex_color"] = row[6]
                entry["parent_project_id"] = row[7]

            entries.append(entry)

        logger.info(f"[claim_project_queue] Claimed {len(entries)} entries for {username}")
        return JSONResponse(entries)

    except Exception as e:
        logger.error(f"[claim_project_queue] Error: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)

# @PRIVATE
@mcp.custom_route("/project-queue/{queue_id}/complete", methods=["POST"])
async def mark_queue_complete(request: Request):
    """Mark a queue entry as complete.

    Bead: solutions-eofy

    Called by frontend after successfully creating projects.
    """
    queue_id = request.path_params.get("queue_id")

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Missing or invalid Authorization header"}, status_code=401)

    token = auth_header[7:]

    # Verify token and get username
    try:
        import httpx
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        resp = httpx.get(
            f"{vikunja_url}/api/v1/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        resp.raise_for_status()
        user_data = resp.json()
        username = user_data.get("username")

        if not username:
            return JSONResponse({"error": "Could not determine username"}, status_code=401)

        # Mark as complete (only if owned by this user)
        from .token_broker import execute
        execute("""
            UPDATE project_creation_queue
            SET status = 'complete', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s AND username = %s
        """, (queue_id, username))

        return JSONResponse({"success": True})

    except Exception as e:
        logger.error(f"[mark_queue_complete] Error: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)


# @PRIVATE
@mcp.custom_route("/project-queue/{queue_id}/cancel", methods=["POST", "DELETE"])
async def cancel_queue_entry(request: Request):
    """Cancel/delete a queue entry.

    Bead: solutions-2iz3

    Allows user to cancel a queued project creation request.
    Only the owner can cancel their own queue entries.
    """
    queue_id = request.path_params.get("queue_id")

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse({"error": "Missing or invalid Authorization header"}, status_code=401)

    token = auth_header[7:]

    try:
        import httpx
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        resp = httpx.get(
            f"{vikunja_url}/api/v1/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        resp.raise_for_status()
        user_data = resp.json()
        username = user_data.get("username")

        if not username:
            return JSONResponse({"error": "Could not determine username"}, status_code=401)

        # Delete entry (only if owned by this user and still pending/processing)
        from .token_broker import execute
        rows = execute("""
            DELETE FROM project_creation_queue
            WHERE id = %s AND username = %s AND status IN ('pending', 'processing')
            RETURNING id, title, projects
        """, (queue_id, username))

        if rows:
            deleted = rows[0]
            title = deleted[1] or (deleted[2][0]["title"] if deleted[2] else "batch")
            logger.info(f"[cancel_queue_entry] User {username} cancelled queue entry {queue_id}: {title}")
            return JSONResponse({"success": True, "cancelled_id": queue_id, "title": title})
        else:
            return JSONResponse({"error": "Queue entry not found or already processed"}, status_code=404)

    except Exception as e:
        logger.error(f"[cancel_queue_entry] Error: {e}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500)


# =============================================================================
# EMAIL ACTION ENDPOINT
# =============================================================================

# @PRIVATE
@mcp.custom_route("/do/{token}", methods=["GET"])
async def execute_email_action(request: Request):
    """
    Execute an action from an email link.

    Email links contain signed, self-authenticating tokens that authorize
    specific actions without requiring the user to be logged in.

    Bead: fa-kwoh (onboarding email)
    Design: docs/EMAIL_ACTION_SERVICE_EXPLAINER.md

    URL format: /do/{base64_payload}.{signature}

    Example actions:
    - approve_project: Create queued project(s)
    - cancel_project: Cancel project creation request
    - complete_task: Mark a task as done
    """
    from .email_actions import execute_action

    token = request.path_params.get("token", "")

    if not token:
        return HTMLResponse(
            content=_action_error_html("Invalid link", "This link is missing required information."),
            status_code=400
        )

    # Execute the action
    result = execute_action(token)

    if result.get("success"):
        return HTMLResponse(
            content=_action_success_html(
                result.get("message", "Action completed!"),
                result.get("redirect"),
            )
        )
    else:
        return HTMLResponse(
            content=_action_error_html(
                "Action Failed",
                result.get("error", "An unknown error occurred."),
                result.get("error_type"),
            ),
            status_code=400
        )


# @PRIVATE
def _action_success_html(message: str, redirect_url: str = None) -> str:
    """Success page for email actions."""
    redirect_script = ""
    redirect_link = ""

    if redirect_url:
        redirect_script = f"""
        <script>
            setTimeout(function() {{
                window.location.href = "{redirect_url}";
            }}, 3000);
        </script>
        """
        redirect_link = f'<p style="margin-top: 20px;"><a href="{redirect_url}" style="color: #667eea;">Continue to Vikunja &rarr;</a></p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Success - Factumerit</title>
    {redirect_script}
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            padding: 40px;
            text-align: center;
        }}
        .icon {{
            font-size: 64px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #2e7d32;
            margin-bottom: 15px;
        }}
        p {{
            color: #666;
            font-size: 16px;
            line-height: 1.6;
        }}
        .redirect-notice {{
            margin-top: 20px;
            font-size: 14px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">&#10003;</div>
        <h1>Success!</h1>
        <p>{message}</p>
        {redirect_link}
        {f'<p class="redirect-notice">Redirecting in 3 seconds...</p>' if redirect_url else ''}
    </div>
</body>
</html>"""


# @PRIVATE
def _action_error_html(title: str, message: str, error_type: str = None) -> str:
    """Error page for email actions."""
    support_hint = ""
    if error_type == "expired":
        support_hint = "<p>Request a new link from your Vikunja bot or check your email for a more recent message.</p>"
    elif error_type == "no_user_token":
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
        support_hint = f'<p><a href="{vikunja_url}" style="color: #667eea;">Log into Vikunja</a> and try again.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Factumerit</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            padding: 40px;
            text-align: center;
        }}
        .icon {{
            font-size: 64px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #c62828;
            margin-bottom: 15px;
        }}
        p {{
            color: #666;
            font-size: 16px;
            line-height: 1.6;
        }}
        a {{
            color: #667eea;
        }}
        .support {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 14px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">&#9888;</div>
        <h1>{title}</h1>
        <p>{message}</p>
        {support_hint}
        <div class="support">
            <p>Need help? Contact <a href="mailto:support@factumerit.app">support@factumerit.app</a></p>
        </div>
    </div>
</body>
</html>"""


# @PRIVATE
@mcp.custom_route("/queue", methods=["GET"])
async def queue_processor(request: Request):
    """Serve the queue processor HTML page.

    Extensible endpoint for various queue operations (projects, tasks, etc).
    Currently handles project creation queue.

    Bead: solutions-eofy
    """
    import os
    from pathlib import Path

    # Try multiple possible locations for the HTML file
    possible_paths = [
        # Development: src/vikunja_mcp/server.py -> ../../static/
        Path(__file__).parent.parent.parent / "static" / "project-queue-processor.html",
        # Installed package: might be in site-packages root
        Path(__file__).parent.parent / "static" / "project-queue-processor.html",
        # Working directory relative
        Path.cwd() / "static" / "project-queue-processor.html",
    ]

    html_content = None
    for html_path in possible_paths:
        if html_path.exists():
            try:
                html_content = html_path.read_text()
                break
            except Exception as e:
                logger.error(f"Error reading {html_path}: {e}")
                continue

    if html_content:
        return HTMLResponse(content=html_content)
    else:
        # Log all attempted paths for debugging
        attempted = ", ".join(str(p) for p in possible_paths)
        logger.error(f"Queue HTML not found. Tried: {attempted}")
        return HTMLResponse(
            content=f"<h1>404 - Queue page not found</h1><p>Searched: {attempted}</p>",
            status_code=404
        )


# @PRIVATE
@mcp.custom_route("/authorize", methods=["GET"])
async def oauth_authorize(request: Request):
    """OAuth2 authorization endpoint with PKCE support."""
    params = request.query_params

    client_id = params.get("client_id")
    redirect_uri = params.get("redirect_uri")
    response_type = params.get("response_type")
    state = params.get("state")
    code_challenge = params.get("code_challenge")
    code_challenge_method = params.get("code_challenge_method", "S256")

    # Validate required params
    if response_type != "code":
        return JSONResponse({"error": "unsupported_response_type"}, status_code=400)

    if not redirect_uri:
        return JSONResponse({"error": "invalid_request", "message": "redirect_uri required"}, status_code=400)

    # For single-user setup, auto-approve (user is already authenticated to access this URL)
    # In a multi-user setup, you'd show a consent screen here

    # Generate authorization code
    code = _generate_code()
    _oauth_codes[code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
        "expires": time.time() + 600,  # 10 min expiry
    }

    # Redirect back with code
    redirect_params = {"code": code}
    if state:
        redirect_params["state"] = state

    redirect_url = f"{redirect_uri}?{urllib.parse.urlencode(redirect_params)}"
    return RedirectResponse(url=redirect_url, status_code=302)


# @PRIVATE
@mcp.custom_route("/token", methods=["POST"])
async def oauth_token(request: Request):
    """OAuth2 token endpoint - exchanges auth code for access token."""
    # Parse form data
    body = await request.body()
    params = dict(urllib.parse.parse_qsl(body.decode()))

    grant_type = params.get("grant_type")
    code = params.get("code")
    redirect_uri = params.get("redirect_uri")
    client_id = params.get("client_id")
    code_verifier = params.get("code_verifier")

    if grant_type != "authorization_code":
        return JSONResponse({"error": "unsupported_grant_type"}, status_code=400)

    # Validate code
    if code not in _oauth_codes:
        return JSONResponse({"error": "invalid_grant", "message": "Invalid or expired code"}, status_code=400)

    code_data = _oauth_codes[code]

    # Check expiry
    if time.time() > code_data["expires"]:
        del _oauth_codes[code]
        return JSONResponse({"error": "invalid_grant", "message": "Code expired"}, status_code=400)

    # Verify redirect_uri matches
    if redirect_uri != code_data["redirect_uri"]:
        return JSONResponse({"error": "invalid_grant", "message": "redirect_uri mismatch"}, status_code=400)

    # Verify PKCE
    if code_data["code_challenge"]:
        if not code_verifier:
            return JSONResponse({"error": "invalid_grant", "message": "code_verifier required"}, status_code=400)
        if not _verify_pkce(code_verifier, code_data["code_challenge"], code_data["code_challenge_method"]):
            return JSONResponse({"error": "invalid_grant", "message": "PKCE verification failed"}, status_code=400)

    # Generate access token
    access_token = _generate_token()
    _oauth_tokens[access_token] = {
        "client_id": client_id,
        "expires": time.time() + 86400 * 30,  # 30 day expiry
    }

    # Delete used code
    del _oauth_codes[code]

    return JSONResponse({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 86400 * 30,
    })


# @PRIVATE
@mcp.custom_route("/.well-known/oauth-authorization-server", methods=["GET"])
async def oauth_metadata(request: Request):
    """OAuth2 server metadata for auto-discovery."""
    # Get base URL from request
    base_url = f"{request.url.scheme}://{request.url.netloc}"

    return JSONResponse({
        "issuer": base_url,
        "authorization_endpoint": f"{base_url}/authorize",
        "token_endpoint": f"{base_url}/token",
        "registration_endpoint": f"{base_url}/register",  # Dynamic Client Registration
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256", "plain"],
        "token_endpoint_auth_methods_supported": ["none", "client_secret_post"],
    })


# In-memory client registration storage
_registered_clients = {}


# @PRIVATE
@mcp.custom_route("/register", methods=["POST"])
async def oauth_register(request: Request):
    """Dynamic Client Registration (RFC 7591)."""
    body = await request.body()
    try:
        client_metadata = json.loads(body.decode()) if body else {}
    except json.JSONDecodeError:
        client_metadata = {}

    # Generate client credentials
    client_id = secrets.token_urlsafe(16)
    client_secret = secrets.token_urlsafe(32)

    # Store client registration
    _registered_clients[client_id] = {
        "client_secret": client_secret,
        "redirect_uris": client_metadata.get("redirect_uris", []),
        "client_name": client_metadata.get("client_name", "Unknown"),
        "created": time.time(),
    }

    return JSONResponse({
        "client_id": client_id,
        "client_secret": client_secret,
        "client_id_issued_at": int(time.time()),
        "client_secret_expires_at": 0,  # Never expires
        "redirect_uris": client_metadata.get("redirect_uris", []),
        "token_endpoint_auth_method": "client_secret_post",
    }, status_code=201)


# @PRIVATE
def _protected_resource_response(request: Request) -> JSONResponse:
    """Build protected resource metadata response."""
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    return JSONResponse({
        "resource": f"{base_url}/mcp",  # MCP endpoint path
        "authorization_servers": [base_url],
        "bearer_methods_supported": ["header"],
        "mcp_endpoint": f"{base_url}/mcp",  # Explicit MCP endpoint for clients
    })


# @PRIVATE
@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET"])
async def oauth_protected_resource(request: Request):
    """OAuth2 Protected Resource Metadata (legacy path)."""
    return _protected_resource_response(request)


# @PRIVATE
@mcp.custom_route("/.well-known/protected-resource-metadata", methods=["GET"])
async def protected_resource_metadata(request: Request):
    """OAuth2 Protected Resource Metadata (RFC 9728)."""
    return _protected_resource_response(request)


# ============================================================================
# SLACK BOT INTEGRATION
# ============================================================================

import re
import random
import anthropic
from slack_bolt import App
from slack_bolt.adapter.starlette import SlackRequestHandler

# Latin thinking messages (rotating with varied emojis)
THINKING_MESSAGES = [
    ":hourglass_flowing_sand: Cogito...",    # I think...
    ":gear: Elaborans...",                    # Working on it...
    ":crystal_ball: Meditans...",             # Meditating...
    ":scales: Perpendo...",                   # I'm considering...
    ":clock3: Momento...",                    # Wait a moment...
    ":arrows_counterclockwise: In processu...",  # In progress...
    ":hammer_and_wrench: Labōrō...",          # I'm working...
    ":mag: Quaerens...",                      # Searching...
    ":bulb: Excogitans...",                   # Devising...
    ":seedling: Patientia...",                # Patience...
    ":scroll: Consultans...",                 # Consulting...
    ":books: Studeo...",                      # I'm studying...
]

# Initialize Slack app (lazy - only if env vars present)
_slack_app = None
_slack_handler = None


# @PRIVATE
def _get_slack_app():
    """Get or create Slack app (lazy initialization)."""
    global _slack_app, _slack_handler
    if _slack_app is None:
        bot_token = os.environ.get("SLACK_BOT_TOKEN")
        signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
        if not bot_token or not signing_secret:
            return None, None

        _slack_app = App(token=bot_token, signing_secret=signing_secret)

        # Register event handlers
# @PRIVATE
        @_slack_app.event("app_mention")
        def handle_mention(event, say, client):
            """Handle @mentions in channels.

            Privacy protection: Responds with ephemeral message (only visible to user)
            with a 'Share to channel' button. User controls what gets shared publicly.
            """
            text = event.get("text", "")
            channel = event.get("channel")
            user_id = event.get("user")
            # Check for attachments (not yet supported)
            if event.get("files"):
                file_types = [f.get("filetype", "file") for f in event["files"]]
                client.chat_postEphemeral(
                    channel=channel,
                    user=user_id,
                    text=f"I can't process attachments yet ({', '.join(file_types)}). Please describe what you need in text, or paste the content directly."
                )
                return
            clean_text = re.sub(r"<@[A-Z0-9]+>\s*", "", text).strip()
            if not clean_text:
                client.chat_postEphemeral(
                    channel=channel,
                    user=user_id,
                    text="Hi! How can I help you with Vikunja? (Your response will be private until you share it.)"
                )
                return
            # Reset ECO streak - using LLM costs tokens
            _reset_eco_streak(user_id)
            # Send thinking indicator (ephemeral)
            client.chat_postEphemeral(
                channel=channel,
                user=user_id,
                text=random.choice(THINKING_MESSAGES)
            )
            try:
                response = _slack_chat_with_claude(clean_text, user_id=user_id, client=client, channel=channel)
                # Send ephemeral response with share button for privacy
                blocks = _build_share_button_blocks(response)
                client.chat_postEphemeral(
                    channel=channel,
                    user=user_id,
                    text=response,  # Fallback for notifications
                    blocks=blocks
                )
            except Exception as e:
                client.chat_postEphemeral(
                    channel=channel,
                    user=user_id,
                    text=f"Error: {str(e)}"
                )

# @PRIVATE
        @_slack_app.action("share_to_channel")
        def handle_share_to_channel(ack, body, client):
            """Handle 'Share to channel' button click - post response publicly."""
            ack()
            channel = body.get("channel", {}).get("id")
            user_id = body.get("user", {}).get("id")
            # Get the response text from button value
            actions = body.get("actions", [])
            response_text = actions[0].get("value", "") if actions else ""

            if channel and response_text:
                # Post the response publicly to the channel
                client.chat_postMessage(
                    channel=channel,
                    text=f"<@{user_id}> shared:\n{response_text}"
                )

# @PRIVATE
        @_slack_app.event("message")
        def handle_dm(event, say, client):
            """Handle direct messages."""
            if event.get("bot_id") or event.get("channel_type") != "im":
                return
            text = event.get("text", "")
            channel = event.get("channel")
            user_id = event.get("user")
            # Check for attachments (not yet supported)
            if event.get("files"):
                file_types = [f.get("filetype", "file") for f in event["files"]]
                say(f"I can't process attachments yet ({', '.join(file_types)}). Please describe what you need in text, or paste the content directly.")
                return
            if not text:
                return
            # Reset ECO streak - using LLM costs tokens
            _reset_eco_streak(user_id)
            # Send thinking indicator
            thinking_msg = client.chat_postMessage(channel=channel, text=random.choice(THINKING_MESSAGES))
            try:
                response = _slack_chat_with_claude(text, user_id=user_id, client=client, channel=channel)
                say(response)
            except Exception as e:
                say(f"Error: {str(e)}")
            finally:
                # Try to delete thinking message (non-blocking if fails)
                try:
                    client.chat_delete(channel=channel, ts=thinking_msg["ts"])
                except Exception:
                    pass  # Bot may lack permission, that's ok

# @PRIVATE
        @_slack_app.event("team_join")
        def handle_team_join(event, client):
            """Send welcome DM when a new user joins the workspace."""
            try:
                user = event.get("user", {})
                user_id = user.get("id")
                if not user_id:
                    return

                # Skip bots
                if user.get("is_bot"):
                    return

                logger.info(f"New user joined workspace: {user_id}")

                # Open DM channel with the new user
                dm_response = client.conversations_open(users=[user_id])
                if not dm_response.get("ok"):
                    logger.error(f"Failed to open DM with {user_id}")
                    return

                channel_id = dm_response["channel"]["id"]

                # Send welcome message with connect prompt
                welcome_message = _get_welcome_message_for_new_user(user_id)
                client.chat_postMessage(channel=channel_id, text=welcome_message)

                logger.info(f"Sent welcome DM to new user {user_id}")
            except Exception as e:
                logger.error(f"Error handling team_join: {e}")

        # ====================================================================
        # SLASH COMMANDS - Pure API, no LLM cost
        # Multi-instance: queries ALL configured instances in parallel
        # ====================================================================

# @PRIVATE
        @_slack_app.command("/overdue")
        def slash_overdue(ack, respond, command):
            """Tasks past due date - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _overdue_tasks_impl, "Overdue Tasks"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/today")
        def slash_today(ack, respond, command):
            """Tasks due today + overdue - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _due_today_impl, "Due Today"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/week")
        def slash_week(ack, respond, command):
            """Tasks due this week - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _due_this_week_impl, "Due This Week"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/priority")
        def slash_priority(ack, respond, command):
            """High priority tasks (3+) - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _high_priority_tasks_impl, "High Priority Tasks"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/urgent")
        def slash_urgent(ack, respond, command):
            """Urgent tasks (priority 4+) - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _urgent_tasks_impl, "Urgent Tasks"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/unscheduled")
        def slash_unscheduled(ack, respond, command):
            """Tasks without due date - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _unscheduled_tasks_impl, "Unscheduled Tasks"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/focus")
        def slash_focus(ack, respond, command):
            """What to work on now (priority OR due today) - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            respond(_slash_command_multi_instance(user_id, _focus_now_impl, "Focus Now"), response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/summary")
        def slash_summary(ack, respond, command):
            """Quick task counts overview - no LLM cost, visible in channel."""
            ack()
            user_id = command.get("user_id")
            instances = _get_instances()
            if not instances:
                respond(":x: No Vikunja instances configured.")
                return
            _increment_eco_streak(user_id)
            result = _task_summary_impl()
            response = _format_summary_for_slack(result)
            response += _format_context_footer(user_id)
            response += _format_eco_footer(user_id)
            respond(response, response_type="in_channel")

# @PRIVATE
        @_slack_app.command("/usage")
        def slash_usage(ack, respond, command):
            """Show usage stats and toggle footer. Use: /usage, /usage on, /usage off"""
            ack()
            user_id = command.get("user_id")
            text = command.get("text", "").strip().lower()
            streak = _get_eco_streak(user_id)
            tokens_saved = streak * _TOKENS_PER_LLM_QUERY

            # Get lifetime usage info
            lifetime_budget = _get_lifetime_budget(user_id)
            lifetime_usage = _get_lifetime_usage(user_id)
            remaining = max(0, lifetime_budget - lifetime_usage)
            pct_used = (lifetime_usage / lifetime_budget * 100) if lifetime_budget > 0 else 0

            if text == "on":
                # Explicitly enable
                config = _load_config()
                if "user_preferences" not in config:
                    config["user_preferences"] = {}
                if user_id not in config["user_preferences"]:
                    config["user_preferences"][user_id] = {}
                config["user_preferences"][user_id]["show_usage_footer"] = True
                _save_config(config)
                new_state = True
            elif text == "off":
                # Explicitly disable
                config = _load_config()
                if "user_preferences" not in config:
                    config["user_preferences"] = {}
                if user_id not in config["user_preferences"]:
                    config["user_preferences"][user_id] = {}
                config["user_preferences"][user_id]["show_usage_footer"] = False
                _save_config(config)
                new_state = False
            else:
                # Toggle
                new_state = _toggle_usage_footer(user_id)

            # Build credit status line
            if remaining <= 0:
                credit_line = f":warning: *Free credit exhausted* (${lifetime_usage:.2f} used)"
            elif pct_used >= 80:
                credit_line = f":hourglass: *${remaining:.2f} remaining* of ${lifetime_budget:.2f} free credit ({pct_used:.0f}% used)"
            else:
                credit_line = f":white_check_mark: *${remaining:.2f} remaining* of ${lifetime_budget:.2f} free credit"

            if new_state:
                respond(
                    f"{credit_line}\n"
                    f"ECO streak: {streak} | ~{tokens_saved:,} tokens saved\n"
                    f"Usage footer: *ON*\n"
                    f"_Slash commands are always free!_"
                )
            else:
                respond(
                    f"{credit_line}\n"
                    f"ECO streak: {streak} | ~{tokens_saved:,} tokens saved\n"
                    f"Usage footer: *OFF*\n"
                    f"_Use `/usage on` to show per-message costs_"
                )

# @PRIVATE
        @_slack_app.command("/credits")
        def slash_credits(ack, respond, command):
            """[ADMIN] Manage user credits. Usage: /credits @user [add N|reset]"""
            ack()
            caller_id = command.get("user_id")
            text = command.get("text", "").strip()

            # Admin check
            if not _is_admin(caller_id):
                respond(":no_entry: This command is for admins only.")
                return

            # Parse arguments
            parts = text.split()
            if not parts:
                respond(
                    "*Usage:*\n"
                    "• `/credits @user` - Show user's credits\n"
                    "• `/credits @user add 5` - Add $5 to budget\n"
                    "• `/credits @user reset` - Reset to $1 default"
                )
                return

            # Extract target user
            target_id = _parse_slack_user_mention(parts[0])
            if not target_id:
                respond(f":warning: Invalid user mention: `{parts[0]}`\nUse format: `/credits @user`")
                return

            # Determine action
            if len(parts) == 1:
                # Show credits
                info = _get_user_credits_info(target_id)
                respond(
                    f"*Credits for <@{target_id}>:*\n"
                    f"• Budget: ${info['budget']:.2f}\n"
                    f"• Used: ${info['usage']:.2f}\n"
                    f"• Remaining: ${info['remaining']:.2f}"
                )
            elif parts[1].lower() == "add" and len(parts) >= 3:
                try:
                    amount = float(parts[2])
                    if amount <= 0:
                        respond(":warning: Amount must be positive")
                        return
                    result = _add_user_credits(target_id, amount)
                    respond(
                        f":white_check_mark: Added ${amount:.2f} to <@{target_id}>\n"
                        f"New budget: ${result['new_budget']:.2f}"
                    )
                except ValueError:
                    respond(f":warning: Invalid amount: `{parts[2]}`")
            elif parts[1].lower() == "reset":
                result = _reset_user_credits(target_id)
                respond(
                    f":arrows_counterclockwise: Reset <@{target_id}> to default\n"
                    f"• Old: ${result['old_budget']:.2f} budget, ${result['old_usage']:.2f} used\n"
                    f"• New: ${result['new_budget']:.2f} budget, ${result['new_usage']:.2f} used"
                )
            else:
                respond(
                    f":warning: Unknown action: `{parts[1]}`\n"
                    "Use `add N` or `reset`"
                )

# @PRIVATE
        @_slack_app.command("/role")
        def slash_role(ack, respond, command):
            """[ADMIN] Manage user roles. Usage: /role @user [set ROLE]"""
            ack()
            caller_id = command.get("user_id")
            text = command.get("text", "").strip()

            # Must have at least admin role to manage roles
            if not _has_role(caller_id, "admin"):
                caller_role = _get_user_role(caller_id)
                respond(f":no_entry: This command requires admin role. Your role: `{caller_role}`")
                return

            # Parse arguments
            parts = text.split()
            if not parts:
                respond(
                    "*Usage:*\n"
                    "• `/role @user` - Show user's role\n"
                    "• `/role @user set admin` - Set user's role\n"
                    "• `/role list` - List all users with roles\n\n"
                    f"*Available roles:* {', '.join(ROLE_HIERARCHY)}\n"
                    "*Note:* You can only grant roles below your own level."
                )
                return

            # Special: list all roles
            if parts[0].lower() == "list":
                config = _load_config()
                user_roles = config.get("user_roles", {})
                if not user_roles:
                    respond("No users have explicit roles assigned.")
                    return
                lines = ["*Users with roles:*"]
                for uid, info in user_roles.items():
                    role = info.get("role", "user") if isinstance(info, dict) else "user"
                    lines.append(f"• <@{uid}>: `{role}`")
                respond("\n".join(lines))
                return

            # Extract target user
            target_id = _parse_slack_user_mention(parts[0])
            if not target_id:
                respond(f":warning: Invalid user mention: `{parts[0]}`\nUse format: `/role @user`")
                return

            # Determine action
            if len(parts) == 1:
                # Show role
                role = _get_user_role(target_id)
                config = _load_config()
                role_info = config.get("user_roles", {}).get(target_id, {})
                granted_by = role_info.get("granted_by", "default") if isinstance(role_info, dict) else "default"
                granted_at = role_info.get("granted_at", "unknown") if isinstance(role_info, dict) else "unknown"
                respond(
                    f"*Role for <@{target_id}>:*\n"
                    f"• Role: `{role}`\n"
                    f"• Granted by: {granted_by}\n"
                    f"• Granted at: {granted_at}"
                )
            elif parts[1].lower() == "set" and len(parts) >= 3:
                new_role = parts[2].lower()
                if new_role not in ROLE_HIERARCHY:
                    respond(f":warning: Invalid role: `{new_role}`\nValid roles: {', '.join(ROLE_HIERARCHY)}")
                    return

                # Check if caller can grant this role
                if not _can_grant_role(caller_id, new_role):
                    caller_role = _get_user_role(caller_id)
                    respond(f":no_entry: You cannot grant `{new_role}` role.\nYour role `{caller_role}` can only grant roles below it.")
                    return

                # Prevent self-demotion for safety
                if target_id == caller_id:
                    respond(":warning: You cannot change your own role.")
                    return

                result = _set_user_role(target_id, new_role, caller_id)
                if "error" in result:
                    respond(f":warning: {result['error']}")
                else:
                    respond(
                        f":white_check_mark: Updated <@{target_id}> role\n"
                        f"• Old: `{result['old_role']}`\n"
                        f"• New: `{result['new_role']}`"
                    )
            else:
                respond(
                    f":warning: Unknown action: `{parts[1]}`\n"
                    "Use `set ROLE` to change a user's role"
                )

# @PRIVATE
        @_slack_app.command("/apikey")
        def slash_apikey(ack, respond, command):
            """Manage your Anthropic API key. Usage: /apikey [set|remove|status|help]"""
            ack()
            user_id = command.get("user_id")
            text = command.get("text", "").strip()

            # Parse subcommand
            parts = text.split(maxsplit=1)
            subcommand = parts[0].lower() if parts else ""

            if subcommand == "set":
                # Extract API key
                api_key = parts[1].strip() if len(parts) > 1 else ""

                if not api_key:
                    respond(
                        ":warning: *No API key provided*\n\n"
                        "Usage: `/apikey set sk-ant-api03-...`\n\n"
                        "_Tip: Create a dedicated key with a spending limit at console.anthropic.com_"
                    )
                    return

                # Basic format validation
                if not api_key.startswith("sk-"):
                    respond(
                        ":warning: *Invalid key format*\n\n"
                        "Anthropic API keys start with `sk-ant-` or `sk-`.\n"
                        "Get your key at: <https://console.anthropic.com/settings/keys|console.anthropic.com>"
                    )
                    return

                # Validate the key works
                respond(":hourglass: Validating API key...")
                is_valid, message = _validate_anthropic_api_key(api_key)

                if not is_valid:
                    respond(f":x: *Key validation failed*\n{message}")
                    return

                # Store encrypted
                result = _set_user_anthropic_api_key(user_id, api_key)
                respond(
                    ":white_check_mark: *API key saved!*\n\n"
                    "Your requests will now use your own API key.\n"
                    "• Usage counts against your Anthropic account\n"
                    "• No more free tier limits\n"
                    "• Use `/apikey status` to check\n"
                    "• Use `/apikey remove` to revert to free tier\n\n"
                    "_Your key is stored encrypted and never logged._"
                )

            elif subcommand == "remove":
                result = _remove_user_anthropic_api_key(user_id)
                if result["had_key"]:
                    respond(
                        ":white_check_mark: *API key removed*\n\n"
                        "You're now back on the free tier ($1 lifetime credit).\n"
                        "_Don't forget to also revoke the key at console.anthropic.com_"
                    )
                else:
                    respond(":information_source: No API key was stored.")

            elif subcommand == "status":
                status = _get_user_api_key_status(user_id)
                if status["has_key"]:
                    set_at = status.get("set_at", "unknown")
                    if set_at and set_at != "unknown":
                        try:
                            dt = datetime.fromisoformat(set_at.replace("Z", "+00:00"))
                            set_at = dt.strftime("%Y-%m-%d")
                        except Exception:
                            pass
                    respond(
                        ":key: *API Key Status*\n\n"
                        f"• Status: *Active* (using your key)\n"
                        f"• Set on: {set_at}\n"
                        "• Your usage counts against your Anthropic account\n\n"
                        "_Use `/apikey remove` to revert to free tier_"
                    )
                else:
                    respond(
                        ":key: *API Key Status*\n\n"
                        "• Status: *Not set* (using free tier)\n"
                        "• Free credit remaining: check with `/usage`\n\n"
                        "_Use `/apikey set <key>` to add your own key_"
                    )

            else:
                # Help / default
                respond(
                    ":key: *Bring Your Own API Key*\n\n"
                    "Use your own Anthropic API key for unlimited usage.\n\n"
                    "*Commands:*\n"
                    "• `/apikey set <key>` - Add your API key\n"
                    "• `/apikey remove` - Remove key, use free tier\n"
                    "• `/apikey status` - Check current status\n\n"
                    "*How to create a safe, limited key:*\n"
                    "1. Go to <https://console.anthropic.com/settings/keys|console.anthropic.com>\n"
                    "2. Create a new API key (name it 'vikunja-bot')\n"
                    "3. *Important:* Set a spending limit (e.g., $10/month) at\n"
                    "   <https://console.anthropic.com/settings/limits|console.anthropic.com/settings/limits>\n"
                    "4. Copy the key and run `/apikey set <your-key>`\n\n"
                    "*Security:*\n"
                    "• Your key is encrypted at rest\n"
                    "• Never logged or transmitted elsewhere\n"
                    "• You can revoke it anytime at console.anthropic.com\n"
                    "• Setting a spend limit protects you from surprise bills"
                )

# @PRIVATE
        @_slack_app.command("/connections")
        def slash_connections(ack, respond, command):
            """Show connected Vikunja instances - no LLM cost."""
            ack()
            respond(_format_instances_for_slack())

# @PRIVATE
        @_slack_app.command("/project")
        def slash_project(ack, respond, command):
            """Set or show active project context."""
            ack()
            user_id = command.get("user_id")
            text = command.get("text", "").strip()

            if not text:
                # Show current active project
                result = _get_active_project_impl(user_id)
                respond(_format_project_for_slack(result))
            else:
                # Set active project - parse "name" or "name N"
                parts = text.rsplit(maxsplit=1)
                if len(parts) == 2 and parts[1].isdigit():
                    query, selection = parts[0], int(parts[1])
                else:
                    query, selection = text, 0
                result = _set_active_project_impl(user_id, query, selection)
                respond(_format_project_for_slack(result))

# @PRIVATE
        @_slack_app.command("/clear")
        def slash_clear(ack, respond, command):
            """Clear active project context."""
            ack()
            user_id = command.get("user_id")
            result = _clear_active_project_impl(user_id)
            respond(_format_project_for_slack(result))

# @PRIVATE
        @_slack_app.command("/connect")
        def slash_connect(ack, respond, command):
            """Connect a Vikunja instance. Always private."""
            ack()
            text = command.get("text", "").strip()
            parts = text.split()

            if len(parts) < 3:
                respond(
                    ":information_source: *Usage:* `/connect <name> <url> <token>`\n\n"
                    "*Example:*\n"
                    "`/connect personal vikunja.example.com abc123...`\n\n"
                    "*Get your token:*\n"
                    "1. Log into your Vikunja instance\n"
                    "2. Go to Settings > API Tokens\n"
                    "3. Create a new token and copy it here"
                )
                return

            name, url, token = parts[0], parts[1], parts[2]
            result = _connect_instance_impl(name, url, token)

            if "error" in result:
                respond(f":x: {result['error']}")
            else:
                respond(
                    f":white_check_mark: Connected *{result['name']}* as {result['username']}\n"
                    f"URL: {result['url']}\n\n"
                    f"Use `/connections` to see all instances."
                )

# @PRIVATE
        @_slack_app.command("/disconnect")
        def slash_disconnect(ack, respond, command):
            """Disconnect a Vikunja instance. Always private."""
            ack()
            name = command.get("text", "").strip()

            if not name:
                # Show available instances
                instances = _get_instances()
                if instances:
                    names = ", ".join(instances.keys())
                    respond(f":information_source: *Usage:* `/disconnect <name>`\n\nAvailable: {names}")
                else:
                    respond(":information_source: No instances configured.")
                return

            result = _disconnect_instance_impl(name)

            if "error" in result:
                respond(f":x: {result['error']}")
            else:
                respond(f":white_check_mark: Disconnected *{result['name']}*")

# @PRIVATE
        @_slack_app.command("/help")
        def slash_help(ack, respond, command):
            """Show help for Factum Erit commands."""
            ack()
            topic = command.get("text", "").strip()
            respond(_format_help_for_slack(topic))

        _slack_handler = SlackRequestHandler(_slack_app)

    return _slack_app, _slack_handler


# Expensive tools excluded from Slack (too many tokens, high cost)
SLACK_EXCLUDED_TOOLS = {"search_all", "list_all_tasks", "list_all_projects"}

# Tool definitions for Claude API (Slack bot) - generated from TOOL_REGISTRY
SLACK_TOOLS = [
    {"name": name, "description": tool["description"], "input_schema": tool["input_schema"]}
    for name, tool in TOOL_REGISTRY.items()
    if name not in SLACK_EXCLUDED_TOOLS
] + [
    # Slack-specific tool for timezone
    {
        "name": "set_user_timezone",
        "description": "Set the user's preferred timezone for displaying dates/times",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {"type": "string", "description": "Timezone name (e.g., America/Los_Angeles, America/New_York, Europe/London, Asia/Tokyo)"}
            },
            "required": ["timezone"]
        }
    },
    # Slack-specific tool for token usage display
    {
        "name": "toggle_token_usage",
        "description": "Toggle display of token usage and cost estimate after each response",
        "input_schema": {
            "type": "object",
            "properties": {
                "enable": {"type": "boolean", "description": "True to show token usage, False to hide, omit to toggle"}
            }
        }
    },
    # Slack-specific tool for model selection
    {
        "name": "set_model",
        "description": "Set the AI model to use: 'haiku' (fastest/cheapest), 'sonnet' (balanced), 'opus' (most capable). Omit model param to see current setting.",
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Model name: haiku, sonnet, or opus"}
            }
        }
    },
    # Slack-specific tool for memory settings
    {
        "name": "set_memory",
        "description": "View or change conversation memory settings. Memory lets the bot remember previous messages in the conversation. Strategies: 'none' (no memory), 'rolling' (last N messages). Omit params to view current settings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "strategy": {"type": "string", "description": "Memory strategy: 'none' or 'rolling'"},
                "window": {"type": "integer", "description": "Number of message pairs to remember (1-50, default 10)"}
            }
        }
    },
    # Reset conversation / clear memory
    {
        "name": "reset_conversation",
        "description": "Start fresh - forget all previous messages in this conversation. Use when user says 'new conversation', 'start over', 'clear history', 'forget everything', etc.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    # Admin tool for user management
    {
        "name": "admin_set_user_token",
        "description": "ADMIN ONLY: Set a user's Vikunja API token. Requires the target user's Slack ID and their Vikunja token.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target_slack_id": {"type": "string", "description": "Slack user ID of the user to configure (e.g., U1234567890)"},
                "vikunja_token": {"type": "string", "description": "The user's Vikunja API token"}
            },
            "required": ["target_slack_id", "vikunja_token"]
        }
    },
    # Admin tool to list configured users
    {
        "name": "admin_list_users",
        "description": "ADMIN ONLY: List all configured users and their status.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    # Admin tool to connect a new Vikunja instance
    {
        "name": "admin_connect_instance",
        "description": "ADMIN ONLY: Connect to a new Vikunja instance. Use for adding additional instances (e.g., 'connect to cloud at https://app.vikunja.cloud with token tk_xxx').",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name for the instance (e.g., 'cloud', 'work')"},
                "url": {"type": "string", "description": "Base URL of the Vikunja instance (e.g., 'https://app.vikunja.cloud')"},
                "token": {"type": "string", "description": "API token for the instance"}
            },
            "required": ["name", "url", "token"]
        }
    },
    # Instance management tools (available to all users)
    {
        "name": "list_instances",
        "description": "List all configured Vikunja instances and show which one is currently active. Use when user asks 'what instances do I have', 'which instance am I on', etc.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "switch_instance",
        "description": "Switch to a different Vikunja instance. Use when user wants to work with a different instance (e.g., 'switch to cloud', 'use personal instance').",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the instance to switch to"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "rename_instance",
        "description": "Rename a Vikunja instance. Use when user wants to change an instance name (e.g., 'rename default to personal').",
        "input_schema": {
            "type": "object",
            "properties": {
                "old_name": {"type": "string", "description": "Current name of the instance"},
                "new_name": {"type": "string", "description": "New name for the instance"}
            },
            "required": ["old_name", "new_name"]
        }
    }
]

# Legacy alias for backward compatibility
ADMIN_SLACK_IDS = ADMIN_USER_IDS


# @PRIVATE
def _is_admin(user_id: str) -> bool:
    """Check if user has admin privileges (admin or owner role).

    This is a backward-compatible wrapper around the new RBAC system.
    For new code, prefer using _has_role() or _has_capability() directly.
    """
    return _has_role(user_id, "admin")


# @PRIVATE
def _get_user_timezone(user_id: str, client) -> str:
    """Get user's timezone from Slack API or cached override."""
    # Check for user override in config
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    if user_config.get("timezone_override"):
        return user_config["timezone_override"]

    # Try to get from Slack API (cache result)
    if user_config.get("timezone"):
        return user_config["timezone"]

    try:
        result = client.users_info(user=user_id)
        tz = result["user"].get("tz", "UTC")
        # Cache it
        if "users" not in config:
            config["users"] = {}
        if user_id not in config["users"]:
            config["users"][user_id] = {}
        config["users"][user_id]["timezone"] = tz
        _save_config(config)
        return tz
    except Exception:
        return "UTC"


# @PRIVATE
def _set_user_timezone_override(user_id: str, timezone: str) -> dict:
    """Set user's timezone override."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    config["users"][user_id]["timezone_override"] = timezone
    _save_config(config)
    return {"user_id": user_id, "timezone": timezone, "set": True}


# @PRIVATE
def _get_user_timezone_override(user_id: str) -> str:
    """Get user's timezone override (for Matrix, no Slack API needed)."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    return user_config.get("timezone_override", "")


# @PRIVATE
def _get_user_show_token_usage(user_id: str) -> bool:
    """Get user's preference for showing token usage."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    return user_config.get("show_token_usage", False)


# @PRIVATE
def _set_user_show_token_usage(user_id: str, show: bool) -> dict:
    """Set user's preference for showing token usage."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    config["users"][user_id]["show_token_usage"] = show
    _save_config(config)
    return {"user_id": user_id, "show_token_usage": show}


# @PRIVATE
def _get_user_model(user_id: str) -> str:
    """Get user's preferred model (haiku, sonnet, opus)."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    return user_config.get("model", DEFAULT_MODEL)


# @PRIVATE
def _set_user_model(user_id: str, model: str) -> dict:
    """Set user's preferred model."""
    if model not in AVAILABLE_MODELS:
        return {"error": f"Unknown model: {model}. Available: {', '.join(AVAILABLE_MODELS.keys())}"}
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    config["users"][user_id]["model"] = model
    _save_config(config)
    return {"user_id": user_id, "model": model, "model_id": AVAILABLE_MODELS[model]}


# @PRIVATE
def _get_user_usage(user_id: str) -> dict:
    """Get user's cumulative token usage for current month."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    usage = user_config.get("usage", {})
    current_month = datetime.now().strftime("%Y-%m")
    month_usage = usage.get(current_month, {"input_tokens": 0, "output_tokens": 0, "cost": 0.0})
    return month_usage


# @PRIVATE
def _update_user_usage(user_id: str, input_tokens: int, output_tokens: int, model: str) -> dict:
    """Update user's cumulative token usage and return updated totals."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    if "usage" not in config["users"][user_id]:
        config["users"][user_id]["usage"] = {}

    current_month = datetime.now().strftime("%Y-%m")
    if current_month not in config["users"][user_id]["usage"]:
        config["users"][user_id]["usage"][current_month] = {
            "input_tokens": 0,
            "output_tokens": 0,
            "cost": 0.0
        }

    # Calculate cost for this request
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["sonnet"])
    msg_cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000

    # Update cumulative totals
    month_data = config["users"][user_id]["usage"][current_month]
    month_data["input_tokens"] += input_tokens
    month_data["output_tokens"] += output_tokens
    month_data["cost"] += msg_cost

    _save_config(config)
    return month_data


# @PRIVATE
def _format_usage_message(input_tokens: int, output_tokens: int, model: str, cumulative: dict) -> str:
    """Format usage message with per-message and cumulative stats, plus alerts."""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["sonnet"])
    msg_cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000
    total_tokens = input_tokens + output_tokens

    monthly_cost = cumulative.get("cost", 0.0)

    # Base message - always show model for transparency
    msg = f"_{model} | {total_tokens:,} tokens (~${msg_cost:.4f}) | Month: ${monthly_cost:.2f}_"

    # Add alerts based on thresholds
    if monthly_cost >= COST_ALERT_THRESHOLD:
        msg += f"\n⚠️ _Approaching ${CLAUDE_PRO_COST}/mo. Consider Claude Pro for unlimited claude.ai usage._"
    elif model != "haiku" and msg_cost > 0.01:
        msg += f"\n💡 _Tip: 'set model haiku' for cheaper responses._"

    return msg


# @PRIVATE
def _get_user_memory_settings(user_id: str) -> dict:
    """Get user's memory settings (strategy and window size)."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    memory = user_config.get("memory", {})
    return {
        "strategy": memory.get("strategy", DEFAULT_MEMORY_STRATEGY),
        "window": memory.get("window", DEFAULT_MEMORY_WINDOW)
    }


# @PRIVATE
def _get_project_llm_instructions(project_id: int) -> str | None:
    """Get LLM instructions for a specific project.

    Returns the llm_instructions field from project config, or None if not set.
    """
    config = _load_config()
    project_config = config.get("projects", {}).get(str(project_id))
    if not project_config:
        return None
    return project_config.get("llm_instructions")


# @PRIVATE
def _get_active_project_instructions() -> str | None:
    """Get LLM instructions for the currently active project context.

    Returns instructions if:
    1. User has set an active project via set_active_context()
    2. That project has llm_instructions configured

    Returns None otherwise.
    """
    config = _load_config()
    mcp_context = config.get("mcp_context", {})
    project_id = mcp_context.get("project_id", 0)

    if not project_id:
        return None

    return _get_project_llm_instructions(project_id)


# @PRIVATE
def _set_user_memory_settings(user_id: str, strategy: str = None, window: int = None) -> dict:
    """Set user's memory settings."""
    if strategy and strategy not in MEMORY_STRATEGIES:
        return {"error": f"Unknown strategy: {strategy}. Available: {', '.join(MEMORY_STRATEGIES)}"}

    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    if "memory" not in config["users"][user_id]:
        config["users"][user_id]["memory"] = {}

    if strategy:
        config["users"][user_id]["memory"]["strategy"] = strategy
    if window is not None:
        config["users"][user_id]["memory"]["window"] = max(1, min(50, window))  # Clamp 1-50

    _save_config(config)
    return _get_user_memory_settings(user_id)


# @PRIVATE
def _reset_user_conversation(user_id: str) -> dict:
    """Reset conversation by storing current timestamp - messages before this are ignored."""
    import time
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    config["users"][user_id]["memory_reset_ts"] = str(time.time())
    _save_config(config)
    return {"status": "Conversation reset. I've forgotten our previous messages."}


# @PRIVATE
def _fetch_slack_history(client, channel: str, limit: int = 20, user_id: str = None) -> list:
    """Fetch recent messages from Slack channel/DM.

    Returns list of dicts with 'role' (user/assistant) and 'content'.
    Respects memory_reset_ts if set for the user.
    """
    if not client or not channel:
        return []

    # Check for memory reset timestamp
    reset_ts = None
    if user_id:
        config = _load_config()
        reset_ts = config.get("users", {}).get(user_id, {}).get("memory_reset_ts")

    try:
        # Get bot's user ID to identify assistant messages
        auth_info = client.auth_test()
        bot_user_id = auth_info.get("user_id")

        # Fetch conversation history
        result = client.conversations_history(
            channel=channel,
            limit=limit * 2 + 1  # Fetch extra to account for system messages
        )

        messages = []
        for msg in reversed(result.get("messages", [])):  # Oldest first
            # Skip messages before reset timestamp
            if reset_ts and float(msg.get("ts", "0")) < float(reset_ts):
                continue

            # Skip bot's "thinking" messages and system messages
            if msg.get("subtype"):
                continue

            text = msg.get("text", "").strip()
            if not text:
                continue

            user = msg.get("user")
            if user == bot_user_id:
                # Strip usage footer from bot messages to prevent Claude echoing it
                # Pattern: _model | N tokens (~$X.XX) | Month: $X.XX_
                # Generic: any word + " | " + digits + " tokens" + anything until "_"
                text = re.sub(r'\n*_\w+\s*\|\s*[\d,]+\s*tokens[^_]+_\s*$', '', text, flags=re.IGNORECASE).strip()
                messages.append({"role": "assistant", "content": text})
            else:
                messages.append({"role": "user", "content": text})

        return messages
    except Exception as e:
        # Log error but don't fail - just proceed without history
        print(f"Error fetching Slack history: {e}")
        return []


# @PRIVATE
def _build_conversation_history(client, channel: str, user_id: str, current_message: str) -> list:
    """Build conversation history for Claude based on user's memory settings.

    Returns list of messages in Claude format, ending with current user message.
    """
    settings = _get_user_memory_settings(user_id)
    strategy = settings["strategy"]
    window = settings["window"]

    if strategy == "none":
        # No memory - just the current message
        return [{"role": "user", "content": current_message}]

    # Rolling strategy - fetch last N message pairs
    history = _fetch_slack_history(client, channel, limit=window * 2, user_id=user_id)

    # Remove the current message if it's already in history (it usually is)
    if history and history[-1].get("content") == current_message:
        history = history[:-1]

    # Ensure we don't exceed window (count pairs)
    pair_count = 0
    trimmed = []
    for msg in reversed(history):
        if msg["role"] == "user":
            pair_count += 1
        if pair_count > window:
            break
        trimmed.insert(0, msg)

    # Ensure conversation starts with user message (Claude requirement)
    while trimmed and trimmed[0]["role"] != "user":
        trimmed = trimmed[1:]

    # Ensure alternating roles (Claude requirement)
    cleaned = []
    last_role = None
    for msg in trimmed:
        if msg["role"] != last_role:
            cleaned.append(msg)
            last_role = msg["role"]
        else:
            # Merge consecutive same-role messages
            if cleaned:
                cleaned[-1]["content"] += "\n\n" + msg["content"]

    # Add current message
    if cleaned and cleaned[-1]["role"] == "user":
        # Merge with last user message
        cleaned[-1]["content"] += "\n\n" + current_message
    else:
        cleaned.append({"role": "user", "content": current_message})

    return cleaned


# @PRIVATE
def _get_user_limits(user_id: str) -> dict:
    """Get user's usage limits (daily/monthly budget and action)."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    limits = user_config.get("limits", {})
    return {
        "daily_budget": limits.get("daily_budget", DEFAULT_DAILY_BUDGET),
        "monthly_budget": limits.get("monthly_budget", DEFAULT_MONTHLY_BUDGET),
        "action": limits.get("action", DEFAULT_LIMIT_ACTION)
    }


# @PRIVATE
def _get_daily_usage(user_id: str) -> float:
    """Get user's usage for today."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    usage = user_config.get("usage", {})
    today = datetime.now().strftime("%Y-%m-%d")
    daily = usage.get("daily", {})
    return daily.get(today, 0.0)


# @PRIVATE
def _update_daily_usage(user_id: str, cost: float) -> float:
    """Update user's daily usage and return new total."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}
    if "usage" not in config["users"][user_id]:
        config["users"][user_id]["usage"] = {}
    if "daily" not in config["users"][user_id]["usage"]:
        config["users"][user_id]["usage"]["daily"] = {}

    today = datetime.now().strftime("%Y-%m-%d")
    current = config["users"][user_id]["usage"]["daily"].get(today, 0.0)
    new_total = current + cost
    config["users"][user_id]["usage"]["daily"][today] = new_total
    _save_config(config)
    return new_total


# @PRIVATE
def _get_lifetime_usage(user_id: str) -> float:
    """Get user's lifetime usage (never resets)."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    return user_config.get("lifetime_usage", 0.0)


# @PRIVATE
def _update_lifetime_usage(user_id: str, cost: float) -> float:
    """Update user's lifetime usage and return new total."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}

    current = config["users"][user_id].get("lifetime_usage", 0.0)
    new_total = current + cost
    config["users"][user_id]["lifetime_usage"] = new_total
    _save_config(config)
    return new_total


# @PRIVATE
def _get_lifetime_budget(user_id: str) -> float:
    """Get user's lifetime budget (default $1, can be increased)."""
    config = _load_config()
    users = config.get("users", {})
    user_config = users.get(user_id, {})
    return user_config.get("lifetime_budget", DEFAULT_LIFETIME_BUDGET)


# @PRIVATE
def _parse_slack_user_mention(text: str) -> str | None:
    """Extract user ID from Slack mention format like <@U12345ABC> or <@U12345ABC|username>."""
    if not text:
        return None
    match = re.match(r"<@([A-Z0-9]+)(?:\|[^>]*)?>", text)
    return match.group(1) if match else None


# @PRIVATE
def _add_user_credits(user_id: str, amount: float) -> dict:
    """Add credits to user's lifetime budget."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}

    old_budget = config["users"][user_id].get("lifetime_budget", DEFAULT_LIFETIME_BUDGET)
    new_budget = old_budget + amount
    config["users"][user_id]["lifetime_budget"] = new_budget
    _save_config(config)

    return {"user_id": user_id, "old_budget": old_budget, "new_budget": new_budget, "added": amount}


# @PRIVATE
def _reset_user_credits(user_id: str) -> dict:
    """Reset user to default state ($1 budget, $0 usage)."""
    config = _load_config()
    if "users" not in config:
        config["users"] = {}
    if user_id not in config["users"]:
        config["users"][user_id] = {}

    old_budget = config["users"][user_id].get("lifetime_budget", DEFAULT_LIFETIME_BUDGET)
    old_usage = config["users"][user_id].get("lifetime_usage", 0.0)

    config["users"][user_id]["lifetime_budget"] = DEFAULT_LIFETIME_BUDGET
    config["users"][user_id]["lifetime_usage"] = 0.0
    _save_config(config)

    return {
        "user_id": user_id,
        "old_budget": old_budget,
        "old_usage": old_usage,
        "new_budget": DEFAULT_LIFETIME_BUDGET,
        "new_usage": 0.0
    }


# @PRIVATE
def _get_user_credits_info(user_id: str) -> dict:
    """Get user's credit info."""
    budget = _get_lifetime_budget(user_id)
    usage = _get_lifetime_usage(user_id)
    return {
        "user_id": user_id,
        "budget": budget,
        "usage": usage,
        "remaining": max(0, budget - usage)
    }


# @PRIVATE
def _check_usage_limits(user_id: str) -> dict:
    """Check if user is within lifetime usage limit.

    Returns dict with:
      - allowed: bool (can make API call)
      - model_override: str or None (force different model)
      - warning: str or None (message to append)
    """
    lifetime_budget = _get_lifetime_budget(user_id)
    lifetime_usage = _get_lifetime_usage(user_id)
    remaining = lifetime_budget - lifetime_usage

    # Lifetime exhausted - block
    if remaining <= 0:
        return {
            "allowed": False,
            "model_override": None,
            "warning": (
                f"You've used your free ${lifetime_budget:.2f} credit!\n\n"
                "To continue using AI chat:\n"
                "• Add your API key: `/apikey your-key`\n"
                "• Or contact admin for more credits\n\n"
                "_Your tasks are safe at vikunja.factumerit.app_\n"
                "_Slash commands like `/today` still work free!_"
            )
        }

    # Approaching limit (80%)
    if remaining <= lifetime_budget * 0.2:
        pct = (lifetime_usage / lifetime_budget) * 100
        return {
            "allowed": True,
            "model_override": None,
            "warning": f"_${remaining:.2f} remaining of ${lifetime_budget:.2f} free credit ({pct:.0f}% used)_"
        }

    return {"allowed": True, "model_override": None, "warning": None}


# @PRIVATE
def _slack_execute_tool(name: str, args: dict, user_id: str = None) -> str:
    """Execute a Vikunja tool for Slack bot using TOOL_REGISTRY dispatch."""
    # Handle Slack-specific tools
    if name == "set_user_timezone":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        try:
            import pytz
            tz = args.get("timezone", "UTC")
            # Validate timezone
            pytz.timezone(tz)
            result = _set_user_timezone_override(user_id, tz)
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Invalid timezone: {e}"})

    if name == "toggle_token_usage":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        enable = args.get("enable")
        if enable is None:
            # Toggle current state
            current = _get_user_show_token_usage(user_id)
            enable = not current
        result = _set_user_show_token_usage(user_id, enable)
        return json.dumps(result, indent=2)

    if name == "set_model":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        model = args.get("model", "").lower()
        if not model:
            # Return current model and available options
            current = _get_user_model(user_id)
            return json.dumps({
                "current_model": current,
                "available_models": list(AVAILABLE_MODELS.keys()),
                "hint": "Use set_model with model='haiku', 'sonnet', or 'opus'"
            }, indent=2)
        result = _set_user_model(user_id, model)
        return json.dumps(result, indent=2)

    if name == "set_memory":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        strategy = args.get("strategy")
        window = args.get("window")
        if not strategy and window is None:
            # Return current settings
            settings = _get_user_memory_settings(user_id)
            return json.dumps({
                "current_strategy": settings["strategy"],
                "current_window": settings["window"],
                "available_strategies": MEMORY_STRATEGIES,
                "hint": "Use set_memory with strategy='none' or 'rolling', and optionally window=N (1-50)"
            }, indent=2)
        result = _set_user_memory_settings(user_id, strategy=strategy, window=window)
        return json.dumps(result, indent=2)

    if name == "reset_conversation":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        result = _reset_user_conversation(user_id)
        return json.dumps(result, indent=2)

    # Admin tools
    if name == "admin_set_user_token":
        if not user_id or not _is_admin(user_id):
            return json.dumps({"error": "This command is admin-only"})
        target_id = args.get("target_slack_id")
        token = args.get("vikunja_token")
        if not target_id or not token:
            return json.dumps({"error": "Both target_slack_id and vikunja_token are required"})
        result = _set_user_vikunja_token(target_id, token)
        return json.dumps(result, indent=2)

    if name == "admin_list_users":
        if not user_id or not _is_admin(user_id):
            return json.dumps({"error": "This command is admin-only"})
        config = _load_config()
        users = config.get("users", {})
        user_list = []
        for uid, uconfig in users.items():
            user_list.append({
                "slack_id": uid,
                "has_vikunja_token": bool(uconfig.get("vikunja_token")),
                "model": uconfig.get("model", DEFAULT_MODEL),
                "memory_strategy": uconfig.get("memory_strategy", DEFAULT_MEMORY_STRATEGY)
            })
        return json.dumps({"users": user_list, "count": len(user_list)}, indent=2)

    if name == "admin_connect_instance":
        if not user_id or not _is_admin(user_id):
            return json.dumps({"error": "This command is admin-only"})
        inst_name = args.get("name")
        url = args.get("url")
        token = args.get("token")
        if not inst_name or not url or not token:
            return json.dumps({"error": "name, url, and token are required"})
        result = _connect_instance(inst_name, url, token)
        return json.dumps(result, indent=2)

    # Instance management tools (available to all users)
    if name == "list_instances":
        instances = _get_instances()
        current = _get_current_instance()
        result = {
            "instances": [
                {"name": n, "url": inst.get("url"), "is_current": n == current}
                for n, inst in instances.items()
            ],
            "current": current
        }
        return json.dumps(result, indent=2)

    if name == "switch_instance":
        inst_name = args.get("name")
        if not inst_name:
            return json.dumps({"error": "name is required"})
        try:
            instances = _get_instances()
            if inst_name not in instances:
                available = ", ".join(instances.keys()) if instances else "none configured"
                return json.dumps({"error": f"Instance '{inst_name}' not found. Available: {available}"})
            _set_current_instance(inst_name)
            return json.dumps({
                "switched_to": inst_name,
                "url": instances[inst_name].get("url")
            }, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    if name == "rename_instance":
        old_name = args.get("old_name")
        new_name = args.get("new_name")
        if not old_name or not new_name:
            return json.dumps({"error": "old_name and new_name are required"})
        try:
            result = _rename_instance(old_name, new_name)
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # Block expensive tools in Slack
    if name in SLACK_EXCLUDED_TOOLS:
        return json.dumps({
            "error": f"Tool '{name}' is disabled in Slack (too expensive). Use list_tasks or list_projects for a specific project instead."
        })

    if name not in TOOL_REGISTRY:
        return json.dumps({"error": f"Unknown tool: {name}"})

    # Validate required parameters before calling impl
    tool_def = TOOL_REGISTRY[name]
    required_params = tool_def.get("input_schema", {}).get("required", [])
    missing = [p for p in required_params if p not in args or args[p] is None]
    if missing:
        # Return helpful error that guides Claude to correct tool
        tool_desc = tool_def.get("description", "")
        return json.dumps({
            "error": f"Missing required parameter(s): {', '.join(missing)}",
            "tool": name,
            "description": tool_desc,
            "hint": f"Did you mean to use a different tool? Check available tools and their required parameters."
        })

    try:
        result = TOOL_REGISTRY[name]["impl"](**args)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


# @PRIVATE
def _slack_chat_with_claude(user_message: str, user_id: str = None, client=None, channel: str = None) -> str:
    """Send message to Claude and handle tool calls for Slack bot."""
    # Check for user's own API key first (BYOK)
    using_own_key = False
    if user_id:
        user_api_key = _get_user_anthropic_api_key(user_id)
        if user_api_key:
            api_key = user_api_key
            using_own_key = True
        else:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        return "Error: ANTHROPIC_API_KEY not configured"

    # Check if user has a Vikunja token configured
    if user_id:
        user_vikunja_token = _get_user_vikunja_token(user_id)
        if not user_vikunja_token:
            # Admins can still use the bot for admin operations (they'll use env var token)
            if not _is_admin(user_id):
                return _get_connect_prompt(user_id)
        else:
            # Set the token and user ID in context for this request
            # CRITICAL: Both must be set for _request to use correct instance URL
            _current_vikunja_token.set(user_vikunja_token)
            _current_user_id.set(user_id)  # Fix: solutions-1qcp - enables per-instance URL lookup

    claude = anthropic.Anthropic(api_key=api_key)

    # Check usage limits before proceeding (skip if user has own key)
    limit_warning = None
    if user_id and not using_own_key:
        limit_check = _check_usage_limits(user_id)
        if not limit_check["allowed"]:
            return limit_check["warning"]
        limit_warning = limit_check.get("warning")
        model_override = limit_check.get("model_override")
    else:
        model_override = None

    # Build conversation history based on user's memory settings
    messages = _build_conversation_history(client, channel, user_id, user_message)

    # Check if user wants token usage reported (stored preference)
    show_usage = _get_user_show_token_usage(user_id) if user_id else False

    # Get user's model preference (may be overridden by limits)
    user_model_key = _get_user_model(user_id) if user_id else DEFAULT_MODEL
    if model_override:
        user_model_key = model_override
    model_id = AVAILABLE_MODELS.get(user_model_key, AVAILABLE_MODELS[DEFAULT_MODEL])

    # Track cumulative token usage across tool-use loop
    total_input_tokens = 0
    total_output_tokens = 0

    # Get user's timezone
    try:
        import pytz
        user_tz = _get_user_timezone(user_id, client) if user_id and client else "UTC"
        tz = pytz.timezone(user_tz)
        now = datetime.now(tz)
        current_time = now.strftime("%Y-%m-%d %H:%M %Z")
    except Exception:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")
        user_tz = "server local"

    # Build system prompt with optional project-specific instructions
    system_prompt_parts = [f"""You are a helpful assistant that manages tasks in Vikunja, a project management tool.
Current date/time: {current_time} ({user_tz}). Task timestamps in Vikunja are UTC.

CRITICAL RULES:
- You MUST use tools to perform actions. NEVER claim you did something without calling the tool.
- NEVER make up task or project data. ALWAYS use tools to fetch real data from Vikunja.
- If a tool fails or returns no results, say so honestly - DO NOT invent fake task names, dates, or details.
- You CANNOT access websites or external URLs. Work only with information the user provides.
- If asked to look something up online, explain you can't and proceed with available info.
- Only report task/project creation AFTER the tool returns success.

Be concise - this is a chat interface.
You have set_user_timezone, toggle_token_usage, set_model, and set_memory tools for preferences.
This conversation has memory - I can see our previous messages."""]

    # Add project-specific instructions if active project has them
    project_instructions = _get_active_project_instructions()
    if project_instructions:
        system_prompt_parts.append(f"\n\nPROJECT-SPECIFIC INSTRUCTIONS:\n{project_instructions}")

    system_prompt = "".join(system_prompt_parts)

    while True:
        try:
            response = claude.messages.create(
                model=model_id,
                max_tokens=1024,
                system=system_prompt,
                tools=SLACK_TOOLS,
                messages=messages
            )
        except anthropic.AuthenticationError as e:
            # User's BYOK key is invalid
            if using_own_key:
                return (
                    ":x: *Your API key is invalid*\n\n"
                    "Your stored API key was rejected by Anthropic. This usually means:\n"
                    "• The key was copied incorrectly\n"
                    "• The key has been revoked\n"
                    "• The key has expired\n\n"
                    "*To fix:*\n"
                    "1. Check your key at <https://console.anthropic.com/settings/keys|console.anthropic.com>\n"
                    "2. Update it: `/apikey set sk-ant-...`\n"
                    "3. Or remove it to use free tier: `/apikey remove`"
                )
            else:
                # Admin's key is invalid - shouldn't happen
                return f"Error: Admin API key is invalid. Contact support. ({e})"

        # Track token usage
        if hasattr(response, 'usage'):
            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = _slack_execute_tool(block.name, block.input, user_id=user_id)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result
                    })
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text

            # Update cumulative usage and append usage message if requested
            if user_id:
                cumulative = _update_user_usage(user_id, total_input_tokens, total_output_tokens, user_model_key)
                # Calculate cost for this request
                pricing = MODEL_PRICING.get(user_model_key, MODEL_PRICING["sonnet"])
                msg_cost = (total_input_tokens * pricing["input"] + total_output_tokens * pricing["output"]) / 1_000_000

                # Only track against free tier limits if using our key (not BYOK)
                if not using_own_key:
                    # Track lifetime usage (never resets)
                    _update_lifetime_usage(user_id, msg_cost)
                    # Also track daily usage (legacy, for reporting)
                    _update_daily_usage(user_id, msg_cost)

                if show_usage:
                    usage_msg = _format_usage_message(total_input_tokens, total_output_tokens, user_model_key, cumulative)
                    if using_own_key:
                        usage_msg += " (using your API key)"
                    final_text += f"\n\n{usage_msg}"

            # Add limit warning if present
            if limit_warning:
                final_text += f"\n\n{limit_warning}"

            # Convert markdown to Slack mrkdwn format
            return _md_to_slack_mrkdwn(final_text)


# ============================================================================
# MATRIX LLM INTEGRATION
# ============================================================================

# Expensive tools excluded from Matrix (too many tokens, high cost)
MATRIX_EXCLUDED_TOOLS = {"search_all", "list_all_tasks", "list_all_projects"}

# Tool definitions for Claude API (Matrix bot) - generated from TOOL_REGISTRY
MATRIX_TOOLS = [
    {"name": name, "description": tool["description"], "input_schema": tool["input_schema"]}
    for name, tool in TOOL_REGISTRY.items()
    if name not in MATRIX_EXCLUDED_TOOLS
] + [
    # Matrix-specific tool for timezone
    {
        "name": "set_user_timezone",
        "description": "Set the user's preferred timezone for displaying dates/times",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {"type": "string", "description": "Timezone name (e.g., America/Los_Angeles, America/New_York, Europe/London, Asia/Tokyo)"}
            },
            "required": ["timezone"]
        }
    },
    # Matrix-specific tool for token usage display
    {
        "name": "toggle_token_usage",
        "description": "Toggle display of token usage and cost estimate after each response",
        "input_schema": {
            "type": "object",
            "properties": {
                "enable": {"type": "boolean", "description": "True to show token usage, False to hide, omit to toggle"}
            }
        }
    },
    # Matrix-specific tool for model selection
    {
        "name": "set_model",
        "description": "Set the AI model to use: 'haiku' (fastest/cheapest), 'sonnet' (balanced), 'opus' (most capable). Omit model param to see current setting.",
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Model name: haiku, sonnet, or opus"}
            }
        }
    },
    # Matrix-specific tool for memory settings
    {
        "name": "set_memory",
        "description": "View or change conversation memory settings. Memory lets the bot remember previous messages in the conversation. Strategies: 'none' (no memory), 'rolling' (last N messages). Omit params to view current settings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "strategy": {"type": "string", "description": "Memory strategy: none, rolling"},
                "window": {"type": "integer", "description": "Number of message pairs to remember (1-50)"}
            }
        }
    },
    # Matrix-specific tool for resetting conversation
    {
        "name": "reset_conversation",
        "description": "Clear conversation memory - the bot will forget previous messages. Use when switching topics or starting fresh.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    # Instance management tools (multi-instance support)
    {
        "name": "list_instances",
        "description": "List all connected Vikunja instances and show which one is currently active. Use when user asks 'what instances do I have', 'which instance am I on', 'show my instances'.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "switch_instance",
        "description": "Switch to a different Vikunja instance. Use when user wants to work with a different instance (e.g., 'switch to business', 'use personal instance', 'go to work tasks').",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the instance to switch to (e.g., 'personal', 'business', 'work')"}
            },
            "required": ["name"]
        }
    },
]


# @PRIVATE
def _matrix_execute_tool(name: str, args: dict, user_id: str = None) -> str:
    """Execute a Vikunja tool for Matrix bot using TOOL_REGISTRY dispatch."""
    # Handle Matrix-specific tools (same as Slack equivalents)
    if name == "set_user_timezone":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        try:
            import pytz
            tz = args.get("timezone", "UTC")
            # Validate timezone
            pytz.timezone(tz)
            result = _set_user_timezone_override(user_id, tz)
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Invalid timezone: {e}"})

    if name == "toggle_token_usage":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        enable = args.get("enable")
        if enable is None:
            # Toggle current state
            current = _get_user_show_token_usage(user_id)
            enable = not current
        result = _set_user_show_token_usage(user_id, enable)
        return json.dumps(result, indent=2)

    if name == "set_model":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        model = args.get("model", "").lower()
        if not model:
            # Return current model and available options
            current = _get_user_model(user_id)
            return json.dumps({
                "current_model": current,
                "available_models": list(AVAILABLE_MODELS.keys()),
                "hint": "Use set_model with model='haiku', 'sonnet', or 'opus'"
            }, indent=2)
        result = _set_user_model(user_id, model)
        return json.dumps(result, indent=2)

    if name == "set_memory":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        strategy = args.get("strategy")
        window = args.get("window")
        if not strategy and window is None:
            # Return current settings
            settings = _get_user_memory_settings(user_id)
            return json.dumps({
                "current_strategy": settings["strategy"],
                "current_window": settings["window"],
                "available_strategies": MEMORY_STRATEGIES,
                "hint": "Use set_memory with strategy='none' or 'rolling', and optionally window=N (1-50)"
            }, indent=2)
        result = _set_user_memory_settings(user_id, strategy=strategy, window=window)
        return json.dumps(result, indent=2)

    if name == "reset_conversation":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        result = _reset_user_conversation(user_id)
        return json.dumps(result, indent=2)

    # Instance management tools (use PostgreSQL-based context system)
    if name == "list_instances":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        from .token_broker import get_user_instances, get_user_active_instance
        instances = get_user_instances(user_id)
        current = get_user_active_instance(user_id)
        if not instances:
            return json.dumps({
                "instances": [],
                "current": None,
                "message": "No Vikunja instances connected. Use !vik to connect."
            }, indent=2)
        return json.dumps({
            "instances": list(instances),
            "current": current,
            "message": f"Active instance: {current}" if current else "No active instance"
        }, indent=2)

    if name == "switch_instance":
        if not user_id:
            return json.dumps({"error": "User ID not available"})
        inst_name = args.get("name", "").strip().lower()
        if not inst_name:
            return json.dumps({"error": "Instance name is required"})
        from .token_broker import get_user_instances
        from .context import switch_instance as ctx_switch_instance
        instances = get_user_instances(user_id)
        if inst_name not in instances:
            available = ", ".join(instances) if instances else "none"
            return json.dumps({
                "error": f"Instance '{inst_name}' not found. Available: {available}"
            })
        # Switch instance (also restores project context for that instance)
        ctx = ctx_switch_instance(user_id, inst_name)
        result = {
            "switched_to": inst_name,
            "message": f"Switched to {inst_name}"
        }
        if ctx.project:
            result["project_restored"] = ctx.project.project_name
            result["message"] += f" (project: {ctx.project.project_name})"
        return json.dumps(result, indent=2)

    # Block expensive tools in Matrix
    if name in MATRIX_EXCLUDED_TOOLS:
        return json.dumps({
            "error": f"Tool '{name}' is disabled in Matrix (too expensive). Use list_tasks or list_projects for a specific project instead."
        })

    if name not in TOOL_REGISTRY:
        return json.dumps({"error": f"Unknown tool: {name}"})

    # Validate required parameters before calling impl
    tool_def = TOOL_REGISTRY[name]
    required_params = tool_def.get("input_schema", {}).get("required", [])
    missing = [p for p in required_params if p not in args or args[p] is None]
    if missing:
        # Return helpful error that guides Claude to correct tool
        tool_desc = tool_def.get("description", "")
        return json.dumps({
            "error": f"Missing required parameter(s): {', '.join(missing)}",
            "tool": name,
            "description": tool_desc,
            "hint": f"Did you mean to use a different tool? Check available tools and their required parameters."
        })

    try:
        result = TOOL_REGISTRY[name]["impl"](**args)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


# @PRIVATE
def _fetch_matrix_history(room_id: str, limit: int = 20, user_id: str = None) -> list:
    """Fetch recent messages from Matrix room for conversation history.

    Returns list of dicts with 'role' (user/assistant) and 'content'.
    Respects memory_reset_ts if set for the user.

    Args:
        room_id: Matrix room ID
        limit: Maximum number of messages to fetch
        user_id: User ID for memory_reset_ts check
    """
    from .matrix_client import get_matrix_bot_instance
    import re

    # Check for memory reset timestamp
    reset_ts = None
    if user_id:
        config = _load_config()
        reset_ts = config.get("users", {}).get(user_id, {}).get("memory_reset_ts")
        # Convert to milliseconds if needed
        if reset_ts:
            reset_ts = float(reset_ts) * 1000  # Convert to milliseconds

    # Get bot instance
    bot = get_matrix_bot_instance()
    if not bot:
        logger.warning("Matrix bot instance not available for conversation history")
        return []

    # Get bot's user ID
    bot_user_id = bot.user_id

    try:
        # Get cached message history from bot
        cached_messages = bot.get_message_history(room_id, limit=limit * 2)

        messages = []
        for timestamp, sender, text in cached_messages:
            # Skip messages before reset timestamp
            if reset_ts and timestamp < reset_ts:
                continue

            text = text.strip()
            if not text:
                continue

            if sender == bot_user_id:
                # Strip usage footer from bot messages to prevent Claude echoing it
                # Pattern: _model | N tokens (~$X.XX) | Month: $X.XX_
                text = re.sub(r'\n*_\w+\s*\|\s*[\d,]+\s*tokens[^_]+_\s*$', '', text, flags=re.IGNORECASE).strip()
                messages.append({"role": "assistant", "content": text})
            else:
                messages.append({"role": "user", "content": text})

        return messages

    except Exception as e:
        # Log error but don't fail - just proceed without history
        logger.error(f"Error fetching Matrix history: {e}")
        return []


# @PRIVATE
def _build_matrix_conversation_history(room_id: str, user_id: str, current_message: str) -> list:
    """Build conversation history for Claude based on user's memory settings.

    Returns list of messages in Claude format, ending with current user message.
    """
    settings = _get_user_memory_settings(user_id)
    strategy = settings["strategy"]
    window = settings["window"]

    if strategy == "none":
        # No memory - just the current message
        return [{"role": "user", "content": current_message}]

    # Rolling strategy - fetch last N message pairs
    history = _fetch_matrix_history(room_id, limit=window * 2, user_id=user_id)

    # Remove the current message if it's already in history
    if history and history[-1].get("content") == current_message:
        history = history[:-1]

    # Ensure we don't exceed window (count pairs)
    pair_count = 0
    trimmed = []
    for msg in reversed(history):
        if msg["role"] == "user":
            pair_count += 1
        if pair_count > window:
            break
        trimmed.insert(0, msg)

    # Ensure conversation starts with user message (Claude requirement)
    while trimmed and trimmed[0]["role"] != "user":
        trimmed = trimmed[1:]

    # Ensure alternating roles (Claude requirement)
    cleaned = []
    last_role = None
    for msg in trimmed:
        if msg["role"] != last_role:
            cleaned.append(msg)
            last_role = msg["role"]

    # Add current message
    cleaned.append({"role": "user", "content": current_message})

    return cleaned


# @PRIVATE
def _matrix_chat_with_claude(user_message: str, user_id: str = None, room_id: str = None) -> str:
    """Send message to Claude and handle tool calls for Matrix bot.

    This is the Matrix equivalent of _slack_chat_with_claude().
    Supports BYOK, usage limits, conversation memory, and tool execution.
    """
    # Check for user's own API key first (BYOK)
    using_own_key = False
    if user_id:
        user_api_key = _get_user_anthropic_api_key(user_id)
        if user_api_key:
            api_key = user_api_key
            using_own_key = True
            # Debug logging
            key_prefix = api_key[:20] if len(api_key) >= 20 else api_key
            key_suffix = api_key[-10:] if len(api_key) >= 10 else ""
            logger.info(f"Using BYOK for user {user_id}: prefix={key_prefix}... suffix=...{key_suffix} length={len(api_key)}")
        else:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            logger.info(f"No BYOK for user {user_id}, using admin key")
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        logger.info("No user_id, using admin key")

    if not api_key:
        return "Error: ANTHROPIC_API_KEY not configured. Contact admin or use `!apikey` to set your own key."

    # Check if user has a Vikunja token configured
    if user_id:
        user_vikunja_token = _get_user_vikunja_token(user_id)
        if not user_vikunja_token:
            return _get_matrix_connect_prompt(user_id)
        else:
            # Set the token and user ID in context for this request
            # CRITICAL: Both must be set for _request to use correct instance URL
            _current_vikunja_token.set(user_vikunja_token)
            _current_user_id.set(user_id)  # Fix: solutions-1qcp - enables per-instance URL lookup
            # Debug: Log which token is being used
            token_preview = user_vikunja_token[:10] + "..." if len(user_vikunja_token) > 10 else user_vikunja_token
            logger.info(f"Matrix user {user_id} using token: {token_preview}")

    claude = anthropic.Anthropic(api_key=api_key)

    # Check usage limits before proceeding (skip if user has own key)
    limit_warning = None
    if user_id and not using_own_key:
        limit_check = _check_usage_limits(user_id)
        if not limit_check["allowed"]:
            return limit_check["warning"]
        limit_warning = limit_check.get("warning")
        model_override = limit_check.get("model_override")
    else:
        model_override = None

    # Build conversation history based on user's memory settings
    messages = _build_matrix_conversation_history(room_id, user_id, user_message)

    # Check if user wants token usage reported (stored preference)
    show_usage = _get_user_show_token_usage(user_id) if user_id else False

    # Get user's model preference (may be overridden by limits)
    user_model_key = _get_user_model(user_id) if user_id else DEFAULT_MODEL
    if model_override:
        user_model_key = model_override
    model_id = AVAILABLE_MODELS.get(user_model_key, AVAILABLE_MODELS[DEFAULT_MODEL])

    # Track cumulative token usage across tool-use loop
    total_input_tokens = 0
    total_output_tokens = 0

    # Get user's timezone
    try:
        import pytz
        user_tz = _get_user_timezone_override(user_id) if user_id else "UTC"
        if not user_tz:
            user_tz = "UTC"
        tz = pytz.timezone(user_tz)
        now = datetime.now(tz)
        current_time = now.strftime("%Y-%m-%d %H:%M %Z")
    except Exception:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")
        user_tz = "server local"

    # Build system prompt with optional project-specific instructions
    system_prompt_parts = [f"""You are a helpful assistant that manages tasks in Vikunja, a project management tool.
Current date/time: {current_time} ({user_tz}). Task timestamps in Vikunja are UTC.

CRITICAL RULES:
- You MUST use tools to perform actions. NEVER claim you did something without calling the tool.
- NEVER make up task or project data. ALWAYS use tools to fetch real data from Vikunja.
- If a tool fails or returns no results, say so honestly - DO NOT invent fake task names, dates, or details.
- You CANNOT access websites or external URLs. Work only with information the user provides.
- If asked to look something up online, explain you can't and proceed with available info.
- Only report task/project creation AFTER the tool returns success.

Be concise - this is a chat interface.
You have set_user_timezone, toggle_token_usage, set_model, and set_memory tools for preferences.
This conversation has memory - I can see our previous messages."""]

    # Add project-specific instructions if active project has them
    project_instructions = _get_active_project_instructions()
    if project_instructions:
        system_prompt_parts.append(f"\n\nPROJECT-SPECIFIC INSTRUCTIONS:\n{project_instructions}")

    system_prompt = "".join(system_prompt_parts)

    while True:
        try:
            response = claude.messages.create(
                model=model_id,
                max_tokens=1024,
                system=system_prompt,
                tools=MATRIX_TOOLS,
                messages=messages
            )
        except anthropic.AuthenticationError as e:
            # Log detailed error for debugging
            logger.error(f"Anthropic AuthenticationError: {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'no dict'}")

            # User's BYOK key is invalid
            if using_own_key:
                return (
                    "❌ **Your API key is invalid**\n\n"
                    "Your stored API key was rejected by Anthropic. This usually means:\n"
                    "• The key was copied incorrectly\n"
                    "• The key has been revoked\n"
                    "• The key has expired\n\n"
                    "**To fix:**\n"
                    "1. Check your key at https://console.anthropic.com/settings/keys\n"
                    "2. Update it: `!apikey sk-ant-...`\n"
                    "3. Or remove it to use free tier: `!apikey clear`\n\n"
                    f"_Debug: {str(e)[:100]}_"
                )
            else:
                # Admin's key is invalid - shouldn't happen
                return f"Error: Admin API key is invalid. Contact support. ({e})"

        # Track token usage
        if hasattr(response, 'usage'):
            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = _matrix_execute_tool(block.name, block.input, user_id=user_id)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result
                    })
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text

            # Update cumulative usage and append usage message if requested
            if user_id:
                cumulative = _update_user_usage(user_id, total_input_tokens, total_output_tokens, user_model_key)
                # Calculate cost for this request
                pricing = MODEL_PRICING.get(user_model_key, MODEL_PRICING["sonnet"])
                msg_cost = (total_input_tokens * pricing["input"] + total_output_tokens * pricing["output"]) / 1_000_000

                # Only track against free tier limits if using our key (not BYOK)
                if not using_own_key:
                    # Track lifetime usage (never resets)
                    _update_lifetime_usage(user_id, msg_cost)
                    # Also track daily usage (legacy, for reporting)
                    _update_daily_usage(user_id, msg_cost)

                if show_usage:
                    usage_msg = _format_usage_message(total_input_tokens, total_output_tokens, user_model_key, cumulative)
                    if using_own_key:
                        usage_msg += " (using your API key)"
                    final_text += f"\n\n{usage_msg}"

            # Add limit warning if present
            if limit_warning:
                final_text += f"\n\n{limit_warning}"

            return final_text


# ============================================================================
# VIKUNJA-NATIVE @EIS LLM INTEGRATION
# ============================================================================

# Import tool registry for allowed tools
from .tool_registry import VIKUNJA_TOOLS, is_allowed, needs_confirmation, ConfirmLevel, check_tier_for_tool

# Build Claude API tool definitions from VIKUNJA_TOOLS
# Only includes tools that are allowed for Vikunja-native @eis
VIKUNJA_NATIVE_TOOLS = []
for tool_name in VIKUNJA_TOOLS.keys():
    if tool_name in TOOL_REGISTRY:
        tool = TOOL_REGISTRY[tool_name]
        VIKUNJA_NATIVE_TOOLS.append({
            "name": tool_name,
            "description": tool["description"],
            "input_schema": tool["input_schema"]
        })


# @PRIVATE
def _vikunja_execute_tool(
    name: str,
    args: dict,
    project_id: int,
    pending_confirmation: dict = None,
    model: str = "haiku"
) -> tuple[str, bool, dict | None]:
    """Execute a tool for Vikunja-native @eis.

    Args:
        name: Tool name
        args: Tool arguments
        project_id: Current project ID (for scope enforcement)
        pending_confirmation: If provided, contains confirmation state
        model: Current model ("haiku", "sonnet", "opus") for tier check (fa-qld6)

    Returns:
        Tuple of (result_json, needs_confirm, confirmation_info)
        - result_json: JSON string of result (or error)
        - needs_confirm: True if tool requires user confirmation
        - confirmation_info: Info for confirmation prompt (if needs_confirm)
    """
    import json

    # Check if tool is allowed
    if not is_allowed(name):
        return json.dumps({
            "error": f"Tool '{name}' is not available. Use tools from the project scope."
        }), False, None

    # Check model tier requirement (fa-qld6)
    allowed, tier_error = check_tier_for_tool(name, model)
    if not allowed:
        return json.dumps({"error": tier_error}), False, None

    # Check if tool exists in registry
    if name not in TOOL_REGISTRY:
        return json.dumps({"error": f"Unknown tool: {name}"}), False, None

    # Enforce project scope - inject project_id where applicable
    # This ensures @eis can only operate within its assigned project
    tool_def = TOOL_REGISTRY[name]
    required_params = tool_def.get("input_schema", {}).get("required", [])

    if "project_id" in required_params and "project_id" not in args:
        args["project_id"] = project_id

    # Count items for batch operations
    item_count = 1
    if name.startswith("batch_") or name.startswith("bulk_"):
        # Estimate item count from args
        if "tasks" in args:
            item_count = len(args.get("tasks", []))
        elif "task_ids" in args:
            item_count = len(args.get("task_ids", []))
        elif "labels" in args:
            item_count = len(args.get("labels", []))

    # Check if confirmation needed
    if needs_confirmation(name, item_count):
        tool_info = VIKUNJA_TOOLS.get(name)
        confirm_info = {
            "tool": name,
            "args": args,
            "item_count": item_count,
            "confirm_level": tool_info.confirm.value if tool_info else "always"
        }
        return json.dumps({
            "confirmation_required": True,
            "tool": name,
            "description": f"This operation requires confirmation",
            "item_count": item_count
        }), True, confirm_info

    # Validate required parameters
    missing = [p for p in required_params if p not in args or args[p] is None]
    if missing:
        tool_desc = tool_def.get("description", "")
        return json.dumps({
            "error": f"Missing required parameter(s): {', '.join(missing)}",
            "tool": name,
            "description": tool_desc,
            "hint": "Check tool parameters and try again."
        }), False, None

    # Execute the tool
    try:
        logger.info(f"[vikunja_execute_tool] Calling {name} with args: {args}")
        result = TOOL_REGISTRY[name]["impl"](**args)
        logger.info(f"[vikunja_execute_tool] {name} returned successfully")
        return json.dumps(result, indent=2, default=str), False, None
    except Exception as e:
        logger.exception(f"Vikunja-native tool {name} failed")
        return json.dumps({"error": str(e)}), False, None


# @PRIVATE
def vikunja_chat_with_claude(
    user_message: str,
    project_id: int,
    project_name: str = "",
    max_turns: int = 10,
    conversation_context: str = None,
    model: str = "haiku",
    requesting_user: str = None,
    requesting_user_id: int = None,
) -> tuple[str, int, int, int]:
    """Send message to Claude and handle tool calls for Vikunja-native @eis.

    Args:
        user_message: The user's request (extracted from @eis mention)
        project_id: The project @eis is operating in
        project_name: Project name for context
        max_turns: Maximum tool-calling iterations
        conversation_context: Previous conversation history (task + comments)
        model: Model to use - "haiku" (default, cheapest), "sonnet", or "opus"
        requesting_user: Username who triggered @eis (for auto-sharing projects)
        requesting_user_id: Numeric user ID (avoids needing user search API)

    Returns:
        Tuple of (response_text, input_tokens, output_tokens, turns_used)
    """
    import anthropic
    import json

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY not configured", 0, 0, 0

    # Get bot token for tool calls (solutions-bvw1)
    # Tools need a Vikunja token to make API calls - use VIKUNJA_BOT_TOKEN
    bot_token = os.environ.get("VIKUNJA_BOT_TOKEN")
    if not bot_token:
        return "Error: VIKUNJA_BOT_TOKEN not configured", 0, 0, 0

    # Strip whitespace that might cause auth issues (solutions-zja1)
    bot_token = bot_token.strip()

    # Debug: Log token being set (solutions-zja1)
    logger.info(f"[vikunja_chat_with_claude] Setting bot token: {bot_token[:20]}... (length: {len(bot_token)})")

    # Set context variables so tools can authenticate with Vikunja API
    # This is critical - without this, tools will fail with "No token available"
    # Also set bot_mode=True so _request() uses env vars instead of YAML config (solutions-zja1)
    token_reset = _current_vikunja_token.set(bot_token)
    bot_mode_reset = _bot_mode.set(True)
    user_reset = _requesting_user.set(requesting_user)
    user_id_reset = _requesting_user_id.set(requesting_user_id)

    try:
        claude = anthropic.Anthropic(api_key=api_key)

        # Get current time
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        current_time = now.strftime("%Y-%m-%d %H:%M UTC")

        # Build system prompt - Claude via Vikunja (parity with Claude Desktop + MCP)
        system_prompt = f"""You are Claude, accessed through Vikunja. The user is communicating with you via task titles and comments in the project "{project_name}".

Current date/time: {current_time}

BE HELPFUL:
- Answer questions directly using your knowledge (don't deflect to "create a task")
- Have natural conversations - you're Claude, not a limited bot
- Be concise since responses appear in task comments
- For bulk operations: just do it, don't explain each step - summarize at the end

VIKUNJA TOOLS (use when managing tasks/projects):
- Create, update, complete, and query tasks
- Create projects and subprojects
- Only use tools when the user explicitly wants to manage their stuff
- If a tool fails, say so honestly

⚠️ CRITICAL: You MUST actually CALL tools, not just describe what you would do.
- WRONG: "I'll create a project called X" (just text - nothing happens!)
- RIGHT: [call create_project tool] then "Created project X"
- If you find yourself writing "I'll create...", STOP and USE THE TOOL instead
- NEVER mention project IDs you haven't received from a tool response

SUBPROJECT CREATION (two-step process):
When user wants a subproject under an existing project (e.g., "create Ukulele under Music"):
1. FIRST call list_projects to find the parent project's ID
2. THEN call create_project with parent_project_id set to that ID
Never skip step 1 - you need the real parent ID.

PROJECT CREATION (IMPORTANT):
When creating projects, you MUST create them under an existing project so the user can see them.
Do NOT create top-level projects (without parent_project_id) - the user won't be able to see them!

Logic:
1. If user specifies a location ("under Hobbies", "in Work"), find that project and use it as parent
2. If no location specified, create under user's Inbox as default

Steps:
1. Call list_projects to find the parent project ID (specified location or Inbox)
2. Call create_project with parent_project_id set to that ID
3. If user wants to move it later, use update_project with parent_project_id=0 (root) or another ID

Examples:
- "Create a project for surfing" → list_projects, create under Inbox
- "Create a surfing project under Hobbies" → list_projects to find Hobbies ID, create under it
- "Create a Music project and put it at root level" → create under Inbox, then update_project(parent_project_id=0)
- "What's overdue?" → Use query tools to check tasks"""

        # Build initial message with conversation context if available
        if conversation_context:
            full_message = f"""Previous conversation:
{conversation_context}

Current request: {user_message}"""
        else:
            full_message = user_message

        messages = [{"role": "user", "content": full_message}]

        total_input_tokens = 0
        total_output_tokens = 0
        turns = 0
        tool_calls_made = 0  # Track actual tool executions

        while turns < max_turns:
            turns += 1
            try:
                # Map model name to Claude model ID
                model_ids = {
                    "haiku": "claude-3-5-haiku-20241022",
                    "sonnet": "claude-sonnet-4-20250514",
                    "opus": "claude-opus-4-20250514",
                }
                model_id = model_ids.get(model, model_ids["haiku"])

                response = claude.messages.create(
                    model=model_id,
                    max_tokens=4096,
                    system=system_prompt,
                    tools=VIKUNJA_NATIVE_TOOLS,
                    messages=messages
                )
            except anthropic.AuthenticationError as e:
                return f"Error: API key is invalid ({e})", 0, 0, turns
            except Exception as e:
                logger.exception("Claude API call failed")
                return f"Error: {e}", total_input_tokens, total_output_tokens, turns

            # Track token usage
            if hasattr(response, 'usage'):
                total_input_tokens += response.usage.input_tokens
                total_output_tokens += response.usage.output_tokens

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        logger.info(f"[vikunja_chat] Claude requested tool: {block.name}, args: {block.input}")
                        result_json, needs_confirm, confirm_info = _vikunja_execute_tool(
                            block.name, block.input, project_id, model=model  # fa-qld6: pass model for tier check
                        )
                        if needs_confirm:
                            # For now, return confirmation prompt instead of continuing
                            # Future: implement async confirmation flow
                            return (
                                f"⚠️ **Confirmation required**\n\n"
                                f"This operation (`{block.name}`) requires confirmation.\n"
                                f"Reply with `@eis yes` to confirm or `@eis no` to cancel."
                            ), total_input_tokens, total_output_tokens, turns

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_json
                        })
                        tool_calls_made += 1
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
            else:
                # End of tool-calling loop
                logger.info(f"[vikunja_chat] Claude finished with stop_reason={response.stop_reason}, turns={turns}, tool_calls={tool_calls_made}")
                final_text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_text += block.text

                # Warn if Claude claims to have done something but made no tool calls
                hallucination_indicators = ["created", "i've created", "i have created", "done", "completed", "deleted", "added"]
                if tool_calls_made == 0 and any(ind in final_text.lower() for ind in hallucination_indicators):
                    logger.warning(f"[vikunja_chat] POSSIBLE HALLUCINATION: Response claims action but 0 tools called. Text: {final_text[:300]}")
                    # Add warning to user (solutions-2dum)
                    final_text += "\n\n---\n⚠️ *I may not have executed this action. Please verify in Vikunja.*"

                # Flush pending projects and add approval links (solutions-eofy, solutions-v36up)
                pending = _pending_projects.get()
                if pending and len(pending) > 0:
                    # Flush to database NOW so we have the queue_id for the link
                    queue_id = _flush_project_queue()
                    if queue_id:
                        project_count = len(pending)
                        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

                        # Build project description
                        project_titles = [p.get("title", "Untitled") for p in pending]
                        if project_count == 1:
                            project_desc = f'"{project_titles[0]}"'
                        else:
                            project_desc = ", ".join(f'"{t}"' for t in project_titles[:3])
                            if project_count > 3:
                                project_desc += f" (+{project_count - 3} more)"

                        # Approval and cancel links with queue_id
                        approve_url = f"{vikunja_url}/queue?id={queue_id}"
                        cancel_url = f"{vikunja_url}/queue?cancel={queue_id}"

                        # Get bot username for @mention instruction
                        bot_username = None
                        requesting_user = _requesting_user.get()
                        if requesting_user:
                            from .bot_provisioning import get_user_bot_credentials
                            user_id = f"vikunja:{requesting_user}"
                            bot_creds = get_user_bot_credentials(user_id)
                            if bot_creds:
                                bot_username, _ = bot_creds

                        bot_mention = f"@{bot_username}" if bot_username else "@eis"

                        final_text += f"\n\n---\n**Your new {'project is' if project_count == 1 else 'projects are'} ready!**\n\n"
                        final_text += f"{project_desc}\n\n"
                        final_text += f"If this is what you want, **[click here to create]({approve_url})**\n\n"
                        final_text += f"To make changes, add a comment below (include '{bot_mention}' anywhere in the thread)\n\n"
                        final_text += f"To cancel, **[click here]({cancel_url})**"

                        logger.info(f"[vikunja_chat] Queued {project_count} projects (queue_id={queue_id})")

                logger.info(f"[vikunja_chat] Final response preview: {final_text[:200] if final_text else '(empty)'}...")
                return final_text, total_input_tokens, total_output_tokens, turns

        # Max turns reached
        return "I've reached the maximum number of steps. Please try a simpler request.", total_input_tokens, total_output_tokens, turns
    finally:
        # Flush any remaining pending projects (normally already done above, but safety net)
        try:
            pending = _pending_projects.get()
            if pending:
                queue_id = _flush_project_queue()
                if queue_id:
                    logger.info(f"[vikunja_chat_with_claude] Safety flush: project queue (id={queue_id})")
        except Exception as e:
            logger.error(f"[vikunja_chat_with_claude] Failed to flush project queue: {e}", exc_info=True)

        # Always reset context variables (solutions-bvw1, solutions-zja1)
        _current_vikunja_token.reset(token_reset)
        _bot_mode.reset(bot_mode_reset)
        _requesting_user.reset(user_reset)
        _requesting_user_id.reset(user_id_reset)


# @PRIVATE
@mcp.custom_route("/slack/events", methods=["POST"])
async def slack_events(request: Request):
    """Slack events webhook endpoint."""
    _, handler = _get_slack_app()
    if handler is None:
        return JSONResponse(
            {"error": "Slack not configured. Set SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET."},
            status_code=503
        )
    return await handler.handle(request)


# ============================================================================
# VIKUNJA WEBHOOK HANDLER (@eis native mode)
# ============================================================================

# Track recently processed tasks to prevent duplicate processing
# Key: task_id, Value: timestamp
_recently_processed_tasks: dict[int, float] = {}
_TASK_DEDUP_TTL = 10.0  # seconds


# @PRIVATE
def _should_skip_duplicate(task_id: int) -> bool:
    """Check if task was recently processed (deduplication)."""
    import time
    now = time.time()

    # Clean old entries
    expired = [k for k, v in _recently_processed_tasks.items() if now - v > _TASK_DEDUP_TTL]
    for k in expired:
        del _recently_processed_tasks[k]

    # Check if recently processed
    if task_id in _recently_processed_tasks:
        return True

    # Mark as processed
    _recently_processed_tasks[task_id] = now
    return False


# @PRIVATE
def _verify_vikunja_webhook_signature(signature: str | None, body: bytes, secret: str) -> bool:
    """Verify Vikunja webhook signature (HMAC-SHA256)."""
    if not signature or not secret:
        return False
    import hmac
    import hashlib
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


# @PRIVATE
def _is_assigned_to_eis(task: dict) -> bool:
    """Check if task is assigned to @eis user.

    Vikunja strips @eis from title when it assigns the task,
    so we check assignees instead of looking for @eis in text.
    """
    assignees = task.get("assignees", [])
    if not assignees:
        return False
    for assignee in assignees:
        username = assignee.get("username", "").lower()
        if username == "eis":
            return True
    return False


# @PRIVATE
def _extract_eis_text(payload: dict, event: str) -> tuple[str | None, int | None, dict | None]:
    """Extract text for @eis processing from webhook payload.

    Vikunja webhook payload structure:
    {
      "event_name": "task.created",
      "time": "...",
      "data": {
        "doer": {...},
        "task": {...}
      }
    }

    Detection methods:
    1. Task assigned to @eis (Vikunja parses @eis and assigns)
    2. @eis in description (for explicit instructions)
    3. @eis in comment text

    Returns:
        Tuple of (text_to_process, task_id, task_creator_info)
    """
    # Vikunja nests data under data.task or data.comment
    data = payload.get("data", {})

    if event in ("task.created", "task.updated"):
        task = data.get("task", {})
        title = task.get("title", "")
        description = task.get("description", "")
        text = f"{title} {description}"

        # Check if assigned to @eis OR @eis in description
        if _is_assigned_to_eis(task) or "@eis" in text.lower():
            return text, task.get("id"), data.get("doer")

    elif event in ("task.comment.created", "comment.created"):
        # Comment events - data.comment contains the comment object
        comment = data.get("comment", {})
        text = comment.get("comment", "") if isinstance(comment, dict) else ""
        task_id = comment.get("task_id") if isinstance(comment, dict) else None
        if "@eis" in text.lower():
            return text, task_id, data.get("doer")

    return None, None, None


# @PRIVATE
async def _process_eis_mention(text: str, task_id: int, creator: dict | None) -> dict:
    """Process @eis mention with LLM and update task.

    Args:
        text: The text containing @eis mention
        task_id: Vikunja task ID
        creator: Task creator info (id, email, etc.)

    Returns:
        Dict with processing result
    """
    from .vikunja_client import BotVikunjaClient, VikunjaAPIError

    # Initialize bot client
    try:
        bot_client = BotVikunjaClient()
    except ValueError as e:
        logger.error(f"BotVikunjaClient init failed: {e}")
        return {"error": str(e), "processed": False}

    # Get current task
    try:
        task = bot_client.get_task(task_id)
    except VikunjaAPIError as e:
        logger.error(f"Failed to get task {task_id}: {e}")
        return {"error": str(e), "processed": False}

    # Remove @eis from text for LLM processing
    clean_text = text.lower().replace("@eis", "").strip()

    # Simple LLM call to interpret the request
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # No LLM available - just acknowledge
        bot_client.add_comment(task_id, "👋 @eis received your message but LLM is not configured.")
        return {"processed": True, "action": "acknowledged_no_llm"}

    try:
        import anthropic
        import json

        claude = anthropic.Anthropic(api_key=api_key)

        # Get current date for relative date parsing
        from datetime import datetime
        import pytz
        now = datetime.now(pytz.UTC)
        current_date = now.strftime("%Y-%m-%d")
        current_day = now.strftime("%A")

        system_prompt = f"""You are @eis, a task assistant. The user mentioned you in a Vikunja task.

Current date: {current_date} ({current_day})
Current task title: {task.get('title', '')}
Current task description: {task.get('description', '')}
Current due date: {task.get('due_date', 'not set')}

Analyze what the user wants and respond with a JSON object:
{{
  "action": "update" | "clarify" | "done",
  "new_title": "cleaned task title" | null,
  "new_due_date": "YYYY-MM-DDTHH:MM:SSZ" | null,
  "new_priority": 1-5 | null,
  "response": "brief confirmation message for user"
}}

Rules:
- If the original title contains "@eis", remove it and set new_title
- Parse relative dates like "tomorrow", "next monday", "in 3 days"
- Priority: 1=lowest, 5=urgent
- Keep response brief (under 100 chars)
- action "done" means mark task complete
- action "clarify" means you need more information

Respond ONLY with valid JSON, no explanation."""

        response = claude.messages.create(
            model="claude-3-5-haiku-20241022",  # Fast, cheap model for parsing
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": clean_text}]
        )

        # Calculate actual cost from token usage
        # Haiku pricing: $0.25/M input, $1.25/M output (as of late 2024)
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        actual_cost_cents = (input_tokens * 0.000025) + (output_tokens * 0.000125)
        actual_cost_cents = round(actual_cost_cents, 2) or 0.01  # minimum 0.01¢

        # Parse LLM response
        response_text = response.content[0].text.strip()
        # Handle markdown code blocks
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()

        result = json.loads(response_text)

        # Apply updates
        updates = {}
        if result.get("new_title"):
            updates["title"] = result["new_title"]
        if result.get("new_due_date"):
            updates["due_date"] = result["new_due_date"]
        if result.get("new_priority"):
            updates["priority"] = result["new_priority"]
        if result.get("action") == "done":
            updates["done"] = True

        if updates:
            bot_client.update_task(task_id, **updates)

        # Post comment with response (use actual token cost, not LLM's guess)
        comment = f"{result.get('response', '✅ Done')} [{actual_cost_cents:.2f}¢]"
        bot_client.add_comment(task_id, comment)

        return {"processed": True, "action": result.get("action"), "updates": updates}

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response: {e}")
        bot_client.add_comment(task_id, "❌ Sorry, I couldn't understand that request.")
        return {"processed": False, "error": "json_parse_error"}
    except Exception as e:
        logger.error(f"LLM processing failed: {e}")
        bot_client.add_comment(task_id, f"❌ Error: {str(e)[:50]}")
        return {"processed": False, "error": str(e)}


# @PRIVATE
@mcp.custom_route("/vikunja-webhook", methods=["POST"])
async def vikunja_webhook(request: Request):
    """Handle Vikunja webhook events for @eis mentions.

    Vikunja sends webhooks for task.created, task.updated, comment.created.
    This endpoint detects @eis mentions and processes them with LLM.

    Bead: solutions-xups
    """
    # Get webhook secret (optional but recommended)
    webhook_secret = os.environ.get("VIKUNJA_WEBHOOK_SECRET", "")

    # Verify signature if secret is configured
    body = await request.body()
    if webhook_secret:
        signature = request.headers.get("X-Vikunja-Signature", "")
        if not _verify_vikunja_webhook_signature(signature, body, webhook_secret):
            logger.warning("Vikunja webhook signature verification failed")
            return JSONResponse({"error": "Invalid signature"}, status_code=401)

    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse webhook payload: {e}")
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    event = payload.get("event_name") or payload.get("event")
    logger.info(f"Vikunja webhook received: event={event}")

    # Debug: log payload structure
    data = payload.get("data", {})
    logger.info(f"Webhook data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    if isinstance(data, dict):
        task = data.get("task", {})
        title = task.get("title", "") if isinstance(task, dict) else ""
        assignees = task.get("assignees", []) if isinstance(task, dict) else []
        assignee_names = [a.get("username", "?") for a in assignees] if assignees else []
        logger.info(f"Webhook task: title='{title[:50]}', assignees={assignee_names}")

    # Skip if doer is the bot itself (prevent infinite loop)
    doer = data.get("doer", {}) if isinstance(data, dict) else {}
    doer_username = doer.get("username", "").lower() if isinstance(doer, dict) else ""
    if doer_username == "eis":
        logger.info("Skipping: doer is @eis (bot's own action)")
        return JSONResponse({"status": "ignored", "reason": "bot's own action"})

    # Extract @eis mention
    text, task_id, creator = _extract_eis_text(payload, event)

    if not text or not task_id:
        return JSONResponse({
            "status": "ignored",
            "reason": "no @eis mention or missing task_id"
        })

    # Deduplicate - skip if task was processed recently
    if _should_skip_duplicate(task_id):
        logger.info(f"Skipping: task_id={task_id} already processed recently")
        return JSONResponse({"status": "ignored", "reason": "duplicate"})

    # Process the mention
    logger.info(f"Processing @eis mention: task_id={task_id}, text={text[:100]}...")
    result = await _process_eis_mention(text, task_id, creator)

    return JSONResponse({"status": "processed", "result": result})


# @PRIVATE
@mcp.custom_route("/webhooks/resend", methods=["POST"])
async def resend_inbound_webhook(request: Request):
    """Handle Resend inbound email webhooks.

    Enables email-as-interface: users can interact with @eis by replying to emails.

    Flow:
    1. User replies to email from @eis
    2. Resend receives reply, sends webhook here
    3. We parse email, extract command, route to @eis
    4. Response sent back via email

    Bead: fa-4mda.1
    """
    from .email_inbound import (
        verify_resend_webhook,
        handle_inbound_email,
    )

    # Get webhook signature headers (Svix format)
    signature = request.headers.get("svix-signature", "")
    timestamp = request.headers.get("svix-timestamp", "")
    webhook_id = request.headers.get("svix-id", "")

    body = await request.body()

    # Verify signature
    if not verify_resend_webhook(body, signature, timestamp, webhook_id):
        logger.warning(f"Resend webhook signature verification failed (id={webhook_id})")
        return JSONResponse({"error": "Invalid signature"}, status_code=401)

    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse Resend webhook payload: {e}")
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    event_type = payload.get("type", "unknown")
    logger.info(f"Resend webhook received: type={event_type}, id={webhook_id}")

    # Process inbound email
    try:
        result = await handle_inbound_email(payload)
        return JSONResponse(result)
    except Exception as e:
        logger.exception(f"Error handling inbound email: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# OAUTH AUTH MIDDLEWARE
# ============================================================================

class OAuthAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate OAuth Bearer tokens."""

    # Paths that don't require auth (exact match)
    PUBLIC_PATHS = {"/", "/health", "/poller-health", "/install-success", "/authorize", "/token", "/register", "/slack/events", "/vikunja-callback", "/vikunja-webhook", "/webhooks/resend", "/waiting-list", "/beta-signup", "/signup-password", "/signup-google", "/activate-bot", "/auth-register", "/oidc-onboard", "/internal/complete-oidc-onboarding", "/queue", "/my-workspaces", "/.well-known/oauth-authorization-server", "/.well-known/oauth-protected-resource", "/.well-known/protected-resource-metadata"}

    # Path prefixes that don't require auth (uses own token-based auth)
    PUBLIC_PREFIXES = ("/calendar/", "/refresh/", "/move/", "/complete/", "/ears-off/", "/capture-off/", "/project-queue")

# @PRIVATE
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public paths (exact match)
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        # Skip auth for public prefixes (calendar endpoint uses URL token auth)
        if request.url.path.startswith(self.PUBLIC_PREFIXES):
            return await call_next(request)

        # Check for OAuth token
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

            # Check if valid OAuth token
            if token in _oauth_tokens:
                token_data = _oauth_tokens[token]
                if time.time() < token_data["expires"]:
                    return await call_next(request)
                else:
                    del _oauth_tokens[token]  # Clean up expired token

            # Also accept MCP_API_KEY for backward compatibility
            api_key = os.environ.get("MCP_API_KEY")
            if api_key and token == api_key:
                return await call_next(request)

        # Check query param fallback
        query_key = request.query_params.get("api_key")
        api_key = os.environ.get("MCP_API_KEY")
        if api_key and query_key == api_key:
            return await call_next(request)

        # Return 401 with WWW-Authenticate header pointing to resource metadata (RFC 9728)
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        return JSONResponse(
            {"error": "unauthorized", "message": "Invalid or missing access token"},
            status_code=401,
            headers={
                "WWW-Authenticate": f'Bearer resource_metadata_uri="{base_url}/.well-known/protected-resource-metadata"'
            }
        )


# ============================================================================
# ICS CALENDAR FEED
# ============================================================================

# @PRIVATE
def _generate_ics_impl(tasks: list[dict], calendar_name: str = "Vikunja Tasks") -> str:
    """Generate ICS calendar content from a list of Vikunja tasks.

    Args:
        tasks: List of task dictionaries from Vikunja API
        calendar_name: Name for the calendar

    Returns:
        ICS formatted string
    """
    from dateutil import parser as dateparser

    cal = Calendar()
    cal.add('prodid', '-//Vikunja MCP//vikunja-mcp//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', calendar_name)

    for task in tasks:
        # Skip tasks without due_date (Vikunja uses 0001-01-01 as sentinel for "no date")
        due_date = task.get('due_date')
        if not due_date or due_date.startswith('0001-01-01'):
            continue

        event = Event()

        # UID for deduplication
        task_id = task.get('id', 0)
        event.add('uid', f"vikunja-{task_id}@factumerit")

        # Summary (title)
        event.add('summary', task.get('title', 'Untitled'))

        # Description (strip HTML tags for ICS compatibility)
        description = task.get('description')
        if description:
            # Strip HTML tags - Vikunja stores descriptions as HTML
            import re
            clean_desc = re.sub(r'<[^>]+>', '', description)
            if clean_desc.strip():
                event.add('description', clean_desc.strip())

        # Parse dates
        try:
            dt_due = dateparser.parse(due_date)

            # Check for start_date (skip sentinel value)
            start_date = task.get('start_date')
            if start_date and not start_date.startswith('0001-01-01'):
                dt_start = dateparser.parse(start_date)
                event.add('dtstart', dt_start)
                event.add('dtend', dt_due)
            else:
                # Use due_date as both start and end (point-in-time event)
                event.add('dtstart', dt_due)
                event.add('dtend', dt_due)
        except (ValueError, TypeError):
            # Skip malformed dates
            continue

        # Add timestamp
        event.add('dtstamp', datetime.now(tz=None))

        cal.add_component(event)

    return cal.to_ical().decode('utf-8')


# @PRIVATE
def _get_ics_feed_impl(label: str = "calendar", instance: Optional[str] = None) -> str:
    """Get ICS feed of tasks filtered by label.

    Args:
        label: Label to filter tasks by (default: "calendar")
        instance: Instance name for multi-instance mode. If None, uses current/default.

    Returns:
        ICS formatted string
    """
    # Get instance config - prefer calendar instances for HTTP endpoint
    if instance:
        calendar_instances = _get_calendar_instances()
        if instance in calendar_instances:
            inst_config = calendar_instances[instance]
            url = inst_config["url"]
            token = inst_config["token"]
            instance_name = instance
        else:
            return _generate_ics_impl([], calendar_name=f"Unknown - {label}")
    else:
        # Fallback to traditional instance config (for MCP tool usage)
        url, token = _get_instance_config()
        instance_name = _get_current_instance() or "Vikunja"

    # Get all projects first
    projects_response = requests.request(
        "GET",
        f"{url}/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"}
    )

    if projects_response.status_code != 200:
        return _generate_ics_impl([], calendar_name=f"{instance_name} - {label}")

    projects = projects_response.json() or []

    # Collect tasks from all projects
    all_tasks = []
    label_lower = label.lower()

    for project in projects:
        project_id = project.get('id')
        if not project_id:
            continue

        tasks_response = requests.request(
            "GET",
            f"{url}/api/v1/projects/{project_id}/tasks",
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": 100}
        )

        if tasks_response.status_code == 200:
            tasks = tasks_response.json() or []
            # Filter by label
            for task in tasks:
                if any(
                    lbl.get('title', '').lower() == label_lower
                    for lbl in (task.get('labels') or [])
                ):
                    all_tasks.append(task)

    return _generate_ics_impl(all_tasks, calendar_name=f"{instance_name} - {label}")


# @PRIVATE
@mcp.tool()
@mcp_tool_with_fallback
def get_ics_feed(
    label: str = Field(
        default="calendar",
        description="Label to filter tasks by. Only tasks with this label will be included."
    )
) -> str:
    """Generate an ICS calendar feed from Vikunja tasks.

    Returns tasks with the specified label as an ICS (iCalendar) file that can be
    imported into Google Calendar, Outlook, or other calendar apps.

    Use the 'calendar' label on tasks you want to appear in your calendar feed.
    """
    return _get_ics_feed_impl(label=label)


# @PRIVATE
def _get_calendar_url_impl(
    label: str = "calendar",
    base_url: str = "",
    instance: str = ""
) -> dict:
    """Implementation for get_calendar_url - separated for testing.

    Args:
        label: Label to filter tasks by (default: "calendar")
        base_url: Base URL of vikunja-mcp server
        instance: Instance name for multi-instance mode. If empty, uses default.

    Returns:
        Dict with url, label, token, instance, and instructions.
    """
    instances = _get_calendar_instances()

    # Validate instance if specified
    if instance:
        if instance not in instances:
            available = list(instances.keys())
            return {
                "error": f"Unknown instance: {instance}",
                "available_instances": available,
                "url": None
            }
        token = instances[instance]["calendar_token"]
        instance_name = instance
    else:
        # Use default/first instance for backward compatibility
        token = _get_calendar_token()
        if not token:
            # Fallback to config file (same pattern as _get_ics_feed_impl)
            try:
                _, api_token = _get_instance_config()
                token = hashlib.sha256(api_token.encode()).hexdigest()[:16]
                instance_name = _get_current_instance() or ""
            except ValueError:
                return {
                    "error": "No Vikunja token configured",
                    "url": None
                }
        else:
            # Determine instance name for URL
            if "default" in instances:
                instance_name = ""  # Don't include instance in path for single-instance
            else:
                instance_name = next(iter(instances.keys()), "")

    # Build the path - include instance only for multi-instance mode
    if instance_name and len(instances) > 1:
        path = f"/calendar/{instance_name}/{token}.ics"
    else:
        path = f"/calendar/{token}.ics"

    if label and label != "calendar":
        path += f"?label={label}"

    # Get base URL from param, env, or leave as path
    base = base_url or os.environ.get("VIKUNJA_MCP_URL", "")

    if base:
        # Remove trailing slash if present
        base = base.rstrip("/")
        full_url = f"{base}{path}"
    else:
        full_url = path

    result = {
        "url": full_url,
        "label": label,
        "token": token,
        "instructions": "Add this URL to Google Calendar: Settings → Add calendar → From URL"
    }

    # Include instance info for multi-instance mode
    if instance_name:
        result["instance"] = instance_name

    # List available instances if multiple configured
    if len(instances) > 1:
        result["available_instances"] = list(instances.keys())

    return result


# @PRIVATE
@mcp.tool()
@mcp_tool_with_fallback
def get_calendar_url(
    label: str = Field(
        default="calendar",
        description="Label to filter tasks by in the calendar feed."
    ),
    base_url: str = Field(
        default="",
        description="Base URL of the vikunja-mcp server. If empty, uses VIKUNJA_MCP_URL env var or returns path only."
    ),
    instance: str = Field(
        default="",
        description="Vikunja instance name (e.g., 'personal', 'business'). If empty, uses default instance."
    )
) -> dict:
    """Get the URL for subscribing to your calendar feed.

    Returns the URL that Google Calendar, Outlook, or other calendar apps
    can use to subscribe to your Vikunja tasks.

    The URL contains a secure token - treat it like a password.
    Anyone with this URL can see tasks with the specified label.

    For multi-instance setups, specify the instance name to get the URL for
    a specific Vikunja instance.
    """
    return _get_calendar_url_impl(label=label, base_url=base_url, instance=instance)


# ============================================================================
# MAIN
# ============================================================================

# @PUBLIC
def main():
    """Run the MCP server."""
    # Grant owner role to users in ADMIN_USER_IDS env var
    _grant_env_admin_roles()

    import argparse
    parser = argparse.ArgumentParser(description="Vikunja MCP Server")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse", "http"],
                        help="Transport protocol (default: stdio)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for SSE transport (default: 8000)")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Host for SSE transport (default: 0.0.0.0)")
    parser.add_argument("--matrix", action="store_true",
                        help="Enable Matrix bot (requires MATRIX_* env vars)")
    parser.add_argument("--smart-tasks", action="store_true",
                        help="Enable @eis smart tasks polling (requires VIKUNJA_BOT_TOKEN)")
    args = parser.parse_args()

    if args.transport in ("sse", "http"):
        import uvicorn
        from starlette.middleware import Middleware

        # Build app with CORS and OAuth middleware
        # CORS: Allow queue processor page (vikunja.factumerit.app) to call API endpoints
        # Bead: solutions-eofy.1
        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=["https://vikunja.factumerit.app"],
                allow_credentials=True,
                allow_methods=["GET", "POST", "OPTIONS"],
                allow_headers=["Authorization", "Content-Type"],
            ),
            Middleware(OAuthAuthMiddleware)
        ]
        app = mcp.http_app(transport=args.transport, middleware=middleware)

        if args.smart_tasks:
            # Run @eis notification poller alongside MCP server
            import asyncio
            import threading
            from .notification_poller import run_poller

# @PRIVATE
            def run_poller_in_thread():
                """Run notification poller in a separate thread with its own event loop.

                Uses run_poller() which supports multi-bot mode (personal bots with JWT auth).
                Falls back to legacy single-bot mode if no personal bots found.
                """
                print("[POLLER] Thread started", flush=True)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    print("[POLLER] Starting run_poller() (multi-bot mode)...", flush=True)
                    loop.run_until_complete(run_poller())
                except Exception as e:
                    print(f"[POLLER] ERROR: {e}", flush=True)
                    logger.error(f"Smart tasks poller error: {e}", exc_info=True)
                finally:
                    loop.close()

            poller_thread = threading.Thread(target=run_poller_in_thread, daemon=True)
            poller_thread.start()
            logger.info("Smart tasks poller started in background thread (multi-bot mode)")

        uvicorn.run(app, host=args.host, port=args.port)
    else:
        if args.matrix:
            logger.warning("--matrix flag requires --transport sse or http")
        mcp.run(show_banner=False)


if __name__ == "__main__":
    main()
