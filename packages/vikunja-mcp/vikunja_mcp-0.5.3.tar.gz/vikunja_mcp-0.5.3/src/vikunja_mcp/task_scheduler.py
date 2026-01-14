"""
Task Scheduler for @eis Smart Tasks.

Manages scheduled updates for smart tasks using APScheduler.

Architecture:
    1. On startup, scan Vikunja for tasks with schedules
    2. Register jobs with APScheduler
    3. When job fires, call API handler and update task
    4. Handle task changes (new schedules, deleted tasks)

Bead: solutions-hgwx.4
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Callable, Awaitable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from .schedule_parser import parse_schedule, ScheduleConfig
from .vikunja_client import BotVikunjaClient, VikunjaAPIError
from .metadata_manager import MetadataManager, SmartTaskMetadata
from .api_clients import get_weather_client, get_stock_client, get_news_client

logger = logging.getLogger(__name__)


@dataclass
class ScheduledTask:
    """Represents a scheduled smart task."""
    task_id: int
    keyword: str  # "weather", "stock", "news"
    schedule: str  # Original schedule string
    args: dict  # Handler arguments (location, ticker, etc.)
    job_id: str  # APScheduler job ID


class TaskScheduler:
    """Manages scheduled smart task updates.

    Usage:
        scheduler = TaskScheduler()
        await scheduler.start()  # Scans tasks, starts scheduler

        # Add a new scheduled task
        scheduler.add_task(task_id=42, keyword="weather",
                          schedule="every morning at 7am",
                          args={"location": "Seattle"})

        # Remove a task
        scheduler.remove_task(task_id=42)

        # Shutdown
        scheduler.stop()
    """

    def __init__(self, client: Optional[BotVikunjaClient] = None):
        """Initialize scheduler.

        Args:
            client: BotVikunjaClient instance (creates one if not provided)
        """
        self.client = client or BotVikunjaClient()
        self.scheduler = AsyncIOScheduler()
        self._tasks: dict[int, ScheduledTask] = {}  # task_id -> ScheduledTask
        self._running = False

    async def start(self, scan_existing: bool = True):
        """Start the scheduler.

        Args:
            scan_existing: If True, scan Vikunja for existing scheduled tasks
        """
        if self._running:
            logger.warning("Scheduler already running")
            return

        logger.info("Starting task scheduler")
        print("[SCHEDULER] Starting task scheduler", flush=True)

        if scan_existing:
            await self._scan_existing_tasks()

        self.scheduler.start()
        self._running = True

        logger.info(f"Scheduler started with {len(self._tasks)} scheduled tasks")
        print(f"[SCHEDULER] Running with {len(self._tasks)} scheduled tasks", flush=True)

    def stop(self):
        """Stop the scheduler."""
        if not self._running:
            return

        logger.info("Stopping task scheduler")
        self.scheduler.shutdown(wait=False)
        self._running = False

    def add_task(
        self,
        task_id: int,
        keyword: str,
        schedule: str,
        args: dict,
    ) -> bool:
        """Add a scheduled task.

        Args:
            task_id: Vikunja task ID
            keyword: Handler keyword (weather, stock, news)
            schedule: Natural language schedule
            args: Handler arguments

        Returns:
            True if task was added, False on error
        """
        # Parse schedule
        config = parse_schedule(schedule)
        if not config.valid:
            logger.error(f"Invalid schedule for task {task_id}: {config.error}")
            return False

        # Remove existing job if any
        self.remove_task(task_id)

        # Create job ID
        job_id = f"task_{task_id}_{keyword}"

        # Get trigger
        trigger_type, trigger_kwargs = config.to_apscheduler_trigger()

        if trigger_type == "cron":
            trigger = CronTrigger(**trigger_kwargs)
        else:
            trigger = IntervalTrigger(**trigger_kwargs)

        # Add job
        self.scheduler.add_job(
            self._execute_update,
            trigger,
            id=job_id,
            args=[task_id, keyword, args],
            replace_existing=True,
        )

        # Track task
        self._tasks[task_id] = ScheduledTask(
            task_id=task_id,
            keyword=keyword,
            schedule=schedule,
            args=args,
            job_id=job_id,
        )

        logger.info(f"Added scheduled task {task_id}: {keyword} @ {schedule}")
        print(f"[SCHEDULER] Added task {task_id}: {keyword} @ {schedule}", flush=True)

        return True

    def remove_task(self, task_id: int) -> bool:
        """Remove a scheduled task.

        Args:
            task_id: Vikunja task ID

        Returns:
            True if task was removed, False if not found
        """
        if task_id not in self._tasks:
            return False

        scheduled = self._tasks.pop(task_id)

        try:
            self.scheduler.remove_job(scheduled.job_id)
            logger.info(f"Removed scheduled task {task_id}")
        except Exception as e:
            logger.warning(f"Could not remove job {scheduled.job_id}: {e}")

        return True

    def get_task(self, task_id: int) -> Optional[ScheduledTask]:
        """Get scheduled task info.

        Args:
            task_id: Vikunja task ID

        Returns:
            ScheduledTask or None if not found
        """
        return self._tasks.get(task_id)

    def list_tasks(self) -> list[ScheduledTask]:
        """List all scheduled tasks."""
        return list(self._tasks.values())

    async def _scan_existing_tasks(self):
        """Scan Vikunja for tasks with schedules."""
        logger.info("Scanning for existing scheduled tasks...")

        try:
            # Get all tasks assigned to @eis bot
            # Note: This requires iterating through projects - simplified for now
            # In practice, we'd need to query all accessible tasks
            pass  # TODO: Implement full task scanning

        except VikunjaAPIError as e:
            logger.error(f"Failed to scan tasks: {e}")

    async def _execute_update(self, task_id: int, keyword: str, args: dict):
        """Execute a scheduled update for a task.

        Args:
            task_id: Vikunja task ID
            keyword: Handler keyword
            args: Handler arguments
        """
        logger.info(f"Executing scheduled update for task {task_id}: {keyword}")
        print(f"[SCHEDULER] Updating task {task_id}: {keyword}", flush=True)

        try:
            # Get fresh data from API
            if keyword == "weather":
                client = get_weather_client()
                response = await client.get_weather(args.get("location", ""))
            elif keyword == "stock":
                client = get_stock_client()
                response = await client.get_quote(args.get("ticker", ""))
            elif keyword == "news":
                client = get_news_client()
                response = await client.get_headlines(
                    query=args.get("query"),
                    category=args.get("category"),
                )
            else:
                logger.error(f"Unknown keyword: {keyword}")
                return

            if not response.success:
                logger.error(f"API error for task {task_id}: {response.error}")
                # Add error comment to task
                try:
                    self.client.add_comment(
                        task_id,
                        f"⚠️ Scheduled update failed: {response.error}"
                    )
                except VikunjaAPIError:
                    pass
                return

            # Get current task to preserve metadata
            try:
                task = self.client.get_task(task_id)
            except VikunjaAPIError as e:
                if "404" in str(e):
                    # Task deleted, remove from scheduler
                    logger.info(f"Task {task_id} deleted, removing from scheduler")
                    self.remove_task(task_id)
                    return
                raise

            # Extract existing metadata
            description = task.get("description", "")
            metadata, _ = MetadataManager.extract(description)

            if not metadata:
                # Create default metadata
                metadata = SmartTaskMetadata(
                    keyword=keyword,
                    schedule=self._tasks.get(task_id, ScheduledTask(
                        task_id=task_id, keyword=keyword,
                        schedule="", args=args, job_id=""
                    )).schedule,
                )

            # Update last_updated
            metadata.last_updated = datetime.now(timezone.utc).isoformat()

            # Format new description with fresh data
            import markdown
            html_content = markdown.markdown(
                response.formatted,
                extensions=['fenced_code', 'tables']
            )
            new_description = MetadataManager.format_html(metadata, html_content)

            # Update task
            self.client.update_task(task_id, description=new_description)

            logger.info(f"Updated task {task_id} with fresh {keyword} data")
            print(f"[SCHEDULER] ✓ Updated task {task_id}", flush=True)

        except VikunjaAPIError as e:
            logger.error(f"Failed to update task {task_id}: {e}")
            print(f"[SCHEDULER] ✗ Failed to update task {task_id}: {e}", flush=True)

        except Exception as e:
            logger.exception(f"Unexpected error updating task {task_id}: {e}")


# Singleton instance
_scheduler: Optional[TaskScheduler] = None


def get_task_scheduler(client: Optional[BotVikunjaClient] = None) -> TaskScheduler:
    """Get task scheduler singleton."""
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler(client)
    return _scheduler


async def run_scheduler():
    """Run the task scheduler (entry point for async execution)."""
    scheduler = get_task_scheduler()
    await scheduler.start()

    # Keep running
    while True:
        await asyncio.sleep(60)
