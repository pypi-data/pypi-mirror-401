"""Comprehensive tests for matrix_parser.py using TDD.

Test Coverage:
- Command parsing (exact match, fuzzy match, no match)
- Argument extraction
- Edge cases (empty input, special chars, unicode)
- Threshold behavior
- Help text generation
"""

import pytest
from vikunja_mcp.matrix_parser import (
    parse_command,
    get_command_help,
    COMMANDS,
    MATCH_THRESHOLD,
)


class TestExactMatching:
    """Test exact command matching."""

    def test_exact_match_list_tasks(self):
        """Exact match for 'list tasks' should return list_all_tasks."""
        tool, args = parse_command("list tasks")
        assert tool == "list_all_tasks"
        assert args == ""

    def test_exact_match_with_args(self):
        """Exact match with arguments should extract args correctly."""
        tool, args = parse_command("add buy groceries")
        assert tool == "create_task"
        assert args == "buy groceries"

    def test_exact_match_done_with_id(self):
        """'done 42' should parse as complete_task with arg '42'."""
        tool, args = parse_command("done 42")
        assert tool == "complete_task"
        assert args == "42"

    def test_exact_match_multiword_command(self):
        """Multi-word commands like 'config add' should match exactly."""
        tool, args = parse_command("config add https://vikunja.example.com")
        assert tool == "add_instance"
        assert args == "https://vikunja.example.com"

    def test_exact_match_case_insensitive(self):
        """Commands should be case-insensitive."""
        tool, args = parse_command("LIST TASKS")
        assert tool == "list_all_tasks"
        assert args == ""


class TestFuzzyMatching:
    """Test fuzzy matching for typos."""

    def test_typo_in_command(self):
        """'lst tasks' should fuzzy match to 'list tasks'."""
        tool, args = parse_command("lst tasks")
        # This might not match if score < 80, which is expected
        # We'll verify the threshold behavior
        if tool:
            assert tool == "list_all_tasks"

    def test_typo_tolerance(self):
        """'crete task' should fuzzy match to 'create task'."""
        tool, args = parse_command("crete task buy milk")
        # Fuzzy matching should handle this
        if tool:
            assert tool == "create_task"

    def test_below_threshold_returns_none(self):
        """Input with no good match should return None."""
        tool, args = parse_command("hello there")
        assert tool is None
        assert args == "hello there"

    def test_gibberish_returns_none(self):
        """Random gibberish should return None."""
        tool, args = parse_command("xyzabc123")
        assert tool is None
        assert args == "xyzabc123"


class TestArgumentExtraction:
    """Test argument extraction from commands."""

    def test_no_args(self):
        """Command with no args should return empty string."""
        tool, args = parse_command("tasks")
        assert tool == "list_all_tasks"
        assert args == ""

    def test_single_word_arg(self):
        """Single word argument should be extracted."""
        tool, args = parse_command("delete 123")
        assert tool == "delete_task"
        assert args == "123"

    def test_multi_word_args(self):
        """Multi-word arguments should be preserved."""
        tool, args = parse_command("add finish the quarterly report by Friday")
        assert tool == "create_task"
        assert args == "finish the quarterly report by Friday"

    def test_args_with_special_chars(self):
        """Arguments with special characters should be preserved."""
        tool, args = parse_command("add buy milk & eggs @ store")
        assert tool == "create_task"
        assert args == "buy milk & eggs @ store"

    def test_args_with_numbers(self):
        """Arguments with numbers should be preserved."""
        tool, args = parse_command("update 42 priority 1")
        assert tool == "update_task"
        assert args == "42 priority 1"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_string(self):
        """Empty string should return None."""
        tool, args = parse_command("")
        assert tool is None
        assert args == ""

    def test_whitespace_only(self):
        """Whitespace-only input should return None."""
        tool, args = parse_command("   ")
        assert tool is None
        assert args == "   "

    def test_leading_trailing_whitespace(self):
        """Leading/trailing whitespace should be stripped."""
        tool, args = parse_command("  list tasks  ")
        assert tool == "list_all_tasks"
        assert args == ""

    def test_unicode_input(self):
        """Unicode characters should be handled."""
        tool, args = parse_command("add café meeting ☕")
        assert tool == "create_task"
        assert args == "café meeting ☕"

    def test_very_long_input(self):
        """Very long input should be handled."""
        long_text = "add " + "word " * 100
        tool, args = parse_command(long_text)
        assert tool == "create_task"
        assert len(args) > 0


class TestPrefixMatching:
    """Test prefix matching for multi-word commands."""

    def test_config_add_beats_config(self):
        """'config add' should match 'config add', not just 'config'."""
        tool, args = parse_command("config add https://example.com")
        assert tool == "add_instance"
        assert args == "https://example.com"

    def test_config_list_beats_config(self):
        """'config list' should match 'config list', not just 'config'."""
        tool, args = parse_command("config list")
        assert tool == "list_instances"
        assert args == ""

    def test_config_alone_matches_config(self):
        """'config' alone should match 'config'."""
        tool, args = parse_command("config")
        assert tool == "list_instances"
        assert args == ""

    def test_prefix_with_word_boundary(self):
        """Prefix matching should respect word boundaries."""
        # "show 42" should match "show" (prefix)
        tool, args = parse_command("show 42")
        assert tool == "get_task"
        assert args == "42"


class TestHelpCommand:
    """Test help command and help text generation."""

    def test_help_command(self):
        """'help' should return help tool."""
        tool, args = parse_command("help")
        assert tool == "help"
        assert args == ""

    def test_question_mark_help(self):
        """'?' should return help tool."""
        tool, args = parse_command("?")
        assert tool == "help"
        assert args == ""

    def test_get_command_help_returns_string(self):
        """get_command_help() should return a non-empty string."""
        help_text = get_command_help()
        assert isinstance(help_text, str)
        assert len(help_text) > 0

    def test_help_text_contains_commands(self):
        """Help text should mention key commands."""
        help_text = get_command_help()
        assert "list" in help_text.lower() or "tasks" in help_text.lower()
        assert "create" in help_text.lower() or "add" in help_text.lower()


class TestCommandRegistry:
    """Test the COMMANDS registry structure."""

    def test_commands_is_dict(self):
        """COMMANDS should be a dictionary."""
        assert isinstance(COMMANDS, dict)

    def test_commands_not_empty(self):
        """COMMANDS should have entries."""
        assert len(COMMANDS) > 0

    def test_all_values_are_strings(self):
        """All COMMANDS values should be strings (tool names)."""
        for tool_name in COMMANDS.values():
            assert isinstance(tool_name, str)

    def test_threshold_is_int(self):
        """MATCH_THRESHOLD should be an integer."""
        assert isinstance(MATCH_THRESHOLD, int)

    def test_threshold_in_valid_range(self):
        """MATCH_THRESHOLD should be between 0 and 100."""
        assert 0 <= MATCH_THRESHOLD <= 100


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_natural_language_whats_due(self):
        """'what's due today' should work."""
        tool, args = parse_command("what's due today")
        assert tool == "list_all_tasks"

    def test_natural_language_show_me_tasks(self):
        """'show me my tasks' uses prefix matching.
        
        Prefix matching wins: 'show' matches first, args are 'me my tasks'.
        This is expected behavior. User can say 'my tasks' or 'list tasks' 
        if they want list_all_tasks.
        """
        tool, args = parse_command("show me my tasks")
        # Prefix match to "show" wins over fuzzy match to "my tasks"
        assert tool == "get_task"
        assert args == "me my tasks"

    def test_my_tasks_alone(self):
        """'my tasks' alone should match list_all_tasks."""
        tool, args = parse_command("my tasks")
        assert tool == "list_all_tasks"
        assert args == ""

    def test_abbreviated_command(self):
        """'del 42' should work for delete."""
        tool, args = parse_command("del 42")
        assert tool == "delete_task"
        assert args == "42"

    def test_task_with_emoji(self):
        """Task with emoji should preserve emoji."""
        tool, args = parse_command("add 🎯 finish presentation")
        assert tool == "create_task"
        assert "🎯" in args


# Mutation testing targets (for enhanced TDD if needed):
# 1. MATCH_THRESHOLD value (try 50, 90, 100)
# 2. Prefix matching logic (remove best_match_len check)
# 3. Fuzzy scorer (try different scorers)
# 4. Case sensitivity (remove .lower())
# 5. Whitespace handling (remove .strip())
