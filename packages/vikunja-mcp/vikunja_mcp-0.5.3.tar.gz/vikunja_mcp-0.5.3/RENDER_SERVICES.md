# Render Service Name Mappings

## Production Services

| Render Service Name | Local/Code Name | Type | Purpose |
|---------------------|-----------------|------|---------|
| `factumerit-bot` | `vikunja-slack-bot` | Web Service | Main bot service (Slack/Matrix integration) |
| `factumerit-matrix` | `vikunja-matrix-bot` | Web Service | Matrix-specific bot service |
| `factumerit-vikunja:0.24.6` | N/A | Web Service | Vikunja task management instance |
| `factumerit-db` | N/A | PostgreSQL | Database for token storage, audit logs |
| `qrcards-deploy` | N/A | Web Service | QRCards application |

## Environment Variables

### `factumerit-bot` (Main Bot Service)
- `TOKEN_ENCRYPTION_KEY` - Fernet encryption key for token storage
- `DATABASE_URL` - PostgreSQL connection string
- `VIKUNJA_URL` - https://vikunja.factumerit.app
- `MATRIX_HOMESERVER` - Matrix server URL
- `SLACK_BOT_TOKEN` - Slack bot token

### `factumerit-matrix` (Matrix Bot)
- TBD - needs investigation

## Token Migration Status

✅ **Completed 2025-12-28**
- Migrated 3 tokens from YAML to PostgreSQL:
  - `@i2:matrix.factumerit.app` → `personal` instance (vikunja.factumerit.app)
  - `@i2:vikunja.cloud` → `business` instance (app.vikunja.cloud)
  - `@admission-attendant:matrix.factumerit.app` → `admission-attendant` instance

## Database

- **Host**: dpg-d54tgckhg0os739oddpg-a.oregon-postgres.render.com
- **Database**: matrix_jfmr
- **User**: factumerit
- **Tables**: `user_tokens`, `token_access_log`, `request_interactions`

