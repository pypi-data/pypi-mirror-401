# Deploy Vikunja on Render

Manual setup for self-hosted Vikunja (SQLite path: ~$11.50/mo).

## Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Select **Deploy an existing image from a registry**
4. Image URL: `vikunja/vikunja:latest`
5. Name: `vikunja` (or `vikunja-factumerit`)
6. Region: Same as your Slack bot
7. Plan: **Starter** ($9/mo)

## Step 2: Configure Settings

Under **Settings**:

- **Port**: `3456` (Vikunja's default)
- **Health Check Path**: `/api/v1/info`

## Step 3: Environment Variables

Add these environment variables:

| Key | Value |
|-----|-------|
| `VIKUNJA_DATABASE_TYPE` | `sqlite` |
| `VIKUNJA_DATABASE_PATH` | `/db/vikunja.db` |
| `VIKUNJA_SERVICE_PUBLICURL` | `https://vikunja-XXXX.onrender.com` (your URL) |
| `VIKUNJA_SERVICE_FRONTENDURL` | Same as PUBLICURL |
| `VIKUNJA_SERVICE_ENABLEREGISTRATION` | `false` |
| `VIKUNJA_MAILER_ENABLED` | `false` |

## Step 4: Add Persistent Disk

1. Scroll to **Disks**
2. Click **Add Disk**
3. Name: `vikunja-data`
4. Mount Path: `/db`
5. Size: `10 GB` ($2.50/mo)

## Step 5: Deploy

Click **Create Web Service**. Wait 2-3 minutes for deployment.

## Step 6: Create Admin User

After deployment:

1. Visit your Vikunja URL
2. Temporarily set `VIKUNJA_SERVICE_ENABLEREGISTRATION=true`
3. Register your admin account
4. Set `VIKUNJA_SERVICE_ENABLEREGISTRATION=false` again
5. Redeploy

## Step 7: Create API Token

1. Log in to Vikunja
2. Go to **Settings** → **API Tokens**
3. Create token named "factum-erit"
4. Copy token (won't be shown again)

## Step 8: Update Slack Bot

Update your Slack bot environment variables:

- `VIKUNJA_URL`: `https://vikunja-XXXX.onrender.com/api/v1`
- `VIKUNJA_TOKEN`: (the token from Step 7)

## Cost Summary

| Service | Monthly Cost |
|---------|-------------|
| Vikunja Web Service (Starter) | $9.00 |
| Persistent Disk (10GB) | $2.50 |
| **Total** | **$11.50** |

## Creating Beta Tester Accounts

For each beta tester:

1. Temporarily enable registration
2. Have them create account at your Vikunja URL
3. They create API token in Settings
4. They send you the token (secure channel)
5. You add to Slack bot config
6. Disable registration again

Or: You create accounts for them and share credentials.

## Troubleshooting

**"Bad Gateway" or 502 error:**
- Wait a few minutes, Render is still deploying
- Check logs in Render dashboard

**"Database locked" errors:**
- SQLite issue under load
- Consider upgrading to PostgreSQL ($7/mo more)

**Can't log in:**
- Check PUBLICURL matches actual URL
- Check FRONTENDURL matches PUBLICURL
