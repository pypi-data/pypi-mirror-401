#!/usr/bin/env python3
"""
Test Vikunja HTML Connect Flow

This script replicates the exact token creation flow used by the HTML
connect pages (connect.html, matrix-connect.html) to see if that approach works.

The HTML flow:
1. User logs in → get JWT token
2. Fetch /api/v1/routes → get available permissions
3. Build permissions object from routes
4. Create token with full permissions + expiry

If this works, we know the issue is with our payload, not with Vikunja itself.
"""

import argparse
import json
import os
import requests
from datetime import datetime, timedelta, timezone

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")


def login(username: str, password: str):
    """Step 1: Login to get JWT token."""
    print("Step 1: Login to get JWT token")
    print("-" * 40)
    
    resp = requests.post(
        f"{VIKUNJA_URL}/api/v1/login",
        headers={"Accept": "application/json"},
        json={"username": username, "password": password},
        timeout=10
    )
    
    if resp.status_code != 200:
        print(f"❌ Login failed: {resp.status_code}")
        print(resp.text)
        return None, None
    
    data = resp.json()
    jwt_token = data.get("token")
    user_id = data.get("id")
    
    print(f"✅ Login successful")
    print(f"   User ID: {user_id}")
    print(f"   JWT Token: {jwt_token[:50]}...")
    print()
    
    return jwt_token, user_id


def fetch_routes(jwt_token: str):
    """Step 2: Fetch available routes/permissions."""
    print("Step 2: Fetch available routes/permissions")
    print("-" * 40)
    
    resp = requests.get(
        f"{VIKUNJA_URL}/api/v1/routes",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/json"
        },
        timeout=10
    )
    
    if resp.status_code != 200:
        print(f"❌ Failed to fetch routes: {resp.status_code}")
        print(resp.text)
        return None
    
    routes = resp.json()
    print(f"✅ Routes fetched successfully")
    print(f"   Route groups: {list(routes.keys())}")
    print(f"   Total groups: {len(routes)}")
    print()
    
    return routes


def build_permissions(routes: dict):
    """Step 3: Build permissions object from routes (like HTML does)."""
    print("Step 3: Build permissions object")
    print("-" * 40)
    
    permissions = {}
    for group, group_routes in routes.items():
        permissions[group] = list(group_routes.keys())
    
    print(f"✅ Permissions built")
    print(f"   Groups: {len(permissions)}")
    for group, perms in list(permissions.items())[:5]:  # Show first 5
        print(f"   {group}: {perms}")
    if len(permissions) > 5:
        print(f"   ... and {len(permissions) - 5} more groups")
    print()
    
    return permissions


def create_token(jwt_token: str, permissions: dict, title: str = "HTML Connect Flow Test"):
    """Step 4: Create API token with full permissions (like HTML does)."""
    print("Step 4: Create API token")
    print("-" * 40)
    
    # Expiry date (365 days from now, like HTML)
    expiry = datetime.now(timezone.utc) + timedelta(days=365)
    # Format as ISO string with Z suffix (replace +00:00 with Z)
    expiry_str = expiry.isoformat().replace('+00:00', 'Z')

    payload = {
        "title": title,
        "expires_at": expiry_str,
        "permissions": permissions
    }
    
    print(f"Payload:")
    print(f"  title: {payload['title']}")
    print(f"  expires_at: {payload['expires_at']}")
    print(f"  permissions: {len(permissions)} groups")
    print()
    
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
    
    print(f"Response Status: {resp.status_code}")

    if resp.status_code in [200, 201]:  # Accept both 200 OK and 201 Created
        data = resp.json()
        token = data.get("token")
        print(f"✅ Token created successfully!")
        print(f"   Token: {token}")
        print(f"   Length: {len(token)}")
        print(f"   Prefix: {token[:3]}")
        print()
        return token
    else:
        print(f"❌ Token creation failed")
        print(f"   Response: {resp.text}")
        print()
        return None


def test_token(api_token: str):
    """Step 5: Test the created token."""
    print("Step 5: Test the created token")
    print("-" * 40)
    
    resp = requests.get(
        f"{VIKUNJA_URL}/api/v1/user",
        headers={
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json"
        },
        timeout=10
    )
    
    print(f"Response Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Token works!")
        print(f"   User: {data.get('username')}")
        print(f"   Email: {data.get('email')}")
        print()
        return True
    else:
        print(f"❌ Token doesn't work")
        print(f"   Response: {resp.text}")
        print()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test Vikunja HTML connect flow for token creation"
    )
    parser.add_argument("--username", required=True, help="Vikunja username")
    parser.add_argument("--password", required=True, help="Vikunja password")
    parser.add_argument("--title", default="HTML Connect Flow Test", help="Token title")
    
    args = parser.parse_args()
    
    print("="*60)
    print("Vikunja HTML Connect Flow Test")
    print("="*60)
    print(f"Target: {VIKUNJA_URL}")
    print(f"User: {args.username}")
    print()
    
    # Step 1: Login
    jwt_token, user_id = login(args.username, args.password)
    if not jwt_token:
        return 1
    
    # Step 2: Fetch routes
    routes = fetch_routes(jwt_token)
    if not routes:
        return 1
    
    # Step 3: Build permissions
    permissions = build_permissions(routes)
    
    # Step 4: Create token
    api_token = create_token(jwt_token, permissions, args.title)
    if not api_token:
        return 1
    
    # Step 5: Test token
    works = test_token(api_token)
    
    print("="*60)
    print("RESULT")
    print("="*60)
    if works:
        print("✅ SUCCESS: HTML connect flow works!")
        print(f"   Token: {api_token}")
        print()
        print("This means:")
        print("  1. Token creation API works when done correctly")
        print("  2. Our bot provisioning needs to use this exact flow")
        print("  3. The issue is with our payload, not Vikunja")
    else:
        print("❌ FAILURE: HTML connect flow doesn't work")
        print()
        print("This means:")
        print("  1. Token creation might be broken in Vikunja")
        print("  2. OR there's a version/config issue")
        print("  3. Need to investigate Vikunja setup")
    print("="*60)
    
    return 0 if works else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

