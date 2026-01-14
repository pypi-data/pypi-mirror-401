"""
Tests for LLM tier handlers (Phase 2).

Bead: solutions-hgwx.2
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from vikunja_mcp.keyword_handlers import KeywordHandlers, HandlerResult
from vikunja_mcp.llm_client import LLMClient, LLMResponse


@pytest.fixture
def mock_client():
    """Create a mock Vikunja client."""
    client = Mock()
    client.get_task = Mock(return_value={
        "id": 42,
        "title": "Test task",
        "description": "Test description",
    })
    client.update_task = Mock()
    client.add_comment = Mock()
    return client


@pytest.fixture
def handlers(mock_client):
    """Create KeywordHandlers with mock client."""
    return KeywordHandlers(client=mock_client)


class TestLLMClient:
    """Test LLM client stub."""

    @pytest.mark.asyncio
    async def test_complete_stub(self):
        """Test stub response for complete."""
        client = LLMClient()
        response = await client.complete("Create a project", cost_tier="$")

        assert response.success is True
        assert response.calls_used == 1
        assert "placeholder" in response.content.lower() or "LLM" in response.content

    @pytest.mark.asyncio
    async def test_complete_tiers(self):
        """Test different cost tiers."""
        client = LLMClient()

        response_cheap = await client.complete("test", cost_tier="$")
        response_medium = await client.complete("test", cost_tier="$$")
        response_expensive = await client.complete("test", cost_tier="$$$")

        assert response_cheap.success
        assert response_medium.success
        assert response_expensive.success

    @pytest.mark.asyncio
    async def test_analyze_task_stub(self):
        """Test stub response for analyze_task."""
        client = LLMClient()
        response = await client.analyze_task(
            task_title="My Task",
            task_description="Some description",
            instruction="summarize",
            cost_tier="$$",
        )

        assert response.success is True
        assert response.calls_used == 1

    @pytest.mark.asyncio
    async def test_format_data_stub(self):
        """Test stub response for format_data."""
        client = LLMClient()
        response = await client.format_data(
            data={"temp": 72, "condition": "sunny"},
            format_instruction="format as friendly weather",
            cost_tier="$",
        )

        assert response.success is True


class TestLLMNaturalHandler:
    """Test Tier 1 LLM natural language handler."""

    @pytest.mark.asyncio
    async def test_llm_natural_success(self, handlers):
        """Test successful LLM natural language command."""
        result = await handlers.llm_natural(
            {"cost_tier": "$", "prompt": "create a project"},
            task_id=42
        )

        assert result.success is True
        assert "LLM calls" in result.message  # Cost footer present
        assert result.data["calls_used"] == 1

    @pytest.mark.asyncio
    async def test_llm_natural_no_prompt(self, handlers):
        """Test LLM natural without prompt."""
        result = await handlers.llm_natural({"cost_tier": "$"})

        assert result.success is False
        assert "No prompt provided" in result.message

    @pytest.mark.asyncio
    async def test_llm_natural_tracks_metadata(self, handlers):
        """Test that metadata is tracked."""
        result = await handlers.llm_natural(
            {"cost_tier": "$$", "prompt": "analyze something"},
            task_id=42
        )

        assert result.success is True
        metadata = result.data["metadata"]
        assert metadata.cost_tier == "$$"
        assert metadata.llm_calls_used == 1


class TestLLMContextHandler:
    """Test Tier 2 LLM context handler."""

    @pytest.mark.asyncio
    async def test_llm_context_success(self, handlers):
        """Test successful LLM context command."""
        result = await handlers.llm_context(
            {"cost_tier": "$$", "task_ref": "42", "instruction": "summarize"}
        )

        assert result.success is True
        assert "#42" in result.message
        assert "Test task" in result.message  # Task title

    @pytest.mark.asyncio
    async def test_llm_context_no_task_ref(self, handlers):
        """Test LLM context without task reference."""
        result = await handlers.llm_context(
            {"cost_tier": "$$", "instruction": "summarize"}
        )

        assert result.success is False
        assert "No task reference" in result.message

    @pytest.mark.asyncio
    async def test_llm_context_no_instruction(self, handlers):
        """Test LLM context without instruction."""
        result = await handlers.llm_context(
            {"cost_tier": "$$", "task_ref": "42"}
        )

        assert result.success is False
        assert "No instruction" in result.message

    @pytest.mark.asyncio
    async def test_llm_context_fuzzy_name_not_supported(self, handlers):
        """Test that fuzzy name lookup is not yet supported."""
        result = await handlers.llm_context(
            {"cost_tier": "$$", "task_ref": "Implement auth", "instruction": "summarize"}
        )

        assert result.success is False
        assert "Fuzzy search not yet implemented" in result.message


class TestBudgetManagement:
    """Test budget management handlers."""

    @pytest.mark.asyncio
    async def test_upgrade_tier_no_task(self, handlers):
        """Test upgrade without task ID."""
        result = await handlers.upgrade_tier({"new_tier": "$$"})

        assert result.success is False
        assert "No task specified" in result.message

    @pytest.mark.asyncio
    async def test_reset_budget_no_task(self, handlers):
        """Test reset without task ID."""
        result = await handlers.reset_budget({})

        assert result.success is False
        assert "No task specified" in result.message

    @pytest.mark.asyncio
    async def test_upgrade_tier_not_smart_task(self, handlers, mock_client):
        """Test upgrade on non-smart task."""
        mock_client.get_task.return_value = {
            "id": 42,
            "title": "Regular task",
            "description": "No YAML frontmatter here",
        }

        result = await handlers.upgrade_tier({"new_tier": "$$"}, task_id=42)

        assert result.success is False
        assert "not a smart task" in result.message

    @pytest.mark.asyncio
    async def test_upgrade_tier_success(self, handlers, mock_client):
        """Test successful tier upgrade."""
        mock_client.get_task.return_value = {
            "id": 42,
            "title": "Smart task",
            "description": """---
smart_task: true
cost_tier: $
llm_calls_used: 25
llm_calls_limit: 30
---

Some content""",
        }

        result = await handlers.upgrade_tier({"new_tier": "$$"}, task_id=42)

        assert result.success is True
        assert "Upgraded" in result.message
        assert "$ to $$" in result.message
        assert "150 calls" in result.message
        mock_client.update_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_budget_success(self, handlers, mock_client):
        """Test successful budget reset."""
        mock_client.get_task.return_value = {
            "id": 42,
            "title": "Smart task",
            "description": """---
smart_task: true
cost_tier: $
llm_calls_used: 25
llm_calls_limit: 30
total_cost: 0.25
---

Some content""",
        }

        result = await handlers.reset_budget({}, task_id=42)

        assert result.success is True
        assert "Reset" in result.message
        assert "25 calls" in result.message
        assert "$0.25" in result.message
        assert "0/30" in result.message
        mock_client.update_task.assert_called_once()
