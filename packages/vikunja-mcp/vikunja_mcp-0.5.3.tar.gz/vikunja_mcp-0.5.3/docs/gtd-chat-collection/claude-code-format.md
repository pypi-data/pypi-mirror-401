# Claude Code Local Storage Format

Research for fa-fz0m: GTD Chat History Collection feature

## Directory Structure

```
~/.claude/
├── history.jsonl           # User input history (all projects)
├── projects/               # Per-project conversation storage
│   └── {encoded-path}/     # Project path with / → -
│       └── {session-id}.jsonl  # Full conversation logs
├── file-history/           # File change tracking
├── session-env/            # Session environment snapshots
├── todos/                  # Per-session todo lists
├── settings.json           # User preferences
└── stats-cache.json        # Usage statistics
```

## history.jsonl Format

Global user input log. One entry per user message across all projects.

```json
{
  "display": "User's input text",
  "pastedContents": {},
  "timestamp": 1759033644349,
  "project": "/home/user/project-path"
}
```

**Fields:**
- `display`: The user's input text
- `pastedContents`: Object containing any pasted file contents
- `timestamp`: Unix timestamp (milliseconds)
- `project`: Absolute path to the project directory

**GTD Value:** Quick scan of what topics were discussed without loading full conversations.

## projects/{encoded-path}/{session-id}.jsonl Format

Full conversation logs with message threading.

### Message Types

| Type | Count (typical) | Purpose |
|------|-----------------|---------|
| `user` | ~28% | User messages |
| `assistant` | ~57% | Claude responses |
| `file-history-snapshot` | ~10% | File state tracking |
| `queue-operation` | ~5% | Internal queueing |
| `summary` | <1% | Conversation summaries |
| `system` | <1% | System events (compaction, etc.) |

### User Message

```json
{
  "type": "user",
  "uuid": "7d0eee35-8c7e-46a9-9ae6-a53345649efa",
  "parentUuid": null,
  "timestamp": "2025-12-22T16:20:02.736Z",
  "sessionId": "8b3581e9-b449-4e9a-abef-177bd7008f60",
  "cwd": "/home/user/project",
  "gitBranch": "main",
  "version": "2.0.75",
  "message": {
    "role": "user",
    "content": "User's message text"
  },
  "userType": "external",
  "isSidechain": false,
  "thinkingMetadata": {"level": "high", "disabled": false, "triggers": []},
  "todos": []
}
```

### Assistant Message

```json
{
  "type": "assistant",
  "uuid": "abc123...",
  "parentUuid": "7d0eee35...",
  "timestamp": "2025-12-22T16:20:05.123Z",
  "sessionId": "8b3581e9...",
  "message": {
    "model": "claude-opus-4-5-20251101",
    "id": "msg_0134gr1RNtP3bZMDPFhAxtSR",
    "type": "message",
    "role": "assistant",
    "content": [...],
    "stop_reason": "end_turn",
    "usage": {
      "input_tokens": 10,
      "output_tokens": 500,
      "cache_read_input_tokens": 12832
    }
  }
}
```

### Summary Entry

Appears at top of file, summarizes conversation branches.

```json
{
  "type": "summary",
  "summary": "Human-readable conversation summary",
  "leafUuid": "a1b33dbd-9644-4c59-889b-2975c78792a4"
}
```

**GTD Value:** Pre-computed summaries for quick triage without parsing full conversation.

### System Events

```json
{
  "type": "system",
  "subtype": "compact_boundary",
  "content": "Conversation compacted",
  "compactMetadata": {"trigger": "auto", "preTokens": 171137}
}
```

## Threading Model

Messages form a tree structure via `parentUuid`:
- Root messages have `parentUuid: null`
- Replies link to parent via `parentUuid`
- `leafUuid` in summaries points to branch endpoints
- `isSidechain: true` indicates alternative conversation branches

## Correlation Strategy

To reconstruct conversations:
1. Load all `.jsonl` files from `projects/{path}/`
2. Filter to `type: user` and `type: assistant`
3. Build tree from `uuid`/`parentUuid` relationships
4. Use `timestamp` for chronological ordering within branches
5. Use `summary` entries for quick overview

## Statistics (Example User)

- 395 conversation files
- 8538 user inputs in history.jsonl
- 23 unique projects
- Files range from ~100 to ~4800 lines

## Privacy Considerations

All data stored locally in `~/.claude/`. No cloud sync unless user explicitly shares.
Contains:
- Full conversation text (user and assistant)
- File paths and git branches
- Token usage statistics
- Timestamps for all interactions
