"""
Bot JWT Manager - Manages JWT tokens for bot authentication.

Since Vikunja API tokens are broken (GitHub issue #105), bots use JWT tokens instead.
This module handles:
- JWT token caching with expiry tracking
- Automatic token refresh
- Thread-safe token management

Bead: solutions-xk9l (JWT Workaround for Broken API Tokens)
"""

import logging
import os
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Optional, Tuple
import httpx

logger = logging.getLogger(__name__)

# JWT token cache: {bot_username: (jwt_token, expiry_datetime)}
_jwt_cache: dict[str, Tuple[str, datetime]] = {}
_cache_lock = Lock()

# JWT tokens expire in 24 hours, refresh at 23 hours to be safe
JWT_EXPIRY_HOURS = 24
JWT_REFRESH_HOURS = 23


class BotJWTError(Exception):
    """Raised when bot JWT operations fail."""
    pass


def get_bot_jwt(
    bot_username: str,
    bot_password: str,
    vikunja_url: str,
    force_refresh: bool = False
) -> str:
    """
    Get JWT token for a bot, with caching.

    Args:
        bot_username: Bot username (e.g., "e-a1b2c3")
        bot_password: Bot password
        vikunja_url: Vikunja base URL (e.g., "https://vikunja.factumerit.app")
        force_refresh: Force refresh even if cached token is valid

    Returns:
        JWT token string

    Raises:
        BotJWTError: If login fails
    """
    with _cache_lock:
        # Check cache first
        if not force_refresh and bot_username in _jwt_cache:
            token, expiry = _jwt_cache[bot_username]
            if datetime.now(timezone.utc) < expiry:
                logger.debug(f"JWT cache hit for {bot_username}")
                return token
            else:
                logger.debug(f"JWT cache expired for {bot_username}")

        # Login to get new JWT
        logger.info(f"Logging in bot {bot_username} to get JWT token")
        try:
            response = httpx.post(
                f"{vikunja_url}/api/v1/login",
                json={
                    "username": bot_username,
                    "password": bot_password
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            jwt_token = data.get("token")
            
            if not jwt_token:
                raise BotJWTError(f"No token in login response for {bot_username}")

            # Cache with expiry
            expiry = datetime.now(timezone.utc) + timedelta(hours=JWT_REFRESH_HOURS)
            _jwt_cache[bot_username] = (jwt_token, expiry)
            
            logger.info(f"JWT token cached for {bot_username} until {expiry}")
            return jwt_token

        except httpx.HTTPStatusError as e:
            error_msg = f"Bot login failed for {bot_username}: {e.response.status_code}"
            if e.response.text:
                error_msg += f" - {e.response.text[:200]}"
            logger.error(error_msg)
            raise BotJWTError(error_msg)
        except httpx.RequestError as e:
            error_msg = f"Bot login request failed for {bot_username}: {e}"
            logger.error(error_msg)
            raise BotJWTError(error_msg)


def clear_bot_jwt_cache(bot_username: Optional[str] = None) -> None:
    """
    Clear JWT cache for a bot or all bots.

    Args:
        bot_username: Bot username to clear, or None to clear all
    """
    with _cache_lock:
        if bot_username:
            if bot_username in _jwt_cache:
                del _jwt_cache[bot_username]
                logger.info(f"Cleared JWT cache for {bot_username}")
        else:
            _jwt_cache.clear()
            logger.info("Cleared all JWT cache")


def get_cache_stats() -> dict:
    """
    Get JWT cache statistics for monitoring.

    Returns:
        Dict with cache size and expiry info
    """
    with _cache_lock:
        now = datetime.now(timezone.utc)
        valid_count = sum(1 for _, expiry in _jwt_cache.values() if now < expiry)
        expired_count = len(_jwt_cache) - valid_count
        
        return {
            "total_cached": len(_jwt_cache),
            "valid_tokens": valid_count,
            "expired_tokens": expired_count,
            "cache_entries": {
                username: {
                    "expires_at": expiry.isoformat(),
                    "is_valid": now < expiry
                }
                for username, (_, expiry) in _jwt_cache.items()
            }
        }

