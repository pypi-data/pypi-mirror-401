#!/usr/bin/env python3
"""
Get JWT token for a user by logging in.

Usage:
    python3 get_jwt_token.py --username ivan_test02 --password <password>
"""

import argparse
import requests
import os

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")


def main():
    parser = argparse.ArgumentParser(description="Get JWT token by logging in")
    parser.add_argument("--username", required=True, help="Vikunja username")
    parser.add_argument("--password", required=True, help="Vikunja password")
    parser.add_argument("--vikunja-url", default=VIKUNJA_URL, help="Vikunja base URL")
    
    args = parser.parse_args()
    
    print(f"Logging in as {args.username}...")
    
    try:
        resp = requests.post(
            f"{args.vikunja_url}/api/v1/login",
            headers={"Accept": "application/json"},
            json={
                "username": args.username,
                "password": args.password
            },
            timeout=10
        )
        
        if resp.status_code == 200:
            data = resp.json()
            jwt_token = data.get("token")
            user_id = data.get("id")
            print(f"\n✅ Login successful!")
            print(f"User ID: {user_id}")
            print(f"JWT Token: {jwt_token}")
            print(f"\nYou can use this token with manual_bot_setup.py:")
            print(f"python3 manual_bot_setup.py --username {args.username} --user-token {jwt_token}")
        else:
            print(f"\n❌ Login failed: {resp.status_code}")
            print(resp.text)
            return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

