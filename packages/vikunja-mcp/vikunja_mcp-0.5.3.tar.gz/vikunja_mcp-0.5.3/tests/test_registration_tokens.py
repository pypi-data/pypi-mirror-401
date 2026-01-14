"""
Unit tests for registration token validation.

Beads: solutions-8zly.2, solutions-8zly.3

These tests use mocking to avoid database dependencies.
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

# Direct import to avoid __init__.py importing server.py
import vikunja_mcp.registration_tokens as registration_tokens
from vikunja_mcp.registration_tokens import (
    validate_registration_token,
    record_token_usage,
    get_token_stats,
    TokenNotFoundError,
    TokenExhaustedError,
    TokenExpiredError,
    TokenRevokedError,
    DuplicateSignupError,
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def mock_db_connection():
    """Create a mock database connection with cursor context manager."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Set up context manager behavior
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    return mock_conn, mock_cursor


@pytest.fixture
def mock_get_db(mock_db_connection):
    """Patch get_db to return mock connection."""
    mock_conn, mock_cursor = mock_db_connection

    with patch.object(registration_tokens, "get_db") as mock:
        mock.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_conn, mock_cursor


# =============================================================================
# VALIDATION TESTS
# =============================================================================


class TestValidateRegistrationToken:
    """Test registration token validation."""

    def test_validate_valid_token(self, mock_get_db):
        """Test validation of valid token."""
        mock_conn, mock_cursor = mock_get_db

        # Mock token data
        mock_cursor.fetchone.side_effect = [
            # First call: token data
            {
                "token": "TEST-TOKEN-50",
                "group_id": None,
                "state": "active",
                "max_uses": 50,
                "uses_remaining": 50,
                "expires_at": None,
                "notes": "Test token",
            },
            # Second call: no duplicate
            None,
        ]

        result = validate_registration_token("TEST-TOKEN-50", "alice@example.com")

        assert result["token"] == "TEST-TOKEN-50"
        assert result["uses_remaining"] == 50
        assert result["group_id"] is None

    def test_validate_nonexistent_token(self, mock_get_db):
        """Test validation of nonexistent token."""
        mock_conn, mock_cursor = mock_get_db

        # Mock no token found
        mock_cursor.fetchone.return_value = None

        with pytest.raises(TokenNotFoundError) as exc_info:
            validate_registration_token("FAKE-TOKEN", "alice@example.com")

        assert "FAKE-TOKEN" in str(exc_info.value)

    def test_validate_exhausted_token(self, mock_get_db):
        """Test validation of exhausted token."""
        mock_conn, mock_cursor = mock_get_db

        # Mock exhausted token
        mock_cursor.fetchone.return_value = {
            "token": "EXHAUSTED-TOKEN",
            "group_id": None,
            "state": "exhausted",
            "max_uses": 5,
            "uses_remaining": 0,
            "expires_at": None,
            "notes": None,
        }

        with pytest.raises(TokenExhaustedError) as exc_info:
            validate_registration_token("EXHAUSTED-TOKEN", "alice@example.com")

        assert "fully used" in str(exc_info.value)

    def test_validate_expired_token(self, mock_get_db):
        """Test validation of expired token."""
        mock_conn, mock_cursor = mock_get_db

        yesterday = datetime.now(timezone.utc) - timedelta(days=1)

        # Mock expired token
        mock_cursor.fetchone.return_value = {
            "token": "EXPIRED-TOKEN",
            "group_id": None,
            "state": "active",
            "max_uses": 10,
            "uses_remaining": 10,
            "expires_at": yesterday,
            "notes": None,
        }

        with pytest.raises(TokenExpiredError) as exc_info:
            validate_registration_token("EXPIRED-TOKEN", "alice@example.com")

        assert "expired" in str(exc_info.value)

    def test_validate_revoked_token(self, mock_get_db):
        """Test validation of revoked token."""
        mock_conn, mock_cursor = mock_get_db

        # Mock revoked token
        mock_cursor.fetchone.return_value = {
            "token": "REVOKED-TOKEN",
            "group_id": None,
            "state": "revoked",
            "max_uses": 10,
            "uses_remaining": 10,
            "expires_at": None,
            "notes": None,
        }

        with pytest.raises(TokenRevokedError) as exc_info:
            validate_registration_token("REVOKED-TOKEN", "alice@example.com")

        assert "revoked" in str(exc_info.value)

    def test_duplicate_signup(self, mock_get_db):
        """Test duplicate signup prevention."""
        mock_conn, mock_cursor = mock_get_db

        # Mock valid token, then duplicate found
        mock_cursor.fetchone.side_effect = [
            # First call: valid token
            {
                "token": "DUP-TOKEN",
                "group_id": None,
                "state": "active",
                "max_uses": 10,
                "uses_remaining": 9,
                "expires_at": None,
                "notes": None,
            },
            # Second call: duplicate exists
            {"exists": 1},
        ]

        with pytest.raises(DuplicateSignupError) as exc_info:
            validate_registration_token("DUP-TOKEN", "alice@example.com")

        assert "alice@example.com" in str(exc_info.value)

    def test_validate_token_not_expired_yet(self, mock_get_db):
        """Test validation of token that expires in the future."""
        mock_conn, mock_cursor = mock_get_db

        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

        # Mock token expiring tomorrow
        mock_cursor.fetchone.side_effect = [
            {
                "token": "FUTURE-TOKEN",
                "group_id": None,
                "state": "active",
                "max_uses": 10,
                "uses_remaining": 10,
                "expires_at": tomorrow,
                "notes": None,
            },
            None,  # No duplicate
        ]

        result = validate_registration_token("FUTURE-TOKEN", "alice@example.com")
        assert result["token"] == "FUTURE-TOKEN"


# =============================================================================
# USAGE RECORDING TESTS
# =============================================================================


class TestRecordTokenUsage:
    """Test token usage recording."""

    def test_record_token_usage(self, mock_get_db):
        """Test recording token usage."""
        mock_conn, mock_cursor = mock_get_db

        record_token_usage("USAGE-TOKEN", "alice@example.com")

        # Verify INSERT was called
        calls = mock_cursor.execute.call_args_list
        assert len(calls) >= 2

        # First call should be INSERT into token_usage
        first_call = calls[0][0][0]
        assert "INSERT INTO token_usage" in first_call

        # Second call should be UPDATE registration_tokens
        second_call = calls[1][0][0]
        assert "UPDATE registration_tokens" in second_call

        # Verify commit was called
        mock_conn.commit.assert_called_once()


# =============================================================================
# STATS TESTS
# =============================================================================


class TestGetTokenStats:
    """Test token statistics retrieval."""

    def test_get_token_stats(self, mock_get_db):
        """Test getting token statistics."""
        mock_conn, mock_cursor = mock_get_db

        # Mock responses for three queries
        mock_cursor.fetchone.side_effect = [
            # Token info
            {
                "token": "STATS-TOKEN",
                "state": "active",
                "max_uses": 10,
                "uses_remaining": 7,
                "expires_at": None,
                "notes": "Test cohort",
            },
            # Used count
            {"used_count": 3},
        ]

        mock_cursor.fetchall.return_value = [
            {"user_id": "alice@example.com", "used_at": datetime.now(timezone.utc)},
            {"user_id": "bob@example.com", "used_at": datetime.now(timezone.utc)},
            {"user_id": "charlie@example.com", "used_at": datetime.now(timezone.utc)},
        ]

        stats = get_token_stats("STATS-TOKEN")

        assert stats["token"] == "STATS-TOKEN"
        assert stats["max_uses"] == 10
        assert stats["uses_remaining"] == 7
        assert stats["used_count"] == 3
        assert stats["notes"] == "Test cohort"
        assert len(stats["recent_signups"]) == 3

    def test_get_token_stats_not_found(self, mock_get_db):
        """Test getting stats for nonexistent token."""
        mock_conn, mock_cursor = mock_get_db

        mock_cursor.fetchone.return_value = None

        with pytest.raises(TokenNotFoundError):
            get_token_stats("NONEXISTENT")


# =============================================================================
# EDGE CASES
# =============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_token_with_zero_remaining(self, mock_get_db):
        """Test token with exactly zero uses remaining."""
        mock_conn, mock_cursor = mock_get_db

        mock_cursor.fetchone.return_value = {
            "token": "ZERO-TOKEN",
            "group_id": None,
            "state": "active",  # State might not be updated yet
            "max_uses": 5,
            "uses_remaining": 0,
            "expires_at": None,
            "notes": None,
        }

        with pytest.raises(TokenExhaustedError):
            validate_registration_token("ZERO-TOKEN", "alice@example.com")

    def test_token_with_group_id(self, mock_get_db):
        """Test token with group_id set (future feature)."""
        mock_conn, mock_cursor = mock_get_db

        mock_cursor.fetchone.side_effect = [
            {
                "token": "GROUP-TOKEN",
                "group_id": 123,
                "state": "active",
                "max_uses": 50,
                "uses_remaining": 50,
                "expires_at": None,
                "notes": "Group token",
            },
            None,
        ]

        result = validate_registration_token("GROUP-TOKEN", "alice@example.com")
        assert result["group_id"] == 123

    def test_expired_token_with_naive_datetime(self, mock_get_db):
        """Test handling of naive datetime from database."""
        mock_conn, mock_cursor = mock_get_db

        # Some databases return naive datetime
        yesterday = datetime.now() - timedelta(days=1)

        mock_cursor.fetchone.return_value = {
            "token": "NAIVE-EXPIRED",
            "group_id": None,
            "state": "active",
            "max_uses": 10,
            "uses_remaining": 10,
            "expires_at": yesterday,  # Naive datetime
            "notes": None,
        }

        with pytest.raises(TokenExpiredError):
            validate_registration_token("NAIVE-EXPIRED", "alice@example.com")
