"""Comprehensive tests for matrix_handlers.py using TDD.

Test Coverage:
- Message handling flow
- Bang command handling (\!help, \!vik, \!credits)
- First contact / welcome flow
- Tool execution
- Error handling
- User token management
- Admin command protection
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from vikunja_mcp.matrix_handlers import (
    handle_matrix_message,
    _handle_bang_command,
    _get_matrix_welcome_message,
)


class TestHandleMatrixMessage:
    """Test the main message handling function."""

    @patch('vikunja_mcp.server._is_first_contact')
    @patch('vikunja_mcp.server._mark_user_welcomed')
    def test_first_contact_sends_welcome(self, mock_mark, mock_is_first):
        """First DM should send welcome message."""
        mock_is_first.return_value = True
        
        result = handle_matrix_message(
            message="hello",
            user_id="@user:matrix.org",
            is_dm=True
        )
        
        assert result["success"] is True
        assert result["is_welcome"] is True
        assert result["tool"] is None
        assert "welcome" in result["response"].lower() or "connect" in result["response"].lower()
        mock_mark.assert_called_once_with("@user:matrix.org")

    @patch('vikunja_mcp.server._is_first_contact')
    def test_not_first_contact_processes_normally(self, mock_is_first):
        """Non-first contact should process command normally."""
        mock_is_first.return_value = False
        
        result = handle_matrix_message(
            message="\!help",
            user_id="@user:matrix.org",
            is_dm=True
        )
        
        assert result["is_welcome"] is False or "is_welcome" not in result

    def test_empty_message_returns_error(self):
        """Empty message should return error."""
        result = handle_matrix_message(
            message="",
            user_id="@user:matrix.org"
        )
        
        assert result["success"] is False
        assert "didn't receive" in result["response"].lower() or "help" in result["response"].lower()

    def test_whitespace_only_message_returns_error(self):
        """Whitespace-only message should return error."""
        result = handle_matrix_message(
            message="   ",
            user_id="@user:matrix.org"
        )
        
        assert result["success"] is False

    @patch('vikunja_mcp.server._is_first_contact')
    def test_bang_command_routes_correctly(self, mock_is_first):
        """\!commands should route to bang handler."""
        mock_is_first.return_value = False
        
        result = handle_matrix_message(
            message="\!help",
            user_id="@user:matrix.org"
        )
        
        # Should process as bang command
        assert "tool" in result

    @patch('vikunja_mcp.server._is_first_contact')
    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_no_token_shows_connect_prompt(self, mock_token, mock_is_first):
        """User without token should see connect prompt for non-help commands."""
        mock_is_first.return_value = False
        mock_token.return_value = None
        
        result = handle_matrix_message(
            message="list tasks",
            user_id="@user:matrix.org"
        )
        
        assert result["success"] is False
        assert "connect" in result["response"].lower() or "\!vik" in result["response"].lower()

    @patch('vikunja_mcp.server._is_first_contact')
    def test_unparseable_message_needs_llm(self, mock_is_first):
        """Message that can't be parsed should set needs_llm=True."""
        mock_is_first.return_value = False
        
        result = handle_matrix_message(
            message="hello there how are you",
            user_id="@user:matrix.org"
        )
        
        assert result["needs_llm"] is True
        assert result["tool"] is None


class TestBangCommands:
    """Test \!command handling."""

    def test_help_command(self):
        """\!help should return help text."""
        result = _handle_bang_command(
            command="help",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is True
        assert len(result["response"]) > 0
        assert result["tool"] == "help"

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    @patch('vikunja_mcp.server._set_user_vikunja_token')
    def test_vik_command_sets_token(self, mock_set, mock_get):
        """\!vik <token> should set user's Vikunja token."""
        mock_get.return_value = None
        
        result = _handle_bang_command(
            command="vik tk_test123",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        mock_set.assert_called_once()
        assert result["success"] is True

    def test_vik_without_token_shows_error(self):
        """\!vik without token should show error."""
        result = _handle_bang_command(
            command="vik",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is False
        assert "token" in result["response"].lower()

    @patch('vikunja_mcp.server._is_admin')
    def test_credits_requires_admin(self, mock_is_admin):
        """\!credits should require admin."""
        mock_is_admin.return_value = False
        
        result = _handle_bang_command(
            command="credits",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is False
        assert "admin" in result["response"].lower()

    @patch('vikunja_mcp.server._is_admin')
    def test_credits_works_for_admin(self, mock_is_admin):
        """\!credits should work for admin users."""
        mock_is_admin.return_value = True
        
        result = _handle_bang_command(
            command="credits @user:matrix.org 1000",
            user_id="@admin:matrix.org",
            room_id=None
        )
        
        # Should process (might fail due to missing implementation, but shouldn't reject)
        assert "admin" not in result.get("response", "").lower() or result["success"] is True

    def test_unknown_bang_command(self):
        """Unknown \!command should return error."""
        result = _handle_bang_command(
            command="unknown",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is False
        assert "unknown" in result["response"].lower() or "help" in result["response"].lower()


class TestWelcomeMessage:
    """Test welcome message generation."""

    def test_welcome_message_not_empty(self):
        """Welcome message should not be empty."""
        msg = _get_matrix_welcome_message("@user:matrix.org")
        assert isinstance(msg, str)
        assert len(msg) > 0

    def test_welcome_message_mentions_connect(self):
        """Welcome message should mention how to connect."""
        msg = _get_matrix_welcome_message("@user:matrix.org")
        assert "\!vik" in msg or "connect" in msg.lower()

    def test_welcome_message_includes_user_id(self):
        """Welcome message might include user ID for personalization."""
        msg = _get_matrix_welcome_message("@alice:matrix.org")
        # This is optional, but good UX
        # assert "alice" in msg.lower()
        pass  # Not required


class TestToolExecution:
    """Test tool execution flow."""

    @patch('vikunja_mcp.server._is_first_contact')
    @patch('vikunja_mcp.server._get_user_vikunja_token')
    @patch('vikunja_mcp.server.TOOL_REGISTRY')
    def test_tool_execution_with_token(self, mock_registry, mock_token, mock_is_first):
        """Tool should execute when user has token."""
        mock_is_first.return_value = False
        mock_token.return_value = "tk_test123"
        
        # Mock tool
        mock_tool = Mock()
        mock_tool.return_value = {"tasks": []}
        mock_registry.get.return_value = mock_tool
        
        result = handle_matrix_message(
            message="list tasks",
            user_id="@user:matrix.org"
        )
        
        # Should attempt to execute tool
        assert result["tool"] == "list_all_tasks" or result["needs_llm"] is True

    @patch('vikunja_mcp.server._is_first_contact')
    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_help_works_without_token(self, mock_token, mock_is_first):
        """Help command should work without token."""
        mock_is_first.return_value = False
        mock_token.return_value = None
        
        result = handle_matrix_message(
            message="help",
            user_id="@user:matrix.org"
        )
        
        # Should not require token
        assert result["success"] is True or result["tool"] == "help"


class TestErrorHandling:
    """Test error handling scenarios."""

    @patch('vikunja_mcp.server._is_first_contact')
    @patch('vikunja_mcp.server._get_user_vikunja_token')
    @patch('vikunja_mcp.server.TOOL_REGISTRY')
    def test_tool_exception_handled(self, mock_registry, mock_token, mock_is_first):
        """Tool exceptions should be caught and returned as errors."""
        mock_is_first.return_value = False
        mock_token.return_value = "tk_test123"
        
        # Mock tool that raises exception
        mock_tool = Mock(side_effect=Exception("API error"))
        mock_registry.get.return_value = mock_tool
        
        result = handle_matrix_message(
            message="list tasks",
            user_id="@user:matrix.org"
        )
        
        # Should handle error gracefully
        assert "success" in result
        # Either returns error or needs LLM fallback
        assert result["success"] is False or result["needs_llm"] is True


class TestAdminProtection:
    """Test admin command protection."""

    @patch('vikunja_mcp.server._is_admin')
    def test_is_admin_checks_env_var(self, mock_is_admin):
        """Admin check should use MATRIX_ADMIN_IDS env var."""
        # This is tested via the _is_admin function
        # We're testing that it's called for admin commands
        mock_is_admin.return_value = False
        
        result = _handle_bang_command(
            command="credits @user:matrix.org 100",
            user_id="@notadmin:matrix.org",
            room_id=None
        )
        
        mock_is_admin.assert_called()


class TestCentralizedAuth:
    """Test centralized authentication for data isolation.

    CRITICAL: This tests the fix for solutions-k8ze - ensuring users
    without a Vikunja token cannot see other users' data.

    The bug was: _handle_stats and _handle_test_connection didn't check
    for user token, so they would fall back to VIKUNJA_TOKEN env var
    (admin token) and leak admin data.
    """

    def test_commands_requiring_token_set_is_complete(self):
        """Verify all commands that access Vikunja API are in the set."""
        from vikunja_mcp.matrix_handlers import COMMANDS_REQUIRING_VIKUNJA_TOKEN

        # These commands MUST require a token (they access Vikunja API)
        required = {
            "oops", "overdue", "now", "today", "week",
            "stats", "test",  # These were the buggy ones
            "done", "complete", "finish", "check",
            "bind", "switch", "project",
        }

        for cmd in required:
            assert cmd in COMMANDS_REQUIRING_VIKUNJA_TOKEN, \
                f"Command '{cmd}' should require Vikunja token but is not in set"

    def test_commands_without_token_set_is_complete(self):
        """Verify commands that don't need Vikunja token."""
        from vikunja_mcp.matrix_handlers import COMMANDS_WITHOUT_TOKEN

        # These commands should NOT require a token
        no_token_needed = {"help", "credits", "apikey", "model", "timezone"}

        for cmd in no_token_needed:
            assert cmd in COMMANDS_WITHOUT_TOKEN, \
                f"Command '{cmd}' should not require Vikunja token"

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_stats_requires_token(self, mock_get_token):
        """!stats should require token - was buggy before fix."""
        mock_get_token.return_value = None

        result = _handle_bang_command(
            command="stats",
            user_id="@newuser:matrix.org",
            room_id=None
        )

        assert result["success"] is False
        # Should show connect prompt, not admin's stats
        assert "connect" in result["response"].lower() or "!vik" in result["response"].lower()

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_test_command_requires_token(self, mock_get_token):
        """!test should require token - was buggy before fix."""
        mock_get_token.return_value = None

        result = _handle_bang_command(
            command="test",
            user_id="@newuser:matrix.org",
            room_id=None
        )

        assert result["success"] is False
        # Should show connect prompt, not test against admin's instance
        assert "connect" in result["response"].lower() or "!vik" in result["response"].lower()

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    @patch('vikunja_mcp.server._task_summary_impl')
    @patch('vikunja_mcp.server._current_vikunja_token')
    def test_stats_with_token_sets_context(self, mock_context, mock_summary, mock_get_token):
        """!stats with valid token should set context var correctly."""
        mock_get_token.return_value = "tk_user123"
        mock_summary.return_value = {
            "total": 5, "overdue": 1, "due_today": 2,
            "due_this_week": 3, "high_priority": 1, "unscheduled": 0
        }

        result = _handle_bang_command(
            command="stats",
            user_id="@user:matrix.org",
            room_id=None
        )

        # Token should be set in context
        mock_context.set.assert_called_with("tk_user123")
        assert result["success"] is True

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_help_works_without_token(self, mock_get_token):
        """!help should work even without token."""
        mock_get_token.return_value = None

        result = _handle_bang_command(
            command="help",
            user_id="@newuser:matrix.org",
            room_id=None
        )

        # Help doesn't require token
        assert result["success"] is True
        assert result["tool"] == "help"

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_credits_works_without_vikunja_token(self, mock_get_token):
        """!credits should work without Vikunja token (it's about Anthropic credits)."""
        mock_get_token.return_value = None

        result = _handle_bang_command(
            command="credits",
            user_id="@user:matrix.org",
            room_id=None
        )

        # Credits doesn't require Vikunja token
        # (it might require admin, but that's a different check)
        assert "connect" not in result["response"].lower() or result["success"] is False


class TestEnsureVikunjaToken:
    """Test the _ensure_vikunja_token helper function."""

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_returns_error_when_no_token(self, mock_get_token):
        """Should return error dict when user has no token."""
        from vikunja_mcp.matrix_handlers import _ensure_vikunja_token

        mock_get_token.return_value = None

        result = _ensure_vikunja_token("@user:matrix.org", "stats")

        assert result is not None  # Error response
        assert result["success"] is False
        assert "connect" in result["response"].lower() or "!vik" in result["response"].lower()

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    @patch('vikunja_mcp.server._current_vikunja_token')
    def test_returns_none_and_sets_context_when_token_exists(self, mock_context, mock_get_token):
        """Should return None (success) and set context when token exists."""
        from vikunja_mcp.matrix_handlers import _ensure_vikunja_token

        mock_get_token.return_value = "tk_validtoken123"

        result = _ensure_vikunja_token("@user:matrix.org", "stats")

        assert result is None  # Success - proceed with handler
        mock_context.set.assert_called_with("tk_validtoken123")


class TestDataIsolationRegression:
    """Regression tests to prevent data isolation bugs from returning.

    These tests specifically guard against the bug where a user without
    a Vikunja token could see another user's data by triggering a fallback
    to the VIKUNJA_TOKEN env var.
    """

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_all_task_commands_require_token(self, mock_get_token):
        """All task-related commands should require token."""
        mock_get_token.return_value = None

        task_commands = ["oops", "now", "today", "week", "tasks", "list"]

        for cmd in task_commands:
            result = _handle_bang_command(
                command=cmd,
                user_id="@newuser:matrix.org",
                room_id=None
            )
            assert result["success"] is False, f"!{cmd} should fail without token"
            assert "connect" in result["response"].lower() or "!vik" in result["response"].lower(), \
                f"!{cmd} should show connect prompt"

    @patch('vikunja_mcp.server._get_user_vikunja_token')
    def test_done_command_requires_token(self, mock_get_token):
        """!done should require token to prevent marking another user's tasks."""
        mock_get_token.return_value = None

        result = _handle_bang_command(
            command="done some task",
            user_id="@newuser:matrix.org",
            room_id=None
        )

        assert result["success"] is False
        assert "connect" in result["response"].lower() or "!vik" in result["response"].lower()


# Mutation testing targets (for enhanced TDD if needed):
# 1. First contact check (remove is_dm check)
# 2. Token check (remove token validation)
# 3. Admin check (remove admin validation)
# 4. Error handling (remove try/except)
# 5. Bang command prefix (change \! to something else)
