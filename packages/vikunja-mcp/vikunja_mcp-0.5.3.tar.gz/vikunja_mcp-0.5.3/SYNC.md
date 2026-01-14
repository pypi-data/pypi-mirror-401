# Code Sync: vikunja-mcp → vikunja-slack-bot

## Architecture

Two repos, shared codebase:

| Repo | Purpose | Deployment |
|------|---------|------------|
| `spawn-solutions/.../vikunja-mcp` | Development, UAT, Claude Desktop | Local (PM2) |
| `vikunja-slack-bot` | Slackbot production | Render |

The `server.py` is identical. Development happens in vikunja-mcp, then syncs to vikunja-slack-bot for deployment.

## Sync Process

After UAT/development in vikunja-mcp:

```bash
# 1. Copy server.py
cp ~/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-mcp/src/vikunja_mcp/server.py \
   ~/vikunja-slack-bot/src/vikunja_mcp/server.py

# 2. Check for new dependencies
diff ~/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-mcp/pyproject.toml \
     ~/vikunja-slack-bot/pyproject.toml

# If dependencies differ, update vikunja-slack-bot/pyproject.toml manually
# (Only the dependencies list - other metadata may differ)

# 3. Verify line count (should match)
wc -l ~/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-mcp/src/vikunja_mcp/server.py
wc -l ~/vikunja-slack-bot/src/vikunja_mcp/server.py

# 4. Test locally (optional)
cd ~/vikunja-slack-bot
uv run pytest

# 5. Commit and push
git add src/vikunja_mcp/server.py pyproject.toml
git commit -m "Sync server.py from vikunja-mcp (feature summary)"
git push

# 6. Render auto-deploys from main branch
```

## What Gets Synced

- `src/vikunja_mcp/server.py` - The entire MCP server + Slack integration
- `pyproject.toml` dependencies - **Must sync manually when new deps added!**

## What Stays Separate

| File | vikunja-mcp | vikunja-slack-bot |
|------|-------------|-------------------|
| `render.yaml` | Reference only | Render deployment config |
| `Dockerfile.vikunja` | Not used | Optional Docker build |
| `DEPLOY_*.md` | Not present | Deployment docs |
| `.env` | Local tokens | Render env vars |
| `tests/` | Full suite | Not synced |

## Lessons Learned

**2025-12-19: Missing dependency broke deploy**
- Added `icalendar` in vikunja-mcp for calendar feature
- Forgot to sync pyproject.toml to vikunja-slack-bot
- Render deploy failed with `ModuleNotFoundError: No module named 'icalendar'`
- Fix: Always diff pyproject.toml when syncing new features

## Why Two Repos?

1. **Separation of concerns**: Dev vs production
2. **Different deployment targets**: Local PM2 vs Render
3. **Secret management**: Different token storage
4. **Git history**: Keep production clean

## Future: Single Source of Truth

Options to consider:
1. **Git submodule**: vikunja-mcp as submodule in slack-bot
2. **Published package**: `pip install vikunja-mcp`
3. **Symlink**: Local dev with symlinked server.py
4. **Monorepo**: Single repo with deployment configs

Current approach (manual copy) works for now. Revisit if sync becomes painful.

## Last Sync

- **Date**: 2025-12-19
- **From**: vikunja-mcp @ 5390 lines
- **Changes**: ICS calendar HTTP endpoint, get_calendar_url tool
- **Beads**: solutions-q7oo (complete)
- **New endpoint**: GET /calendar/{token}.ics?label=calendar
- **New tool**: get_calendar_url - returns subscription URL for Google Calendar
