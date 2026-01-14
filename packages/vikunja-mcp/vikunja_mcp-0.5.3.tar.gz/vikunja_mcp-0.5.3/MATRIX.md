# Matrix Bot

Chat-based task management via Matrix protocol.

## Quick Commands (ECO mode - no AI cost)

| Command | Description |
|---------|-------------|
| `!help` | Show all commands |
| `!oops` | Overdue tasks |
| `!now` | Due today |
| `!fire` | Priority 5 (urgent) |
| `!vip` | Priority 3+ (high) |
| `!week` | Due this week |
| `!maybe` | Unscheduled tasks |
| `!zen` | Focus mode |
| `!done <title>` | Complete task by fuzzy title match |
| `!stats` | Task summary |

## Settings

| Command | Description |
|---------|-------------|
| `!tz` | View current timezone |
| `!tz <zone>` | Set timezone (e.g., `America/New_York`, `eastern`, `pacific`) |
| `!model` | View/change AI model (haiku, sonnet, opus) |
| `!credits` | Check usage/remaining credits |
| `!apikey` | Manage your API key (BYOK) |

## Connection

| Command | Description |
|---------|-------------|
| `!vik <token>` | Connect Vikunja with API token |
| `!viki` | List connections |
| `!test` | Test connection |

## Room Binding (rooms only, not DMs)

Bind a Matrix room to a Vikunja project for automatic context:

| Command | Description |
|---------|-------------|
| `!bind <project>` | Bind room to project (fuzzy search) |
| `!unbind` | Remove binding |
| `!binding` | Show current binding |

When a room is bound, commands automatically use that project context:
- `add task` → adds to bound project
- `list tasks` → shows bound project tasks

Each user has their own bindings (personal mode).

## Natural Language

Any message that isn't a `!command` is processed by AI:
- "what's due today"
- "add buy groceries"
- "show me urgent tasks"

## Environment Variables

```bash
MATRIX_HOMESERVER="https://matrix.example.com"
MATRIX_USER="@bot:example.com"
MATRIX_PASSWORD="bot-password"
# OR
MATRIX_ACCESS_TOKEN="syt_..."
```

## Architecture

```
Matrix ─→ matrix_client.py ─→ matrix_handlers.py ─→ Claude API
                                      │                  │
                                      ├── !commands ─────┘
                                      └── needs_llm ────→ _matrix_chat_with_claude()
                                                                    │
                                                              MATRIX_TOOLS
                                                                    │
                                                              TOOL_REGISTRY
```

**Key files:**
- `matrix_client.py` - Matrix transport (matrix-nio)
- `matrix_handlers.py` - Command routing, !bang commands
- `matrix_parser.py` - Fuzzy command parsing (RapidFuzz)
- `server.py` - TOOL_REGISTRY, `_matrix_chat_with_claude()`
