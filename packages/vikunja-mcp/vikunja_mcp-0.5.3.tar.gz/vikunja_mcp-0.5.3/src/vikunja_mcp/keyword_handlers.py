"""
Keyword Handlers for @eis Smart Tasks.

Tier 1/2: LLM-backed handlers with cost tracking
Tier 3: Deterministic command handlers (FREE, no LLM)

Based on: docs/factumerit/101-SMART_TASKS_IMPLEMENTATION.md
Bead: solutions-iweb, solutions-hgwx.1, solutions-hgwx.2, solutions-hgwx.3
"""

import logging
import re
from dataclasses import dataclass
from typing import Optional

from .vikunja_client import BotVikunjaClient, VikunjaAPIError
from .metadata_manager import MetadataManager, SmartTaskMetadata
from .api_clients import get_weather_client, get_stock_client, get_news_client
from .schedule_parser import parse_schedule
from .config import is_llm_enabled

logger = logging.getLogger(__name__)


@dataclass
class HandlerResult:
    """Result from a keyword handler execution."""
    success: bool
    message: str
    data: Optional[dict] = None


class KeywordHandlers:
    """Tier 3 keyword handlers for deterministic @eis commands.

    Usage:
        handlers = KeywordHandlers()
        result = await handlers.complete_task({"task_ids": [42]})
        print(result.message)  # "Completed 1 task: #42"
    """

    def __init__(self, client: Optional[BotVikunjaClient] = None):
        """Initialize handlers.

        Args:
            client: BotVikunjaClient instance (creates one if not provided)
        """
        self.client = client or BotVikunjaClient()

    async def complete_task(self, args: dict) -> HandlerResult:
        """Mark task(s) as complete.

        Supports batch operations: {"task_ids": [1, 2, 3]}

        Args:
            args: {"task_ids": [int, ...]}

        Returns:
            HandlerResult with success status and message
        """
        task_ids = args.get("task_ids", [])

        if not task_ids:
            return HandlerResult(
                success=False,
                message="No task ID provided. Usage: @eis !x 42"
            )

        completed = []
        errors = []

        for task_id in task_ids:
            try:
                self.client.update_task(task_id, done=True)
                # Add comment to show @eis did the work
                try:
                    self.client.add_comment(task_id, "✅ Marked complete by eis")
                except VikunjaAPIError:
                    pass  # Comment is nice-to-have, don't fail if it doesn't work
                completed.append(task_id)
                logger.info(f"Completed task #{task_id}")
            except VikunjaAPIError as e:
                error_msg = f"#{task_id}: {e}"
                errors.append(error_msg)
                logger.error(f"Failed to complete task {task_id}: {e}")
            except Exception as e:
                error_msg = f"#{task_id}: {e}"
                errors.append(error_msg)
                logger.exception(f"Unexpected error completing task {task_id}")

        # Build response message
        parts = []
        if completed:
            if len(completed) == 1:
                parts.append(f"✅ Completed task #{completed[0]}")
            else:
                task_list = ", ".join(f"#{t}" for t in completed)
                parts.append(f"✅ Completed {len(completed)} tasks: {task_list}")

        if errors:
            parts.append("Errors:\n" + "\n".join(errors))

        return HandlerResult(
            success=len(errors) == 0,
            message="\n".join(parts) if parts else "No tasks completed",
            data={"completed": completed, "errors": errors}
        )

    async def set_reminder(self, args: dict) -> HandlerResult:
        """Set reminder for a task.

        Args:
            args: {"task_id": int, "when": str}

        Returns:
            HandlerResult with status
        """
        task_id = args.get("task_id")
        when = args.get("when")

        if not task_id:
            return HandlerResult(
                success=False,
                message="No task ID provided. Usage: @eis !r 42 / tomorrow at 3pm"
            )

        if not when:
            return HandlerResult(
                success=False,
                message="No time specified. Usage: @eis !r 42 / tomorrow at 3pm"
            )

        # TODO: Parse "when" into datetime and set reminder
        # For Phase 1, just acknowledge the request
        return HandlerResult(
            success=False,
            message=f"Reminder parsing not yet implemented (Phase 2). Got: task #{task_id}, when=\"{when}\""
        )

    async def weather_handler(self, args: dict) -> HandlerResult:
        """Get weather info or create auto-updating weather task.

        Args:
            args: {"location": str, "schedule": str (optional)}

        Returns:
            HandlerResult with weather data or schedule confirmation
        """
        location = args.get("location") or "San Francisco"
        schedule = args.get("schedule")
        target_project = args.get("target_project")

        # Get weather data from API
        weather_client = get_weather_client()
        response = await weather_client.get_weather(location)

        if not response.success:
            return HandlerResult(
                success=False,
                message=f"Weather error: {response.error}"
            )

        # Build smart title from weather data
        weather = response.data
        icon_map = {
            "01d": "☀️", "01n": "🌙",
            "02d": "⛅", "02n": "☁️",
            "03d": "☁️", "03n": "☁️",
            "04d": "☁️", "04n": "☁️",
            "09d": "🌧️", "09n": "🌧️",
            "10d": "🌦️", "10n": "🌧️",
            "11d": "⛈️", "11n": "⛈️",
            "13d": "❄️", "13n": "❄️",
            "50d": "🌫️", "50n": "🌫️",
        }
        icon = icon_map.get(weather.get("icon", ""), "🌡️")
        loc = weather.get("location", location)
        temp = weather.get("temp_f", "?")
        smart_title = f"{loc} {temp}°F {icon}"

        # Build base data
        data = {
            "weather": response.data,
            "keyword": "weather",
            "handler_args": {"location": location},
            "keep_task": True,  # Info commands keep the task
            "smart_title": smart_title,
        }

        if target_project:
            data["target_project"] = target_project

        # Schedule handling
        if schedule:
            schedule_config = parse_schedule(schedule)
            if not schedule_config.valid:
                return HandlerResult(
                    success=True,
                    message=f"{response.formatted}\n\n---\n⚠️ Invalid schedule: {schedule_config.error}",
                    data=data
                )

            data["schedule"] = schedule

        # Return weather data - action bar added by notification poller/refresh handler
        return HandlerResult(
            success=True,
            message=response.formatted,
            data=data
        )

    async def stock_handler(self, args: dict) -> HandlerResult:
        """Get stock info or create auto-updating stock task.

        Args:
            args: {"ticker": str, "schedule": str (optional)}

        Returns:
            HandlerResult with stock data or schedule confirmation
        """
        ticker = args.get("ticker")
        schedule = args.get("schedule")
        target_project = args.get("target_project")

        if not ticker:
            return HandlerResult(
                success=False,
                message="No ticker symbol provided. Usage: @eis !s AAPL"
            )

        # Get stock data from API
        stock_client = get_stock_client()
        response = await stock_client.get_quote(ticker)

        if not response.success:
            return HandlerResult(
                success=False,
                message=f"Stock error: {response.error}"
            )

        # Build smart title from stock data
        stock = response.data
        price = stock.get("price", 0)
        change = stock.get("change_pct", 0)
        if change > 0:
            icon = "📈"
        elif change < 0:
            icon = "📉"
        else:
            icon = "➖"
        smart_title = f"{ticker.upper()} ${price:.2f} {icon}"

        # Build base data
        data = {
            "stock": response.data,
            "keyword": "stock",
            "handler_args": {"ticker": ticker},
            "keep_task": True,
            "smart_title": smart_title,
        }

        if target_project:
            data["target_project"] = target_project

        # Schedule handling
        if schedule:
            schedule_config = parse_schedule(schedule)
            if not schedule_config.valid:
                return HandlerResult(
                    success=True,
                    message=f"{response.formatted}\n\n---\n⚠️ Invalid schedule: {schedule_config.error}",
                    data=data
                )

            data["schedule"] = schedule
            return HandlerResult(
                success=True,
                message=f"{response.formatted}\n\n---\n🔄 *Auto-updating: {schedule}*",
                data=data
            )

        return HandlerResult(
            success=True,
            message=response.formatted,
            data=data
        )

    async def news_handler(self, args: dict) -> HandlerResult:
        """Get news headlines.

        Args:
            args: {"query": str (optional), "category": str (optional), "target_project": str (optional)}

        Returns:
            HandlerResult with news data
        """
        query = args.get("query")
        category = args.get("category")
        target_project = args.get("target_project")

        # Get news from API
        news_client = get_news_client()
        response = await news_client.get_headlines(query=query, category=category)

        if not response.success:
            return HandlerResult(
                success=False,
                message=f"News error: {response.error}"
            )

        # Build base data
        data = {
            "news": response.data,
            "keyword": "news",
            "handler_args": {"query": query, "category": category},
            "keep_task": True,  # Info commands keep the task
        }

        if target_project:
            data["target_project"] = target_project

        return HandlerResult(
            success=True,
            message=response.formatted,
            data=data
        )

    async def rss_handler(self, args: dict) -> HandlerResult:
        """Fetch RSS/Atom feed.

        Args:
            args: {"url": str, "schedule": str (optional), "target_project": str (optional)}

        Returns:
            HandlerResult with feed entries
        """
        from .api_clients import get_rss_client

        url = args.get("url", "").strip()
        schedule = args.get("schedule")
        target_project = args.get("target_project")

        if not url:
            return HandlerResult(
                success=False,
                message="No URL provided. Usage: @eis !rss <feed_url>"
            )

        # Basic URL validation
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        # Get feed from client
        rss_client = get_rss_client()
        response = await rss_client.get_feed(url)

        if not response.success:
            return HandlerResult(
                success=False,
                message=f"RSS error: {response.error}"
            )

        # Build base data
        data = {
            "rss": response.data,
            "keyword": "rss",
            "handler_args": {"url": url},
            "keep_task": True,  # Info commands keep the task
        }

        if schedule:
            data["schedule"] = schedule
            data["handler_args"]["schedule"] = schedule

        if target_project:
            data["target_project"] = target_project

        return HandlerResult(
            success=True,
            message=response.formatted,
            data=data
        )

    # =========================================================================
    # Tier 1/2: LLM-backed handlers (Phase 2)
    # =========================================================================

    async def llm_natural(
        self,
        args: dict,
        task_id: Optional[int] = None,
        project_id: Optional[int] = None,
        project_name: Optional[str] = None,
        conversation_context: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> HandlerResult:
        """Execute Tier 1 LLM natural language command ($ prefix).

        Delegates to llm_tools for actual LLM call. The cost_tier ($, $$, $$$)
        signals model choice (future: Haiku for $, Sonnet for $$, Opus for $$$).

        Args:
            args: {"cost_tier": str, "prompt": str}
            task_id: Optional task ID (for updating existing task)
            project_id: Project ID for scope enforcement
            project_name: Project name for context
            conversation_context: Optional conversation history for refinement
            user_id: User ID for budget tracking

        Returns:
            HandlerResult with LLM response
        """
        cost_tier = args.get("cost_tier", "$")
        prompt = args.get("prompt", "")

        if not prompt:
            return HandlerResult(
                success=False,
                message="No prompt provided. Usage: @eis $ <your request>"
            )

        # Delegate to llm_tools which has the real Claude integration
        return await self.llm_tools(
            args={"prompt": prompt, "cost_tier": cost_tier},
            task_id=task_id,
            project_id=project_id,
            project_name=project_name,
            conversation_context=conversation_context,
            user_id=user_id,
        )

    async def llm_context(
        self,
        args: dict,
        task_id: Optional[int] = None,
        project_id: Optional[int] = None,
        project_name: Optional[str] = None,
        conversation_context: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> HandlerResult:
        """Execute Tier 2 LLM command with task context.

        Operates on an existing task. Uses tool-calling loop for analysis.

        Args:
            args: {"cost_tier": str, "task_ref": str, "instruction": str}
            task_id: Optional source task ID
            project_id: Project ID for scope enforcement
            project_name: Project name for context
            conversation_context: Optional conversation history for refinement
            user_id: User ID for budget tracking

        Returns:
            HandlerResult with LLM analysis
        """
        cost_tier = args.get("cost_tier", "$$")
        task_ref = args.get("task_ref", "")
        instruction = args.get("instruction", "")

        if not task_ref:
            return HandlerResult(
                success=False,
                message="No task reference provided. Usage: @eis $$ 42 / <instruction>"
            )

        if not instruction:
            return HandlerResult(
                success=False,
                message="No instruction provided. Usage: @eis $$ 42 / summarize comments"
            )

        # Resolve task reference (number or fuzzy name)
        target_task_id = None
        task_title = ""
        task_description = ""

        try:
            # Try as numeric ID first
            target_task_id = int(task_ref)
            task = self.client.get_task(target_task_id)
            task_title = task.get("title", "")
            task_description = task.get("description", "")
        except ValueError:
            # Not a number - would need fuzzy search (Phase 3+)
            return HandlerResult(
                success=False,
                message=f"Task '{task_ref}' not found. Fuzzy search not yet implemented. Use task ID instead."
            )
        except VikunjaAPIError as e:
            return HandlerResult(
                success=False,
                message=f"Could not fetch task #{task_ref}: {e}"
            )

        # Build prompt with task context
        prompt = f"""Analyze task #{target_task_id}: "{task_title}"

Task description:
{task_description or "(no description)"}

User instruction: {instruction}"""

        # Delegate to llm_tools which has the real Claude integration
        return await self.llm_tools(
            args={"prompt": prompt, "cost_tier": cost_tier},
            task_id=task_id,
            project_id=project_id,
            project_name=project_name,
            conversation_context=conversation_context,
            user_id=user_id,
        )

    async def llm_tools(
        self,
        args: dict,
        task_id: Optional[int] = None,
        project_id: Optional[int] = None,
        project_name: Optional[str] = None,
        conversation_context: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> HandlerResult:
        """Execute natural language command with full tool access.

        Uses the tool-calling loop to give @eis full access to Vikunja
        tools within the project scope.

        Args:
            args: {"prompt": str} - Natural language request
            task_id: Task ID for context (optional)
            project_id: Project ID for scope enforcement
            project_name: Project name for context
            conversation_context: Previous conversation history
            user_id: User ID for budget tracking (vikunja:<username>)

        Returns:
            HandlerResult with LLM response
        """
        prompt = args.get("prompt", "")

        if not prompt:
            return HandlerResult(
                success=False,
                message="No request provided. Just tell me what you need!"
            )

        if not project_id:
            return HandlerResult(
                success=False,
                message="Could not determine project context."
            )

        # Check user budget before making LLM call
        if user_id:
            from .budget_service import check_budget, deduct_credit, InsufficientCreditError
            if not check_budget(user_id):
                return HandlerResult(
                    success=False,
                    message="❌ **Out of AI credit.** Your balance is $0.00.\n\n"
                            "You can still use ! commands (like `!weather`, `!stock`, `!rss`) - those are free!\n\n"
                            "Contact support to add more credit."
                )

        # Import the tool-calling loop
        from .server import vikunja_chat_with_claude

        # Count context for token display
        context_info = ""
        if conversation_context:
            # Count comments in context
            comment_count = conversation_context.count("**") // 2  # Each comment has **author:**
            if comment_count > 0:
                context_info = f" (+{comment_count} comments)"

        try:
            max_turns = 10
            # Map cost tier to model (solutions-2dum)
            cost_tier = args.get("cost_tier", "$")
            tier_to_model = {
                "$": "haiku",
                "$$": "sonnet",
                "$$$": "opus",
            }
            model = tier_to_model.get(cost_tier, "haiku")
            # Extract username from user_id (format: "vikunja:<username>:<id>")
            requesting_user = None
            if user_id and user_id.startswith("vikunja:"):
                parts = user_id.split(":")
                if len(parts) >= 2:
                    requesting_user = parts[1]  # Just the username, not "username:id"
            # Extract numeric user_id if available (format: "vikunja:<username>:<id>")
            requesting_user_id = None
            if user_id and user_id.count(":") >= 2:
                try:
                    requesting_user_id = int(user_id.rsplit(":", 1)[1])
                except (ValueError, IndexError):
                    pass
            response_text, input_tokens, output_tokens, turns_used = vikunja_chat_with_claude(
                user_message=prompt,
                project_id=project_id,
                project_name=project_name or "",
                max_turns=max_turns,
                conversation_context=conversation_context,
                model=model,
                requesting_user=requesting_user,
                requesting_user_id=requesting_user_id,
            )

            # Calculate cost based on model
            # Haiku 3.5: $0.80/M in, $4/M out
            # Sonnet 4: $3/M in, $15/M out
            # Opus 4: $15/M in, $75/M out
            model_costs = {
                "haiku": (0.80, 4.0),
                "sonnet": (3.0, 15.0),
                "opus": (15.0, 75.0),
            }
            in_cost, out_cost = model_costs.get(model, (0.80, 4.0))
            cost = (input_tokens * in_cost + output_tokens * out_cost) / 1_000_000
            # Always show as dollars (e.g., ~$0.006) - cents symbol was confusing
            cost_str = f"~${cost:.4f}"

            # Deduct from user budget (use actual calculated cost, not estimate)
            balance_str = ""
            if user_id:
                try:
                    # Convert dollars to cents for budget system
                    cost_cents = int(cost * 100) + 1  # Round up to nearest cent
                    budget_info = deduct_credit(
                        user_id,
                        cost_cents,
                        f"LLM call ({model}): {input_tokens}→{output_tokens} tokens"
                    )
                    balance_str = f" | Balance: {budget_info.format_balance()}"
                except InsufficientCreditError:
                    # Already used their last credit - allow this call but warn
                    balance_str = " | ⚠️ Credit exhausted"
                except Exception as e:
                    logger.warning(f"Budget deduction failed for {user_id}: {e}")

            # Build cost footer
            cost_footer = f"{cost_str}{balance_str}"

            return HandlerResult(
                success=True,
                message=f"{response_text}\n\n---\n{cost_footer}",
                data={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost": cost_footer,
                    "model": model.title(),  # "haiku" → "Haiku"
                    "tokens": f"{input_tokens}{context_info}→{output_tokens}",
                    "tools": f"{turns_used}/{max_turns}",
                }
            )
        except Exception as e:
            logger.exception("llm_tools handler failed")
            return HandlerResult(
                success=False,
                message=f"Error: {e}"
            )

    # =========================================================================
    # Budget management commands
    # =========================================================================

    async def upgrade_tier(self, args: dict, task_id: Optional[int] = None) -> HandlerResult:
        """Upgrade a smart task to a higher cost tier.

        Args:
            args: {"new_tier": str} - The tier to upgrade to
            task_id: Task ID to upgrade

        Returns:
            HandlerResult with upgrade status
        """
        new_tier = args.get("new_tier", "$$")

        if not task_id:
            return HandlerResult(
                success=False,
                message="No task specified. Use this command on a smart task."
            )

        # Get current task
        try:
            task = self.client.get_task(task_id)
            description = task.get("description", "")
        except VikunjaAPIError as e:
            return HandlerResult(
                success=False,
                message=f"Could not fetch task #{task_id}: {e}"
            )

        # Extract metadata
        metadata, content = MetadataManager.extract(description)

        if not metadata:
            return HandlerResult(
                success=False,
                message=f"Task #{task_id} is not a smart task (no metadata found)"
            )

        old_tier = metadata.cost_tier
        if not metadata.upgrade_tier(new_tier):
            return HandlerResult(
                success=False,
                message=f"Invalid tier '{new_tier}'. Valid tiers: $, $$, $$$"
            )

        # Update task description with new metadata
        new_description = MetadataManager.format(metadata, content)
        try:
            self.client.update_task(task_id, description=new_description)
        except VikunjaAPIError as e:
            return HandlerResult(
                success=False,
                message=f"Could not update task #{task_id}: {e}"
            )

        return HandlerResult(
            success=True,
            message=f"Upgraded task #{task_id} from {old_tier} to {new_tier}. New limit: {metadata.llm_calls_limit} calls.",
            data={"metadata": metadata.to_dict()}
        )

    # Admin users who can use privileged commands
    # Format: "vikunja:username" - matches "vikunja:username" or "vikunja:username:123"
    ADMIN_USERS = {"vikunja:ivan"}

    @staticmethod
    def _is_admin(user_id: str) -> bool:
        """Check if user_id matches any admin pattern.

        Handles format mismatch: notifications return "vikunja:ivan:123"
        but config has "vikunja:ivan". Match by prefix.
        """
        if not user_id:
            return False
        for admin in KeywordHandlers.ADMIN_USERS:
            # Exact match or prefix match (vikunja:ivan matches vikunja:ivan:123)
            if user_id == admin or user_id.startswith(f"{admin}:"):
                return True
        return False

    async def reset_budget(
        self, args: dict, task_id: Optional[int] = None, user_id: Optional[str] = None
    ) -> HandlerResult:
        """Reset the budget counter for a smart task (admin only).

        Args:
            args: {} (no args needed)
            task_id: Task ID to reset
            user_id: User ID for admin check

        Returns:
            HandlerResult with reset status
        """
        # Admin check
        if not self._is_admin(user_id):
            return HandlerResult(
                success=False,
                message="This command is admin-only. Use `!balance` to check your credit."
            )

        if not task_id:
            return HandlerResult(
                success=False,
                message="No task specified. Use this command on a smart task."
            )

        # Get current task
        try:
            task = self.client.get_task(task_id)
            description = task.get("description", "")
        except VikunjaAPIError as e:
            return HandlerResult(
                success=False,
                message=f"Could not fetch task #{task_id}: {e}"
            )

        # Extract metadata
        metadata, content = MetadataManager.extract(description)

        if not metadata:
            return HandlerResult(
                success=False,
                message=f"Task #{task_id} is not a smart task (no metadata found)"
            )

        old_used = metadata.llm_calls_used
        old_cost = metadata.total_cost
        metadata.reset_budget()

        # Update task description
        new_description = MetadataManager.format(metadata, content)
        try:
            self.client.update_task(task_id, description=new_description)
        except VikunjaAPIError as e:
            return HandlerResult(
                success=False,
                message=f"Could not update task #{task_id}: {e}"
            )

        return HandlerResult(
            success=True,
            message=f"Reset budget for task #{task_id}. Previous: {old_used} calls (${old_cost:.2f}). Now: 0/{metadata.llm_calls_limit} calls.",
            data={"metadata": metadata.to_dict()}
        )

    async def grant_credit(
        self, args: dict, task_id: Optional[int] = None, user_id: Optional[str] = None
    ) -> HandlerResult:
        """Grant AI credit to a user (admin only).

        Usage:
            @eis !grant $5        → Grant $5 to self
            @eis !grant $10 ivan  → Grant $10 to user ivan

        Args:
            args: {"amount": str, "target_user": str (optional)}
            user_id: User ID for admin check

        Returns:
            HandlerResult with grant status
        """
        # Admin check
        if not self._is_admin(user_id):
            return HandlerResult(
                success=False,
                message="This command is admin-only."
            )

        # Parse amount
        amount_str = args.get("amount", "")
        if not amount_str:
            return HandlerResult(
                success=False,
                message="Usage: `!grant $5` or `!grant username $10`"
            )

        # Parse dollar amount (e.g., "$5", "5", "$10.50")
        match = re.search(r'\$?(\d+(?:\.\d{1,2})?)', amount_str)
        if not match:
            return HandlerResult(
                success=False,
                message=f"Invalid amount: {amount_str}. Use format like `$5` or `$10.50`"
            )

        amount_dollars = float(match.group(1))
        amount_cents = int(amount_dollars * 100)

        if amount_cents <= 0:
            return HandlerResult(
                success=False,
                message="Amount must be positive."
            )

        # Determine target user
        target_user = args.get("target_user", "").strip()
        if target_user:
            # Admin granting to another user - look up their full user ID
            if not target_user.startswith("vikunja:"):
                # Look up user to get numeric ID for proper user_id format
                try:
                    users = self.client._request("GET", f"/users?s={target_user}")
                    found_user = None
                    for u in users:
                        if u.get("username", "").lower() == target_user.lower():
                            found_user = u
                            break
                    if found_user:
                        numeric_id = found_user.get("id")
                        target_user = f"vikunja:{target_user}:{numeric_id}" if numeric_id else f"vikunja:{target_user}"
                    else:
                        return HandlerResult(
                            success=False,
                            message=f"User `{target_user}` not found in Vikunja."
                        )
                except Exception as e:
                    # Fall back to simple format if lookup fails
                    target_user = f"vikunja:{target_user}"
        else:
            # Admin granting to self
            target_user = user_id

        # Grant credit
        from .budget_service import add_credit
        try:
            result = add_credit(target_user, amount_cents, user_id, "Admin grant")
            new_balance = result.balance_cents

            # TODO (solutions-notif): Notify grantee when granting to someone else
            # Needs: find grantee's Inbox project, create task there, assign to them
            # For now, grantee can check with !balance

            return HandlerResult(
                success=True,
                message=f"Granted **${amount_dollars:.2f}** to {target_user}. New balance: **${new_balance/100:.2f}**"
            )
        except Exception as e:
            return HandlerResult(
                success=False,
                message=f"Failed to grant credit: {e}"
            )

    async def balance_handler(self, args: dict, task_id: int = None, project_id: int = None, user_id: Optional[str] = None) -> HandlerResult:
        """Check user's AI credit balance.

        Args:
            args: {} (no args needed)
            user_id: User ID for budget lookup (vikunja:<username>)

        Returns:
            HandlerResult with balance information
        """
        if not user_id:
            return HandlerResult(
                success=False,
                message="Could not determine your user. Please try again."
            )

        from .budget_service import get_user_budget, ensure_user_budget, get_transaction_history

        try:
            # Get or create budget
            budget = ensure_user_budget(user_id)

            # Get recent transactions
            transactions = get_transaction_history(user_id, limit=5)

            # Build response
            lines = [
                f"**AI Credit Balance: {budget.format_balance()}**",
                "",
                f"- Total spent: ${budget.total_spent_cents / 100:.2f}",
                f"- Total added: ${budget.total_added_cents / 100:.2f}",
            ]

            if transactions:
                lines.append("")
                lines.append("**Recent activity:**")
                for tx in transactions[:5]:
                    amount = tx["amount_cents"]
                    sign = "+" if amount > 0 else ""
                    desc = tx.get("description", tx["transaction_type"])
                    lines.append(f"- {sign}{amount}¢: {desc}")

            if budget.balance_cents <= 0:
                lines.append("")
                lines.append("⚠️ **No credit remaining.** Contact support to add more.")
            elif budget.balance_cents < 25:  # Less than 25¢
                lines.append("")
                lines.append("⚠️ Running low on credit.")

            # Format timestamp for title (use user's timezone)
            from datetime import datetime
            from zoneinfo import ZoneInfo
            from .server import _get_user_timezone_override

            user_tz_name = _get_user_timezone_override(user_id) if user_id else None
            if user_tz_name:
                try:
                    user_tz = ZoneInfo(user_tz_name)
                except Exception:
                    user_tz = ZoneInfo("UTC")
            else:
                user_tz = ZoneInfo("UTC")
            now = datetime.now(user_tz).strftime("%b %d %H:%M")

            # Delete previous balance tasks in this project
            if project_id and task_id:
                self._delete_previous_info_tasks(project_id, task_id, "!balance", "balance:")

            return HandlerResult(
                success=True,
                message="\n".join(lines),
                data={"keep_task": True, "smart_title": f"Balance: {budget.format_balance()} ({now})"}
            )

        except Exception as e:
            logger.exception(f"balance_handler failed for {user_id}")
            return HandlerResult(
                success=False,
                message=f"Error checking balance: {e}"
            )

    # =========================================================================
    # Help command (auto-generated from command_registry.py)
    # =========================================================================

    # Topic aliases for fuzzy help lookups
    HELP_ALIASES = {
        "w": "weather",
        "s": "stock",
        "stocks": "stock",
        "n": "news",
        "headlines": "news",
        "x": "complete",
        "done": "complete",
        "$": "llm",
        "ai": "llm",
        "tier": "llm",
        "tiers": "llm",
        "schedules": "schedule",
        "auto": "schedule",
        "update": "schedule",
        "projects": "project",
        "pipe": "project",
        "|": "project",
        "credit": "budget",
        "credits": "budget",
        "balance": "budget",
        "bal": "budget",
        "cost": "budget",
        "billing": "budget",
        "money": "budget",
    }

    # Model definitions (extensible for future models)
    MODELS = {
        "haiku": {
            "name": "Claude Haiku",
            "tier": "$",
            "cost": "~$0.01-0.05",
            "description": "Fast & affordable. Quick tasks, simple questions, info lookup.",
            "tools": 3,
        },
        "sonnet": {
            "name": "Claude Sonnet",
            "tier": "$$",
            "cost": "~$0.05-0.15",
            "description": "Balanced. Complex analysis, multi-step planning, detailed writing.",
            "tools": 10,
        },
        "opus": {
            "name": "Claude Opus",
            "tier": "$$$",
            "cost": "~$0.15-0.50",
            "description": "Most capable. Deep research, strategic thinking, nuanced tasks.",
            "tools": 25,
        },
    }

    async def model_handler(self, args: dict) -> HandlerResult:
        """Show available AI models and their capabilities.

        Args:
            args: {"model": str (optional)} - specific model to show

        Returns:
            HandlerResult with model information
        """
        selected = args.get("model", "").lower()

        # If specific model requested, show details
        if selected and selected in self.MODELS:
            m = self.MODELS[selected]
            return HandlerResult(
                success=True,
                message=(
                    f"**{m['name']}** ({m['tier']})\n\n"
                    f"{m['description']}\n\n"
                    f"- Cost: {m['cost']} per request\n"
                    f"- Tool calls: up to {m['tools']}\n\n"
                    f"Usage: `@eis {m['tier']} <your request>`"
                ),
                data={"keyword": "model", "keep_task": True, "smart_title": f"Model: {m['name']}"}
            )

        # Show all models
        lines = ["# AI Models\n"]
        lines.append("| Tier | Model | Best For | Cost |")
        lines.append("|------|-------|----------|------|")

        for key, m in self.MODELS.items():
            lines.append(f"| {m['tier']} | {m['name']} | {m['description'].split('.')[0]} | {m['cost']} |")

        lines.append("\n## Usage")
        lines.append("```")
        lines.append("@eis $ quick question      → Haiku (fast, cheap)")
        lines.append("@eis $$ plan my project    → Sonnet (balanced)")
        lines.append("@eis $$$ strategic review  → Opus (powerful)")
        lines.append("```")
        lines.append("\n**Current default:** Haiku ($)")

        return HandlerResult(
            success=True,
            message="\n".join(lines),
            data={"keyword": "model", "keep_task": True, "smart_title": "AI Models"}
        )

    async def help_handler(self, args: dict) -> HandlerResult:
        """Show help documentation (auto-generated from command registry).

        Args:
            args: {"topic": str (optional)}

        Returns:
            HandlerResult with help content
        """
        from .command_registry import build_help_overview, build_help_topic

        topic = args.get("topic", "").strip().lower()

        if topic:
            # Resolve aliases
            resolved = self.HELP_ALIASES.get(topic, topic)

            # Try to get topic-specific help
            content = build_help_topic(resolved)
            if not content:
                # Unknown topic - show overview with hint
                content = build_help_overview()
                content += f"\n\n---\n⚠️ Unknown topic: `{topic}`. Showing overview."
        else:
            content = build_help_overview()

        return HandlerResult(
            success=True,
            message=content.strip(),
            data={
                "keyword": "help",
                "keep_task": True,
                "handler_args": {"topic": topic},
            }
        )

    async def cheatsheet_handler(self, args: dict) -> HandlerResult:
        """Quick command reference card for @eis.

        Args:
            args: {} (no args needed)

        Returns:
            HandlerResult with cheatsheet content
        """
        llm_enabled = is_llm_enabled()

        # Base cheatsheet - always shown
        lines = [
            "# @eis Quick Commands",
            "",
            "## 📋 Task Actions",
            "| Do This | Command |",
            "|---------|---------|",
            "| Complete task #42 | `@eis !x 42` |",
            "| Complete multiple | `@eis !x 1 2 3` |",
            "",
            "## 🌤️ Info Commands",
            "| Get This | Command |",
            "|----------|---------|",
            "| Weather | `@eis !w Tokyo` |",
            "| Weather hourly | `@eis !w Seattle hourly` |",
            "| RSS feed | `@eis !rss https://example.com/feed.xml` |",
            "",
        ]

        # AI Commands section - only when LLM enabled
        if llm_enabled:
            lines.extend([
                "## 🤖 AI Commands",
                "| Effort | Command |",
                "|--------|---------|",
                "| Quick (3 tools) | `@eis $ plan a party` |",
                "| Medium (10 tools) | `@eis $$ write proposal` |",
                "| Deep (25 tools) | `@eis $$$ business plan` |",
                "",
            ])

        # Auto-refresh section
        lines.extend([
            "## ⏰ Auto-Refresh",
            "| Interval | Example |",
            "|----------|---------|",
            "| Sub-daily | `@eis !w Tokyo hourly` or `6h` |",
            "| Daily+ | `@eis !w Tokyo every day` (Vikunja syntax) |",
            "",
            "## 📁 Target Project",
            "Use Vikunja's `+Project` syntax:",
            "`@eis !w Tokyo +Dashboard`",
            "",
        ])

        # Budget section - only when LLM enabled
        if llm_enabled:
            lines.extend([
                "## 💰 Budget",
                "| Check | Command |",
                "|-------|---------|",
                "| Your balance | `@eis !balance` |",
                "",
            ])

        # More help section
        lines.append("## 💡 More Help")
        lines.append("`@eis !help` - Full documentation")
        if llm_enabled:
            lines.append("`@eis !model` - AI models & pricing")

        return HandlerResult(
            success=True,
            message="\n".join(lines).strip(),
            data={
                "keyword": "cheatsheet",
                "keep_task": True,
                "smart_title": "⚡ Quick Commands",
            }
        )

    def _delete_opposite_toggle_tasks(
        self, project_id: int, current_task_id: int, pattern: str, opposite_state: str
    ) -> int:
        """Delete previous toggle tasks with opposite state.

        For toggle commands like !ears on/off, we only want to show
        the latest state. This deletes tasks matching the opposite pattern.

        Args:
            project_id: Project to search in
            current_task_id: Current task ID (don't delete this one)
            pattern: Pattern to match in title (e.g., "ears off")
            opposite_state: The opposite state keyword (e.g., "off", "on")

        Returns:
            Number of tasks deleted
        """
        deleted = 0
        try:
            tasks = self.client.list_tasks(project_id=project_id)
            for task in tasks:
                if task["id"] == current_task_id:
                    continue
                title = task.get("title", "").lower()
                # Match tasks that contain the opposite toggle pattern
                if pattern.lower() in title or f"ears {opposite_state}" in title:
                    try:
                        self.client.delete_task(task["id"])
                        deleted += 1
                        logger.info(f"[toggle] Deleted opposite toggle task #{task['id']}: {task.get('title')}")
                    except Exception as e:
                        logger.warning(f"[toggle] Failed to delete #{task['id']}: {e}")
        except Exception as e:
            logger.warning(f"[toggle] Failed to list tasks for cleanup: {e}")
        return deleted

    def _delete_previous_info_tasks(
        self, project_id: int, current_task_id: int, *patterns: str
    ) -> int:
        """Delete previous info tasks matching any pattern.

        For info commands like !balance, we only want to show the latest.
        This deletes older tasks matching any of the patterns.

        Args:
            project_id: Project to search in
            current_task_id: Current task ID (don't delete this one)
            *patterns: Patterns to match in title (case-insensitive)

        Returns:
            Number of tasks deleted
        """
        deleted = 0
        try:
            tasks = self.client.list_tasks(project_id=project_id)
            for task in tasks:
                if task["id"] == current_task_id:
                    continue
                title = task.get("title", "").lower()
                # Match tasks that contain any of the patterns
                if any(p.lower() in title for p in patterns):
                    try:
                        self.client.delete_task(task["id"])
                        deleted += 1
                        logger.info(f"[info] Deleted previous info task #{task['id']}: {task.get('title')}")
                    except Exception as e:
                        logger.warning(f"[info] Failed to delete #{task['id']}: {e}")
        except Exception as e:
            logger.warning(f"[info] Failed to list tasks for cleanup: {e}")
        return deleted

    async def ears_handler(self, args: dict, task_id: int = None, user_id: str = None) -> HandlerResult:
        """Toggle project-level @eis ears mode (listen to all new tasks).

        When enabled, @eis listens and processes all new tasks in the project
        without needing explicit @mention.

        Args:
            args: {"action": "on"|"off"}
            task_id: Current task ID (to get project context)
            user_id: User ID for service tracking (vikunja:<username>:<id>)

        Returns:
            HandlerResult with confirmation

        Bead: solutions-bx4t, solutions-skqu
        """
        # EARS requires LLM to process tasks - disabled when LLM features are off
        if not is_llm_enabled():
            return HandlerResult(
                success=False,
                message="👂 EARS mode requires AI features (coming soon). Use !help for available commands."
            )

        import os
        from .server import _get_project_ears, _update_project_ears, _generate_action_token

        action = args.get("action", "on").lower()  # Default to "on" if just !ears

        # Get project_id from task
        if not task_id:
            return HandlerResult(
                success=False,
                message="❌ No task context. Run this command in a task."
            )

        try:
            task = self.client.get_task(task_id)
            project_id = task.get("project_id")
        except Exception as e:
            return HandlerResult(
                success=False,
                message=f"❌ Could not get task info: {e}"
            )

        if not project_id:
            return HandlerResult(
                success=False,
                message="❌ Could not determine project."
            )

        # Get project name for display
        try:
            project = self.client.get_project(project_id)
            project_name = project.get("title", f"Project {project_id}")
        except Exception:
            project_name = f"Project {project_id}"

        if action == "on":
            _update_project_ears(project_id, enabled=True)

            # Set service_needed flag for this user (solutions-skqu)
            if user_id:
                from .bot_provisioning import set_service_needed
                set_service_needed(user_id, needed=True, reason="ears_on")

            # Delete any previous "ears off" tasks in this project
            self._delete_opposite_toggle_tasks(project_id, task_id, "ears off", "off")

            # Generate turn-off link
            mcp_url = os.environ.get("MCP_URL", "https://mcp.factumerit.app")
            token = _generate_action_token("ears-off", project_id)
            off_url = f"{mcp_url}/ears-off/{project_id}/{token}"

            return HandlerResult(
                success=True,
                message=(
                    f"👂 **Ears ON** for {project_name}\n\n"
                    f"All new tasks will be processed automatically.\n\n"
                    f"[Turn off]({off_url})"
                ),
                data={"keyword": "ears", "keep_task": True, "smart_title": "👂 Ears ON - auto-processing tasks"}
            )

        else:  # off (default if not "on")
            _update_project_ears(project_id, enabled=False)

            # Clear service_needed flag if no other EARS projects (solutions-skqu)
            if user_id:
                from .bot_provisioning import set_service_needed
                from .server import _get_ears_enabled_projects

                # Check if user has any other EARS projects
                ears_projects = _get_ears_enabled_projects()
                if not ears_projects:
                    # No more EARS projects, can disable service
                    set_service_needed(user_id, needed=False)

            # Delete any previous "ears on" tasks in this project
            self._delete_opposite_toggle_tasks(project_id, task_id, "ears on", "on")

            return HandlerResult(
                success=True,
                message=f"🔇 **Ears OFF** for {project_name}\n\nMention @eis to engage.",
                data={"keyword": "ears", "keep_task": True, "smart_title": f"🔇 Ears OFF"}
            )

    async def project_handler(self, args: dict, task_id: int = None, user_id: str = None) -> HandlerResult:
        """Handle project management commands: add, delete, rename.

        Args:
            args: {"action": "add"|"delete"|"rename", "name": str, "parent": str, "new_name": str}
            task_id: Current task ID (for context - used to infer current project)
            user_id: User ID for sharing (format: vikunja:username:id)

        Returns:
            HandlerResult with operation status
        """
        from .server import (
            _create_project_impl, _delete_project_impl, _list_projects_impl,
            _requesting_user, _requesting_user_id, _bot_mode, _current_vikunja_token
        )
        import os

        # Set bot token context for API calls
        bot_token = os.environ.get("VIKUNJA_BOT_TOKEN", "").strip()
        if bot_token:
            _bot_mode.set(True)
            _current_vikunja_token.set(bot_token)

        # Get current project context and user info from task
        current_project_id = None
        current_project_name = None
        task_creator_id = None
        task_creator_name = None
        if task_id:
            try:
                task = self.client.get_task(task_id)
                current_project_id = task.get("project_id")
                if current_project_id:
                    project = self.client.get_project(current_project_id)
                    current_project_name = project.get("title", "")
                # Get task creator info (more reliable than notification doer)
                created_by = task.get("created_by", {})
                if isinstance(created_by, dict):
                    task_creator_id = created_by.get("id")
                    task_creator_name = created_by.get("username", "")
                    logger.info(f"[project_handler] Task creator: username={task_creator_name}, id={task_creator_id}")
            except Exception:
                pass  # No context available

        # Use task creator for auto-share (more reliable than notification doer)
        # Only fall back to user_id from notification if task creator not available
        if task_creator_id and task_creator_name:
            _requesting_user.set(task_creator_name)
            _requesting_user_id.set(task_creator_id)
        elif user_id:
            # Fallback to notification user_id
            parts = user_id.split(":")
            if len(parts) >= 2:
                _requesting_user.set(parts[1])
            if len(parts) >= 3:
                try:
                    _requesting_user_id.set(int(parts[2]))
                except ValueError:
                    pass

        action = args.get("action", "").lower()
        name = args.get("name", "").strip()
        parent = args.get("parent", "").strip()
        new_name = args.get("new_name", "").strip()

        if not action:
            return HandlerResult(
                success=False,
                message="❌ Usage: `!project add|delete|rename <name>`"
            )

        # === ADD PROJECT ===
        if action == "add":
            # Handle "to" syntax with greedy right-match
            use_to_syntax = args.get("use_to_syntax", False)
            raw = args.get("raw", "")

            if use_to_syntax and raw:
                # Greedy right-match: find longest suffix after " to " that matches a project
                try:
                    projects = _list_projects_impl()
                    project_titles = {p["title"].lower(): p for p in projects}

                    # Find all " to " positions and try from rightmost
                    raw_lower = raw.lower()
                    to_positions = []
                    pos = 0
                    while True:
                        pos = raw_lower.find(" to ", pos)
                        if pos == -1:
                            break
                        to_positions.append(pos)
                        pos += 1

                    # Try from rightmost " to " to find a matching parent
                    parent_id = 0
                    for to_pos in reversed(to_positions):
                        potential_parent = raw[to_pos + 4:].strip()  # After " to "
                        potential_name = raw[:to_pos].strip()  # Before " to "

                        # Try exact match first, then fuzzy
                        if potential_parent.lower() in project_titles:
                            parent_id = project_titles[potential_parent.lower()]["id"]
                            name = potential_name
                            parent = potential_parent
                            break
                        else:
                            # Fuzzy match
                            matches = [p for p in projects if potential_parent.lower() in p["title"].lower()]
                            if len(matches) == 1:
                                parent_id = matches[0]["id"]
                                name = potential_name
                                parent = matches[0]["title"]
                                break

                    if not parent_id:
                        return HandlerResult(
                            success=False,
                            message=f"❌ Could not find parent project in: `{raw}`\n\nTry: `!project add <name> to <parent>`"
                        )
                except Exception as e:
                    return HandlerResult(
                        success=False,
                        message=f"❌ Error parsing: {e}"
                    )
            else:
                # Standard parsing (no "to" or using | fallback)
                if not name:
                    return HandlerResult(
                        success=False,
                        message="❌ Usage: `!project add <name>` or `!project add <name> to <parent>`"
                    )

                # Use current project as default parent if no explicit parent
                parent_id = current_project_id or 0
                if parent_id and not parent:
                    parent = current_project_name  # For display in success message

                # Find parent project if explicitly specified
                if parent and not parent_id:
                    try:
                        projects = _list_projects_impl()
                        # Fuzzy match parent name
                        parent_lower = parent.lower()
                        matches = [p for p in projects if parent_lower in p.get("title", "").lower()]
                        if not matches:
                            return HandlerResult(
                                success=False,
                                message=f"❌ Parent project '{parent}' not found"
                            )
                        if len(matches) > 1:
                            # Multiple matches - list them
                            match_list = "\n".join(f"- {m['title']}" for m in matches[:5])
                            return HandlerResult(
                                success=False,
                                message=f"❌ Multiple projects match '{parent}':\n{match_list}\n\nBe more specific."
                            )
                        parent_id = matches[0]["id"]
                    except Exception as e:
                        return HandlerResult(
                            success=False,
                            message=f"❌ Error finding parent project: {e}"
                        )

            # Create project
            try:
                result = _create_project_impl(
                    title=name,
                    parent_project_id=parent_id
                )
                project_id = result.get("id")
                parent_info = f" under **{parent}**" if parent else ""
                shared_with = result.get("shared_with", [])
                share_info = f"\nShared with: {', '.join(shared_with)}" if shared_with else ""

                return HandlerResult(
                    success=True,
                    message=f"✅ Created project **{name}**{parent_info} (ID: {project_id}){share_info}",
                    data={"keyword": "project", "delete_task": True}
                )
            except Exception as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Failed to create project: {e}"
                )

        # === DELETE PROJECT ===
        elif action == "delete":
            if not name:
                return HandlerResult(
                    success=False,
                    message="❌ Usage: `!project delete <name>`"
                )

            # Find project by name
            try:
                projects = _list_projects_impl()
                # Exact match preferred, then fuzzy
                exact = [p for p in projects if p.get("title", "").lower() == name.lower()]
                if exact:
                    target = exact[0]
                else:
                    fuzzy = [p for p in projects if name.lower() in p.get("title", "").lower()]
                    if not fuzzy:
                        return HandlerResult(
                            success=False,
                            message=f"❌ Project '{name}' not found"
                        )
                    if len(fuzzy) > 1:
                        match_list = "\n".join(f"- {m['title']}" for m in fuzzy[:5])
                        return HandlerResult(
                            success=False,
                            message=f"❌ Multiple projects match '{name}':\n{match_list}\n\nUse exact name."
                        )
                    target = fuzzy[0]

                project_id = target["id"]
                project_title = target["title"]

                _delete_project_impl(project_id)
                return HandlerResult(
                    success=True,
                    message=f"✅ Deleted project **{project_title}** (ID: {project_id})",
                    data={"keyword": "project", "delete_task": True}
                )
            except Exception as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Failed to delete project: {e}"
                )

        # === RENAME PROJECT ===
        elif action == "rename":
            # Handle "to" syntax with greedy left-match
            use_to_syntax = args.get("use_to_syntax", False)
            raw = args.get("raw", "")

            if use_to_syntax and raw:
                # Greedy left-match: find longest prefix before " to " that matches a project
                try:
                    projects = _list_projects_impl()
                    project_titles = {p["title"].lower(): p for p in projects}

                    # Find all " to " positions and try from leftmost
                    raw_lower = raw.lower()
                    to_positions = []
                    pos = 0
                    while True:
                        pos = raw_lower.find(" to ", pos)
                        if pos == -1:
                            break
                        to_positions.append(pos)
                        pos += 1

                    # Try from leftmost " to " to find a matching project
                    target = None
                    for to_pos in to_positions:
                        potential_old = raw[:to_pos].strip()  # Before " to "
                        potential_new = raw[to_pos + 4:].strip()  # After " to "

                        # Try exact match first, then fuzzy
                        if potential_old.lower() in project_titles:
                            target = project_titles[potential_old.lower()]
                            new_name = potential_new
                            break
                        else:
                            # Fuzzy match
                            matches = [p for p in projects if potential_old.lower() in p["title"].lower()]
                            if len(matches) == 1:
                                target = matches[0]
                                new_name = potential_new
                                break

                    if not target:
                        return HandlerResult(
                            success=False,
                            message=f"❌ Could not find project to rename in: `{raw}`\n\nTry: `!project rename <old> to <new>`"
                        )

                    project_id = target["id"]
                    old_title = target["title"]
                except Exception as e:
                    return HandlerResult(
                        success=False,
                        message=f"❌ Error parsing: {e}"
                    )
            else:
                # Standard parsing (using -> syntax)
                if not name or not new_name:
                    return HandlerResult(
                        success=False,
                        message="❌ Usage: `!project rename <old> to <new>`"
                    )

                # Find project by name
                try:
                    projects = _list_projects_impl()
                    exact = [p for p in projects if p.get("title", "").lower() == name.lower()]
                    if exact:
                        target = exact[0]
                    else:
                        fuzzy = [p for p in projects if name.lower() in p.get("title", "").lower()]
                        if not fuzzy:
                            return HandlerResult(
                                success=False,
                                message=f"❌ Project '{name}' not found"
                            )
                        if len(fuzzy) > 1:
                            match_list = "\n".join(f"- {m['title']}" for m in fuzzy[:5])
                            return HandlerResult(
                                success=False,
                                message=f"❌ Multiple projects match '{name}':\n{match_list}\n\nUse exact name."
                            )
                        target = fuzzy[0]

                    project_id = target["id"]
                    old_title = target["title"]
                except Exception as e:
                    return HandlerResult(
                        success=False,
                        message=f"❌ Error finding project: {e}"
                    )

            # Update project title via API
            try:
                from .server import _request
                _request("PUT", f"/api/v1/projects/{project_id}", json={"title": new_name})

                return HandlerResult(
                    success=True,
                    message=f"✅ Renamed **{old_title}** → **{new_name}**",
                    data={"keyword": "project", "delete_task": True}
                )
            except Exception as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Failed to rename project: {e}"
                )

        else:
            return HandlerResult(
                success=False,
                message=f"❌ Unknown action '{action}'. Use: add, delete, rename"
            )

    async def share_handler(
        self,
        args: dict,
        task_id: int = None,
        project_id: int = None,
        user_id: str = None,
    ) -> HandlerResult:
        """Generate public share links for a project.

        Usage:
            !share - share current project
            !share <project_name> - share specified project

        Args:
            args: {"project_name": str} - optional project name
            task_id: Current task ID
            project_id: Current project ID

        Returns:
            HandlerResult with share links for each view

        Bead: solutions-ekim
        """
        import os

        target_project_name = args.get("project_name", "").strip()
        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

        # Determine which project to share
        if target_project_name:
            # Find project by name (use user's client, not global context)
            try:
                projects = self.client.get_projects()
                exact = [p for p in projects if p.get("title", "").lower() == target_project_name.lower()]
                if exact:
                    target_project = exact[0]
                else:
                    fuzzy = [p for p in projects if target_project_name.lower() in p.get("title", "").lower()]
                    if not fuzzy:
                        return HandlerResult(
                            success=False,
                            message=f"❌ Project '{target_project_name}' not found"
                        )
                    if len(fuzzy) > 1:
                        match_list = "\n".join(f"- {m['title']}" for m in fuzzy[:5])
                        return HandlerResult(
                            success=False,
                            message=f"❌ Multiple projects match '{target_project_name}':\n{match_list}\n\nUse exact name."
                        )
                    target_project = fuzzy[0]
                target_project_id = target_project["id"]
                project_title = target_project["title"]
            except Exception as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Error finding project: {e}"
                )
        elif project_id:
            # Use current project
            target_project_id = project_id
            try:
                project_info = self.client.get_project(project_id)
                project_title = project_info.get("title", f"Project {project_id}")
            except Exception:
                project_title = f"Project {project_id}"
        else:
            return HandlerResult(
                success=False,
                message="❌ Could not determine project. Usage: `!share` or `!share <project_name>`"
            )

        # Get or create a link share for the project
        try:
            # Check for existing share
            existing_shares = self.client.get_link_shares(target_project_id)
            if existing_shares:
                # Reuse existing share
                share = existing_shares[0]
            else:
                # Create new read-only share
                share = self.client.create_link_share(target_project_id, right=0)

            share_hash = share.get("hash", "")
            if not share_hash:
                return HandlerResult(
                    success=False,
                    message="❌ Failed to get share link - no hash returned"
                )

            # Get all views for the project
            views = self.client.get_project_views(target_project_id)

            # Build share links for each view
            links = []
            if views:
                for view in views:
                    view_id = view.get("id")
                    view_title = view.get("title", "View")
                    view_kind = view.get("view_kind", "")
                    kind_emoji = {"list": "📋", "kanban": "📊", "gantt": "📅", "table": "📊"}.get(view_kind, "📄")
                    link = f"{vikunja_url}/projects/{target_project_id}/{view_id}#share-auth-token={share_hash}"
                    links.append(f"| {kind_emoji} {view_title} | [Open]({link}) |")
            else:
                # Fallback: just link to project
                link = f"{vikunja_url}/projects/{target_project_id}#share-auth-token={share_hash}"
                links.append(f"| 📋 Default | [Open]({link}) |")

            # Build response
            links_table = "\n".join(links)
            message = f"""📤 **Share Links for '{project_title}'**

| View | Link |
|------|------|
{links_table}

*Links are read-only and don't require a Vikunja account.*"""

            return HandlerResult(
                success=True,
                message=message,
                data={"keyword": "share", "keep_task": True, "project_id": target_project_id}
            )

        except VikunjaAPIError as e:
            return HandlerResult(
                success=False,
                message=f"❌ Failed to create share link: {e}"
            )
        except Exception as e:
            logger.exception(f"share_handler error: {e}")
            return HandlerResult(
                success=False,
                message=f"❌ Error: {e}"
            )

    async def delete_handler(
        self,
        args: dict,
        task_id: int = None,
        project_id: int = None,
        user_id: str = None,
    ) -> HandlerResult:
        """Delete task(s) - project-scoped for safety.

        Tier 3 (FREE):
        - !delete - delete this task
        - !delete all - delete all tasks in current project
        - !delete <id> - delete specific task (must be in same project)

        Tier 1 (LLM, costs $):
        - !delete <criteria> - LLM interprets and filters

        Args:
            args: {"target": "all"|"<id>"|"<criteria>", "task_ids": [...]}
            task_id: Current task ID (the command task)
            project_id: Current project ID (scope limiter)
            user_id: User ID for LLM budget

        Returns:
            HandlerResult with deletion status

        Bead: solutions-zfhb
        """
        target = args.get("target", "").strip().lower()
        explicit_ids = args.get("task_ids", [])

        if not task_id:
            return HandlerResult(
                success=False,
                message="❌ No task context. Run this in a task."
            )

        if not project_id:
            # Get project from current task
            try:
                task = self.client.get_task(task_id)
                project_id = task.get("project_id")
            except Exception as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Could not get task context: {e}"
                )

        # Case 1: No target = delete current task only
        if not target and not explicit_ids:
            try:
                self.client.delete_task(task_id)
                return HandlerResult(
                    success=True,
                    message=f"🗑️ Deleted task #{task_id}",
                    data={"deleted": [task_id], "delete_task": True}
                )
            except VikunjaAPIError as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Failed to delete: {e}"
                )

        # Case 2: Explicit IDs provided
        if explicit_ids:
            return await self._delete_by_ids(explicit_ids, project_id, task_id)

        # Case 3: "all" - delete all tasks in project
        if target == "all":
            return await self._delete_all_in_project(project_id, task_id)

        # Case 4: Numeric ID
        if target.isdigit():
            return await self._delete_by_ids([int(target)], project_id, task_id)

        # Case 5: Criteria string - use LLM (costs $)
        # For now, just parse simple patterns
        return await self._delete_by_criteria(target, project_id, task_id, user_id)

    async def _delete_by_ids(
        self, task_ids: list[int], project_id: int, command_task_id: int
    ) -> HandlerResult:
        """Delete specific tasks by ID (must be in same project)."""
        deleted = []
        errors = []
        skipped = []

        for tid in task_ids:
            if tid == command_task_id:
                continue  # Don't double-delete command task

            try:
                # Verify task is in same project
                task = self.client.get_task(tid)
                if task.get("project_id") != project_id:
                    skipped.append(f"#{tid} (different project)")
                    continue

                self.client.delete_task(tid)
                deleted.append(tid)
            except VikunjaAPIError as e:
                errors.append(f"#{tid}: {e}")

        # Build response
        parts = []
        if deleted:
            parts.append(f"🗑️ Deleted {len(deleted)} task(s): " + ", ".join(f"#{t}" for t in deleted))
        if skipped:
            parts.append("⚠️ Skipped (wrong project): " + ", ".join(skipped))
        if errors:
            parts.append("❌ Errors: " + ", ".join(errors))

        return HandlerResult(
            success=len(errors) == 0,
            message="\n".join(parts) if parts else "Nothing deleted",
            data={"deleted": deleted, "delete_task": True}
        )

    async def _delete_all_in_project(self, project_id: int, command_task_id: int) -> HandlerResult:
        """Delete all tasks in the current project."""
        try:
            # Get all tasks in project
            tasks = self.client.list_tasks(project_id=project_id)
            task_ids = [t["id"] for t in tasks if t["id"] != command_task_id]

            if not task_ids:
                return HandlerResult(
                    success=True,
                    message="📭 No other tasks in this project to delete.",
                    data={"deleted": [], "delete_task": True}
                )

            deleted = []
            errors = []

            for tid in task_ids:
                try:
                    self.client.delete_task(tid)
                    deleted.append(tid)
                except VikunjaAPIError as e:
                    errors.append(f"#{tid}: {e}")

            parts = [f"🗑️ Deleted {len(deleted)} task(s) from project"]
            if errors:
                parts.append("❌ Errors: " + ", ".join(errors))

            return HandlerResult(
                success=len(errors) == 0,
                message="\n".join(parts),
                data={"deleted": deleted, "delete_task": True}
            )

        except Exception as e:
            return HandlerResult(
                success=False,
                message=f"❌ Failed to list/delete tasks: {e}"
            )

    async def _delete_by_criteria(
        self, criteria: str, project_id: int, command_task_id: int, user_id: str = None
    ) -> HandlerResult:
        """Delete tasks matching criteria (uses LLM for interpretation).

        Examples:
        - "completed" → delete done tasks
        - "related to music" → semantic match
        - "everything except instruments" → inverse match
        """
        # Simple pattern matching first (free)
        criteria_lower = criteria.lower()

        # "completed" / "done" - delete completed tasks
        if criteria_lower in ("completed", "done", "finished"):
            try:
                tasks = self.client.list_tasks(project_id=project_id)
                done_ids = [t["id"] for t in tasks if t.get("done") and t["id"] != command_task_id]

                if not done_ids:
                    return HandlerResult(
                        success=True,
                        message="📭 No completed tasks to delete.",
                        data={"deleted": [], "delete_task": True}
                    )

                return await self._delete_by_ids(done_ids, project_id, command_task_id)

            except Exception as e:
                return HandlerResult(
                    success=False,
                    message=f"❌ Failed: {e}"
                )

        # For complex criteria, would use LLM - for now just explain
        # TODO: Implement LLM-based criteria matching (costs $)
        return HandlerResult(
            success=False,
            message=f"❌ Complex criteria not yet supported: `{criteria}`\n\n"
                    f"**Supported:**\n"
                    f"- `!delete` - delete this task\n"
                    f"- `!delete all` - delete all in project\n"
                    f"- `!delete <id>` - delete by ID\n"
                    f"- `!delete done` - delete completed tasks\n\n"
                    f"*LLM-powered criteria matching coming soon.*"
        )

    async def token_handler(
        self,
        args: dict,
        task_id: int = None,
        project_id: int = None,
        user_id: str = None,
    ) -> HandlerResult:
        """Generate MCP config for Claude Desktop.

        Creates a ready-to-paste JSON config block that users can add to their
        Claude Desktop claude_desktop_config.json file.

        This creates a permanent API token using the user's stored JWT.

        Args:
            args: {} (no args needed)
            task_id: Current task ID
            project_id: Current project ID
            user_id: User ID (vikunja:<username>:<id>)

        Returns:
            HandlerResult with MCP config JSON

        Bead: fa-jmdf
        """
        import json
        import os
        import httpx
        from datetime import datetime, timedelta

        if not user_id:
            return HandlerResult(
                success=False,
                message="❌ Could not determine your user. Please try again."
            )

        vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

        # Normalize user_id - strip numeric ID suffix if present
        # Notifications use "vikunja:username:123" but personal_bots uses "vikunja:username"
        normalized_user_id = user_id
        parts = user_id.split(":")
        if len(parts) == 3 and parts[2].isdigit():
            normalized_user_id = f"{parts[0]}:{parts[1]}"

        # Get user's stored JWT from personal_bots table
        from .bot_provisioning import get_bot_owner_token
        jwt_token = get_bot_owner_token(normalized_user_id)

        if not jwt_token:
            return HandlerResult(
                success=False,
                message=(
                    "❌ **No authentication found.**\n\n"
                    "Your account may need to be reconnected.\n"
                    "Please contact support for help."
                )
            )

        # Create a permanent API token via Vikunja API
        try:
            # Generate a unique token title
            token_title = f"Claude Desktop ({datetime.now().strftime('%Y-%m-%d')})"

            # First, get available permissions from /api/v1/routes
            routes_response = httpx.get(
                f"{vikunja_url}/api/v1/routes",
                headers={"Authorization": f"Bearer {jwt_token}"},
                timeout=30.0
            )
            routes_response.raise_for_status()
            routes = routes_response.json()

            # Build permissions dict from available routes (all permissions)
            permissions = {}
            for group, group_routes in routes.items():
                if isinstance(group_routes, dict):
                    permissions[group] = list(group_routes.keys())

            # Set expiry to 1 year
            expiry_date = datetime.now() + timedelta(days=365)

            # Vikunja API uses PUT for token creation, not POST
            response = httpx.put(
                f"{vikunja_url}/api/v1/tokens",
                headers={"Authorization": f"Bearer {jwt_token}"},
                json={
                    "title": token_title,
                    "expires_at": expiry_date.isoformat() + "Z",
                    "permissions": permissions
                },
                timeout=30.0
            )

            if response.status_code == 401:
                return HandlerResult(
                    success=False,
                    message=(
                        "❌ **Session expired.**\n\n"
                        "Your authentication has expired. Please:\n"
                        "1. Go to [Vikunja Settings](https://vikunja.factumerit.app/user/settings/api-tokens)\n"
                        "2. Create a new API token manually\n"
                        "3. Use that token in your Claude Desktop config"
                    )
                )

            response.raise_for_status()
            token_data = response.json()
            token = token_data.get("token", "")

            if not token:
                raise ValueError("No token in response")

        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to create API token: {e.response.status_code} - {e.response.text[:200]}")
            return HandlerResult(
                success=False,
                message=(
                    f"❌ **Failed to create token** (HTTP {e.response.status_code})\n\n"
                    "Please create a token manually:\n"
                    "1. Go to [Vikunja Settings > API Tokens](https://vikunja.factumerit.app/user/settings/api-tokens)\n"
                    "2. Create a new token with all permissions\n"
                    "3. Copy the token for your Claude Desktop config"
                )
            )
        except Exception as e:
            logger.error(f"Token creation error: {e}")
            return HandlerResult(
                success=False,
                message=(
                    "❌ **Error creating token.**\n\n"
                    "Please create a token manually:\n"
                    "1. Go to [Vikunja Settings > API Tokens](https://vikunja.factumerit.app/user/settings/api-tokens)\n"
                    "2. Create a new token with all permissions\n"
                    "3. Copy the token for your Claude Desktop config"
                )
            )

        # Build MCP config JSON
        mcp_config = {
            "mcpServers": {
                "vikunja": {
                    "command": "uvx",
                    "args": ["vikunja-mcp"],
                    "env": {
                        "VIKUNJA_URL": vikunja_url,
                        "VIKUNJA_TOKEN": token
                    }
                }
            }
        }

        # Format as pretty JSON
        config_json = json.dumps(mcp_config, indent=2)

        # Build response with instructions
        message = f"""🔧 **Claude Desktop MCP Config**

Add this to your `claude_desktop_config.json`:

```json
{config_json}
```

**Setup Instructions:**

1. Open Claude Desktop settings
2. Find `claude_desktop_config.json`:
   - **macOS**: `~/Library/Application Support/Claude/`
   - **Windows**: `%APPDATA%\\Claude\\`
3. Add the config above (merge if you have existing servers)
4. Restart Claude Desktop

**Test it:**
> "What's on my todo list today?"

---
*Token starts with: {token[:12]}...*"""

        # Delete previous token tasks in this project
        if project_id and task_id:
            self._delete_previous_info_tasks(project_id, task_id, "!token", "!mcp", "MCP Config")

        return HandlerResult(
            success=True,
            message=message,
            data={
                "keyword": "token",
                "keep_task": True,
                "smart_title": "🔧 Claude Desktop Config"
            }
        )

    async def whoami_handler(
        self,
        args: dict,
        task_id: int = None,
        project_id: int = None,
        user_id: str = None,
    ) -> HandlerResult:
        """Show user's bot info (username and display name).

        Args:
            args: {} (no args needed)
            task_id: Current task ID
            project_id: Current project ID
            user_id: User ID (vikunja:<username>:<id>)

        Returns:
            HandlerResult with bot info
        """
        if not user_id:
            return HandlerResult(
                success=False,
                message="❌ Could not determine your user."
            )

        # Get bot credentials for this user
        from .bot_provisioning import get_bot_credentials

        bot_creds = get_bot_credentials(user_id)
        if not bot_creds:
            return HandlerResult(
                success=False,
                message="❌ No bot configured for your account."
            )

        message = f"""**Your @eis Bot**

- **Username**: `{bot_creds.username}`
- **Display Name**: {bot_creds.display_name or bot_creds.username}

Mention `@{bot_creds.username}` in task titles to trigger commands."""

        return HandlerResult(
            success=True,
            message=message,
            data={"keyword": "whoami", "keep_task": True, "smart_title": f"Bot: @{bot_creds.username}"}
        )

    def get_handler(self, handler_name: str):
        """Get handler method by name.

        Args:
            handler_name: Handler name from CommandParser (e.g., "complete_task")

        Returns:
            Handler method or None if not found
        """
        return getattr(self, handler_name, None)
