# Claude Desktop Export Format

Research for fa-sv6a: GTD Chat History Collection feature

## Export Process

From [Claude Help Center](https://support.claude.com/en/articles/9450526-how-can-i-export-my-claude-data):

1. Settings > Privacy > Export data
2. Export processed, download link emailed (24h expiry)
3. ZIP file containing JSON data

## ZIP Structure

```
data-{timestamp}-batch-{n}.zip
├── users.json          # Account info (~150 bytes)
├── conversations.json  # All chat history (~111 MB for 347 convos)
├── memories.json       # Claude memory feature (~26 KB)
└── projects.json       # Project artifacts (~4.4 MB)
```

## users.json

```json
[
  {
    "uuid": "b3498171-...",
    "full_name": "Name",
    "email_address": "email@example.com",
    "verified_phone_number": null
  }
]
```

## conversations.json

Main chat history. Array of conversation objects.

### Conversation Object

```json
{
  "uuid": "afc58ea9-bff1-434f-97fa-180262029ff0",
  "name": "Conversation title",
  "summary": "Optional summary",
  "created_at": "2025-12-14T18:33:11.903723Z",
  "updated_at": "2025-12-14T23:05:37.287929Z",
  "account": {...},
  "chat_messages": [...]
}
```

### Message Object

```json
{
  "uuid": "019b1e23-62e3-7768-999c-f4bb7ffab051",
  "text": "Plain text version of message",
  "content": [...],
  "sender": "human|assistant",
  "created_at": "2025-12-14T18:33:14.284238Z",
  "updated_at": "2025-12-14T18:33:14.284238Z",
  "attachments": [],
  "files": []
}
```

### Content Block Types

```json
{
  "type": "text",
  "text": "Message content",
  "start_timestamp": "...",
  "stop_timestamp": "...",
  "flags": null,
  "citations": []
}
```

Other types: `tool_use`, `tool_result`, etc.

## memories.json

Claude's memory feature - accumulated context about user.

```json
[
  {
    "conversations_memory": "**Work context**\nUser is...",
    "project_memories": {...},
    "account_uuid": "..."
  }
]
```

**GTD Value:** Pre-existing user context, potential reference material.

## projects.json

Project artifacts (files uploaded, custom instructions).

```json
[
  {
    "uuid": "...",
    "name": "Project Name",
    "description": "...",
    "is_private": true,
    "prompt_template": "",
    "created_at": "...",
    "docs": [
      {
        "uuid": "...",
        "filename": "file.md",
        "content": "..."
      }
    ]
  }
]
```

**GTD Value:** Reference materials, project contexts.

## Statistics (Example Export)

| Metric | Value |
|--------|-------|
| Conversations | 347 |
| Total messages | 11,998 |
| Human messages | 6,014 |
| Assistant messages | 5,984 |
| Export size (compressed) | 29 MB |
| Export size (uncompressed) | 116 MB |

## Comparison: Desktop vs Code

| Aspect | Desktop | Code |
|--------|---------|------|
| Format | Single JSON file | JSONL per session |
| Threading | Flat (within conversation) | Tree (uuid/parentUuid) |
| Summaries | Per-conversation | Per-branch (leafUuid) |
| Metadata | Minimal | Rich (git, cwd, version) |
| Tool calls | In content blocks | Separate entries |

## Unified Parser Strategy

1. Normalize both formats to common schema:
   ```json
   {
     "conversation_id": "...",
     "source": "desktop|code",
     "messages": [
       {"role": "user|assistant", "content": "...", "timestamp": "..."}
     ],
     "metadata": {...}
   }
   ```

2. Desktop: Iterate `conversations[].chat_messages[]`
3. Code: Iterate project JSONL, filter to user/assistant types
4. Merge by timestamp proximity for deduplication
