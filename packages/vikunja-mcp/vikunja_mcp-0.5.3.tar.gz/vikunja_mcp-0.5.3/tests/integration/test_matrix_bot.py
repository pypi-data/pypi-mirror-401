"""Integration tests for Matrix bot commands.

Tests the Matrix bot's command handling by sending actual messages
and verifying responses.

Run with: uv run pytest tests/integration/test_matrix_bot.py -v -m integration

Requires environment variables (see conftest.py for details).
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestStatsCommand:
    """Tests for the !stats command."""

    async def test_stats_command_returns_response(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """Sending !stats should return a stats response."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!stats",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !stats"
        # TODO: Add specific assertions about stats format
        # Expected: response contains task counts, project info, etc.

    async def test_stats_response_format(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """Stats response should have expected format."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!stats",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !stats"
        # TODO: Verify response format
        # Expected patterns:
        # - Contains task count
        # - Contains project info
        # - Contains instance indicator


class TestSwitchCommand:
    """Tests for the !switch command."""

    async def test_switch_to_personal_instance(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!switch personal should change context to personal instance."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!switch personal",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !switch"
        # TODO: Verify switch confirmation
        # Expected: message confirms switch to personal instance

    async def test_switch_to_work_instance(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!switch work should change context to work instance."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!switch work",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !switch"
        # TODO: Verify switch confirmation

    async def test_switch_invalid_instance(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!switch with invalid instance should return error."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!switch nonexistent",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !switch"
        # TODO: Verify error message about unknown instance


class TestContextPersistence:
    """Tests for context persistence across commands."""

    async def test_context_persists_after_switch(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """Context should persist after switching instances."""
        # First, switch to a specific instance
        switch_response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!switch personal",
            bot_user,
            timeout=30.0,
        )
        assert switch_response is not None, "Bot did not respond to !switch"

        # Then run a command and verify context in footer
        stats_response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!stats",
            bot_user,
            timeout=30.0,
        )
        assert stats_response is not None, "Bot did not respond to !stats"
        # TODO: Verify footer shows correct instance context

    async def test_context_shown_in_response_footer(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """Responses should include context indicator in footer."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "list my tasks",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond"
        # TODO: Verify footer format
        # Expected: response ends with context info like "[personal]" or "[work]"


class TestHelpCommand:
    """Tests for the !help command."""

    async def test_help_returns_command_list(
        self, matrix_client, bot_dm_room, bot_user
    ):
        """!help should return list of available commands."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "!help",
            bot_user,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !help"
        # TODO: Verify help content
        # Expected: lists available commands like !stats, !switch, etc.
