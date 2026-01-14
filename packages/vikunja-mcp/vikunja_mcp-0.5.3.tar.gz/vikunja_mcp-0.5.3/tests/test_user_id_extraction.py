"""Tests for user ID extraction and model tier mapping.

Covers:
- solutions-2dum: LLM hallucination and project sharing fix
- User ID format: vikunja:<username>:<numeric_id>
- Cost tier to model mapping: $ -> haiku, $$ -> sonnet, $$$ -> opus
"""

import pytest
from unittest.mock import Mock


class TestUserIdExtraction:
    """Test _extract_user_id returns format with numeric ID."""

    def test_extract_user_id_from_doer_with_id(self):
        """Doer with numeric ID returns vikunja:<username>:<id> format."""
        from src.vikunja_mcp.notification_poller import NotificationPoller

        poller = NotificationPoller(client=Mock())
        notification = {
            "notification": {
                "doer": {"username": "ivan", "id": 42}
            }
        }
        result = poller._extract_user_id(notification)
        assert result == "vikunja:ivan:42"

    def test_extract_user_id_from_doer_without_id(self):
        """Doer without numeric ID returns vikunja:<username> format."""
        from src.vikunja_mcp.notification_poller import NotificationPoller

        poller = NotificationPoller(client=Mock())
        notification = {
            "notification": {
                "doer": {"username": "ivan"}
            }
        }
        result = poller._extract_user_id(notification)
        assert result == "vikunja:ivan"

    def test_extract_user_id_from_comment_author(self):
        """Comment author with ID returns correct format."""
        from src.vikunja_mcp.notification_poller import NotificationPoller

        poller = NotificationPoller(client=Mock())
        notification = {
            "notification": {
                "comment": {
                    "author": {"username": "alice", "id": 123}
                }
            }
        }
        result = poller._extract_user_id(notification)
        assert result == "vikunja:alice:123"

    def test_extract_user_id_from_task_creator(self):
        """Task creator with ID returns correct format."""
        from src.vikunja_mcp.notification_poller import NotificationPoller

        poller = NotificationPoller(client=Mock())
        notification = {
            "notification": {
                "task": {
                    "created_by": {"username": "bob", "id": 456}
                }
            }
        }
        result = poller._extract_user_id(notification)
        assert result == "vikunja:bob:456"

    def test_extract_user_id_empty_notification(self):
        """Empty notification returns empty string."""
        from src.vikunja_mcp.notification_poller import NotificationPoller

        poller = NotificationPoller(client=Mock())
        notification = {"notification": {}}
        result = poller._extract_user_id(notification)
        assert result == ""


class TestRequestingUserParsing:
    """Test parsing of user_id into requesting_user and requesting_user_id."""

    def test_parse_user_id_with_numeric_id(self):
        """vikunja:<username>:<id> extracts both correctly."""
        user_id = "vikunja:ivan:42"

        # Extract username (everything between first and last colon)
        requesting_user = None
        if user_id and user_id.startswith("vikunja:"):
            parts = user_id.split(":")
            if len(parts) >= 2:
                requesting_user = parts[1]

        # Extract numeric user_id
        requesting_user_id = None
        if user_id and user_id.count(":") >= 2:
            try:
                requesting_user_id = int(user_id.rsplit(":", 1)[1])
            except (ValueError, IndexError):
                pass

        assert requesting_user == "ivan"
        assert requesting_user_id == 42

    def test_parse_user_id_without_numeric_id(self):
        """vikunja:<username> extracts username, no ID."""
        user_id = "vikunja:ivan"

        requesting_user = None
        if user_id and user_id.startswith("vikunja:"):
            parts = user_id.split(":")
            if len(parts) >= 2:
                requesting_user = parts[1]

        requesting_user_id = None
        if user_id and user_id.count(":") >= 2:
            try:
                requesting_user_id = int(user_id.rsplit(":", 1)[1])
            except (ValueError, IndexError):
                pass

        assert requesting_user == "ivan"
        assert requesting_user_id is None


class TestCostTierToModel:
    """Test cost tier to model mapping."""

    def test_tier_dollar_maps_to_haiku(self):
        """$ tier maps to haiku model."""
        tier_to_model = {
            "$": "haiku",
            "$$": "sonnet",
            "$$$": "opus",
        }
        assert tier_to_model.get("$", "haiku") == "haiku"

    def test_tier_double_dollar_maps_to_sonnet(self):
        """$$ tier maps to sonnet model."""
        tier_to_model = {
            "$": "haiku",
            "$$": "sonnet",
            "$$$": "opus",
        }
        assert tier_to_model.get("$$", "haiku") == "sonnet"

    def test_tier_triple_dollar_maps_to_opus(self):
        """$$$ tier maps to opus model."""
        tier_to_model = {
            "$": "haiku",
            "$$": "sonnet",
            "$$$": "opus",
        }
        assert tier_to_model.get("$$$", "haiku") == "opus"

    def test_default_tier_maps_to_haiku(self):
        """Unknown tier defaults to haiku."""
        tier_to_model = {
            "$": "haiku",
            "$$": "sonnet",
            "$$$": "opus",
        }
        assert tier_to_model.get("unknown", "haiku") == "haiku"


class TestNormalizeVikunjaUserId:
    """Test normalize_vikunja_user_id function.

    Bead: fa-me5dj - Fix user_id format mismatch
    """

    def test_normalize_3_element_to_2_element(self):
        """3-element vikunja:user:id should normalize to vikunja:user."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        result = normalize_vikunja_user_id("vikunja:ivan:1")
        assert result == "vikunja:ivan"

    def test_normalize_3_element_with_large_id(self):
        """3-element format with large numeric ID."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        result = normalize_vikunja_user_id("vikunja:alice:12345")
        assert result == "vikunja:alice"

    def test_keep_2_element_unchanged(self):
        """2-element vikunja:user should remain unchanged."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        result = normalize_vikunja_user_id("vikunja:ivan")
        assert result == "vikunja:ivan"

    def test_keep_non_vikunja_unchanged(self):
        """Non-vikunja formats should remain unchanged."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        assert normalize_vikunja_user_id("slack:U123") == "slack:U123"
        assert normalize_vikunja_user_id("matrix:@user:server") == "matrix:@user:server"

    def test_keep_3_element_non_vikunja_unchanged(self):
        """3-element non-vikunja formats should remain unchanged."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        result = normalize_vikunja_user_id("other:user:123")
        assert result == "other:user:123"

    def test_empty_string(self):
        """Empty string should return empty string."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        assert normalize_vikunja_user_id("") == ""

    def test_none_returns_none(self):
        """None should return None."""
        from src.vikunja_mcp.bot_provisioning import normalize_vikunja_user_id

        assert normalize_vikunja_user_id(None) is None


class TestModelCostCalculation:
    """Test cost calculation for different models."""

    def test_haiku_cost(self):
        """Haiku cost: $0.80/M in, $4/M out."""
        model_costs = {
            "haiku": (0.80, 4.0),
            "sonnet": (3.0, 15.0),
            "opus": (15.0, 75.0),
        }
        in_cost, out_cost = model_costs["haiku"]
        # 1000 input, 500 output tokens
        cost = (1000 * in_cost + 500 * out_cost) / 1_000_000
        assert cost == pytest.approx(0.0028, rel=0.01)

    def test_sonnet_cost(self):
        """Sonnet cost: $3/M in, $15/M out."""
        model_costs = {
            "haiku": (0.80, 4.0),
            "sonnet": (3.0, 15.0),
            "opus": (15.0, 75.0),
        }
        in_cost, out_cost = model_costs["sonnet"]
        # 1000 input, 500 output tokens
        cost = (1000 * in_cost + 500 * out_cost) / 1_000_000
        assert cost == pytest.approx(0.0105, rel=0.01)

    def test_opus_cost(self):
        """Opus cost: $15/M in, $75/M out."""
        model_costs = {
            "haiku": (0.80, 4.0),
            "sonnet": (3.0, 15.0),
            "opus": (15.0, 75.0),
        }
        in_cost, out_cost = model_costs["opus"]
        # 1000 input, 500 output tokens
        cost = (1000 * in_cost + 500 * out_cost) / 1_000_000
        assert cost == pytest.approx(0.0525, rel=0.01)


class TestMeetsTierRequirement:
    """Test meets_tier_requirement function.

    Bead: fa-qld6 - Block mutating tools for Haiku
    """

    def test_haiku_meets_dollar_tier(self):
        """Haiku can use $ tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("haiku", "$") is True

    def test_haiku_blocks_double_dollar(self):
        """Haiku cannot use $$ tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("haiku", "$$") is False

    def test_haiku_blocks_triple_dollar(self):
        """Haiku cannot use $$$ tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("haiku", "$$$") is False

    def test_sonnet_meets_dollar_tier(self):
        """Sonnet can use $ tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("sonnet", "$") is True

    def test_sonnet_meets_double_dollar(self):
        """Sonnet can use $$ tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("sonnet", "$$") is True

    def test_sonnet_blocks_triple_dollar(self):
        """Sonnet cannot use $$$ tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("sonnet", "$$$") is False

    def test_opus_meets_all_tiers(self):
        """Opus can use all tier tools."""
        from src.vikunja_mcp.tool_registry import meets_tier_requirement

        assert meets_tier_requirement("opus", "$") is True
        assert meets_tier_requirement("opus", "$$") is True
        assert meets_tier_requirement("opus", "$$$") is True


class TestCheckTierForTool:
    """Test check_tier_for_tool function.

    Bead: fa-qld6 - Block mutating tools for Haiku
    """

    def test_haiku_blocked_for_create_task(self):
        """Haiku is blocked from create_task."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("create_task", "haiku")
        assert allowed is False
        assert "requires $$" in error
        assert "upgrade" in error.lower()

    def test_sonnet_allowed_for_create_task(self):
        """Sonnet is allowed for create_task."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("create_task", "sonnet")
        assert allowed is True
        assert error is None

    def test_opus_allowed_for_create_task(self):
        """Opus is allowed for create_task."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("create_task", "opus")
        assert allowed is True
        assert error is None

    def test_haiku_allowed_for_list_tasks(self):
        """Haiku is allowed for list_tasks (read-only)."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("list_tasks", "haiku")
        assert allowed is True
        assert error is None

    def test_haiku_blocked_for_create_project(self):
        """Haiku is blocked from create_project."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("create_project", "haiku")
        assert allowed is False
        assert "requires $$" in error

    def test_haiku_blocked_for_batch_create_tasks(self):
        """Haiku is blocked from batch_create_tasks."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("batch_create_tasks", "haiku")
        assert allowed is False
        assert "requires $$" in error

    def test_unknown_tool_passes_through(self):
        """Unknown tools pass through (handled elsewhere)."""
        from src.vikunja_mcp.tool_registry import check_tier_for_tool

        allowed, error = check_tier_for_tool("nonexistent_tool", "haiku")
        assert allowed is True
        assert error is None
