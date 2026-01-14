#!/usr/bin/env python3
"""
UAT Script for Smart Tasks Phase 2: Cost Tiers and Metadata Storage

Run against a live Vikunja instance to validate Phase 2 functionality.

Usage:
    # Set environment variables
    export VIKUNJA_API_URL="https://vikunja.factumerit.app/api/v1"
    export VIKUNJA_API_TOKEN="your-bot-token"

    # Run all tests
    python tests/uat_phase2_cost_tiers.py

    # Run specific test
    python tests/uat_phase2_cost_tiers.py --test cost_tier_parsing

Bead: solutions-hgwx.2
"""

import argparse
import asyncio
import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vikunja_mcp.command_parser import CommandParser
from vikunja_mcp.metadata_manager import MetadataManager, SmartTaskMetadata, COST_TIERS
from vikunja_mcp.keyword_handlers import KeywordHandlers
from vikunja_mcp.llm_client import LLMClient


@dataclass
class TestResult:
    """Result of a UAT test."""
    name: str
    passed: bool
    message: str
    duration_ms: float = 0.0


class UATRunner:
    """UAT test runner for Phase 2."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results: list[TestResult] = []
        self.parser = CommandParser()

    def log(self, msg: str):
        if self.verbose:
            print(msg)

    def record(self, name: str, passed: bool, message: str, duration_ms: float = 0.0):
        result = TestResult(name, passed, message, duration_ms)
        self.results.append(result)

        status = "✅ PASS" if passed else "❌ FAIL"
        self.log(f"  {status}: {name}")
        if not passed:
            self.log(f"         {message}")

    # =========================================================================
    # Test: Cost Tier Parsing
    # =========================================================================

    def test_cost_tier_parsing(self):
        """Test that $, $$, $$$ are parsed correctly."""
        self.log("\n📋 Test: Cost Tier Parsing")

        # Test $
        result = self.parser.parse("@eis $ create a project")
        self.record(
            "Parse $ tier",
            result.tier == "tier1" and result.args.get("cost_tier") == "$",
            f"Got tier={result.tier}, cost_tier={result.args.get('cost_tier')}"
        )

        # Test $$
        result = self.parser.parse("@eis $$ analyze something")
        self.record(
            "Parse $$ tier",
            result.tier == "tier1" and result.args.get("cost_tier") == "$$",
            f"Got tier={result.tier}, cost_tier={result.args.get('cost_tier')}"
        )

        # Test $$$
        result = self.parser.parse("@eis $$$ research deeply")
        self.record(
            "Parse $$$ tier",
            result.tier == "tier1" and result.args.get("cost_tier") == "$$$",
            f"Got tier={result.tier}, cost_tier={result.args.get('cost_tier')}"
        )

        # Test Tier 2 with task reference
        result = self.parser.parse("@eis $$ 42 / summarize comments")
        self.record(
            "Parse Tier 2 command",
            result.tier == "tier2" and result.args.get("task_ref") == "42",
            f"Got tier={result.tier}, task_ref={result.args.get('task_ref')}"
        )

        # Test handler assignment
        result = self.parser.parse("@eis $ plan a party")
        self.record(
            "Tier 1 has llm_natural handler",
            result.handler == "llm_natural",
            f"Got handler={result.handler}"
        )

        result = self.parser.parse("@eis $$ 42 / break down")
        self.record(
            "Tier 2 has llm_context handler",
            result.handler == "llm_context",
            f"Got handler={result.handler}"
        )

    # =========================================================================
    # Test: Metadata Manager
    # =========================================================================

    def test_metadata_manager(self):
        """Test YAML frontmatter handling."""
        self.log("\n📋 Test: Metadata Manager")

        # Create metadata
        metadata = MetadataManager.create_initial(
            cost_tier="$$",
            prompt="test prompt",
            keyword="weather",
            schedule="every morning"
        )

        self.record(
            "Create initial metadata",
            metadata.cost_tier == "$$" and metadata.llm_calls_limit == 150,
            f"Got cost_tier={metadata.cost_tier}, limit={metadata.llm_calls_limit}"
        )

        # Format as YAML
        content = "Weather: 72F, sunny"
        formatted = MetadataManager.format(metadata, content)

        self.record(
            "Format includes YAML frontmatter",
            formatted.startswith("---\n") and "smart_task: true" in formatted,
            f"Starts with ---: {formatted.startswith('---')}"
        )

        # Extract metadata back
        extracted, extracted_content = MetadataManager.extract(formatted)

        self.record(
            "Extract metadata from formatted",
            extracted is not None and extracted.cost_tier == "$$",
            f"Extracted cost_tier={extracted.cost_tier if extracted else 'None'}"
        )

        self.record(
            "Extract preserves content",
            "72F" in extracted_content,
            f"Content preserved: {'72F' in extracted_content}"
        )

        # Test non-smart-task is ignored
        regular_desc = "Just a regular description without YAML"
        meta, content = MetadataManager.extract(regular_desc)

        self.record(
            "Non-smart-task returns None",
            meta is None,
            f"Got metadata={meta}"
        )

    # =========================================================================
    # Test: Budget Tracking
    # =========================================================================

    def test_budget_tracking(self):
        """Test budget tracking and enforcement."""
        self.log("\n📋 Test: Budget Tracking")

        # Test tier limits
        self.record(
            "$ tier has 30 call limit",
            COST_TIERS["$"]["max_calls"] == 30,
            f"Got {COST_TIERS['$']['max_calls']}"
        )

        self.record(
            "$$ tier has 150 call limit",
            COST_TIERS["$$"]["max_calls"] == 150,
            f"Got {COST_TIERS['$$']['max_calls']}"
        )

        self.record(
            "$$$ tier has 600 call limit",
            COST_TIERS["$$$"]["max_calls"] == 600,
            f"Got {COST_TIERS['$$$']['max_calls']}"
        )

        # Test increment usage
        metadata = SmartTaskMetadata(cost_tier="$")

        self.record(
            "Initial usage is 0",
            metadata.llm_calls_used == 0,
            f"Got {metadata.llm_calls_used}"
        )

        metadata.increment_usage(5)

        self.record(
            "Increment usage works",
            metadata.llm_calls_used == 5 and metadata.total_cost == 0.05,
            f"Got used={metadata.llm_calls_used}, cost=${metadata.total_cost}"
        )

        # Test budget remaining
        self.record(
            "Budget remaining calculated",
            metadata.budget_remaining == 25,
            f"Got {metadata.budget_remaining}"
        )

        # Test budget exhaustion
        metadata.llm_calls_used = 30

        self.record(
            "Budget exhausted detection",
            metadata.budget_exhausted is True,
            f"Got {metadata.budget_exhausted}"
        )

        # Test increment fails when exhausted
        result = metadata.increment_usage(1)

        self.record(
            "Increment fails when exhausted",
            result is False and metadata.llm_calls_used == 30,
            f"Increment returned {result}, usage={metadata.llm_calls_used}"
        )

        # Test upgrade tier
        metadata.upgrade_tier("$$")

        self.record(
            "Upgrade tier increases limit",
            metadata.llm_calls_limit == 150 and metadata.cost_tier == "$$",
            f"Got limit={metadata.llm_calls_limit}, tier={metadata.cost_tier}"
        )

        # Test reset budget
        metadata.reset_budget()

        self.record(
            "Reset budget clears usage",
            metadata.llm_calls_used == 0 and metadata.total_cost == 0.0,
            f"Got used={metadata.llm_calls_used}, cost=${metadata.total_cost}"
        )

    # =========================================================================
    # Test: LLM Client Stub
    # =========================================================================

    async def test_llm_client_stub(self):
        """Test LLM client stub responses."""
        self.log("\n📋 Test: LLM Client Stub")

        client = LLMClient()

        # Test complete
        response = await client.complete("Create a project", cost_tier="$")

        self.record(
            "LLM complete returns success",
            response.success is True,
            f"Got success={response.success}"
        )

        self.record(
            "LLM complete tracks calls",
            response.calls_used == 1,
            f"Got calls_used={response.calls_used}"
        )

        self.record(
            "LLM complete returns content",
            len(response.content) > 0,
            f"Got {len(response.content)} chars"
        )

        # Test analyze_task
        response = await client.analyze_task(
            task_title="Test Task",
            task_description="Some description",
            instruction="summarize",
            cost_tier="$$"
        )

        self.record(
            "LLM analyze_task works",
            response.success is True,
            f"Got success={response.success}"
        )

    # =========================================================================
    # Test: Budget Management Commands
    # =========================================================================

    def test_budget_commands(self):
        """Test !upgrade and !reset-budget commands."""
        self.log("\n📋 Test: Budget Management Commands")

        # Test !upgrade parsing
        result = self.parser.parse("@eis !upgrade $$")

        self.record(
            "Parse !upgrade command",
            result.handler == "upgrade_tier" and result.args.get("new_tier") == "$$",
            f"Got handler={result.handler}, new_tier={result.args.get('new_tier')}"
        )

        # Test !upgrade $$$
        result = self.parser.parse("@eis !upgrade $$$")

        self.record(
            "Parse !upgrade $$$ command",
            result.args.get("new_tier") == "$$$",
            f"Got new_tier={result.args.get('new_tier')}"
        )

        # Test !reset-budget parsing
        result = self.parser.parse("@eis !reset-budget")

        self.record(
            "Parse !reset-budget command",
            result.handler == "reset_budget",
            f"Got handler={result.handler}"
        )

        # Test !reset alias
        result = self.parser.parse("@eis !reset")

        self.record(
            "Parse !reset alias",
            result.handler == "reset_budget",
            f"Got handler={result.handler}"
        )

    # =========================================================================
    # Test: LLM Handlers
    # =========================================================================

    async def test_llm_handlers(self):
        """Test LLM tier handlers."""
        self.log("\n📋 Test: LLM Handlers")

        # Create handlers with mock client
        from unittest.mock import Mock
        mock_client = Mock()
        mock_client.get_task = Mock(return_value={
            "id": 42,
            "title": "Test Task",
            "description": "Test description",
        })
        mock_client.update_task = Mock()
        mock_client.add_comment = Mock()

        handlers = KeywordHandlers(client=mock_client)

        # Test llm_natural
        result = await handlers.llm_natural(
            {"cost_tier": "$", "prompt": "create a project"},
            task_id=42
        )

        self.record(
            "llm_natural handler succeeds",
            result.success is True,
            f"Got success={result.success}, message={result.message[:50]}..."
        )

        self.record(
            "llm_natural includes cost footer",
            "LLM calls" in result.message,
            f"Cost footer present: {'LLM calls' in result.message}"
        )

        # Test llm_context
        result = await handlers.llm_context(
            {"cost_tier": "$$", "task_ref": "42", "instruction": "summarize"},
            task_id=99
        )

        self.record(
            "llm_context handler succeeds",
            result.success is True,
            f"Got success={result.success}"
        )

        self.record(
            "llm_context references target task",
            "#42" in result.message,
            f"Task reference present: {'#42' in result.message}"
        )

        # Test no prompt error
        result = await handlers.llm_natural({"cost_tier": "$"})

        self.record(
            "llm_natural requires prompt",
            result.success is False and "No prompt" in result.message,
            f"Got success={result.success}"
        )

    # =========================================================================
    # Test: YAML Frontmatter Roundtrip
    # =========================================================================

    def test_yaml_roundtrip(self):
        """Test full YAML frontmatter roundtrip."""
        self.log("\n📋 Test: YAML Frontmatter Roundtrip")

        # Create metadata
        original = SmartTaskMetadata(
            cost_tier="$$",
            keyword="weather",
            prompt="update weather",
            schedule="every morning at 6:30",
            llm_calls_used=15,
        )

        # Format
        content = "Current weather: Sunny, 72F"
        formatted = MetadataManager.format(original, content)

        # Parse back
        parsed, parsed_content = MetadataManager.extract(formatted)

        self.record(
            "Roundtrip preserves cost_tier",
            parsed.cost_tier == original.cost_tier,
            f"Got {parsed.cost_tier}, expected {original.cost_tier}"
        )

        self.record(
            "Roundtrip preserves keyword",
            parsed.keyword == original.keyword,
            f"Got {parsed.keyword}, expected {original.keyword}"
        )

        self.record(
            "Roundtrip preserves llm_calls_used",
            parsed.llm_calls_used == original.llm_calls_used,
            f"Got {parsed.llm_calls_used}, expected {original.llm_calls_used}"
        )

        self.record(
            "Roundtrip preserves schedule",
            parsed.schedule == original.schedule,
            f"Got {parsed.schedule}, expected {original.schedule}"
        )

        self.record(
            "Roundtrip preserves content",
            "Sunny, 72F" in parsed_content,
            f"Content preserved: {'Sunny' in parsed_content}"
        )

    # =========================================================================
    # Test: Budget Warning Messages
    # =========================================================================

    def test_budget_warnings(self):
        """Test budget warning message formatting."""
        self.log("\n📋 Test: Budget Warning Messages")

        # Near exhaustion (80%)
        metadata = SmartTaskMetadata(
            cost_tier="$",
            llm_calls_used=24,
            llm_calls_limit=30,
        )

        footer = MetadataManager.format_cost_footer(metadata)

        self.record(
            "Cost footer shows usage",
            "24/30" in footer,
            f"Usage shown: {'24/30' in footer}"
        )

        self.record(
            "Cost footer warns when 80%+ used",
            "6 calls remaining" in footer,
            f"Warning shown: {'remaining' in footer}"
        )

        # Exhausted
        metadata.llm_calls_used = 30
        metadata.total_cost = 0.30

        warning = MetadataManager.format_budget_warning(metadata)

        self.record(
            "Budget warning shows exhausted",
            "Budget exhausted" in warning,
            f"Exhausted shown: {'exhausted' in warning}"
        )

        self.record(
            "Budget warning shows upgrade option",
            "!upgrade" in warning,
            f"Upgrade shown: {'!upgrade' in warning}"
        )

        self.record(
            "Budget warning shows reset option",
            "!reset-budget" in warning,
            f"Reset shown: {'!reset-budget' in warning}"
        )

    # =========================================================================
    # Run All Tests
    # =========================================================================

    async def run_all(self):
        """Run all UAT tests."""
        self.log("=" * 60)
        self.log("UAT: Smart Tasks Phase 2 - Cost Tiers and Metadata Storage")
        self.log("=" * 60)

        start = time.time()

        # Sync tests
        self.test_cost_tier_parsing()
        self.test_metadata_manager()
        self.test_budget_tracking()
        self.test_budget_commands()
        self.test_yaml_roundtrip()
        self.test_budget_warnings()

        # Async tests
        await self.test_llm_client_stub()
        await self.test_llm_handlers()

        duration = (time.time() - start) * 1000

        # Summary
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)

        self.log("\n" + "=" * 60)
        self.log(f"Results: {passed} passed, {failed} failed ({duration:.0f}ms)")
        self.log("=" * 60)

        if failed > 0:
            self.log("\nFailed tests:")
            for r in self.results:
                if not r.passed:
                    self.log(f"  ❌ {r.name}: {r.message}")

        return failed == 0


def main():
    parser = argparse.ArgumentParser(description="UAT for Smart Tasks Phase 2")
    parser.add_argument("--test", help="Run specific test (e.g., cost_tier_parsing)")
    parser.add_argument("--quiet", action="store_true", help="Less verbose output")
    args = parser.parse_args()

    runner = UATRunner(verbose=not args.quiet)

    if args.test:
        # Run specific test
        test_method = getattr(runner, f"test_{args.test}", None)
        if test_method is None:
            print(f"Unknown test: {args.test}")
            print("Available tests:")
            for name in dir(runner):
                if name.startswith("test_"):
                    print(f"  - {name[5:]}")
            sys.exit(1)

        if asyncio.iscoroutinefunction(test_method):
            asyncio.run(test_method())
        else:
            test_method()

        passed = all(r.passed for r in runner.results)
    else:
        # Run all tests
        passed = asyncio.run(runner.run_all())

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
