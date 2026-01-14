# Role-Based Access Control (RBAC)

> **Status**: Implemented (Dec 26, 2025)
> **Issue**: solutions-xzpb.1.9

## Overview

The bot uses a role-based access control system to manage permissions. This replaces the previous binary admin system (`ADMIN_SLACK_IDS` env var) with a hierarchical role model.

## Role Hierarchy

Roles are ordered from least to most privileged:

| Level | Role | Description |
|-------|------|-------------|
| 0 | `user` | Default role. Can use bot, see own usage. |
| 1 | `support` | Can view any user's usage (read-only). |
| 2 | `moderator` | Can set tiers (up to pro), suspend users. |
| 3 | `admin` | Can grant unlimited, manage moderators, add credits. |
| 4 | `owner` | All capabilities. Can manage admins, emergency stop. |

## Capabilities by Role

```
user:       use_bot, see_own_usage
support:    + view_any_usage
moderator:  + set_tier_basic, set_tier_pro, suspend_user
admin:      + set_tier_unlimited, manage_moderators, add_credits
owner:      * (all capabilities)
```

## Storage

Roles are stored in the YAML config:

```yaml
user_roles:
  "U12345ABC":                    # Slack user ID
    role: admin
    granted_by: "U98765XYZ"       # Who granted the role
    granted_at: "2025-12-26T10:00:00+00:00"
  "@ivan:matrix.example.com":     # Matrix user ID
    role: owner
    granted_by: "system:migration"
    granted_at: "2025-12-26T10:00:00+00:00"
```

Users without an entry default to `user` role.

## Slack Commands

### `/role` (admin+ only)

```
/role @user           Show user's current role
/role @user set admin Set user's role
/role list            List all users with explicit roles
```

**Constraints:**
- You can only grant roles *below* your own level
- You cannot change your own role
- Owner role cannot be granted via commands

### Examples

```
/role @alice              → Shows Alice's role
/role @alice set admin    → Promotes Alice to admin (if you're owner)
/role @bob set moderator  → Promotes Bob to moderator (if you're admin+)
/role list                → Lists all users with roles
```

## Migration from ADMIN_SLACK_IDS

On startup, the bot automatically migrates users listed in `ADMIN_SLACK_IDS` to the `owner` role:

```python
# Environment variable (legacy)
ADMIN_SLACK_IDS=U12345ABC,U98765XYZ

# After migration, these users have:
user_roles:
  "U12345ABC": {role: owner, granted_by: system:migration, ...}
  "U98765XYZ": {role: owner, granted_by: system:migration, ...}
```

The migration is idempotent—it only runs if users don't already have a role assigned.

## Developer Reference

### Core Functions

```python
from vikunja_mcp.server import (
    _get_user_role,
    _set_user_role,
    _has_role,
    _has_capability,
    _can_grant_role,
    _is_admin,  # backward-compatible wrapper
)
```

### `_get_user_role(user_id: str) -> str`

Get user's role. Returns `"user"` if not set.

```python
role = _get_user_role("U12345ABC")  # "admin"
role = _get_user_role("unknown")     # "user"
```

### `_has_role(user_id: str, required_role: str) -> bool`

Check if user has *at least* the required role level.

```python
_has_role("U12345ABC", "admin")      # True if admin or owner
_has_role("U12345ABC", "owner")      # True only if owner
_has_role("U12345ABC", "user")       # Always True (everyone is at least user)
```

### `_has_capability(user_id: str, capability: str) -> bool`

Check if user has a specific capability.

```python
_has_capability(user_id, "add_credits")     # True for admin+
_has_capability(user_id, "view_any_usage")  # True for support+
```

### `_can_grant_role(granter_id: str, target_role: str) -> bool`

Check if granter can assign the target role (must be strictly higher).

```python
# If granter is admin (level 3):
_can_grant_role(admin_id, "moderator")  # True (3 > 2)
_can_grant_role(admin_id, "admin")      # False (3 > 3 is false)
_can_grant_role(admin_id, "owner")      # False (3 > 4 is false)
```

### `_set_user_role(user_id: str, role: str, granted_by: str) -> dict`

Set a user's role. Returns success/error dict.

```python
result = _set_user_role("U12345ABC", "admin", "U98765XYZ")
# {"user_id": "U12345ABC", "old_role": "user", "new_role": "admin",
#  "granted_by": "U98765XYZ", "success": True}
```

### `_is_admin(user_id: str) -> bool` (backward-compatible)

Legacy function. Returns `True` if user has `admin` or `owner` role.

```python
# Equivalent to:
_has_role(user_id, "admin")
```

## Security Considerations

1. **No self-elevation**: Users cannot change their own role via `/role` command.

2. **Hierarchy enforcement**: Can only grant roles below your level. Owners can grant admin, admins can grant moderator, etc.

3. **Owner is special**: The `owner` role can only be assigned through:
   - Migration from `ADMIN_SLACK_IDS`
   - Direct config file edit
   - Not via `/role` command

4. **Audit trail**: Role changes include `granted_by` and `granted_at` for accountability.

## Future Enhancements

- [ ] Matrix `/role` command (currently Slack-only)
- [ ] Audit logging for role changes (xzpb.1.10)
- [ ] Role expiration (`expires_at` field)
- [ ] Capability-based checks in more places
