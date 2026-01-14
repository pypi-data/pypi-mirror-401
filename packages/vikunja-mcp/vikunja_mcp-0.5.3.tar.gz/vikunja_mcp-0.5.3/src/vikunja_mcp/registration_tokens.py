"""
Registration token validation for gated beta access.

Bead: solutions-8zly.2, solutions-8zly.3
"""
from datetime import datetime, timezone
from typing import Any

from psycopg.rows import dict_row

from .token_broker import get_db, execute


# =============================================================================
# EXCEPTIONS
# =============================================================================


class RegistrationTokenError(Exception):
    """Base exception for registration token errors."""
    pass


class TokenNotFoundError(RegistrationTokenError):
    """Token does not exist."""
    pass


class TokenExhaustedError(RegistrationTokenError):
    """Token has no remaining uses."""
    pass


class TokenExpiredError(RegistrationTokenError):
    """Token has expired."""
    pass


class TokenRevokedError(RegistrationTokenError):
    """Token has been revoked."""
    pass


class DuplicateSignupError(RegistrationTokenError):
    """User has already signed up with this token."""
    pass


# =============================================================================
# CORE API
# =============================================================================


def validate_registration_token(token: str, user_id: str) -> dict[str, Any]:
    """
    Validate registration token and check if user can sign up.

    Args:
        token: Registration token (e.g., NSA-NORTHWEST-50)
        user_id: User identifier (email)

    Returns:
        dict with token info: {
            'token': str,
            'group_id': int | None,
            'max_uses': int,
            'uses_remaining': int,
            'expires_at': datetime | None,
            'notes': str | None,
            'initial_credit_cents': int,
            'ttl_days': int | None  # Days until promo credit expires after signup
        }

    Raises:
        TokenNotFoundError: Token does not exist
        TokenRevokedError: Token has been revoked
        TokenExpiredError: Token has expired
        TokenExhaustedError: Token has no remaining uses
        DuplicateSignupError: User already used this token
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Fetch token
            cur.execute("""
                SELECT token, group_id, state, max_uses, uses_remaining,
                       expires_at, notes, initial_credit_cents, ttl_days
                FROM registration_tokens
                WHERE token = %s
            """, (token,))

            result = cur.fetchone()

            if not result:
                raise TokenNotFoundError(f"Registration code '{token}' not found")

            token_data = dict(result)

            # Check state
            if token_data['state'] == 'revoked':
                raise TokenRevokedError("Registration code has been revoked")

            # Check expiration
            if token_data['expires_at']:
                now = datetime.now(timezone.utc)
                expires_at = token_data['expires_at']
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                if now > expires_at:
                    raise TokenExpiredError(
                        f"Registration code expired on {token_data['expires_at'].date()}"
                    )

            # Check for duplicate signup FIRST (before exhaustion check)
            # This ensures duplicate POSTs get the correct error message
            cur.execute("""
                SELECT 1 FROM token_usage
                WHERE token = %s AND user_id = %s
            """, (token, user_id))

            if cur.fetchone():
                raise DuplicateSignupError(
                    f"Email '{user_id}' has already signed up with this code"
                )

            # Check uses remaining (after duplicate check)
            if token_data['uses_remaining'] <= 0:
                raise TokenExhaustedError(
                    f"Registration code has been fully used "
                    f"({token_data['max_uses']}/{token_data['max_uses']} signups)"
                )

            return token_data


def record_token_usage(token: str, user_id: str) -> None:
    """
    Record token usage and decrement uses_remaining.

    This should be called AFTER successful user provisioning.
    Uses a transaction to ensure atomicity.

    Args:
        token: Registration token
        user_id: User identifier (email)
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            # Insert usage record
            cur.execute("""
                INSERT INTO token_usage (token, user_id, used_at)
                VALUES (%s, %s, NOW())
            """, (token, user_id))

            # Decrement uses_remaining and update state if exhausted
            cur.execute("""
                UPDATE registration_tokens
                SET uses_remaining = uses_remaining - 1,
                    state = CASE
                        WHEN uses_remaining - 1 <= 0 THEN 'exhausted'
                        ELSE state
                    END
                WHERE token = %s
            """, (token,))

            conn.commit()


def get_token_stats(token: str) -> dict[str, Any]:
    """
    Get usage statistics for a registration token.

    Args:
        token: Registration token

    Returns:
        dict with stats: {
            'token': str,
            'state': str,
            'max_uses': int,
            'uses_remaining': int,
            'used_count': int,
            'initial_credit_cents': int,
            'ttl_days': int | None,
            'expires_at': datetime | None,
            'notes': str | None,
            'recent_signups': list[dict]  # Last 10 signups
        }
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Get token info
            cur.execute("""
                SELECT token, state, max_uses, uses_remaining, expires_at, notes, initial_credit_cents, ttl_days
                FROM registration_tokens
                WHERE token = %s
            """, (token,))

            token_data = cur.fetchone()
            if not token_data:
                raise TokenNotFoundError(f"Token '{token}' not found")

            stats = dict(token_data)

            # Get usage count
            cur.execute("""
                SELECT COUNT(*) as used_count
                FROM token_usage
                WHERE token = %s
            """, (token,))

            stats['used_count'] = cur.fetchone()['used_count']

            # Get recent signups
            cur.execute("""
                SELECT user_id, used_at
                FROM token_usage
                WHERE token = %s
                ORDER BY used_at DESC
                LIMIT 10
            """, (token,))

            stats['recent_signups'] = [dict(row) for row in cur.fetchall()]

            return stats
