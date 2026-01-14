# Migration 004: Add instance_url Column

**Bead**: solutions-mr8f  
**Date**: 2025-12-29  
**Status**: Ready to deploy

---

## What This Fixes

**Problem**: Bot used `VIKUNJA_URL` env var for ALL instances, so users with multiple instances (personal on `vikunja.factumerit.app`, business on `app.vikunja.cloud`) had all queries go to the same URL.

**Solution**: Store the instance URL in PostgreSQL when users connect, so each instance has its own URL.

---

## How to Run the Migration

### Option 1: Render Dashboard (Recommended)

1. Go to https://dashboard.render.com/d/dpg-d50p4ns9c44c738capjg (PostgreSQL database)
2. Click **"Query"** tab
3. Copy/paste the SQL from `migrations/004_add_instance_url.sql`
4. Click **"Run Query"**
5. Verify: `SELECT user_id, vikunja_instance, instance_url FROM user_tokens;`

### Option 2: psql Command Line

```bash
# Get DATABASE_URL from Render dashboard (Environment → DATABASE_URL)
export DATABASE_URL="postgres://..."

# Run migration
psql $DATABASE_URL -f migrations/004_add_instance_url.sql

# Verify
psql $DATABASE_URL -c "SELECT user_id, vikunja_instance, instance_url FROM user_tokens;"
```

---

## After Migration

### Existing Users Need to Reconnect

Users who connected BEFORE this migration will have `instance_url = 'https://vikunja.factumerit.app'` (the default).

**If they have instances on different URLs**, they need to reconnect:

```
!vik https://vikunja.factumerit.app <token> personal
!vik https://app.vikunja.cloud <token> business
```

### New Users (After Migration)

New users who connect via:
- **OAuth**: URL automatically set to `VIKUNJA_URL` env var
- **Manual `!vik <url> <token>`**: URL stored from command

---

## Verification

After migration and reconnecting, run:

```
!viki
```

Should show:
```
**Connected Vikunja Instances:**

- business: https://app.vikunja.cloud
- personal: https://vikunja.factumerit.app ✓ (active)
```

Then test that `!now` works correctly with the active instance.

---

## Rollback (If Needed)

```sql
ALTER TABLE user_tokens DROP COLUMN instance_url;
DELETE FROM token_broker_migrations WHERE version = 4;
```

Then redeploy commit `2011195` (before this migration).

