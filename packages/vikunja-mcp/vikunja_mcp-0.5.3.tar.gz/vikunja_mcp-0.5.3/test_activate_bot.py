#!/usr/bin/env python3
"""
Test script for activate-bot endpoint smoke test.

Usage:
    python test_activate_bot.py <username>
    
Example:
    python test_activate_bot.py testuser
"""

import sys
import requests
import os

def test_activate_bot(username: str, base_url: str = None):
    """Test the activate-bot endpoint with a username."""
    
    if not base_url:
        base_url = os.environ.get("MCP_BASE_URL", "http://localhost:8000")
    
    url = f"{base_url}/activate-bot?user={username}"
    
    print(f"Testing activate-bot endpoint...")
    print(f"URL: {url}")
    print(f"Username: {username}")
    print("-" * 60)
    
    try:
        response = requests.get(url, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
        print("-" * 60)
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! Smoke test passed.")
            print("\nResponse preview:")
            print(response.text[:500])
            
            # Save full HTML to file for inspection
            output_file = f"activate_bot_response_{username}.html"
            with open(output_file, 'w') as f:
                f.write(response.text)
            print(f"\nFull response saved to: {output_file}")
            
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            print("\nResponse:")
            print(response.text[:1000])
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: {e}")
        return False
    
    return response.status_code == 200


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_activate_bot.py <username>")
        print("\nExample: python test_activate_bot.py testuser")
        sys.exit(1)
    
    username = sys.argv[1]
    
    # Allow optional base URL override
    base_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = test_activate_bot(username, base_url)
    sys.exit(0 if success else 1)

