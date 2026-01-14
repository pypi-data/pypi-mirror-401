"""
Tests for @eis command parser.

Bead: solutions-3kse, solutions-hgwx.1
"""

import os
import pytest
from vikunja_mcp.command_parser import CommandParser, ParseResult


@pytest.fixture
def parser():
    """Create a CommandParser instance."""
    return CommandParser()


@pytest.fixture
def enable_llm(monkeypatch):
    """Enable LLM features for tests that require them."""
    monkeypatch.setenv("ENABLE_LLM_FEATURES", "true")


class TestTier3Commands:
    """Test Tier 3 (deterministic) commands."""

    def test_complete_single_task(self, parser):
        """Test !complete with single task ID."""
        result = parser.parse("@eis !complete 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        assert result.args["task_ids"] == [42]
        assert result.confidence == 1.0

    def test_complete_alias_done(self, parser):
        """Test !done alias."""
        result = parser.parse("@eis !done 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        assert result.args["task_ids"] == [42]

    def test_complete_alias_do(self, parser):
        """Test !do alias."""
        result = parser.parse("@eis !do 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"

    def test_complete_alias_x(self, parser):
        """Test !x super short alias."""
        result = parser.parse("@eis !x 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        assert result.args["task_ids"] == [42]

    def test_batch_complete_comma_separated(self, parser):
        """Test batch complete with comma-separated IDs."""
        result = parser.parse("@eis !x 1,2,3")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        assert result.args["task_ids"] == [1, 2, 3]

    def test_batch_complete_space_separated(self, parser):
        """Test batch complete with space-separated IDs."""
        result = parser.parse("@eis !x 1 2 3")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        assert result.args["task_ids"] == [1, 2, 3]

    def test_remind_command(self, parser):
        """Test !remind command."""
        result = parser.parse("@eis !remind 42 / tomorrow at 3pm")

        assert result.tier == "tier3"
        assert result.handler == "set_reminder"
        assert result.args["task_id"] == 42
        assert result.args["when"] == "tomorrow at 3pm"

    def test_remind_alias_r(self, parser):
        """Test !r short alias."""
        result = parser.parse("@eis !r 42 / next week")

        assert result.tier == "tier3"
        assert result.handler == "set_reminder"
        assert result.args["task_id"] == 42
        assert result.args["when"] == "next week"

    def test_weather_command(self, parser):
        """Test !weather command."""
        result = parser.parse("@eis !weather San Francisco")

        assert result.tier == "tier3"
        assert result.handler == "weather_handler"
        assert result.args["location"] == "San Francisco"

    def test_weather_with_schedule(self, parser):
        """Test !weather with sub-daily schedule keyword."""
        result = parser.parse("@eis !weather Tokyo hourly")

        assert result.tier == "tier3"
        assert result.handler == "weather_handler"
        assert result.args["location"] == "Tokyo"
        assert result.args["schedule"] == "hourly"

    def test_weather_alias_w(self, parser):
        """Test !w short alias with schedule."""
        result = parser.parse("@eis !w Seattle 6h")

        assert result.tier == "tier3"
        assert result.handler == "weather_handler"
        assert result.args["schedule"] == "6h"

    @pytest.mark.skip(reason="Stock command disabled (solutions-js3e)")
    def test_stock_command(self, parser):
        """Test !stock command."""
        result = parser.parse("@eis !stock AAPL")

        assert result.tier == "tier3"
        assert result.handler == "stock_handler"
        assert result.args["ticker"] == "AAPL"

    @pytest.mark.skip(reason="Stock command disabled (solutions-js3e)")
    def test_stock_with_schedule(self, parser):
        """Test !stock with sub-daily schedule keyword."""
        result = parser.parse("@eis !s AAPL hourly")

        assert result.tier == "tier3"
        assert result.handler == "stock_handler"
        assert result.args["ticker"] == "AAPL"
        assert result.args["schedule"] == "hourly"


class TestFuzzyMatching:
    """Test fuzzy command matching."""

    def test_fuzzy_complete_typo(self, parser):
        """Test fuzzy matching with typo."""
        result = parser.parse("@eis !complet 42")  # Missing 'e'

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        assert result.confidence >= 0.7

    def test_fuzzy_weather_typo(self, parser):
        """Test fuzzy matching for weather."""
        result = parser.parse("@eis !wether Boston")  # Typo

        assert result.tier == "tier3"
        assert result.handler == "weather_handler"

    def test_fuzzy_no_match(self, parser):
        """Test that garbage doesn't match."""
        result = parser.parse("@eis !xyzabc 42")

        assert result.tier == "unknown"
        assert "Unknown command" in result.error


class TestAliasNormalization:
    """Test @e → @eis alias normalization."""

    def test_e_alias_space(self, parser):
        """Test @e with space."""
        result = parser.parse("@e !x 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"

    def test_e_alias_bang(self, parser):
        """Test @e! (no space)."""
        result = parser.parse("@e!x 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"

    def test_e_alias_dollar(self, parser, enable_llm):
        """Test @e$ for LLM tier."""
        result = parser.parse("@e$ plan a party")

        assert result.tier == "tier1"
        assert result.handler == "llm_natural"
        assert result.args["cost_tier"] == "$"
        assert result.args["prompt"] == "plan a party"


@pytest.mark.usefixtures("enable_llm")
class TestLLMTiers:
    """Test LLM tier parsing (Phase 2). Requires ENABLE_LLM_FEATURES=true."""

    def test_tier1_single_dollar(self, parser):
        """Test $ (Tier 1) command."""
        result = parser.parse("@eis $ create a sourdough project")

        assert result.tier == "tier1"
        assert result.handler == "llm_natural"
        assert result.args["cost_tier"] == "$"
        assert result.args["prompt"] == "create a sourdough project"
        assert result.error is None  # Phase 2: no error
        assert result.confidence == 1.0

    def test_tier1_double_dollar(self, parser):
        """Test $$ (Tier 1) command."""
        result = parser.parse("@eis $$ analyze my project")

        assert result.tier == "tier1"
        assert result.handler == "llm_natural"
        assert result.args["cost_tier"] == "$$"

    def test_tier1_triple_dollar(self, parser):
        """Test $$$ (Tier 1) command."""
        result = parser.parse("@eis $$$ research best practices")

        assert result.tier == "tier1"
        assert result.handler == "llm_natural"
        assert result.args["cost_tier"] == "$$$"

    def test_tier2_with_task_ref_number(self, parser):
        """Test Tier 2 with numeric task reference."""
        result = parser.parse("@eis $ 42 / summarize comments")

        assert result.tier == "tier2"
        assert result.handler == "llm_context"
        assert result.args["task_ref"] == "42"
        assert result.args["instruction"] == "summarize comments"
        assert result.error is None  # Phase 2: no error

    def test_tier2_with_task_ref_quoted(self, parser):
        """Test Tier 2 with quoted task reference."""
        result = parser.parse('@eis $$ "Implement auth" / break into subtasks')

        assert result.tier == "tier2"
        assert result.handler == "llm_context"
        assert result.args["task_ref"] == "Implement auth"
        assert result.args["instruction"] == "break into subtasks"


class TestBudgetCommands:
    """Test budget management commands (Phase 2)."""

    def test_upgrade_command(self, parser):
        """Test !upgrade command."""
        result = parser.parse("@eis !upgrade $$")

        assert result.tier == "tier3"
        assert result.handler == "upgrade_tier"
        assert result.args["new_tier"] == "$$"

    def test_upgrade_to_triple_dollar(self, parser):
        """Test upgrading to $$$ tier."""
        result = parser.parse("@eis !upgrade $$$")

        assert result.tier == "tier3"
        assert result.handler == "upgrade_tier"
        assert result.args["new_tier"] == "$$$"

    def test_reset_budget_command(self, parser):
        """Test !reset-budget command."""
        result = parser.parse("@eis !reset-budget")

        assert result.tier == "tier3"
        assert result.handler == "reset_budget"

    def test_reset_alias(self, parser):
        """Test !reset short alias."""
        result = parser.parse("@eis !reset")

        assert result.tier == "tier3"
        assert result.handler == "reset_budget"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_no_eis_mention(self, parser):
        """Test text without @eis."""
        result = parser.parse("Buy groceries")

        assert result.tier == "unknown"
        assert "No @mention found" in result.error

    def test_empty_text(self, parser):
        """Test empty string."""
        result = parser.parse("")

        assert result.tier == "unknown"

    def test_eis_no_command(self, parser):
        """Test @eis with no command after."""
        result = parser.parse("@eis")

        assert result.tier == "unknown"
        assert result.error is not None

    def test_case_insensitive(self, parser):
        """Test case insensitivity for @eis."""
        result = parser.parse("@EIS !x 42")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"

    def test_eis_in_middle_of_text(self, parser):
        """Test @eis in middle of text."""
        result = parser.parse("Hey @eis !complete 42 please")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        # Note: "please" gets included in args but regex ignores non-digits
        assert result.args["task_ids"] == [42]

    def test_complete_no_task_id(self, parser):
        """Test !complete without task ID."""
        result = parser.parse("@eis !complete")

        assert result.tier == "tier3"
        assert result.handler == "complete_task"
        # No task IDs found - args is empty dict, handler will report error
        assert result.args == {} or result.args.get("task_ids") == []


@pytest.mark.usefixtures("enable_llm")
class TestTierNatural:
    """Test tier_natural (natural language with tool access). Requires ENABLE_LLM_FEATURES=true."""

    def test_natural_language_question(self, parser):
        """Test natural language question goes to tier_natural."""
        result = parser.parse("@eis what tasks are overdue?")

        assert result.tier == "tier_natural"
        assert result.handler == "llm_tools"
        assert result.args["prompt"] == "what tasks are overdue?"
        assert result.confidence == 0.8

    def test_natural_language_request(self, parser):
        """Test natural language request goes to tier_natural."""
        result = parser.parse("@eis show me high priority tasks")

        assert result.tier == "tier_natural"
        assert result.handler == "llm_tools"
        assert result.args["prompt"] == "show me high priority tasks"

    def test_natural_language_action(self, parser):
        """Test natural language action goes to tier_natural."""
        result = parser.parse("@eis create a task for grocery shopping")

        assert result.tier == "tier_natural"
        assert result.handler == "llm_tools"
        assert result.args["prompt"] == "create a task for grocery shopping"

    def test_natural_with_e_alias(self, parser):
        """Test @e alias works for natural language."""
        result = parser.parse("@e list tasks due today")

        assert result.tier == "tier_natural"
        assert result.handler == "llm_tools"
        assert result.args["prompt"] == "list tasks due today"

    def test_implicit_mention_natural(self, parser):
        """Test implicit mention with natural language."""
        result = parser.parse("what's on my plate today?", implicit_mention=True)

        assert result.tier == "tier_natural"
        assert result.handler == "llm_tools"
        assert result.args["prompt"] == "what's on my plate today?"
