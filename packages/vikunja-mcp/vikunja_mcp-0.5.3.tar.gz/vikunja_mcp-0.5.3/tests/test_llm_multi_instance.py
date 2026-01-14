"""
Tests for multi-instance LLM tool routing.

Verifies that LLM tool calls correctly use the user's active instance
URL and token from PostgreSQL, not YAML/env var fallbacks.

Bead: solutions-1qcp (regression tests for user context fix)
"""

import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path
import contextvars

# Load server module directly to avoid heavy imports
src_path = Path(__file__).parent.parent / "src"

# We need to mock several dependencies before importing server
mock_modules = {
    'mcp': MagicMock(),
    'mcp.server': MagicMock(),
    'mcp.server.models': MagicMock(),
    'mcp.types': MagicMock(),
    'markdown': MagicMock(),
    'markdown.extensions': MagicMock(),
    'markdown.extensions.fenced_code': MagicMock(),
    'anthropic': MagicMock(),
    'slack_sdk': MagicMock(),
    'slack_sdk.web': MagicMock(),
    'nio': MagicMock(),
    'pytz': MagicMock(),
}

for mod_name, mock_mod in mock_modules.items():
    if mod_name not in sys.modules:
        sys.modules[mod_name] = mock_mod


class TestCurrentUserIdContextVar:
    """Tests for _current_user_id context variable usage."""

    def test_context_var_exists(self):
        """Verify _current_user_id context var is defined."""
        # Import the context var directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "server_partial",
            src_path / "vikunja_mcp" / "server.py"
        )
        # We can't fully load server.py due to dependencies,
        # but we can verify the pattern exists in the file
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        assert "_current_user_id: contextvars.ContextVar" in server_code
        assert "_current_user_id.set(user_id)" in server_code

    def test_matrix_handler_sets_user_id(self):
        """Verify _matrix_chat_with_claude sets _current_user_id."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        # Find the _matrix_chat_with_claude function
        matrix_func_start = server_code.find("def _matrix_chat_with_claude")
        assert matrix_func_start != -1, "_matrix_chat_with_claude not found"

        # Find the next function definition (end of this function)
        next_func = server_code.find("\ndef ", matrix_func_start + 1)
        matrix_func_code = server_code[matrix_func_start:next_func]

        # Verify both context vars are set
        assert "_current_vikunja_token.set(user_vikunja_token)" in matrix_func_code
        assert "_current_user_id.set(user_id)" in matrix_func_code

    def test_slack_handler_sets_user_id(self):
        """Verify _slack_chat_with_claude sets _current_user_id."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        # Find the _slack_chat_with_claude function
        slack_func_start = server_code.find("def _slack_chat_with_claude")
        assert slack_func_start != -1, "_slack_chat_with_claude not found"

        # Find the next function definition
        next_func = server_code.find("\ndef ", slack_func_start + 1)
        slack_func_code = server_code[slack_func_start:next_func]

        # Verify both context vars are set
        assert "_current_vikunja_token.set(user_vikunja_token)" in slack_func_code
        assert "_current_user_id.set(user_id)" in slack_func_code


class TestRequestFunctionUserContext:
    """Tests for _request function's user context handling."""

    def test_request_checks_user_id_first(self):
        """Verify _request checks _current_user_id before falling back to YAML."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        # Find the _request function
        request_func_start = server_code.find("def _request(method: str, endpoint: str")
        assert request_func_start != -1, "_request function not found"

        # Find end of function (next def at same indentation)
        next_func = server_code.find("\ndef ", request_func_start + 1)
        request_func_code = server_code[request_func_start:next_func]

        # Verify it checks user_id context var
        assert "user_id = _current_user_id.get()" in request_func_code

        # Verify it uses _get_user_instance_config when user_id is set
        assert "_get_user_instance_config(user_id)" in request_func_code

    def test_request_uses_user_config_when_set(self):
        """Verify _request uses PostgreSQL config when user context is available."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        request_func_start = server_code.find("def _request(method: str, endpoint: str")
        next_func = server_code.find("\ndef ", request_func_start + 1)
        request_func_code = server_code[request_func_start:next_func]

        # The logic should be: if user_id -> use _get_user_instance_config
        # else -> use _get_instance_config (YAML fallback)
        assert "if user_id:" in request_func_code
        assert "_get_user_instance_config(user_id)" in request_func_code
        assert "_get_instance_config()" in request_func_code


class TestGetUserInstanceConfig:
    """Tests for _get_user_instance_config function."""

    def test_gets_active_instance(self):
        """Verify _get_user_instance_config gets user's active instance."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _get_user_instance_config(user_id: str)")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should get active instance
        assert "_get_user_instance(user_id)" in func_code

        # Should get token for that instance
        assert "_get_user_vikunja_token(user_id)" in func_code

        # Should get URL from PostgreSQL
        assert "get_user_instance_url" in func_code


class TestToolRegistryIntegration:
    """Tests for TOOL_REGISTRY tools using _request."""

    def test_list_tasks_uses_request(self):
        """Verify list_tasks impl uses _request (inherits user context)."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        # Find _list_tasks_impl
        func_start = server_code.find("def _list_tasks_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should use _fetch_all_pages which uses _request
        assert "_fetch_all_pages" in func_code

    def test_create_task_uses_request(self):
        """Verify create_task impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _create_task_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        assert "_request(" in func_code

    def test_get_task_uses_request(self):
        """Verify get_task impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _get_task_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        assert "_request(" in func_code

    def test_update_task_uses_request(self):
        """Verify update_task impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _update_task_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        assert "_request(" in func_code

    def test_complete_task_uses_request(self):
        """Verify complete_task impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _complete_task_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        assert "_request(" in func_code

    def test_delete_task_uses_request(self):
        """Verify delete_task impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _delete_task_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        assert "_request(" in func_code

    def test_list_projects_uses_request(self):
        """Verify list_projects impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _list_projects_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Uses _fetch_all_pages which uses _request
        assert "_fetch_all_pages" in func_code

    def test_create_project_uses_request(self):
        """Verify create_project impl uses _request."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _create_project_impl(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        assert "_request(" in func_code


class TestFetchAllPagesUsesRequest:
    """Tests for _fetch_all_pages using _request."""

    def test_fetch_all_pages_delegates_to_request(self):
        """Verify _fetch_all_pages uses _request for each page."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def _fetch_all_pages(")
        assert func_start != -1

        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should call _request for each page
        assert "_request(method, endpoint" in func_code


class TestMultiInstanceScenarios:
    """Integration-style tests for multi-instance scenarios."""

    def test_critical_comment_present_in_matrix_handler(self):
        """Verify the fix includes explanatory comment."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        # The fix should have a comment explaining why both are needed
        assert "CRITICAL: Both must be set for _request to use correct instance URL" in server_code

    def test_critical_comment_present_in_slack_handler(self):
        """Verify the fix comment is in both handlers."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        # Count occurrences - should be 2 (Matrix and Slack)
        count = server_code.count("CRITICAL: Both must be set for _request to use correct instance URL")
        assert count == 2, f"Expected 2 occurrences, found {count}"

    def test_solutions_1qcp_reference_present(self):
        """Verify the fix references the bead for traceability."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        assert "solutions-1qcp" in server_code


class TestContextVarOrder:
    """Tests for correct order of context var operations."""

    def test_token_set_before_user_id_in_matrix(self):
        """Token should be set, then user_id (order matters for logging)."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        matrix_start = server_code.find("def _matrix_chat_with_claude")
        next_func = server_code.find("\ndef ", matrix_start + 1)
        matrix_code = server_code[matrix_start:next_func]

        token_set_pos = matrix_code.find("_current_vikunja_token.set(")
        user_id_set_pos = matrix_code.find("_current_user_id.set(")

        # Both should exist
        assert token_set_pos != -1
        assert user_id_set_pos != -1

        # Token set should come first (for logging preview)
        assert token_set_pos < user_id_set_pos

    def test_token_set_before_user_id_in_slack(self):
        """Token should be set, then user_id in Slack handler too."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        slack_start = server_code.find("def _slack_chat_with_claude")
        next_func = server_code.find("\ndef ", slack_start + 1)
        slack_code = server_code[slack_start:next_func]

        token_set_pos = slack_code.find("_current_vikunja_token.set(")
        user_id_set_pos = slack_code.find("_current_user_id.set(")

        assert token_set_pos != -1
        assert user_id_set_pos != -1
        assert token_set_pos < user_id_set_pos


class TestVikunjaEisBotTokenSetup:
    """Tests for vikunja_chat_with_claude (@eis bot) token setup.

    Regression tests for solutions-bvw1: @eis was seeing 0 tasks because
    vikunja_chat_with_claude wasn't setting _current_vikunja_token before
    calling tools.
    """

    def test_vikunja_chat_with_claude_exists(self):
        """Verify vikunja_chat_with_claude function exists."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()
        assert "def vikunja_chat_with_claude(" in server_code

    def test_sets_bot_token_context_var(self):
        """Verify vikunja_chat_with_claude sets _current_vikunja_token with VIKUNJA_BOT_TOKEN."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        assert func_start != -1, "vikunja_chat_with_claude not found"

        # Find the next function definition (end of this function)
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should get VIKUNJA_BOT_TOKEN from environment
        assert 'os.environ.get("VIKUNJA_BOT_TOKEN")' in func_code

        # Should set context variable before tool-calling loop
        assert "_current_vikunja_token.set(" in func_code

    def test_validates_bot_token_exists(self):
        """Verify vikunja_chat_with_claude validates VIKUNJA_BOT_TOKEN is configured."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should check if bot_token exists and return error if not
        assert "if not bot_token:" in func_code
        assert 'return "Error: VIKUNJA_BOT_TOKEN not configured"' in func_code

    def test_wraps_in_try_finally(self):
        """Verify vikunja_chat_with_claude wraps tool-calling in try/finally."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should have try/finally block
        assert "try:" in func_code
        assert "finally:" in func_code

        # Should reset token in finally block
        assert "_current_vikunja_token.reset(" in func_code

    def test_token_set_before_claude_call(self):
        """Verify token is set before creating Claude client."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        token_set_pos = func_code.find("_current_vikunja_token.set(")
        claude_create_pos = func_code.find("anthropic.Anthropic(")

        # Both should exist
        assert token_set_pos != -1, "Token set not found"
        assert claude_create_pos != -1, "Claude client creation not found"

        # Token should be set before Claude client is created
        assert token_set_pos < claude_create_pos

    def test_solutions_bvw1_reference_present(self):
        """Verify the fix references solutions-bvw1 for traceability."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should reference the bead issue
        assert "solutions-bvw1" in func_code

    def test_uses_bot_token_not_user_token(self):
        """Verify vikunja_chat_with_claude uses VIKUNJA_BOT_TOKEN, not user tokens."""
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should use VIKUNJA_BOT_TOKEN
        assert "VIKUNJA_BOT_TOKEN" in func_code

        # Should NOT call _get_user_vikunja_token (this is for bot, not user)
        assert "_get_user_vikunja_token" not in func_code

    def test_no_user_id_context_var(self):
        """Verify vikunja_chat_with_claude does NOT set _current_user_id.

        This is a bot function operating with system token, not a user-specific
        function like _slack_chat_with_claude or _matrix_chat_with_claude.
        """
        server_code = (src_path / "vikunja_mcp" / "server.py").read_text()

        func_start = server_code.find("def vikunja_chat_with_claude(")
        next_func = server_code.find("\ndef ", func_start + 1)
        func_code = server_code[func_start:next_func]

        # Should NOT set _current_user_id (this is bot context, not user context)
        assert "_current_user_id.set(" not in func_code
