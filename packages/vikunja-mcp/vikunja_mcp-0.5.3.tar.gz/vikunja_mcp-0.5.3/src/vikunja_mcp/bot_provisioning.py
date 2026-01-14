"""
Personal Bot Provisioning Service.

Creates personal @eis-{username} bot accounts for each user during signup.
This provides physical user isolation - each bot only sees its owner's projects.

Bead: solutions-xk9l.1, solutions-aczq

Flow:
1. User signs up for Factumerit
2. provision_personal_bot(username) creates @eis-{username} in Vikunja
3. Bot token stored, used for all @eis operations for that user
4. User shares projects with their personal bot

Bot Naming (solutions-aczq):
- Default: @eis-{username} (e.g., @eis-jmuggli, @eis-mariaman24)
- Predictable, collision-free, easy to identify
- Custom names supported via bot_username parameter

Functions:
- provision_personal_bot(username, bot_username=None) -> BotCredentials
- get_user_bot_token(username) -> str
- share_project_with_personal_bot(username, project_id) -> bool
"""

import logging
import os
import secrets
import string
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

from .token_broker import encrypt_token, decrypt_token, execute
from .budget_service import forfeit_balance

logger = logging.getLogger(__name__)

# Default Vikunja instance for bot provisioning
VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
DEFAULT_INSTANCE = "default"


def normalize_vikunja_user_id(user_id: str) -> str:
    """
    Normalize Vikunja user_id to 2-element format.

    Vikunja notifications return 3-element format (vikunja:username:numeric_id)
    but our tables store 2-element format (vikunja:username).

    Args:
        user_id: User ID in either format

    Returns:
        Normalized 2-element format (vikunja:username)

    Examples:
        "vikunja:ivan:1" -> "vikunja:ivan"
        "vikunja:ivan" -> "vikunja:ivan"
        "slack:U123" -> "slack:U123" (non-vikunja unchanged)

    Bead: fa-me5dj
    """
    if not user_id:
        return user_id
    parts = user_id.split(":")
    if len(parts) == 3 and parts[0] == "vikunja":
        return f"{parts[0]}:{parts[1]}"
    return user_id


@dataclass
class BotCredentials:
    """Credentials for a provisioned personal bot."""
    vikunja_user_id: int
    username: str  # @eis-{random}
    display_name: str  # What users see (e.g., "eis" or "Jarvis")
    email: str
    password: str  # Bot password for JWT authentication
    created_at: datetime


class ProvisioningError(Exception):
    """Error during bot provisioning."""
    pass


def _generate_secure_password(length: int = 32) -> str:
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def provision_personal_bot(
    username: str,
    display_name: str = "eis",
    vikunja_url: str = None,
    bot_username: str = None,
) -> BotCredentials:
    """
    Provision a personal bot account for a user.

    Creates @eis-{username} in Vikunja with credentials for JWT authentication.

    NOTE: API tokens are broken in Vikunja (GitHub issue #105), so we use JWT tokens.
    Bot logs in with username/password to get JWT tokens instead of API tokens.

    Args:
        username: The user's username (used for bot username if bot_username not provided)
        display_name: Display name shown in UI (default: "eis")
        vikunja_url: Vikunja instance URL (default: VIKUNJA_URL env)
        bot_username: Optional custom bot username. If not provided, uses "eis-{username}"

    Returns:
        BotCredentials with the bot's password for JWT authentication

    Raises:
        ProvisioningError: If bot creation fails

    Note:
        Bot username defaults to eis-{username} for predictable, collision-free naming.
        Display name is what users see in comments.
        Example: username="jmuggli" -> bot_username="eis-jmuggli"
    """
    base_url = (vikunja_url or VIKUNJA_URL).rstrip('/')

    # Use predictable bot username: eis-{username}
    # This avoids collisions (username is unique) and makes bots easy to identify
    if not bot_username:
        bot_username = f"eis-{username}"

    # CRITICAL: Use real email domain (factumerit.app) with + addressing
    # Vikunja might validate email domains or do DNS checks. Using bot.factumerit.app
    # (unregistered domain) could cause "user does not exist" errors in sharing API.
    # All bot emails go to eis@factumerit.app inbox via + addressing.
    bot_email = f"eis+{bot_username}@factumerit.app"
    bot_password = _generate_secure_password()

    logger.info(f"[provision] Creating personal bot: {bot_username}")

    # Step 1: Register bot user
    # Get admin token for nginx auth (required for registration)
    vikunja_admin_token = os.environ.get("VIKUNJA_ADMIN_TOKEN", "")

    try:
        resp = requests.post(
            f"{base_url}/api/v1/register",
            headers={"X-Admin-Token": vikunja_admin_token} if vikunja_admin_token else {},
            json={
                "username": bot_username,
                "email": bot_email,
                "password": bot_password,
            },
            timeout=30,
        )

        if resp.status_code == 400:
            error = resp.json().get("message", "")
            if "already exists" in error.lower():
                raise ProvisioningError(f"Bot {bot_username} already exists")
            raise ProvisioningError(f"Registration failed: {error}")

        resp.raise_for_status()
        reg_data = resp.json()

        vikunja_user_id = reg_data.get("id")
        jwt_token = reg_data.get("token")

        logger.info(f"[provision] Bot registered: {bot_username} (id={vikunja_user_id})")

        # If no JWT token (email verification enabled), login to get one
        if not jwt_token:
            logger.info(f"[provision] No JWT token from registration (email verification enabled), logging in...")
            login_resp = requests.post(
                f"{base_url}/api/v1/login",
                headers={"Accept": "application/json"},
                json={
                    "username": bot_username,
                    "password": bot_password
                },
                timeout=30
            )

            if login_resp.status_code == 200:
                login_data = login_resp.json()
                jwt_token = login_data.get("token")
                vikunja_user_id = login_data.get("id") or vikunja_user_id
                logger.info(f"[provision] Login successful, got JWT token")
            else:
                raise ProvisioningError(f"Login failed after registration: {login_resp.status_code} - {login_resp.text}")

    except requests.RequestException as e:
        raise ProvisioningError(f"Registration request failed: {e}")

    # Step 2: Set display name (what users see in UI)
    # NOTE: overdue_tasks_reminders_time is REQUIRED (valid:"time,required" in user_settings.go line 52)
    # Format is HH:MM in 24-hour time. Default from user.go line 97 is "09:00"
    try:
        resp = requests.post(
            f"{base_url}/api/v1/user/settings/general",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={
                "name": display_name,
                "overdue_tasks_reminders_time": "09:00",  # Required field, using Vikunja default
            },
            timeout=30,
        )

        if resp.status_code == 200:
            logger.info(f"[provision] Display name set to '{display_name}' for {bot_username}")
        else:
            # Non-fatal - bot still works, just won't have nice display name
            logger.warning(f"[provision] Failed to set display name: {resp.status_code}")

    except requests.RequestException as e:
        logger.warning(f"[provision] Failed to set display name: {e}")
        # Non-fatal - continue with provisioning

    credentials = BotCredentials(
        vikunja_user_id=vikunja_user_id,
        username=bot_username,
        display_name=display_name,
        email=bot_email,
        password=bot_password,  # Store password for JWT authentication
        created_at=datetime.now(timezone.utc),
    )

    logger.info(f"[provision] Bot provisioned successfully: {bot_username} (using JWT auth)")
    return credentials


def store_bot_credentials(
    user_id: str,
    credentials: BotCredentials,
    owner_vikunja_user_id: int = None,
    owner_vikunja_token: str = None,
    vikunja_instance: str = DEFAULT_INSTANCE,
) -> None:
    """
    Store bot credentials in database (encrypted).

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        credentials: BotCredentials from provision_personal_bot()
        owner_vikunja_user_id: Owner's Vikunja user ID (for bot→user sharing)
        owner_vikunja_token: Owner's JWT token (for bot→user sharing, since bot tokens can't see users)
        vikunja_instance: Vikunja instance name for multi-instance support
    """
    encrypted_password = encrypt_token(credentials.password)
    encrypted_owner_token = encrypt_token(owner_vikunja_token) if owner_vikunja_token else None

    execute(
        """
        INSERT INTO personal_bots (user_id, bot_username, display_name, vikunja_user_id, encrypted_password, vikunja_instance, owner_vikunja_user_id, owner_vikunja_token, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            bot_username = EXCLUDED.bot_username,
            display_name = EXCLUDED.display_name,
            vikunja_user_id = EXCLUDED.vikunja_user_id,
            encrypted_password = EXCLUDED.encrypted_password,
            vikunja_instance = EXCLUDED.vikunja_instance,
            owner_vikunja_user_id = EXCLUDED.owner_vikunja_user_id,
            owner_vikunja_token = EXCLUDED.owner_vikunja_token
        """,
        (user_id, credentials.username, credentials.display_name, credentials.vikunja_user_id, encrypted_password, vikunja_instance, owner_vikunja_user_id, encrypted_owner_token, credentials.created_at),
    )

    logger.info(f"[store] Bot credentials stored for {user_id} -> {credentials.username} (owner_id={owner_vikunja_user_id}, has_owner_token={bool(owner_vikunja_token)})")


def get_user_bot_credentials(user_id: str, vikunja_instance: str = DEFAULT_INSTANCE) -> Optional[tuple[str, str]]:
    """
    Get bot credentials (username, password) for JWT authentication.

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        vikunja_instance: Vikunja instance name

    Returns:
        Tuple of (bot_username, bot_password), or None if not found
    """
    rows = execute(
        """
        SELECT bot_username, encrypted_password FROM personal_bots
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    if not rows:
        logger.debug(f"[get_user_bot_credentials] No bot found for {user_id}")
        return None

    bot_username = rows[0][0]
    encrypted_password = rows[0][1]

    if not encrypted_password:
        logger.warning(f"[get_user_bot_credentials] Bot {bot_username} has no password (old bot?)")
        return None

    # Update last_used_at
    execute(
        """
        UPDATE personal_bots SET last_used_at = NOW()
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    bot_password = decrypt_token(bytes(encrypted_password))
    return (bot_username, bot_password)


def get_user_bot_token(user_id: str, vikunja_instance: str = DEFAULT_INSTANCE) -> Optional[str]:
    """
    DEPRECATED: Get the API token for a user's personal bot.

    This function is deprecated because API tokens are broken in Vikunja.
    Use get_user_bot_credentials() instead to get username/password for JWT auth.

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        vikunja_instance: Vikunja instance name

    Returns:
        Bot's API token, or None if not found
    """
    logger.warning("[get_user_bot_token] DEPRECATED: API tokens are broken, use get_user_bot_credentials() instead")

    rows = execute(
        """
        SELECT encrypted_token FROM personal_bots
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    if not rows or not rows[0][0]:
        logger.debug(f"[get_user_bot_token] No bot token found for {user_id}")
        return None

    encrypted_token = rows[0][0]
    return decrypt_token(bytes(encrypted_token))


def get_user_bot_vikunja_id(user_id: str, vikunja_instance: str = DEFAULT_INSTANCE) -> Optional[int]:
    """
    Get the Vikunja user ID for a user's personal bot.

    Needed for sharing projects with the bot.

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        vikunja_instance: Vikunja instance name

    Returns:
        Bot's Vikunja user ID, or None if not found
    """
    rows = execute(
        """
        SELECT vikunja_user_id FROM personal_bots
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    if not rows:
        return None

    return rows[0][0]


def get_bot_owner_token(user_id: str, vikunja_instance: str = DEFAULT_INSTANCE) -> Optional[str]:
    """
    Get the owner's JWT token for a user's personal bot.

    Used for bot→user project sharing. Bot API tokens can't see users,
    but owner's JWT token can. We use owner's token to share bot-created
    projects with the owner.

    Fixes solutions-2x6i: Bot Project Sharing Bug

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        vikunja_instance: Vikunja instance name

    Returns:
        Decrypted owner JWT token, or None if not found
    """
    rows = execute(
        """
        SELECT owner_vikunja_token FROM personal_bots
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    if not rows or not rows[0][0]:
        return None

    encrypted = rows[0][0]
    return decrypt_token(encrypted)


def get_user_bot_info(user_id: str, vikunja_instance: str = DEFAULT_INSTANCE) -> Optional[dict]:
    """
    Get full info for a user's personal bot from database.

    Used by EARS to get bot username and display name without needing API access.
    Fixes solutions-5yv5: bot token doesn't have /api/v1/user permission.

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        vikunja_instance: Vikunja instance name

    Returns:
        Dict with bot_username, display_name, vikunja_user_id, or None if not found
    """
    rows = execute(
        """
        SELECT bot_username, display_name, vikunja_user_id FROM personal_bots
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    if not rows:
        return None

    return {
        "bot_username": rows[0][0],
        "display_name": rows[0][1],
        "vikunja_user_id": rows[0][2],
    }



def get_bot_owner_vikunja_id(user_id: str, vikunja_instance: str = DEFAULT_INSTANCE) -> Optional[int]:
    """
    Get the owner's Vikunja user ID for a bot.

    Used when bot creates a project and needs to share it back to owner.

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        vikunja_instance: Vikunja instance name

    Returns:
        Owner's Vikunja user ID, or None if not found
    """
    rows = execute(
        """
        SELECT owner_vikunja_user_id FROM personal_bots
        WHERE user_id = %s AND vikunja_instance = %s
        """,
        (user_id, vikunja_instance),
    )

    if not rows or rows[0][0] is None:
        logger.debug(f"[get_bot_owner_vikunja_id] No owner ID found for {user_id}")
        return None

    return rows[0][0]


def share_project_with_personal_bot(
    user_id: str,
    project_id: int,
    user_token: str,
    vikunja_url: str = None,
    vikunja_instance: str = DEFAULT_INSTANCE,
) -> bool:
    """
    Share a project with the user's personal bot.

    Called when user creates a new project so their bot can see it.

    Args:
        user_id: The user's ID (e.g., "vikunja:alice")
        project_id: Project to share
        user_token: User's Vikunja token (to make the share call)
        vikunja_url: Vikunja instance URL
        vikunja_instance: Vikunja instance name

    Returns:
        True if shared successfully
    """
    base_url = (vikunja_url or VIKUNJA_URL).rstrip('/')

    # Get bot's Vikunja user ID
    bot_vikunja_id = get_user_bot_vikunja_id(user_id, vikunja_instance)
    if not bot_vikunja_id:
        logger.error(f"[share] No bot found for {user_id}")
        return False

    # Share project with bot (read/write access)
    try:
        resp = requests.put(
            f"{base_url}/api/v1/projects/{project_id}/users",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "user_id": bot_vikunja_id,
                "right": 1,  # read/write
            },
            timeout=30,
        )

        if resp.status_code == 409:
            # Already shared - that's fine
            logger.debug(f"[share] Project {project_id} already shared with bot")
            return True

        resp.raise_for_status()
        logger.info(f"[share] Shared project {project_id} with bot for {user_id}")
        return True

    except requests.RequestException as e:
        logger.error(f"[share] Failed to share project {project_id}: {e}")
        return False


def get_all_bot_tokens(vikunja_instance: str = DEFAULT_INSTANCE) -> list[tuple[str, str]]:
    """
    DEPRECATED: Get all active bot tokens for multi-bot polling.

    This function is deprecated because API tokens are broken in Vikunja.
    Use get_all_bot_user_ids() instead.

    Returns:
        List of (user_id, bot_token) tuples (empty if no API tokens)
    """
    logger.warning("[get_all_bot_tokens] DEPRECATED: Use get_all_bot_user_ids() instead")
    rows = execute(
        """
        SELECT user_id, encrypted_token FROM personal_bots
        WHERE vikunja_instance = %s AND encrypted_token IS NOT NULL
        ORDER BY created_at
        """,
        (vikunja_instance,),
    )

    result = []
    for user_id, encrypted_token in rows:
        try:
            token = decrypt_token(bytes(encrypted_token))
            result.append((user_id, token))
        except Exception as e:
            logger.error(f"[get_all_bot_tokens] Failed to decrypt token for {user_id}: {e}")

    return result


def get_all_bot_user_ids(vikunja_instance: str = DEFAULT_INSTANCE) -> list[str]:
    """
    Get all user IDs that have personal bots (for multi-bot polling).

    Used by notification poller to create BotVikunjaClient instances with JWT auth.

    Returns:
        List of user_ids (e.g., ["vikunja:alice", "vikunja:bob"])
    """
    rows = execute(
        """
        SELECT user_id FROM personal_bots
        WHERE vikunja_instance = %s AND encrypted_password IS NOT NULL
        ORDER BY created_at
        """,
        (vikunja_instance,),
    )

    return [row[0] for row in rows]


def get_users_needing_service() -> list[str]:
    """
    Get user IDs that currently need bot service.

    This is the primary query for the centralized poller to determine
    which bots to initialize.

    Only returns Vikunja personal bot users (user_id starts with 'vikunja:').
    Matrix users are excluded (deprecated architecture).

    Returns:
        List of user IDs that have service_needed=true

    Bead: solutions-skqu
    """
    rows = execute(
        """
        SELECT user_id FROM factumerit_users
        WHERE service_needed = TRUE
        AND is_active = TRUE
        AND user_id LIKE %s
        ORDER BY service_requested_at
        """,
        ('vikunja:%',),
    )

    return [row[0] for row in rows]


def set_service_needed(user_id: str, needed: bool, reason: str = None):
    """
    Set service_needed flag for a user.

    Args:
        user_id: User ID (e.g., "vikunja:alice" or "vikunja:alice:123")
        needed: True if user needs service, False otherwise
        reason: Reason for service request (e.g., "ears_on", "mention", "manual")

    Note: user_id is normalized to 2-element format (fa-me5dj)

    Bead: solutions-skqu
    """
    # Normalize to 2-element format (fa-me5dj)
    user_id = normalize_vikunja_user_id(user_id)

    if needed:
        execute(
            """
            UPDATE factumerit_users
            SET service_needed = TRUE,
                service_requested_at = NOW(),
                service_reason = %s
            WHERE user_id = %s
            """,
            (reason, user_id),
        )
        logger.info(f"[set_service_needed] {user_id}: service_needed=TRUE (reason: {reason})")
    else:
        execute(
            """
            UPDATE factumerit_users
            SET service_needed = FALSE,
                service_reason = NULL
            WHERE user_id = %s
            """,
            (user_id,),
        )
        logger.info(f"[set_service_needed] {user_id}: service_needed=FALSE")


def update_service_last_active(user_id: str):
    """
    Update service_last_active timestamp for a user.

    Called by the poller after each poll/EARS scan to track activity.

    Args:
        user_id: User ID (e.g., "vikunja:alice" or "vikunja:alice:123")

    Note: user_id is normalized to 2-element format (fa-me5dj)

    Bead: solutions-skqu
    """
    # Normalize to 2-element format (fa-me5dj)
    user_id = normalize_vikunja_user_id(user_id)

    execute(
        """
        UPDATE factumerit_users
        SET service_last_active = NOW()
        WHERE user_id = %s
        """,
        (user_id,),
    )


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Look up a Factumerit user by their email address.

    Args:
        email: Email address to search for

    Returns:
        Dict with user_id, platform, email, is_active, or None if not found
    """
    rows = execute(
        """
        SELECT user_id, platform, email, is_active
        FROM factumerit_users
        WHERE email = %s
        """,
        (email,),
    )

    if not rows:
        return None

    return {
        "user_id": rows[0][0],
        "platform": rows[0][1],
        "email": rows[0][2],
        "is_active": rows[0][3],
    }


def get_user_email(user_id: str) -> Optional[str]:
    """
    Get a Factumerit user's email address by their user_id.

    Args:
        user_id: Factumerit user ID (e.g., "vikunja:username")

    Returns:
        Email address or None if not found
    """
    rows = execute(
        """
        SELECT email
        FROM factumerit_users
        WHERE user_id = %s
        """,
        (user_id,),
    )

    if not rows or not rows[0][0]:
        return None

    return rows[0][0]


@dataclass
class DeleteUserResult:
    """Result of delete_user operation."""
    email: str
    user_id: str                    # factumerit user_id (e.g., "vikunja:username")
    owner_vikunja_id: Optional[int] # User's Vikunja account ID
    bot_vikunja_id: Optional[int]   # Bot's Vikunja account ID
    bot_username: Optional[str]     # Bot username (e.g., "eis-username")

    # What was deleted
    factumerit_deleted: bool        # factumerit_users record
    bot_record_deleted: bool        # personal_bots record
    vikunja_user_deleted: bool      # User's Vikunja account
    vikunja_bot_deleted: bool       # Bot's Vikunja account
    balance_forfeited_cents: int    # Unspent credit returned to equity

    errors: list[str]


def _delete_vikunja_account(base_url: str, vikunja_id: int, account_type: str) -> tuple[bool, Optional[str]]:
    """
    Delete a Vikunja account via API using JWT auth.

    Args:
        base_url: Vikunja API base URL
        vikunja_id: Vikunja user ID to delete
        account_type: "user" or "bot" (for logging)

    Returns:
        (success, error_message)
    """
    vikunja_user = os.environ.get("VIKUNJA_USER")
    vikunja_password = os.environ.get("VIKUNJA_PASSWORD")

    if not vikunja_user or not vikunja_password:
        return False, "VIKUNJA_USER/VIKUNJA_PASSWORD not set - cannot delete Vikunja account"

    try:
        # Get JWT token
        login_resp = requests.post(
            f"{base_url}/api/v1/login",
            json={"username": vikunja_user, "password": vikunja_password},
            timeout=30,
        )
        if login_resp.status_code != 200:
            return False, f"Vikunja login failed: {login_resp.status_code}"

        token = login_resp.json().get("token")
        if not token:
            return False, "No JWT token in login response"

        # Delete the account
        resp = requests.delete(
            f"{base_url}/api/v1/users/{vikunja_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )

        if resp.status_code == 200:
            logger.info(f"[delete] Deleted Vikunja {account_type} (id={vikunja_id})")
            return True, None
        elif resp.status_code == 404:
            logger.info(f"[delete] Vikunja {account_type} (id={vikunja_id}) not found (already deleted?)")
            return True, None
        else:
            return False, f"Vikunja API returned {resp.status_code}: {resp.text}"

    except requests.RequestException as e:
        return False, f"Vikunja API request failed: {e}"


def delete_user(
    email: str,
    vikunja_url: str = None,
    vikunja_instance: str = DEFAULT_INSTANCE,
    dry_run: bool = False,
) -> DeleteUserResult:
    """
    Delete a Factumerit user completely.

    Removes:
    1. User's Vikunja account (the human's account)
    2. Bot's Vikunja account (eis-username)
    3. personal_bots record (bot credentials)
    4. factumerit_users record (user registration)

    Args:
        email: User's email address
        vikunja_url: Vikunja instance URL
        vikunja_instance: Vikunja instance name
        dry_run: Show what would be deleted without deleting

    Returns:
        DeleteUserResult with status of each deletion

    Raises:
        ProvisioningError: If user not found

    Bead: fa-letl
    """
    base_url = (vikunja_url or VIKUNJA_URL).rstrip('/')
    errors = []

    # Look up user by email
    user = get_user_by_email(email)
    if not user:
        raise ProvisioningError(f"No user found with email: {email}")

    user_id = user["user_id"]

    # Get bot info (may not exist)
    bot_info = get_user_bot_info(user_id, vikunja_instance)
    bot_username = bot_info["bot_username"] if bot_info else None
    bot_vikunja_id = bot_info["vikunja_user_id"] if bot_info else None

    # Get owner's Vikunja ID
    owner_vikunja_id = get_bot_owner_vikunja_id(user_id, vikunja_instance)

    logger.info(f"[delete_user] {'[DRY RUN] ' if dry_run else ''}Deleting user: {email}")
    logger.info(f"[delete_user]   user_id: {user_id}")
    logger.info(f"[delete_user]   owner_vikunja_id: {owner_vikunja_id}")
    logger.info(f"[delete_user]   bot_username: {bot_username}")
    logger.info(f"[delete_user]   bot_vikunja_id: {bot_vikunja_id}")

    result = DeleteUserResult(
        email=email,
        user_id=user_id,
        owner_vikunja_id=owner_vikunja_id,
        bot_vikunja_id=bot_vikunja_id,
        bot_username=bot_username,
        factumerit_deleted=False,
        bot_record_deleted=False,
        vikunja_user_deleted=False,
        vikunja_bot_deleted=False,
        balance_forfeited_cents=0,
        errors=[],
    )

    if dry_run:
        result.factumerit_deleted = True
        result.bot_record_deleted = bot_info is not None
        result.vikunja_user_deleted = owner_vikunja_id is not None
        result.vikunja_bot_deleted = bot_vikunja_id is not None
        return result

    # Step 0: Forfeit any remaining balance (returns to equity)
    try:
        forfeited = forfeit_balance(user_id, reason=f"Account deleted: {email}")
        result.balance_forfeited_cents = forfeited
        if forfeited > 0:
            logger.info(f"[delete_user] Forfeited {forfeited}¢ balance")
    except Exception as e:
        errors.append(f"Failed to forfeit balance: {e}")

    # Step 1: Delete bot's Vikunja account
    if bot_vikunja_id:
        success, err = _delete_vikunja_account(base_url, bot_vikunja_id, "bot")
        result.vikunja_bot_deleted = success
        if err:
            errors.append(err)

    # Step 2: Delete user's Vikunja account
    if owner_vikunja_id:
        success, err = _delete_vikunja_account(base_url, owner_vikunja_id, "user")
        result.vikunja_user_deleted = success
        if err:
            errors.append(err)

    # Step 3: Delete personal_bots record
    if bot_info:
        try:
            execute(
                "DELETE FROM personal_bots WHERE user_id = %s AND vikunja_instance = %s",
                (user_id, vikunja_instance),
            )
            result.bot_record_deleted = True
            logger.info(f"[delete_user] Deleted personal_bots record")
        except Exception as e:
            errors.append(f"Failed to delete personal_bots: {e}")

    # Step 4: Delete factumerit_users record
    try:
        execute(
            "DELETE FROM factumerit_users WHERE user_id = %s",
            (user_id,),
        )
        result.factumerit_deleted = True
        logger.info(f"[delete_user] Deleted factumerit_users record")
    except Exception as e:
        errors.append(f"Failed to delete factumerit_users: {e}")

    result.errors = errors
    return result


# Backwards compatibility alias
def delete_user_bot(email: str, delete_user: bool = False, delete_vikunja: bool = False, **kwargs):
    """DEPRECATED: Use delete_user() instead."""
    logger.warning("[delete_user_bot] DEPRECATED: Use delete_user() instead")
    return delete_user(email, **kwargs)
