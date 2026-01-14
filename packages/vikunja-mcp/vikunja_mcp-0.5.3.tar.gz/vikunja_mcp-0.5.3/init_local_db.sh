#!/bin/bash
# Initialize local PostgreSQL database with migrations

set -e

echo "🔧 Initializing local database..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
until docker-compose -f docker-compose.local.yml exec -T postgres pg_isready -U vikunja; do
  sleep 1
done

echo "✅ PostgreSQL is ready"

# Run migrations in order
MIGRATIONS=(
  "001_token_broker.sql"
  "003_add_request_interactions.sql"
  "004_add_instance_url.sql"
  "005_user_project_context.sql"
  "006_pending_connections.sql"
  "007_users_table.sql"
  "008_registration_tokens.sql"
  "009_token_usage.sql"
  "010_user_budgets.sql"
  "011_personal_bots.sql"
  "012_personal_bots_display_name.sql"
  "013_personal_bots_owner_id.sql"
  "014_personal_bots_owner_token.sql"
  "015_personal_bots_password.sql"
)

for migration in "${MIGRATIONS[@]}"; do
  echo "📝 Running migration: $migration"
  docker-compose -f docker-compose.local.yml exec -T postgres psql -U vikunja -d vikunja < "migrations/$migration"
done

echo "✅ Database initialized successfully!"
echo ""
echo "🎉 You can now:"
echo "   - Access Vikunja: http://localhost:3456"
echo "   - Access MCP Server: http://localhost:8000"
echo "   - Test beta signup: http://localhost:8000/beta-signup?code=LOCAL-TEST&email=test@example.com"

