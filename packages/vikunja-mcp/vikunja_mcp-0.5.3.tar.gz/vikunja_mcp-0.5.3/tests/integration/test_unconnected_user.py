"""Integration tests for users without Vikunja connection.

Tests that verify proper behavior when a Matrix user has NOT connected
to Vikunja yet. Critical for solutions-k8ze fix validation.

Run with: uv run pytest tests/integration/test_unconnected_user.py -v -m integration
"""

import pytest
import os
from dataclasses import dataclass

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@dataclass
class UnconnectedUserConfig:
    """Configuration for testing unconnected user behavior."""
    homeserver: str
    user_id: str
    access_token: str
    bot_user_id: str
    dm_room_id: str


def get_unconnected_user_config() -> UnconnectedUserConfig:
    """Load configuration for unconnected user testing.

    This requires a separate test account that has NO Vikunja token stored.

    Environment variables:
    - MATRIX_HOMESERVER
    - UNCONNECTED_USER_ID
    - UNCONNECTED_USER_TOKEN
    - MATRIX_BOT_USER_ID
    - UNCONNECTED_DM_ROOM_ID
    """
    homeserver = os.environ.get("MATRIX_HOMESERVER", "")
    user_id = os.environ.get("UNCONNECTED_USER_ID", "")
    access_token = os.environ.get("UNCONNECTED_USER_TOKEN", "")
    bot_user_id = os.environ.get("MATRIX_BOT_USER_ID", "")
    dm_room_id = os.environ.get("UNCONNECTED_DM_ROOM_ID", "")

    if not all([homeserver, user_id, access_token, bot_user_id, dm_room_id]):
        pytest.skip("Unconnected user test environment not configured")

    return UnconnectedUserConfig(
        homeserver=homeserver,
        user_id=user_id,
        access_token=access_token,
        bot_user_id=bot_user_id,
        dm_room_id=dm_room_id,
    )


class TestUnconnectedUserCommands:
    """Tests for commands when user has no Vikunja connection.

    CRITICAL: These tests verify the data isolation fix.
    An unconnected user should NEVER see any Vikunja data.
    """

    @pytest.fixture
    async def unconnected_client(self):
        """Create a Matrix client for an unconnected user."""
        from nio import AsyncClient
        from tests.integration.conftest import MatrixTestClient

        config = get_unconnected_user_config()

        client = AsyncClient(
            homeserver=config.homeserver,
            user=config.user_id,
        )
        client.access_token = config.access_token
        client.user_id = config.user_id

        wrapper = MatrixTestClient(client, config)
        await wrapper.start_sync()

        yield wrapper, config

        await client.close()

    async def test_stats_shows_connect_prompt(self, unconnected_client):
        """!stats from unconnected user should show connect prompt."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            "!stats",
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !stats"

        # CRITICAL: Must show connect prompt, NOT task data
        assert any([
            "connect" in response.lower(),
            "!vik" in response.lower(),
            "vikunja" in response.lower(),
        ]), f"Expected connect prompt but got: {response[:300]}"

        # CRITICAL: Must NOT show task statistics
        assert "Total:" not in response, \
            f"Unconnected user saw task stats: {response[:300]}"
        assert "overdue" not in response.lower() or "connect" in response.lower(), \
            f"Unconnected user saw task data: {response[:300]}"

    async def test_oops_shows_connect_prompt(self, unconnected_client):
        """!oops from unconnected user should show connect prompt."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            "!oops",
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !oops"

        # CRITICAL: Must show connect prompt
        assert any([
            "connect" in response.lower(),
            "!vik" in response.lower(),
        ]), f"Expected connect prompt but got: {response[:300]}"

    async def test_now_shows_connect_prompt(self, unconnected_client):
        """!now from unconnected user should show connect prompt."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            "!now",
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !now"

        # CRITICAL: Must show connect prompt
        assert any([
            "connect" in response.lower(),
            "!vik" in response.lower(),
        ]), f"Expected connect prompt but got: {response[:300]}"

    async def test_test_shows_connect_prompt(self, unconnected_client):
        """!test from unconnected user should show connect prompt.

        This was one of the buggy handlers before the fix.
        """
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            "!test",
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !test"

        # CRITICAL: Must show connect prompt, NOT project list
        assert any([
            "connect" in response.lower(),
            "!vik" in response.lower(),
        ]), f"Expected connect prompt but got: {response[:300]}"

        # CRITICAL: Must NOT show project count (would indicate data leak)
        assert "project" not in response.lower() or "connect" in response.lower(), \
            f"Unconnected user saw project data: {response[:300]}"

    async def test_done_shows_connect_prompt(self, unconnected_client):
        """!done from unconnected user should show connect prompt."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            "!done some task",
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !done"

        # Must show connect prompt
        assert any([
            "connect" in response.lower(),
            "!vik" in response.lower(),
        ]), f"Expected connect prompt but got: {response[:300]}"

    async def test_help_works_without_connection(self, unconnected_client):
        """!help should work even without Vikunja connection."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            "!help",
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, "Bot did not respond to !help"

        # Help should work (no Vikunja needed)
        assert len(response) > 100, "Help text seems too short"

        # Should mention commands
        assert "!oops" in response or "oops" in response.lower(), \
            "Help should list commands"


class TestAllTaskCommandsRequireToken:
    """Verify all task-related commands require Vikunja token.

    This is a regression test for solutions-k8ze.
    """

    @pytest.fixture
    async def unconnected_client(self):
        """Create a Matrix client for an unconnected user."""
        from nio import AsyncClient
        from tests.integration.conftest import MatrixTestClient

        config = get_unconnected_user_config()

        client = AsyncClient(
            homeserver=config.homeserver,
            user=config.user_id,
        )
        client.access_token = config.access_token
        client.user_id = config.user_id

        wrapper = MatrixTestClient(client, config)
        await wrapper.start_sync()

        yield wrapper, config

        await client.close()

    @pytest.mark.parametrize("command", [
        "!oops",
        "!overdue",
        "!now",
        "!today",
        "!week",
        "!fire",
        "!urgent",
        "!vip",
        "!priority",
        "!maybe",
        "!unscheduled",
        "!zen",
        "!focus",
        "!tasks",
        "!list",
        "!stats",
        "!test",
        "!done test task",
        "!switch personal",
        "!project",
        "!bind TestProject",
    ])
    async def test_command_requires_token(self, unconnected_client, command):
        """All task-related commands should require Vikunja token."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            command,
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, f"Bot did not respond to {command}"

        # CRITICAL: Must require connection
        assert any([
            "connect" in response.lower(),
            "!vik" in response.lower(),
            "vikunja" in response.lower(),
        ]), f"{command} did not require token: {response[:300]}"


class TestSafeCommandsWithoutToken:
    """Verify safe commands work without Vikunja token."""

    @pytest.fixture
    async def unconnected_client(self):
        """Create a Matrix client for an unconnected user."""
        from nio import AsyncClient
        from tests.integration.conftest import MatrixTestClient

        config = get_unconnected_user_config()

        client = AsyncClient(
            homeserver=config.homeserver,
            user=config.user_id,
        )
        client.access_token = config.access_token
        client.user_id = config.user_id

        wrapper = MatrixTestClient(client, config)
        await wrapper.start_sync()

        yield wrapper, config

        await client.close()

    @pytest.mark.parametrize("command,expected_content", [
        ("!help", ["command", "!oops"]),
        ("!h", ["command"]),
        ("!?", ["command"]),
    ])
    async def test_safe_command_works(self, unconnected_client, command, expected_content):
        """Safe commands should work without Vikunja token."""
        client, config = unconnected_client

        response = await client.send_and_wait(
            config.dm_room_id,
            command,
            config.bot_user_id,
            timeout=30.0,
        )

        assert response is not None, f"Bot did not respond to {command}"

        # Should NOT show connect prompt (command doesn't need Vikunja)
        # Note: Response might mention Vikunja in general context, that's OK
        for content in expected_content:
            assert content.lower() in response.lower(), \
                f"{command} response missing '{content}': {response[:300]}"
