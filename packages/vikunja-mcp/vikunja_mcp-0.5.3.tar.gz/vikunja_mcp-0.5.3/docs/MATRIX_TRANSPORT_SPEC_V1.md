# Matrix Transport Layer Specification

## Overview

Add Matrix as a third transport layer alongside Slack and MCP. The Matrix bot connects as `@eis:matrix.factumerit.app` and provides identical Vikunja capabilities as the Slack bot.

## Architecture

```
                         ┌─────────────────────────────────┐
                         │       Shared Core               │
                         │                                 │
                         │  - TOOL_REGISTRY (58 tools)     │
                         │  - Claude API integration       │
                         │  - User config (YAML)           │
                         │  - Usage/credit tracking        │
                         │  - Multi-instance Vikunja       │
                         └───────────────┬─────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│ Slack Transport │             │  MCP Transport  │             │ Matrix Transport│
│                 │             │                 │             │     (NEW)       │
│ - slack_bolt    │             │ - FastMCP       │             │ - matrix-nio    │
│ - Events API    │             │ - HTTP/SSE      │             │ - Sync loop     │
│ - Slash cmds    │             │ - OAuth 2.0     │             │ - !commands     │
│ - Ephemeral     │             │                 │             │ - DM privacy    │
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

## Environment Variables

```bash
# Required for Matrix bot
MATRIX_HOMESERVER_URL=https://matrix.factumerit.app
MATRIX_USER_ID=@eis:matrix.factumerit.app
MATRIX_PASSWORD=<bot_password>

# Optional
MATRIX_DEVICE_ID=vikunja_bot_001      # Session persistence
MATRIX_ALLOWED_ROOMS=                  # Comma-separated room IDs (empty = all)
MATRIX_ADMIN_IDS=@i2:matrix.factumerit.app  # Admin users (like ADMIN_SLACK_IDS)
```

---

## Feature Mapping: Slack → Matrix

### 1. Message Handling

| Slack | Matrix | Notes |
|-------|--------|-------|
| `@bot message` (channel) | `@eis message` (room) | Privacy: respond in DM |
| DM to bot | DM to @eis | Direct response in DM |
| Ephemeral response | DM + reaction in channel | Matrix has no ephemeral |
| "Share to channel" button | User copy/pastes from DM | No interactive buttons |
| Typing indicator | Typing indicator | `m.typing` event |
| Thinking message | Typing indicator | No deletable messages |

#### Privacy Model (Channel Mentions)
```
Room #general:
  Alice: @eis list my tasks
  [eis reacts with ✅]

DM to Alice:
  eis: 📋 Your tasks:
       - Task 1 (due today)
       - Task 2 (overdue)
```

### 2. Slash Commands → !Commands

Matrix has no native slash commands. Use `!command` prefix:

#### Task Filters (No LLM cost - direct API)
| Slack | Matrix | Behavior |
|-------|--------|----------|
| `/overdue` | `!overdue` | Tasks past due |
| `/today` | `!today` | Due today + overdue |
| `/week` | `!week` | Due this week |
| `/priority` | `!priority` | Priority 3+ |
| `/urgent` | `!urgent` | Priority 5 |
| `/unscheduled` | `!unscheduled` | No due date |
| `/focus` | `!focus` | Today's focus |
| `/summary` | `!summary` | Task counts |

**ECO Mode**: These commands increment ECO streak (no LLM cost).

#### Multi-Instance Management
| Slack | Matrix | Behavior |
|-------|--------|----------|
| `/connections` | `!connections` | List Vikunja instances |
| `/connect` | `!connect` | Generate auth URL for Vikunja linking |
| `/disconnect` | `!disconnect` | Unlink Vikunja account |

#### Project Context
| Slack | Matrix | Behavior |
|-------|--------|----------|
| `/project <name>` | `!project <name>` | Set active project |
| `/project` | `!project` | Show current |
| `/clear` | `!clear` | Clear context |

#### User Settings
| Slack | Matrix | Behavior |
|-------|--------|----------|
| `/usage` | `!usage` | Token usage stats |
| `/credits` | `!credits` | Admin: credit management |
| `/help` | `!help` | Command reference |

### 3. User Preferences (via Claude tools)

These work identically - Claude calls the tool, settings stored in config.yaml:

| Tool | Function |
|------|----------|
| `set_user_timezone` | Store timezone preference |
| `toggle_token_usage` | Show/hide usage footer |
| `set_model` | Choose haiku/sonnet/opus |
| `set_memory` | Conversation memory settings |
| `reset_conversation` | Clear memory |

### 4. Conversation Memory

**Slack**: Fetches channel history via `conversations.history` API
**Matrix**: Fetch room history via `/messages` endpoint

Same logic applies:
- `strategy: none` → No memory
- `strategy: rolling` → Last N message pairs
- Window: 1-50 (default 10)
- Ensures alternating user/assistant roles

### 5. Admin Functionality

| Feature | Slack | Matrix |
|---------|-------|--------|
| Admin check | `ADMIN_SLACK_IDS` env var | `MATRIX_ADMIN_IDS` env var |
| Admin tools | `admin_set_user_token`, `admin_list_users`, `admin_connect_instance` | Same tools, check Matrix ID |
| `/credits` command | Admin only | `!credits` admin only |

### 6. User Authentication Flow

**Slack OAuth flow**:
1. User: `/connect`
2. Bot: Creates pending connection (nonce), returns auth URL
3. User: Clicks URL, authenticates with Vikunja
4. Vikunja: Redirects to `/vikunja-callback` with token
5. Bot: Stores token, DMs user confirmation

**Matrix equivalent**:
1. User: `!connect`
2. Bot: Creates pending connection (Matrix user ID), returns auth URL
3. User: Clicks URL, authenticates with Vikunja
4. Vikunja: Redirects to `/vikunja-callback` with token
5. Bot: Stores token, DMs user confirmation

Key change: Use Matrix user ID instead of Slack user ID for pending connection lookup.

### 7. Welcome Messages

**Slack**: `team_join` event → DM new user with connect prompt
**Matrix**: Room invite accepted → DM user with connect prompt (optional)

### 8. Usage Tracking & Limits

Identical system, keyed by user ID:

```yaml
users:
  "@alice:matrix.factumerit.app":
    vikunja_token: "tk_xxx"
    timezone: "America/New_York"
    model: "haiku"
    memory:
      strategy: "rolling"
      window: 10
    lifetime_usage: 0.42
    lifetime_budget: 1.00
    daily_usage: ...
```

### 9. ECO Streak

- In-memory tracking (resets on restart)
- Incremented by `!commands` (no LLM cost)
- Reset when LLM is used
- Display in command footer: `🌿 ECO streak: 5 | ~2,500 tokens saved`

### 10. Thinking Indicators

**Slack**:
- Channel: Ephemeral "Cogito..." message
- DM: Posted message, deleted when done

**Matrix**:
- Typing indicator (native Matrix feature)
- No "thinking" message needed

---

## Components to Implement

### 1. MatrixClient Class

```python
class MatrixClient:
    """Matrix bot using matrix-nio AsyncClient."""

    def __init__(self, homeserver: str, user_id: str, password: str):
        self.client: AsyncClient
        self.homeserver = homeserver
        self.user_id = user_id
        self.password = password
        self.dm_rooms: dict[str, str] = {}  # user_id -> room_id cache

    async def start(self) -> None:
        """Login, sync, register callbacks."""

    async def stop(self) -> None:
        """Graceful shutdown."""

    async def send_message(self, room_id: str, message: str,
                           reply_to: str = None) -> None:
        """Send message, optionally as reply."""

    async def send_reaction(self, room_id: str, event_id: str,
                            reaction: str = "✅") -> None:
        """React to a message."""

    async def send_typing(self, room_id: str, timeout: int = 30000) -> None:
        """Send typing indicator."""

    async def get_or_create_dm(self, user_id: str) -> str:
        """Get DM room with user, create if needed."""

    async def fetch_room_history(self, room_id: str, limit: int) -> list:
        """Fetch recent messages for conversation memory."""
```

### 2. Event Handlers

```python
async def on_room_message(room: MatrixRoom, event: RoomMessageText) -> None:
    """Handle room messages."""
    # Skip own messages
    if event.sender == client.user_id:
        return

    text = event.body
    sender = event.sender
    room_id = room.room_id
    is_dm = room.member_count == 2

    # Check for !command
    if text.startswith("!"):
        await handle_command(text, sender, room_id, is_dm, event.event_id)
        return

    # Check for mention
    if is_mentioned(text, client.user_id):
        clean_text = remove_mention(text)
        await handle_mention(clean_text, sender, room_id, event.event_id)
        return

    # DM: respond to any message
    if is_dm:
        await handle_dm(text, sender, room_id)

async def on_room_invite(room: MatrixRoom, event: InviteMemberEvent) -> None:
    """Auto-accept room invites."""
    if event.state_key == client.user_id:
        await client.join(room.room_id)
        logger.info(f"Joined room: {room.room_id}")
```

### 3. Command Handler

```python
async def handle_command(text: str, sender: str, room_id: str,
                         is_dm: bool, event_id: str) -> None:
    """Handle !commands (no LLM cost)."""
    parts = text[1:].lower().split()
    cmd = parts[0] if parts else ""
    args = parts[1:] if len(parts) > 1 else []

    # Increment ECO streak
    _increment_eco_streak(sender)

    handlers = {
        "overdue": lambda: _slash_command_multi_instance(sender, _overdue_tasks_impl, "Overdue"),
        "today": lambda: _slash_command_multi_instance(sender, _due_today_impl, "Due Today"),
        # ... etc
        "connections": lambda: _format_instances_for_matrix(sender),
        "connect": lambda: _get_connect_prompt_matrix(sender),
        "help": lambda: _format_help_for_matrix(),
    }

    if cmd in handlers:
        response = handlers[cmd]()
        await send_response(response, sender, room_id, is_dm, event_id)
    else:
        await send_response(f"Unknown command: !{cmd}. Try !help", sender, room_id, is_dm, event_id)
```

### 4. Message Router

```python
async def handle_mention(text: str, sender: str, room_id: str, event_id: str) -> None:
    """Handle @mentions in rooms (privacy: respond in DM)."""
    # React in channel to acknowledge
    await client.send_reaction(room_id, event_id, "✅")

    # Send typing in DM
    dm_room = await client.get_or_create_dm(sender)
    await client.send_typing(dm_room)

    # Get response from Claude
    response = _matrix_chat_with_claude(text, user_id=sender, room_id=dm_room)

    # Send to DM
    await client.send_message(dm_room, response)

async def handle_dm(text: str, sender: str, room_id: str) -> None:
    """Handle DMs (full response in same room)."""
    await client.send_typing(room_id)
    response = _matrix_chat_with_claude(text, user_id=sender, room_id=room_id)
    await client.send_message(room_id, response)
```

### 5. Claude Integration

```python
def _matrix_chat_with_claude(user_message: str, user_id: str, room_id: str) -> str:
    """Send message to Claude with Matrix context.

    Mirrors _slack_chat_with_claude() with Matrix-specific changes:
    - Uses Matrix user ID for config/token lookup
    - Uses Matrix room history for conversation memory
    - Returns markdown (no Slack mrkdwn conversion)
    """
    # Check Vikunja token
    user_vikunja_token = _get_user_vikunja_token(user_id)
    if not user_vikunja_token and not _is_matrix_admin(user_id):
        return _get_connect_prompt_matrix(user_id)

    # Set context var for this request
    if user_vikunja_token:
        _current_vikunja_token.set(user_vikunja_token)

    # Check usage limits
    limit_check = _check_usage_limits(user_id)
    if not limit_check["allowed"]:
        return limit_check["warning"]

    # Build conversation history (from Matrix room)
    messages = _build_matrix_conversation_history(room_id, user_id, user_message)

    # Call Claude (same as Slack)
    # ... tool loop ...

    # Return markdown (no conversion needed)
    return response_text
```

### 6. Response Formatting

```python
def _md_to_matrix(text: str) -> str:
    """Ensure response is Matrix-compatible markdown.

    Matrix natively supports:
    - **bold**, *italic*
    - `code`, ```code blocks```
    - [links](url)
    - Lists, headers

    Minimal conversion needed (unlike Slack).
    """
    # Remove any Slack-specific formatting that might leak
    text = text.replace("<@", "@").replace(">", "")
    return text
```

---

## Integration Points

### Shared Code (No Changes)
- `TOOL_REGISTRY` - All 58 Vikunja tools
- `_request()` - Vikunja API calls
- `_load_config()` / `_save_config()` - User preferences
- `_get_user_*` / `_set_user_*` - Preference accessors
- `_check_usage_limits()` - Credit system
- `_update_lifetime_usage()` - Usage tracking
- `_increment_eco_streak()` - ECO mode
- Multi-instance Vikunja support

### Refactored Code
- Extract `_base_chat_with_claude()` from `_slack_chat_with_claude()`
- Add `_matrix_chat_with_claude()` wrapper
- Add `_build_matrix_conversation_history()` (parallel to Slack version)
- Add `_is_matrix_admin()` function

### New Code
- `matrix_transport.py` - MatrixClient, event handlers
- Matrix-specific formatters
- Matrix room history fetching

---

## File Structure

```
src/vikunja_mcp/
├── server.py              # Main server (add Matrix init to main())
├── matrix_transport.py    # NEW: Matrix client and handlers
└── __init__.py
```

---

## Startup Sequence

```python
# In server.py main()
async def main():
    # Existing: Start MCP server
    # Existing: Initialize Slack if configured

    # NEW: Initialize Matrix if configured
    matrix_client = None
    if os.environ.get("MATRIX_HOMESERVER_URL"):
        from .matrix_transport import MatrixClient
        matrix_client = MatrixClient(
            homeserver=os.environ["MATRIX_HOMESERVER_URL"],
            user_id=os.environ["MATRIX_USER_ID"],
            password=os.environ["MATRIX_PASSWORD"]
        )
        await matrix_client.start()

    # Run server
    try:
        await run_server()
    finally:
        if matrix_client:
            await matrix_client.stop()
```

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Network disconnect | Retry with exponential backoff |
| Auth failure | Log error, don't crash server |
| Message send fails | Log, continue |
| Invalid room | Ignore (user left) |
| Malformed event | Log, skip |
| Tool execution error | Return error message to user |

---

## Testing Strategy

### Unit Tests
- Command parsing (`!overdue` → handler)
- Mention detection
- Response formatting

### Integration Tests (against real Matrix)
- Connect as @eis
- Send test message, verify response
- Test room invite handling
- Test DM flow
- Test !commands

### Manual Testing Checklist
- [ ] Bot logs in
- [ ] Bot accepts room invite
- [ ] Bot responds to @mention (DM + reaction)
- [ ] Bot responds to DM
- [ ] !overdue returns tasks
- [ ] !connect returns auth URL
- [ ] Memory persists across messages
- [ ] Reconnects after disconnect

---

## Success Criteria

- [ ] Bot connects as @eis:matrix.factumerit.app
- [ ] Responds to mentions in rooms (via DM)
- [ ] Responds to direct messages
- [ ] All 16 !commands work
- [ ] Vikunja tools work (list tasks, create, etc.)
- [ ] Multi-instance support works
- [ ] User preferences persist
- [ ] Usage tracking works
- [ ] Reconnects automatically
- [ ] No crashes on errors

---

## Implementation Order

1. **solutions-3k2u**: Add matrix-nio dependency, env vars
2. **solutions-baft**: MatrixClient class, login, sync loop
3. **solutions-6c21**: Message handler, !command parser, Claude routing
4. **solutions-jgy3**: Response sender, DM privacy flow, formatting
5. **solutions-ury0**: Room management (invites, DM creation)
