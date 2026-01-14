#!/usr/bin/env python3
"""
Manual Bot Setup Script

Use this to manually provision a bot and link it to a user account
when automatic token creation fails.

Usage:
    python3 manual_bot_setup.py --username ivan --user-token tk_abc123...

This will:
1. Provision a personal bot for the user
2. Store bot credentials in database
3. Share user's Inbox with the bot
4. Create welcome task with bot username
"""

import argparse
import sys
import os

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vikunja_mcp.bot_provisioning import provision_personal_bot, store_bot_credentials, ProvisioningError
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")


def main():
    parser = argparse.ArgumentParser(description="Manually provision a bot for a user")
    parser.add_argument("--username", required=True, help="Vikunja username (e.g., ivan)")
    parser.add_argument("--user-token", required=True, help="User's JWT token (from login)")
    parser.add_argument("--vikunja-url", default=VIKUNJA_URL, help="Vikunja base URL")
    parser.add_argument("--admin-token", help="Vikunja admin token (for nginx auth)")

    args = parser.parse_args()

    # Set admin token in environment if provided
    if args.admin_token:
        os.environ["VIKUNJA_ADMIN_TOKEN"] = args.admin_token
    
    username = args.username
    user_token = args.user_token
    vikunja_url = args.vikunja_url
    
    logger.info(f"Starting manual bot setup for user: {username}")
    
    # Step 1: Get user's Vikunja ID
    logger.info("Fetching user info...")
    try:
        user_resp = requests.get(
            f"{vikunja_url}/api/v1/user",
            headers={
                "Authorization": f"Bearer {user_token}",
                "Accept": "application/json"
            },
            timeout=10
        )
        user_resp.raise_for_status()
        user_data = user_resp.json()
        vikunja_user_id = user_data.get("id")
        logger.info(f"User ID: {vikunja_user_id}")
    except Exception as e:
        logger.error(f"Failed to get user info: {e}")
        logger.error("Make sure the token is valid and has not expired")
        return 1
    
    # Step 2: Provision bot
    logger.info("Provisioning personal bot...")
    try:
        bot_creds = provision_personal_bot(username, vikunja_url=vikunja_url)
        logger.info(f"Bot provisioned: {bot_creds.username} (ID: {bot_creds.vikunja_user_id})")
    except ProvisioningError as e:
        logger.error(f"Failed to provision bot: {e}")
        return 1
    
    # Step 3: Store credentials in database
    logger.info("Storing bot credentials in database...")
    user_id = f"vikunja:{username}"
    try:
        store_bot_credentials(
            user_id,
            bot_creds,
            owner_vikunja_user_id=vikunja_user_id,
            owner_vikunja_token=user_token
        )
        logger.info(f"Credentials stored for {user_id}")
    except Exception as e:
        logger.error(f"Failed to store credentials: {e}")
        return 1
    
    # Step 4: Find user's Inbox
    logger.info("Finding user's Inbox...")
    try:
        projects_resp = requests.get(
            f"{vikunja_url}/api/v1/projects",
            headers={
                "Authorization": f"Bearer {user_token}",
                "Accept": "application/json"
            },
            timeout=10
        )
        projects_resp.raise_for_status()
        projects = projects_resp.json()
        
        inbox = next((p for p in projects if p.get("title", "").lower() == "inbox"), None)
        if not inbox and projects:
            inbox = projects[0]
            logger.info(f"No 'Inbox' found, using first project: {inbox.get('title')}")
        elif inbox:
            logger.info(f"Found Inbox (ID: {inbox.get('id')})")
        else:
            logger.warning("No projects found!")
            inbox = None
    except Exception as e:
        logger.error(f"Failed to get projects: {e}")
        inbox = None
    
    # Step 5: Share Inbox with bot
    if inbox:
        inbox_id = inbox.get("id")
        logger.info(f"Sharing Inbox {inbox_id} with bot...")
        try:
            share_resp = requests.put(
                f"{vikunja_url}/api/v1/projects/{inbox_id}/users",
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Accept": "application/json"
                },
                json={
                    "user_id": bot_creds.vikunja_user_id,
                    "right": 1  # read/write
                },
                timeout=10
            )
            share_resp.raise_for_status()
            logger.info(f"✅ Inbox shared with bot!")
        except Exception as e:
            logger.error(f"Failed to share Inbox: {e}")
    
    # Step 6: Create welcome task
    if inbox:
        logger.info("Creating welcome task...")
        try:
            task_resp = requests.put(
                f"{vikunja_url}/api/v1/projects/{inbox_id}/tasks",
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Accept": "application/json"
                },
                json={
                    "title": f"👋 Welcome! Your AI assistant is @{bot_creds.username}",
                    "description": f"""Welcome to Factumerit! 🎉

Your personal AI assistant has been set up and is ready to help you manage tasks.

**Your bot username:** @{bot_creds.username}

**Try these commands:**
- @{bot_creds.username} !help - See all available commands
- @{bot_creds.username} !now - See what's on your plate
- @{bot_creds.username} create task buy milk tomorrow - Add a new task

You can @mention your bot in any task or comment, and it will respond to your requests!
""",
                    "priority": 5
                },
                timeout=10
            )
            task_resp.raise_for_status()
            logger.info(f"✅ Welcome task created!")
        except Exception as e:
            logger.error(f"Failed to create welcome task: {e}")
    
    logger.info(f"\n🎉 Setup complete! Bot username: @{bot_creds.username}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

