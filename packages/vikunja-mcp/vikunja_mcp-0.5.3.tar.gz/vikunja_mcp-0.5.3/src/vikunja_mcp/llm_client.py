"""
LLM Client for @eis Smart Tasks.

Stub implementation for Phase 2. Actual LLM integration in Phase 3+.

This module provides a unified interface for LLM calls with:
- Cost tier enforcement
- Token counting
- Response formatting (haiku default)

Based on: docs/factumerit/083-SMART_TASKS_DESIGN.md
Bead: solutions-hgwx.2
"""

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM call."""

    content: str
    success: bool
    calls_used: int = 1  # Number of LLM calls consumed
    error: Optional[str] = None

    # Token usage (for cost tracking)
    input_tokens: int = 0
    output_tokens: int = 0


class LLMClient:
    """Client for LLM calls with cost tier enforcement.

    Phase 2: Stub implementation that returns placeholder responses.
    Phase 3+: Will integrate with actual LLM (Claude, OpenAI, etc.)

    Usage:
        client = LLMClient()
        response = await client.complete("Create a sourdough project", cost_tier="$")

        if response.success:
            print(response.content)
        else:
            print(f"Error: {response.error}")
    """

    # Cost tier limits (calls per request)
    TIER_LIMITS = {
        "$": 1,    # Single LLM call
        "$$": 5,   # Up to 5 calls (multi-step reasoning)
        "$$$": 20, # Up to 20 calls (research, complex tasks)
    }

    def __init__(self):
        """Initialize LLM client."""
        self._stub_mode = True  # Phase 2: always stub

    async def complete(
        self,
        prompt: str,
        cost_tier: str = "$",
        output_format: str = "haiku",
        context: Optional[str] = None,
    ) -> LLMResponse:
        """Complete a prompt using LLM.

        Args:
            prompt: User prompt
            cost_tier: Cost tier ("$", "$$", "$$$")
            output_format: Output format ("haiku", "prose", "structured")
            context: Optional context (e.g., task description for Tier 2)

        Returns:
            LLMResponse with content or error
        """
        if self._stub_mode:
            return self._stub_response(prompt, cost_tier, output_format, context)

        # Phase 3+: Actual LLM integration goes here
        raise NotImplementedError("LLM integration not yet implemented")

    async def analyze_task(
        self,
        task_title: str,
        task_description: str,
        instruction: str,
        cost_tier: str = "$$",
    ) -> LLMResponse:
        """Analyze an existing task (Tier 2 command).

        Args:
            task_title: Task title
            task_description: Task description
            instruction: User instruction (e.g., "break into subtasks")
            cost_tier: Cost tier

        Returns:
            LLMResponse with analysis
        """
        context = f"Task: {task_title}\n\nDescription:\n{task_description}"
        return await self.complete(instruction, cost_tier, context=context)

    async def format_data(
        self,
        data: dict,
        format_instruction: str,
        cost_tier: str = "$",
    ) -> LLMResponse:
        """Format raw data using LLM (e.g., weather, stock data).

        Args:
            data: Raw data dict
            format_instruction: How to format (e.g., "friendly weather summary")
            cost_tier: Cost tier

        Returns:
            LLMResponse with formatted content
        """
        prompt = f"{format_instruction}\n\nData:\n{data}"
        return await self.complete(prompt, cost_tier, output_format="prose")

    def _stub_response(
        self,
        prompt: str,
        cost_tier: str,
        output_format: str,
        context: Optional[str],
    ) -> LLMResponse:
        """Generate stub response for Phase 2.

        Returns placeholder that indicates LLM would be called here.
        """
        tier_label = {
            "$": "simple",
            "$$": "moderate",
            "$$$": "complex",
        }.get(cost_tier, "simple")

        # Generate a placeholder response
        if output_format == "haiku":
            content = (
                f"*[LLM placeholder - {tier_label} task]*\n\n"
                f"Prompt received well,\n"
                f"Processing waits for Phase 3,\n"
                f"Answers coming soon.\n\n"
                f"---\n"
                f"*Original prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}*"
            )
        else:
            content = (
                f"**[LLM Placeholder - {tier_label.title()} Task]**\n\n"
                f"This is where the LLM response would appear.\n\n"
                f"**Prompt:** {prompt}\n\n"
                f"**Cost Tier:** {cost_tier}\n"
                f"**Max Calls:** {self.TIER_LIMITS.get(cost_tier, 1)}\n\n"
                f"*LLM integration coming in Phase 3.*"
            )

        if context:
            content += f"\n\n**Context provided:** {len(context)} chars"

        logger.info(f"LLM stub called: tier={cost_tier}, prompt_len={len(prompt)}")

        return LLMResponse(
            content=content,
            success=True,
            calls_used=1,
            input_tokens=len(prompt.split()),  # Rough estimate
            output_tokens=len(content.split()),
        )


# Singleton instance
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get the LLM client singleton."""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
