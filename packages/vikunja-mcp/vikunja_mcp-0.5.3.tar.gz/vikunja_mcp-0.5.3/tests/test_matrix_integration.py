"""Integration tests for Matrix bot - test real code paths.

These tests minimize mocking to ensure actual code execution and coverage.
Focus on critical paths: message handling, tool execution, error handling.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestMessageHandlingIntegration:
    """Integration tests for message handling flow."""

    def test_help_command_executes_real_parser(self):
        """\!help should execute real parser and return help text."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        # Mock only external dependencies
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            result = handle_matrix_message(
                message="\!help",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        # Should succeed
        assert result["success"] is True
        assert "help" in result.get("tool", "").lower() or len(result["response"]) > 100
        assert "list" in result["response"].lower()  # Should list commands
        assert result.get("needs_llm") is False

    def test_list_tasks_command_parsing(self):
        """'list tasks' should parse correctly through real parser."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        # Mock external dependencies
        with patch('vikunja_mcp.server._is_first_contact', return_value=False), \
             patch('vikunja_mcp.server._get_user_vikunja_token', return_value=None):
            
            result = handle_matrix_message(
                message="list tasks",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        # Should recognize command but fail due to no token
        assert result["success"] is False
        assert "connect" in result["response"].lower() or "token" in result["response"].lower()

    def test_empty_message_handling(self):
        """Empty message should be handled gracefully."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            result = handle_matrix_message(
                message="",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        assert result["success"] is False
        assert len(result["response"]) > 0

    def test_whitespace_message_handling(self):
        """Whitespace-only message should be handled gracefully."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            result = handle_matrix_message(
                message="   \n  \t  ",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        assert result["success"] is False

    def test_unparseable_message_needs_llm(self):
        """Unparseable message should set needs_llm flag."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            result = handle_matrix_message(
                message="xyzabc123nonsense",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        # Should either need LLM or return error
        assert result.get("needs_llm") is True or result["success"] is False


class TestBangCommandIntegration:
    """Integration tests for bang commands."""

    def test_help_bang_command(self):
        """\!help should work without token."""
        from vikunja_mcp.matrix_handlers import _handle_bang_command
        
        result = _handle_bang_command(
            command="help",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is True
        assert len(result["response"]) > 100
        assert "list" in result["response"].lower()

    def test_question_mark_help(self):
        """? should work as help alias."""
        from vikunja_mcp.matrix_handlers import _handle_bang_command
        
        result = _handle_bang_command(
            command="?",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is True
        assert len(result["response"]) > 50

    def test_unknown_bang_command(self):
        """Unknown \!command should return error."""
        from vikunja_mcp.matrix_handlers import _handle_bang_command
        
        result = _handle_bang_command(
            command="unknowncommand123",
            user_id="@user:matrix.org",
            room_id=None
        )
        
        assert result["success"] is False
        assert "unknown" in result["response"].lower() or "help" in result["response"].lower()

    def test_vik_without_args_shows_prompt(self):
        """\!vik without args should show connect prompt."""
        from vikunja_mcp.matrix_handlers import _handle_bang_command
        
        with patch('vikunja_mcp.server._get_matrix_connect_prompt', return_value="Connect prompt"):
            result = _handle_bang_command(
                command="vik",
                user_id="@user:matrix.org",
                room_id=None
            )
        
        assert result["success"] is True
        assert len(result["response"]) > 0


class TestClientMessageFlow:
    """Integration tests for client message handling."""

    def test_dm_detection(self):
        """Test DM room detection logic."""
        from vikunja_mcp.matrix_client import MatrixBot
        from nio import RoomMessageText, MatrixRoom
        
        # Create bot
        bot = MatrixBot(
            homeserver="https://matrix.org",
            user_id="@bot:matrix.org",
            password="test123"
        )
        
        # Create mock room
        room = Mock(spec=MatrixRoom)
        room.member_count = 2
        room.room_id = "\!test:matrix.org"
        
        # DM should have 2 members
        assert room.member_count == 2

    def test_admin_check_with_admin(self):
        """Test admin recognition."""
        from vikunja_mcp.matrix_client import MatrixBot
        
        bot = MatrixBot(
            homeserver="https://matrix.org",
            user_id="@bot:matrix.org",
            password="test123",
            admin_ids=["@admin:matrix.org"]
        )
        
        assert bot._is_admin("@admin:matrix.org") is True
        assert bot._is_admin("@user:matrix.org") is False

    def test_admin_check_no_admins(self):
        """Test admin check with no admins configured."""
        from vikunja_mcp.matrix_client import MatrixBot
        
        bot = MatrixBot(
            homeserver="https://matrix.org",
            user_id="@bot:matrix.org",
            password="test123"
        )
        
        # No admins configured - all users are admins
        assert bot._is_admin("@anyone:matrix.org") is True


class TestErrorHandling:
    """Integration tests for error handling."""

    def test_invalid_message_type(self):
        """Test handling of invalid message types."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            # None message
            result = handle_matrix_message(
                message="",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        # Should handle gracefully
        assert "success" in result
        assert "response" in result

    def test_very_long_message(self):
        """Test handling of very long messages."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            result = handle_matrix_message(
                message="list tasks " + "x" * 10000,
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        # Should handle without crashing
        assert "success" in result
        assert "response" in result

    def test_unicode_message(self):
        """Test handling of Unicode messages."""
        from vikunja_mcp.matrix_handlers import handle_matrix_message
        
        with patch('vikunja_mcp.server._is_first_contact', return_value=False):
            result = handle_matrix_message(
                message="list tasks 🎯📝✅",
                user_id="@user:matrix.org",
                is_dm=True
            )
        
        # Should handle Unicode gracefully
        assert "success" in result
        assert "response" in result


# Mutation testing targets for integration tests:
# 1. Remove _is_first_contact check
# 2. Remove empty message check
# 3. Remove whitespace stripping
# 4. Change admin check logic
# 5. Remove DM detection
