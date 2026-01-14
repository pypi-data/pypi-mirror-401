# X-Q Agent Guide

> How to check and process the Exchange Queue

## What is X-Q?

X-Q (Exchange Queue) is the human→agent task handoff system. When humans drop feature requests, file specs, or tasks in X-Q, agents pick them up for processing.

*"Well X-Q me!"* — Tasks politely excuse themselves to the queue.

## Quick Check

When asked to "check X-Q" or "check the exchange queue":

### 1. Read the config to get credentials and project IDs

```bash
cat ~/.vikunja-mcp/config.yaml
```

Key fields:
```yaml
instances:
  business:
    url: https://app.vikunja.cloud
    token: tk_xxx...
  personal:
    url: https://vikunja.factumerit.app
    token: eyJ...

xq:
  business: 14915    # X-Q project ID for business instance
  personal: 8        # X-Q project ID for personal instance
```

### 2. Query the X-Q project for pending tasks

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  "<URL>/api/v1/projects/<XQ_PROJECT_ID>/tasks" | python3 -c "
import json, sys
tasks = json.load(sys.stdin)
print(f'Found {len(tasks)} tasks in X-Q')
for t in tasks:
    if not t.get('done'):
        print(f\"  [{t['id']}] {t['title'][:60]}\")"
```

### 3. Get details on a specific task

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  "<URL>/api/v1/tasks/<TASK_ID>" | python3 -c "
import json, sys
t = json.load(sys.stdin)
print(f\"Task #{t['id']}: {t['title']}\")
print(f\"Created: {t.get('created')}\")
print(f\"Description:\")
print(t.get('description', '(none)'))"
```

## Example Session

User: "check the exchange queue for user @i2"

Agent response:
1. Read config → get business instance token and X-Q project ID (14915)
2. Query tasks → find pending items
3. Report back with task IDs and titles
4. If user asks about specific task → get full details

## Processing X-Q Tasks

After checking, common actions:

| Action | How |
|--------|-----|
| Create bead | `bd create --title="..." --description="From X-Q task <ID>. ..."` |
| Research | Investigate the request, document findings |
| Implement | If straightforward, do the work |
| Clarify | Ask user for more context if needed |

## MCP Tools (if available)

The bot has built-in X-Q tools:
- `check_xq(instance)` — List pending tasks
- `claim_xq_task(instance, task_id)` — Mark task as in-progress
- `complete_xq_task(instance, task_id, result)` — Mark done with notes

Use these if running within the MCP context. Use curl for direct API access.

## X-Q Project Structure

Each X-Q project has views/buckets:
- **Inbox** — New items awaiting processing
- **Review** — Being evaluated
- **Filed** — Completed (moved to bead, implemented, etc.)

## Tips

1. Always report task ID so user can reference it
2. Create a bead for non-trivial requests
3. Note the source: "From X-Q task 244147"
4. Close the loop — tell user what you found and what action you took
