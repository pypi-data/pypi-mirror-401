"""
Unit tests for VikunjaClient module.

Tests the HTTP client for Vikunja API with focus on
multi-instance token retrieval.

Bead: solutions-lt0f (regression test for token lookup bug)
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import importlib.util

# Load modules directly, bypassing vikunja_mcp package __init__.py
src_path = Path(__file__).parent.parent / "src"

# Mock token_broker before importing
mock_token_broker = MagicMock()
mock_token_broker.get_user_token = MagicMock(return_value="test_token_123")
mock_token_broker.get_user_instance_url = MagicMock(return_value="https://vikunja.test")
mock_token_broker.get_user_active_instance = MagicMock(return_value="personal")
mock_token_broker.AuthRequired = Exception
sys.modules['vikunja_mcp.token_broker'] = mock_token_broker

# Load vikunja_client module
client_path = src_path / "vikunja_mcp" / "vikunja_client.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.vikunja_client", client_path)
vikunja_client = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.vikunja_client'] = vikunja_client
spec.loader.exec_module(vikunja_client)

VikunjaClient = vikunja_client.VikunjaClient


class TestVikunjaClientTokenRetrieval:
    """Tests for token retrieval with correct instance parameter."""

    def test_get_token_passes_instance_correctly(self):
        """CRITICAL: get_user_token must receive instance as named parameter.

        This test catches the bug where instance was passed as 'purpose'
        parameter due to positional argument mismatch.
        """
        # Reset mock to track calls
        mock_token_broker.get_user_token.reset_mock()

        # Create client for non-default instance
        client = VikunjaClient(
            user_id="@test:matrix.example.com",
            instance="business"  # NOT "default"
        )

        # Trigger token retrieval
        client._get_token()

        # Verify get_user_token was called with correct named parameters
        mock_token_broker.get_user_token.assert_called_once()
        call_kwargs = mock_token_broker.get_user_token.call_args

        # The instance parameter MUST be "business", not "default"
        # Before the fix, instance would be passed as purpose (positional)
        # and instance would default to "default"
        assert call_kwargs.kwargs.get("instance") == "business", \
            f"Instance should be 'business', got {call_kwargs}"

    def test_get_token_for_personal_instance(self):
        """Token retrieval works for 'personal' instance."""
        mock_token_broker.get_user_token.reset_mock()

        client = VikunjaClient(
            user_id="@test:matrix.example.com",
            instance="personal"
        )
        client._get_token()

        call_kwargs = mock_token_broker.get_user_token.call_args
        assert call_kwargs.kwargs.get("instance") == "personal"

    def test_get_token_for_default_instance(self):
        """Token retrieval works for 'default' instance."""
        mock_token_broker.get_user_token.reset_mock()

        client = VikunjaClient(
            user_id="@test:matrix.example.com",
            instance="default"
        )
        client._get_token()

        call_kwargs = mock_token_broker.get_user_token.call_args
        assert call_kwargs.kwargs.get("instance") == "default"

    def test_get_token_includes_purpose(self):
        """Token retrieval includes purpose for audit logging."""
        mock_token_broker.get_user_token.reset_mock()

        client = VikunjaClient(
            user_id="@test:matrix.example.com",
            instance="work"
        )
        client._get_token()

        call_kwargs = mock_token_broker.get_user_token.call_args
        assert "purpose" in call_kwargs.kwargs
        assert call_kwargs.kwargs["purpose"] == "vikunja_api_call"

    def test_get_token_includes_caller(self):
        """Token retrieval includes caller for audit logging."""
        mock_token_broker.get_user_token.reset_mock()

        client = VikunjaClient(
            user_id="@test:matrix.example.com",
            instance="work"
        )
        client._get_token()

        call_kwargs = mock_token_broker.get_user_token.call_args
        assert "caller" in call_kwargs.kwargs


class TestVikunjaClientMultiInstance:
    """Tests for multi-instance scenarios."""

    def test_different_instances_use_different_tokens(self):
        """Each instance should request its own token."""
        mock_token_broker.get_user_token.reset_mock()

        # Create client for "personal"
        client1 = VikunjaClient("@user:test", instance="personal")
        client1._get_token()

        # Create client for "business"
        client2 = VikunjaClient("@user:test", instance="business")
        client2._get_token()

        # Should have 2 calls with different instances
        assert mock_token_broker.get_user_token.call_count == 2

        calls = mock_token_broker.get_user_token.call_args_list
        instances = [call.kwargs.get("instance") for call in calls]

        assert "personal" in instances
        assert "business" in instances

    def test_instance_from_active_when_not_specified(self):
        """Uses active instance when not explicitly specified."""
        mock_token_broker.get_user_active_instance.return_value = "work"
        mock_token_broker.get_user_token.reset_mock()

        client = VikunjaClient("@user:test")  # No instance specified

        # Should use "work" from get_user_active_instance
        assert client.instance == "work"
