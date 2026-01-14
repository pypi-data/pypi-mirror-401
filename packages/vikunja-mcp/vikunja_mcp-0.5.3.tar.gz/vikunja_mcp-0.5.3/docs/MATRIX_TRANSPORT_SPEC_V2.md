# Matrix Transport Layer Specification V2

**Version**: 2.0
**Date**: 2025-12-24
**Changes from V1**:
- Added Matrix-specific features (room binding, reactions, HTML formatting, threading)
- **PLAYFUL COMMAND NAMES** (!oops, !now, !fire, !zen, !vik, !viki, !vikui, !vikuii, !viktus)
- Vikui knowledge base system (RAG)
- ECO streak gamification
- User-defined command aliases

---

## Overview

Add Matrix as a third transport layer alongside Slack and MCP. The Matrix bot connects as `@eis:matrix.factumerit.app` and provides identical Vikunja capabilities as the Slack bot, **plus Matrix-native enhancements** that leverage the platform's unique features.

### The Magic Formula

```
PROJECT (Vikunja)     = STATE (tasks, deadlines, status)
+
VIKUI (RAG)           = CONTENT (docs, notes, knowledge)
+
CLAUDE (LLM)          = INTELLIGENCE (reasoning, actions)
=
🎯 CONTEXT-AWARE AI WORKSPACE
```

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
│                 │             │                 │             │ - Room binding  │
│                 │             │                 │             │ - Reactions     │
│                 │             │                 │             │ - HTML format   │
│                 │             │                 │             │ - Threads       │
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
MATRIX_ENABLE_E2EE=false               # Enable E2EE support (requires device verification)
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
| Thinking message | Editable "🤔 Thinking..." | Matrix supports message edits |

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

#### Task Filters (No LLM cost - direct API) - PLAYFUL NAMES! 🎉
| Slack | Matrix (Playful) | Behavior | Why It's Fun |
|-------|------------------|----------|--------------|
| `/overdue` | `!oops` | Tasks past due | "Oops, I missed these!" |
| `/today` | `!now` | Due today + overdue | "What's happening NOW?" |
| `/week` | `!week` | Due this week | (kept simple) |
| `/priority` | `!vip` | Priority 3+ | "VIP tasks!" |
| `/urgent` | `!fire` | Priority 5 | 🔥 Fire drill! |
| `/unscheduled` | `!maybe` | No due date | "Someday/maybe" (GTD) |
| `/focus` | `!zen` | Today's focus | 🧘 Zen mode |
| `/summary` | `!stats` | Task counts | 📊 Show me the stats |

**ECO Mode**: These commands increment ECO streak (no LLM cost). Build your streak! 🌿

**Backward Compatibility**: Old names (`!overdue`, `!today`, etc.) still work as aliases.

#### Multi-Instance Management - PLAYFUL NAMES! 🎉
| Slack | Matrix (Playful) | Behavior | Why It's Fun |
|-------|------------------|----------|--------------|
| `/connections` | `!viki` | List Vikunja instances | Plural of "vik" |
| `/connect` | `!vik` | Connect to Vikunja | Short for "Vikunja" |
| `/disconnect` | `!novik` | Disconnect from Vikunja | "No more vik" |

#### Project Context
| Slack | Matrix | Behavior |
|-------|--------|----------|
| `/project <name>` | `!project <name>` | Set active project |
| `/project` | `!project` | Show current |
| `/clear` | `!clear` | Clear context |

#### Knowledge Base (NEW!) - The Vik Family
| Command | Behavior |
|---------|----------|
| `!vikui <name>` | Bind room to knowledge base (room admins) |
| `!vikui` | Show current binding |
| `!novikui` | Remove binding |
| `!vikuii` | List available knowledge bases |
| `!viktus` | Show all connection status (Vikunja + vikui + context) |

See **VIKUI_SPEC.md** for full details on the knowledge base system.

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
**Matrix**: ~~Room invite accepted~~ **Only on first DM** → Send connect prompt

**Rationale**: Matrix users join many rooms. Only welcome them when they initiate contact.

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
    room_bindings:  # NEW: Matrix-specific
      "!abc123:matrix.factumerit.app": "Client XYZ"
      "!def456:matrix.factumerit.app": "Internal Ops"
```

### 9. ECO Streak (Gamification!)

**Concept**: Reward users for using efficient `!commands` instead of LLM queries.

**Tracking**:
- In-memory tracking (resets on restart)
- Incremented by `!commands` (no LLM cost)
- Reset when LLM is used
- Display in command footer: `🌿 ECO streak: 5 | ~2,500 tokens saved`

**Milestones** (celebratory messages):
- 🌱 Streak 5: "You're getting the hang of this!"
- 🌿 Streak 10: "ECO warrior!"
- 🌳 Streak 25: "Token-saving champion!"
- 🏆 Streak 50: "ECO legend! You've saved ~25,000 tokens!"

**Implementation**:
```python
# In-memory storage
eco_streaks = {}  # {user_id: streak_count}

def _increment_eco_streak(user_id: str) -> int:
    """Increment ECO streak and return new count."""
    eco_streaks[user_id] = eco_streaks.get(user_id, 0) + 1
    streak = eco_streaks[user_id]

    # Check for milestones
    if streak == 5:
        return streak, "🌱 You're getting the hang of this!"
    elif streak == 10:
        return streak, "🌿 ECO warrior!"
    elif streak == 25:
        return streak, "🌳 Token-saving champion!"
    elif streak == 50:
        return streak, "🏆 ECO legend! You've saved ~25,000 tokens!"

    return streak, None

def _reset_eco_streak(user_id: str):
    """Reset ECO streak when LLM is used."""
    eco_streaks[user_id] = 0

def _get_eco_streak(user_id: str) -> int:
    """Get current ECO streak."""
    return eco_streaks.get(user_id, 0)
```

**Footer Format**:
```python
def format_command_response(result: dict, user_id: str) -> str:
    """Format command result with ECO streak footer."""
    response = result.get("message", "")

    streak, milestone = _increment_eco_streak(user_id)
    tokens_saved = streak * 500  # Estimate

    # Add ECO footer
    if streak > 0:
        response += f"\n\n🌿 ECO streak: {streak} | ~{tokens_saved:,} tokens saved"

        # Add milestone celebration
        if milestone:
            response += f"\n\n🎉 **{milestone}**"

    return response
```

### 10. Thinking Indicators

**Slack**:
- Channel: Ephemeral "Cogito..." message
- DM: Posted message, deleted when done

**Matrix**:
- Send "🤔 Thinking..." message
- Edit to final response when done (Matrix supports message edits)
- Typing indicator for <30s operations only (they timeout)

---

## Matrix-Specific Features (NEW in V2)

### 1. Room-Project Binding (Model 1 - Personal Context)

**Problem**: Slack users manually `/project` switch. Matrix rooms are persistent workspaces.

**Solution**: Each user can bind a room to their own Vikunja project for automatic context.

**Model**: Personal room bindings (Model 1)
- Each user has their own room→project mappings
- Privacy preserved (Alice's binding ≠ Bob's binding)
- Matches current Slack behavior (personal context)
- **Future**: Model 2 (shared room bindings) planned - see `MATRIX_ROOM_BINDING_MODEL2.md`

| Command | Behavior |
|---------|----------|
| `!bind <project>` | Link current room to project (fuzzy search, personal binding) |
| `!bind <project> N` | Link to Nth match if multiple results |
| `!unbind` | Remove personal room binding |
| `!binding` | Show current personal binding |

**Implementation**:
```python
# Store in config.yaml under user (personal binding)
users:
  "@alice:matrix.factumerit.app":
    room_bindings:
      "!abc123:matrix.factumerit.app": "Client XYZ"
      "!def456:matrix.factumerit.app": "Internal Ops"

  "@bob:matrix.factumerit.app":
    room_bindings:
      "!abc123:matrix.factumerit.app": "Different Project"  # Same room, different binding!

# Auto-inject project context for all commands in bound rooms
def get_room_project(room_id: str, user_id: str) -> Optional[str]:
    """Get user's personal room binding."""
    config = _load_config()
    return config.get("users", {}).get(user_id, {}).get("room_bindings", {}).get(room_id)
```

**User Experience**:
```
Room #client-xyz:
  Alice: !bind Client XYZ
  eis: [DMs Alice] ✅ Room bound to "Client XYZ" project (personal binding)

  Alice: !today
  eis: [DMs Alice] 📋 Due Today (Client XYZ):
       - Task 1
       - Task 2

  Bob: !today
  eis: [DMs Bob] 📋 Due Today (no project set):
       - Task 3
       - Task 4

  # Alice and Bob see different projects - privacy preserved!
```

**Benefits**:
- No manual project switching
- Room = workspace = project (natural mapping)
- Works with all commands and Claude interactions
- Privacy preserved (each user has own bindings)
- Simple (no permission model, no conflicts)

### 2. Reaction Quick Actions

**Problem**: Mobile users don't want to type commands.

**Solution**: React to bot messages with emoji to trigger actions.

| Reaction | Action | Applies To |
|----------|--------|------------|
| ✅ | Complete task | Task messages |
| 📌 | Set priority to 5 | Task messages |
| 🗑️ | Delete task | Task messages |
| ⏰ | Set due date to today | Task messages |
| 🔄 | Refresh/re-run command | Any bot message |

**Implementation**:
```python
@client.on_event(ReactionEvent)
async def handle_reaction(room: MatrixRoom, event: ReactionEvent):
    """Handle reactions to bot messages."""
    # Only process reactions to our own messages
    if not is_bot_message(event.relates_to):
        return

    # Extract task ID from original message
    task_id = extract_task_id(event.relates_to)
    if not task_id:
        return

    user_id = event.sender

    if event.key == "✅":
        result = _update_task_impl(task_id, done=True)
        await client.send_message(room.room_id, f"✅ Completed: {result['title']}")
    elif event.key == "📌":
        result = _update_task_impl(task_id, priority=5)
        await client.send_message(room.room_id, f"📌 Prioritized: {result['title']}")
    elif event.key == "🗑️":
        result = _delete_task_impl(task_id)
        await client.send_message(room.room_id, f"🗑️ Deleted: {result['title']}")
    elif event.key == "⏰":
        today = datetime.now().strftime("%Y-%m-%d")
        result = _update_task_impl(task_id, due_date=today)
        await client.send_message(room.room_id, f"⏰ Due today: {result['title']}")
```

**Message Format** (to enable reactions):
```
📋 Your tasks:

1. [#123] Review contract (due today) 🔴
2. [#456] Update docs (due Friday) 🟡

React: ✅ complete | 📌 prioritize | 🗑️ delete | ⏰ due today
```

**Benefits**:
- Mobile-friendly (no typing)
- Natural Matrix UX (reactions are common)
- Works in both rooms and DMs

### 3. HTML Formatting

**Problem**: Plain markdown lacks visual hierarchy for task lists.

**Solution**: Use Matrix's HTML support for color-coded, rich formatting.

**Implementation**:
```python
def format_task_list_html(tasks: list) -> tuple[str, str]:
    """Return (markdown, html) tuple for Matrix formatted message."""

    # Markdown fallback
    md_lines = ["📋 Your tasks:\n"]

    # HTML with color coding
    html_lines = ["<h4>📋 Your tasks:</h4><ul>"]

    for task in tasks:
        task_id = task["id"]
        title = task["title"]
        due = task.get("due_date")
        priority = task.get("priority", 0)
        done = task.get("done", False)

        # Determine color
        if done:
            color = "#00ff00"  # Green
            icon = "✓"
        elif is_overdue(due):
            color = "#ff0000"  # Red
            icon = "🔴"
        elif is_due_today(due):
            color = "#ffaa00"  # Yellow
            icon = "🟡"
        elif priority >= 4:
            color = "#ff6600"  # Orange
            icon = "📌"
        else:
            color = "#ffffff"  # White
            icon = "⚪"

        # Markdown
        md_lines.append(f"{icon} [{task_id}] {title}")

        # HTML
        html_lines.append(
            f'<li><strong>[#{task_id}]</strong> '
            f'<span data-mx-color="{color}">{icon} {title}</span>'
        )
        if due:
            html_lines.append(f' <em>(due {due})</em>')
        html_lines.append('</li>')

    html_lines.append("</ul>")

    return "\n".join(md_lines), "".join(html_lines)

# Send with both formats
md, html = format_task_list_html(tasks)
await client.send_message(room_id, body=md, formatted_body=html, format="org.matrix.custom.html")
```

**Visual Result** (in Element Web):
```
📋 Your tasks:

• [#123] 🔴 Review contract (due yesterday)
• [#456] 🟡 Update docs (due today)
• [#789] 📌 Call client (priority 5)
• [#101] ⚪ Research options (due next week)
```

**Benefits**:
- Better visual hierarchy
- Color-coded urgency (red = overdue, yellow = today)
- Works in Element Web/Desktop (most common clients)
- Graceful fallback to markdown for other clients

### 4. Thread Support

**Problem**: Task discussions clutter the main room.

**Solution**: Use Matrix threads for task-specific conversations.

**Implementation**:
```python
async def create_task_with_thread(room_id: str, task: dict):
    """Create task and start a thread for discussion."""

    # Send task creation message
    task_msg = f"✅ Created task: {task['title']} (#{task['id']})"
    event_id = await client.send_message(room_id, task_msg)

    # Start thread
    thread_msg = (
        f"💬 Discuss task #{task['id']} here\n\n"
        f"Use this thread for:\n"
        f"• Questions about the task\n"
        f"• Progress updates\n"
        f"• Related links/files\n\n"
        f"React to the parent message to take quick actions (✅ complete, 📌 prioritize)"
    )
    await client.send_message(
        room_id,
        thread_msg,
        reply_to=event_id,
        thread=True
    )
```

**User Experience**:
```
Room #client-xyz:
  Alice: @eis create task: Review contract
  eis: ✅ Created task: Review contract (#123)
    └─ 💬 Discuss task #123 here
       └─ Alice: I need the latest version
       └─ Bob: Sent via email
       └─ Alice: Thanks!
```

**Benefits**:
- Organized task discussions
- Doesn't clutter main room
- Native Matrix feature (works in Element)

**Scope for V1**: Optional - only enable if user requests it via `!thread <task_id>`

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
        self.thinking_messages: dict[str, str] = {}  # room_id -> event_id

    async def start(self) -> None:
        """Login, sync, register callbacks."""

    async def stop(self) -> None:
        """Graceful shutdown."""

    async def send_message(self, room_id: str, message: str,
                           reply_to: str = None, html: str = None) -> str:
        """Send message, optionally as reply with HTML formatting.

        Returns event_id for later editing/reactions.
        """

    async def edit_message(self, room_id: str, event_id: str, new_text: str) -> None:
        """Edit a previously sent message."""

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
@client.on_event(RoomMessageText)
async def handle_message(room: MatrixRoom, event: RoomMessageText):
    """Handle incoming text messages."""

    # Ignore own messages
    if event.sender == client.user_id:
        return

    # Ignore old messages (from backfill)
    if event.server_timestamp < startup_time:
        return

    message = event.body
    user_id = event.sender
    room_id = room.room_id

    # Check if bot is mentioned or DM
    is_dm = len(room.users) == 2
    is_mentioned = f"@{client.user_id.split(':')[0]}" in message or client.user_id in message

    if not (is_dm or is_mentioned):
        return

    # Route to command handler or Claude
    await route_message(room_id, user_id, message, is_dm)


@client.on_event(ReactionEvent)
async def handle_reaction(room: MatrixRoom, event: ReactionEvent):
    """Handle reactions to bot messages (quick actions)."""

    # Only process reactions to our own messages
    if not is_bot_message(event.relates_to):
        return

    # Extract task ID and execute action
    await handle_quick_action(room.room_id, event.sender, event.key, event.relates_to)


@client.on_event(InviteMemberEvent)
async def handle_invite(room: MatrixRoom, event: InviteMemberEvent):
    """Auto-join rooms when invited."""

    if event.membership == "invite" and event.state_key == client.user_id:
        await client.join(room.room_id)
        logger.info(f"Joined room {room.room_id}")
```

### 3. Command Handler

```python
async def route_message(room_id: str, user_id: str, message: str, is_dm: bool):
    """Route message to !command handler or Claude."""

    # Check for !command
    if message.strip().startswith("!"):
        await handle_command(room_id, user_id, message, is_dm)
        return

    # Otherwise, route to Claude
    await chat_with_claude(room_id, user_id, message, is_dm)


async def handle_command(room_id: str, user_id: str, message: str, is_dm: bool):
    """Handle !commands (no LLM cost)."""

    parts = message.strip().split(maxsplit=1)
    command = parts[0][1:]  # Remove !
    args = parts[1] if len(parts) > 1 else ""

    # Get room binding for auto-project context
    project = get_room_project(room_id, user_id)

    # Map commands to implementations
    handlers = {
        # Playful task filters (NEW!)
        "oops": lambda: _get_overdue_tasks_impl(project=project),
        "now": lambda: _get_today_tasks_impl(project=project),
        "week": lambda: _get_week_tasks_impl(project=project),
        "vip": lambda: _get_priority_tasks_impl(project=project),
        "fire": lambda: _get_urgent_tasks_impl(project=project),
        "maybe": lambda: _get_unscheduled_tasks_impl(project=project),
        "zen": lambda: _get_focus_tasks_impl(project=project),
        "stats": lambda: _get_summary_impl(project=project),

        # Backward compatibility (old names still work)
        "overdue": lambda: _get_overdue_tasks_impl(project=project),
        "today": lambda: _get_today_tasks_impl(project=project),
        "priority": lambda: _get_priority_tasks_impl(project=project),
        "urgent": lambda: _get_urgent_tasks_impl(project=project),
        "unscheduled": lambda: _get_unscheduled_tasks_impl(project=project),
        "focus": lambda: _get_focus_tasks_impl(project=project),
        "summary": lambda: _get_summary_impl(project=project),

        # Project context
        "project": lambda: _set_project_impl(args) if args else _get_project_impl(),
        "clear": lambda: _clear_project_impl(),
        "bind": lambda: _bind_room_impl(room_id, user_id, args),
        "unbind": lambda: _unbind_room_impl(room_id, user_id),
        "binding": lambda: _get_binding_impl(room_id, user_id),

        # Vikunja connection (playful names!)
        "vik": lambda: _generate_connect_url_impl(user_id),
        "novik": lambda: _disconnect_impl(user_id),
        "viki": lambda: _list_connections_impl(user_id),

        # Backward compatibility
        "connect": lambda: _generate_connect_url_impl(user_id),
        "disconnect": lambda: _disconnect_impl(user_id),
        "connections": lambda: _list_connections_impl(user_id),

        # Vikui (NEW!) - Knowledge base
        "vikui": lambda: _vikui_bind_impl(room_id, user_id, args) if args else _vikui_show_impl(room_id),
        "novikui": lambda: _vikui_unbind_impl(room_id, user_id),
        "vikuii": lambda: _vikuii_list_impl(user_id),

        # Viktus (NEW!) - Status dashboard
        "viktus": lambda: _viktus_impl(user_id, room_id),

        # User settings
        "usage": lambda: _get_usage_impl(user_id),
        "credits": lambda: _admin_credits_impl(user_id, args),
        "help": lambda: _get_help_impl(),
    }

    handler = handlers.get(command)
    if not handler:
        response = f"❌ Unknown command: !{command}\n\nType !help for available commands."
    else:
        try:
            # Increment ECO streak
            _increment_eco_streak(user_id)

            # Execute command
            result = handler()
            response = format_command_response(result, user_id)
        except Exception as e:
            logger.exception(f"Command error: {command}")
            response = f"❌ Error: {str(e)}"

    # Send response (DM if mentioned in room, direct if DM)
    if is_dm:
        await client.send_message(room_id, response)
    else:
        # React in room, respond in DM
        await client.send_reaction(room_id, event_id, "✅")
        dm_room = await client.get_or_create_dm(user_id)
        await client.send_message(dm_room, response)
```

### 4. Message Router & Claude Integration

```python
async def chat_with_claude(room_id: str, user_id: str, message: str, is_dm: bool):
    """Send message to Claude with tool access."""

    # Check authentication
    if not _is_user_connected(user_id):
        response = (
            "⚠️ You need to connect your Vikunja account first.\n\n"
            "Use !connect to get started."
        )
        if is_dm:
            await client.send_message(room_id, response)
        else:
            dm_room = await client.get_or_create_dm(user_id)
            await client.send_message(dm_room, response)
        return

    # Check usage limits
    if not _check_usage_limits(user_id):
        response = "❌ You've reached your usage limit. Contact admin for more credits."
        if is_dm:
            await client.send_message(room_id, response)
        else:
            dm_room = await client.get_or_create_dm(user_id)
            await client.send_message(dm_room, response)
        return

    # Get room binding for auto-project context
    project = get_room_project(room_id, user_id)

    # Build conversation history
    history = await _build_matrix_conversation_history(room_id, user_id)

    # Add project context to system prompt if bound
    system_prompt = SYSTEM_PROMPT
    if project:
        system_prompt += f"\n\nCurrent project context: {project}"

    # Send thinking indicator
    if is_dm:
        thinking_event = await client.send_message(room_id, "🤔 Thinking...")
        client.thinking_messages[room_id] = thinking_event
    else:
        await client.send_typing(room_id, timeout=30000)

    # Reset ECO streak (using LLM)
    _reset_eco_streak(user_id)

    # Call Claude with tools
    response_text, usage = await _call_claude_with_tools(
        user_id=user_id,
        message=message,
        history=history,
        system_prompt=system_prompt,
        tools=TOOL_REGISTRY
    )

    # Update usage tracking
    _update_user_usage(user_id, usage)

    # Format response with usage footer
    final_response = _format_response_with_usage(response_text, user_id, usage)

    # Send response
    if is_dm:
        # Edit thinking message
        thinking_event = client.thinking_messages.pop(room_id, None)
        if thinking_event:
            await client.edit_message(room_id, thinking_event, final_response)
        else:
            await client.send_message(room_id, final_response)
    else:
        # React in room, respond in DM
        await client.send_reaction(room_id, event_id, "✅")
        dm_room = await client.get_or_create_dm(user_id)
        await client.send_message(dm_room, final_response)


async def _build_matrix_conversation_history(room_id: str, user_id: str) -> list:
    """Build conversation history from Matrix room."""

    config = _load_config()
    user_config = config.get("users", {}).get(user_id, {})
    memory_config = user_config.get("memory", {})

    strategy = memory_config.get("strategy", "rolling")
    if strategy == "none":
        return []

    window = memory_config.get("window", 10)

    # Fetch room history
    messages = await client.fetch_room_history(room_id, limit=window * 2)

    # Filter to user <-> bot exchanges
    history = []
    for msg in messages:
        if msg.sender == user_id:
            history.append({"role": "user", "content": msg.body})
        elif msg.sender == client.user_id:
            history.append({"role": "assistant", "content": msg.body})

    # Ensure alternating roles
    return _ensure_alternating_roles(history[-window*2:])
```

### 5. Response Formatting

```python
def format_command_response(result: dict, user_id: str) -> str:
    """Format command result with ECO streak footer."""

    # Get ECO streak
    streak = _get_eco_streak(user_id)
    tokens_saved = streak * 500  # Estimate

    # Format main response
    response = result.get("message", "")

    # Add ECO footer
    if streak > 0:
        response += f"\n\n🌿 ECO streak: {streak} | ~{tokens_saved:,} tokens saved"

    return response


def format_task_list_html(tasks: list) -> tuple[str, str]:
    """Return (markdown, html) for Matrix formatted message."""
    # (Implementation shown in Matrix-Specific Features section above)
    pass


def _get_help_impl() -> dict:
    """Return playful help text with all commands."""

    help_text = """
🎯 **eis - Your Playful Vikunja Assistant**

I help you manage tasks with fun, memorable commands!

---

### 🔥 Quick Filters (No LLM cost - builds ECO streak!)

**Playful Commands:**
• `!oops` - Overdue tasks (oops, I missed these!)
• `!now` - Due today + overdue (what's happening NOW?)
• `!week` - Due this week
• `!fire` - Urgent tasks (priority 5) 🔥
• `!zen` - Today's focus (one task to rule them all) 🧘
• `!maybe` - Unscheduled tasks (someday/maybe)
• `!vip` - Priority tasks (3+)
• `!stats` - Task summary (show me the numbers) 📊

**Old names still work:** `!overdue`, `!today`, `!urgent`, `!focus`, etc.

---

### 🔗 Vikunja Connection

• `!vik` - Connect to Vikunja (get OAuth URL)
• `!novik` - Disconnect from Vikunja
• `!viki` - List your connected Vikunja instances

**Old names:** `!connect`, `!disconnect`, `!connections`

---

### 📌 Project Context

• `!project <name>` - Set active project
• `!project` - Show current project
• `!clear` - Clear project context
• `!bind <project>` - Bind this room to a project (personal)
• `!unbind` - Remove room binding
• `!binding` - Show current room binding

---

### 📚 Vikui (Knowledge Base)

• `!vikui <name>` - Bind room to knowledge base (room admins)
• `!vikui` - Show current binding
• `!novikui` - Remove binding
• `!vikuii` - List available knowledge bases

**What's Vikui?** Room-specific knowledge bases that make me an expert on different topics! Ask me anything related to the bound knowledge base.

---

### 📊 Viktus (Status Dashboard)

• `!viktus` - Show all connection status
  - Vikunja connection (state)
  - Vikui binding (content)
  - Active project context
  - ECO streak
  - Usage stats

**One command to see everything!**

---

### 💬 Natural Language (Uses Claude)

Just mention me or DM me:
• `@eis create a task to review PR by Friday`
• `@eis what's on my plate today?`
• `@eis move task #123 to next week`

I have access to 58 Vikunja tools and can help with:
• Creating, updating, deleting tasks
• Managing projects, labels, assignees
• Setting due dates, priorities, reminders
• Searching and filtering tasks
• And much more!

---

### ⚡ Quick Actions (React to my messages)

React to task messages with:
• ✅ - Mark task as done
• 📌 - Set priority to 5 (urgent)
• 🗑️ - Delete task
• ⏰ - Set due date to today

---

### 🌿 ECO Streak

Every time you use a `!command` instead of asking Claude, you build your ECO streak and save tokens!

**Milestones:**
• 🌱 Streak 5: "You're getting the hang of this!"
• 🌿 Streak 10: "ECO warrior!"
• 🌳 Streak 25: "Token-saving champion!"
• 🏆 Streak 50: "ECO legend!"

---

### ⚙️ Settings

• `!usage` - Check your token usage
• `!credits` - (Admin) Manage user credits

---

### 🎨 Personality

I'm:
• 🎯 **Helpful** - Always ready to assist
• 😄 **Playful** - Fun commands, emoji, gamification
• 🌿 **Eco-conscious** - Celebrates token savings
• 💪 **Motivating** - Positive reinforcement, no judgment
• 🧘 **Zen** - Helps you focus on what matters

---

**Pro Tips:**
1. Use `!commands` for quick filters (no LLM cost, builds streak!)
2. Bind rooms to projects for auto-context
3. React to task messages for instant actions
4. Ask me anything in natural language when you need help

**Need more help?** Just ask! I'm here to make task management fun and easy. 🚀
"""

    return {"message": help_text.strip()}
```

---

## Integration Points

### Shared Code (No Changes)

- `TOOL_REGISTRY` - All 58 tools work identically
- `_call_claude_with_tools()` - Tool execution loop
- `_load_config()`, `_save_config()` - User config YAML
- `_check_usage_limits()`, `_update_user_usage()` - Usage tracking
- `_get_instances()`, `_get_current_instance()` - Multi-instance support
- All `_*_impl()` functions - Tool implementations

### Refactored Code (Extract to Shared)

Currently Slack-specific, need to extract:

```python
# Extract from Slack implementation
def _build_conversation_history(user_id: str, channel_id: str, ts: str) -> list:
    """Slack-specific history builder."""
    # Move Slack API calls here
    pass

# New generic version
def _ensure_alternating_roles(messages: list) -> list:
    """Ensure user/assistant alternation (shared logic)."""
    # Extract from _build_conversation_history
    pass

# Matrix implementation
async def _build_matrix_conversation_history(room_id: str, user_id: str) -> list:
    """Matrix-specific history builder."""
    # Fetch from Matrix API, call _ensure_alternating_roles()
    pass
```

### New Code (Matrix-Specific)

- `MatrixClient` class
- Matrix event handlers
- `chat_with_claude()` for Matrix
- `handle_command()` for Matrix
- Room binding functions: `_bind_room_impl()`, `_unbind_room_impl()`, `_get_binding_impl()`
- Reaction handler: `handle_quick_action()`
- HTML formatting: `format_task_list_html()`
- Thread support: `create_task_with_thread()` (optional for V1)

---

## E2EE Considerations

**Current Decision**: Disable E2EE support for V1.

**Rationale**:
- Bot can't read encrypted rooms without device verification
- Device verification requires user interaction (emoji comparison or QR scan)
- Adds complexity to onboarding
- Most Factumerit rooms are not encrypted (business use case)

**Configuration**:
```bash
MATRIX_ENABLE_E2EE=false  # Default
```

**Future Enhancement** (V2+):
If E2EE is needed:
1. Use `matrix-nio` with `store_path` for device keys
2. Implement device verification flow
3. Auto-verify admin devices
4. Document user verification process

---

## Testing Strategy

### Unit Tests

```python
# test_matrix_client.py
async def test_send_message():
    """Test message sending."""
    pass

async def test_dm_creation():
    """Test DM room creation."""
    pass

async def test_reaction_handling():
    """Test reaction quick actions."""
    pass

# test_room_binding.py
def test_bind_room():
    """Test room-project binding."""
    pass

def test_auto_project_context():
    """Test automatic project injection."""
    pass

# test_command_handler.py
async def test_overdue_command():
    """Test !overdue command."""
    pass

async def test_eco_streak():
    """Test ECO streak tracking."""
    pass
```

### Integration Tests

```python
# test_matrix_integration.py
async def test_full_flow():
    """Test: mention bot → Claude response → DM."""
    pass

async def test_command_flow():
    """Test: !today → task list → reaction → complete task."""
    pass

async def test_room_binding_flow():
    """Test: !bind → auto-context → task creation."""
    pass
```

### Manual Testing Checklist

- [ ] Bot joins room when invited
- [ ] Mention in room → DM response
- [ ] DM to bot → direct response
- [ ] !commands work (overdue, today, etc.)
- [ ] ECO streak increments/resets correctly
- [ ] Claude integration works (tool calls, conversation memory)
- [ ] Usage tracking enforces limits
- [ ] Admin commands restricted to admins
- [ ] OAuth callback flow works (!connect)
- [ ] Multi-instance switching works
- [ ] Room binding works (!bind, auto-context)
- [ ] Reaction quick actions work (✅, 📌, etc.)
- [ ] HTML formatting displays correctly in Element
- [ ] Message edits work (thinking indicator)
- [ ] Typing indicators work

---

## Success Criteria

### MVP (V1) - Feature Parity

- [ ] All 58 Vikunja tools accessible via Claude
- [ ] All !commands work (overdue, today, week, etc.)
- [ ] DM privacy model works (mention in room → DM response)
- [ ] User authentication via !connect
- [ ] Usage tracking & limits enforced
- [ ] Conversation memory (rolling window)
- [ ] ECO streak tracking
- [ ] Multi-instance Vikunja support
- [ ] Admin functionality (credits, user management)

### V1 - Matrix-Specific Features

- [ ] Room-project binding (!bind, auto-context)
- [ ] Reaction quick actions (✅, 📌, 🗑️, ⏰)
- [ ] HTML formatting for task lists
- [ ] Message edits for thinking indicator

### V2 - Advanced Features (Future)

- [ ] Thread support for task discussions
- [ ] Presence-based reminders (opt-in)
- [ ] Room-specific command aliases
- [ ] E2EE support with device verification
- [ ] Rich media attachments (images, files)
- [ ] Calendar integration (iCal feed)

---

## Implementation Order

### Phase 1: Core Infrastructure (solutions-3k2u)
- [ ] Add matrix-nio dependency to pyproject.toml
- [ ] Add Matrix env vars to .env.example
- [ ] Create MatrixClient class skeleton
- [ ] Implement login & sync loop
- [ ] Test: Bot comes online, joins rooms

### Phase 2: Message Handling (solutions-baft)
- [ ] Implement RoomMessageText handler
- [ ] Implement mention detection
- [ ] Implement DM detection
- [ ] Test: Bot responds to mentions and DMs

### Phase 3: Command System (solutions-6c21)
- [ ] Implement !command parser
- [ ] Wire up all !commands to existing implementations
- [ ] Implement ECO streak tracking
- [ ] Test: All !commands work

### Phase 4: Claude Integration (solutions-jgy3)
- [ ] Implement chat_with_claude() for Matrix
- [ ] Implement conversation history builder
- [ ] Implement thinking indicator (message edits)
- [ ] Test: Claude responds with tool calls

### Phase 5: Room Management (solutions-ury0)
- [ ] Implement DM room creation
- [ ] Implement auto-join on invite
- [ ] Test: DM privacy model works

### Phase 6: Matrix-Specific Features (solutions-NEW)
- [ ] Implement room-project binding (!bind, !unbind, !binding)
- [ ] Implement auto-project context injection
- [ ] Implement reaction quick actions
- [ ] Implement HTML formatting for task lists
- [ ] Test: All Matrix-specific features work

### Phase 7: Testing & Polish (solutions-NEW)
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Manual testing checklist
- [ ] Documentation updates
- [ ] Deploy to production

---

## Deployment

### Environment Variables

```bash
# Matrix Bot
MATRIX_HOMESERVER_URL=https://matrix.factumerit.app
MATRIX_USER_ID=@eis:matrix.factumerit.app
MATRIX_PASSWORD=<secure_password>
MATRIX_DEVICE_ID=vikunja_bot_001
MATRIX_ADMIN_IDS=@i2:matrix.factumerit.app
MATRIX_ENABLE_E2EE=false

# Existing vars (Slack, MCP, Vikunja, Claude, etc.)
# ... unchanged ...
```

### Startup Command

```bash
# Run all three transports
python -m vikunja_mcp.server \
  --slack \
  --matrix \
  --mcp
```

### Health Checks

```python
# Add Matrix health check endpoint
@app.get("/health/matrix")
async def matrix_health():
    """Check Matrix bot status."""
    if matrix_client and matrix_client.logged_in:
        return {"status": "ok", "user_id": matrix_client.user_id}
    return {"status": "error", "message": "Not logged in"}, 503
```

---

## Migration Notes

### For Existing Slack Users

No changes required. Slack bot continues to work identically.

### For New Matrix Users

1. Admin creates bot account: `@eis:matrix.factumerit.app`
2. Admin invites bot to rooms
3. Users DM bot or mention in room
4. Bot prompts for !connect
5. Users authenticate with Vikunja
6. Users can optionally !bind rooms to projects

### Config File Changes

```yaml
# config.yaml - new Matrix user structure
users:
  # Slack users (unchanged)
  "U12345":
    vikunja_token: "tk_xxx"
    # ... existing fields ...

  # Matrix users (new)
  "@alice:matrix.factumerit.app":
    vikunja_token: "tk_yyy"
    timezone: "America/New_York"
    model: "haiku"
    memory:
      strategy: "rolling"
      window: 10
    room_bindings:  # NEW
      "!abc123:matrix.factumerit.app": "Client XYZ"
      "!def456:matrix.factumerit.app": "Internal Ops"
```

---

## Summary of Changes from V1

### Added Matrix-Specific Features

1. **Room-Project Binding** - `!bind` command for automatic project context
2. **Reaction Quick Actions** - ✅📌🗑️⏰ reactions to trigger actions
3. **HTML Formatting** - Color-coded task lists with visual hierarchy
4. **Thread Support** - Optional threaded task discussions (V2)

### Enhanced Sections

1. **Message Handling** - Added message edit strategy for thinking indicator
2. **Command System** - Added room binding commands (!bind, !unbind, !binding)
3. **Response Formatting** - Added HTML formatting functions
4. **Event Handlers** - Added ReactionEvent handler for quick actions
5. **Testing Strategy** - Added tests for Matrix-specific features
6. **Success Criteria** - Split into MVP (parity) and V1 (Matrix-specific)
7. **Implementation Order** - Added Phase 6 for Matrix-specific features

### Technical Improvements

1. **Auto-Project Context** - Room bindings eliminate manual `/project` switching
2. **Mobile UX** - Reaction quick actions for mobile users
3. **Visual Polish** - HTML formatting for better task list readability
4. **Organized Discussions** - Thread support for task-specific conversations

### Scope Decisions

**Included in V1**:
- Room-project binding (high value, low effort)
- Reaction quick actions (mobile UX win)
- HTML formatting (visual polish)

**Deferred to V2**:
- Thread support (optional, user-requested only)
- Presence-based reminders (low priority)
- E2EE support (adds complexity)

---

## Questions for Review

1. ~~**Room Binding Model**~~ - ✅ **RESOLVED**: Model 1 (personal) for V1, Model 2 (shared) planned for future
2. **Reaction Permissions** - Allow any user to react, or only task creator/assignee?
3. **HTML Fallback** - How to handle clients that don't support HTML? (Current: markdown fallback)
4. **Thread Auto-Creation** - Create thread on every task creation, or only on !thread command?
5. **E2EE Timeline** - When should we add E2EE support? (Current: V2+)

---

## Related Documents

- **MATRIX_TRANSPORT_SPEC_V1.md** - Original spec (feature parity only)
- **MATRIX_ROOM_BINDING_MODEL2.md** - Future enhancement: Shared room bindings for collaborative workspaces

---

**End of Specification V2**


