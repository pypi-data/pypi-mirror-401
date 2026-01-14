#!/bin/bash
# Factumerit Admin CLI launcher
# Sources .env for database credentials and runs fa.py
#
# Usage:
#   ./run-fa.sh vikunja delete-user user@example.com --dry-run
#   ./run-fa.sh vikunja list-users
#
# Bead: fa-letl

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Source .env if it exists (contains DATABASE_URL, VIKUNJA_ADMIN_TOKEN, etc.)
# Check project dir first, then home dir
if [ -f .env ]; then
    source .env
elif [ -f ~/.env ]; then
    source ~/.env
fi

# Run the fa CLI using uv
exec uv run python scripts/fa.py "$@"
