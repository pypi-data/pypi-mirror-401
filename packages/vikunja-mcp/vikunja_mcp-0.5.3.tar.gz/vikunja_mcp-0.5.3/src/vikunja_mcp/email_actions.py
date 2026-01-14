"""
Email Action Service - Signed action tokens for email-driven workflows.

Enables users to take actions via email links without logging into Vikunja.
Links contain self-authenticating tokens that are validated server-side.

Bead: fa-kwoh (onboarding email), fa-up17 (AI Tinkerers prep)
Design: docs/EMAIL_ACTION_SERVICE_EXPLAINER.md

Flow:
1. Event triggers email (signup, project queued, task due)
2. Email contains signed action URL: /do/{token}
3. User clicks link
4. Server validates token signature and expiration
5. Server executes action using stored user credentials
6. User sees success page

Token Structure:
    payload = {"a": action, "r": resource_id, "u": user_id, "x": expiration}
    token = base64url(json(payload)) + "." + hmac_sha256(payload, key)[:16]
"""

import base64
import hashlib
import hmac
import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Derive HMAC key from existing encryption key
# This keeps us to a single secret while using the right primitive for signing
_ENCRYPTION_KEY = os.environ.get("TOKEN_ENCRYPTION_KEY", "")

# Base URL for action links
MCP_PUBLIC_URL = os.environ.get("MCP_PUBLIC_URL", "https://mcp.factumerit.app")

# Default token expiration (72 hours)
DEFAULT_EXPIRY_SECONDS = int(os.environ.get("EMAIL_ACTION_DEFAULT_EXPIRY", 72 * 3600))


def _get_signing_key() -> bytes:
    """Derive HMAC signing key from encryption key."""
    if not _ENCRYPTION_KEY:
        raise ValueError("TOKEN_ENCRYPTION_KEY not configured")
    # Use HKDF-style derivation: HMAC(key, context)
    # This creates a separate key for email actions vs token encryption
    return hmac.new(
        _ENCRYPTION_KEY.encode(),
        b"email-action-signing-v1",
        hashlib.sha256
    ).digest()


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ActionTokenError(Exception):
    """Base exception for action token errors."""
    pass


class TokenExpiredError(ActionTokenError):
    """Token has expired."""
    pass


class InvalidSignatureError(ActionTokenError):
    """Token signature is invalid (tampered or wrong key)."""
    pass


class InvalidPayloadError(ActionTokenError):
    """Token payload is malformed."""
    pass


class UnknownActionError(ActionTokenError):
    """Action type not recognized."""
    pass


class ActionExecutionError(ActionTokenError):
    """Action failed to execute."""
    pass


# =============================================================================
# TOKEN GENERATION
# =============================================================================

def create_action_url(
    action: str,
    user_id: str,
    resource_id: int,
    expires_in: int = None,
    **extra_data
) -> str:
    """
    Generate a signed action URL for email.

    Args:
        action: Action type (e.g., "approve_project", "complete_task")
        user_id: User ID (e.g., "vikunja:alice")
        resource_id: Resource being acted on (queue_id, task_id, etc.)
        expires_in: Seconds until expiration (default: 72 hours)
        **extra_data: Additional action-specific data (e.g., days=3 for snooze)

    Returns:
        Full URL: https://mcp.factumerit.app/do/{token}

    Example:
        url = create_action_url("approve_project", "vikunja:alice", 42)
        # https://mcp.factumerit.app/do/eyJhIjoi...abc123
    """
    if expires_in is None:
        expires_in = DEFAULT_EXPIRY_SECONDS

    payload = {
        "a": action,
        "r": resource_id,
        "u": user_id,
        "x": int(time.time()) + expires_in,
    }

    # Add extra data if provided
    if extra_data:
        payload["d"] = extra_data

    token = _encode_token(payload)
    return f"{MCP_PUBLIC_URL}/do/{token}"


def create_action_token(
    action: str,
    user_id: str,
    resource_id: int,
    expires_in: int = None,
    **extra_data
) -> str:
    """
    Generate just the token (without URL prefix).

    Useful when you need to construct the URL differently.
    """
    if expires_in is None:
        expires_in = DEFAULT_EXPIRY_SECONDS

    payload = {
        "a": action,
        "r": resource_id,
        "u": user_id,
        "x": int(time.time()) + expires_in,
    }

    if extra_data:
        payload["d"] = extra_data

    return _encode_token(payload)


def _encode_token(payload: dict) -> str:
    """Encode payload as signed token."""
    # JSON encode and base64url
    payload_json = json.dumps(payload, separators=(",", ":"))  # Compact JSON
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip("=")

    # Sign with HMAC-SHA256, truncate to 16 chars (64 bits)
    signature = hmac.new(
        _get_signing_key(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()[:16]

    return f"{payload_b64}.{signature}"


# =============================================================================
# TOKEN VALIDATION
# =============================================================================

@dataclass
class ActionPayload:
    """Validated action token payload."""
    action: str
    resource_id: int
    user_id: str
    expires_at: int
    extra_data: dict

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at


def validate_action_token(token: str) -> ActionPayload:
    """
    Validate and decode an action token.

    Args:
        token: The token string (payload.signature)

    Returns:
        ActionPayload with decoded fields

    Raises:
        InvalidPayloadError: Token is malformed
        InvalidSignatureError: Signature doesn't match
        TokenExpiredError: Token has expired
    """
    # Split token into payload and signature
    if "." not in token:
        raise InvalidPayloadError("Token missing signature separator")

    parts = token.rsplit(".", 1)
    if len(parts) != 2:
        raise InvalidPayloadError("Token has invalid format")

    payload_b64, signature = parts

    # Verify signature first (before any JSON parsing)
    expected_sig = hmac.new(
        _get_signing_key(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()[:16]

    if not hmac.compare_digest(signature, expected_sig):
        logger.warning(f"[validate_action_token] Invalid signature for token")
        raise InvalidSignatureError("Token signature is invalid")

    # Decode payload
    try:
        # Add back padding if needed
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding

        payload_json = base64.urlsafe_b64decode(payload_b64).decode()
        payload = json.loads(payload_json)
    except Exception as e:
        logger.warning(f"[validate_action_token] Failed to decode payload: {e}")
        raise InvalidPayloadError(f"Token payload is malformed: {e}")

    # Validate required fields
    required = ["a", "r", "u", "x"]
    for field in required:
        if field not in payload:
            raise InvalidPayloadError(f"Token missing required field: {field}")

    # Build ActionPayload
    action_payload = ActionPayload(
        action=payload["a"],
        resource_id=payload["r"],
        user_id=payload["u"],
        expires_at=payload["x"],
        extra_data=payload.get("d", {}),
    )

    # Check expiration
    if action_payload.is_expired:
        logger.info(f"[validate_action_token] Token expired for user {action_payload.user_id}")
        raise TokenExpiredError("This link has expired")

    return action_payload


# =============================================================================
# ACTION REGISTRY
# =============================================================================

# Type for action handlers
ActionHandler = Callable[[ActionPayload, str], dict]

# Registry of action handlers
_action_registry: dict[str, ActionHandler] = {}


def register_action(action_name: str):
    """Decorator to register an action handler."""
    def decorator(func: ActionHandler):
        _action_registry[action_name] = func
        logger.info(f"[email_actions] Registered action handler: {action_name}")
        return func
    return decorator


def get_action_handler(action_name: str) -> Optional[ActionHandler]:
    """Get handler for an action type."""
    return _action_registry.get(action_name)


def list_registered_actions() -> list[str]:
    """List all registered action types."""
    return list(_action_registry.keys())


# =============================================================================
# ACTION EXECUTION
# =============================================================================

def execute_action(token: str) -> dict:
    """
    Validate token and execute the action.

    Args:
        token: The action token from URL

    Returns:
        dict with action result:
            {"success": True, "message": "...", "redirect": "..."}
        or
            {"success": False, "error": "...", "error_type": "..."}
    """
    # Validate token
    try:
        payload = validate_action_token(token)
    except TokenExpiredError:
        return {
            "success": False,
            "error": "This link has expired. Please request a new one.",
            "error_type": "expired",
        }
    except InvalidSignatureError:
        return {
            "success": False,
            "error": "This link is invalid. Please request a new one.",
            "error_type": "invalid_signature",
        }
    except InvalidPayloadError as e:
        return {
            "success": False,
            "error": f"This link is malformed: {e}",
            "error_type": "invalid_payload",
        }

    # Get handler
    handler = get_action_handler(payload.action)
    if not handler:
        logger.warning(f"[execute_action] Unknown action: {payload.action}")
        return {
            "success": False,
            "error": f"Unknown action type: {payload.action}",
            "error_type": "unknown_action",
        }

    # Get user's stored Vikunja token
    try:
        from .bot_provisioning import get_bot_owner_token
        user_token = get_bot_owner_token(payload.user_id)

        if not user_token:
            logger.warning(f"[execute_action] No stored token for user {payload.user_id}")
            return {
                "success": False,
                "error": "Your session has expired. Please log into Vikunja and try again.",
                "error_type": "no_user_token",
            }
    except Exception as e:
        logger.error(f"[execute_action] Failed to get user token: {e}")
        return {
            "success": False,
            "error": "Unable to authenticate. Please try again later.",
            "error_type": "auth_error",
        }

    # Execute action
    try:
        result = handler(payload, user_token)
        logger.info(f"[execute_action] Action {payload.action} succeeded for user {payload.user_id}")
        return result
    except Exception as e:
        logger.error(f"[execute_action] Action {payload.action} failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Action failed: {str(e)}",
            "error_type": "execution_error",
        }


# =============================================================================
# BUILT-IN ACTION HANDLERS
# =============================================================================

@register_action("approve_project")
def handle_approve_project(payload: ActionPayload, user_token: str) -> dict:
    """
    Create project(s) from the approval queue.

    Uses the same logic as the /queue page, but server-side.
    """
    import httpx
    from .token_broker import execute

    queue_id = payload.resource_id
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    # Fetch queue entry
    rows = execute("""
        SELECT id, username, bot_username, title, description, hex_color,
               parent_project_id, projects, status
        FROM project_creation_queue
        WHERE id = %s
    """, (queue_id,))

    if not rows:
        return {
            "success": False,
            "error": "This project request was not found. It may have already been processed.",
            "error_type": "not_found",
        }

    row = rows[0]
    status = row[8]

    if status == "complete":
        return {
            "success": False,
            "error": "This project has already been created.",
            "error_type": "already_processed",
        }

    if status == "cancelled":
        return {
            "success": False,
            "error": "This project request was cancelled.",
            "error_type": "cancelled",
        }

    # Extract project specs (batch mode or single mode)
    projects_json = row[7]  # projects column (JSONB)
    bot_username = row[2]

    if projects_json:
        # Batch mode
        project_specs = projects_json
    else:
        # Single mode
        project_specs = [{
            "title": row[3],
            "description": row[4] or "",
            "hex_color": row[5] or "",
            "parent_project_id": row[6] or 0,
        }]

    # Create projects using user's token
    created_projects = []
    id_map = {}  # temp_id -> real_id for parent resolution

    with httpx.Client(timeout=30) as client:
        for spec in project_specs:
            # Resolve parent ID if it's a temp reference
            parent_id = spec.get("parent_project_id", 0)
            if parent_id and parent_id < 0:
                parent_id = id_map.get(parent_id, 0)

            # Create project
            resp = client.request(
                "PUT",
                f"{vikunja_url}/api/v1/projects",
                headers={"Authorization": f"Bearer {user_token}"},
                json={
                    "title": spec["title"],
                    "description": spec.get("description", ""),
                    "hex_color": spec.get("hex_color", ""),
                    "parent_project_id": parent_id,
                },
            )

            if resp.status_code not in (200, 201):
                logger.error(f"[approve_project] Failed to create project: {resp.status_code} {resp.text}")
                return {
                    "success": False,
                    "error": f"Failed to create project '{spec['title']}': {resp.text}",
                    "error_type": "api_error",
                }

            project_data = resp.json()
            project_id = project_data["id"]
            created_projects.append({"id": project_id, "title": spec["title"]})

            # Track temp_id mapping
            if "temp_id" in spec:
                id_map[spec["temp_id"]] = project_id

            # Share with bot if configured
            if bot_username:
                try:
                    client.put(
                        f"{vikunja_url}/api/v1/projects/{project_id}/users",
                        headers={"Authorization": f"Bearer {user_token}"},
                        json={"username": bot_username, "right": 2},
                    )
                except Exception as e:
                    logger.warning(f"[approve_project] Failed to share with bot: {e}")

    # Mark queue entry complete
    execute("""
        UPDATE project_creation_queue
        SET status = 'complete', completed_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (queue_id,))

    # Build success message
    if len(created_projects) == 1:
        message = f"Project '{created_projects[0]['title']}' created successfully!"
        redirect = f"{vikunja_url}/projects/{created_projects[0]['id']}"
    else:
        titles = ", ".join(p["title"] for p in created_projects[:3])
        if len(created_projects) > 3:
            titles += f" (+{len(created_projects) - 3} more)"
        message = f"Created {len(created_projects)} projects: {titles}"
        redirect = f"{vikunja_url}/projects/{created_projects[0]['id']}"

    return {
        "success": True,
        "message": message,
        "redirect": redirect,
        "projects": created_projects,
    }


@register_action("cancel_project")
def handle_cancel_project(payload: ActionPayload, user_token: str) -> dict:
    """
    Cancel a project creation request.
    """
    from .token_broker import execute

    queue_id = payload.resource_id

    # Check current status
    rows = execute("""
        SELECT status, title, projects FROM project_creation_queue
        WHERE id = %s
    """, (queue_id,))

    if not rows:
        return {
            "success": False,
            "error": "This project request was not found.",
            "error_type": "not_found",
        }

    status = rows[0][0]
    title = rows[0][1]
    projects = rows[0][2]

    if status == "complete":
        return {
            "success": False,
            "error": "This project has already been created and cannot be cancelled.",
            "error_type": "already_processed",
        }

    if status == "cancelled":
        return {
            "success": True,
            "message": "This request was already cancelled.",
        }

    # Cancel it
    execute("""
        UPDATE project_creation_queue
        SET status = 'cancelled', completed_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (queue_id,))

    # Build message
    if projects:
        project_names = ", ".join(p["title"] for p in projects[:3])
        if len(projects) > 3:
            project_names += f" (+{len(projects) - 3} more)"
    else:
        project_names = title or "Untitled"

    return {
        "success": True,
        "message": f"Cancelled: {project_names}",
    }


@register_action("complete_task")
def handle_complete_task(payload: ActionPayload, user_token: str) -> dict:
    """
    Mark a task as complete.
    """
    import httpx

    task_id = payload.resource_id
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

    with httpx.Client(timeout=30) as client:
        # Get task first to get title
        resp = client.get(
            f"{vikunja_url}/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        if resp.status_code == 404:
            return {
                "success": False,
                "error": "Task not found.",
                "error_type": "not_found",
            }

        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"Failed to fetch task: {resp.text}",
                "error_type": "api_error",
            }

        task_data = resp.json()
        task_title = task_data.get("title", "Task")

        if task_data.get("done"):
            return {
                "success": True,
                "message": f"'{task_title}' was already complete.",
            }

        # Mark complete
        resp = client.post(
            f"{vikunja_url}/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"done": True},
        )

        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"Failed to complete task: {resp.text}",
                "error_type": "api_error",
            }

    return {
        "success": True,
        "message": f"Completed: '{task_title}'",
        "redirect": f"{vikunja_url}/tasks/{task_id}",
    }
