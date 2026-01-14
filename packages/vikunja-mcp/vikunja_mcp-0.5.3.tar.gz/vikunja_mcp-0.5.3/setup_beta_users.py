#!/usr/bin/env python3
"""
Setup personal bots for beta users.

This script provisions personal bots for the beta users:
- @ivan
- (other beta users to be added)

Run with:
    uv run setup_beta_users.py
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vikunja_mcp.bot_provisioning import provision_personal_bot, store_bot_credentials


# Beta users to provision
BETA_USERS = [
    {
        "username": "ivan",
        "user_id": "vikunja:ivan",  # Adjust based on your user ID format
        "display_name": "eis",
    },
    # Add other beta users here
    # {
    #     "username": "alice",
    #     "user_id": "vikunja:alice",
    #     "display_name": "eis",
    # },
]


def setup_beta_user(username: str, user_id: str, display_name: str):
    """Provision a personal bot for a beta user."""
    print(f"\n{'='*70}")
    print(f"Setting up bot for: {username}")
    print(f"{'='*70}")
    
    try:
        # Check if user already has a bot
        from vikunja_mcp.bot_provisioning import get_user_bot_credentials
        existing = get_user_bot_credentials(user_id)
        
        if existing:
            bot_username, _ = existing
            print(f"⚠️  User {username} already has a bot: {bot_username}")
            print(f"   Skipping provisioning")
            return True
        
        # Provision new bot
        print(f"📝 Provisioning personal bot for {username}...")
        credentials = provision_personal_bot(username, display_name=display_name)
        
        print(f"✅ Bot provisioned successfully!")
        print(f"   - Bot Username: {credentials.username}")
        print(f"   - Vikunja ID: {credentials.vikunja_user_id}")
        print(f"   - Display Name: {credentials.display_name}")
        
        # Store credentials in database
        print(f"💾 Storing bot credentials in database...")
        store_bot_credentials(user_id, credentials)
        print(f"✅ Credentials stored successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to setup bot for {username}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("🤖 Beta User Bot Provisioning")
    print(f"⏰ Started at: {datetime.now()}")
    
    # Check environment
    required_env = ["DATABASE_URL", "VIKUNJA_URL", "VIKUNJA_ADMIN_TOKEN", "TOKEN_ENCRYPTION_KEY"]
    missing = [var for var in required_env if not os.environ.get(var)]
    if missing:
        print(f"\n❌ Missing environment variables: {', '.join(missing)}")
        print("\nPlease set:")
        for var in missing:
            print(f"  export {var}=\"...\"")
        sys.exit(1)
    
    print(f"\n✅ Environment configured")
    print(f"   - VIKUNJA_URL: {os.environ['VIKUNJA_URL']}")
    print(f"   - DATABASE_URL: {os.environ['DATABASE_URL'].split('@')[1] if '@' in os.environ['DATABASE_URL'] else '(local)'}")
    
    # Provision bots for each beta user
    success_count = 0
    fail_count = 0
    
    for user in BETA_USERS:
        if setup_beta_user(user["username"], user["user_id"], user["display_name"]):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Summary")
    print(f"{'='*70}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📊 Total: {len(BETA_USERS)}")
    
    if fail_count > 0:
        print(f"\n⚠️  Some users failed - check errors above")
        sys.exit(1)
    else:
        print(f"\n🎉 All beta users provisioned successfully!")


if __name__ == "__main__":
    main()

