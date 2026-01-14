"""
Integration tests for Context Management.

These tests run against a real PostgreSQL database to verify the full workflow.
Requires DATABASE_URL environment variable.

Bead: solutions-lt0f.9
"""

import os
import pytest
from datetime import datetime

# Skip all tests if DATABASE_URL not set
pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL not set"
)


# Add src to path and load modules directly (bypassing vikunja_mcp __init__.py)
import sys
from pathlib import Path
import importlib.util

src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Load token_broker module directly
token_broker_path = src_path / "vikunja_mcp" / "token_broker.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.token_broker", token_broker_path)
token_broker = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.token_broker'] = token_broker
spec.loader.exec_module(token_broker)

# Load context module directly
context_path = src_path / "vikunja_mcp" / "context.py"
spec = importlib.util.spec_from_file_location("vikunja_mcp.context", context_path)
context = importlib.util.module_from_spec(spec)
sys.modules['vikunja_mcp.context'] = context
spec.loader.exec_module(context)

# Import what we need
get_db = token_broker.get_db
get_user_active_instance = token_broker.get_user_active_instance
set_user_active_instance = token_broker.set_user_active_instance

get_project_context = context.get_project_context
set_project_context = context.set_project_context
clear_project_context = context.clear_project_context
get_user_context = context.get_user_context
switch_instance = context.switch_instance
ProjectContext = context.ProjectContext
UserContext = context.UserContext


# Test user ID (uses a test prefix to avoid conflicts)
TEST_USER = "@integration-test:matrix.factumerit.app"
TEST_INSTANCE_1 = "test-instance-1"
TEST_INSTANCE_2 = "test-instance-2"


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test data before and after each test."""
    _cleanup_test_data()
    yield
    _cleanup_test_data()


def _cleanup_test_data():
    """Remove all test data from database."""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Clean up user_project_context
                cur.execute(
                    "DELETE FROM user_project_context WHERE user_id = %s",
                    (TEST_USER,)
                )
                # Clean up user_preferences
                cur.execute(
                    "DELETE FROM user_preferences WHERE user_id = %s",
                    (TEST_USER,)
                )
                conn.commit()
    except Exception:
        pass  # Table might not exist yet


class TestProjectContextIntegration:
    """Integration tests for per-instance project context."""

    def test_set_and_get_project_context(self):
        """Can set and retrieve project context for an instance."""
        # Set project context
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")

        # Retrieve it
        ctx = get_project_context(TEST_USER, TEST_INSTANCE_1)

        assert ctx is not None
        assert ctx.project_id == 123
        assert ctx.project_name == "Kitchen"

    def test_project_context_is_per_instance(self):
        """Different instances have independent project contexts."""
        # Set different projects for different instances
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")
        set_project_context(TEST_USER, TEST_INSTANCE_2, 456, "Office")

        # Retrieve them
        ctx1 = get_project_context(TEST_USER, TEST_INSTANCE_1)
        ctx2 = get_project_context(TEST_USER, TEST_INSTANCE_2)

        assert ctx1.project_id == 123
        assert ctx1.project_name == "Kitchen"
        assert ctx2.project_id == 456
        assert ctx2.project_name == "Office"

    def test_clear_project_context(self):
        """Can clear project context for an instance."""
        # Set then clear
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")
        clear_project_context(TEST_USER, TEST_INSTANCE_1)

        # Verify cleared
        ctx = get_project_context(TEST_USER, TEST_INSTANCE_1)
        assert ctx is None

    def test_clear_does_not_affect_other_instances(self):
        """Clearing one instance's project doesn't affect others."""
        # Set projects for both instances
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")
        set_project_context(TEST_USER, TEST_INSTANCE_2, 456, "Office")

        # Clear only instance 1
        clear_project_context(TEST_USER, TEST_INSTANCE_1)

        # Instance 2 should still have its project
        ctx2 = get_project_context(TEST_USER, TEST_INSTANCE_2)
        assert ctx2 is not None
        assert ctx2.project_id == 456

    def test_update_project_context(self):
        """Can update existing project context."""
        # Set initial project
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")

        # Update to different project
        set_project_context(TEST_USER, TEST_INSTANCE_1, 789, "Bathroom")

        # Verify update
        ctx = get_project_context(TEST_USER, TEST_INSTANCE_1)
        assert ctx.project_id == 789
        assert ctx.project_name == "Bathroom"


class TestUserContextIntegration:
    """Integration tests for combined user context (instance + project)."""

    def test_get_user_context_with_instance_and_project(self):
        """get_user_context returns both instance and project."""
        # Set up context
        set_user_active_instance(TEST_USER, TEST_INSTANCE_1)
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")

        # Get combined context
        ctx = get_user_context(TEST_USER)

        assert ctx.user_id == TEST_USER
        assert ctx.active_instance == TEST_INSTANCE_1
        assert ctx.project is not None
        assert ctx.project.project_id == 123
        assert ctx.project.project_name == "Kitchen"

    def test_get_user_context_without_project(self):
        """get_user_context works when no project is set."""
        # Set only instance
        set_user_active_instance(TEST_USER, TEST_INSTANCE_1)

        # Get context
        ctx = get_user_context(TEST_USER)

        assert ctx.active_instance == TEST_INSTANCE_1
        assert ctx.project is None


class TestSwitchInstanceIntegration:
    """Integration tests for instance switching with project context restoration."""

    def test_switch_restores_project_context(self):
        """Switching instances restores that instance's project context."""
        # Set up project contexts for two instances
        set_user_active_instance(TEST_USER, TEST_INSTANCE_1)
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")
        set_project_context(TEST_USER, TEST_INSTANCE_2, 456, "Office")

        # Switch to instance 2
        ctx = switch_instance(TEST_USER, TEST_INSTANCE_2)

        # Should have instance 2's project
        assert ctx.active_instance == TEST_INSTANCE_2
        assert ctx.project is not None
        assert ctx.project.project_id == 456
        assert ctx.project.project_name == "Office"

        # Switch back to instance 1
        ctx = switch_instance(TEST_USER, TEST_INSTANCE_1)

        # Should have instance 1's project
        assert ctx.active_instance == TEST_INSTANCE_1
        assert ctx.project.project_id == 123
        assert ctx.project.project_name == "Kitchen"

    def test_switch_to_instance_without_project(self):
        """Switching to instance without project context returns no project."""
        # Set up only instance 1 with a project
        set_user_active_instance(TEST_USER, TEST_INSTANCE_1)
        set_project_context(TEST_USER, TEST_INSTANCE_1, 123, "Kitchen")

        # Switch to instance 2 (no project set)
        ctx = switch_instance(TEST_USER, TEST_INSTANCE_2)

        assert ctx.active_instance == TEST_INSTANCE_2
        assert ctx.project is None


class TestFullUserWorkflow:
    """Integration test for full user workflow."""

    def test_complete_workflow(self):
        """Tests complete user workflow: connect, set project, switch, restore."""
        # 1. User connects their first instance and sets active
        set_user_active_instance(TEST_USER, TEST_INSTANCE_1)

        # 2. User sets a project for this instance
        set_project_context(TEST_USER, TEST_INSTANCE_1, 100, "Home Renovation")

        # 3. Verify context
        ctx = get_user_context(TEST_USER)
        assert ctx.active_instance == TEST_INSTANCE_1
        assert ctx.project.project_name == "Home Renovation"

        # 4. User connects a second instance and switches to it
        # (In real usage, they would !vik to connect, then !switch)
        set_project_context(TEST_USER, TEST_INSTANCE_2, 200, "Work Tasks")
        ctx = switch_instance(TEST_USER, TEST_INSTANCE_2)

        # 5. Verify switched to instance 2 with its project
        assert ctx.active_instance == TEST_INSTANCE_2
        assert ctx.project.project_name == "Work Tasks"

        # 6. User switches back to instance 1
        ctx = switch_instance(TEST_USER, TEST_INSTANCE_1)

        # 7. Verify project context is restored
        assert ctx.active_instance == TEST_INSTANCE_1
        assert ctx.project.project_name == "Home Renovation"

        # 8. User clears project context for instance 1
        clear_project_context(TEST_USER, TEST_INSTANCE_1)
        ctx = get_user_context(TEST_USER)
        assert ctx.project is None

        # 9. Instance 2's project should still be there
        ctx = switch_instance(TEST_USER, TEST_INSTANCE_2)
        assert ctx.project.project_name == "Work Tasks"
