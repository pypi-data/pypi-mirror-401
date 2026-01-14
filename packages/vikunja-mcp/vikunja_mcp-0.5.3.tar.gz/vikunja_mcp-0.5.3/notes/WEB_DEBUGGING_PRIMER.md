# Web Debugging Primer

**For developers new to DevTools, JWTs, and service workers.**  
*Written after debugging avatar caching issues - January 2026*

---

## JWT (JSON Web Token)

**What it is:** A signed "ticket" that proves you're logged in. The server creates it, you store it, and send it with every request.

**Structure:** Three parts separated by dots:
```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Iml2YW4ifQ.signature
│                      │                              │
└─ Header (algorithm)  └─ Payload (your data)         └─ Signature (proof)
```

**How to decode:** Paste into [jwt.io](https://jwt.io) - shows the payload (username, email, expiry, etc.)

**Where it lives:** Usually in `localStorage` or cookies. Check DevTools → Application → Local Storage.

**Why it matters:** If the JWT has wrong data (like old username), the app shows wrong things even though the database is correct.

---

## Service Workers

**What it is:** JavaScript that runs in the background, intercepts network requests, and can serve cached responses. Powers offline mode and PWAs.

**The problem:** Service workers can cache aggressively and **ignore cache headers**. Even if the server says "don't cache this", the service worker might serve a stale copy anyway.

**How to check:** DevTools → Network tab. Look for:
- `(from service worker)` = served from cache, didn't hit server
- `200` without that label = actually fetched from server

**How to clear:**
1. DevTools → Application → Service Workers → **Unregister**
2. DevTools → Application → Storage → **Clear site data**
3. Hard refresh: **Ctrl+Shift+R**

**Nuclear option:** Open **Incognito window** (Ctrl+Shift+N) - no service workers, no cache.

---

## DevTools Tabs We Used

### Network Tab
Shows every request the browser makes.
- **Status**: 200 = success, 304 = not modified, 404 = not found
- **Size**: `(from service worker)` or `(disk cache)` = didn't hit server
- **Headers**: Click a request to see request/response headers
- **Filter**: Type "avatar" to find avatar requests

### Application Tab
- **Service Workers**: See registered workers, unregister them
- **Storage**: Clear local storage, session storage, cache storage
- **Local Storage**: Where apps store data (like JWT tokens)
- **Cache Storage**: Where service workers store cached responses

---

## The Caching Layers

When you request an image, it goes through multiple caches:

```
Browser Request
     ↓
[Service Worker Cache] ← Most aggressive, can ignore headers
     ↓
[Browser HTTP Cache] ← Respects cache headers (usually)
     ↓
[CDN Cache (Cloudflare)] ← Check cf-cache-status header
     ↓
[Server]
```

**To bypass all browser caches:** Use `curl` from command line:
```bash
curl -s "https://example.com/avatar.png" -o /tmp/test.png
```

If curl shows correct data but browser doesn't → browser/service worker cache issue.
If curl shows wrong data → server-side issue.

---

## Avatar Debugging Checklist

1. **Check database**: Is `avatar_provider` correct? Is `username` correct?
2. **Check JWT**: Does it have the right username? (jwt.io)
3. **Check Network tab**: Is avatar `(from service worker)` or fresh?
4. **Clear service worker**: Unregister + clear site data
5. **Test incognito**: If still wrong, it's server-side
6. **Test with curl**: Bypasses all browser caching

---

## What Happened With Our "P" Avatar

1. User registers via OIDC → Vikunja creates user with random username (starts with "P")
2. Avatar gets cached somewhere (service worker or server)
3. Spinal tap updates username to "ivanschneider"
4. But cached avatar still shows "P" for old username
5. Even incognito shows "P" → server-side caching issue

**Lesson:** When updating usernames, we need to invalidate avatar caches at every layer.

---

*See also: `OIDC_LOGIN_LOOP_FIX.md`, `middleware/OIDC_MIDDLEWARE_EXPLAINER.md`*

