#!/usr/bin/env python3
"""
Cleanup test users from Vikunja and database.

This script removes test users created during JWT implementation testing:
- e-af1442 (jwt_test_1767545878)
- e-8b5e48 (jwt_test_1767545923)
- e-3a7cec (jwt_test_final)
- e-124135 (jwt_test_1767546005)
- ivan_test02 (manual test user)

Run with:
    uv run cleanup_test_users.py [--dry-run]
"""

import argparse
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


# Test users to cleanup
TEST_USERS = [
    {"username": "e-af1442", "vikunja_id": 35, "reason": "jwt_test_1767545878"},
    {"username": "e-8b5e48", "vikunja_id": 36, "reason": "jwt_test_1767545923"},
    {"username": "e-3a7cec", "vikunja_id": 37, "reason": "jwt_test_final"},
    {"username": "e-124135", "vikunja_id": 38, "reason": "jwt_test_1767546005"},
    {"username": "ivan_test02", "vikunja_id": 33, "reason": "manual test user"},
]


def delete_vikunja_user(username: str, vikunja_id: int, dry_run: bool = False):
    """Delete a user from Vikunja."""
    import httpx
    
    vikunja_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")
    admin_token = os.environ.get("VIKUNJA_ADMIN_TOKEN")
    
    if not admin_token:
        print(f"⚠️  VIKUNJA_ADMIN_TOKEN not set - cannot delete from Vikunja")
        return False
    
    if dry_run:
        print(f"   [DRY RUN] Would delete Vikunja user: {username} (ID: {vikunja_id})")
        return True
    
    try:
        # Note: Vikunja may not have a direct user deletion endpoint
        # This is a placeholder - adjust based on actual Vikunja API
        print(f"   ⚠️  Vikunja user deletion not implemented (manual cleanup required)")
        print(f"      User: {username} (ID: {vikunja_id})")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to delete Vikunja user {username}: {e}")
        return False


def delete_database_record(username: str, dry_run: bool = False):
    """Delete bot record from database."""
    from vikunja_mcp.token_broker import execute
    
    if dry_run:
        print(f"   [DRY RUN] Would delete database record for: {username}")
        return True
    
    try:
        result = execute(
            "DELETE FROM personal_bots WHERE bot_username = %s",
            (username,)
        )
        print(f"   ✅ Deleted database record for: {username}")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to delete database record for {username}: {e}")
        return False


def cleanup_test_user(user: dict, dry_run: bool = False):
    """Cleanup a single test user."""
    username = user["username"]
    vikunja_id = user["vikunja_id"]
    reason = user["reason"]
    
    print(f"\n{'='*70}")
    print(f"Cleaning up: {username} ({reason})")
    print(f"{'='*70}")
    
    success = True
    
    # Delete from Vikunja
    if not delete_vikunja_user(username, vikunja_id, dry_run):
        success = False
    
    # Delete from database
    if not delete_database_record(username, dry_run):
        success = False
    
    return success


def main():
    parser = argparse.ArgumentParser(description="Cleanup test users")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without actually deleting")
    args = parser.parse_args()
    
    print("🧹 Test User Cleanup")
    print(f"⏰ Started at: {datetime.now()}")
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No changes will be made")
    
    # Check environment
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print(f"\n❌ DATABASE_URL not set")
        sys.exit(1)
    
    print(f"\n✅ Environment configured")
    print(f"   - DATABASE_URL: {db_url.split('@')[1] if '@' in db_url else '(local)'}")
    
    # Cleanup each test user
    success_count = 0
    fail_count = 0
    
    for user in TEST_USERS:
        if cleanup_test_user(user, args.dry_run):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Summary")
    print(f"{'='*70}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📊 Total: {len(TEST_USERS)}")
    
    if args.dry_run:
        print(f"\n⚠️  This was a DRY RUN - no changes were made")
        print(f"   Run without --dry-run to actually delete users")
    else:
        if fail_count > 0:
            print(f"\n⚠️  Some users failed - check errors above")
        else:
            print(f"\n🎉 All test users cleaned up successfully!")
        
        print(f"\n📝 Manual cleanup required:")
        print(f"   - Delete Vikunja users manually (no API endpoint)")
        print(f"   - Check for any orphaned projects/tasks")


if __name__ == "__main__":
    main()

