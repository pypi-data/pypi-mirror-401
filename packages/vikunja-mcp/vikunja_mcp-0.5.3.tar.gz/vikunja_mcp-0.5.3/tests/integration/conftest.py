"""Shared fixtures for integration tests.

Matrix bot and OAuth flow integration tests.

Environment variables required (see .env.example):
- MATRIX_HOMESERVER: Matrix server URL (e.g., https://matrix.factumerit.app)
- MATRIX_USER_ID: Test user's Matrix ID (e.g., @testuser:factumerit.app)
- MATRIX_ACCESS_TOKEN: Access token for test user
- MATRIX_BOT_USER_ID: Bot's Matrix ID (e.g., @salve:factumerit.app)
- TEST_DM_ROOM_ID: Room ID for test DM with bot
- OAUTH_BASE_URL: Base URL for OAuth pages (e.g., https://vikunja.factumerit.app)
"""

import asyncio
import os
from dataclasses import dataclass
from typing import AsyncGenerator, Optional

import pytest
import pytest_asyncio
from nio import AsyncClient, RoomMessageText


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class MatrixConfig:
    """Matrix connection configuration."""
    homeserver: str
    user_id: str
    access_token: str
    bot_user_id: str
    dm_room_id: str


@dataclass
class OAuthConfig:
    """OAuth test configuration."""
    base_url: str
    connect_page: str = "/connect.html"
    matrix_connect_page: str = "/matrix-connect.html"


def get_matrix_config() -> MatrixConfig:
    """Load Matrix configuration from environment."""
    homeserver = os.environ.get("MATRIX_HOMESERVER", "")
    user_id = os.environ.get("MATRIX_USER_ID", "")
    access_token = os.environ.get("MATRIX_ACCESS_TOKEN", "")
    bot_user_id = os.environ.get("MATRIX_BOT_USER_ID", "")
    dm_room_id = os.environ.get("TEST_DM_ROOM_ID", "")

    if not all([homeserver, user_id, access_token, bot_user_id, dm_room_id]):
        pytest.skip("Matrix environment variables not configured")

    return MatrixConfig(
        homeserver=homeserver,
        user_id=user_id,
        access_token=access_token,
        bot_user_id=bot_user_id,
        dm_room_id=dm_room_id,
    )


def get_oauth_config() -> OAuthConfig:
    """Load OAuth configuration from environment."""
    base_url = os.environ.get("OAUTH_BASE_URL", "https://vikunja.factumerit.app")
    return OAuthConfig(base_url=base_url)


# =============================================================================
# Matrix Client Wrapper
# =============================================================================

class MatrixTestClient:
    """Wrapper around matrix-nio AsyncClient for testing.

    Provides convenience methods for sending messages and waiting for responses.
    """

    def __init__(self, client: AsyncClient, config: MatrixConfig):
        self.client = client
        self.config = config
        self._response_queue: asyncio.Queue = asyncio.Queue()

    async def send_message(self, room_id: str, message: str) -> str:
        """Send a text message to a room.

        Args:
            room_id: The room to send to
            message: The message text

        Returns:
            The event ID of the sent message
        """
        response = await self.client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message,
            },
        )
        return response.event_id

    async def send_and_wait(
        self,
        room_id: str,
        message: str,
        from_user: str,
        timeout: float = 30.0,
    ) -> Optional[str]:
        """Send a message and wait for a response from a specific user.

        Args:
            room_id: The room to send to
            message: The message text
            from_user: The user ID to wait for response from
            timeout: Maximum time to wait for response

        Returns:
            The response message body, or None if timeout
        """
        # Clear any pending messages
        while not self._response_queue.empty():
            try:
                self._response_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        # Send our message
        await self.send_message(room_id, message)

        # Wait for response
        try:
            start_time = asyncio.get_event_loop().time()
            while True:
                remaining = timeout - (asyncio.get_event_loop().time() - start_time)
                if remaining <= 0:
                    return None

                try:
                    event = await asyncio.wait_for(
                        self._response_queue.get(),
                        timeout=remaining,
                    )
                    if event.sender == from_user:
                        return event.body
                except asyncio.TimeoutError:
                    return None
        except Exception:
            return None

    def _on_message(self, room, event):
        """Callback for incoming messages."""
        if isinstance(event, RoomMessageText):
            self._response_queue.put_nowait(event)

    async def start_sync(self):
        """Start syncing with the homeserver."""
        self.client.add_event_callback(self._on_message, RoomMessageText)
        # Do initial sync
        await self.client.sync(timeout=10000)

    async def sync_once(self, timeout: int = 30000):
        """Do a single sync."""
        await self.client.sync(timeout=timeout)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def matrix_config() -> MatrixConfig:
    """Provide Matrix configuration."""
    return get_matrix_config()


@pytest.fixture(scope="session")
def oauth_config() -> OAuthConfig:
    """Provide OAuth configuration."""
    return get_oauth_config()


@pytest_asyncio.fixture(scope="function")
async def matrix_client(matrix_config: MatrixConfig) -> AsyncGenerator[MatrixTestClient, None]:
    """Provide a connected Matrix client for testing.

    Creates a new client for each test function to ensure isolation.
    """
    client = AsyncClient(
        homeserver=matrix_config.homeserver,
        user=matrix_config.user_id,
    )
    client.access_token = matrix_config.access_token
    client.user_id = matrix_config.user_id

    wrapper = MatrixTestClient(client, matrix_config)
    await wrapper.start_sync()

    yield wrapper

    await client.close()


@pytest.fixture(scope="function")
def bot_dm_room(matrix_config: MatrixConfig) -> str:
    """Provide the DM room ID for bot testing."""
    return matrix_config.dm_room_id


@pytest.fixture(scope="function")
def bot_user(matrix_config: MatrixConfig) -> str:
    """Provide the bot's user ID."""
    return matrix_config.bot_user_id


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure Playwright browser context."""
    return {
        "ignore_https_errors": True,
        "viewport": {"width": 1280, "height": 720},
    }
