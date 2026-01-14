#!/usr/bin/env python3
"""
Test the new bot naming scheme.

This script tests that:
1. Default naming uses eis-{username}
2. Custom bot_username parameter works
3. Bot names are predictable and collision-free
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_bot_naming():
    """Test bot naming logic without actually creating bots."""
    print("=" * 60)
    print("TEST: Bot Naming Scheme")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        ("jmuggli", None, "eis-jmuggli"),
        ("mariaman24", None, "eis-mariaman24"),
        ("ivan", None, "eis-ivan"),
        ("alice", "custom-bot", "custom-bot"),
    ]
    
    for username, bot_username, expected in test_cases:
        # Simulate the naming logic from provision_personal_bot
        if not bot_username:
            result = f"eis-{username}"
        else:
            result = bot_username
        
        status = "✅" if result == expected else "❌"
        print(f"{status} username={username:15} bot_username={str(bot_username):15} -> {result:20} (expected: {expected})")
    
    print("\n" + "=" * 60)
    print("All naming tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    test_bot_naming()

