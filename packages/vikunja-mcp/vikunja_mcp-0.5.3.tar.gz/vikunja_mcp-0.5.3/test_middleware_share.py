#!/usr/bin/env python3
"""
Test script for middleware /internal/share-project endpoint.

This tests the database sharing operation directly to isolate the bug.

Usage:
    python test_middleware_share.py <project_id> <user_id> [permission]
    
Example:
    python test_middleware_share.py 123 456 1
"""

import sys
import requests
import os
import json

def test_middleware_share(project_id: int, user_id: int, permission: int = 1, base_url: str = None):
    """Test the middleware share-project endpoint."""
    
    if not base_url:
        base_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    
    url = f"{base_url}/internal/share-project"
    
    payload = {
        "project_id": project_id,
        "user_id": user_id,
        "permission": permission
    }
    
    print(f"Testing middleware /internal/share-project endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("-" * 60)
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
        print("-" * 60)
        
        print("\nResponse:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2))
        except:
            print(response.text)
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! Share operation completed.")
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: {e}")
        return False
    
    return response.status_code == 200


def get_bot_info_for_user(username: str):
    """Helper to get bot info from database for a user."""
    print(f"\n📋 Looking up bot info for user: {username}")
    print("=" * 60)
    
    # This would need database access - for now just show what's needed
    print("To get the required IDs, run this SQL query:")
    print(f"""
    SELECT 
        pb.vikunja_user_id as bot_vikunja_id,
        pb.owner_vikunja_user_id as owner_vikunja_id,
        pb.bot_username
    FROM personal_bots pb
    WHERE pb.user_id = 'vikunja:{username}';
    """)
    print("\nThen get the Inbox project ID from Vikunja API or database.")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_middleware_share.py <project_id> <user_id> [permission]")
        print("\nExample: python test_middleware_share.py 123 456 1")
        print("\nTo find the IDs for a user:")
        print("  python test_middleware_share.py --lookup <username>")
        sys.exit(1)
    
    if sys.argv[1] == "--lookup":
        if len(sys.argv) < 3:
            print("Usage: python test_middleware_share.py --lookup <username>")
            sys.exit(1)
        get_bot_info_for_user(sys.argv[2])
        sys.exit(0)
    
    project_id = int(sys.argv[1])
    user_id = int(sys.argv[2])
    permission = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    
    # Allow optional base URL override
    base_url = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = test_middleware_share(project_id, user_id, permission, base_url)
    sys.exit(0 if success else 1)

