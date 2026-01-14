"""
Command Parser for @eis Smart Tasks.

3-tier command parsing:
- Tier 1: LLM Natural Language ($, $$, $$$) - Phase 2
- Tier 2: LLM + Context (task reference + instruction) - Phase 2
- Tier 3: Deterministic Commands (!complete, !remind, !weather) - Phase 1

Based on: docs/factumerit/101-SMART_TASKS_IMPLEMENTATION.md
Bead: solutions-pbja, solutions-hgwx.1
"""

import os
import re
from dataclasses import dataclass
from typing import Optional

from rapidfuzz import process, fuzz

from .command_registry import TIER3_COMMANDS
from .config import is_llm_enabled


@dataclass
class ParseResult:
    """Result of parsing an @eis command."""
    tier: str  # "tier1", "tier2", "tier3", "unknown"
    handler: Optional[str] = None
    args: Optional[dict] = None
    matched_command: Optional[str] = None
    confidence: float = 0.0
    error: Optional[str] = None


# Sub-daily schedule keywords (daily+ uses Vikunja's "every day" syntax)
SUB_DAILY_SCHEDULES = {'hourly', '1h', '2h', '4h', '6h', '12h'}


def _extract_schedule(text: str) -> tuple[str, Optional[str]]:
    """Extract sub-daily schedule keyword from end of text.

    For daily+ intervals, use Vikunja's native "every day" syntax instead.

    Args:
        text: Input text like "Seattle hourly" or "url 6h"

    Returns:
        Tuple of (remaining_text, schedule or None)
    """
    words = text.strip().split()
    if words and words[-1].lower() in SUB_DAILY_SCHEDULES:
        schedule = words[-1].lower()
        remaining = " ".join(words[:-1])
        return remaining, schedule
    return text, None


def _extract_target_project(text: str) -> tuple[str, Optional[str]]:
    """Extract target project from text using | syntax.

    Note: +Project is handled by Vikunja's Quick Add Magic, not @eis.
    We only handle | for backwards compatibility.

    Args:
        text: Input text like "Seattle | Dashboard"

    Returns:
        Tuple of (remaining_text, target_project or None)
    """
    # Check for | Project syntax (legacy, prefer Vikunja's +Project)
    if "|" in text:
        args_part, target_part = text.rsplit("|", 1)
        return args_part.strip(), target_part.strip()

    return text, None


class CommandParser:
    """3-tier command parsing for @eis Smart Tasks.

    Usage:
        parser = CommandParser()
        result = parser.parse("@eis !complete 42")

        if result.tier == "tier3":
            handler = getattr(keyword_handlers, result.handler)
            await handler(result.args)
    """

    # Tier 3 commands are auto-generated from command_registry.py
    TIER3_COMMANDS = TIER3_COMMANDS

    def __init__(self, fuzzy_threshold: int = 70):
        """Initialize parser.

        Args:
            fuzzy_threshold: Minimum score for fuzzy command matching (0-100)
        """
        self.fuzzy_threshold = fuzzy_threshold

    def parse(self, text: str, implicit_mention: bool = False) -> ParseResult:
        """Parse command from text.

        Args:
            text: Task title, description, or comment
            implicit_mention: If True, skip the @mention check (for task.assigned notifications)

        Returns:
            ParseResult with tier, handler, args, and confidence

        Examples:
            >>> parser.parse("@eis !complete 42")
            ParseResult(tier="tier3", handler="complete_task", args={"task_ids": [42]})

            >>> parser.parse("!complete 42", implicit_mention=True)
            ParseResult(tier="tier3", handler="complete_task", args={"task_ids": [42]})

            >>> parser.parse("$ plan a birthday party", implicit_mention=True)
            ParseResult(tier="tier1", error="LLM tier not yet implemented")

            >>> parser.parse("Buy milk")
            ParseResult(tier="unknown", error="No @mention found")
        """
        if not text:
            return ParseResult(tier="unknown", error="Empty text")

        # Normalize aliases: @e → @eis
        text = self._normalize_aliases(text)

        if implicit_mention:
            # For task.assigned notifications, the command is the full text
            command_text = text.strip()
        else:
            # Check for @eis mention
            if "@eis" not in text.lower():
                return ParseResult(tier="unknown", error="No @mention found")

            # Extract text after @eis
            eis_match = re.search(r'@eis\s*(.*)', text, re.IGNORECASE)
            if not eis_match:
                return ParseResult(tier="unknown", error="Could not extract command after @mention")

            command_text = eis_match.group(1).strip()

        if not command_text:
            return ParseResult(tier="unknown", error="No command found")

        # Tier 3: Direct commands (starts with !)
        if command_text.startswith("!"):
            return self._parse_tier3(command_text)

        # Tier 1/2: LLM tiers (starts with $)
        if command_text.startswith("$"):
            if not is_llm_enabled():
                return ParseResult(
                    tier="disabled",
                    error="AI features coming soon. Use !help to see available commands."
                )
            return self._parse_llm_tier(command_text)

        # Natural language - try fuzzy matching to ! commands first
        fuzzy_result = self._fuzzy_match_natural_language(command_text)
        if fuzzy_result:
            return fuzzy_result

        # If LLM disabled and no fuzzy match, return helpful error
        if not is_llm_enabled():
            return ParseResult(
                tier="disabled",
                error="Try a ! command like !help, !w Seattle, or !list"
            )

        # LLM enabled: Natural language → tool-calling loop
        return ParseResult(
            tier="tier_natural",
            handler="llm_tools",
            args={"prompt": command_text},
            confidence=0.8  # Lower confidence for natural language
        )

    def _normalize_aliases(self, text: str) -> str:
        """Normalize @e → @eis and other aliases."""
        # @e followed by space, !, or $
        text = re.sub(r'@e\s+', '@eis ', text)
        text = re.sub(r'@e!', '@eis !', text)
        text = re.sub(r'@e\$', '@eis $', text)
        return text

    # Natural language patterns that map to ! commands when LLM is disabled
    # Format: (regex_pattern, command, arg_extractor)
    NATURAL_LANGUAGE_PATTERNS = [
        # Weather - various phrasings
        (r"weather\s+(?:in\s+)?(.+)", "!w", lambda m: m.group(1)),
        (r"what(?:'s|\s+is)\s+(?:the\s+)?weather\s+(?:in\s+|like\s+in\s+)?(.+)?", "!w", lambda m: m.group(1) or ""),
        (r"forecast\s+(?:for\s+)?(.+)?", "!w", lambda m: m.group(1) or ""),
        (r"how(?:'s|\s+is)\s+(?:the\s+)?weather\s+(?:in\s+)?(.+)?", "!w", lambda m: m.group(1) or ""),
        # Help
        (r"help(?:\s+me)?$", "!help", lambda m: ""),
        (r"what\s+can\s+you\s+do", "!help", lambda m: ""),
        (r"commands?$", "!help", lambda m: ""),
        # Note: !list, !s (stock) not implemented yet - see bead fa-ehfl
    ]

    def _fuzzy_match_natural_language(self, text: str) -> Optional[ParseResult]:
        """Try to match natural language to a ! command.

        This provides a graceful fallback when LLM is disabled,
        allowing common phrases like "weather in Seattle" to work.

        Returns:
            ParseResult if matched, None otherwise
        """
        text_lower = text.lower().strip()

        for pattern, command, extract_args in self.NATURAL_LANGUAGE_PATTERNS:
            match = re.match(pattern, text_lower, re.IGNORECASE)
            if match:
                args_text = extract_args(match).strip() if extract_args else ""
                # Parse as if it were the ! command
                return self._parse_tier3(f"{command} {args_text}".strip())

        return None

    def _parse_tier3(self, text: str) -> ParseResult:
        """Parse Tier 3 direct commands with fuzzy matching.

        Args:
            text: Text starting with ! (e.g., "!complete 42")
        """
        # Extract command word
        parts = text.split(maxsplit=1)
        command_word = parts[0].lower()
        args_text = parts[1] if len(parts) > 1 else ""

        # Try exact match first
        if command_word in self.TIER3_COMMANDS:
            handler = self.TIER3_COMMANDS[command_word]
            return ParseResult(
                tier="tier3",
                handler=handler,
                args=self._extract_args(handler, args_text),
                matched_command=command_word,
                confidence=1.0
            )

        # Fuzzy match
        match_result = process.extractOne(
            command_word,
            self.TIER3_COMMANDS.keys(),
            scorer=fuzz.ratio
        )

        if match_result and match_result[1] >= self.fuzzy_threshold:
            matched_cmd = match_result[0]
            score = match_result[1]
            handler = self.TIER3_COMMANDS[matched_cmd]

            return ParseResult(
                tier="tier3",
                handler=handler,
                args=self._extract_args(handler, args_text),
                matched_command=matched_cmd,
                confidence=score / 100.0
            )

        # No match
        return ParseResult(
            tier="unknown",
            error=f"Unknown command: {command_word}"
        )

    def _parse_llm_tier(self, text: str) -> ParseResult:
        """Parse LLM tier commands ($ / $$ / $$$).

        Tier 1: Pure natural language (e.g., "$ create a sourdough project")
        Tier 2: LLM + context (e.g., "$ 42 / summarize comments")
        """
        # Count $ symbols to determine tier
        if text.startswith("$$$"):
            tier_cost = "$$$"
        elif text.startswith("$$"):
            tier_cost = "$$"
        else:
            tier_cost = "$"

        # Check for task reference (Tier 2)
        remaining = text[len(tier_cost):].strip()

        # Tier 2 pattern: task-ref followed by separator (/, ,, :)
        tier2_pattern = r'^(\d+|"[^"]+"|\'[^\']+\')\s*[/,:](.*)$'
        tier2_match = re.match(tier2_pattern, remaining)

        if tier2_match:
            return ParseResult(
                tier="tier2",
                handler="llm_context",
                args={
                    "cost_tier": tier_cost,
                    "task_ref": tier2_match.group(1).strip('"\''),
                    "instruction": tier2_match.group(2).strip()
                },
                confidence=1.0,
            )

        # Tier 1: Pure natural language
        return ParseResult(
            tier="tier1",
            handler="llm_natural",
            args={
                "cost_tier": tier_cost,
                "prompt": remaining
            },
            confidence=1.0,
        )

    def _extract_args(self, handler: str, args_text: str) -> dict:
        """Extract arguments for specific handlers."""

        if handler == "complete_task":
            # Extract task IDs: "42", "1,2,3", "1 2 3"
            task_ids = [int(x) for x in re.findall(r'\d+', args_text)]
            return {"task_ids": task_ids} if task_ids else {}

        elif handler == "set_reminder":
            # Parse "42 / tomorrow at 3pm"
            if "/" in args_text:
                task_part, when_part = args_text.split("/", 1)
                task_id_match = re.search(r'\d+', task_part)
                return {
                    "task_id": int(task_id_match.group()) if task_id_match else None,
                    "when": when_part.strip()
                }
            # Just task ID without time
            task_id_match = re.search(r'\d+', args_text)
            return {"task_id": int(task_id_match.group())} if task_id_match else {}

        elif handler == "weather_handler":
            # Parse "location hourly" or "location | project" (legacy)
            # Examples:
            #   "Seattle" -> location only
            #   "Seattle hourly" -> location + sub-daily schedule
            #   "Seattle | Inbox" -> location + target project (legacy, prefer +Inbox)
            # Note: For daily+, use Vikunja's "every day +Project" syntax
            result = {}

            # Extract target project (| syntax for backwards compat)
            args_text, target = _extract_target_project(args_text)
            if target:
                result["target_project"] = target

            # Extract sub-daily schedule (hourly, 6h, etc.)
            args_text, schedule = _extract_schedule(args_text)
            if schedule:
                result["schedule"] = schedule

            result["location"] = args_text.strip() or None
            return result

        elif handler == "stock_handler":
            # Parse "AAPL hourly" or "AAPL | project" (legacy)
            # Examples:
            #   "AAPL" -> ticker only
            #   "AAPL 4h" -> ticker + sub-daily schedule
            #   "AAPL | Investments" -> ticker + target project (legacy)
            result = {}

            # Extract target project (| syntax for backwards compat)
            args_text, target = _extract_target_project(args_text)
            if target:
                result["target_project"] = target

            # Extract sub-daily schedule (hourly, 6h, etc.)
            args_text, schedule = _extract_schedule(args_text)
            if schedule:
                result["schedule"] = schedule

            result["ticker"] = args_text.strip().upper() or None
            return result

        elif handler == "upgrade_tier":
            # Parse "$$" or "$$$" - the new tier to upgrade to
            tier = args_text.strip()
            if tier in ("$", "$$", "$$$"):
                return {"new_tier": tier}
            return {"new_tier": "$$"}  # Default to $$

        elif handler == "reset_budget":
            # No args needed
            return {}

        elif handler == "balance_handler":
            # No args needed
            return {}

        elif handler == "grant_credit":
            # Parse flexibly: "!grant $5", "!grant $10 ivan", "!grant ivan $10", "!grant ivan 10"
            parts = args_text.strip().split()
            result = {}
            amount_part = None
            user_part = None

            for part in parts:
                # Check if this part looks like an amount (has digits, optional $ and decimal)
                if re.match(r'^\$?\d+(?:\.\d{1,2})?$', part):
                    amount_part = part
                else:
                    user_part = part

            if amount_part:
                result["amount"] = amount_part
            if user_part:
                result["target_user"] = user_part
            return result

        elif handler == "model_handler":
            # Model name is everything after !model
            return {"model": args_text.strip()}

        elif handler == "help_handler":
            # Topic is everything after !help
            return {"topic": args_text.strip()}

        elif handler == "news_handler":
            # Parse "query | project" or "query +project" or just query
            result = {}

            # Extract target project (| or + syntax)
            args_text, target = _extract_target_project(args_text)
            if target:
                result["target_project"] = target

            if not args_text:
                return result

            # Check for category prefix (e.g., "category:technology" or "cat:sports")
            if args_text.lower().startswith(("category:", "cat:")):
                category = args_text.split(":", 1)[1].strip()
                result["category"] = category
            else:
                # Otherwise treat as search query
                result["query"] = args_text

            return result

        elif handler == "rss_handler":
            # Parse "url 6h" or "url | project" (legacy)
            # Examples:
            #   "https://example.com/feed.xml" -> url only
            #   "https://example.com/feed.xml 6h" -> url + sub-daily schedule
            #   "https://example.com/feed.xml | Reading" -> url + target project (legacy)
            # Note: For daily+, use Vikunja's "every day +Project" syntax
            result = {}

            # Extract target project (| syntax for backwards compat)
            args_text, target = _extract_target_project(args_text)
            if target:
                result["target_project"] = target

            # Extract sub-daily schedule (hourly, 6h, etc.)
            args_text, schedule = _extract_schedule(args_text)
            if schedule:
                result["schedule"] = schedule

            result["url"] = args_text.strip()
            return result

        elif handler == "cheatsheet_handler":
            # No args needed for cheatsheet
            return {}

        elif handler == "ears_handler":
            # Parse "on" or "off" (default to "on" if just !ears)
            action = args_text.strip().lower()
            if action in ("on", "off"):
                return {"action": action}
            return {"action": "on"}  # Default to "on" - !ears means turn on

        elif handler == "project_handler":
            # Parse project commands with natural "to" syntax:
            #   "add <name> to <parent>" or "add <name>" (top-level)
            #   "delete <name>"
            #   "rename <old> to <new>"
            # Fallback: | and -> syntax still supported
            result = {}
            parts = args_text.strip().split(maxsplit=1)
            if not parts:
                return result

            action = parts[0].lower()
            remaining = parts[1] if len(parts) > 1 else ""
            result["action"] = action

            if action == "add":
                # Try "to" syntax first: "add X to Y"
                # The part after "to" should match an existing project
                if " to " in remaining.lower():
                    # Mark for handler to do greedy right-match on " to "
                    result["raw"] = remaining
                    result["use_to_syntax"] = True
                else:
                    # Fallback: | syntax
                    remaining, parent = _extract_target_project(remaining)
                    result["name"] = remaining.strip()
                    if parent:
                        result["parent"] = parent

            elif action == "delete":
                result["name"] = remaining.strip()

            elif action == "rename":
                # Try "to" syntax first: "rename X to Y"
                # The part before "to" should match an existing project
                if " to " in remaining.lower():
                    # Mark for handler to do greedy left-match on " to "
                    result["raw"] = remaining
                    result["use_to_syntax"] = True
                # Fallback: -> or → syntax
                elif " -> " in remaining:
                    old, new = remaining.split(" -> ", 1)
                    result["name"] = old.strip()
                    result["new_name"] = new.strip()
                elif " → " in remaining:
                    old, new = remaining.split(" → ", 1)
                    result["name"] = old.strip()
                    result["new_name"] = new.strip()

            return result

        elif handler == "delete_handler":
            # Parse delete commands:
            #   !delete → delete current task
            #   !delete all → delete all in project
            #   !delete 42 → delete specific task
            #   !delete 1 2 3 → delete multiple tasks
            #   !delete done → delete completed tasks
            #   !delete <criteria> → LLM-based (future)
            result = {}
            text = args_text.strip()

            if not text:
                # No args = delete current task
                return result

            # Check for multiple numeric IDs
            task_ids = [int(x) for x in re.findall(r'\d+', text)]
            if task_ids and len(task_ids) > 1:
                # Multiple IDs: "1 2 3" or "1, 2, 3"
                result["task_ids"] = task_ids
                return result

            # Single target (could be "all", "done", ID, or criteria)
            result["target"] = text
            return result

        elif handler == "share_handler":
            # Parse optional project name:
            #   !share → share current project
            #   !share Dashboard → share "Dashboard" project
            return {"project_name": args_text.strip() if args_text.strip() else ""}

        return {}
