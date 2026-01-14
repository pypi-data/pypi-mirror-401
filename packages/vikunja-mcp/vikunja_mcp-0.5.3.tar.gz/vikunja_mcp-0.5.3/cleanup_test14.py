#!/usr/bin/env python3
"""
Clean up test14 user so they can retry signup after deployment.

This removes the token usage record and factumerit_users entry,
allowing the user to sign up again with the same email.

Run with:
    uv run cleanup_test14.py
"""

import sys
import os
import psycopg

def cleanup_test_user(email, code, user_id):
    """Clean up a test user so they can retry signup."""

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)

    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    try:
        # 1. Clear token usage
        cur.execute(
            "UPDATE beta_signup_tokens SET used_at = NULL WHERE registration_code = %s AND email = %s",
            (code, email)
        )
        print(f"✓ Cleared token usage for {email}")
        
        # 2. Delete from factumerit_users (this will cascade to bot_credentials)
        cur.execute(
            "DELETE FROM factumerit_users WHERE user_id = %s",
            (user_id,)
        )
        print(f"✓ Deleted factumerit_users entry for {user_id}")
        
        conn.commit()
        print(f"\n✅ Cleanup complete! {email} can now retry signup.")
        print(f"\nNote: The Vikunja user 'ivan_test14' still exists in Vikunja.")
        print(f"If you want to use the same email, you'll need to delete it from Vikunja too.")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    # Clean up test14 and test15
    cleanup_test_user(
        email="ivan+test14@ivantohelpyou.com",
        code="BETA-VHDL-2026",
        user_id="vikunja:ivan_test14"
    )
    cleanup_test_user(
        email="ivan+test15@ivantohelpyou.com",
        code="BETA-VHDL-2026",
        user_id="vikunja:ivan_test15"
    )

