"""
Token Broker - Secure token management for multi-tenant Vikunja access.

This module provides a single entry point for all token operations with:
- Encryption at rest (Fernet)
- Comprehensive audit logging
- No fallback to admin token
- Multi-instance support

Bead: solutions-kik7
Design: docs/designs/TOKEN_BROKER_DESIGN.md
"""

import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Optional
import base64

from cryptography.fernet import Fernet
from psycopg_pool import ConnectionPool

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class AuthRequired(Exception):
    """Raised when user needs to connect/reconnect to Vikunja.

    Attributes:
        refresh_url: One-click URL for seamless re-authentication (if token expired)
    """

    def __init__(self, message: str, refresh_url: str = None):
        super().__init__(message)
        self.refresh_url = refresh_url


class TokenBrokerUnavailable(Exception):
    """Raised when token broker cannot access database."""

    pass


# =============================================================================
# CONFIGURATION
# =============================================================================

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL")

# Encryption key (32-byte Fernet key, base64 encoded)
ENCRYPTION_KEY = os.environ.get("TOKEN_ENCRYPTION_KEY")

# OAuth base URL for refresh links
VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

# Cache settings
CACHE_TTL_SECONDS = 60  # 1 minute cache


# =============================================================================
# DATABASE CONNECTION POOL
# =============================================================================

_pool: Optional[ConnectionPool] = None


def _get_pool() -> ConnectionPool:
    """Get or create connection pool (lazy initialization)."""
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            raise TokenBrokerUnavailable("DATABASE_URL not configured")
        _pool = ConnectionPool(
            DATABASE_URL,
            min_size=2,  # Minimum connections
            max_size=10,  # Maximum connections (safe with 97 limit on Render Basic)
            timeout=30,  # Wait timeout for connection
            max_idle=300,  # Close idle connections after 5 min
            open=True,  # Explicitly open pool (required in future psycopg versions)
        )
    return _pool


@contextmanager
def get_db():
    """Get database connection from pool with automatic cleanup."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


def execute(query: str, params: tuple = None) -> list:
    """Execute query and return results."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:  # Has results
                return cur.fetchall()
            return []


# =============================================================================
# ENCRYPTION
# =============================================================================

_fernet: Optional[Fernet] = None


def _get_fernet() -> Fernet:
    """Get or create Fernet instance (lazy initialization)."""
    global _fernet
    if _fernet is None:
        if not ENCRYPTION_KEY:
            raise TokenBrokerUnavailable("TOKEN_ENCRYPTION_KEY not configured")
        _fernet = Fernet(ENCRYPTION_KEY.encode())
    return _fernet


def encrypt_token(token: str) -> bytes:
    """Encrypt a token for storage."""
    return _get_fernet().encrypt(token.encode())


def decrypt_token(encrypted: bytes) -> str:
    """Decrypt a token from storage."""
    return _get_fernet().decrypt(encrypted).decode()


# =============================================================================
# CACHING (Short-lived to reduce DB load)
# =============================================================================

_token_cache: dict[tuple[str, str], tuple[str, datetime]] = {}


def _get_cached_token(user_id: str, instance: str) -> Optional[str]:
    """Get token from cache if not expired."""
    key = (user_id, instance)
    if key in _token_cache:
        token, expires_at = _token_cache[key]
        if datetime.now(timezone.utc) < expires_at:
            return token
        del _token_cache[key]
    return None


def _set_cached_token(user_id: str, instance: str, token: str) -> None:
    """Cache token with TTL."""
    key = (user_id, instance)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=CACHE_TTL_SECONDS)
    _token_cache[key] = (token, expires_at)


def _invalidate_cache(user_id: str, instance: str) -> None:
    """Remove token from cache."""
    key = (user_id, instance)
    _token_cache.pop(key, None)


# =============================================================================
# CALLER TRACKING (Explicit, not inspect-based)
# =============================================================================


def token_operation(func):
    """Decorator to track caller info for audit logging."""

    @wraps(func)
    def wrapper(*args, caller: str = None, **kwargs):
        # Caller MUST be provided explicitly
        if caller is None:
            caller = f"{func.__module__}.{func.__name__}:unknown"
        return func(*args, caller=caller, **kwargs)

    return wrapper


# =============================================================================
# AUDIT LOGGING
# =============================================================================


def _log_access(
    user_id: str,
    instance: str,
    action: str,
    purpose: str,
    caller: str,
    success: bool,
    error: str = None,
) -> None:
    """Log token access to audit table.

    Args:
        user_id: Matrix or Slack user ID
        instance: Vikunja instance name
        action: What operation ('get', 'set', 'revoke')
        purpose: Why the token was needed ('!stats command', etc.)
        caller: Full caller path (e.g., 'matrix_handlers._handle_stats')
        success: Whether the operation succeeded
        error: Error message if failed
    """
    # Parse caller into module + function
    if "." in caller:
        caller_module, caller_function = caller.rsplit(".", 1)
    else:
        caller_module, caller_function = "unknown", caller

    try:
        execute(
            """
            INSERT INTO token_access_log
            (user_id, action, purpose, caller_module, caller_function, success, error_message)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (user_id, action, purpose, caller_module, caller_function, success, error),
        )
    except Exception as e:
        # Don't fail the main operation if logging fails
        logger.warning(f"Failed to log token access: {e}")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def _get_refresh_url(user_id: str, instance: str) -> str:
    """Generate one-click OAuth refresh URL for seamless re-authentication.

    Args:
        user_id: Matrix or Slack user ID
        instance: Vikunja instance name

    Returns:
        OAuth URL with state parameter encoding user context
    """
    # Encode user_id + instance in state parameter for callback to restore context
    state = base64.urlsafe_b64encode(f"{user_id}:{instance}".encode()).decode()

    # Use instance-specific OAuth URL if not default
    oauth_base = VIKUNJA_URL  # Default instance
    if instance != "default":
        # Could look up instance-specific URL from config
        pass

    return f"{oauth_base}/api/v1/auth/openid/factumerit?state={state}"


# =============================================================================
# CORE API
# =============================================================================


@token_operation
def get_user_token(
    user_id: str,
    purpose: str,
    instance: str = "default",
    caller: str = None,
) -> str:
    """
    Get decrypted Vikunja token for a user.

    Args:
        user_id: Matrix or Slack user ID
        purpose: Why the token is needed (for audit log)
        instance: Vikunja instance name (default: "default")
        caller: Who is calling (e.g., "matrix_handlers._handle_stats")

    Returns:
        Decrypted Vikunja API token

    Raises:
        AuthRequired: If user has no token or token is revoked/expired
        TokenBrokerUnavailable: If database is unavailable
    """
    # Check cache first
    cached = _get_cached_token(user_id, instance)
    if cached:
        logger.debug(f"Cache hit for {user_id}/{instance}")
        return cached

    try:
        # Query database
        rows = execute(
            """
            SELECT encrypted_token, revoked, expires_at
            FROM user_tokens
            WHERE user_id = %s AND vikunja_instance = %s
        """,
            (user_id, instance),
        )

        if not rows:
            _log_access(
                user_id, instance, "get", purpose, caller, success=False, error="no token found"
            )
            raise AuthRequired(f"No token for {user_id}")

        row = rows[0]
        encrypted_token, revoked, expires_at = row

        if revoked:
            _log_access(
                user_id, instance, "get", purpose, caller, success=False, error="token revoked"
            )
            raise AuthRequired(f"Token revoked for {user_id}")

        # Check expiration - raise with refresh URL for seamless re-auth
        if expires_at and datetime.now(timezone.utc) > expires_at:
            _log_access(
                user_id, instance, "get", purpose, caller, success=False, error="token expired"
            )
            # Include refresh URL so handler can show one-click re-auth
            raise AuthRequired(
                f"Token expired for {user_id}", refresh_url=_get_refresh_url(user_id, instance)
            )

        # Decrypt
        token = decrypt_token(encrypted_token)

        # Update access stats (async/background would be better)
        execute(
            """
            UPDATE user_tokens
            SET last_accessed_at = NOW(), access_count = access_count + 1
            WHERE user_id = %s AND vikunja_instance = %s
        """,
            (user_id, instance),
        )

        _log_access(user_id, instance, "get", purpose, caller, success=True)

        # Cache for subsequent requests
        _set_cached_token(user_id, instance, token)

        return token

    except (AuthRequired, TokenBrokerUnavailable):
        raise
    except Exception as e:
        logger.exception(f"Database error in get_user_token: {e}")
        _log_access(
            user_id, instance, "get", purpose, caller, success=False, error=f"database error: {e}"
        )
        raise TokenBrokerUnavailable("Token service temporarily unavailable")


@token_operation
def set_user_token(
    user_id: str,
    token: str,
    source: str,
    expires_at: datetime,
    instance: str = "default",
    instance_url: str = None,
    caller: str = None,
) -> None:
    """
    Store encrypted token for a user.

    Args:
        user_id: Matrix or Slack user ID
        token: Plaintext Vikunja API token
        source: Where the token came from ('oauth', 'manual', 'migration')
        expires_at: When the token expires (from Vikunja API response)
        instance: Vikunja instance name
        instance_url: Vikunja base URL (e.g., https://vikunja.factumerit.app)
        caller: Who is calling

    Note:
        If expires_at is unknown (e.g., migration), use:
            expires_at=datetime.now(timezone.utc) + timedelta(days=365)
    """
    encrypted = encrypt_token(token)

    execute(
        """
        INSERT INTO user_tokens (user_id, vikunja_instance, encrypted_token, expires_at, instance_url, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        ON CONFLICT (user_id, vikunja_instance) DO UPDATE SET
            encrypted_token = EXCLUDED.encrypted_token,
            expires_at = EXCLUDED.expires_at,
            instance_url = EXCLUDED.instance_url,
            revoked = FALSE,
            revoked_at = NULL,
            revoked_reason = NULL
    """,
        (user_id, instance, encrypted, expires_at, instance_url),
    )

    # Invalidate cache
    _invalidate_cache(user_id, instance)

    _log_access(user_id, instance, "set", source, caller, success=True)

    # Auto-set active instance if user doesn't have one
    # This ensures first-time users don't get "No active instance" errors
    try:
        if not get_user_active_instance(user_id):
            set_user_active_instance(user_id, instance)
    except Exception as e:
        # Don't fail token storage if active instance setting fails
        # (e.g., in tests with mocked database)
        logger.warning(f"Could not auto-set active instance for {user_id}: {e}")


@token_operation
def revoke_user_token(
    user_id: str,
    reason: str,
    instance: str = "default",
    caller: str = None,
) -> bool:
    """
    Revoke a user's token.

    Args:
        user_id: Matrix or Slack user ID
        reason: Why the token is being revoked
        instance: Vikunja instance name
        caller: Who is calling

    Returns:
        True if token was revoked, False if no token existed
    """
    result = execute(
        """
        UPDATE user_tokens
        SET revoked = TRUE, revoked_at = NOW(), revoked_reason = %s
        WHERE user_id = %s AND vikunja_instance = %s AND revoked = FALSE
        RETURNING user_id
    """,
        (reason, user_id, instance),
    )

    # Invalidate cache
    _invalidate_cache(user_id, instance)

    success = len(result) > 0
    _log_access(user_id, instance, "revoke", reason, caller, success=success)

    return success


def has_user_token(user_id: str, instance: str = "default") -> bool:
    """
    Quick check if user has a valid token (for early UX feedback).
    Does NOT log access or update stats.
    """
    # Check cache first
    if _get_cached_token(user_id, instance):
        return True

    try:
        rows = execute(
            """
            SELECT 1 FROM user_tokens
            WHERE user_id = %s AND vikunja_instance = %s AND revoked = FALSE
        """,
            (user_id, instance),
        )
        return len(rows) > 0
    except Exception:
        return False  # Fail open for UX check only


def get_system_token(name: str, purpose: str) -> str:
    """
    Get a system token for admin operations.

    This is completely separate from user tokens.
    Only used for: waiting list, health checks, etc.

    Args:
        name: Token name ('waiting_list', 'admin')
        purpose: Why the token is needed

    Returns:
        Decrypted system token

    Raises:
        ValueError: If system token not configured
    """
    rows = execute(
        """
        SELECT encrypted_token FROM system_tokens WHERE name = %s
    """,
        (name,),
    )

    if not rows:
        raise ValueError(f"System token '{name}' not configured")

    logger.info(f"System token '{name}' accessed for: {purpose}")

    return decrypt_token(rows[0][0])


# =============================================================================
# DEBUGGING / ADMIN
# =============================================================================


def get_user_token_info(user_id: str, instance: str = "default") -> Optional[dict]:
    """Get token metadata (without the actual token) for debugging."""
    rows = execute(
        """
        SELECT
            created_at, last_accessed_at, access_count,
            expires_at, revoked, revoked_at, revoked_reason
        FROM user_tokens
        WHERE user_id = %s AND vikunja_instance = %s
    """,
        (user_id, instance),
    )

    if not rows:
        return None

    row = rows[0]
    return {
        "user_id": user_id,
        "instance": instance,
        "created_at": row[0],
        "last_accessed_at": row[1],
        "access_count": row[2],
        "expires_at": row[3],
        "revoked": row[4],
        "revoked_at": row[5],
        "revoked_reason": row[6],
    }


def get_token_stats() -> dict:
    """Get token statistics for monitoring dashboard."""
    rows = execute(
        """
        SELECT
            COUNT(*) FILTER (WHERE revoked = FALSE) as active_tokens,
            COUNT(*) FILTER (WHERE revoked = TRUE) as revoked_tokens,
            COUNT(*) FILTER (WHERE revoked = FALSE AND expires_at < NOW()) as expired_tokens,
            COUNT(*) FILTER (WHERE revoked = FALSE AND expires_at BETWEEN NOW() AND NOW() + INTERVAL '30 days') as expiring_soon
        FROM user_tokens
    """
    )

    if not rows:
        return {"active_tokens": 0, "revoked_tokens": 0, "expired_tokens": 0, "expiring_soon": 0}

    row = rows[0]
    return {
        "active_tokens": row[0] or 0,
        "revoked_tokens": row[1] or 0,
        "expired_tokens": row[2] or 0,
        "expiring_soon": row[3] or 0,
    }


# =============================================================================
# REQUEST INTERACTION LOGGING
# =============================================================================

def log_interaction(
    user_id: str,
    vikunja_instance: str,
    command: str,
    request_type: str,
    results_count: int,
    success: bool,
    filter_applied: str = None,
    error_message: str = None,
    response_preview: str = None,
    execution_time_ms: int = None,
) -> None:
    """Log user interaction for debugging and analytics.
    
    Args:
        user_id: Matrix or Slack user ID
        vikunja_instance: Which Vikunja instance
        command: Command executed ('!maybe', '!stats', etc.)
        request_type: Type of request ('filter_command', 'llm_query', 'test')
        results_count: How many results returned
        success: Whether the request succeeded
        filter_applied: Filter used (if any)
        error_message: Error message (if failed)
        response_preview: First 200 chars of response
        execution_time_ms: Execution time in milliseconds
    """
    try:
        # Truncate response preview to 200 chars
        if response_preview and len(response_preview) > 200:
            response_preview = response_preview[:197] + "..."
        
        execute(
            """
            INSERT INTO request_interactions
            (user_id, vikunja_instance, command, request_type, filter_applied, 
             results_count, success, error_message, response_preview, execution_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                user_id,
                vikunja_instance,
                command,
                request_type,
                filter_applied,
                results_count,
                success,
                error_message,
                response_preview,
                execution_time_ms,
            ),
        )
    except Exception as e:
        # Don't fail the main operation if logging fails
        logger.warning(f"Failed to log interaction: {e}")


def get_user_instances(user_id: str) -> list[str]:
    """Get list of all Vikunja instances the user has tokens for.

    Args:
        user_id: Matrix or Slack user ID

    Returns:
        List of instance names (e.g., ['personal', 'business'])
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT vikunja_instance
                    FROM user_tokens
                    WHERE user_id = %s AND revoked = FALSE
                    ORDER BY vikunja_instance
                    """,
                    (user_id,)
                )
                rows = cur.fetchall()
                return [row[0] for row in rows]
    except Exception as e:
        logger.error(f"Error getting instances for {user_id}: {e}")
        return []


def get_user_active_instance(user_id: str) -> str | None:
    """Get user's active Vikunja instance from PostgreSQL.

    Args:
        user_id: Matrix or Slack user ID

    Returns:
        Instance name if set, None otherwise
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT active_instance FROM user_preferences WHERE user_id = %s",
                    (user_id,)
                )
                row = cur.fetchone()
                return row[0] if row else None
    except Exception as e:
        logger.error(f"Error getting active instance for {user_id}: {e}")
        return None


def set_user_active_instance(user_id: str, instance: str) -> None:
    """Set user's active Vikunja instance in PostgreSQL.

    Args:
        user_id: Matrix or Slack user ID
        instance: Instance name to set as active
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_preferences (user_id, active_instance)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET active_instance = %s, updated_at = NOW()
                    """,
                    (user_id, instance, instance)
                )
                conn.commit()
                logger.info(f"Set active_instance={instance} for {user_id}")
    except Exception as e:
        logger.error(f"Error setting active instance for {user_id}: {e}")
        raise


def get_user_instance_url(user_id: str, instance: str = "default") -> str | None:
    """Get Vikunja base URL for a user's instance.

    Args:
        user_id: Matrix or Slack user ID
        instance: Instance name

    Returns:
        Base URL (e.g., https://vikunja.factumerit.app) or None if not set
    """
    try:
        rows = execute(
            "SELECT instance_url FROM user_tokens WHERE user_id = %s AND vikunja_instance = %s AND revoked = FALSE",
            (user_id, instance),
        )
        if rows and rows[0][0]:
            return rows[0][0]
        return None
    except Exception as e:
        logger.error(f"Error getting instance URL for {user_id}/{instance}: {e}")
        return None


def get_user_active_project(user_id: str) -> dict | None:
    """Get user's active Vikunja project from PostgreSQL.

    Args:
        user_id: Matrix or Slack user ID

    Returns:
        Dict with 'id' and 'name' keys if set, None otherwise
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT active_project_id, active_project_name FROM user_preferences WHERE user_id = %s",
                    (user_id,)
                )
                row = cur.fetchone()
                if row and row[0] is not None:
                    return {"id": row[0], "name": row[1]}
                return None
    except Exception as e:
        logger.error(f"Error getting active project for {user_id}: {e}")
        return None


def set_user_active_project(user_id: str, project_id: int | None, project_name: str | None = None) -> None:
    """Set user's active Vikunja project in PostgreSQL.

    Args:
        user_id: Matrix or Slack user ID
        project_id: Project ID to set as active, or None to clear
        project_name: Project name (optional, for display)
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                if project_id is None:
                    # Clear active project
                    cur.execute(
                        """
                        UPDATE user_preferences
                        SET active_project_id = NULL, active_project_name = NULL, updated_at = NOW()
                        WHERE user_id = %s
                        """,
                        (user_id,)
                    )
                else:
                    # Set active project (upsert)
                    cur.execute(
                        """
                        INSERT INTO user_preferences (user_id, active_project_id, active_project_name)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE
                        SET active_project_id = %s, active_project_name = %s, updated_at = NOW()
                        """,
                        (user_id, project_id, project_name, project_id, project_name)
                    )
                conn.commit()
                if project_id is None:
                    logger.info(f"Cleared active_project for {user_id}")
                else:
                    logger.info(f"Set active_project={project_id} ({project_name}) for {user_id}")
    except Exception as e:
        logger.error(f"Error setting active project for {user_id}: {e}")
        raise


# =============================================================================
# PENDING CONNECTIONS (OAuth Nonces) - PostgreSQL-backed
# =============================================================================
# These functions replace the YAML-file based pending connections.
# Fixes issue where Render deploys wipe the ephemeral filesystem.
# Bead: solutions-fp44

import secrets

PENDING_CONNECTION_TTL_SECONDS = 600  # 10 minutes (was 5, increased for mobile)

_pending_connections_table_ensured = False


def _ensure_pending_connections_table() -> None:
    """Ensure pending_connections table exists (auto-migration)."""
    global _pending_connections_table_ensured
    if _pending_connections_table_ensured:
        return

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS pending_connections (
                        nonce TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        platform TEXT NOT NULL DEFAULT 'slack',
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        expires_at TIMESTAMPTZ NOT NULL
                    )
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_pending_connections_expires
                    ON pending_connections (expires_at)
                """)
                conn.commit()
        _pending_connections_table_ensured = True
        logger.debug("Ensured pending_connections table exists")
    except Exception as e:
        logger.warning(f"Could not ensure pending_connections table: {e}")


def create_pending_connection(user_id: str, platform: str = None) -> str:
    """Create a pending OAuth connection in PostgreSQL.

    Args:
        user_id: User ID (Matrix @user:domain or Slack ID)
        platform: 'slack' or 'matrix' (auto-detected if not provided)

    Returns:
        nonce: Cryptographically secure random string to use as OAuth state
    """
    # Ensure table exists (auto-migration on first use)
    _ensure_pending_connections_table()

    # Auto-detect platform from user_id format
    if platform is None:
        platform = "matrix" if user_id.startswith("@") and ":" in user_id else "slack"

    # Generate cryptographically secure nonce
    nonce = secrets.token_urlsafe(32)

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Clean up expired entries first (housekeeping)
                cur.execute(
                    "DELETE FROM pending_connections WHERE expires_at < NOW()"
                )

                # Insert new pending connection
                cur.execute(
                    """
                    INSERT INTO pending_connections (nonce, user_id, platform, expires_at)
                    VALUES (%s, %s, %s, NOW() + INTERVAL '%s seconds')
                    """,
                    (nonce, user_id, platform, PENDING_CONNECTION_TTL_SECONDS)
                )
                conn.commit()

        logger.info(f"Created pending connection for {platform} user {user_id}: {nonce[:8]}...")
        return nonce

    except Exception as e:
        logger.error(f"Error creating pending connection for {user_id}: {e}")
        raise


def get_pending_connection(nonce: str) -> dict | None:
    """Get pending connection by nonce.

    Args:
        nonce: OAuth state parameter

    Returns:
        Dict with user_id and platform, or None if not found/expired
    """
    try:
        rows = execute(
            """
            SELECT user_id, platform
            FROM pending_connections
            WHERE nonce = %s AND expires_at > NOW()
            """,
            (nonce,)
        )

        if rows:
            return {
                "user_id": rows[0][0],
                "platform": rows[0][1],
            }
        return None

    except Exception as e:
        logger.error(f"Error getting pending connection {nonce[:8]}...: {e}")
        return None


def delete_pending_connection(nonce: str) -> bool:
    """Delete a pending connection (after successful OAuth).

    Args:
        nonce: OAuth state parameter

    Returns:
        True if deleted, False if not found
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM pending_connections WHERE nonce = %s",
                    (nonce,)
                )
                deleted = cur.rowcount > 0
                conn.commit()

        if deleted:
            logger.debug(f"Deleted pending connection: {nonce[:8]}...")
        return deleted

    except Exception as e:
        logger.error(f"Error deleting pending connection {nonce[:8]}...: {e}")
        return False


def cleanup_expired_pending_connections() -> int:
    """Clean up expired pending connections.

    Returns:
        Number of entries deleted
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM pending_connections WHERE expires_at < NOW()"
                )
                count = cur.rowcount
                conn.commit()

        if count > 0:
            logger.info(f"Cleaned up {count} expired pending connections")
        return count

    except Exception as e:
        logger.error(f"Error cleaning up pending connections: {e}")
        return 0


# =============================================================================
# USER REGISTRATION (Factumerit authorization)
# =============================================================================
# These functions manage the `users` table which is the source of truth
# for who is authorized to use LLM features.

_users_table_ensured = False


def _ensure_users_table() -> None:
    """Ensure factumerit_users table exists (auto-migration)."""
    global _users_table_ensured
    if _users_table_ensured:
        return

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS factumerit_users (
                        user_id TEXT PRIMARY KEY,
                        platform TEXT NOT NULL,
                        email TEXT,
                        registered_at TIMESTAMPTZ DEFAULT NOW(),
                        registered_via TEXT DEFAULT 'oauth',
                        is_active BOOLEAN DEFAULT TRUE,
                        notes TEXT
                    )
                """)
                conn.commit()
        _users_table_ensured = True
    except Exception as e:
        logger.warning(f"Could not ensure factumerit_users table: {e}")


def get_canonical_email(email: str) -> str:
    """Extract canonical email by stripping +alias.

    Examples:
        ivan+work@gmail.com -> ivan@gmail.com
        ivan@gmail.com -> ivan@gmail.com
    """
    if not email or '@' not in email:
        return email
    import re
    return re.sub(r'\+[^@]*@', '@', email)


def register_user(
    user_id: str,
    platform: str = None,
    email: str = None,
    registered_via: str = "oauth",
    workspace_name: str = None,
    is_primary: bool = None
) -> bool:
    """Register a user as authorized Factumerit user.

    This should ONLY be called from official onboarding flows (OAuth callback).
    NOT from !vik commands.

    Args:
        user_id: Matrix or Slack user ID
        platform: 'matrix' or 'slack' (auto-detected if not provided)
        email: User's email (optional)
        registered_via: How they registered ('oauth', 'admin', 'migration')
        workspace_name: Name for this workspace (e.g., 'Business', 'Personal')
        is_primary: Whether this is the primary workspace for this identity

    Returns:
        True if registered (or already registered), False on error
    """
    _ensure_users_table()

    # Auto-detect platform
    if platform is None:
        if user_id.startswith("vikunja:"):
            platform = "vikunja"
        elif user_id.startswith("@") and ":" in user_id:
            platform = "matrix"
        else:
            platform = "slack"

    # Extract canonical email (strip +alias)
    google_identity = get_canonical_email(email) if email else None

    # If this is the first account for this identity, make it primary
    if is_primary is None and google_identity:
        existing = get_user_workspaces(google_identity)
        is_primary = len(existing) == 0

    # Default workspace name
    if workspace_name is None:
        workspace_name = "Default"

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO factumerit_users
                        (user_id, platform, email, registered_via, google_identity, is_primary, workspace_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET is_active = TRUE,
                        email = COALESCE(EXCLUDED.email, factumerit_users.email),
                        google_identity = COALESCE(EXCLUDED.google_identity, factumerit_users.google_identity),
                        workspace_name = COALESCE(EXCLUDED.workspace_name, factumerit_users.workspace_name)
                    """,
                    (user_id, platform, email, registered_via, google_identity, is_primary, workspace_name)
                )
                conn.commit()

        logger.info(f"Registered user {user_id} via {registered_via} (workspace: {workspace_name}, primary: {is_primary})")
        return True

    except Exception as e:
        logger.error(f"Error registering user {user_id}: {e}")
        return False


def get_user_workspaces(google_identity: str) -> list[dict]:
    """Get all workspaces/accounts linked to a Google identity.

    Args:
        google_identity: Canonical email (e.g., ivan@gmail.com)

    Returns:
        List of workspace dicts with user_id, workspace_name, is_primary, email
    """
    _ensure_users_table()

    try:
        rows = execute(
            """
            SELECT user_id, workspace_name, is_primary, email, registered_at
            FROM factumerit_users
            WHERE google_identity = %s AND is_active = TRUE
            ORDER BY is_primary DESC, registered_at ASC
            """,
            (google_identity,)
        )
        return [
            {
                "user_id": row[0],
                "workspace_name": row[1] or "Default",
                "is_primary": row[2] or False,
                "email": row[3],
                "registered_at": row[4].isoformat() if row[4] else None
            }
            for row in (rows or [])
        ]
    except Exception as e:
        logger.error(f"Error getting workspaces for {google_identity}: {e}")
        return []


def link_workspace(
    google_identity: str,
    user_id: str,
    workspace_name: str = None,
    is_primary: bool = False
) -> bool:
    """Link an existing Vikunja account to a Google identity.

    Use this to associate existing accounts with your canonical identity.

    Args:
        google_identity: Canonical email (e.g., ivan@gmail.com)
        user_id: Vikunja user ID (e.g., vikunja:ivan-personal)
        workspace_name: Display name for this workspace
        is_primary: Whether this should be the primary workspace

    Returns:
        True on success, False on error
    """
    _ensure_users_table()

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # If setting as primary, clear other primaries first
                if is_primary:
                    cur.execute(
                        "UPDATE factumerit_users SET is_primary = FALSE WHERE google_identity = %s",
                        (google_identity,)
                    )

                cur.execute(
                    """
                    UPDATE factumerit_users
                    SET google_identity = %s,
                        workspace_name = COALESCE(%s, workspace_name, 'Default'),
                        is_primary = %s
                    WHERE user_id = %s
                    """,
                    (google_identity, workspace_name, is_primary, user_id)
                )

                if cur.rowcount == 0:
                    logger.warning(f"User {user_id} not found for linking")
                    return False

                conn.commit()

        logger.info(f"Linked {user_id} to {google_identity} (workspace: {workspace_name}, primary: {is_primary})")
        return True

    except Exception as e:
        logger.error(f"Error linking workspace {user_id} to {google_identity}: {e}")
        return False


def set_primary_workspace(google_identity: str, user_id: str) -> bool:
    """Set a workspace as the primary for a Google identity.

    Args:
        google_identity: Canonical email
        user_id: User ID to make primary

    Returns:
        True on success, False on error
    """
    _ensure_users_table()

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Clear existing primary
                cur.execute(
                    "UPDATE factumerit_users SET is_primary = FALSE WHERE google_identity = %s",
                    (google_identity,)
                )
                # Set new primary
                cur.execute(
                    "UPDATE factumerit_users SET is_primary = TRUE WHERE user_id = %s AND google_identity = %s",
                    (user_id, google_identity)
                )
                if cur.rowcount == 0:
                    logger.warning(f"User {user_id} not found or not linked to {google_identity}")
                    return False
                conn.commit()

        logger.info(f"Set {user_id} as primary for {google_identity}")
        return True

    except Exception as e:
        logger.error(f"Error setting primary workspace: {e}")
        return False


def is_registered_user(user_id: str) -> bool:
    """Check if user is a registered (authorized) Factumerit user.

    This is the gate for LLM access.

    Args:
        user_id: Matrix or Slack user ID

    Returns:
        True if user is registered and active, False otherwise
    """
    _ensure_users_table()

    try:
        rows = execute(
            "SELECT is_active FROM factumerit_users WHERE user_id = %s",
            (user_id,)
        )
        if rows and rows[0][0]:
            return True
        return False

    except Exception as e:
        logger.error(f"Error checking user registration {user_id}: {e}")
        return False


def deactivate_user(user_id: str, reason: str = None) -> bool:
    """Deactivate a user (revoke LLM access without deleting).

    Args:
        user_id: Matrix or Slack user ID
        reason: Optional reason for deactivation

    Returns:
        True if deactivated, False on error
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE factumerit_users
                    SET is_active = FALSE, notes = COALESCE(notes || E'\n', '') || %s
                    WHERE user_id = %s
                    """,
                    (f"Deactivated: {reason}" if reason else "Deactivated", user_id)
                )
                conn.commit()

        logger.info(f"Deactivated user {user_id}: {reason}")
        return True

    except Exception as e:
        logger.error(f"Error deactivating user {user_id}: {e}")
        return False
