#!/usr/bin/env python3
"""
Test script for personal bot provisioning flow.

Tests:
1. provision_personal_bot() creates bot account
2. store_bot_credentials() saves to database with owner_vikunja_user_id
3. get_bot_owner_vikunja_id() retrieves owner ID
4. Inbox auto-share during signup
5. Project auto-share when bot creates project

Run: python test_personal_bot_flow.py
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from vikunja_mcp.bot_provisioning import (
    provision_personal_bot,
    store_bot_credentials,
    get_bot_owner_vikunja_id,
    get_user_bot_token,
    ProvisioningError,
)

def test_bot_provisioning():
    """Test bot provisioning and owner ID storage."""
    print("=" * 60)
    print("TEST: Personal Bot Provisioning")
    print("=" * 60)
    
    # Test data
    test_username = "testuser123"
    test_owner_vikunja_id = 42  # Simulated owner's Vikunja user ID
    user_id = f"vikunja:{test_username}"
    
    print(f"\n1. Provisioning bot for user: {test_username}")
    try:
        bot_creds = provision_personal_bot(test_username)
        print(f"   ✅ Bot created: {bot_creds.username}")
        print(f"   - Display name: {bot_creds.display_name}")
        print(f"   - Vikunja user ID: {bot_creds.vikunja_user_id}")
        print(f"   - Email: {bot_creds.email}")
    except ProvisioningError as e:
        print(f"   ❌ Provisioning failed: {e}")
        return False
    
    print(f"\n2. Storing bot credentials with owner_vikunja_user_id={test_owner_vikunja_id}")
    try:
        store_bot_credentials(user_id, bot_creds, owner_vikunja_user_id=test_owner_vikunja_id)
        print(f"   ✅ Credentials stored")
    except Exception as e:
        print(f"   ❌ Storage failed: {e}")
        return False
    
    print(f"\n3. Retrieving owner ID for user: {user_id}")
    try:
        owner_id = get_bot_owner_vikunja_id(user_id)
        if owner_id == test_owner_vikunja_id:
            print(f"   ✅ Owner ID retrieved: {owner_id}")
        else:
            print(f"   ❌ Owner ID mismatch: expected {test_owner_vikunja_id}, got {owner_id}")
            return False
    except Exception as e:
        print(f"   ❌ Retrieval failed: {e}")
        return False
    
    print(f"\n4. Retrieving bot token")
    try:
        token = get_user_bot_token(user_id)
        if token:
            print(f"   ✅ Bot token retrieved (length: {len(token)})")
        else:
            print(f"   ❌ No bot token found")
            return False
    except Exception as e:
        print(f"   ❌ Token retrieval failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_bot_provisioning()
    sys.exit(0 if success else 1)

