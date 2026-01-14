#!/usr/bin/env python3
"""
One-time script to update the password for vikunja:ivan's bot (eis).

This script will be run on the Render server where TOKEN_ENCRYPTION_KEY is available.
"""
import sys
import os

# Add src to path so we can import from vikunja_mcp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def update_bot_password(user_id: str, password: str):
    """Update the encrypted password for a bot."""
    # Import here to avoid module loading issues
    from vikunja_mcp.token_broker import encrypt_token, execute

    encrypted_password = encrypt_token(password)

    execute(
        """
        UPDATE personal_bots
        SET encrypted_password = %s
        WHERE user_id = %s
        """,
        (encrypted_password, user_id),
    )

    print(f"✅ Updated password for {user_id}")

if __name__ == "__main__":
    # Update password for vikunja:ivan's bot
    update_bot_password("vikunja:ivan", "AVrYTecGag7hXwl5CgI3")
    print("Done!")

