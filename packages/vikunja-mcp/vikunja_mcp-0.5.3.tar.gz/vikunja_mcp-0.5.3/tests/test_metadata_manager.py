"""
Tests for Smart Task Metadata Manager.

Bead: solutions-hgwx.2
"""

import pytest
from vikunja_mcp.metadata_manager import (
    MetadataManager,
    SmartTaskMetadata,
    COST_TIERS,
)


class TestSmartTaskMetadata:
    """Test SmartTaskMetadata dataclass."""

    def test_default_values(self):
        """Test default metadata values."""
        metadata = SmartTaskMetadata()

        assert metadata.smart_task is True
        assert metadata.cost_tier == "$"
        assert metadata.llm_calls_used == 0
        assert metadata.llm_calls_limit == 30  # $ tier default
        assert metadata.total_cost == 0.0

    def test_tier_defaults(self):
        """Test that tier sets correct limits."""
        meta_cheap = SmartTaskMetadata(cost_tier="$")
        meta_medium = SmartTaskMetadata(cost_tier="$$")
        meta_expensive = SmartTaskMetadata(cost_tier="$$$")

        assert meta_cheap.llm_calls_limit == 30
        assert meta_medium.llm_calls_limit == 150
        assert meta_expensive.llm_calls_limit == 600

    def test_budget_remaining(self):
        """Test budget_remaining property."""
        metadata = SmartTaskMetadata(cost_tier="$", llm_calls_used=10)

        assert metadata.budget_remaining == 20
        assert not metadata.budget_exhausted

    def test_budget_exhausted(self):
        """Test budget_exhausted property."""
        metadata = SmartTaskMetadata(cost_tier="$", llm_calls_used=30)

        assert metadata.budget_remaining == 0
        assert metadata.budget_exhausted

    def test_budget_percent_used(self):
        """Test budget_percent_used property."""
        metadata = SmartTaskMetadata(cost_tier="$", llm_calls_used=15)

        assert metadata.budget_percent_used == 50.0

    def test_increment_usage_success(self):
        """Test successful usage increment."""
        metadata = SmartTaskMetadata(cost_tier="$")

        assert metadata.increment_usage(1)
        assert metadata.llm_calls_used == 1
        assert metadata.total_cost == 0.01

    def test_increment_usage_multiple(self):
        """Test incrementing multiple calls."""
        metadata = SmartTaskMetadata(cost_tier="$")

        assert metadata.increment_usage(5)
        assert metadata.llm_calls_used == 5
        assert metadata.total_cost == 0.05

    def test_increment_usage_exceeds_budget(self):
        """Test that incrementing beyond budget fails."""
        metadata = SmartTaskMetadata(cost_tier="$", llm_calls_used=29)

        # Can add 1 more
        assert metadata.increment_usage(1)
        assert metadata.llm_calls_used == 30

        # Cannot add more
        assert not metadata.increment_usage(1)
        assert metadata.llm_calls_used == 30  # Unchanged

    def test_upgrade_tier(self):
        """Test upgrading to higher tier."""
        metadata = SmartTaskMetadata(cost_tier="$", llm_calls_used=25)

        assert metadata.upgrade_tier("$$")
        assert metadata.cost_tier == "$$"
        assert metadata.llm_calls_limit == 150
        # Usage preserved
        assert metadata.llm_calls_used == 25

    def test_upgrade_tier_invalid(self):
        """Test upgrading to invalid tier fails."""
        metadata = SmartTaskMetadata(cost_tier="$")

        assert not metadata.upgrade_tier("$$$$")  # Invalid
        assert metadata.cost_tier == "$"  # Unchanged

    def test_reset_budget(self):
        """Test resetting budget counter."""
        metadata = SmartTaskMetadata(
            cost_tier="$",
            llm_calls_used=25,
            total_cost=0.25
        )

        metadata.reset_budget()

        assert metadata.llm_calls_used == 0
        assert metadata.total_cost == 0.0
        assert metadata.llm_calls_limit == 30  # Limit preserved

    def test_to_dict(self):
        """Test serialization to dict."""
        metadata = SmartTaskMetadata(
            cost_tier="$$",
            keyword="weather",
            prompt="update weather",
            llm_calls_used=5,
        )

        data = metadata.to_dict()

        assert data["smart_task"] is True
        assert data["cost_tier"] == "$$"
        assert data["keyword"] == "weather"
        assert data["prompt"] == "update weather"
        assert data["llm_calls_used"] == 5

    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "smart_task": True,
            "cost_tier": "$$$",
            "keyword": "stock",
            "llm_calls_used": 100,
            "llm_calls_limit": 600,
            "total_cost": 1.00,
        }

        metadata = SmartTaskMetadata.from_dict(data)

        assert metadata.cost_tier == "$$$"
        assert metadata.keyword == "stock"
        assert metadata.llm_calls_used == 100
        assert metadata.llm_calls_limit == 600


class TestMetadataManager:
    """Test MetadataManager static methods."""

    def test_extract_no_frontmatter(self):
        """Test extracting from description without frontmatter."""
        description = "Just a regular task description."

        metadata, content = MetadataManager.extract(description)

        assert metadata is None
        assert content == description

    def test_extract_empty(self):
        """Test extracting from empty description."""
        metadata, content = MetadataManager.extract("")

        assert metadata is None
        assert content == ""

    def test_extract_with_frontmatter(self):
        """Test extracting YAML frontmatter."""
        description = """---
smart_task: true
cost_tier: $$
llm_calls_used: 5
llm_calls_limit: 150
---

Weather update content here."""

        metadata, content = MetadataManager.extract(description)

        assert metadata is not None
        assert metadata.cost_tier == "$$"
        assert metadata.llm_calls_used == 5
        assert "Weather update" in content

    def test_extract_non_smart_task(self):
        """Test that non-smart-task frontmatter is ignored."""
        description = """---
some_key: value
---

Regular content."""

        metadata, content = MetadataManager.extract(description)

        # No smart_task: true, so returns None
        assert metadata is None
        assert content == description

    def test_format(self):
        """Test formatting metadata + content."""
        metadata = SmartTaskMetadata(
            cost_tier="$",
            keyword="weather",
        )
        content = "Weather: 72F, sunny"

        result = MetadataManager.format(metadata, content)

        assert result.startswith("---\n")
        assert "smart_task: true" in result
        assert "cost_tier:" in result and "$" in result  # YAML may or may not quote
        assert "Weather: 72F, sunny" in result

    def test_roundtrip(self):
        """Test extract -> modify -> format roundtrip."""
        original = """---
smart_task: true
cost_tier: $
llm_calls_used: 5
llm_calls_limit: 30
---

Original content."""

        # Extract
        metadata, content = MetadataManager.extract(original)
        assert metadata is not None

        # Modify
        metadata.increment_usage(1)

        # Format
        result = MetadataManager.format(metadata, content)

        # Re-extract
        metadata2, content2 = MetadataManager.extract(result)
        assert metadata2.llm_calls_used == 6
        assert "Original content" in content2

    def test_create_initial(self):
        """Test creating initial metadata."""
        metadata = MetadataManager.create_initial(
            cost_tier="$$",
            prompt="Create a project",
            keyword="project",
            schedule="weekly",
        )

        assert metadata.smart_task is True
        assert metadata.cost_tier == "$$"
        assert metadata.prompt == "Create a project"
        assert metadata.keyword == "project"
        assert metadata.schedule == "weekly"
        assert metadata.llm_calls_limit == 150
        assert metadata.llm_calls_used == 0
        assert metadata.created_at is not None

    def test_format_budget_warning(self):
        """Test budget warning message."""
        metadata = SmartTaskMetadata(
            cost_tier="$",
            llm_calls_used=30,
            llm_calls_limit=30,
            total_cost=0.30,
        )

        warning = MetadataManager.format_budget_warning(metadata)

        assert "Budget exhausted" in warning
        assert "30/30" in warning
        assert "$0.30" in warning
        assert "!upgrade" in warning
        assert "!reset-budget" in warning

    def test_format_cost_footer(self):
        """Test cost footer formatting."""
        metadata = SmartTaskMetadata(
            cost_tier="$",
            llm_calls_used=24,
            llm_calls_limit=30,
            total_cost=0.24,
        )

        footer = MetadataManager.format_cost_footer(metadata)

        assert "24/30" in footer
        assert "$0.24" in footer
        # 80% used, should show warning
        assert "6 calls remaining" in footer


class TestCostTiers:
    """Test cost tier configuration."""

    def test_tier_config_exists(self):
        """Test that all tiers are configured."""
        assert "$" in COST_TIERS
        assert "$$" in COST_TIERS
        assert "$$$" in COST_TIERS

    def test_tier_values(self):
        """Test tier configuration values."""
        assert COST_TIERS["$"]["max_calls"] == 30
        assert COST_TIERS["$$"]["max_calls"] == 150
        assert COST_TIERS["$$$"]["max_calls"] == 600

        # All have same cost per call
        for tier in COST_TIERS.values():
            assert tier["cost_per_call"] == 0.01


class TestHTMLMetadata:
    """Test HTML comment metadata format."""

    def test_format_html(self):
        """Test formatting metadata as plaintext code."""
        metadata = SmartTaskMetadata(
            cost_tier="$$",
            llm_calls_used=5,
            llm_calls_limit=150,
        )
        html_content = "<p>Hello world</p>"

        result = MetadataManager.format_html(metadata, html_content)

        assert "<p>Hello world</p>" in result
        assert "[eis:$$:5/150]" in result
        assert "<small>" in result

    def test_extract_html(self):
        """Test extracting metadata from HTML comment."""
        description = '''<!-- eis-meta: {"smart_task":true,"cost_tier":"$","llm_calls_used":3,"llm_calls_limit":30,"total_cost":0.03} -->
<p>Task content here</p>'''

        metadata, content = MetadataManager.extract(description)

        assert metadata is not None
        assert metadata.smart_task is True
        assert metadata.cost_tier == "$"
        assert metadata.llm_calls_used == 3
        assert "<p>Task content here</p>" in content

    def test_html_roundtrip(self):
        """Test format_html -> extract roundtrip."""
        original_metadata = SmartTaskMetadata(
            cost_tier="$$$",
            llm_calls_used=10,
            llm_calls_limit=600,
            total_cost=0.10,
        )
        html_content = "<h1>Title</h1><p>Content</p>"

        # Format
        formatted = MetadataManager.format_html(original_metadata, html_content)

        # Extract
        extracted_metadata, extracted_content = MetadataManager.extract(formatted)

        assert extracted_metadata is not None
        assert extracted_metadata.cost_tier == "$$$"
        assert extracted_metadata.llm_calls_used == 10
        assert "<h1>Title</h1>" in extracted_content
        assert "<p>Content</p>" in extracted_content
