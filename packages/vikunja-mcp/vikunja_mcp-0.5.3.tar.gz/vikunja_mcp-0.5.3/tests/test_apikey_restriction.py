"""Test !apikey restriction on shared servers.

Security requirement: !apikey should only work on isolated instances
to prevent prompt injection attacks where user A steals user B's API key.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from vikunja_mcp.matrix_handlers import _handle_apikey


class TestApikeyRestriction:
    """Test !apikey command restriction based on ISOLATED_INSTANCE env var."""

    def test_apikey_blocked_on_shared_server(self):
        """!apikey should be blocked when ISOLATED_INSTANCE is not set."""
        with patch.dict(os.environ, {}, clear=False):
            # Remove ISOLATED_INSTANCE if it exists
            os.environ.pop("ISOLATED_INSTANCE", None)
            
            result = _handle_apikey("sk-ant-test123", "@user:matrix.org")
            
            assert result["success"] is False
            assert "API Key Management Disabled" in result["response"]
            assert "isolated bot instances" in result["response"]
            assert "prompt injection" in result["response"]

    def test_apikey_blocked_when_isolated_false(self):
        """!apikey should be blocked when ISOLATED_INSTANCE=false."""
        with patch.dict(os.environ, {"ISOLATED_INSTANCE": "false"}):
            result = _handle_apikey("sk-ant-test123", "@user:matrix.org")
            
            assert result["success"] is False
            assert "API Key Management Disabled" in result["response"]

    def test_apikey_blocked_when_isolated_0(self):
        """!apikey should be blocked when ISOLATED_INSTANCE=0."""
        with patch.dict(os.environ, {"ISOLATED_INSTANCE": "0"}):
            result = _handle_apikey("sk-ant-test123", "@user:matrix.org")
            
            assert result["success"] is False
            assert "API Key Management Disabled" in result["response"]

    @patch("vikunja_mcp.server._get_user_anthropic_api_key")
    def test_apikey_allowed_when_isolated_true(self, mock_get_key):
        """!apikey should work when ISOLATED_INSTANCE=true."""
        mock_get_key.return_value = None

        with patch.dict(os.environ, {"ISOLATED_INSTANCE": "true"}):
            result = _handle_apikey("", "@user:matrix.org")

            # Should show status, not block
            assert result["success"] is True
            assert "API Key Status" in result["response"]
            assert "API Key Management Disabled" not in result["response"]

    @patch("vikunja_mcp.server._get_user_anthropic_api_key")
    def test_apikey_allowed_when_isolated_1(self, mock_get_key):
        """!apikey should work when ISOLATED_INSTANCE=1."""
        mock_get_key.return_value = None

        with patch.dict(os.environ, {"ISOLATED_INSTANCE": "1"}):
            result = _handle_apikey("", "@user:matrix.org")

            # Should show status, not block
            assert result["success"] is True
            assert "API Key Status" in result["response"]

    @patch("vikunja_mcp.server._get_user_anthropic_api_key")
    def test_apikey_allowed_when_isolated_yes(self, mock_get_key):
        """!apikey should work when ISOLATED_INSTANCE=yes."""
        mock_get_key.return_value = None

        with patch.dict(os.environ, {"ISOLATED_INSTANCE": "yes"}):
            result = _handle_apikey("", "@user:matrix.org")

            # Should show status, not block
            assert result["success"] is True
            assert "API Key Status" in result["response"]

    def test_apikey_status_check_blocked(self):
        """!apikey with no args (status check) should also be blocked."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ISOLATED_INSTANCE", None)
            
            result = _handle_apikey("", "@user:matrix.org")
            
            assert result["success"] is False
            assert "API Key Management Disabled" in result["response"]

    def test_apikey_clear_blocked(self):
        """!apikey clear should be blocked on shared servers."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ISOLATED_INSTANCE", None)
            
            result = _handle_apikey("clear", "@user:matrix.org")
            
            assert result["success"] is False
            assert "API Key Management Disabled" in result["response"]

    def test_error_message_explains_security_risk(self):
        """Error message should explain the security risk clearly."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ISOLATED_INSTANCE", None)
            
            result = _handle_apikey("sk-ant-test", "@user:matrix.org")
            
            # Check that error message is helpful
            assert "prompt injection" in result["response"]
            assert "isolated" in result["response"]
            assert "Options:" in result["response"]
            assert "free tier" in result["response"]

    @patch("vikunja_mcp.server._get_user_anthropic_api_key")
    @patch("vikunja_mcp.server._set_user_anthropic_api_key")
    def test_apikey_set_works_on_isolated(self, mock_set_key, mock_get_key):
        """Setting API key should work on isolated instances."""
        mock_get_key.return_value = None

        with patch.dict(os.environ, {"ISOLATED_INSTANCE": "true"}):
            result = _handle_apikey("sk-ant-api03-" + "x" * 50, "@user:matrix.org")

            # Should succeed
            assert result["success"] is True
            assert "validated and saved" in result["response"]
            mock_set_key.assert_called_once()

