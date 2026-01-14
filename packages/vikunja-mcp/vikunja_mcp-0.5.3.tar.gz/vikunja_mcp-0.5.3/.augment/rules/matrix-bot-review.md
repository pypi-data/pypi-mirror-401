# Matrix Bot Code Review Rules

**Purpose**: Automated code review rules for Matrix bot implementation  
**Scope**: vikunja-slack-bot Matrix transport layer  
**Last Updated**: 2025-12-24

---

## Integration Checks

### Rule: No Breaking Changes to Slack Bot

**Check**: Ensure Matrix bot implementation doesn't break existing Slack functionality.

**Examples of violations**:
- Modifying shared MCP tool signatures without updating Slack bot
- Changing config.yaml structure without backwards compatibility
- Removing or renaming shared utility functions
- Modifying shared error handling patterns

**How to verify**:
- Run Slack bot tests after Matrix changes
- Check that config.yaml still loads for Slack bot
- Verify shared utilities are not modified

---

### Rule: All MCP Tools Must Be Integrated

**Check**: All 58 MCP tools from vikunja-mcp must be accessible via Matrix bot.

**MCP Tools to verify**:
- Task management: create_task, list_tasks, update_task, delete_task, complete_task
- Project management: list_projects, get_project
- Label management: list_labels, create_label
- User management: get_current_user
- Search: search_tasks
- Filters: list_filters, apply_filter
- Admin tools: admin_set_user_token, admin_list_users, admin_connect_instance
- ... (all 58 tools)

**How to verify**:
- Check that Matrix message handler routes to all tools
- Verify command parser recognizes all tool names
- Ensure response formatter handles all tool outputs

---

### Rule: Config Changes Must Be Backwards Compatible

**Check**: Changes to config.yaml must not break existing deployments.

**Examples of violations**:
- Removing required fields without migration path
- Changing field types without validation
- Renaming fields without aliases

**How to verify**:
- Old config.yaml files still load
- New fields have sensible defaults
- Migration guide exists for breaking changes

---

## Security Checks

### Rule: Admin Commands Must Check MATRIX_ADMIN_IDS

**Check**: All admin commands must verify user is in MATRIX_ADMIN_IDS before executing.

**Admin commands**:
- `!credits` - Manage user credits
- `admin_set_user_token` - Set Vikunja token for user
- `admin_list_users` - List all users
- `admin_connect_instance` - Connect Vikunja instance

**Required pattern**:
```python
def _is_admin(user_id: str) -> bool:
    admin_ids = os.getenv('MATRIX_ADMIN_IDS', '').split(',')
    return user_id.strip() in [aid.strip() for aid in admin_ids if aid.strip()]

async def _handle_admin_command(user_id: str, args: list) -> dict:
    if not _is_admin(user_id):
        return {'message': '❌ Admin only command'}
    # ... execute admin logic
```

**Examples of violations**:
- Admin command without `_is_admin()` check
- Admin check after executing sensitive logic
- Revealing admin list in error messages

---

### Rule: No Hardcoded Secrets

**Check**: No passwords, tokens, or API keys in code.

**Examples of violations**:
- `MATRIX_PASSWORD = "secret123"`
- `bot_token = "xoxb-..."`
- `api_key = "sk-..."`

**Required pattern**:
- All secrets from environment variables: `os.getenv('MATRIX_PASSWORD')`
- No secrets in logs or error messages
- No secrets in config files committed to git

---

### Rule: E2EE Must Be Disabled (V1)

**Check**: MATRIX_ENABLE_E2EE must default to false.

**Rationale**: E2EE requires device verification, which blocks bot from reading messages.

**Required**:
- `MATRIX_ENABLE_E2EE` defaults to `false`
- Startup validation confirms E2EE is disabled
- Error message if E2EE accidentally enabled

**Reference**: docs/MATRIX_SECURITY.md, docs/MATRIX_TRANSPORT_SPEC_V2.md

---

### Rule: Input Sanitization for User Commands

**Check**: All user input must be sanitized before processing.

**Required sanitization**:
- Strip HTML tags from task titles: `re.sub(r'<[^>]+>', '', title)`
- Limit string lengths: `title[:256]`
- Escape HTML in markdown: `html.escape(text)`
- Validate command arguments

**Examples of violations**:
- Passing raw user input to database queries
- Rendering user input as HTML without escaping
- No length limits on user input

---

## Consistency Checks

### Rule: Match Existing Error Handling Patterns

**Check**: Error handling must match Slack bot patterns.

**Required pattern**:
```python
try:
    result = await some_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return {'error': 'User-friendly message'}
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    return {'error': 'Something went wrong'}
```

**Examples of violations**:
- Bare `except:` without logging
- Exposing internal errors to users
- Inconsistent error message format

---

### Rule: Follow Established Logging Conventions

**Check**: Logging must match existing patterns.

**Required pattern**:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed debug info")
logger.info("Important state changes")
logger.warning("Recoverable issues")
logger.error("Errors that need attention")
logger.exception("Errors with stack traces")
```

**Examples of violations**:
- Using `print()` instead of `logger`
- Inconsistent log levels
- Logging sensitive data (passwords, tokens)

---

### Rule: Response Formatting Must Match Slack Bot Style

**Check**: Matrix bot responses must match Slack bot formatting.

**Required**:
- Task lists use color-coded HTML
- Error messages start with ❌
- Success messages start with ✅
- Thinking indicators use "🤔 Thinking..."
- ECO streak footer format matches Slack

**Examples of violations**:
- Plain text task lists (should be HTML)
- Inconsistent emoji usage
- Different success/error message format

---

## Completeness Checks

### Rule: All Playful Commands Must Be Implemented

**Check**: All playful commands from PLAYFUL_COMMANDS_SUMMARY.md must work.

**Required commands**:
- `!vik` - Connect to Vikunja
- `!novik` - Disconnect from Vikunja
- `!viki` - List Vikunja instances
- `!vikui` - Connect to knowledge base
- `!novikui` - Disconnect from knowledge base
- `!vikuii` - List knowledge bases
- `!viktus` - Show connection status
- `!oops` - Undo last action
- `!now` - Tasks due now
- `!fire` - Urgent tasks
- `!zen` - Calm tasks

**Backward compatibility**:
- Old commands still work: `!overdue`, `!today`, etc.

---

### Rule: DM Privacy Model Must Be Implemented

**Check**: Channel mentions must trigger DM responses + reaction.

**Required behavior**:
- User mentions bot in channel → Bot sends DM + reacts with 📬
- User DMs bot → Bot responds in DM
- No task data in public channels

**Reference**: docs/MATRIX_TRANSPORT_SPEC_V2.md (Privacy Model section)

---

### Rule: Thinking Indicators Must Work

**Check**: Bot must show typing indicator and "thinking" message.

**Required behavior**:
1. User sends message
2. Bot shows typing indicator
3. Bot sends "🤔 Thinking..." message
4. Bot edits message to final response

**Reference**: docs/MATRIX_TRANSPORT_SPEC_V2.md (Response Formatting section)

---

### Rule: Reconnection Logic Must Handle Edge Cases

**Check**: Bot must reconnect gracefully on disconnect.

**Required**:
- Exponential backoff on reconnection
- Max retry limit
- Preserve message queue during disconnect
- Log reconnection attempts

**Edge cases to handle**:
- Network timeout
- Server restart
- Invalid credentials
- Rate limiting

---

## Performance Checks

### Rule: No Synchronous Operations Blocking Event Loop

**Check**: All I/O operations must be async.

**Examples of violations**:
- `requests.get()` instead of `aiohttp.get()`
- `time.sleep()` instead of `asyncio.sleep()`
- Synchronous file I/O in async functions

**Required**:
- Use `async`/`await` for all I/O
- Use `asyncio.sleep()` for delays
- Use async libraries (aiohttp, asyncpg, etc.)


