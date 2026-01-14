"""Matrix client for Vikunja bot.

Connects to Matrix homeserver and bridges messages to the handler layer.
Uses matrix-nio for the Matrix protocol.
"""

import asyncio
import logging
import os
import time
from typing import Optional

import aiohttp
from aiohttp import ClientTimeout

from nio import (
    AsyncClient,
    AsyncClientConfig,
    InviteMemberEvent,
    LoginResponse,
    MatrixRoom,
    RoomMessageText,
    RoomPreset,
    SyncResponse,
)
from nio.store import SqliteStore

from .matrix_handlers import handle_matrix_message, _get_matrix_welcome_message
from .server import _matrix_chat_with_claude, _is_first_contact, _mark_user_welcomed

logger = logging.getLogger(__name__)

# Global bot instance for conversation history access
_matrix_bot_instance: Optional["MatrixBot"] = None


class MatrixBot:
    """Matrix bot that bridges messages to Vikunja handlers."""

    def __init__(
        self,
        homeserver: str,
        user_id: str,
        password: Optional[str] = None,
        access_token: Optional[str] = None,
        device_id: Optional[str] = None,
        admin_ids: Optional[list[str]] = None,
        welcome_room_id: Optional[str] = None,
    ):
        """Initialize Matrix bot.

        Args:
            homeserver: Matrix homeserver URL (e.g., https://matrix.example.com)
            user_id: Bot's Matrix user ID (e.g., @bot:matrix.example.com)
            password: Bot's password (optional if access_token provided)
            access_token: Bot's access token (optional, preferred over password)
            device_id: Optional device ID for session persistence
            admin_ids: List of admin Matrix user IDs
            welcome_room_id: Room ID to monitor for new user joins (auto-DM welcome)
        """
        self.homeserver = homeserver
        self.user_id = user_id
        self.password = password
        self.access_token = access_token
        self.device_id = device_id or "vikunja_bot"
        self.admin_ids = admin_ids or []
        self.welcome_room_id = welcome_room_id

        # Set up crypto store for E2EE (unverified mode)
        # Store path from env var or default to /data/crypto_store
        store_path = os.environ.get("MATRIX_CRYPTO_STORE_PATH", "/data/crypto_store")

        # Ensure crypto store directory exists
        os.makedirs(store_path, exist_ok=True)

        # Create crypto store for E2EE support
        store = SqliteStore(
            user_id=user_id,
            device_id=self.device_id,
            store_path=store_path,
        )

        # Client config - enable E2EE (unverified mode)
        # This eliminates "room not encrypted" warnings on every login
        # Users will see one-time "bot not verified" prompt (dismissible)
        config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            encryption_enabled=True,  # Enable E2EE
            store_sync_tokens=True,   # Persist sync tokens
            store=store,              # Crypto store for keys
        )

        self.client = AsyncClient(
            homeserver=homeserver,
            user=user_id,
            device_id=self.device_id,
            config=config,
        )

        # If access token provided, set it directly (along with user_id)
        if access_token:
            self.client.access_token = access_token
            self.client.user_id = user_id  # Required for sync to work
            logger.info(f"Matrix bot initialized with access token for {user_id} on {homeserver}")
        else:
            logger.info(f"Matrix bot initialized with password for {user_id} on {homeserver}")

        # Track startup time to ignore old messages
        self.startup_time = int(time.time() * 1000)

        # Cache for DM room IDs
        self.dm_rooms: dict[str, str] = {}  # user_id -> room_id

        # Message history cache for conversation memory
        # Structure: {room_id: [(timestamp, sender_id, message_text), ...]}
        # Keep last 100 messages per room
        self.message_cache: dict[str, list[tuple[int, str, str]]] = {}
        self.max_cache_size = 100

        # Sync state
        self.next_batch: Optional[str] = None

    async def _nio_sync_loop(self) -> None:
        """Sync loop using nio's sync() for proper E2EE support.

        Uses nio's sync() instead of sync_forever() for more control,
        while still benefiting from nio's automatic decryption.

        Bead: solutions-3yrh
        """
        timeout = 30000  # 30 seconds
        sync_count = 0

        while True:
            try:
                sync_count += 1
                print(f"[SYNC] Sync #{sync_count} starting", flush=True)
                logger.info(f"Sync #{sync_count} starting")

                # Use nio's sync() - handles E2EE decryption automatically
                response = await self.client.sync(timeout=timeout, full_state=(sync_count == 1))

                if isinstance(response, SyncResponse):
                    print(f"[SYNC] Sync #{sync_count} received {len(response.rooms.join)} room updates", flush=True)

                    # Process joined rooms
                    for room_id, room_info in response.rooms.join.items():
                        # Process timeline events (nio has already decrypted them)
                        for event in room_info.timeline.events:
                            await self._process_nio_event(room_id, event)

                        # Process state events
                        for event in room_info.state:
                            await self._process_nio_event(room_id, event)

                    # Process invites
                    for room_id in response.rooms.invite:
                        logger.info(f"Received invite to room {room_id}, auto-joining...")
                        await self._join_room(room_id)

                else:
                    # SyncError - log and retry
                    logger.error(f"Sync error: {response}")
                    print(f"[SYNC] Sync error: {response}", flush=True)
                    await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Error in sync loop: {e}", exc_info=True)
                print(f"[SYNC] ERROR in sync loop: {e}", flush=True)
                await asyncio.sleep(5)

    async def _process_nio_event(self, room_id: str, event) -> None:
        """Process a matrix-nio event (already decrypted if needed)."""
        # Handle RoomMessageText events (decrypted messages)
        if isinstance(event, RoomMessageText):
            sender = event.sender
            body = event.body
            timestamp = event.server_timestamp

            print(f"[MESSAGE] room={room_id}, sender={sender}, body={body[:50] if body else ''}", flush=True)

            # Ignore old messages (before bot startup)
            if timestamp < self.startup_time:
                print(f"[MESSAGE] Ignoring old message", flush=True)
                return

            # Cache the message
            self._cache_message(room_id, timestamp, sender, body)

            # Ignore our own messages
            if sender == self.user_id:
                return

            await self._handle_message(room_id, sender, body, timestamp)
            return

        # Handle MegolmEvent (failed to decrypt - missing keys)
        if hasattr(event, 'source') and event.source.get('type') == 'm.room.encrypted':
            sender = getattr(event, 'sender', 'unknown')
            logger.warning(f"Could not decrypt message from {sender} in {room_id} - missing keys")
            print(f"[CRYPTO] Failed to decrypt message from {sender} - missing session keys", flush=True)
            return

        # Handle membership events
        if isinstance(event, InviteMemberEvent):
            await self._handle_membership_event(room_id, {
                "type": "m.room.member",
                "sender": event.sender,
                "state_key": event.state_key,
                "content": {"membership": event.membership},
                "origin_server_ts": getattr(event, 'server_timestamp', 0),
            })
            return

        # Handle other room member events
        if hasattr(event, 'membership'):
            await self._handle_membership_event(room_id, {
                "type": "m.room.member",
                "sender": getattr(event, 'sender', ''),
                "state_key": getattr(event, 'state_key', ''),
                "content": {"membership": event.membership},
                "origin_server_ts": getattr(event, 'server_timestamp', 0),
            })

    async def _handle_message(self, room_id: str, sender: str, body: str, timestamp: int) -> None:
        """Handle a decrypted message."""
        logger.info(f"Received message from {sender} in {room_id}: {body[:50]}...")

        # Check if this is a DM
        is_dm = await self._is_dm_room(room_id)
        print(f"[MESSAGE] is_dm={is_dm} for room {room_id}", flush=True)

        # If message is in public room, only respond if mentioned
        if not is_dm:
            bot_mentioned = f"@{self.user_id.split(':')[0][1:]}" in body or self.user_id in body
            if bot_mentioned:
                auto_response = f"👋 Hi! Let's take this to DMs for a better experience. Please send me a direct message!"
                await self._send_message(room_id, auto_response)
            return

        # Handle the message
        try:
            result = handle_matrix_message(
                message=body,
                user_id=sender,
                room_id=room_id,
                is_dm=is_dm,
            )

            if result.get("response"):
                await self._send_message(room_id, result["response"])
            elif result.get("needs_llm"):
                # User-level registration check for LLM access (defense in depth)
                # Must be in `users` table (set via OAuth callback, not !vik)
                from .token_broker import is_registered_user
                from .server import _get_matrix_connect_prompt

                if not is_registered_user(sender):
                    # No token = no LLM access, show connect prompt
                    connect_msg = (
                        "To use natural language commands, please connect your Vikunja account first.\n\n"
                        + _get_matrix_connect_prompt(sender) + "\n\n"
                        "_Or use `!help` to see available commands._"
                    )
                    await self._send_message(room_id, connect_msg)
                else:
                    # Has token, allow LLM access
                    try:
                        llm_response = _matrix_chat_with_claude(
                            user_message=result.get("original_message", body),
                            user_id=sender,
                            room_id=room_id,
                        )
                        if llm_response:
                            await self._send_message(room_id, llm_response)
                    except Exception as llm_error:
                        logger.error(f"LLM error: {llm_error}", exc_info=True)
                        await self._send_message(room_id, "Sorry, I encountered an error. Try `!help` for commands.")
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)

    # Legacy custom sync loop - kept for fallback if nio sync fails
    async def _custom_sync_loop(self) -> None:
        """Custom sync loop using raw HTTP (fallback, no E2EE decryption)."""
        timeout = 30000  # 30 seconds
        sync_count = 0

        client_timeout = ClientTimeout(total=60, sock_read=35)
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            while True:
                try:
                    sync_count += 1
                    url = f"{self.homeserver}/_matrix/client/v3/sync"
                    params = {"timeout": timeout}
                    if self.next_batch:
                        params["since"] = self.next_batch

                    headers = {"Authorization": f"Bearer {self.client.access_token}"}
                    print(f"[SYNC-LEGACY] Sync #{sync_count} starting", flush=True)

                    async with session.get(url, params=params, headers=headers) as resp:
                        if resp.status != 200:
                            logger.error(f"Sync failed: {resp.status}")
                            await asyncio.sleep(5)
                            continue

                        data = await resp.json()
                        self.next_batch = data.get("next_batch")

                        rooms = data.get("rooms", {})
                        joined_rooms = rooms.get("join", {})

                        for room_id, room_data in joined_rooms.items():
                            for event in room_data.get("state", {}).get("events", []):
                                await self._process_event(room_id, event)
                            for event in room_data.get("timeline", {}).get("events", []):
                                await self._process_event(room_id, event)

                        for room_id in rooms.get("invite", {}):
                            await self._join_room(room_id)

                except Exception as e:
                    logger.error(f"Error in sync loop: {e}", exc_info=True)
                    await asyncio.sleep(5)

    async def _process_event(self, room_id: str, event: dict) -> None:
        """Process a single Matrix event."""
        event_type = event.get("type")

        # Handle membership events (for welcome room auto-DM)
        if event_type == "m.room.member":
            await self._handle_membership_event(room_id, event)
            return

        if event_type == "m.room.message":
            sender = event.get("sender")
            content = event.get("content", {})
            body = content.get("body", "")
            event_id = event.get("event_id")
            timestamp = event.get("origin_server_ts", 0)

            print(f"[MESSAGE] room={room_id}, sender={sender}, body={body[:50]}, timestamp={timestamp}", flush=True)

            # Ignore old messages (before bot startup)
            if timestamp < self.startup_time:
                print(f"[MESSAGE] Ignoring old message (timestamp={timestamp} < startup={self.startup_time})", flush=True)
                return

            # Cache user message (even if it's from us, for conversation history)
            self._cache_message(room_id, timestamp, sender, body)

            # Ignore our own messages for processing
            if sender == self.user_id:
                print(f"[MESSAGE] Ignoring our own message", flush=True)
                return

            logger.info(f"Received message from {sender} in {room_id}: {body}")
            print(f"[MESSAGE] Processing message from {sender}", flush=True)

            # Check if this is a DM or public room
            is_dm = await self._is_dm_room(room_id)
            print(f"[MESSAGE] is_dm={is_dm} for room {room_id}", flush=True)

            # If message is in public room (like #salve), only respond if mentioned
            if not is_dm:
                # Check if bot is mentioned
                bot_mentioned = f"@{self.user_id.split(':')[0][1:]}" in body or self.user_id in body
                print(f"[MESSAGE] Public room message, bot_mentioned={bot_mentioned}", flush=True)

                if bot_mentioned:
                    logger.info(f"Bot mentioned in public room {room_id}, sending auto-responder")
                    auto_response = f"👋 Hi! Let's take this to DMs for a better experience. Please send me a direct message!"
                    await self._send_message(room_id, auto_response)
                else:
                    logger.info(f"Ignoring public room message (not mentioned)")

                return

            # Handle the message (not async, returns dict)
            try:
                result = handle_matrix_message(
                    message=body,
                    user_id=sender,
                    room_id=room_id,
                    is_dm=is_dm,
                )
                logger.info(f"Handler result: success={result.get('success')}, has_response={bool(result.get('response'))}")

                # Send response if available (even if success=False, we want to send error messages)
                if result.get("response"):
                    logger.info(f"Sending response to {room_id}: {result['response'][:100]}...")
                    await self._send_message(room_id, result["response"])
                elif result.get("needs_llm"):
                    # Use LLM to handle natural language
                    logger.info(f"needs_llm=True, calling _matrix_chat_with_claude")
                    try:
                        llm_response = _matrix_chat_with_claude(
                            user_message=result.get("original_message", body),
                            user_id=sender,
                            room_id=room_id,
                        )
                        if llm_response:
                            await self._send_message(room_id, llm_response)
                        else:
                            logger.warning("LLM returned empty response")
                    except Exception as llm_error:
                        logger.error(f"LLM error: {llm_error}", exc_info=True)
                        await self._send_message(
                            room_id,
                            f"Sorry, I encountered an error processing your request. Try `!help` for commands."
                        )
                else:
                    logger.warning(f"No response to send: {result}")
            except Exception as e:
                logger.error(f"Error handling message: {e}", exc_info=True)

    async def _join_room(self, room_id: str) -> None:
        """Join a room using raw HTTP."""
        url = f"{self.homeserver}/_matrix/client/v3/rooms/{room_id}/join"
        headers = {"Authorization": f"Bearer {self.client.access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as resp:
                if resp.status == 200:
                    logger.info(f"Joined room {room_id}")
                else:
                    logger.error(f"Failed to join room {room_id}: {await resp.text()}")

    async def _handle_membership_event(self, room_id: str, event: dict) -> None:
        """Handle m.room.member events for welcome room auto-DM.

        When a new user joins the welcome room, automatically DM them
        with a welcome message and Vikunja connect link.
        """
        content = event.get("content", {})
        membership = content.get("membership")
        state_key = event.get("state_key", "?")

        # Debug: log ALL membership events
        print(f"[MATRIX] Membership event: room={room_id}, user={state_key}, membership={membership}", flush=True)

        # Only process if welcome room is configured
        if not self.welcome_room_id:
            print(f"[MATRIX] No welcome room configured, skipping", flush=True)
            return

        # Only process events from the welcome room
        if room_id != self.welcome_room_id:
            print(f"[MATRIX] Not welcome room ({self.welcome_room_id}), skipping", flush=True)
            return

        # Only process joins
        if membership != "join":
            print(f"[MATRIX] Not a join event, skipping", flush=True)
            return

        # Get the user who joined (state_key is the user ID for membership events)
        new_user_id = event.get("state_key")
        if not new_user_id:
            print(f"[MATRIX] No state_key, skipping", flush=True)
            return

        # Don't welcome ourselves
        if new_user_id == self.user_id:
            print(f"[MATRIX] It's us ({self.user_id}), skipping", flush=True)
            return

        # Check if we've already welcomed this user
        if not _is_first_contact(new_user_id):
            print(f"[MATRIX] User {new_user_id} already welcomed, skipping", flush=True)
            return

        # Check timestamp to avoid welcoming on historical events
        timestamp = event.get("origin_server_ts", 0)
        print(f"[MATRIX] Timestamp check: event={timestamp}, startup={self.startup_time}", flush=True)
        if timestamp < self.startup_time:
            print(f"[MATRIX] Historical event from {new_user_id}, skipping", flush=True)
            return

        print(f"[MATRIX] *** SENDING WELCOME DM to {new_user_id} ***", flush=True)
        logger.info(f"New user {new_user_id} joined welcome room, sending DM")

        try:
            # Step 1: Send public welcome in #salve
            public_welcome = f"👋 Welcome, {new_user_id}! I've sent you a DM to get started. Please accept the chat request from me."
            await self._send_message(room_id, public_welcome)
            logger.info(f"Sent public welcome to {new_user_id} in {room_id}")

            # Step 2: Create or get DM room with the new user
            dm_room_id = await self._get_or_create_dm(new_user_id)
            if not dm_room_id:
                logger.error(f"Failed to create DM room with {new_user_id}")
                return

            # Step 3: Generate full welcome message with connect link (for DM only)
            welcome_msg = _get_matrix_welcome_message(new_user_id)

            # Step 4: Send the private welcome message
            await self._send_message(dm_room_id, welcome_msg)

            # Mark user as welcomed
            _mark_user_welcomed(new_user_id)

            logger.info(f"Successfully welcomed new user {new_user_id}")

        except Exception as e:
            logger.error(f"Error welcoming new user {new_user_id}: {e}", exc_info=True)

    async def _send_message(self, room_id: str, message: str) -> None:
        """Send a message to a room using raw HTTP."""
        url = f"{self.homeserver}/_matrix/client/v3/rooms/{room_id}/send/m.room.message"
        headers = {
            "Authorization": f"Bearer {self.client.access_token}",
            "Content-Type": "application/json",
        }
        body = {
            "msgtype": "m.text",
            "body": message,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as resp:
                if resp.status == 200:
                    logger.debug(f"Sent message to {room_id}")
                    # Cache bot's response for conversation history
                    timestamp = int(time.time() * 1000)
                    self._cache_message(room_id, timestamp, self.user_id, message)
                else:
                    logger.error(f"Failed to send message to {room_id}: {await resp.text()}")

    def _cache_message(self, room_id: str, timestamp: int, sender: str, message: str) -> None:
        """Cache a message for conversation history.

        Args:
            room_id: Matrix room ID
            timestamp: Message timestamp in milliseconds
            sender: User ID of sender
            message: Message text
        """
        if room_id not in self.message_cache:
            self.message_cache[room_id] = []

        # Add message to cache
        self.message_cache[room_id].append((timestamp, sender, message))

        # Trim cache if too large (keep most recent messages)
        if len(self.message_cache[room_id]) > self.max_cache_size:
            self.message_cache[room_id] = self.message_cache[room_id][-self.max_cache_size:]

    def get_message_history(self, room_id: str, limit: int = 20) -> list[tuple[int, str, str]]:
        """Get cached message history for a room.

        Args:
            room_id: Matrix room ID
            limit: Maximum number of messages to return

        Returns:
            List of (timestamp, sender_id, message_text) tuples, oldest first
        """
        if room_id not in self.message_cache:
            return []

        # Return last N messages
        messages = self.message_cache[room_id][-limit:]
        return messages

    async def start(self) -> bool:
        """Start the bot - login and begin sync loop.

        Returns:
            True if started successfully, False otherwise
        """
        global _matrix_bot_instance

        try:
            # Login (only if access token not already set)
            if not self.access_token:
                logger.info(f"Attempting password login to {self.homeserver} as {self.user_id}")
                response = await self.client.login(self.password, device_name=self.device_id)

                if not isinstance(response, LoginResponse):
                    logger.error(f"Failed to login: {response}")
                    logger.error(f"Response type: {type(response)}")
                    if hasattr(response, '__dict__'):
                        logger.error(f"Response details: {response.__dict__}")
                    return False

                logger.info(f"Logged in as {self.user_id}")
            else:
                logger.info(f"Using access token for {self.user_id}")

            # Set global instance for conversation history access
            _matrix_bot_instance = self

            # Load crypto store if it exists (restores E2EE session keys)
            # This is critical for surviving restarts without losing decryption ability
            if self.client.store:
                logger.info("Loading crypto store...")
                print("[CRYPTO] Loading crypto store from persistent storage", flush=True)

            # Start nio sync loop with E2EE support
            # Falls back to custom loop if nio sync has issues
            logger.info("Starting nio sync loop with E2EE...")
            try:
                await self._nio_sync_loop()
            except Exception as e:
                logger.error(f"Nio sync failed: {e}, falling back to custom sync (no E2EE)")
                print(f"[SYNC] Nio sync failed, falling back to legacy (no E2EE): {e}", flush=True)
                await self._custom_sync_loop()

            return True
        except Exception as e:
            logger.error(f"Exception during Matrix bot startup: {e}", exc_info=True)
            return False

    async def stop(self) -> None:
        """Stop the bot gracefully."""
        logger.info("Stopping Matrix bot...")
        await self.client.close()

    async def _on_message(self, room: MatrixRoom, event: RoomMessageText) -> None:
        """Handle incoming text messages."""
        # Ignore our own messages
        if event.sender == self.user_id:
            return

        # Ignore old messages (from before we started)
        if event.server_timestamp < self.startup_time:
            return

        message = event.body
        sender = event.sender
        room_id = room.room_id

        # Check if this is a DM (room with only 2 members)
        is_dm = len(room.users) <= 2

        # Check if bot is mentioned (for non-DM rooms)
        bot_localpart = self.user_id.split(":")[0]  # @eis -> @eis
        is_mentioned = bot_localpart in message or self.user_id in message

        # Only respond if DM or mentioned
        if not is_dm and not is_mentioned:
            return

        # Remove mention from message if present
        if is_mentioned and not is_dm:
            message = message.replace(self.user_id, "").replace(bot_localpart, "").strip()

        logger.info(f"Message from {sender} in {room_id} (DM={is_dm}): {message[:50]}...")

        # Handle the message
        result = handle_matrix_message(
            message=message,
            user_id=sender,
            room_id=room_id,
            is_dm=is_dm,
        )

        # Send response
        response = result.get("response")
        if response:
            if is_dm:
                # Respond in DM directly
                await self._send_message(room_id, response)
            else:
                # For room mentions, DM the user (privacy model)
                dm_room_id = await self._get_or_create_dm(sender)
                if dm_room_id:
                    await self._send_message(dm_room_id, response)
                    # React in original room to acknowledge
                    await self._send_reaction(room_id, event.event_id, "✅")
                else:
                    # Fallback: respond in room if can't create DM
                    await self._send_message(room_id, response)

    async def _on_invite(self, room: MatrixRoom, event: InviteMemberEvent) -> None:
        """Handle room invites - auto-join."""
        if event.state_key != self.user_id:
            return

        if event.membership == "invite":
            logger.info(f"Invited to room {room.room_id}, joining...")
            await self.client.join(room.room_id)
            logger.info(f"Joined room {room.room_id}")

    async def _send_message(self, room_id: str, message: str) -> Optional[str]:
        """Send a text message to a room.

        Returns:
            Event ID of sent message, or None on failure
        """
        try:
            response = await self.client.room_send(
                room_id=room_id,
                message_type="m.room.message",
                content={
                    "msgtype": "m.text",
                    "body": message,
                    # Add formatted body for markdown
                    "format": "org.matrix.custom.html",
                    "formatted_body": self._markdown_to_html(message),
                },
            )
            return response.event_id if hasattr(response, "event_id") else None
        except Exception as e:
            logger.error(f"Failed to send message to {room_id}: {e}")
            return None

    async def _send_reaction(self, room_id: str, event_id: str, reaction: str) -> None:
        """Send a reaction to a message."""
        try:
            await self.client.room_send(
                room_id=room_id,
                message_type="m.reaction",
                content={
                    "m.relates_to": {
                        "rel_type": "m.annotation",
                        "event_id": event_id,
                        "key": reaction,
                    }
                },
            )
        except Exception as e:
            logger.error(f"Failed to send reaction: {e}")

    async def _is_dm_room(self, room_id: str) -> bool:
        """Check if a room is a DM (2 users) or a public room (3+ users).

        Returns:
            True if DM, False if public room
        """
        # Quick check: If it's the welcome room, it's NOT a DM
        if room_id == self.welcome_room_id:
            print(f"[DM_CHECK] Room {room_id} is welcome room, NOT a DM", flush=True)
            return False

        # Check if room is in our client's room list
        if room_id in self.client.rooms:
            room = self.client.rooms[room_id]
            user_count = len(room.users)
            print(f"[DM_CHECK] Room {room_id} has {user_count} users", flush=True)
            # DM = exactly 2 users (bot + one other user)
            is_dm = user_count == 2
            print(f"[DM_CHECK] Returning is_dm={is_dm}", flush=True)
            return is_dm

        # If room not in cache, assume it's a DM (safe default)
        print(f"[DM_CHECK] Room {room_id} not in cache, assuming DM", flush=True)
        return True

    async def _get_or_create_dm(self, user_id: str) -> Optional[str]:
        """Get or create a DM room with a user.

        Returns:
            Room ID of the DM room, or None on failure
        """
        # Check cache
        if user_id in self.dm_rooms:
            return self.dm_rooms[user_id]

        # Search for existing DM room
        for room_id, room in self.client.rooms.items():
            if len(room.users) == 2 and user_id in [u.user_id for u in room.users.values()]:
                self.dm_rooms[user_id] = room_id
                return room_id

        # Create new DM room with E2EE enabled
        try:
            response = await self.client.room_create(
                preset=RoomPreset.trusted_private_chat,  # Private DM, auto-visible
                is_direct=True,
                invite=[user_id],
                name=None,  # DMs don't need names
                initial_state=[
                    {
                        "type": "m.room.encryption",
                        "state_key": "",
                        "content": {
                            "algorithm": "m.megolm.v1.aes-sha2"
                        }
                    }
                ],
            )
            if hasattr(response, "room_id"):
                self.dm_rooms[user_id] = response.room_id
                logger.info(f"Created encrypted DM room with {user_id}: {response.room_id}")
                return response.room_id
        except Exception as e:
            logger.error(f"Failed to create DM room with {user_id}: {e}")

        return None

    def _markdown_to_html(self, text: str) -> str:
        """Convert markdown to HTML for Matrix formatted messages."""
        import re

        # Basic markdown to HTML conversion
        html = text

        # Escape HTML entities FIRST (before any markdown processing)
        # This prevents <title> from being interpreted as an HTML tag
        html = html.replace("&", "&amp;")  # Must be first
        html = html.replace("<", "&lt;")
        html = html.replace(">", "&gt;")

        # Bold: **text** -> <strong>text</strong>
        html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html)

        # Italic: *text* -> <em>text</em> (but not inside bold)
        html = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", html)

        # Italic with underscores: _text_ -> <em>text</em>
        # Match _text_ but not inside words (e.g., snake_case)
        html = re.sub(r"(?<![a-zA-Z0-9])_([^_]+)_(?![a-zA-Z0-9])", r"<em>\1</em>", html)

        # Code: `text` -> <code>text</code>
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

        # Links: [text](url) -> <a href="url">text</a>
        html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', html)

        # Line breaks
        html = html.replace("\n", "<br>")

        return html


def get_matrix_bot_instance() -> Optional[MatrixBot]:
    """Get the global Matrix bot instance.

    Returns:
        MatrixBot instance if bot is running, None otherwise
    """
    return _matrix_bot_instance


def create_matrix_bot() -> Optional[MatrixBot]:
    """Create Matrix bot from environment variables.

    Returns:
        MatrixBot instance, or None if required env vars are missing

    Supported env var names (for compatibility):
        - MATRIX_HOMESERVER or MATRIX_HOMESERVER_URL
        - MATRIX_USER or MATRIX_USER_ID
        - MATRIX_PASSWORD or MATRIX_ACCESS_TOKEN (one required)
        - MATRIX_DEVICE_ID (optional)
        - MATRIX_ADMIN_IDS or ADMIN_MATRIX_IDS (optional)
        - MATRIX_WELCOME_ROOM_ID (optional, for auto-DM on new user join)
    """
    # Support both naming conventions
    homeserver = os.environ.get("MATRIX_HOMESERVER") or os.environ.get("MATRIX_HOMESERVER_URL")
    user_id = os.environ.get("MATRIX_USER") or os.environ.get("MATRIX_USER_ID")
    password = os.environ.get("MATRIX_PASSWORD")
    access_token = os.environ.get("MATRIX_ACCESS_TOKEN")

    # Need either password or access token
    if not all([homeserver, user_id]) or not (password or access_token):
        missing = []
        if not homeserver:
            missing.append("MATRIX_HOMESERVER")
        if not user_id:
            missing.append("MATRIX_USER")
        if not password and not access_token:
            missing.append("MATRIX_PASSWORD or MATRIX_ACCESS_TOKEN")
        logger.warning(f"Matrix bot not configured - missing: {', '.join(missing)}")
        return None

    device_id = os.environ.get("MATRIX_DEVICE_ID", "vikunja_bot")
    admin_ids_str = os.environ.get("MATRIX_ADMIN_IDS") or os.environ.get("ADMIN_MATRIX_IDS", "")
    admin_ids = [x.strip() for x in admin_ids_str.split(",") if x.strip()]
    welcome_room_id = os.environ.get("MATRIX_WELCOME_ROOM_ID")

    # Debug: print to stdout to bypass logger issues
    print(f"[MATRIX] MATRIX_WELCOME_ROOM_ID env var: {welcome_room_id!r}")

    if welcome_room_id:
        logger.info(f"Welcome room configured: {welcome_room_id}")
        print(f"[MATRIX] Welcome room configured: {welcome_room_id}")

    return MatrixBot(
        homeserver=homeserver,
        user_id=user_id,
        password=password,
        access_token=access_token,
        device_id=device_id,
        admin_ids=admin_ids,
        welcome_room_id=welcome_room_id,
    )


async def run_matrix_bot() -> None:
    """Run the Matrix bot (blocking)."""
    bot = create_matrix_bot()
    if not bot:
        logger.error("Cannot start Matrix bot - not configured")
        return

    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Interrupted, shutting down...")
    finally:
        await bot.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_matrix_bot())
