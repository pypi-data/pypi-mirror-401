# MCP Server Fix - Missing run-mcp.sh Script

## Problem

After reboot, Claude Desktop couldn't start the Vikunja MCP server with error:
```
Server transport closed unexpectedly, this is likely due to 
the process exiting early.
```

## Root Causes

### Issue 1: Missing Script
The `run-mcp.sh` script was missing from the repository. Claude Desktop calls this script via WSL to launch the MCP server.

### Issue 2: PATH Not Inherited
WSL doesn't inherit the full PATH when called from Windows, so the `uv` command was not found even after creating the script.

Error:
```
/home/ivanadamin/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-mcp/run-mcp.sh: line 17: exec: uv: not found
```

## Solution

Created `/home/ivanadamin/factumerit/backend/run-mcp.sh` with **full path to uv**:

```bash
#\!/bin/bash
# MCP Server launcher for Vikunja
# This script is called by Claude Desktop via WSL

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The actual server is in the factumerit backend
SERVER_DIR="/home/ivanadamin/factumerit/backend"

# Change to server directory
cd "$SERVER_DIR"

# Run the MCP server using uv (use full path since WSL doesn't inherit full PATH)
exec /home/ivanadamin/.local/bin/uv run python -m vikunja_mcp.server
```

**Key features:**
- ✅ Uses `uv run` to automatically manage Python dependencies
- ✅ Uses **full path** to `uv` (`/home/ivanadamin/.local/bin/uv`) to avoid PATH issues
- ✅ Points to the correct server location
- ✅ Made executable (`chmod +x`)

## Testing

```bash
$ timeout 3 /home/ivanadamin/factumerit/backend/run-mcp.sh 2>&1 || true
[12/26/25 21:38:31] INFO     Starting MCP server 'vikunja' with transport 'stdio'
```

✅ Server starts successfully
✅ All 54 tools verified in TOOL_REGISTRY including new create_view and update_view

## Deployment

- ✅ Committed: `f4bb3a9` (initial script)
- ✅ Committed: `3c9b9f5` (full path fix)
- ✅ Pushed to GitHub
- ⏳ Restart Claude Desktop to pick up the fix

## Related

- solutions-4bqk (view tools implementation)
- Commit: 24af598 (view tools)
- Commit: f4bb3a9 (run-mcp.sh script)
- Commit: 3c9b9f5 (full path to uv)
