"""
Unit tests for Context Management module.

Tests for the per-instance project context system.
These tests use mocking to avoid database dependencies.

Bead: solutions-lt0f.4
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import importlib.util

# Load context module directly, bypassing vikunja_mcp package __init__.py
# which imports heavy server.py dependencies

src_path = Path(__file__).parent.parent / "src"

# First, mock the token_broker module that context.py imports
mock_token_broker = MagicMock()
mock_token_broker.get_db = MagicMock()
mock_token_broker.get_user_active_instance = MagicMock(return_value=None)
mock_token_broker.set_user_active_instance = MagicMock()
sys.modules['vikunja_mcp.token_broker'] = mock_token_broker

# Now load context module directly
context_path = src_path / "vikunja_mcp" / "context.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.context", context_path)
context = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.context'] = context
spec.loader.exec_module(context)

# Import the classes and functions
ProjectContext = context.ProjectContext
UserContext = context.UserContext
get_project_context = context.get_project_context
set_project_context = context.set_project_context
clear_project_context = context.clear_project_context
get_user_context = context.get_user_context
switch_instance = context.switch_instance


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def mock_db():
    """Mock database connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    with patch.object(context, "get_db") as mock_get_db:
        mock_get_db.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_get_db.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_get_db, mock_conn, mock_cursor


# =============================================================================
# PROJECT CONTEXT TESTS
# =============================================================================


class TestGetProjectContext:
    """Tests for get_project_context function."""

    def test_returns_project_when_found(self, mock_db):
        """Returns ProjectContext when record exists."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = (123, "Kitchen")

        result = get_project_context("@user:matrix.example.com", "personal")

        assert result is not None
        assert result.project_id == 123
        assert result.project_name == "Kitchen"

    def test_returns_none_when_not_found(self, mock_db):
        """Returns None when no record exists."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None

        result = get_project_context("@user:matrix.example.com", "personal")

        assert result is None

    def test_handles_database_error(self, mock_db):
        """Returns None on database error (doesn't crash)."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.execute.side_effect = Exception("DB error")

        result = get_project_context("@user:matrix.example.com", "personal")

        assert result is None


class TestSetProjectContext:
    """Tests for set_project_context function."""

    def test_inserts_new_context(self, mock_db):
        """Inserts new record when none exists."""
        mock_get_db, mock_conn, mock_cursor = mock_db

        set_project_context("@user:matrix.example.com", "personal", 123, "Kitchen")

        # Verify execute was called with INSERT ... ON CONFLICT
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args
        assert "INSERT INTO user_project_context" in call_args[0][0]
        assert "@user:matrix.example.com" in call_args[0][1]
        assert "personal" in call_args[0][1]
        assert 123 in call_args[0][1]

    def test_raises_on_database_error(self, mock_db):
        """Raises exception on database error."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.execute.side_effect = Exception("DB error")

        with pytest.raises(Exception, match="DB error"):
            set_project_context("@user:matrix.example.com", "personal", 123, "Kitchen")


class TestClearProjectContext:
    """Tests for clear_project_context function."""

    def test_deletes_context(self, mock_db):
        """Deletes the project context record."""
        mock_get_db, mock_conn, mock_cursor = mock_db

        clear_project_context("@user:matrix.example.com", "personal")

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args
        assert "DELETE FROM user_project_context" in call_args[0][0]


# =============================================================================
# USER CONTEXT TESTS
# =============================================================================


class TestGetUserContext:
    """Tests for get_user_context function."""

    def test_returns_full_context(self, mock_db):
        """Returns UserContext with instance and project."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = (456, "Bathroom")

        with patch.object(context, "get_user_active_instance") as mock_instance:
            mock_instance.return_value = "personal"

            result = get_user_context("@user:matrix.example.com")

        assert result.user_id == "@user:matrix.example.com"
        assert result.active_instance == "personal"
        assert result.project is not None
        assert result.project.project_id == 456
        assert result.project.project_name == "Bathroom"

    def test_returns_context_without_project(self, mock_db):
        """Returns UserContext with instance but no project."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None

        with patch.object(context, "get_user_active_instance") as mock_instance:
            mock_instance.return_value = "personal"

            result = get_user_context("@user:matrix.example.com")

        assert result.user_id == "@user:matrix.example.com"
        assert result.active_instance == "personal"
        assert result.project is None

    def test_returns_context_without_instance(self, mock_db):
        """Returns UserContext with no instance (new user)."""
        mock_get_db, mock_conn, mock_cursor = mock_db

        with patch.object(context, "get_user_active_instance") as mock_instance:
            mock_instance.return_value = None

            result = get_user_context("@newuser:matrix.example.com")

        assert result.user_id == "@newuser:matrix.example.com"
        assert result.active_instance is None
        assert result.project is None


class TestSwitchInstance:
    """Tests for switch_instance function."""

    def test_switches_and_restores_project(self, mock_db):
        """Switches instance and restores project context."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = (789, "Office")

        with patch.object(context, "set_user_active_instance") as mock_set_instance:

            result = switch_instance("@user:matrix.example.com", "work")

        mock_set_instance.assert_called_once_with("@user:matrix.example.com", "work")
        assert result.user_id == "@user:matrix.example.com"
        assert result.active_instance == "work"
        assert result.project is not None
        assert result.project.project_id == 789
        assert result.project.project_name == "Office"

    def test_switches_without_project(self, mock_db):
        """Switches instance when no project context exists."""
        mock_get_db, mock_conn, mock_cursor = mock_db
        mock_cursor.fetchone.return_value = None

        with patch.object(context, "set_user_active_instance") as mock_set_instance:

            result = switch_instance("@user:matrix.example.com", "new-instance")

        assert result.active_instance == "new-instance"
        assert result.project is None


# =============================================================================
# DATACLASS TESTS
# =============================================================================


class TestDataclasses:
    """Tests for dataclass creation and equality."""

    def test_project_context_creation(self):
        """ProjectContext can be created with required fields."""
        ctx = ProjectContext(project_id=123)
        assert ctx.project_id == 123
        assert ctx.project_name is None

    def test_project_context_with_name(self):
        """ProjectContext can include project name."""
        ctx = ProjectContext(project_id=123, project_name="My Project")
        assert ctx.project_id == 123
        assert ctx.project_name == "My Project"

    def test_user_context_creation(self):
        """UserContext can be created with minimal fields."""
        ctx = UserContext(user_id="@test:example.com")
        assert ctx.user_id == "@test:example.com"
        assert ctx.active_instance is None
        assert ctx.project is None

    def test_user_context_full(self):
        """UserContext can be created with all fields."""
        project = ProjectContext(project_id=123, project_name="Kitchen")
        ctx = UserContext(
            user_id="@test:example.com",
            active_instance="personal",
            project=project
        )
        assert ctx.user_id == "@test:example.com"
        assert ctx.active_instance == "personal"
        assert ctx.project.project_id == 123
