# OIDC Existing User Login Loop - FIXED

**Date**: 2025-01-10
**Status**: ✅ Fixed and deployed
**Commit**: `e5b668c` in vikunja-factumerit repo

---

## Problem

Existing users logging in via Google OAuth got stuck in a login loop. The middleware correctly generated a JWT and returned `{"token": "..."}`, but the Vikunja frontend didn't process it - instead looping back to the login screen.

## Root Cause

**Off-by-one error in JWT type claim.**

The middleware was generating JWT tokens with `type: 0`, but Vikunja's auth type constants are:

```go
const (
    AuthTypeUnknown int = iota  // = 0
    AuthTypeUser                // = 1
    AuthTypeLinkShare           // = 2
)
```

So `type: 0` means "AuthTypeUnknown", not "AuthTypeUser"!

The Vikunja frontend checks:
```javascript
const authUser = computed(() => {
    return authenticated.value && (
        info.value &&
        info.value.type === AUTH_TYPES.USER  // AUTH_TYPES.USER = 1
    )
})
```

Since `0 !== 1`, the `authUser` check failed and the user was redirected to login.

## Fix

Changed `middleware/main.py` line 66:

```python
# Before (wrong)
claims = {
    "type": 0,  # AuthTypeUser  <-- WRONG!
    ...
}

# After (correct)
claims = {
    "type": 1,  # AuthTypeUser (0=Unknown, 1=User, 2=LinkShare)
    ...
}
```

Also updated the test in `tests/test_oidc_callback.py` to verify `type == 1`.

## Files Changed

- `/home/ivanadamin/projects/factumerit/vikunja-factumerit/middleware/main.py`
- `/home/ivanadamin/projects/factumerit/vikunja-factumerit/tests/test_oidc_callback.py`

## Verification

All 19 tests pass:
```
uv run pytest tests/test_oidc_callback.py -v
# ======================= 19 passed, 14 warnings in 1.14s ========================
```

## Deployment

The fix was pushed to `main` branch. Render auto-deploys from main, so the fix should be live within a few minutes.

## Lesson Learned

When mimicking another system's JWT format, always verify the exact enum values from the source code, not from comments that might be wrong. The comment `# AuthTypeUser` was misleading because the actual value was wrong.

---

## Related Docs

- `vikunja-factumerit/middleware/OIDC_MIDDLEWARE_EXPLAINER.md` - Full middleware architecture
- `docs/FACTUMERIT_EPIC_JOURNEY.md` - Historical context (Act X: The OIDC Puzzle)
- Vikunja source: `pkg/modules/auth/auth.go` - Authoritative auth type constants

