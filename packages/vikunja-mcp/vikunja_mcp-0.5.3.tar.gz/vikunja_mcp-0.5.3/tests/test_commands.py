"""
Unit tests for Commands module.

Tests for the rewritten Matrix bot commands.
These tests use mocking to avoid database and API dependencies.

Bead: solutions-lt0f.5, solutions-lt0f.6, solutions-lt0f.7, solutions-lt0f.8
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import importlib.util

# Load modules directly, bypassing vikunja_mcp package __init__.py
src_path = Path(__file__).parent.parent / "src"

# Mock the dependencies
mock_token_broker = MagicMock()
mock_token_broker.get_db = MagicMock()
mock_token_broker.get_user_active_instance = MagicMock(return_value="personal")
mock_token_broker.set_user_active_instance = MagicMock()
mock_token_broker.get_user_instances = MagicMock(return_value=["personal", "work"])
mock_token_broker.get_user_token = MagicMock(return_value="test_token")
mock_token_broker.get_user_instance_url = MagicMock(return_value="https://vikunja.test")
mock_token_broker.AuthRequired = Exception
sys.modules['vikunja_mcp.token_broker'] = mock_token_broker

# Load context module
context_path = src_path / "vikunja_mcp" / "context.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.context", context_path)
context = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.context'] = context
spec.loader.exec_module(context)

# Load vikunja_client module
client_path = src_path / "vikunja_mcp" / "vikunja_client.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.vikunja_client", client_path)
vikunja_client = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.vikunja_client'] = vikunja_client
spec.loader.exec_module(vikunja_client)

# Load commands module
commands_path = src_path / "vikunja_mcp" / "commands.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.commands", commands_path)
commands = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.commands'] = commands
spec.loader.exec_module(commands)

# Import what we need
from vikunja_mcp.commands import (
    handle_switch,
    handle_project,
    handle_now,
    handle_week,
    _format_context,
    _format_tasks,
)
from vikunja_mcp.context import UserContext, ProjectContext
from vikunja_mcp.vikunja_client import Task


# =============================================================================
# HELPER TESTS
# =============================================================================


class TestFormatContext:
    """Tests for _format_context helper."""

    def test_format_with_instance_and_project(self):
        """Formats context with both instance and project."""
        ctx = UserContext(
            user_id="@test:example.com",
            active_instance="personal",
            project=ProjectContext(project_id=123, project_name="Kitchen")
        )
        result = _format_context(ctx)
        assert "personal" in result
        assert "Kitchen" in result

    def test_format_without_project(self):
        """Formats context without project."""
        ctx = UserContext(
            user_id="@test:example.com",
            active_instance="work",
            project=None
        )
        result = _format_context(ctx)
        assert "work" in result
        assert "All" in result

    def test_format_without_instance(self):
        """Formats context without instance."""
        ctx = UserContext(
            user_id="@test:example.com",
            active_instance=None,
            project=None
        )
        result = _format_context(ctx)
        assert "default" in result


class TestFormatTasks:
    """Tests for _format_tasks helper."""

    def test_format_empty_tasks(self):
        """Formats empty task list."""
        result = _format_tasks([], "Due Today")
        assert "Due Today" in result
        assert "No tasks found" in result

    def test_format_single_task(self):
        """Formats single task."""
        tasks = [Task(id=1, title="Buy milk", done=False)]
        result = _format_tasks(tasks, "Due Today")
        assert "Due Today" in result
        assert "1 task" in result
        assert "Buy milk" in result

    def test_format_multiple_tasks(self):
        """Formats multiple tasks."""
        tasks = [
            Task(id=1, title="Task 1", done=False),
            Task(id=2, title="Task 2", done=False),
        ]
        result = _format_tasks(tasks, "Due Today")
        assert "2 tasks" in result
        assert "Task 1" in result
        assert "Task 2" in result

    def test_format_high_priority_task(self):
        """High priority tasks get fire emoji."""
        tasks = [Task(id=1, title="Urgent task", done=False, priority=5)]
        result = _format_tasks(tasks, "Urgent")
        assert "🔥" in result

    def test_format_limits_to_20(self):
        """Task list is limited to 20 items."""
        tasks = [Task(id=i, title=f"Task {i}", done=False) for i in range(25)]
        result = _format_tasks(tasks, "All Tasks")
        assert "...and 5 more" in result


# =============================================================================
# !switch TESTS
# =============================================================================


class TestHandleSwitch:
    """Tests for handle_switch command."""

    def test_no_args_shows_instances(self):
        """No args shows current instance and options."""
        with patch.object(commands, "get_user_instances") as mock_instances, \
             patch.object(commands, "get_user_active_instance") as mock_active, \
             patch.object(commands, "get_user_context") as mock_ctx:

            mock_instances.return_value = ["personal", "work"]
            mock_active.return_value = "personal"
            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=None
            )

            result = handle_switch("", "@test:example.com")

            assert result["success"] is True
            assert "personal" in result["response"]
            assert "work" in result["response"]
            assert result["eco_mode"] is True

    def test_no_instances_connected(self):
        """Shows message when no instances connected."""
        with patch.object(commands, "get_user_instances") as mock_instances:
            mock_instances.return_value = []

            result = handle_switch("", "@test:example.com")

            assert result["success"] is True
            assert "No Vikunja instances" in result["response"]
            assert "!vik" in result["response"]

    def test_switch_to_valid_instance(self):
        """Switches to a valid instance."""
        with patch.object(commands, "get_user_instances") as mock_instances, \
             patch.object(commands, "switch_instance") as mock_switch:

            mock_instances.return_value = ["personal", "work"]
            mock_switch.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="work",
                project=ProjectContext(project_id=456, project_name="Office")
            )

            result = handle_switch("work", "@test:example.com")

            assert result["success"] is True
            assert "Switched to **work**" in result["response"]
            assert "Project context restored" in result["response"]
            mock_switch.assert_called_once_with("@test:example.com", "work")

    def test_switch_to_invalid_instance(self):
        """Error when switching to non-existent instance."""
        with patch.object(commands, "get_user_instances") as mock_instances:
            mock_instances.return_value = ["personal", "work"]

            result = handle_switch("invalid", "@test:example.com")

            assert result["success"] is False
            assert "not found" in result["response"]
            assert "`personal`" in result["response"]


# =============================================================================
# !project TESTS
# =============================================================================


class TestHandleProject:
    """Tests for handle_project command."""

    def test_no_instance_connected(self):
        """Error when no instance connected."""
        with patch.object(commands, "get_user_context") as mock_ctx:
            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance=None,
                project=None
            )

            result = handle_project("", "@test:example.com")

            assert result["success"] is False
            assert "No Vikunja instance connected" in result["response"]

    def test_no_args_shows_current_project(self):
        """No args shows current project."""
        with patch.object(commands, "get_user_context") as mock_ctx:
            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=ProjectContext(project_id=123, project_name="Kitchen")
            )

            result = handle_project("", "@test:example.com")

            assert result["success"] is True
            assert "Kitchen" in result["response"]
            assert "!project clear" in result["response"]

    def test_no_args_no_project(self):
        """No args with no project set."""
        with patch.object(commands, "get_user_context") as mock_ctx:
            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=None
            )

            result = handle_project("", "@test:example.com")

            assert result["success"] is True
            assert "No active project" in result["response"]

    def test_clear_project(self):
        """Clears project context."""
        with patch.object(commands, "get_user_context") as mock_ctx, \
             patch.object(commands, "clear_project_context") as mock_clear:

            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=None
            )

            result = handle_project("clear", "@test:example.com")

            assert result["success"] is True
            assert "cleared" in result["response"]
            mock_clear.assert_called_once_with("@test:example.com", "personal")


# =============================================================================
# !now TESTS
# =============================================================================


class TestHandleNow:
    """Tests for handle_now command."""

    def test_no_instance_connected(self):
        """Error when no instance connected."""
        with patch.object(commands, "get_user_context") as mock_ctx:
            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance=None,
                project=None
            )

            result = handle_now("@test:example.com")

            assert result["success"] is False
            assert "No Vikunja instance connected" in result["response"]

    def test_returns_tasks_due_today(self):
        """Returns tasks due today."""
        with patch.object(commands, "get_user_context") as mock_ctx, \
             patch.object(commands, "VikunjaClient") as mock_client_class:

            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=None
            )

            mock_client = MagicMock()
            mock_client.get_tasks_due_today.return_value = [
                Task(id=1, title="Buy groceries", done=False),
                Task(id=2, title="Call mom", done=False),
            ]
            mock_client_class.return_value = mock_client

            result = handle_now("@test:example.com")

            assert result["success"] is True
            assert "Due Today" in result["response"]
            assert "Buy groceries" in result["response"]
            assert "2 tasks" in result["response"]
            assert result["eco_mode"] is True

    def test_respects_project_context(self):
        """Uses project context when set."""
        with patch.object(commands, "get_user_context") as mock_ctx, \
             patch.object(commands, "VikunjaClient") as mock_client_class:

            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=ProjectContext(project_id=123, project_name="Kitchen")
            )

            mock_client = MagicMock()
            mock_client.get_tasks_due_today.return_value = []
            mock_client_class.return_value = mock_client

            result = handle_now("@test:example.com")

            assert result["success"] is True
            assert "Kitchen" in result["response"]
            mock_client.get_tasks_due_today.assert_called_once_with(project_id=123)


# =============================================================================
# !week TESTS
# =============================================================================


class TestHandleWeek:
    """Tests for handle_week command."""

    def test_no_instance_connected(self):
        """Error when no instance connected."""
        with patch.object(commands, "get_user_context") as mock_ctx:
            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance=None,
                project=None
            )

            result = handle_week("@test:example.com")

            assert result["success"] is False
            assert "No Vikunja instance connected" in result["response"]

    def test_returns_tasks_due_this_week(self):
        """Returns tasks due this week."""
        with patch.object(commands, "get_user_context") as mock_ctx, \
             patch.object(commands, "VikunjaClient") as mock_client_class:

            mock_ctx.return_value = UserContext(
                user_id="@test:example.com",
                active_instance="personal",
                project=None
            )

            mock_client = MagicMock()
            mock_client.get_tasks_due_this_week.return_value = [
                Task(id=1, title="Weekly review", done=False),
            ]
            mock_client_class.return_value = mock_client

            result = handle_week("@test:example.com")

            assert result["success"] is True
            assert "Due This Week" in result["response"]
            assert "Weekly review" in result["response"]
            assert result["eco_mode"] is True
