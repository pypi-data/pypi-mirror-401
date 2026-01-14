# Integration Tests

Integration tests for Matrix bot, OAuth flows, registration, and data isolation.

## Quick Start

```bash
# 1. Setup environment
cp tests/integration/.env.example tests/integration/.env
# Edit .env with your test credentials

# 2. Install dependencies
uv sync --group dev
playwright install chromium

# 3. Run tests
cd backend
source tests/integration/.env
uv run pytest tests/integration/ -v -m integration
```

## Test Suites

| Suite | File | Purpose | Priority |
|-------|------|---------|----------|
| **Data Isolation** | `test_data_isolation.py` | Users can't see each other's data | P0 |
| **Unconnected User** | `test_unconnected_user.py` | Proper behavior without Vikunja token | P0 |
| **Matrix Bot** | `test_matrix_bot.py` | Bot command handling | P1 |
| **OAuth Flow** | `test_oauth_flow.py` | OAuth connect pages | P1 |
| **Registration** | `test_registration_flow.py` | User registration journey | P1 |
| **HTML Escaping** | `test_html_escaping.py` | XSS protection | P1 |

### Critical Tests (P0)

#### Data Isolation (`test_data_isolation.py`)
- Connected user sees only their own tasks
- Cross-user isolation verification
- Race condition tests for rapid commands

#### Unconnected User (`test_unconnected_user.py`)
- All task commands require Vikunja token
- No data leakage to unconnected users
- Safe commands work without connection

## Running Tests

### All Integration Tests
```bash
source tests/integration/.env
uv run pytest tests/integration/ -v -m integration
```

### Data Isolation Only (Critical)
```bash
uv run pytest tests/integration/test_data_isolation.py tests/integration/test_unconnected_user.py -v -m integration
```

### Matrix Bot Tests Only
```bash
uv run pytest tests/integration/test_matrix_bot.py -v -m integration
```

### Playwright Tests Only
```bash
uv run pytest tests/integration/test_oauth_flow.py tests/integration/test_registration_flow.py -v
```

### With Coverage
```bash
uv run pytest tests/integration/ -v -m integration --cov=vikunja_mcp
```

### Headed Mode (See Browser)
```bash
uv run pytest tests/integration/test_oauth_flow.py --headed -v
```

## Environment Variables

### For Matrix Bot Tests
```bash
MATRIX_HOMESERVER=https://matrix.factumerit.app
MATRIX_USER_ID=@testuser:matrix.factumerit.app
MATRIX_ACCESS_TOKEN=syt_xxx
MATRIX_BOT_USER_ID=@eis:matrix.factumerit.app
TEST_DM_ROOM_ID=!xxx:matrix.factumerit.app
```

### For Unconnected User Tests (CRITICAL)
```bash
UNCONNECTED_USER_ID=@newuser:matrix.factumerit.app
UNCONNECTED_USER_TOKEN=syt_xxx
UNCONNECTED_DM_ROOM_ID=!xxx:matrix.factumerit.app
```

### For Two-User Isolation Tests
```bash
MATRIX_USER_A_ID=@usera:matrix.factumerit.app
MATRIX_USER_A_TOKEN=syt_xxx
MATRIX_USER_B_ID=@userb:matrix.factumerit.app
MATRIX_USER_B_TOKEN=syt_xxx
```

### For OAuth Tests
```bash
OAUTH_BASE_URL=https://vikunja.factumerit.app
```

## Test Data Requirements

### Matrix Accounts Needed

| Account | Purpose | Has Vikunja Token? |
|---------|---------|-------------------|
| Connected user | Main test user | Yes |
| Unconnected user | Data isolation test | **NO** |
| Second user | Cross-user isolation | Yes (different Vikunja) |

### Creating Test Accounts

```bash
# Generate registration token
wallet pick 1 "Integration Test User"

# Register at https://matrix.factumerit.app/register
```

### Getting Access Tokens

1. Log into Element or another Matrix client
2. Settings > Help & About > Access Token (show)
3. Copy the access token

## Test Structure

```
tests/integration/
├── conftest.py                 # Shared fixtures
├── test_data_isolation.py      # P0: Data isolation tests
├── test_unconnected_user.py    # P0: Unconnected user tests
├── test_matrix_bot.py          # P1: Bot command tests
├── test_oauth_flow.py          # P1: OAuth page tests
├── test_registration_flow.py   # P1: Registration flow tests
├── test_html_escaping.py       # P1: XSS protection tests
├── .env.example                # Environment template
└── README.md                   # This file
```

## Writing New Tests

### Matrix Bot Tests

```python
async def test_my_command(matrix_client, bot_dm_room, bot_user):
    response = await matrix_client.send_and_wait(
        bot_dm_room,
        "!mycommand arg1",
        bot_user,
        timeout=30.0,
    )
    assert response is not None
    assert "expected text" in response
```

### OAuth Flow Tests (Playwright)

```python
def test_page_loads(page, oauth_config):
    url = f"{oauth_config.base_url}/connect.html"
    page.goto(url)
    expect(page).to_have_title("Expected Title")
```

### Parametrized Command Tests

```python
@pytest.mark.parametrize("command", ["!oops", "!now", "!stats"])
async def test_commands_require_token(unconnected_client, command):
    client, config = unconnected_client
    response = await client.send_and_wait(...)
    assert "connect" in response.lower()
```

## CI Integration

### GitHub Actions

```yaml
- name: Run Integration Tests
  env:
    MATRIX_HOMESERVER: ${{ secrets.MATRIX_HOMESERVER }}
    MATRIX_USER_ID: ${{ secrets.TEST_USER_ID }}
    MATRIX_ACCESS_TOKEN: ${{ secrets.TEST_USER_TOKEN }}
    MATRIX_BOT_USER_ID: ${{ secrets.BOT_USER_ID }}
    TEST_DM_ROOM_ID: ${{ secrets.TEST_DM_ROOM_ID }}
  run: |
    uv run pytest tests/integration/ -v -m integration
```

## Troubleshooting

### Tests Skip with "environment not configured"
- Ensure all required env vars are set
- Source the .env file: `source tests/integration/.env`

### Matrix Client Timeout
- Check Matrix homeserver is reachable
- Verify access tokens are valid (not expired)
- Increase timeout in `send_and_wait()`

### Playwright Tests Fail
- Run `playwright install chromium`
- Check OAUTH_BASE_URL is accessible
- Use `--headed` to see what's happening

### "No module named 'nio'"
- Install matrix-nio: `uv add matrix-nio[e2e]`

## Related Issues

- `solutions-k8ze` - Data isolation fix (CLOSED)
- `solutions-pg8k` - Integration testing framework (IN_PROGRESS)
- `solutions-w616` - Playwright OAuth tests (OPEN)
- `solutions-rekr` - matrix-nio bot tests (OPEN)
