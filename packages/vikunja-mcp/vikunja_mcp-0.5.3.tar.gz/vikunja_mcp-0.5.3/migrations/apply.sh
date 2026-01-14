#!/bin/bash
# Apply token broker migration to factumerit-db
#
# Usage:
#   ./apply.sh                    # Uses DATABASE_URL env var
#   ./apply.sh "postgres://..."   # Direct connection string
#
# Or via Render CLI:
#   render psql dpg-d54tgckhg0os739oddpg-a
#   Then paste contents of 001_token_broker.sql

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATION_FILE="$SCRIPT_DIR/001_token_broker.sql"

if [ -n "$1" ]; then
    DATABASE_URL="$1"
fi

if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL not set"
    echo ""
    echo "Options:"
    echo "  1. Export DATABASE_URL and run again"
    echo "  2. Pass connection string as argument: ./apply.sh 'postgres://...'"
    echo "  3. Run 'render psql dpg-d54tgckhg0os739oddpg-a' and paste SQL manually"
    exit 1
fi

echo "Applying migration: 001_token_broker.sql"
echo "Database: ${DATABASE_URL%%@*}@..."  # Hide password
echo ""

psql "$DATABASE_URL" -f "$MIGRATION_FILE"

echo ""
echo "Migration complete! Verifying..."
psql "$DATABASE_URL" -c "SELECT * FROM token_broker_migrations;"
