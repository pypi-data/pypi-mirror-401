"""Tests for OAuth callback platform support (Slack + Matrix)."""

import pytest
from datetime import datetime, timezone, timedelta


class TestPlatformDetection:
    """Test user ID platform detection."""

    def test_detect_slack_user(self):
        """Slack user IDs start with U followed by alphanumerics."""
        from vikunja_mcp.server import _detect_user_platform

        assert _detect_user_platform("U12345ABC") == "slack"
        assert _detect_user_platform("UABCD1234") == "slack"

    def test_detect_matrix_user(self):
        """Matrix user IDs are @user:server format."""
        from vikunja_mcp.server import _detect_user_platform

        assert _detect_user_platform("@alice:matrix.org") == "matrix"
        assert _detect_user_platform("@i2:matrix.factumerit.app") == "matrix"
        assert _detect_user_platform("@eis:matrix.factumerit.app") == "matrix"

    def test_edge_cases(self):
        """Edge cases default to slack."""
        from vikunja_mcp.server import _detect_user_platform

        # @ without : is not Matrix format
        assert _detect_user_platform("@noserver") == "slack"
        # Empty string
        assert _detect_user_platform("") == "slack"


class TestPendingConnections:
    """Test pending connection management."""

    def test_create_pending_connection_slack(self):
        """Create pending connection for Slack user."""
        from vikunja_mcp.server import (
            _create_pending_connection,
            _get_pending_connection,
            _delete_pending_connection,
        )

        user_id = "U12345ABC"
        nonce = _create_pending_connection(user_id)

        # Should return a nonce
        assert nonce is not None
        assert len(nonce) > 20  # Token should be reasonably long

        # Retrieve pending connection
        pending = _get_pending_connection(nonce)
        assert pending is not None
        assert pending["user_id"] == user_id
        assert pending["platform"] == "slack"

        # Clean up
        _delete_pending_connection(nonce)

    def test_create_pending_connection_matrix(self):
        """Create pending connection for Matrix user."""
        from vikunja_mcp.server import (
            _create_pending_connection,
            _get_pending_connection,
            _delete_pending_connection,
        )

        user_id = "@alice:matrix.org"
        nonce = _create_pending_connection(user_id)

        # Should return a nonce
        assert nonce is not None

        # Retrieve pending connection
        pending = _get_pending_connection(nonce)
        assert pending is not None
        assert pending["user_id"] == user_id
        assert pending["platform"] == "matrix"

        # Clean up
        _delete_pending_connection(nonce)

    def test_explicit_platform_override(self):
        """Platform can be explicitly specified."""
        from vikunja_mcp.server import (
            _create_pending_connection,
            _get_pending_connection,
            _delete_pending_connection,
        )

        # Force matrix platform even for Slack-like user ID
        user_id = "U12345ABC"
        nonce = _create_pending_connection(user_id, platform="matrix")

        pending = _get_pending_connection(nonce)
        assert pending["platform"] == "matrix"

        # Clean up
        _delete_pending_connection(nonce)

    def test_get_nonexistent_connection(self):
        """Getting nonexistent connection returns None."""
        from vikunja_mcp.server import _get_pending_connection

        result = _get_pending_connection("nonexistent_nonce_12345")
        assert result is None

    def test_delete_pending_connection(self):
        """Deleting removes connection and returns True."""
        from vikunja_mcp.server import (
            _create_pending_connection,
            _get_pending_connection,
            _delete_pending_connection,
        )

        nonce = _create_pending_connection("U12345ABC")

        # Delete should return True
        assert _delete_pending_connection(nonce) is True

        # Should no longer exist
        assert _get_pending_connection(nonce) is None

        # Second delete should return False
        assert _delete_pending_connection(nonce) is False


class TestMatrixConnectPrompt:
    """Test Matrix connect prompt generation."""

    def test_manual_connect_prompt(self, monkeypatch):
        """Without OAuth enabled, shows manual instructions."""
        from vikunja_mcp.server import _get_matrix_connect_prompt

        # Ensure MATRIX_OAUTH_ENABLED is not set
        monkeypatch.delenv("MATRIX_OAUTH_ENABLED", raising=False)

        user_id = "@alice:matrix.org"
        prompt = _get_matrix_connect_prompt(user_id)

        # Should contain manual instructions
        assert "!vik" in prompt
        assert "API Tokens" in prompt
        assert "OAuth is coming soon" in prompt

    def test_oauth_connect_prompt(self, monkeypatch):
        """With OAuth enabled, shows OAuth link."""
        from vikunja_mcp.server import _get_matrix_connect_prompt

        monkeypatch.setenv("MATRIX_OAUTH_ENABLED", "true")
        monkeypatch.setenv("VIKUNJA_URL", "https://vikunja.example.com")

        user_id = "@alice:matrix.org"
        prompt = _get_matrix_connect_prompt(user_id)

        # Should contain OAuth link
        assert "matrix-connect" in prompt
        assert "Click here to connect" in prompt


class TestCallbackSuccessHtml:
    """Test success HTML generation."""

    def test_slack_success_page(self):
        """Slack success page mentions Slack."""
        from vikunja_mcp.server import _callback_success_html

        html = _callback_success_html("slack")
        assert "Slack bot" in html
        assert "return to Slack" in html

    def test_matrix_success_page(self):
        """Matrix success page mentions eis bot and Element."""
        from vikunja_mcp.server import _callback_success_html

        html = _callback_success_html("matrix")
        assert "eis bot" in html
        assert "return to Element" in html

    def test_default_is_slack(self):
        """Default platform is Slack."""
        from vikunja_mcp.server import _callback_success_html

        html = _callback_success_html()
        assert "Slack bot" in html


class TestMatrixHandlerConnect:
    """Test Matrix handler connect command."""

    def test_connect_no_args_shows_prompt(self, monkeypatch):
        """!vik with no args shows connect prompt."""
        from vikunja_mcp.matrix_handlers import _handle_connect

        monkeypatch.delenv("MATRIX_OAUTH_ENABLED", raising=False)

        result = _handle_connect("", "@alice:matrix.org")

        assert result["success"] is True
        assert "API Tokens" in result["response"]  # Manual flow

    def test_connect_single_arg_invalid_token(self):
        """!vik with invalid token format shows error."""
        from vikunja_mcp.matrix_handlers import _handle_connect

        result = _handle_connect("invalid_token", "@alice:matrix.org")

        assert result["success"] is False
        assert "Invalid token format" in result["response"]
        assert "tk_" in result["response"]


class TestFirstContactTracking:
    """Test first contact detection for Matrix onboarding."""

    def test_new_user_is_first_contact(self):
        """User with no config is first contact."""
        from vikunja_mcp.server import _is_first_contact, _load_config, _save_config

        # Use a unique user ID for this test
        test_user = "@test_new_user_12345:matrix.org"

        # Ensure user doesn't exist
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)

        assert _is_first_contact(test_user) is True

    def test_welcomed_user_is_not_first_contact(self):
        """User marked as welcomed is not first contact."""
        from vikunja_mcp.server import (
            _is_first_contact,
            _mark_user_welcomed,
            _load_config,
            _save_config,
        )

        test_user = "@test_welcomed_user_12345:matrix.org"

        # Mark user as welcomed
        _mark_user_welcomed(test_user)

        # Should no longer be first contact
        assert _is_first_contact(test_user) is False

        # Clean up
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)

    def test_user_with_token_but_not_welcomed(self):
        """User with token but no welcomed flag is first contact."""
        from vikunja_mcp.server import (
            _is_first_contact,
            _set_user_vikunja_token,
            _load_config,
            _save_config,
        )

        test_user = "@test_token_no_welcome_12345:matrix.org"

        # Set token but don't mark welcomed
        _set_user_vikunja_token(test_user, "tk_test_token")

        # Should still be first contact (has token but not welcomed)
        assert _is_first_contact(test_user) is True

        # Clean up
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)


class TestMatrixOnboardingFlow:
    """Test Matrix onboarding DM flow."""

    def test_first_dm_sends_welcome(self, monkeypatch):
        """First DM from new user sends welcome message."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        from vikunja_mcp.server import _load_config, _save_config

        monkeypatch.delenv("MATRIX_OAUTH_ENABLED", raising=False)

        test_user = "@test_first_dm_12345:matrix.org"

        # Ensure user doesn't exist
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)

        # First DM should trigger welcome
        result = handle_matrix_message("hello", test_user, is_dm=True)

        assert result["success"] is True
        assert result.get("is_welcome") is True
        assert "Welcome to Factum Erit" in result["response"]
        assert "eis" in result["response"]

        # Clean up
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)

    def test_second_dm_does_not_send_welcome(self, monkeypatch):
        """Second DM from user does not send welcome again."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        from vikunja_mcp.server import _load_config, _save_config, _mark_user_welcomed

        monkeypatch.delenv("MATRIX_OAUTH_ENABLED", raising=False)

        test_user = "@test_second_dm_12345:matrix.org"

        # Mark user as already welcomed
        _mark_user_welcomed(test_user)

        # Second DM should not trigger welcome
        result = handle_matrix_message("hello", test_user, is_dm=True)

        # Should NOT be a welcome message
        assert result.get("is_welcome") is not True

        # Clean up
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)

    def test_room_message_does_not_trigger_welcome(self, monkeypatch):
        """Message in room (not DM) does not trigger welcome."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        from vikunja_mcp.server import _load_config, _save_config

        monkeypatch.delenv("MATRIX_OAUTH_ENABLED", raising=False)

        test_user = "@test_room_msg_12345:matrix.org"

        # Ensure user doesn't exist
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)

        # Room message (is_dm=False) should not trigger welcome
        result = handle_matrix_message("hello", test_user, is_dm=False)

        # Should NOT be a welcome message
        assert result.get("is_welcome") is not True

        # Clean up (user shouldn't have been marked welcomed)
        config = _load_config()
        if test_user in config.get("users", {}):
            del config["users"][test_user]
            _save_config(config)
