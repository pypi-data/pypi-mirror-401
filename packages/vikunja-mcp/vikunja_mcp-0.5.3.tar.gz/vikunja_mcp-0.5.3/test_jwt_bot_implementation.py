#!/usr/bin/env python3
"""
Test JWT-based bot authentication implementation.

This script tests the complete JWT workaround for broken API tokens:
1. Bot provisioning with password storage
2. JWT token caching and refresh
3. BotVikunjaClient using JWT authentication

Run with:
    python3 test_jwt_bot_implementation.py --username test_user --password <password>

Prerequisites:
    - DATABASE_URL environment variable set
    - VIKUNJA_URL environment variable set
    - VIKUNJA_ADMIN_TOKEN environment variable set (for registration)
    - Database migration 015 applied
"""

import argparse
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vikunja_mcp.bot_provisioning import (
    provision_personal_bot,
    store_bot_credentials,
    get_user_bot_credentials,
)
from vikunja_mcp.bot_jwt_manager import get_bot_jwt, get_cache_stats, clear_bot_jwt_cache
from vikunja_mcp.vikunja_client import BotVikunjaClient


def test_bot_provisioning(username: str):
    """Test 1: Provision a bot and store credentials."""
    print("\n" + "="*70)
    print("TEST 1: Bot Provisioning")
    print("="*70)
    
    user_id = f"vikunja:{username}"
    
    try:
        print(f"📝 Provisioning bot for user: {user_id}")
        credentials = provision_personal_bot(username, display_name="test-bot")
        
        print(f"✅ Bot provisioned successfully!")
        print(f"   - Username: {credentials.username}")
        print(f"   - Vikunja ID: {credentials.vikunja_user_id}")
        print(f"   - Display Name: {credentials.display_name}")
        print(f"   - Has Password: {bool(credentials.password)}")
        
        print(f"\n💾 Storing bot credentials in database...")
        store_bot_credentials(user_id, credentials)
        print(f"✅ Credentials stored successfully!")
        
        return credentials
        
    except Exception as e:
        print(f"❌ Bot provisioning failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_jwt_authentication(username: str, credentials):
    """Test 2: JWT token retrieval and caching."""
    print("\n" + "="*70)
    print("TEST 2: JWT Authentication")
    print("="*70)
    
    user_id = f"vikunja:{username}"
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    
    try:
        # Retrieve credentials from database
        print(f"🔍 Retrieving bot credentials from database...")
        bot_creds = get_user_bot_credentials(user_id)
        
        if not bot_creds:
            print(f"❌ No credentials found in database")
            return False
        
        bot_username, bot_password = bot_creds
        print(f"✅ Retrieved credentials for: {bot_username}")
        
        # Get JWT token (first time - should login)
        print(f"\n🔑 Getting JWT token (first time)...")
        jwt_token = get_bot_jwt(bot_username, bot_password, vikunja_url)
        print(f"✅ JWT token obtained: {jwt_token[:30]}...")
        
        # Get JWT token (second time - should use cache)
        print(f"\n🔑 Getting JWT token (second time - should use cache)...")
        jwt_token2 = get_bot_jwt(bot_username, bot_password, vikunja_url)
        print(f"✅ JWT token obtained: {jwt_token2[:30]}...")
        
        if jwt_token == jwt_token2:
            print(f"✅ Cache working! Same token returned")
        else:
            print(f"⚠️  Different tokens - cache may not be working")
        
        # Check cache stats
        print(f"\n📊 Cache statistics:")
        stats = get_cache_stats()
        print(f"   - Total cached: {stats['total_cached']}")
        print(f"   - Valid tokens: {stats['valid_tokens']}")
        print(f"   - Expired tokens: {stats['expired_tokens']}")
        
        return True
        
    except Exception as e:
        print(f"❌ JWT authentication failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bot_client(username: str):
    """Test 3: BotVikunjaClient with JWT authentication."""
    print("\n" + "="*70)
    print("TEST 3: BotVikunjaClient Operations")
    print("="*70)
    
    user_id = f"vikunja:{username}"
    
    try:
        print(f"🤖 Creating BotVikunjaClient for user: {user_id}")
        client = BotVikunjaClient(user_id=user_id)
        print(f"✅ Client created successfully!")
        
        # Test API call - get user info
        print(f"\n📡 Testing API call: GET /api/v1/user")
        user_info = client.get_bot_user()
        print(f"✅ API call successful!")
        print(f"   - Bot username: {user_info.get('username')}")
        print(f"   - Bot ID: {user_info.get('id')}")
        print(f"   - Bot name: {user_info.get('name')}")
        
        # Test getting projects
        print(f"\n📡 Testing API call: GET /api/v1/projects")
        projects = client.get_projects()
        print(f"✅ API call successful!")
        print(f"   - Projects found: {len(projects)}")
        
        return True
        
    except Exception as e:
        print(f"❌ BotVikunjaClient test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Test JWT bot implementation")
    parser.add_argument("--username", required=True, help="Test username")
    args = parser.parse_args()
    
    print("🧪 JWT Bot Implementation Test Suite")
    print(f"⏰ Started at: {datetime.now()}")
    
    # Check environment
    required_env = ["DATABASE_URL", "VIKUNJA_URL"]
    missing = [var for var in required_env if not os.environ.get(var)]
    if missing:
        print(f"\n❌ Missing environment variables: {', '.join(missing)}")
        print("Please set these variables and try again.")
        sys.exit(1)
    
    # Run tests
    credentials = test_bot_provisioning(args.username)
    if not credentials:
        print("\n❌ Bot provisioning failed - stopping tests")
        sys.exit(1)
    
    if not test_jwt_authentication(args.username, credentials):
        print("\n❌ JWT authentication failed - stopping tests")
        sys.exit(1)
    
    if not test_bot_client(args.username):
        print("\n❌ BotVikunjaClient test failed")
        sys.exit(1)
    
    # All tests passed!
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n🎉 JWT bot implementation is working correctly!")
    print("\nNext steps:")
    print("1. Apply migration: psql $DATABASE_URL -f migrations/015_personal_bots_password.sql")
    print("2. Update existing bots to use JWT (re-provision or migrate)")
    print("3. Monitor JWT cache performance in production")


if __name__ == "__main__":
    main()

