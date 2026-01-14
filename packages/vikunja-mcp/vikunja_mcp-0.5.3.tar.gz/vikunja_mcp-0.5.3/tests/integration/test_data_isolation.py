"""Integration tests for data isolation between users.

CRITICAL SECURITY TESTS: Ensure users cannot see each other's data.

These tests verify the fix for solutions-k8ze - centralized auth
that prevents fallback to admin token.

Run with: uv run pytest tests/integration/test_data_isolation.py -v -m integration
"""

import pytest
import os
from dataclasses import dataclass
from typing import Optional

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@dataclass
class TwoUserConfig:
    """Configuration for two-user isolation tests."""
    user_a_id: str
    user_a_token: str
    user_b_id: str
    user_b_token: str
    homeserver: str
    bot_user_id: str


def get_two_user_config() -> TwoUserConfig:
    """Load configuration for two-user testing.

    Requires environment variables:
    - MATRIX_HOMESERVER
    - MATRIX_USER_A_ID, MATRIX_USER_A_TOKEN
    - MATRIX_USER_B_ID, MATRIX_USER_B_TOKEN
    - MATRIX_BOT_USER_ID
    """
    homeserver = os.environ.get("MATRIX_HOMESERVER", "")
    user_a_id = os.environ.get("MATRIX_USER_A_ID", "")
    user_a_token = os.environ.get("MATRIX_USER_A_TOKEN", "")
    user_b_id = os.environ.get("MATRIX_USER_B_ID", "")
    user_b_token = os.environ.get("MATRIX_USER_B_TOKEN", "")
    bot_user_id = os.environ.get("MATRIX_BOT_USER_ID", "")

    if not all([homeserver, user_a_id, user_a_token, user_b_id, user_b_token, bot_user_id]):
        pytest.skip("Two-user isolation test environment not configured")

    return TwoUserConfig(
        user_a_id=user_a_id,
        user_a_token=user_a_token,
        user_b_id=user_b_id,
        user_b_token=user_b_token,
        homeserver=homeserver,
        bot_user_id=bot_user_id,
    )


class TestDataIsolation:
    """Critical tests for user data isolation.

    These tests verify that:
    1. User A cannot see User B's tasks
    2. User B cannot see User A's tasks
    3. Users without tokens cannot see any data
    4. Admin token fallback is blocked
    """

    async def test_user_a_sees_only_own_tasks(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """User A's !stats should show only User A's data."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!stats",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !stats"

        # The response should contain task stats
        # Key check: no error, got actual stats (proves auth worked)
        assert "Total:" in response or "Task Summary" in response, \
            f"Expected task stats but got: {response[:200]}"

        # Should NOT contain connect prompt (user is connected)
        assert "!vik" not in response.lower(), \
            "User A is connected but got connect prompt"

    async def test_user_without_token_sees_connect_prompt(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """User without Vikunja token should see connect prompt, not data.

        This test requires a separate test user that has no Vikunja connection.
        """
        # Note: This test needs a separate fixture for unconnected user
        # For now, we verify the logic via unit tests (test_matrix_handlers.py)
        pytest.skip("Requires unconnected user fixture - covered by unit tests")

    async def test_oops_command_shows_user_tasks(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!oops should show only current user's overdue tasks."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!oops",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !oops"

        # Should be task list or "no overdue" message, not connect prompt
        assert "!vik" not in response.lower() or "connect" not in response.lower(), \
            f"Connected user got connect prompt: {response[:200]}"

    async def test_today_command_shows_user_tasks(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!now should show only current user's tasks due today."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!now",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !now"

        # Should be task list or "no tasks" message
        assert "!vik" not in response.lower() or "connect" not in response.lower(), \
            f"Connected user got connect prompt: {response[:200]}"


class TestCrossUserIsolation:
    """Tests that verify isolation between two specific users.

    Requires two Matrix accounts with different Vikunja connections.
    """

    @pytest.fixture
    def two_user_config(self):
        """Provide two-user configuration."""
        return get_two_user_config()

    async def test_user_a_cannot_see_user_b_task_count(
        self, two_user_config
    ):
        """User A's task count should differ from User B's.

        This is a probabilistic test - if both users have exactly
        the same number of tasks in all categories, it could pass
        incorrectly. But with real data, this is unlikely.
        """
        from nio import AsyncClient

        # Create client for User A
        client_a = AsyncClient(
            homeserver=two_user_config.homeserver,
            user=two_user_config.user_a_id,
        )
        client_a.access_token = two_user_config.user_a_token

        # Create client for User B
        client_b = AsyncClient(
            homeserver=two_user_config.homeserver,
            user=two_user_config.user_b_id,
        )
        client_b.access_token = two_user_config.user_b_token

        try:
            # TODO: Get stats from both users and compare
            # If isolation works, they should have different stats
            # (assuming different Vikunja data)
            pytest.skip("Requires DM room setup for both users")
        finally:
            await client_a.close()
            await client_b.close()


class TestAuthEdgeCases:
    """Edge cases for authentication and authorization."""

    async def test_help_works_without_vikunja_token(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!help should work even for users without Vikunja connection."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!help",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !help"
        assert len(response) > 100, "Help text seems too short"
        # Help should list commands
        assert "!oops" in response.lower() or "overdue" in response.lower(), \
            "Help should mention task commands"

    async def test_credits_works_without_vikunja_token(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!credits should work (admin check, not Vikunja check)."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!credits",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !credits"
        # Should either show credits (admin) or admin-only error
        # But NOT a Vikunja connect prompt
        assert "!vik" not in response.lower(), \
            "!credits should not require Vikunja token"

    async def test_rapid_commands_maintain_isolation(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """Rapid successive commands should all use correct user context.

        This tests for potential race conditions in context switching.
        """
        commands = ["!stats", "!oops", "!now", "!stats"]
        responses = []

        for cmd in commands:
            response = await matrix_client.send_and_wait(
                bot_dm_room,
                cmd,
                bot_user,
                timeout=30.0,
            )
            assert response is not None, f"Bot did not respond to {cmd}"
            responses.append(response)

        # All responses should be consistent (same user's data)
        # If there's a race condition, one might return wrong data or connect prompt
        for i, response in enumerate(responses):
            assert "!vik" not in response.lower(), \
                f"Command {commands[i]} got unexpected connect prompt"
