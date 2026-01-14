# Factumerit Development Context

This is the PRIVATE factumerit repo. It contains both public and private code.

## vikunja-mcp Public/Private Split

**Two repos exist:**
- **Private** (here): `/home/ivanadamin/gt/factumerit/crew/ivan` - full factumerit bot
- **Public**: `~/vikunja-mcp` - clean vikunja-mcp for PyPI

**NEVER publish from the private repo directly** - it contains:
- User management (`_get_user_*`, `_set_user_*`)
- Auth/OAuth flows
- Slack/Matrix bot handlers
- Billing, credits, usage tracking
- Bot provisioning, signup workflows

### Adding New Public Tools

When adding MCP tools to `src/vikunja_mcp/server.py`:

1. **Tag with `# @PUBLIC`** if it's a generic Vikunja operation:
   ```python
   # @PUBLIC
   @mcp.tool()
   def my_new_tool(...):
       ...
   ```

2. **DO NOT tag** if it touches:
   - User management (user_id, _get_user_*, _set_user_*)
   - Auth/OAuth (oauth_*, vikunja_callback)
   - Slack handlers (slash_*, handle_*)
   - Matrix handlers (_matrix_*)
   - Billing (credits, usage, limits, api_key)
   - Factumerit-specific logic

3. **Run extraction** after tagging:
   ```bash
   python scripts/extract_public.py --dry-run  # Preview
   python scripts/extract_public.py            # Generate
   ```

4. **Test and publish** from ~/vikunja-mcp:
   ```bash
   cd ~/vikunja-mcp
   uv build && uv publish --token $PYPI_TOKEN
   ```

### Tag Reference

| Tag | Use For |
|-----|---------|
| `# @PUBLIC` | Tools safe for public PyPI release |
| `# @PUBLIC_HELPER` | Helper functions needed by public tools |
| `# @PRIVATE` | Factumerit-specific, never publish |

**EVERY function must be tagged.** Run `python scripts/check_tags.py` to verify.

### Publishing Checklist

Before publishing to PyPI:
1. [ ] Verify no private code in ~/vikunja-mcp (`ls src/vikunja_mcp/`)
2. [ ] Check wheel contents (`unzip -l dist/*.whl`)
3. [ ] Bump version in pyproject.toml
4. [ ] Build and publish from ~/vikunja-mcp only

## Admin CLI (`fa`)

The `fa` command is the Factumerit Admin CLI. Shell wrapper at `~/spawn-solutions/scripts/fa.sh`, aliased as `fa`.

```bash
fa health              # Check all services
fa ledger balances     # Double-entry accounting - all account balances
fa ledger user <id>    # User's ledger entries (e.g., fa ledger user vikunja:alice)
fa ledger integrity    # Verify debits = credits
fa ledger summary      # Aggregate by account type
fa vikunja list-users  # List all Factumerit users
fa vikunja delete-user <email>  # Delete user completely
```

The ledger commands use `scripts/fa.py` which requires the project venv (handled automatically via `uv run`).

## Development Notes

- Use `uv` for all Python operations
- Never commit secrets/tokens - use .env files
- Run tests: `uv run pytest tests/ -v`
