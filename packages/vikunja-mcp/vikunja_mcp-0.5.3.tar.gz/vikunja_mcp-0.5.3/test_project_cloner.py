#!/usr/bin/env python3
"""
Test script for project cloner.

Tests the bot→user project cloning flow without needing full MCP setup.

Usage:
    python test_project_cloner.py
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from vikunja_mcp.project_cloner import clone_project_to_user


def test_clone():
    """Test cloning a project from bot to user."""
    
    # Configuration
    bot_token = os.environ.get("VIKUNJA_BOT_TOKEN")
    user_token = os.environ.get("VIKUNJA_USER_TOKEN")  # User's JWT token
    bot_project_id = int(os.environ.get("TEST_PROJECT_ID", "0"))
    
    if not bot_token:
        print("❌ VIKUNJA_BOT_TOKEN not set")
        return False
    
    if not user_token:
        print("❌ VIKUNJA_USER_TOKEN not set")
        print("   Get your JWT token from Vikunja UI:")
        print("   1. Open browser DevTools (F12)")
        print("   2. Go to Application → Local Storage → vikunja.factumerit.app")
        print("   3. Copy the 'token' value")
        return False
    
    if not bot_project_id:
        print("❌ TEST_PROJECT_ID not set")
        print("   Create a test project in bot's account and set its ID")
        return False
    
    print(f"🧪 Testing project clone: bot#{bot_project_id} → user")
    print(f"   Bot token: {bot_token[:20]}...")
    print(f"   User token: {user_token[:20]}...")
    
    # Run clone
    result = clone_project_to_user(
        bot_project_id=bot_project_id,
        target_user_token=user_token,
        bot_token=bot_token,
        parent_project_id=None,  # Create at root level
        delete_original=False,  # Keep bot's copy for testing
    )
    
    if result["success"]:
        print(f"✅ Clone successful!")
        print(f"   User project ID: {result['user_project_id']}")
        print(f"\n   📊 Cloning Statistics:")
        print(f"      Tasks: {result['cloned_tasks']}")
        print(f"      Task relationships: {result['cloned_relations']}")
        print(f"      Task assignees: {result['cloned_assignees']}")
        print(f"      Task comments: {result['cloned_comments']}")
        print(f"      Task attachments: {result['cloned_attachments']}")
        print(f"      Views: {result['cloned_views']}")
        print(f"      Buckets: {result['cloned_buckets']}")
        print(f"      Bucket assignments: {result['bucket_assignments']}")
        print(f"\n   🔗 Check: https://vikunja.factumerit.app/projects/{result['user_project_id']}")
        return True
    else:
        print(f"❌ Clone failed: {result.get('error')}")
        return False


if __name__ == "__main__":
    success = test_clone()
    sys.exit(0 if success else 1)

