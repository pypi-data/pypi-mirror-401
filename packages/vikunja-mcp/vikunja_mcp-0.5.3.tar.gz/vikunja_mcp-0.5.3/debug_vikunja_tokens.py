#!/usr/bin/env python3
"""
Debug Vikunja API Token System

This script investigates how Vikunja's API token system works internally
by testing different token creation and validation scenarios.

Based on: spawn/spawn-solutions/docs/factumerit/097-TOKEN_CREATION_ROOT_CAUSE_INVESTIGATION.md

Issues discovered:
1. API tokens created via UI return 401 Unauthorized
2. API tokens created via API return "Invalid Data"
3. JWT tokens work correctly

This script will:
1. Test token creation with different payloads
2. Examine token format and structure
3. Test token validation
4. Check database state
"""

import argparse
import json
import os
import requests
from datetime import datetime, timedelta

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")


def test_jwt_login(username: str, password: str):
    """Test JWT authentication (known to work)."""
    print("\n" + "="*60)
    print("TEST 1: JWT Authentication (Baseline)")
    print("="*60)
    
    resp = requests.post(
        f"{VIKUNJA_URL}/api/v1/login",
        headers={"Accept": "application/json"},
        json={"username": username, "password": password},
        timeout=10
    )
    
    if resp.status_code == 200:
        data = resp.json()
        jwt_token = data.get("token")
        user_id = data.get("id")
        print(f"✅ JWT Login successful")
        print(f"   User ID: {user_id}")
        print(f"   JWT Token (first 50 chars): {jwt_token[:50]}...")
        print(f"   JWT Token length: {len(jwt_token)}")
        return jwt_token, user_id
    else:
        print(f"❌ JWT Login failed: {resp.status_code}")
        print(f"   Response: {resp.text}")
        return None, None


def test_token_creation_minimal(jwt_token: str):
    """Test API token creation with minimal payload (just title)."""
    print("\n" + "="*60)
    print("TEST 2: Token Creation - Minimal Payload")
    print("="*60)
    
    payload = {"title": "Debug Token - Minimal"}
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    resp = requests.put(
        f"{VIKUNJA_URL}/api/v1/tokens",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    if resp.status_code == 200:
        data = resp.json()
        token = data.get("token")
        print(f"✅ Token created: {token[:20]}... (length: {len(token)})")
        return token
    else:
        print(f"❌ Token creation failed")
        return None


def test_token_creation_with_permissions(jwt_token: str):
    """Test API token creation with empty permissions dict."""
    print("\n" + "="*60)
    print("TEST 3: Token Creation - With Empty Permissions")
    print("="*60)
    
    payload = {
        "title": "Debug Token - Empty Permissions",
        "permissions": {}
    }
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    resp = requests.put(
        f"{VIKUNJA_URL}/api/v1/tokens",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    if resp.status_code == 200:
        data = resp.json()
        token = data.get("token")
        print(f"✅ Token created: {token[:20]}... (length: {len(token)})")
        return token
    else:
        print(f"❌ Token creation failed")
        return None


def test_token_creation_with_expiry(jwt_token: str):
    """Test API token creation with expiry date."""
    print("\n" + "="*60)
    print("TEST 4: Token Creation - With Expiry")
    print("="*60)

    expiry = datetime.utcnow() + timedelta(days=365)
    payload = {
        "title": "Debug Token - With Expiry",
        "expires_at": expiry.isoformat() + "Z"
    }
    print(f"Payload: {json.dumps(payload, indent=2)}")

    resp = requests.put(
        f"{VIKUNJA_URL}/api/v1/tokens",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )

    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

    if resp.status_code == 200:
        data = resp.json()
        token = data.get("token")
        print(f"✅ Token created: {token[:20]}... (length: {len(token)})")
        return token
    else:
        print(f"❌ Token creation failed")
        return None


def test_get_routes(jwt_token: str):
    """Fetch available routes/permissions (like the HTML connect flow does)."""
    print("\n" + "="*60)
    print("TEST 5: Fetch Available Routes/Permissions")
    print("="*60)

    resp = requests.get(
        f"{VIKUNJA_URL}/api/v1/routes",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json"
        },
        timeout=10
    )

    print(f"Status: {resp.status_code}")

    if resp.status_code == 200:
        routes = resp.json()
        print(f"✅ Routes fetched successfully")
        print(f"   Route groups: {list(routes.keys())}")
        return routes
    else:
        print(f"❌ Failed to fetch routes: {resp.text}")
        return None


def test_token_creation_with_full_permissions(jwt_token: str, routes: dict):
    """Test API token creation with full permissions (like HTML connect flow)."""
    print("\n" + "="*60)
    print("TEST 6: Token Creation - Full Permissions (Like UI)")
    print("="*60)

    # Build permissions dict from routes
    permissions = {}
    if routes:
        for group, group_routes in routes.items():
            permissions[group] = list(group_routes.keys())

    expiry = datetime.utcnow() + timedelta(days=365)
    payload = {
        "title": "Debug Token - Full Permissions",
        "expires_at": expiry.isoformat() + "Z",
        "permissions": permissions
    }

    print(f"Payload (permissions truncated):")
    print(f"  title: {payload['title']}")
    print(f"  expires_at: {payload['expires_at']}")
    print(f"  permissions groups: {list(permissions.keys())}")

    resp = requests.put(
        f"{VIKUNJA_URL}/api/v1/tokens",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )

    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

    if resp.status_code == 200:
        data = resp.json()
        token = data.get("token")
        print(f"✅ Token created: {token[:20]}... (length: {len(token)})")
        return token
    else:
        print(f"❌ Token creation failed")
        return None


def test_token_usage(api_token: str, token_name: str):
    """Test using an API token to make authenticated requests."""
    print(f"\n{'='*60}")
    print(f"TEST: Using {token_name}")
    print("="*60)
    
    resp = requests.get(
        f"{VIKUNJA_URL}/api/v1/user",
        headers={
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json"
        },
        timeout=10
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:200]}")
    
    if resp.status_code == 200:
        print(f"✅ Token works!")
        return True
    else:
        print(f"❌ Token doesn't work")
        return False


def main():
    parser = argparse.ArgumentParser(description="Debug Vikunja API token system")
    parser.add_argument("--username", required=True, help="Vikunja username")
    parser.add_argument("--password", required=True, help="Vikunja password")
    parser.add_argument("--manual-token", help="Manually created token to test")
    
    args = parser.parse_args()
    
    print("Vikunja API Token Debugging Tool")
    print(f"Target: {VIKUNJA_URL}")
    print(f"User: {args.username}")
    
    # Test 1: JWT login (baseline)
    jwt_token, user_id = test_jwt_login(args.username, args.password)
    if not jwt_token:
        print("\n❌ Cannot proceed without JWT token")
        return 1
    
    # Test 2-4: Try different token creation payloads
    token_minimal = test_token_creation_minimal(jwt_token)
    token_permissions = test_token_creation_with_permissions(jwt_token)
    token_expiry = test_token_creation_with_expiry(jwt_token)

    # Test 5-6: Fetch routes and create token with full permissions
    routes = test_get_routes(jwt_token)
    token_full_perms = test_token_creation_with_full_permissions(jwt_token, routes)

    # Test token usage
    print("\n" + "="*60)
    print("TOKEN USAGE TESTS")
    print("="*60)

    # Test JWT token (should work)
    test_token_usage(jwt_token, "JWT Token")

    # Test created tokens
    if token_minimal:
        test_token_usage(token_minimal, "Minimal Token")
    if token_permissions:
        test_token_usage(token_permissions, "Permissions Token")
    if token_expiry:
        test_token_usage(token_expiry, "Expiry Token")
    if token_full_perms:
        test_token_usage(token_full_perms, "Full Permissions Token")
    
    # Test manually created token if provided
    if args.manual_token:
        test_token_usage(args.manual_token, "Manual Token (from UI)")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("Check the results above to identify:")
    print("1. Which token creation payloads work")
    print("2. Which created tokens can be used for API calls")
    print("3. Differences between working and non-working tokens")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

