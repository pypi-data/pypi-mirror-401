"""
Notification Poller for @eis Smart Tasks.

Polls Vikunja notifications API to detect @eis mentions.
Much more efficient than webhooks (only processes mentions, not all events).

Architecture:
    User mentions @eis in task/comment
        ↓
    Vikunja creates notification for @eis user
        ↓
    Poller detects notification
        ↓
    CommandParser extracts command
        ↓
    KeywordHandlers executes command
        ↓
    Bot adds comment with result
        ↓
    Notification marked as read

Based on: docs/factumerit/101-SMART_TASKS_IMPLEMENTATION.md
Bead: solutions-klfj, solutions-hgwx.1
"""

import asyncio
import logging
import re
from typing import Optional

import markdown

from .vikunja_client import BotVikunjaClient, VikunjaAPIError
from .command_parser import CommandParser
from .keyword_handlers import KeywordHandlers

logger = logging.getLogger(__name__)

# Status labels for @eis processing visual feedback
# These are emoji-only labels shown on tasks during/after processing
STATUS_LABELS = {
    "thinking": "⏳",      # Processing in progress
    "success": "🤖",       # Successfully handled
    "needs_input": "💬",   # Question/clarification needed
    "error": "❌",         # Error occurred
}

# Cache label IDs to avoid repeated API lookups
_label_id_cache: dict[str, int] = {}

# Schedule to seconds conversion for Vikunja repeat_after
SCHEDULE_TO_SECONDS = {
    "hourly": 3600,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "12h": 43200,
    "daily": 86400,
    "24h": 86400,
}


def _schedule_to_repeat_after(schedule: str) -> int:
    """Convert schedule string to Vikunja repeat_after seconds.

    Args:
        schedule: Schedule string like 'hourly', '6h', 'daily'

    Returns:
        Seconds for repeat_after, or 0 if unknown
    """
    return SCHEDULE_TO_SECONDS.get(schedule.lower(), 0)


def _response_needs_input(response: str) -> bool:
    """Detect if response indicates @eis is asking for user input.

    Args:
        response: The response message from @eis

    Returns:
        True if response contains a question or asks for clarification
    """
    if not response:
        return False

    # Check for question patterns
    question_patterns = [
        "?",  # Direct question
        "which one",
        "which project",
        "do you want",
        "would you like",
        "should i",
        "please clarify",
        "please specify",
        "could you",
        "can you tell me",
        "let me know",
        "confirmation required",
    ]

    response_lower = response.lower()
    return any(pattern in response_lower for pattern in question_patterns)


def md_to_html(text: str) -> str:
    """Convert markdown to HTML for Vikunja descriptions."""
    return markdown.markdown(text, extensions=['fenced_code', 'tables'])


def strip_html(text: str) -> str:
    """Strip HTML tags from text (for parsing commands from Vikunja)."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _format_cost_footer(handler_data: dict) -> str:
    """Format cost footer from handler data.

    Args:
        handler_data: Dict with model, tokens, cost, tools

    Returns:
        Formatted footer like "Sonnet | 1234 (+3 comments)→567 tokens | tools: 1/10 | ~0.02¢"
    """
    model = handler_data.get("model", "")
    tokens = handler_data.get("tokens", "")
    cost = handler_data.get("cost", "")
    tools = handler_data.get("tools", "")

    parts = []
    if model:
        parts.append(model)
    if tokens:
        parts.append(f"{tokens} tokens")
    if tools:
        parts.append(f"tools: {tools}")
    if cost:
        parts.append(cost)
    return " | ".join(parts)


class NotificationPoller:
    """Polls Vikunja notifications for @eis mentions.

    Usage:
        poller = NotificationPoller()
        await poller.start()  # Runs forever, polling every 10 seconds
    """

    def __init__(
        self,
        poll_interval: float = 10.0,
        client: Optional[BotVikunjaClient] = None
    ):
        """Initialize poller.

        Args:
            poll_interval: Seconds between polls (default 10)
            client: BotVikunjaClient instance (creates one if not provided)
        """
        self.poll_interval = poll_interval
        self.client = client or BotVikunjaClient()
        self.parser = CommandParser()
        self.handlers = KeywordHandlers(self.client)
        self._running = False
        self._processed_ids: set[int] = set()  # Track processed notifications
        self._processed_comment_ids: set[int] = set()  # Track processed comments (ears mode)
        self._scheduler = None  # Task scheduler (lazy init)
        self._ears_scan_interval = 30  # seconds between ears scans
        self._ears_scan_counter = 0  # Counter for ears scan timing
        # Skip notifications older than startup to prevent backlog reprocessing after deploy
        from datetime import datetime, timezone
        self._startup_time = datetime.now(timezone.utc)
        # Cache bot info for comment scanning
        self._bot_username: Optional[str] = None  # Bot's username for EARS matching
        self._bot_display_name: Optional[str] = None

    def _get_label_id(self, status: str) -> int:
        """Get or create a status label and return its ID.

        Args:
            status: One of 'thinking', 'success', 'needs_input', 'error'

        Returns:
            Label ID
        """
        global _label_id_cache

        if status in _label_id_cache:
            return _label_id_cache[status]

        emoji = STATUS_LABELS.get(status)
        if not emoji:
            raise ValueError(f"Unknown status: {status}")

        try:
            label = self.client.get_or_create_label(emoji)
            _label_id_cache[status] = label["id"]
            return label["id"]
        except Exception as e:
            logger.warning(f"Failed to get/create label '{emoji}': {e}")
            raise

    def _set_status_label(self, task_id: int, status: str) -> None:
        """Set status label on task, removing any other status labels.

        Args:
            task_id: Task ID
            status: One of 'thinking', 'success', 'needs_input', 'error'
        """
        try:
            # Get current labels on task
            current_labels = self.client.get_task_labels(task_id)
            status_emojis = set(STATUS_LABELS.values())

            # Remove any existing status labels
            for label in current_labels:
                if label.get("title") in status_emojis:
                    try:
                        self.client.remove_label_from_task(task_id, label["id"])
                    except Exception as e:
                        logger.debug(f"Failed to remove label {label['id']}: {e}")

            # Add new status label
            label_id = self._get_label_id(status)
            self.client.add_label_to_task(task_id, label_id)
            logger.debug(f"Set status '{status}' on task {task_id}")

        except Exception as e:
            logger.warning(f"Failed to set status label on task {task_id}: {e}")
            # Don't fail the whole operation for label issues

    async def start(self):
        """Start the polling loop (runs forever)."""
        self._running = True
        print(f"[POLLER] Starting notification poller (interval: {self.poll_interval}s)", flush=True)
        logger.info(f"Starting notification poller (interval: {self.poll_interval}s)")

        # Start the task scheduler
        from .task_scheduler import get_task_scheduler
        self._scheduler = get_task_scheduler(self.client)
        await self._scheduler.start(scan_existing=False)  # Don't scan on startup for now

        # Note: Can't clear stale notifications - Vikunja API doesn't work as expected
        # We rely on _processed_ids to skip already-handled notifications

        while self._running:
            try:
                await self._poll_once()
            except Exception as e:
                logger.exception(f"Error in polling loop: {e}")

            # Run ears scan periodically
            self._ears_scan_counter += self.poll_interval
            if self._ears_scan_counter >= self._ears_scan_interval:
                try:
                    await self._scan_ears_projects()
                except Exception as e:
                    logger.exception(f"Error in ears scan: {e}")
                self._ears_scan_counter = 0

            await asyncio.sleep(self.poll_interval)

    def stop(self):
        """Stop the polling loop."""
        self._running = False
        logger.info("Stopping notification poller")

    async def _scan_ears_projects(self):
        """Scan ears-enabled projects (!ears on) for new unprocessed tasks AND comments.

        Only processes items created after ears mode was enabled.
        Only scans projects the bot has access to (filters out 403 errors).
        """
        from .server import _get_ears_enabled_projects

        try:
            ears_projects = _get_ears_enabled_projects()
        except Exception as e:
            logger.error(f"Failed to get ears projects: {e}")
            return

        if not ears_projects:
            return

        # Get bot's accessible projects to filter EARS list
        try:
            accessible_projects = self.client.get_projects()
            accessible_ids = {p.get("id") for p in accessible_projects}
        except Exception as e:
            logger.warning(f"Failed to get accessible projects, scanning all EARS projects: {e}")
            accessible_ids = None  # Scan all if we can't get the list

        for project_id, ears_since in ears_projects:
            # Skip projects the bot doesn't have access to
            if accessible_ids is not None and project_id not in accessible_ids:
                continue

            try:
                # Scan tasks
                await self._scan_project_for_ears(project_id, ears_since)
                # Scan comments (solutions-hx4u)
                await self._scan_project_comments(project_id, ears_since)
            except Exception as e:
                logger.error(f"Error scanning project {project_id}: {e}")

    async def _scan_project_for_ears(self, project_id: int, ears_since: str):
        """Scan a single ears-enabled project for tasks to process.

        Args:
            project_id: Project ID to scan
            ears_since: ISO timestamp - only process tasks created after this
        """
        from datetime import datetime

        try:
            tasks = self.client.get_project_tasks(project_id)
        except VikunjaAPIError as e:
            logger.error(f"Failed to get tasks for project {project_id}: {e}")
            return

        if not tasks:
            return

        # Parse ears_since timestamp
        try:
            since_dt = datetime.fromisoformat(ears_since.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            logger.warning(f"Invalid ears_since timestamp: {ears_since}")
            return

        for task in tasks:
            # Skip tasks created before ears was enabled
            created_at = task.get("created", "")
            if not created_at:
                continue
            try:
                created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if created_dt <= since_dt:
                    continue
            except (ValueError, TypeError):
                continue

            # Skip if already has 🤖 label (already processed)
            labels = task.get("labels") or []
            if any(l.get("title") == "🤖" for l in labels):
                continue

            # Skip if already has any status label (being processed or was processed)
            status_emojis = set(STATUS_LABELS.values())
            if any(l.get("title") in status_emojis for l in labels):
                continue

            # Process this task
            await self._process_ears_task(task, project_id)

    async def _process_ears_task(self, task: dict, project_id: int):
        """Process a task in an ears-enabled project (!ears on).

        Args:
            task: Task object from Vikunja API
            project_id: Project ID the task is in
        """
        from .server import _generate_action_token
        import os

        task_id = task["id"]
        title = task.get("title", "")

        print(f"[EARS] Processing task #{task_id}: {title[:50]}", flush=True)

        # Set thinking label while processing
        self._set_status_label(task_id, "thinking")

        # Parse as natural language (implicit @eis - all ears tasks go to LLM)
        result = self.parser.parse(title, implicit_mention=True)

        # Get project name for context
        project_name = None
        try:
            project_info = self.client.get_project(project_id)
            project_name = project_info.get("title", "")
        except Exception:
            project_name = f"Project {project_id}"

        # Extract task creator for project sharing (solutions-2dum)
        user_id = None
        created_by = task.get("created_by", {})
        if isinstance(created_by, dict):
            username = created_by.get("username", "")
            if username:
                # Use consistent format without numeric_id (fa-2y1z)
                user_id = f"vikunja:{username}"

        # Execute command
        response_message, is_success, handler_data = await self._execute_command(
            result,
            task_id=task_id,
            project_id=project_id,
            project_name=project_name,
            user_id=user_id,
        )

        print(f"[EARS] Result for #{task_id}: success={is_success}", flush=True)

        # Build ears footer with turn-off link
        mcp_url = os.environ.get("MCP_URL", "https://mcp.factumerit.app")
        off_token = _generate_action_token("ears-off", project_id)
        off_url = f"{mcp_url}/ears-off/{project_id}/{off_token}"
        ears_footer = f"\n\n---\n🤖 *Processed by ears* · [Turn off]({off_url})"

        # Update task based on result type
        if result.tier == "tier_natural":
            # Natural language: update description with response
            try:
                # Clean up title - remove @eis prefix if present
                clean_title = re.sub(r'^@e(is)?\s*', '', title).strip()
                if not clean_title:
                    clean_title = "Captured Task"

                # Convert response to HTML with capture footer
                html_description = md_to_html(response_message + ears_footer)

                # Add cost footer if available
                if handler_data and handler_data.get("cost"):
                    footer = _format_cost_footer(handler_data)
                    html_description += f"\n<p><small>{footer}</small></p>"

                self.client.update_task(task_id, title=clean_title, description=html_description)
                logger.info(f"Updated ears task #{task_id}")
            except VikunjaAPIError as e:
                self._log_api_error(f"update ears task #{task_id}", e)
                self._set_status_label(task_id, "error")
                return
        elif result.tier == "tier3" and handler_data and handler_data.get("keep_task"):
            # Info command: update description with result
            try:
                from .metadata_manager import MetadataManager, SmartTaskMetadata

                # Generate smart title
                clean_title = self._generate_smart_title(handler_data, title)

                # Build action bar
                action_bar = self._build_action_bar(task_id, handler_data)

                # Replace refresh hint with action bar
                message_with_links = re.sub(
                    r'💬 \*Reply `@eis.*?` to refresh\*',
                    action_bar,
                    response_message
                )

                # Create metadata
                keyword = handler_data.get("keyword", "info")
                handler_args = handler_data.get("handler_args", {})
                metadata = SmartTaskMetadata(
                    keyword=keyword,
                    handler_args=handler_args,
                    schedule=handler_data.get("schedule"),
                )

                # Convert to HTML with capture footer
                html_content = md_to_html(message_with_links + ears_footer)
                html_description = MetadataManager.format_html(metadata, html_content)

                self.client.update_task(task_id, title=clean_title, description=html_description)
                logger.info(f"Updated ears info task #{task_id}")
            except VikunjaAPIError as e:
                self._log_api_error(f"update ears info task #{task_id}", e)
                self._set_status_label(task_id, "error")
                return
        elif not is_success:
            # Error: add as comment
            try:
                html_comment = md_to_html(response_message + ears_footer)
                self.client.add_comment(task_id, html_comment)
            except VikunjaAPIError as e:
                self._log_api_error(f"add error comment to ears task #{task_id}", e)
            self._set_status_label(task_id, "error")
            return

        # Set success label
        if _response_needs_input(response_message):
            self._set_status_label(task_id, "needs_input")
        else:
            self._set_status_label(task_id, "success")

    def _get_bot_info(self) -> tuple[str, str]:
        """Get bot's username and display name (cached).

        Priority:
        1. Personal bot: Look up from personal_bots table (if user_id set)
        2. Shared bot: Use env vars VIKUNJA_BOT_USERNAME, VIKUNJA_BOT_DISPLAY_NAME

        Fixes solutions-5yv5: bot token doesn't have /api/v1/user permission.

        Returns:
            Tuple of (username, display_name)
        """
        import os
        if self._bot_username is None or self._bot_display_name is None:
            # Try personal bot lookup first (if user_id is set on client)
            user_id = getattr(self.client, 'user_id', None)
            if user_id:
                try:
                    from .bot_provisioning import get_user_bot_info
                    bot_info = get_user_bot_info(user_id)
                    if bot_info:
                        self._bot_username = bot_info["bot_username"]
                        self._bot_display_name = bot_info["display_name"]
                        logger.info(f"[EARS] Bot info from DB: username='{self._bot_username}', display='{self._bot_display_name}'")
                        return (self._bot_username, self._bot_display_name)
                except Exception as e:
                    logger.warning(f"[EARS] Could not get bot info from DB: {e}")

            # Fallback to env vars (shared bot mode)
            bot_username = os.environ.get("VIKUNJA_BOT_USERNAME", "eis")
            display_name = os.environ.get("VIKUNJA_BOT_DISPLAY_NAME", bot_username)
            self._bot_username = bot_username
            self._bot_display_name = display_name
            logger.info(f"[EARS] Bot info from env: username='{bot_username}', display='{display_name}'")

        return (self._bot_username, self._bot_display_name)

    async def _scan_project_comments(self, project_id: int, ears_since: str):
        """Scan comments in an ears-enabled project for @-free invocation.

        When !ears on is enabled, users can mention the bot by display name
        without @ (e.g., "jarvis what's for dinner?" instead of "@jarvis ...").

        Args:
            project_id: Project ID to scan
            ears_since: ISO timestamp - only process comments created after this

        Bead: solutions-hx4u
        """
        from datetime import datetime

        bot_username, bot_display_name = self._get_bot_info()
        if not bot_username:
            return

        # Normalize display name for matching (case-insensitive)
        display_name_lower = bot_display_name.lower()

        try:
            tasks = self.client.get_project_tasks(project_id)
        except VikunjaAPIError as e:
            logger.error(f"[EARS] Failed to get tasks for project {project_id}: {e}")
            return

        if not tasks:
            return

        # Parse ears_since timestamp
        try:
            since_dt = datetime.fromisoformat(ears_since.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            logger.warning(f"[EARS] Invalid ears_since timestamp: {ears_since}")
            return

        for task in tasks:
            task_id = task["id"]

            try:
                comments = self.client.get_comments(task_id)
            except VikunjaAPIError:
                continue  # Skip tasks we can't read comments for

            if not comments:
                continue

            for comment in comments:
                comment_id = comment.get("id")
                if not comment_id:
                    continue

                # Skip already processed
                if comment_id in self._processed_comment_ids:
                    continue

                # Skip bot's own comments (match by username since we may not have numeric ID)
                author = comment.get("author", {})
                if author.get("username", "").lower() == bot_username.lower():
                    continue

                # Skip old comments
                created_at = comment.get("created", "")
                if not created_at:
                    continue
                try:
                    created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if created_dt <= since_dt:
                        continue
                except (ValueError, TypeError):
                    continue

                # Check if comment mentions bot display name (case-insensitive)
                comment_text = comment.get("comment", "")
                if display_name_lower not in comment_text.lower():
                    continue

                # Mark as processed before handling (avoid re-processing on error)
                self._processed_comment_ids.add(comment_id)

                # Process this comment as a command
                await self._process_ears_comment(
                    comment=comment,
                    task_id=task_id,
                    project_id=project_id,
                    bot_display_name=bot_display_name,
                )

    async def _process_ears_comment(
        self,
        comment: dict,
        task_id: int,
        project_id: int,
        bot_display_name: str,
    ):
        """Process a comment detected by ears mode (!ears on).

        Extracts the command from the comment text (removing the display name prefix)
        and executes it as if the user had mentioned @eis.

        Args:
            comment: Comment object from Vikunja API
            task_id: Task ID the comment is on
            project_id: Project ID
            bot_display_name: The bot's display name to strip from command

        Bead: solutions-hx4u
        """

        comment_id = comment.get("id")
        comment_text = comment.get("comment", "").strip()
        author = comment.get("author", {})
        author_name = author.get("username", "user")

        print(f"[EARS] Processing comment #{comment_id} on task #{task_id}: {comment_text[:50]}", flush=True)

        # Strip the display name from the start of the comment (case-insensitive)
        # Handle variations: "jarvis ...", "Jarvis, ...", "jarvis: ..."
        pattern = rf'^{re.escape(bot_display_name)}[,:\s]*'
        command_text = re.sub(pattern, '', comment_text, flags=re.IGNORECASE).strip()

        if not command_text:
            # Just mentioned the name with no command - skip
            logger.debug(f"[EARS] Comment #{comment_id} has no command after display name, skipping")
            return

        # Parse as natural language (implicit @eis)
        result = self.parser.parse(command_text, implicit_mention=True)

        # Get project name for context
        project_name = None
        try:
            project_info = self.client.get_project(project_id)
            project_name = project_info.get("title", "")
        except Exception:
            project_name = f"Project {project_id}"

        # Build conversation context from prior comments
        conversation_context = await self._build_comment_context(task_id, comment_id)

        # Get user_id for budget tracking (consistent format, fa-2y1z)
        user_id = f"vikunja:{author_name}"

        # Execute command
        response_message, is_success, handler_data = await self._execute_command(
            result,
            task_id=task_id,
            project_id=project_id,
            project_name=project_name,
            conversation_context=conversation_context,
            user_id=user_id,
        )

        print(f"[EARS] Result for comment #{comment_id}: success={is_success}", flush=True)

        # Add response as comment
        try:
            html_comment = md_to_html(response_message)
            self.client.add_comment(task_id, html_comment)
            logger.info(f"[EARS] Replied to comment #{comment_id} on task #{task_id}")
        except VikunjaAPIError as e:
            self._log_api_error(f"reply to comment #{comment_id}", e)

    async def _build_comment_context(self, task_id: int, current_comment_id: int) -> str:
        """Build conversation context from prior comments on a task.

        Args:
            task_id: Task to get comments from
            current_comment_id: Current comment ID to exclude

        Returns:
            Formatted string of prior comments for LLM context
        """
        try:
            comments = self.client.get_comments(task_id)
        except VikunjaAPIError:
            return ""

        if not comments:
            return ""

        # Filter out the current comment
        prior_comments = [c for c in comments if c.get("id") != current_comment_id]

        if not prior_comments:
            return ""

        # Format as conversation
        lines = []
        for c in prior_comments[-5:]:  # Last 5 comments for context
            author = c.get("author", {}).get("username", "user")
            text = c.get("comment", "")
            lines.append(f"**{author}:** {text}")

        return "\n\n".join(lines)

    async def _poll_once(self):
        """Poll for notifications and process any @eis mentions."""
        try:
            notifications = self.client.get_notifications()
            # Handle null/None response from API
            if notifications is None:
                notifications = []
        except VikunjaAPIError as e:
            logger.error(f"Failed to get notifications: {e}")
            return
        except Exception as e:
            logger.exception(f"Unexpected error getting notifications: {e}")
            return

        if not notifications:
            return

        # Filter to notifications we haven't processed
        new_notifications = [
            n for n in notifications
            if n.get("id") not in self._processed_ids
            and n.get("name") in ("task.assigned", "task.comment")
        ]

        if new_notifications:
            types = [n.get("name") for n in new_notifications]
            print(f"[POLLER] Found {len(new_notifications)} new notification(s): {types}", flush=True)

        for notification in notifications:
            notification_id = notification.get("id")
            # Skip already processed
            if notification_id in self._processed_ids:
                continue
            await self._process_notification(notification)

    async def _process_notification(self, notification: dict):
        """Process a single notification.

        Args:
            notification: Notification object from Vikunja API
        """
        notification_id = notification.get("id")

        # Skip already processed (in-memory dedup)
        if notification_id in self._processed_ids:
            return

        # Skip already read notifications
        # Note: '0001-01-01T00:00:00Z' is Go's zero time, meaning "not read yet"
        read_at = notification.get("read_at", "")
        if read_at and read_at != "0001-01-01T00:00:00Z":
            return

        # Skip notifications older than server startup (prevents backlog reprocessing after deploy)
        created_at = notification.get("created", "")
        if created_at:
            try:
                from datetime import datetime
                # Parse ISO format: "2026-01-03T07:47:00Z"
                created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if created_dt < self._startup_time:
                    # Mark as processed so we don't log this every poll
                    self._processed_ids.add(notification_id)
                    return
            except Exception:
                pass  # If we can't parse, process it anyway

        # Extract notification details
        notification_type = notification.get("name", "")

        # Process task.assigned (new command tasks) and task.comment (refinement)
        if notification_type == "task.assigned":
            await self._process_command_task(notification)
        elif notification_type == "task.comment":
            await self._process_comment(notification)
        else:
            # Skip other notification types
            self._processed_ids.add(notification_id)
            return

    async def _process_command_task(self, notification: dict):
        """Process a task.assigned notification (new command task).

        Args:
            notification: Notification object from Vikunja API
        """
        notification_id = notification.get("id")
        task_id = self._extract_task_id(notification)
        text = self._extract_text(notification)

        print(f"[POLLER] Processing task.assigned: task_id={task_id}, text={text[:200] if text else 'EMPTY'}", flush=True)

        if not text:
            print(f"[POLLER] No text found, marking read", flush=True)
            self._mark_read(notification_id)
            self._processed_ids.add(notification_id)
            return

        logger.info(f"Processing command task {notification_id}: {text[:100]}")

        # Parse command (implicit_mention=True because @mention was converted to assignment)
        result = self.parser.parse(text, implicit_mention=True)

        if result.tier == "unknown":
            logger.debug(f"Not a valid @eis command: {result.error}")
            self._mark_read(notification_id)
            self._processed_ids.add(notification_id)
            return

        # Set "thinking" status label while processing
        if task_id:
            self._set_status_label(task_id, "thinking")

        # Fetch task for project context (needed for LLM tiers)
        project_id = None
        project_name = None
        if result.tier in ("tier_natural", "tier1", "tier2") and task_id:
            try:
                task_info = self.client.get_task(task_id)
                project_id = task_info.get("project_id")
                # Get project name if we have project_id
                if project_id:
                    try:
                        project_info = self.client.get_project(project_id)
                        project_name = project_info.get("title", "")
                    except Exception:
                        project_name = f"Project {project_id}"
            except Exception as e:
                logger.warning(f"Could not fetch task {task_id} for project context: {e}")

        # Extract user ID for budget tracking
        # Debug: Log notification structure to understand user ID extraction
        notif_data = notification.get("notification", {})
        doer = notif_data.get("doer", {})
        task_creator = notif_data.get("task", {}).get("created_by", {})
        logger.info(f"[POLLER] Notification doer: username={doer.get('username')}, id={doer.get('id')}")
        logger.info(f"[POLLER] Task creator: username={task_creator.get('username') if isinstance(task_creator, dict) else 'N/A'}, id={task_creator.get('id') if isinstance(task_creator, dict) else 'N/A'}")
        user_id = self._extract_user_id(notification)

        # Execute command
        response_message, is_success, handler_data = await self._execute_command(
            result,
            task_id=task_id,
            project_id=project_id,
            project_name=project_name,
            user_id=user_id,
        )

        print(f"[POLLER] Command result: {response_message[:100]}", flush=True)

        # Handle based on tier
        if result.tier == "tier_natural":
            # Natural language with tools: Update task description with result
            try:
                current_task = self.client.get_task(task_id)
                original_title = current_task.get("title", "")

                # Clean up title - remove @eis prefix
                clean_title = re.sub(r'^@e(is)?\s*', '', original_title).strip()
                if not clean_title:
                    clean_title = "Query Result"

                # Convert response to HTML
                html_description = md_to_html(response_message)

                # Add cost footer if available
                if handler_data and handler_data.get("cost"):
                    footer = _format_cost_footer(handler_data)
                    html_description += f"\n<p><small>{footer}</small></p>"

                self.client.update_task(task_id, title=clean_title, description=html_description)
                logger.info(f"Updated tool response task #{task_id}")
                print(f"[POLLER] Updated tool response #{task_id}: {clean_title}", flush=True)

                # Set outcome label based on response
                if _response_needs_input(response_message):
                    self._set_status_label(task_id, "needs_input")
                else:
                    self._set_status_label(task_id, "success")
            except VikunjaAPIError as e:
                self._log_api_error(f"handle tier_natural for task #{task_id}", e)
                self._set_status_label(task_id, "error")
        elif result.tier in ("tier1", "tier2"):
            # LLM tier: Keep the task and update description with HTML + metadata
            try:
                from .metadata_manager import MetadataManager

                current_task = self.client.get_task(task_id)
                original_title = current_task.get("title", "")
                # Clean up title - remove @eis prefix and/or $ symbols
                # @eis may have been converted to assignment, so title might be just "$ ..."
                clean_title = re.sub(r'^(@e(is)?\s*)?\$+\s*', '', original_title).strip()
                if not clean_title:
                    clean_title = "Smart Task"

                # Get metadata from handler result
                metadata = handler_data.get("metadata") if handler_data else None

                # Convert markdown to HTML and embed metadata
                html_content = md_to_html(response_message)
                if metadata:
                    html_description = MetadataManager.format_html(metadata, html_content)
                else:
                    html_description = html_content

                self.client.update_task(task_id, title=clean_title, description=html_description)
                logger.info(f"Updated smart task #{task_id} with LLM response")
                print(f"[POLLER] Updated smart task #{task_id}: {clean_title}", flush=True)

                # Set outcome label
                if _response_needs_input(response_message):
                    self._set_status_label(task_id, "needs_input")
                else:
                    self._set_status_label(task_id, "success")
            except VikunjaAPIError as e:
                self._log_api_error(f"update smart task #{task_id}", e)
                self._set_status_label(task_id, "error")
        elif is_success:
            # Check if this is a scheduled task (weather/stock/news with schedule)
            if handler_data and handler_data.get("schedule"):
                # Keep the task, update with content, register schedule
                try:
                    from .metadata_manager import MetadataManager, SmartTaskMetadata
                    from .task_scheduler import get_task_scheduler

                    current_task = self.client.get_task(task_id)
                    original_title = current_task.get("title", "")

                    # Generate smart title from API response data (includes schedule)
                    clean_title = self._generate_smart_title(handler_data, original_title)

                    # Create metadata with schedule
                    metadata = SmartTaskMetadata(
                        keyword=handler_data.get("keyword"),
                        schedule=handler_data.get("schedule"),
                    )

                    # Convert to HTML and embed metadata
                    html_content = md_to_html(response_message)
                    html_description = MetadataManager.format_html(metadata, html_content)

                    # Set repeat_after for Vikunja's native recurrence (shows icon)
                    schedule = handler_data.get("schedule")
                    repeat_after = _schedule_to_repeat_after(schedule)

                    self.client.update_task(
                        task_id,
                        title=clean_title,
                        description=html_description,
                        repeat_after=repeat_after,
                        repeat_mode=0,  # Repeat from due date
                    )

                    # Register with scheduler
                    scheduler = get_task_scheduler(self.client)
                    scheduler.add_task(
                        task_id=task_id,
                        keyword=handler_data.get("keyword"),
                        schedule=handler_data.get("schedule"),
                        args=handler_data.get("handler_args", {}),
                    )

                    logger.info(f"Created scheduled task #{task_id}: {handler_data.get('keyword')} @ {handler_data.get('schedule')}")
                    print(f"[POLLER] Scheduled task #{task_id}: {clean_title}", flush=True)
                    self._set_status_label(task_id, "success")
                except VikunjaAPIError as e:
                    self._log_api_error(f"create scheduled task #{task_id}", e)
                    self._set_status_label(task_id, "error")
            elif handler_data and handler_data.get("keep_task"):
                # Info commands (weather/stock/news without schedule): update in place
                try:
                    from .metadata_manager import MetadataManager, SmartTaskMetadata

                    current_task = self.client.get_task(task_id)
                    original_title = current_task.get("title", "")

                    # Generate smart title from API response data
                    clean_title = self._generate_smart_title(handler_data, original_title)

                    # Build action bar with one-click links
                    action_bar = self._build_action_bar(task_id, handler_data)

                    # Add action bar to message (replace the comment-based refresh hint)
                    message_with_link = response_message
                    # Replace "Reply `@eis !w..." with action bar
                    message_with_link = re.sub(
                        r'💬 \*Reply `@eis.*?` to refresh\*',
                        action_bar,
                        message_with_link
                    )

                    # Create metadata for future refreshes
                    keyword = handler_data.get("keyword", "info")
                    handler_args = handler_data.get("handler_args", {})
                    metadata = SmartTaskMetadata(
                        keyword=keyword,
                        handler_args=handler_args,
                        schedule=handler_data.get("schedule"),
                    )

                    # Convert markdown to HTML and embed metadata
                    html_content = md_to_html(message_with_link)
                    html_description = MetadataManager.format_html(metadata, html_content)

                    # Check if we should create in a different project
                    target_project = handler_data.get("target_project")
                    if target_project:
                        # Find target project by name (with fuzzy matching)
                        target_project_id, candidates = self._find_project_by_name(target_project)
                        if target_project_id:
                            # Create task in target project (need to regenerate URL for new task)
                            new_task = self.client.create_task(
                                project_id=target_project_id,
                                title=clean_title,
                                description=""  # Placeholder, will update with correct URL
                            )
                            new_task_id = new_task.get("id")

                            # Regenerate action bar for new task
                            new_action_bar = self._build_action_bar(new_task_id, handler_data)
                            # Replace old action bar pattern (various link formats)
                            new_message = re.sub(
                                r'🔄 \[Refresh\]\([^)]+\).*?(?=\n|$)',
                                new_action_bar,
                                message_with_link
                            )
                            new_html = md_to_html(new_message)
                            new_html_description = MetadataManager.format_html(metadata, new_html)
                            self.client.update_task(new_task_id, description=new_html_description)

                            logger.info(f"Created task #{new_task_id} in project '{target_project}'")
                            print(f"[POLLER] Created task #{new_task_id} in '{target_project}'", flush=True)

                            # Set success label on new task
                            self._set_status_label(new_task_id, "success")

                            # Delete the original command task
                            try:
                                self.client.delete_task(task_id)
                                logger.info(f"Deleted command task #{task_id}")
                            except VikunjaAPIError as e:
                                self._log_api_error(f"delete command task #{task_id}", e)
                        elif candidates:
                            # Multiple matches - show move options
                            move_links = " | ".join([
                                f"[{c['title']}]({self._generate_move_url(task_id, c['id'])})"
                                for c in candidates
                            ])
                            warning = f"\n\n---\n📁 **Move to:** {move_links}"
                            html_with_options = md_to_html(message_with_link + warning)
                            html_description_options = MetadataManager.format_html(metadata, html_with_options)
                            self.client.update_task(task_id, title=clean_title, description=html_description_options)
                            logger.info(f"Project '{target_project}' ambiguous, showing {len(candidates)} options")
                            print(f"[POLLER] Project '{target_project}' ambiguous, showing move options", flush=True)
                            self._set_status_label(task_id, "needs_input")
                        else:
                            # No matches at all - update in place with all projects as options
                            try:
                                all_projects = self.client.get_projects()
                                # Deduplicate by project ID
                                seen_ids = set()
                                unique_projects = []
                                for p in all_projects:
                                    pid = p.get("id")
                                    if pid and pid not in seen_ids:
                                        seen_ids.add(pid)
                                        unique_projects.append(p)
                                unique_projects = unique_projects[:6]  # Max 6 options
                                if unique_projects:
                                    move_links = " | ".join([
                                        f"[{p.get('title', 'Untitled')}]({self._generate_move_url(task_id, p.get('id'))})"
                                        for p in unique_projects
                                    ])
                                    warning = f"\n\n---\n📁 **Move to:** {move_links}"
                                else:
                                    warning = f"\n\n---\n⚠️ No projects found"
                            except VikunjaAPIError:
                                warning = f"\n\n---\n⚠️ Project '{target_project}' not found"
                            html_with_warning = md_to_html(message_with_link + warning)
                            html_description_warning = MetadataManager.format_html(metadata, html_with_warning)
                            self.client.update_task(task_id, title=clean_title, description=html_description_warning)
                            logger.warning(f"Project '{target_project}' not found, showing move options")
                            print(f"[POLLER] Project '{target_project}' not found, showing move options", flush=True)
                            self._set_status_label(task_id, "needs_input")
                    else:
                        # No target project - update command task in place
                        self.client.update_task(task_id, title=clean_title, description=html_description)
                        logger.info(f"Updated info task #{task_id}")
                        print(f"[POLLER] Updated info task #{task_id}: {clean_title}", flush=True)
                        self._set_status_label(task_id, "success")
                except VikunjaAPIError as e:
                    self._log_api_error(f"update info task #{task_id}", e)
                    self._set_status_label(task_id, "error")
            else:
                # Tier 3 action commands (complete, remind): Delete the command task on success
                task_deleted = False
                try:
                    self.client.delete_task(task_id)
                    task_deleted = True
                    logger.info(f"Deleted command task #{task_id}")
                    print(f"[POLLER] Deleted command task #{task_id}", flush=True)
                except VikunjaAPIError as e:
                    self._log_api_error(f"delete command task #{task_id}", e)

                # Set outcome label if task wasn't deleted
                if not task_deleted and task_id:
                    self._set_status_label(task_id, "success")
        else:
            # Post error as comment
            try:
                self.client.add_comment(task_id, response_message)
                logger.info(f"Posted error to task #{task_id}")
            except VikunjaAPIError as e:
                self._log_api_error(f"post comment to task #{task_id}", e)

            # Set error or needs_input label
            if task_id:
                if _response_needs_input(response_message):
                    self._set_status_label(task_id, "needs_input")
                else:
                    self._set_status_label(task_id, "error")

        self._mark_read(notification_id)
        self._processed_ids.add(notification_id)
        self._cleanup_processed_ids()

    async def _process_comment(self, notification: dict):
        """Process a task.comment notification (refinement on smart task).

        Gathers full conversation context and passes to LLM.

        Args:
            notification: Notification object from Vikunja API
        """
        notification_id = notification.get("id")
        task_id = self._extract_task_id(notification)
        comment_text = self._extract_comment_text(notification)

        # Strip HTML tags from comment (Vikunja stores comments as HTML)
        comment_text = strip_html(comment_text)

        print(f"[POLLER] Processing task.comment: task_id={task_id}, comment={comment_text[:100] if comment_text else 'EMPTY'}", flush=True)

        if not task_id or not comment_text:
            self._mark_read(notification_id)
            self._processed_ids.add(notification_id)
            return

        # Skip comments made by @eis itself (prevents feedback loop)
        comment_author = self._extract_comment_author(notification)
        if comment_author.lower() in ("eis", "e"):
            print(f"[POLLER] Skipping self-comment by {comment_author}", flush=True)
            self._mark_read(notification_id)
            self._processed_ids.add(notification_id)
            return

        # Check if comment mentions @eis
        if "@eis" not in comment_text.lower() and "@e " not in comment_text.lower():
            # Not a command, just a regular comment
            self._mark_read(notification_id)
            self._processed_ids.add(notification_id)
            return

        # Set "thinking" status label while processing
        if task_id:
            self._set_status_label(task_id, "thinking")

        # Get full task context
        try:
            task = self.client.get_task(task_id)
            comments = self.client.get_comments(task_id)
        except VikunjaAPIError as e:
            self._log_api_error(f"get task context for #{task_id}", e)
            self._mark_read(notification_id)
            self._processed_ids.add(notification_id)
            return

        # Check if this is a smart task
        from .metadata_manager import MetadataManager
        description = task.get("description", "")
        metadata, content = MetadataManager.extract(description)

        if not metadata:
            # No persisted metadata - create default (comment on @eis = smart task)
            from .metadata_manager import SmartTaskMetadata
            metadata = SmartTaskMetadata(cost_tier="$")
            content = description

        # Build conversation context for LLM
        conversation = self._build_conversation_context(task, comments, metadata, content)

        # Parse the refinement command
        result = self.parser.parse(comment_text)

        if result.tier == "unknown":
            # No explicit command - treat as natural language refinement
            result = self.parser.parse(f"@eis $ {comment_text}")

        # Get project info for LLM tiers
        project_id = task.get("project_id")
        project_name = None
        if result.tier in ("tier_natural", "tier1", "tier2") and project_id:
            try:
                project_info = self.client.get_project(project_id)
                project_name = project_info.get("title", "")
            except Exception:
                project_name = f"Project {project_id}"

        # Extract user ID for budget tracking
        user_id = self._extract_user_id(notification)

        # Execute with full context
        response_message, is_success, handler_data = await self._execute_command(
            result,
            task_id=task_id,
            conversation_context=conversation,
            project_id=project_id,
            project_name=project_name,
            user_id=user_id,
        )

        print(f"[POLLER] Refinement result: {response_message[:100]}", flush=True)

        # Post response as comment (convert to HTML)
        try:
            html_comment = md_to_html(response_message)
            # Add cost footer for LLM responses
            if handler_data and handler_data.get("cost"):
                footer = _format_cost_footer(handler_data)
                html_comment += f"\n<p><small>{footer}</small></p>"
            self.client.add_comment(task_id, html_comment)
            logger.info(f"Posted refinement response to task #{task_id}")

            # Set outcome label
            if is_success:
                if _response_needs_input(response_message):
                    self._set_status_label(task_id, "needs_input")
                else:
                    self._set_status_label(task_id, "success")
            else:
                self._set_status_label(task_id, "error")
        except VikunjaAPIError as e:
            self._log_api_error(f"post refinement response to #{task_id}", e)
            self._set_status_label(task_id, "error")

        # Update metadata usage if LLM was called
        if is_success and result.tier in ("tier1", "tier2"):
            # Get updated metadata from handler if available
            new_metadata = handler_data.get("metadata") if handler_data else None
            if new_metadata:
                metadata = new_metadata
            else:
                metadata.increment_usage(1)
            # Use format_html since content is HTML
            new_description = MetadataManager.format_html(metadata, content)
            try:
                self.client.update_task(task_id, description=new_description)
            except VikunjaAPIError as e:
                self._log_api_error(f"update metadata for #{task_id}", e)

        self._mark_read(notification_id)
        self._processed_ids.add(notification_id)
        self._cleanup_processed_ids()

    def _build_conversation_context(
        self,
        task: dict,
        comments: list[dict],
        metadata,
        content: str
    ) -> str:
        """Build conversation context string for LLM.

        Args:
            task: Task object
            comments: List of comment objects
            metadata: SmartTaskMetadata
            content: Task content (without frontmatter)

        Returns:
            Formatted conversation context string
        """
        parts = []

        # Task info
        parts.append(f"## Task: {task.get('title', 'Untitled')}")
        parts.append(f"**Original request:** {metadata.prompt or 'N/A'}")
        parts.append(f"**Cost tier:** {metadata.cost_tier}")
        parts.append("")

        # Current description content
        if content:
            parts.append("## Current Content")
            parts.append(content)
            parts.append("")

        # Conversation history
        if comments:
            parts.append("## Conversation History")
            for comment in comments:
                author = comment.get("author", {}).get("username", "user")
                text = comment.get("comment", "")
                # Skip @eis's own comments in context (avoid echo)
                if author.lower() in ("eis", "e"):
                    parts.append(f"**@eis:** {text[:500]}")
                else:
                    parts.append(f"**{author}:** {text}")
            parts.append("")

        return "\n".join(parts)

    def _extract_comment_text(self, notification: dict) -> str:
        """Extract comment text from notification.

        Args:
            notification: Notification object

        Returns:
            Comment text or empty string
        """
        data = notification.get("notification", {})

        if "comment" in data and isinstance(data["comment"], dict):
            return data["comment"].get("comment", "")

        return ""

    def _extract_comment_author(self, notification: dict) -> str:
        """Extract comment author username from notification.

        Args:
            notification: Notification object

        Returns:
            Author username or empty string
        """
        data = notification.get("notification", {})

        if "comment" in data and isinstance(data["comment"], dict):
            author = data["comment"].get("author", {})
            return author.get("username", "")

        # Also check doer for notifications
        if "doer" in data and isinstance(data["doer"], dict):
            return data["doer"].get("username", "")

        return ""

    def _extract_user_id(self, notification: dict) -> str:
        """Extract user ID from notification for budget tracking and project sharing.

        Args:
            notification: Notification object

        Returns:
            User ID in format "vikunja:<username>:<numeric_id>" or "vikunja:<username>"
        """
        data = notification.get("notification", {})

        # Try doer first (who triggered the action)
        if "doer" in data and isinstance(data["doer"], dict):
            doer = data["doer"]
            username = doer.get("username", "")
            numeric_id = doer.get("id")
            if username:
                # Include numeric ID for project sharing (solutions-2dum)
                if numeric_id:
                    return f"vikunja:{username}:{numeric_id}"
                return f"vikunja:{username}"

        # Try comment author
        if "comment" in data and isinstance(data["comment"], dict):
            author = data["comment"].get("author", {})
            if isinstance(author, dict):
                username = author.get("username", "")
                numeric_id = author.get("id")
                if username:
                    if numeric_id:
                        return f"vikunja:{username}:{numeric_id}"
                    return f"vikunja:{username}"

        # Try task creator
        if "task" in data and isinstance(data["task"], dict):
            created_by = data["task"].get("created_by", {})
            if isinstance(created_by, dict):
                username = created_by.get("username", "")
                numeric_id = created_by.get("id")
                if username:
                    if numeric_id:
                        return f"vikunja:{username}:{numeric_id}"
                    return f"vikunja:{username}"

        return ""

    def _extract_user_info(self, notification: dict) -> tuple[str, int | None]:
        """Extract username and numeric user_id from notification.

        Args:
            notification: Notification object

        Returns:
            Tuple of (username, user_id) - user_id may be None
        """
        data = notification.get("notification", {})

        # Try doer first (who triggered the action)
        if "doer" in data and isinstance(data["doer"], dict):
            doer = data["doer"]
            username = doer.get("username", "")
            user_id = doer.get("id")
            if username:
                return username, user_id

        # Try comment author
        if "comment" in data and isinstance(data["comment"], dict):
            author = data["comment"].get("author", {})
            if isinstance(author, dict):
                username = author.get("username", "")
                user_id = author.get("id")
                if username:
                    return username, user_id

        # Try task creator
        if "task" in data and isinstance(data["task"], dict):
            created_by = data["task"].get("created_by", {})
            if isinstance(created_by, dict):
                username = created_by.get("username", "")
                user_id = created_by.get("id")
                if username:
                    return username, user_id

        return "", None

    def _cleanup_processed_ids(self):
        """Clean up old processed IDs to prevent memory growth."""
        if len(self._processed_ids) > 1000:
            oldest = sorted(self._processed_ids)[:500]
            self._processed_ids -= set(oldest)

    def _find_project_by_name(self, name: str) -> tuple[Optional[int], list[dict]]:
        """Find project ID by name with fuzzy matching.

        Args:
            name: Project name to search for

        Returns:
            Tuple of (project_id, candidates):
            - If exact match: (project_id, [])
            - If single fuzzy match (score >= 80): (project_id, [])
            - If multiple fuzzy matches: (None, [{"id": id, "title": title, "score": score}, ...])
            - If no matches: (None, [])
        """
        from rapidfuzz import process, fuzz

        try:
            projects = self.client.get_projects()
            if not projects:
                return (None, [])

            name_lower = name.lower().strip()

            # Try exact match first
            for project in projects:
                if project.get("title", "").lower().strip() == name_lower:
                    return (project.get("id"), [])

            # Fuzzy match
            project_map = {p.get("title", ""): p for p in projects}
            matches = process.extract(
                name,
                project_map.keys(),
                scorer=fuzz.WRatio,
                limit=5
            )

            # Filter to matches with score >= 60
            good_matches = [m for m in matches if m[1] >= 60]

            if not good_matches:
                return (None, [])

            # If single high-confidence match (>= 80), use it
            if len(good_matches) == 1 and good_matches[0][1] >= 80:
                title = good_matches[0][0]
                return (project_map[title].get("id"), [])

            # If top match is significantly better (20+ points), use it
            if len(good_matches) >= 2:
                if good_matches[0][1] - good_matches[1][1] >= 20 and good_matches[0][1] >= 75:
                    title = good_matches[0][0]
                    return (project_map[title].get("id"), [])

            # Multiple candidates - return them for user to choose
            candidates = [
                {
                    "id": project_map[m[0]].get("id"),
                    "title": m[0],
                    "score": m[1]
                }
                for m in good_matches[:4]  # Max 4 options
            ]
            return (None, candidates)

        except VikunjaAPIError as e:
            logger.error(f"Failed to search projects: {e}")
            return (None, [])

    def _generate_refresh_url(self, task_id: int) -> str:
        """Generate a refresh URL for a smart task.

        Args:
            task_id: Task ID to generate URL for

        Returns:
            Full refresh URL with token
        """
        import hashlib
        import os

        bot_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")
        token = hashlib.sha256(f"{task_id}:{bot_token}".encode()).hexdigest()[:12]

        mcp_url = os.environ.get("MCP_URL", "https://mcp.factumerit.app")
        return f"{mcp_url}/refresh/{task_id}/{token}"

    def _generate_move_url(self, task_id: int, project_id: int) -> str:
        """Generate a move URL for a task.

        Args:
            task_id: Task ID to move
            project_id: Target project ID

        Returns:
            Full move URL with token
        """
        import hashlib
        import os

        bot_token = os.environ.get("VIKUNJA_BOT_TOKEN", "")
        # Include both task_id and project_id in token for security
        token = hashlib.sha256(f"{task_id}:{project_id}:{bot_token}".encode()).hexdigest()[:12]

        mcp_url = os.environ.get("MCP_URL", "https://mcp.factumerit.app")
        return f"{mcp_url}/move/{task_id}/{project_id}/{token}"

    def _build_action_bar(self, task_id: int, handler_data: dict) -> str:
        """Build row of action links based on context.

        Args:
            task_id: Task ID
            handler_data: Data from keyword handler with keyword, schedule, supports_schedule

        Returns:
            Formatted action bar like "✖️ [Remove](url) · ⏰ [hourly](url)..."
        """
        from .server import _generate_action_token
        import os
        from urllib.parse import quote

        mcp_url = os.environ.get("MCP_URL", "https://mcp.factumerit.app")
        actions = []

        keyword = handler_data.get("keyword", "")
        current_schedule = handler_data.get("schedule")
        handler_args = handler_data.get("handler_args", {})

        # Source link (replaces Refresh - solutions-v1x9)
        if keyword == "weather":
            location = handler_args.get("location", "")
            if location:
                # Link to weather.com search
                source_url = f"https://weather.com/weather/today/l/{quote(location)}"
                actions.append(f"🔗 [Full forecast]({source_url})")
        elif keyword == "rss":
            feed_url = handler_args.get("url", "")
            if feed_url:
                actions.append(f"🔗 [View feed]({feed_url})")

        # Remove (DELETE task, not mark complete - solutions-nzo3)
        remove_token = _generate_action_token("remove", task_id)
        actions.append(f"✖️ [Remove]({mcp_url}/remove/{task_id}/{remove_token})")

        # One-click schedule links (solutions-n5aa)
        if keyword in ("weather", "rss"):
            schedule_options = ["hourly", "6h", "12h", "daily"]
            schedule_links = []
            for sched in schedule_options:
                if sched == current_schedule:
                    # Current schedule shown as plain text (no link)
                    schedule_links.append(sched)
                else:
                    # Clickable link to change schedule
                    sched_token = _generate_action_token(f"schedule-{sched}", task_id)
                    schedule_links.append(f"[{sched}]({mcp_url}/set-schedule/{task_id}/{sched}/{sched_token})")

            # Add "off" option if currently scheduled
            if current_schedule:
                off_token = _generate_action_token("schedule-off", task_id)
                schedule_links.append(f"[off]({mcp_url}/set-schedule/{task_id}/off/{off_token})")

            actions.append("⏰ " + " ".join(schedule_links))

        return " · ".join(actions)

    def _generate_smart_title(self, handler_data: dict, original_title: str) -> str:
        """Generate a smart title from API response data.

        For weather: "Tokyo, JP" or "Tokyo, JP (hourly)"
        For stock: "AAPL" or "AAPL (daily)"
        For news: "Tech Headlines" or fallback

        Args:
            handler_data: Data from keyword handler (weather/stock/news dicts)
            original_title: Original task title (fallback)

        Returns:
            Clean, formatted title
        """
        # Check for explicit smart_title from handler
        if handler_data.get("smart_title"):
            return handler_data["smart_title"]

        keyword = handler_data.get("keyword", "")
        schedule = handler_data.get("schedule")

        # Build schedule suffix if present
        schedule_suffix = f" ({schedule})" if schedule else ""

        # Weather: Use location + country from API response
        if keyword == "weather" and handler_data.get("weather"):
            weather = handler_data["weather"]
            location = weather.get("location", "")
            country = weather.get("country", "")
            if location:
                if country:
                    return f"{location}, {country}{schedule_suffix}"
                return f"{location}{schedule_suffix}"

        # Stock: Use ticker from API response
        if keyword == "stock" and handler_data.get("stock"):
            stock = handler_data["stock"]
            ticker = stock.get("ticker", "")
            if ticker:
                return f"{ticker}{schedule_suffix}"

        # News: Use query or category
        if keyword == "news" and handler_data.get("news"):
            news = handler_data["news"]
            if news.get("query"):
                return f"{news['query'].title()} Headlines{schedule_suffix}"
            if news.get("category"):
                return f"{news['category'].title()} Headlines{schedule_suffix}"
            return f"Headlines{schedule_suffix}"

        # RSS: Use feed title from response
        if keyword == "rss" and handler_data.get("rss"):
            rss = handler_data["rss"]
            feed_title = rss.get("feed_title", "")
            if feed_title and feed_title != "RSS Feed":
                return f"{feed_title}{schedule_suffix}"
            # Fallback to domain name from URL
            handler_args = handler_data.get("handler_args", {})
            url = handler_args.get("url", "")
            if url:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                if domain:
                    return f"{domain}{schedule_suffix}"
            return f"RSS Feed{schedule_suffix}"

        # Help: Use topic or "Command Reference"
        if keyword == "help":
            handler_args = handler_data.get("handler_args", {})
            topic = handler_args.get("topic", "")
            if topic:
                return f"@eis Help: {topic.title()}"
            return "@eis Command Reference"

        # Fallback: Clean up original title
        clean = re.sub(r'^(@e(is)?\s*)?!?\w+\s*', '', original_title).strip()
        # Remove pipe and everything after (target project syntax)
        clean = re.sub(r'\s*\|.*$', '', clean).strip()
        if clean:
            return f"{clean}{schedule_suffix}"

        # Last resort: keyword-based default
        return f"{keyword.title() if keyword else 'Smart'} {'Update' if schedule else 'Info'}"

    def _log_api_error(self, action: str, error: VikunjaAPIError):
        """Log API error, downgrading 404s to debug level.

        404s are expected when tasks are deleted outside the poller.
        """
        if "404" in str(error):
            logger.debug(f"Task gone (404) while trying to {action}")
        else:
            logger.error(f"Failed to {action}: {error}")
            print(f"[POLLER] Failed to {action}: {error}", flush=True)

    def _extract_task_id(self, notification: dict) -> Optional[int]:
        """Extract task ID from notification.

        Args:
            notification: Notification object

        Returns:
            Task ID or None if not found
        """
        # Vikunja notifications have different structures
        # Try common patterns
        if "task" in notification:
            return notification["task"].get("id")
        if "task_id" in notification:
            return notification["task_id"]
        if "doer" in notification and "task" in notification.get("notification", {}):
            return notification["notification"]["task"].get("id")

        # Try to find task ID in notification data
        data = notification.get("notification", {})
        if isinstance(data, dict):
            if "task" in data:
                return data["task"].get("id")

        return None

    def _extract_text(self, notification: dict) -> str:
        """Extract text content from notification.

        Args:
            notification: Notification object

        Returns:
            Text content (task title, comment text, etc.)
        """
        # Try different notification structures
        data = notification.get("notification", {})

        # Task mention - get title
        if "task" in data and isinstance(data["task"], dict):
            task = data["task"]
            text_parts = []
            if task.get("title"):
                text_parts.append(task["title"])
            if task.get("description"):
                text_parts.append(task["description"])
            return " ".join(text_parts)

        # Comment mention
        if "comment" in data and isinstance(data["comment"], dict):
            return data["comment"].get("comment", "")

        # Direct text field
        if "text" in data:
            return data["text"]

        return ""

    async def _execute_command(
        self,
        result,
        task_id: Optional[int] = None,
        conversation_context: Optional[str] = None,
        project_id: Optional[int] = None,
        project_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[str, bool, Optional[dict]]:
        """Execute a parsed command and return response message with success status.

        Args:
            result: ParseResult from CommandParser
            task_id: Optional task ID for context
            conversation_context: Optional conversation history for LLM
            project_id: Project ID for tool scope (tier_natural)
            project_name: Project name for context (tier_natural)
            user_id: User ID for budget tracking (vikunja:<username>)

        Returns:
            Tuple of (response_message, is_success, handler_data)
        """
        if result.tier == "tier3":
            # Deterministic command
            handler = self.handlers.get_handler(result.handler)
            if handler:
                try:
                    # Build kwargs based on handler signature
                    import inspect
                    sig = inspect.signature(handler)
                    kwargs = {}
                    if 'task_id' in sig.parameters:
                        kwargs['task_id'] = task_id
                    if 'project_id' in sig.parameters:
                        kwargs['project_id'] = project_id
                    if 'user_id' in sig.parameters:
                        kwargs['user_id'] = user_id
                    handler_result = await handler(result.args or {}, **kwargs)
                    return (handler_result.message, handler_result.success, handler_result.data)
                except Exception as e:
                    logger.exception(f"Handler {result.handler} failed")
                    return (f"Error executing {result.matched_command}: {e}", False, None)
            else:
                return (f"Unknown handler: {result.handler}", False, None)

        elif result.tier in ("tier1", "tier2"):
            # LLM tiers - same as tier_natural, pass full context
            handler = self.handlers.get_handler(result.handler)
            if handler:
                try:
                    handler_result = await handler(
                        result.args or {},
                        task_id=task_id,
                        project_id=project_id,
                        project_name=project_name,
                        conversation_context=conversation_context,
                        user_id=user_id,
                    )
                    return (handler_result.message, handler_result.success, handler_result.data)
                except Exception as e:
                    logger.exception(f"LLM handler {result.handler} failed")
                    return (f"Error executing LLM command: {e}", False, None)
            else:
                return (f"Unknown LLM handler: {result.handler}", False, None)

        elif result.tier == "tier_natural":
            # Natural language with full tool access
            handler = self.handlers.get_handler(result.handler)
            if handler:
                try:
                    handler_result = await handler(
                        result.args or {},
                        task_id=task_id,
                        project_id=project_id,
                        project_name=project_name,
                        conversation_context=conversation_context,
                        user_id=user_id,
                    )
                    return (handler_result.message, handler_result.success, handler_result.data)
                except Exception as e:
                    logger.exception(f"LLM tools handler {result.handler} failed")
                    return (f"Error executing natural language command: {e}", False, None)
            else:
                return (f"Unknown handler: {result.handler}", False, None)

        else:
            return (result.error or "Could not parse command", False, None)

    def _mark_read(self, notification_id: int):
        """Mark notification as read.

        Args:
            notification_id: Notification ID

        Note: Vikunja's notification read endpoints don't work as expected.
        We rely on _processed_ids to prevent re-processing instead.
        TODO: Figure out correct Vikunja API for marking notifications read.
        """
        # Disabled - Vikunja API returns errors for both:
        # - POST /notifications/{id}/read
        # - POST /notifications/read
        # The _processed_ids set prevents re-processing anyway.
        pass


class CentralizedPoller:
    """Centralized poller for all personal bots.

    Instead of creating N pollers (one per bot), this creates a single poller
    that manages all bots and distributes work appropriately.

    Benefits:
    - Sequential polling (no rate limit burst on startup)
    - Single EARS scan per project (not N scans)
    - Lower memory footprint
    - Easier rate limiting / backoff logic

    Bead: solutions-gaid
    """

    def __init__(self, poll_interval: float = 10.0, idle_timeout_minutes: int = 30):
        """Initialize centralized poller.

        Args:
            poll_interval: Seconds between poll cycles (default 10)
            idle_timeout_minutes: Minutes of inactivity before bot goes to standby (default 30)
        """
        self.poll_interval = poll_interval
        self.idle_timeout_minutes = idle_timeout_minutes
        self.bot_clients: dict[str, BotVikunjaClient] = {}  # user_id -> client
        self.bot_pollers: dict[str, NotificationPoller] = {}  # user_id -> poller instance
        self.bot_last_activity: dict[str, float] = {}  # user_id -> timestamp of last activity
        self._running = False
        self._ears_scan_interval = 30  # seconds between ears scans
        self._ears_scan_counter = 0

        # Dispatch bot (central @eis bot for EARS and @mentions)
        self.dispatch_client: Optional[BotVikunjaClient] = None
        self.dispatch_poller: Optional[NotificationPoller] = None

        # Health monitoring
        self._health = {
            "started_at": None,
            "total_poll_cycles": 0,
            "total_ears_scans": 0,
            "poll_errors": {},  # user_id -> error_count
            "ears_errors": {},  # user_id -> error_count
            "last_poll_time": None,
            "last_ears_scan_time": None,
            "bots_added": 0,
            "bots_failed_init": 0,
            "bots_removed_idle": 0,
        }

    def get_health_status(self) -> dict:
        """Get health status of the centralized poller.

        Returns:
            dict with health metrics
        """
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        uptime_seconds = (now - self._health["started_at"]).total_seconds() if self._health["started_at"] else 0

        # Calculate error rates
        total_poll_errors = sum(self._health["poll_errors"].values())
        total_ears_errors = sum(self._health["ears_errors"].values())

        return {
            "status": "running" if self._running else "stopped",
            "uptime_seconds": uptime_seconds,
            "uptime_human": f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m",
            "bot_count": len(self.bot_pollers),
            "bot_count_active": len(self.bot_pollers),
            "poll_cycles": self._health["total_poll_cycles"],
            "ears_scans": self._health["total_ears_scans"],
            "poll_errors": {
                "total": total_poll_errors,
                "by_bot": dict(self._health["poll_errors"]),
            },
            "ears_errors": {
                "total": total_ears_errors,
                "by_bot": dict(self._health["ears_errors"]),
            },
            "last_poll": self._health["last_poll_time"].isoformat() if self._health["last_poll_time"] else None,
            "last_ears_scan": self._health["last_ears_scan_time"].isoformat() if self._health["last_ears_scan_time"] else None,
            "bots_added": self._health["bots_added"],
            "bots_failed_init": self._health["bots_failed_init"],
            "bots_removed_idle": self._health["bots_removed_idle"],
            "idle_timeout_minutes": self.idle_timeout_minutes,
        }

    def _should_keep_bot_active(self, user_id: str) -> bool:
        """Check if bot should stay active (service_needed=true in database).

        Bot Lifecycle:
        - ALERT (service_needed=true): Stay initialized, poll continuously
        - STANDBY (service_needed=false): Remove from memory
        - WAKE UP (@mention or EARS ON): Set service_needed=true, lazy-init on demand

        Args:
            user_id: User ID for the bot

        Returns:
            True if bot should stay active, False if it should go to standby
        """
        from .bot_provisioning import get_users_needing_service

        # Check database for service_needed flag
        try:
            users_needing_service = get_users_needing_service()
            return user_id in users_needing_service
        except Exception as e:
            logger.error(f"Error checking service_needed for {user_id}: {e}")
            # On error, keep bot active (conservative)
            return True

    async def _get_or_create_bot_client(self, user_id: str) -> tuple[BotVikunjaClient, NotificationPoller]:
        """Get existing bot client or create new one (lazy initialization).

        Args:
            user_id: User ID for the bot

        Returns:
            Tuple of (client, poller)

        Raises:
            Exception if bot initialization fails
        """
        import time

        if user_id in self.bot_clients:
            # Update last activity timestamp
            self.bot_last_activity[user_id] = time.time()
            return self.bot_clients[user_id], self.bot_pollers[user_id]

        # Lazy initialization - create bot client on first use
        start_time = time.time()
        logger.info(f"[CentralizedPoller] Lazy-initializing bot for {user_id}")

        try:
            client = BotVikunjaClient(user_id=user_id)
            poller = NotificationPoller(client=client)

            # Measure time to first API call (triggers JWT fetch)
            # This happens automatically on first poll, but we can measure it
            init_time = time.time() - start_time

            self.bot_clients[user_id] = client
            self.bot_pollers[user_id] = poller
            self.bot_last_activity[user_id] = time.time()
            self._health["bots_added"] += 1

            logger.info(f"[CentralizedPoller] Bot {user_id} initialized in {init_time:.2f}s")
            print(f"[POLLER] Lazy init: {user_id} ({init_time:.2f}s)", flush=True)

            return client, poller

        except Exception as e:
            self._health["bots_failed_init"] += 1
            logger.error(f"[CentralizedPoller] Failed to initialize bot {user_id}: {e}")
            raise

    async def start(self):
        """Start the centralized polling loop."""
        import os
        from datetime import datetime, timezone

        self._running = True
        self._health["started_at"] = datetime.now(timezone.utc)

        from .bot_provisioning import get_all_bot_user_ids

        # Initialize dispatch bot (central @eis bot for EARS and @mentions)
        dispatch_token = os.environ.get("VIKUNJA_BOT_TOKEN")
        if dispatch_token:
            try:
                self.dispatch_client = BotVikunjaClient()  # Uses VIKUNJA_BOT_TOKEN from env
                self.dispatch_poller = NotificationPoller(client=self.dispatch_client)
                logger.info("[CentralizedPoller] Dispatch bot initialized (VIKUNJA_BOT_TOKEN)")
                print("[POLLER] Dispatch bot: @eis (EARS + @mentions)", flush=True)
            except Exception as e:
                logger.error(f"[CentralizedPoller] Failed to initialize dispatch bot: {e}")
                print(f"[POLLER] Dispatch bot failed: {e}", flush=True)
        else:
            logger.warning("[CentralizedPoller] No VIKUNJA_BOT_TOKEN - dispatch bot disabled")
            print("[POLLER] No dispatch bot (VIKUNJA_BOT_TOKEN not set)", flush=True)

        # Get list of bot user IDs (but don't initialize them yet - lazy init on first poll)
        try:
            bot_user_ids = get_all_bot_user_ids()
        except Exception as e:
            logger.error(f"[CentralizedPoller] Failed to get bot user IDs: {e}")
            bot_user_ids = []

        if not bot_user_ids:
            logger.warning("[CentralizedPoller] No personal bots found, waiting...")
            print("[POLLER] Centralized mode: No personal bots yet, waiting for first signup", flush=True)
        else:
            logger.info(f"[CentralizedPoller] Starting with {len(bot_user_ids)} personal bots (lazy init)")
            print(f"[POLLER] Centralized mode: {len(bot_user_ids)} personal bots (lazy init)", flush=True)

        # Main polling loop
        while self._running:
            try:
                # Poll dispatch bot first (handles EARS and @mentions)
                if self.dispatch_poller:
                    try:
                        await self.dispatch_poller._poll_once()
                    except Exception as e:
                        logger.error(f"[CentralizedPoller] Dispatch bot poll failed: {e}")

                # Poll all personal bots sequentially (avoid rate limit burst)
                await self._poll_all_bots()
                self._health["total_poll_cycles"] += 1

                # Run EARS scans periodically (dispatch bot scans ALL EARS projects)
                self._ears_scan_counter += self.poll_interval
                if self._ears_scan_counter >= self._ears_scan_interval:
                    if self.dispatch_poller:
                        try:
                            await self.dispatch_poller._scan_ears_projects()
                        except Exception as e:
                            logger.error(f"[CentralizedPoller] Dispatch EARS scan failed: {e}")

                    # Also scan for personal bots (legacy, may be removed later)
                    await self._scan_all_ears_projects()
                    self._ears_scan_counter = 0

                # Cleanup idle bots every 5 minutes (30 poll cycles at 10s interval)
                if self._health["total_poll_cycles"] % 30 == 0:
                    await self._cleanup_idle_bots()

                # Log health status every 10 minutes (60 poll cycles at 10s interval)
                if self._health["total_poll_cycles"] % 60 == 0:
                    health = self.get_health_status()
                    logger.info(f"[CentralizedPoller] Health: {health['bot_count']} bots, "
                               f"{health['poll_cycles']} cycles, "
                               f"{health['poll_errors']['total']} poll errors, "
                               f"{health['ears_errors']['total']} EARS errors, "
                               f"{health['bots_removed_idle']} removed (idle), "
                               f"uptime {health['uptime_human']}")

            except Exception as e:
                logger.exception(f"[CentralizedPoller] Error in main loop: {e}")

            await asyncio.sleep(self.poll_interval)

    async def _cleanup_idle_bots(self):
        """Remove idle bots from memory (send to standby).

        Bots are removed if:
        - No EARS projects are active
        - No activity in last N minutes (idle_timeout_minutes)

        They will be lazy-initialized again when needed.
        """
        import time

        bots_to_remove = []

        for user_id in list(self.bot_clients.keys()):
            if not self._should_keep_bot_active(user_id):
                bots_to_remove.append(user_id)

        for user_id in bots_to_remove:
            logger.info(f"[CentralizedPoller] Removing idle bot: {user_id}")
            print(f"[POLLER] Standby: {user_id} (idle)", flush=True)

            # Remove from active bots
            del self.bot_clients[user_id]
            del self.bot_pollers[user_id]
            if user_id in self.bot_last_activity:
                del self.bot_last_activity[user_id]

            self._health["bots_removed_idle"] += 1

        if bots_to_remove:
            logger.info(f"[CentralizedPoller] Removed {len(bots_to_remove)} idle bots")

    async def _poll_all_bots(self):
        """Poll notifications for all bots sequentially (TRUE LAZY - only poll active bots).

        True lazy approach:
        - Query database for users with service_needed=true
        - Only initialize/poll bots for users who need service
        - Update service_last_active after each poll
        - Add 0.5s delay between bots to avoid 429 rate limits
        """
        import asyncio
        from datetime import datetime, timezone
        from .bot_provisioning import get_users_needing_service, update_service_last_active

        # Get users who need service (from database)
        try:
            users_needing_service = get_users_needing_service()
        except Exception as e:
            logger.error(f"[CentralizedPoller] Failed to get users needing service: {e}")
            return

        # Poll only bots for users who need service
        for i, user_id in enumerate(users_needing_service):
            try:
                # Lazy initialization - create bot client if needed
                client, poller = await self._get_or_create_bot_client(user_id)

                # Use the existing NotificationPoller._poll_once() method
                await poller._poll_once()

                # Update last active timestamp
                update_service_last_active(user_id)

                # Add delay between bots to avoid 429 rate limits (skip after last bot)
                if i < len(users_needing_service) - 1:
                    await asyncio.sleep(0.5)

            except Exception as e:
                # Track error
                if user_id not in self._health["poll_errors"]:
                    self._health["poll_errors"][user_id] = 0
                self._health["poll_errors"][user_id] += 1

                logger.error(f"[CentralizedPoller] Polling failed for {user_id}: {e}")
                # Continue with other bots even if one fails

        self._health["last_poll_time"] = datetime.now(timezone.utc)

    async def _scan_all_ears_projects(self):
        """Scan EARS-enabled projects (TRUE LAZY - only scan for users needing service).

        True lazy approach:
        - Query database for users with service_needed=true
        - Only scan EARS projects for those users
        - Update service_last_active after each scan
        """
        from datetime import datetime, timezone
        from .bot_provisioning import get_users_needing_service, update_service_last_active
        from .server import _get_ears_enabled_projects

        # Check if any EARS projects exist
        try:
            ears_projects = _get_ears_enabled_projects()
            if not ears_projects:
                logger.debug("[CentralizedPoller] No EARS projects, skipping scan")
                return
        except Exception as e:
            logger.error(f"[CentralizedPoller] Failed to get EARS projects: {e}")
            return

        logger.info(f"[CentralizedPoller] Found {len(ears_projects)} EARS-enabled projects")

        # Get users who need service (from database)
        try:
            users_needing_service = get_users_needing_service()
        except Exception as e:
            logger.error(f"[CentralizedPoller] Failed to get users needing service: {e}")
            return

        # Only scan for users who need service
        for user_id in users_needing_service:
            try:
                # Lazy initialization - create bot client if needed
                client, poller = await self._get_or_create_bot_client(user_id)

                # Use the existing NotificationPoller._scan_ears_projects() method
                await poller._scan_ears_projects()

                # Update last active timestamp
                update_service_last_active(user_id)

            except Exception as e:
                # Track error
                if user_id not in self._health["ears_errors"]:
                    self._health["ears_errors"][user_id] = 0
                self._health["ears_errors"][user_id] += 1

                logger.error(f"[CentralizedPoller] EARS scan failed for {user_id}: {e}")
                # Continue with other bots even if one fails

        self._health["total_ears_scans"] += 1
        self._health["last_ears_scan_time"] = datetime.now(timezone.utc)


async def run_poller():
    """Run the notification poller (entry point for async execution).

    Supports two modes:
    1. Legacy single-bot mode: Uses VIKUNJA_BOT_TOKEN env var
    2. Centralized multi-bot mode: Polls for all personal bots from database (JWT auth)

    Centralized mode is used when personal_bots table has entries.
    Falls back to legacy mode if no personal bots found.

    Bead: solutions-gaid (centralized poller architecture)
    """
    import os
    from .bot_provisioning import get_all_bot_user_ids

    # Try to get personal bot user IDs from database
    try:
        bot_user_ids = get_all_bot_user_ids()
    except Exception as e:
        logger.warning(f"[run_poller] Failed to get personal bot user IDs: {e}")
        bot_user_ids = []

    if bot_user_ids or True:  # Always use centralized mode (handles 0 bots gracefully)
        # Centralized multi-bot mode: single poller for all bots
        logger.info(f"[run_poller] Starting centralized poller for {len(bot_user_ids)} personal bots")
        print(f"[POLLER] Centralized mode: {len(bot_user_ids)} personal bots (JWT auth)", flush=True)

        poller = CentralizedPoller(poll_interval=10.0)

        # Store global reference for health monitoring
        try:
            from . import server
            server._centralized_poller = poller
        except Exception as e:
            logger.warning(f"[run_poller] Could not set global poller reference: {e}")

        await poller.start()

    else:
        # Legacy single-bot mode: use VIKUNJA_BOT_TOKEN (deprecated)
        if os.environ.get("VIKUNJA_BOT_TOKEN"):
            logger.info("[run_poller] Starting legacy single-bot polling")
            print("[POLLER] Legacy mode: single bot from VIKUNJA_BOT_TOKEN", flush=True)
            poller = NotificationPoller()
            await poller.start()
        else:
            logger.warning("[run_poller] No bots configured - nothing to poll")
            print("[POLLER] No bots configured - waiting for first signup", flush=True)
            # Wait and retry periodically for new bots
            while True:
                await asyncio.sleep(60)
                try:
                    bot_user_ids = get_all_bot_user_ids()
                    if bot_user_ids:
                        logger.info(f"[run_poller] Found {len(bot_user_ids)} bots, restarting")
                        # Restart with new bots
                        return await run_poller()
                except Exception:
                    pass


if __name__ == "__main__":
    # Run directly for testing
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_poller())
