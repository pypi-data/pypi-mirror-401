"""
Tests for Schedule Parser and Task Scheduler.

Bead: solutions-hgwx.4
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from vikunja_mcp.schedule_parser import ScheduleParser, parse_schedule, ScheduleConfig


class TestScheduleParser:
    """Tests for schedule parsing."""

    @pytest.fixture
    def parser(self):
        return ScheduleParser()

    def test_parse_hourly(self, parser):
        """Test 'hourly' schedule."""
        config = parser.parse("hourly")
        assert config.valid
        assert config.minute == "0"

        trigger_type, kwargs = config.to_apscheduler_trigger()
        assert trigger_type == "cron"
        assert kwargs["minute"] == "0"

    def test_parse_daily(self, parser):
        """Test 'daily' schedule."""
        config = parser.parse("daily")
        assert config.valid
        assert config.hour == "9"  # Default 9am
        assert config.minute == "0"

    def test_parse_every_morning_at_7am(self, parser):
        """Test 'every morning at 7am'."""
        config = parser.parse("every morning at 7am")
        assert config.valid
        assert config.hour == "7"
        assert config.minute == "0"

    def test_parse_at_3pm(self, parser):
        """Test 'at 3pm'."""
        config = parser.parse("at 3pm")
        assert config.valid
        assert config.hour == "15"
        assert config.minute == "0"

    def test_parse_at_330pm(self, parser):
        """Test 'at 3:30pm'."""
        config = parser.parse("at 3:30pm")
        assert config.valid
        assert config.hour == "15"
        assert config.minute == "30"

    def test_parse_24h_time(self, parser):
        """Test '14:30'."""
        config = parser.parse("14:30")
        assert config.valid
        assert config.hour == "14"
        assert config.minute == "30"

    def test_parse_every_30_minutes(self, parser):
        """Test 'every 30 minutes'."""
        config = parser.parse("every 30 minutes")
        assert config.valid
        assert config.interval_minutes == 30

        trigger_type, kwargs = config.to_apscheduler_trigger()
        assert trigger_type == "interval"
        assert kwargs["minutes"] == 30

    def test_parse_every_2_hours(self, parser):
        """Test 'every 2 hours'."""
        config = parser.parse("every 2 hours")
        assert config.valid
        assert config.interval_hours == 2

        trigger_type, kwargs = config.to_apscheduler_trigger()
        assert trigger_type == "interval"
        assert kwargs["hours"] == 2

    def test_parse_weekday_morning(self, parser):
        """Test 'weekday morning at 8am'."""
        config = parser.parse("weekday morning at 8am")
        assert config.valid
        assert config.hour == "8"
        assert config.day_of_week == "mon-fri"

    def test_parse_monday_at_9am(self, parser):
        """Test 'monday at 9am'."""
        config = parser.parse("monday at 9am")
        assert config.valid
        assert config.hour == "9"
        assert config.day_of_week == "mon"

    def test_parse_noon(self, parser):
        """Test 'noon'."""
        config = parser.parse("noon")
        assert config.valid
        assert config.hour == "12"
        assert config.minute == "0"

    def test_parse_evening(self, parser):
        """Test 'evening'."""
        config = parser.parse("evening")
        assert config.valid
        assert config.hour == "18"
        assert config.minute == "0"

    def test_parse_invalid(self, parser):
        """Test invalid schedule."""
        config = parser.parse("whenever")
        assert not config.valid
        assert config.error is not None

    def test_parse_empty(self, parser):
        """Test empty schedule."""
        config = parser.parse("")
        assert not config.valid
        assert "Empty" in config.error

    def test_convenience_function(self):
        """Test parse_schedule convenience function."""
        config = parse_schedule("every morning at 6:30am")
        assert config.valid
        assert config.hour == "6"
        assert config.minute == "30"


class TestTaskScheduler:
    """Tests for TaskScheduler."""

    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        client.get_task = MagicMock(return_value={
            "id": 42,
            "title": "Weather Update",
            "description": "",
        })
        client.update_task = MagicMock()
        client.add_comment = MagicMock()
        return client

    async def test_add_task(self, mock_client):
        """Test adding a scheduled task."""
        from vikunja_mcp.task_scheduler import TaskScheduler

        scheduler = TaskScheduler(client=mock_client)

        result = scheduler.add_task(
            task_id=42,
            keyword="weather",
            schedule="every 30 minutes",
            args={"location": "Seattle"},
        )

        assert result is True
        assert 42 in scheduler._tasks
        assert scheduler._tasks[42].keyword == "weather"
        assert scheduler._tasks[42].schedule == "every 30 minutes"

    async def test_add_task_invalid_schedule(self, mock_client):
        """Test adding task with invalid schedule."""
        from vikunja_mcp.task_scheduler import TaskScheduler

        scheduler = TaskScheduler(client=mock_client)

        result = scheduler.add_task(
            task_id=42,
            keyword="weather",
            schedule="whenever",  # Invalid
            args={"location": "Seattle"},
        )

        assert result is False
        assert 42 not in scheduler._tasks

    async def test_remove_task(self, mock_client):
        """Test removing a scheduled task."""
        from vikunja_mcp.task_scheduler import TaskScheduler

        scheduler = TaskScheduler(client=mock_client)

        scheduler.add_task(
            task_id=42,
            keyword="weather",
            schedule="hourly",
            args={"location": "Seattle"},
        )

        result = scheduler.remove_task(42)

        assert result is True
        assert 42 not in scheduler._tasks

    async def test_remove_nonexistent_task(self, mock_client):
        """Test removing a task that doesn't exist."""
        from vikunja_mcp.task_scheduler import TaskScheduler

        scheduler = TaskScheduler(client=mock_client)
        result = scheduler.remove_task(999)

        assert result is False

    async def test_list_tasks(self, mock_client):
        """Test listing scheduled tasks."""
        from vikunja_mcp.task_scheduler import TaskScheduler

        scheduler = TaskScheduler(client=mock_client)

        scheduler.add_task(42, "weather", "hourly", {"location": "Seattle"})
        scheduler.add_task(43, "stock", "every 30 minutes", {"ticker": "AAPL"})

        tasks = scheduler.list_tasks()

        assert len(tasks) == 2
        assert any(t.task_id == 42 for t in tasks)
        assert any(t.task_id == 43 for t in tasks)


class TestKeywordHandlersWithSchedule:
    """Test keyword handlers with schedule parameter."""

    async def test_weather_with_valid_schedule(self):
        """Test weather handler with valid schedule."""
        from vikunja_mcp.keyword_handlers import KeywordHandlers
        from vikunja_mcp.api_clients import APIResponse

        mock_client = MagicMock()
        handlers = KeywordHandlers(client=mock_client)

        mock_response = APIResponse(
            success=True,
            data={"temp_f": 65},
            formatted="☀️ **Seattle**\n65°F",
        )

        with patch("vikunja_mcp.keyword_handlers.get_weather_client") as mock_weather:
            mock_weather.return_value.get_weather = AsyncMock(return_value=mock_response)

            result = await handlers.weather_handler({
                "location": "Seattle",
                "schedule": "every morning at 7am",
            })

        assert result.success is True
        assert "Auto-updating" in result.message
        assert result.data.get("schedule") == "every morning at 7am"
        assert result.data.get("keyword") == "weather"
        assert result.data.get("handler_args") == {"location": "Seattle"}

    async def test_weather_with_invalid_schedule(self):
        """Test weather handler with invalid schedule."""
        from vikunja_mcp.keyword_handlers import KeywordHandlers
        from vikunja_mcp.api_clients import APIResponse

        mock_client = MagicMock()
        handlers = KeywordHandlers(client=mock_client)

        mock_response = APIResponse(
            success=True,
            data={"temp_f": 65},
            formatted="☀️ **Seattle**\n65°F",
        )

        with patch("vikunja_mcp.keyword_handlers.get_weather_client") as mock_weather:
            mock_weather.return_value.get_weather = AsyncMock(return_value=mock_response)

            result = await handlers.weather_handler({
                "location": "Seattle",
                "schedule": "whenever",  # Invalid
            })

        assert result.success is True  # Still shows weather
        assert "Invalid schedule" in result.message
        assert result.data.get("schedule") is None  # No schedule in data

    async def test_stock_with_schedule(self):
        """Test stock handler with schedule."""
        from vikunja_mcp.keyword_handlers import KeywordHandlers
        from vikunja_mcp.api_clients import APIResponse

        mock_client = MagicMock()
        handlers = KeywordHandlers(client=mock_client)

        mock_response = APIResponse(
            success=True,
            data={"price": 150.0},
            formatted="📈 **AAPL** $150.00",
        )

        with patch("vikunja_mcp.keyword_handlers.get_stock_client") as mock_stock:
            mock_stock.return_value.get_quote = AsyncMock(return_value=mock_response)

            result = await handlers.stock_handler({
                "ticker": "AAPL",
                "schedule": "every 30 minutes",
            })

        assert result.success is True
        assert "Auto-updating" in result.message
        assert result.data.get("keyword") == "stock"
        assert result.data.get("handler_args") == {"ticker": "AAPL"}
