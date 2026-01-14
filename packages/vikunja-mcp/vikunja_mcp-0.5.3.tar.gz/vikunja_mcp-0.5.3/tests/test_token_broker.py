"""
Unit tests for Token Broker module.

These tests use mocking to avoid database dependencies.
For integration tests, see tests/integration/test_token_broker_integration.py
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

# Import the module under test
from vikunja_mcp import token_broker
from vikunja_mcp.token_broker import (
    AuthRequired,
    TokenBrokerUnavailable,
    get_user_token,
    set_user_token,
    revoke_user_token,
    has_user_token,
    encrypt_token,
    decrypt_token,
    _invalidate_cache,
    _set_cached_token,
    _get_cached_token,
    get_user_active_instance,
    set_user_active_instance,
    get_user_active_project,
    set_user_active_project,
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def mock_db():
    """Mock database execute function."""
    with patch.object(token_broker, "execute") as mock:
        yield mock


@pytest.fixture
def mock_fernet():
    """Mock encryption functions."""
    with patch.object(token_broker, "encrypt_token") as mock_encrypt, patch.object(
        token_broker, "decrypt_token"
    ) as mock_decrypt:
        mock_encrypt.return_value = b"encrypted_token_bytes"
        mock_decrypt.return_value = "decrypted_token_value"
        yield mock_encrypt, mock_decrypt


@pytest.fixture
def clear_cache():
    """Clear token cache before each test."""
    token_broker._token_cache.clear()
    yield
    token_broker._token_cache.clear()


# =============================================================================
# ENCRYPTION TESTS
# =============================================================================


class TestEncryption:
    """Test encryption/decryption functions."""

    def test_encrypt_decrypt_roundtrip(self):
        """Encrypted token can be decrypted to original value."""
        # Skip if no encryption key configured
        if not token_broker.ENCRYPTION_KEY:
            pytest.skip("TOKEN_ENCRYPTION_KEY not configured")

        original = "tk_test_token_12345"
        encrypted = encrypt_token(original)
        decrypted = decrypt_token(encrypted)

        assert decrypted == original
        assert encrypted != original.encode()  # Should be different

    def test_encryption_is_deterministic_per_call(self):
        """Each encryption produces different ciphertext (Fernet uses random IV)."""
        if not token_broker.ENCRYPTION_KEY:
            pytest.skip("TOKEN_ENCRYPTION_KEY not configured")

        original = "tk_test_token"
        encrypted1 = encrypt_token(original)
        encrypted2 = encrypt_token(original)

        # Fernet uses random IV, so same plaintext → different ciphertext
        assert encrypted1 != encrypted2


# =============================================================================
# CACHING TESTS
# =============================================================================


class TestCaching:
    """Test in-memory token cache."""

    def test_cache_hit(self, clear_cache):
        """Cached token is returned without DB query."""
        user_id = "@test:matrix.factumerit.app"
        instance = "default"
        token = "cached_token"

        _set_cached_token(user_id, instance, token)
        cached = _get_cached_token(user_id, instance)

        assert cached == token

    def test_cache_miss(self, clear_cache):
        """Missing cache entry returns None."""
        cached = _get_cached_token("@unknown:matrix.factumerit.app", "default")
        assert cached is None

    def test_cache_expiry(self, clear_cache):
        """Expired cache entries are removed."""
        user_id = "@test:matrix.factumerit.app"
        instance = "default"
        token = "expired_token"

        # Set cache with expired time
        key = (user_id, instance)
        token_broker._token_cache[key] = (token, datetime.now(timezone.utc) - timedelta(seconds=1))

        cached = _get_cached_token(user_id, instance)
        assert cached is None
        assert key not in token_broker._token_cache

    def test_cache_invalidation(self, clear_cache):
        """Cache invalidation removes entry."""
        user_id = "@test:matrix.factumerit.app"
        instance = "default"

        _set_cached_token(user_id, instance, "token")
        assert _get_cached_token(user_id, instance) is not None

        _invalidate_cache(user_id, instance)
        assert _get_cached_token(user_id, instance) is None


# =============================================================================
# GET_USER_TOKEN TESTS
# =============================================================================


class TestGetUserToken:
    """Test get_user_token function."""

    def test_get_token_success(self, mock_db, clear_cache):
        """Successfully retrieves and decrypts token."""
        user_id = "@alice:matrix.factumerit.app"
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)

        # Mock DB to return valid token
        mock_db.return_value = [(b"encrypted_token", False, expires_at)]

        with patch.object(token_broker, "decrypt_token", return_value="tk_alice_token"):
            token = get_user_token(
                user_id, purpose="test", caller="test_token_broker.test_get_token_success"
            )

        assert token == "tk_alice_token"

    def test_get_token_not_found_raises_auth_required(self, mock_db, clear_cache):
        """Missing token raises AuthRequired."""
        mock_db.return_value = []  # No rows

        with pytest.raises(AuthRequired) as exc_info:
            get_user_token(
                "@unknown:matrix.factumerit.app",
                purpose="test",
                caller="test_token_broker.test_not_found",
            )

        assert "No token" in str(exc_info.value)
        assert exc_info.value.refresh_url is None

    def test_get_token_revoked_raises_auth_required(self, mock_db, clear_cache):
        """Revoked token raises AuthRequired."""
        mock_db.return_value = [(b"encrypted", True, datetime.now(timezone.utc) + timedelta(days=30))]

        with pytest.raises(AuthRequired) as exc_info:
            get_user_token(
                "@revoked:matrix.factumerit.app",
                purpose="test",
                caller="test_token_broker.test_revoked",
            )

        assert "revoked" in str(exc_info.value).lower()

    def test_get_token_expired_raises_auth_required_with_refresh_url(self, mock_db, clear_cache):
        """Expired token raises AuthRequired with refresh_url."""
        expired = datetime.now(timezone.utc) - timedelta(days=1)
        mock_db.return_value = [(b"encrypted", False, expired)]

        with pytest.raises(AuthRequired) as exc_info:
            get_user_token(
                "@expired:matrix.factumerit.app",
                purpose="test",
                caller="test_token_broker.test_expired",
            )

        assert "expired" in str(exc_info.value).lower()
        assert exc_info.value.refresh_url is not None
        assert "factumerit" in exc_info.value.refresh_url

    def test_get_token_uses_cache(self, mock_db, clear_cache):
        """Second call uses cache, not DB."""
        user_id = "@cached:matrix.factumerit.app"
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)

        mock_db.return_value = [(b"encrypted", False, expires_at)]

        with patch.object(token_broker, "decrypt_token", return_value="tk_cached"):
            # First call hits DB
            token1 = get_user_token(user_id, purpose="test1", caller="test1")
            call_count_after_first = mock_db.call_count

            # Second call should use cache
            token2 = get_user_token(user_id, purpose="test2", caller="test2")
            call_count_after_second = mock_db.call_count

        assert token1 == token2 == "tk_cached"
        # DB should only be called for first request (SELECT + UPDATE)
        assert call_count_after_second == call_count_after_first


# =============================================================================
# SET_USER_TOKEN TESTS
# =============================================================================


class TestSetUserToken:
    """Test set_user_token function."""

    def test_set_token_encrypts_and_stores(self, mock_db, clear_cache):
        """Token is encrypted before storage."""
        user_id = "@new:matrix.factumerit.app"
        token = "tk_new_token"
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)

        with patch.object(token_broker, "encrypt_token", return_value=b"encrypted") as mock_enc:
            set_user_token(
                user_id,
                token,
                source="test",
                expires_at=expires_at,
                caller="test_set_token",
            )

            mock_enc.assert_called_once_with(token)

        # Verify INSERT was called
        assert mock_db.call_count >= 1
        insert_call = mock_db.call_args_list[0]
        assert "INSERT INTO user_tokens" in insert_call[0][0]

    def test_set_token_invalidates_cache(self, mock_db, clear_cache):
        """Setting new token invalidates cache."""
        user_id = "@update:matrix.factumerit.app"
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)

        # Pre-populate cache
        _set_cached_token(user_id, "default", "old_token")
        assert _get_cached_token(user_id, "default") == "old_token"

        with patch.object(token_broker, "encrypt_token", return_value=b"encrypted"):
            set_user_token(
                user_id,
                "new_token",
                source="test",
                expires_at=expires_at,
                caller="test_set_token",
            )

        # Cache should be invalidated
        assert _get_cached_token(user_id, "default") is None


# =============================================================================
# REVOKE_USER_TOKEN TESTS
# =============================================================================


class TestRevokeUserToken:
    """Test revoke_user_token function."""

    def test_revoke_existing_token(self, mock_db, clear_cache):
        """Revoking existing token returns True."""
        mock_db.return_value = [("@user:matrix.factumerit.app",)]  # RETURNING user_id

        result = revoke_user_token(
            "@user:matrix.factumerit.app",
            reason="user requested",
            caller="test_revoke",
        )

        assert result is True

    def test_revoke_nonexistent_token(self, mock_db, clear_cache):
        """Revoking nonexistent token returns False."""
        mock_db.return_value = []  # No rows updated

        result = revoke_user_token(
            "@unknown:matrix.factumerit.app",
            reason="test",
            caller="test_revoke",
        )

        assert result is False

    def test_revoke_invalidates_cache(self, mock_db, clear_cache):
        """Revoking token invalidates cache."""
        user_id = "@revoke:matrix.factumerit.app"
        mock_db.return_value = [(user_id,)]

        # Pre-populate cache
        _set_cached_token(user_id, "default", "token_to_revoke")

        revoke_user_token(user_id, reason="test", caller="test_revoke")

        assert _get_cached_token(user_id, "default") is None


# =============================================================================
# HAS_USER_TOKEN TESTS
# =============================================================================


class TestHasUserToken:
    """Test has_user_token function."""

    def test_has_token_true(self, mock_db, clear_cache):
        """Returns True when token exists."""
        mock_db.return_value = [(1,)]  # SELECT 1 returns a row

        assert has_user_token("@exists:matrix.factumerit.app") is True

    def test_has_token_false(self, mock_db, clear_cache):
        """Returns False when no token."""
        mock_db.return_value = []

        assert has_user_token("@missing:matrix.factumerit.app") is False

    def test_has_token_uses_cache(self, clear_cache):
        """Uses cache before DB query."""
        user_id = "@cached:matrix.factumerit.app"
        _set_cached_token(user_id, "default", "token")

        # Should return True from cache without DB
        with patch.object(token_broker, "execute") as mock_db:
            result = has_user_token(user_id)
            mock_db.assert_not_called()

        assert result is True

    def test_has_token_fails_open(self, mock_db, clear_cache):
        """Returns False on database error (fail open for UX)."""
        mock_db.side_effect = Exception("DB error")

        # Should return False, not raise
        assert has_user_token("@error:matrix.factumerit.app") is False


# =============================================================================
# AUDIT LOGGING TESTS
# =============================================================================


class TestAuditLogging:
    """Test audit log functionality."""

    def test_get_token_logs_success(self, mock_db, clear_cache):
        """Successful get_user_token logs access."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)
        mock_db.return_value = [(b"encrypted", False, expires_at)]

        with patch.object(token_broker, "decrypt_token", return_value="token"):
            get_user_token("@user:matrix.factumerit.app", purpose="!stats", caller="handlers.stats")

        # Find the INSERT INTO token_access_log call
        log_calls = [
            call for call in mock_db.call_args_list if "token_access_log" in str(call[0][0])
        ]
        assert len(log_calls) >= 1

    def test_get_token_logs_failure(self, mock_db, clear_cache):
        """Failed get_user_token logs error."""
        mock_db.return_value = []  # No token found

        with pytest.raises(AuthRequired):
            get_user_token("@missing:matrix.factumerit.app", purpose="test", caller="test")

        # Should log the failure
        log_calls = [
            call for call in mock_db.call_args_list if "token_access_log" in str(call[0][0])
        ]
        assert len(log_calls) >= 1


# =============================================================================
# MULTI-INSTANCE TESTS
# =============================================================================


class TestMultiInstance:
    """Test multi-instance support."""

    def test_different_instances_isolated(self, mock_db, clear_cache):
        """Tokens for different instances are isolated."""
        user_id = "@multi:matrix.factumerit.app"
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)

        # Set up mock to return different tokens for different instances
        def mock_execute(query, params):
            if "SELECT" in query and params:
                if params[1] == "default":
                    return [(b"encrypted_default", False, expires_at)]
                elif params[1] == "work":
                    return [(b"encrypted_work", False, expires_at)]
            return []

        mock_db.side_effect = mock_execute

        with patch.object(token_broker, "decrypt_token") as mock_decrypt:
            mock_decrypt.side_effect = lambda x: (
                "token_default" if x == b"encrypted_default" else "token_work"
            )

            token_default = get_user_token(
                user_id, purpose="test", instance="default", caller="test"
            )
            token_work = get_user_token(user_id, purpose="test", instance="work", caller="test")

        assert token_default == "token_default"
        assert token_work == "token_work"

    def test_cache_keys_include_instance(self, clear_cache):
        """Cache separates tokens by instance."""
        user_id = "@user:matrix.factumerit.app"

        _set_cached_token(user_id, "default", "token_default")
        _set_cached_token(user_id, "work", "token_work")

        assert _get_cached_token(user_id, "default") == "token_default"
        assert _get_cached_token(user_id, "work") == "token_work"

        _invalidate_cache(user_id, "default")
        assert _get_cached_token(user_id, "default") is None
        assert _get_cached_token(user_id, "work") == "token_work"  # Still cached



# =============================================================================
# USER PREFERENCES TESTS
# =============================================================================


class TestUserPreferences:
    """Test user preference functions (active instance, active project)."""

    @patch.object(token_broker, "get_db")
    def test_get_user_active_instance_exists(self, mock_get_db):
        """Get active instance when user has one set."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("personal",)
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = get_user_active_instance("@user:matrix.org")

        assert result == "personal"
        mock_cursor.execute.assert_called_once()

    @patch.object(token_broker, "get_db")
    def test_get_user_active_instance_not_set(self, mock_get_db):
        """Get active instance when user has no preference."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = get_user_active_instance("@user:matrix.org")

        assert result is None

    @patch.object(token_broker, "get_db")
    def test_set_user_active_instance(self, mock_get_db):
        """Set active instance for user."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        set_user_active_instance("@user:matrix.org", "work")

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch.object(token_broker, "get_db")
    def test_get_user_active_project_exists(self, mock_get_db):
        """Get active project when user has one set."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (123, "My Project")
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = get_user_active_project("@user:matrix.org")

        assert result == {"id": 123, "name": "My Project"}
        mock_cursor.execute.assert_called_once()

    @patch.object(token_broker, "get_db")
    def test_get_user_active_project_not_set(self, mock_get_db):
        """Get active project when user has no preference."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = get_user_active_project("@user:matrix.org")

        assert result is None

    @patch.object(token_broker, "get_db")
    def test_get_user_active_project_id_null(self, mock_get_db):
        """Get active project when project_id is NULL."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (None, None)
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = get_user_active_project("@user:matrix.org")

        assert result is None

    @patch.object(token_broker, "get_db")
    def test_set_user_active_project(self, mock_get_db):
        """Set active project for user."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        set_user_active_project("@user:matrix.org", 456, "Work Project")

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch.object(token_broker, "get_db")
    def test_clear_user_active_project(self, mock_get_db):
        """Clear active project for user."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        set_user_active_project("@user:matrix.org", None)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()


# =============================================================================
# WORKSPACE / MULTI-ACCOUNT TESTS
# =============================================================================


class TestCanonicalEmail:
    """Test get_canonical_email function."""

    def test_strips_plus_alias(self):
        """Strips +alias from email."""
        from vikunja_mcp.token_broker import get_canonical_email

        assert get_canonical_email("ivan+work@gmail.com") == "ivan@gmail.com"
        assert get_canonical_email("ivan+personal@gmail.com") == "ivan@gmail.com"
        assert get_canonical_email("user+tag+nested@example.com") == "user@example.com"

    def test_preserves_email_without_alias(self):
        """Preserves email without +alias."""
        from vikunja_mcp.token_broker import get_canonical_email

        assert get_canonical_email("ivan@gmail.com") == "ivan@gmail.com"
        assert get_canonical_email("test@example.org") == "test@example.org"

    def test_handles_none_and_empty(self):
        """Handles None and empty strings."""
        from vikunja_mcp.token_broker import get_canonical_email

        assert get_canonical_email(None) is None
        assert get_canonical_email("") == ""

    def test_handles_invalid_email(self):
        """Handles emails without @ symbol."""
        from vikunja_mcp.token_broker import get_canonical_email

        assert get_canonical_email("notanemail") == "notanemail"


class TestGetUserWorkspaces:
    """Test get_user_workspaces function."""

    @patch.object(token_broker, "execute")
    def test_returns_workspaces(self, mock_execute):
        """Returns list of workspaces for identity."""
        from vikunja_mcp.token_broker import get_user_workspaces
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        mock_execute.return_value = [
            ("vikunja:ivan-business", "Business", True, "ivan@gmail.com", now),
            ("vikunja:ivan-personal", "Personal", False, "ivan+personal@gmail.com", now),
        ]

        result = get_user_workspaces("ivan@gmail.com")

        assert len(result) == 2
        assert result[0]["user_id"] == "vikunja:ivan-business"
        assert result[0]["is_primary"] is True
        assert result[1]["workspace_name"] == "Personal"

    @patch.object(token_broker, "execute")
    def test_returns_empty_for_unknown_identity(self, mock_execute):
        """Returns empty list for unknown identity."""
        from vikunja_mcp.token_broker import get_user_workspaces

        mock_execute.return_value = []

        result = get_user_workspaces("unknown@example.com")

        assert result == []

    @patch.object(token_broker, "execute")
    def test_handles_null_workspace_name(self, mock_execute):
        """Handles null workspace_name gracefully."""
        from vikunja_mcp.token_broker import get_user_workspaces
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        mock_execute.return_value = [
            ("vikunja:ivan", None, True, "ivan@gmail.com", now),
        ]

        result = get_user_workspaces("ivan@gmail.com")

        assert result[0]["workspace_name"] == "Default"


class TestLinkWorkspace:
    """Test link_workspace function."""

    @patch.object(token_broker, "get_db")
    def test_links_workspace(self, mock_get_db):
        """Links workspace to identity."""
        from vikunja_mcp.token_broker import link_workspace

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = link_workspace(
            "ivan@gmail.com",
            "vikunja:ivan-personal",
            "Personal",
            is_primary=False
        )

        assert result is True
        assert mock_conn.commit.called  # May be called multiple times due to _ensure_users_table

    @patch.object(token_broker, "get_db")
    def test_link_primary_clears_others(self, mock_get_db):
        """Linking as primary clears other primaries."""
        from vikunja_mcp.token_broker import link_workspace

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        link_workspace(
            "ivan@gmail.com",
            "vikunja:ivan-new",
            "New Primary",
            is_primary=True
        )

        # Should have two execute calls: one to clear primaries, one to update
        assert mock_cursor.execute.call_count == 2

    @patch.object(token_broker, "get_db")
    def test_link_nonexistent_user(self, mock_get_db):
        """Returns False for nonexistent user."""
        from vikunja_mcp.token_broker import link_workspace

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # No rows updated
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = link_workspace(
            "ivan@gmail.com",
            "vikunja:nonexistent",
            "Test"
        )

        assert result is False


class TestSetPrimaryWorkspace:
    """Test set_primary_workspace function."""

    @patch.object(token_broker, "get_db")
    def test_sets_primary(self, mock_get_db):
        """Sets workspace as primary."""
        from vikunja_mcp.token_broker import set_primary_workspace

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = set_primary_workspace("ivan@gmail.com", "vikunja:ivan-business")

        assert result is True
        # Should have two execute calls: clear old primary, set new
        assert mock_cursor.execute.call_count == 2

    @patch.object(token_broker, "get_db")
    def test_set_primary_unlinked_user(self, mock_get_db):
        """Returns False if user not linked to identity."""
        from vikunja_mcp.token_broker import set_primary_workspace

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # No rows updated
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        result = set_primary_workspace("ivan@gmail.com", "vikunja:other-user")

        assert result is False


class TestRegisterUserWithWorkspace:
    """Test register_user with workspace parameters."""

    @patch.object(token_broker, "get_db")
    @patch.object(token_broker, "get_user_workspaces")
    def test_first_account_becomes_primary(self, mock_get_workspaces, mock_get_db):
        """First account for identity becomes primary."""
        from vikunja_mcp.token_broker import register_user

        mock_get_workspaces.return_value = []  # No existing workspaces
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        register_user(
            "vikunja:newuser",
            email="newuser@gmail.com",
            workspace_name="First Workspace"
        )

        # Check that is_primary=True was passed (7th parameter in INSERT)
        call_args = mock_cursor.execute.call_args[0]
        insert_values = call_args[1]
        assert insert_values[5] is True  # is_primary

    @patch.object(token_broker, "get_db")
    @patch.object(token_broker, "get_user_workspaces")
    def test_subsequent_account_not_primary(self, mock_get_workspaces, mock_get_db):
        """Subsequent accounts are not primary by default."""
        from vikunja_mcp.token_broker import register_user
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        mock_get_workspaces.return_value = [
            {"user_id": "vikunja:existing", "is_primary": True, "workspace_name": "Main", "email": None, "registered_at": now.isoformat()}
        ]
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        register_user(
            "vikunja:second",
            email="user@gmail.com",
            workspace_name="Second Workspace"
        )

        call_args = mock_cursor.execute.call_args[0]
        insert_values = call_args[1]
        assert insert_values[5] is False  # is_primary

    @patch.object(token_broker, "get_db")
    @patch.object(token_broker, "get_user_workspaces")
    def test_explicit_primary_overrides(self, mock_get_workspaces, mock_get_db):
        """Explicit is_primary=True overrides default."""
        from vikunja_mcp.token_broker import register_user
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        mock_get_workspaces.return_value = [
            {"user_id": "vikunja:existing", "is_primary": True, "workspace_name": "Main", "email": None, "registered_at": now.isoformat()}
        ]
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value.__enter__.return_value = mock_conn

        register_user(
            "vikunja:force-primary",
            email="user@gmail.com",
            is_primary=True  # Explicit override
        )

        call_args = mock_cursor.execute.call_args[0]
        insert_values = call_args[1]
        assert insert_values[5] is True  # is_primary
