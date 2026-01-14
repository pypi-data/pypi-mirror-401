#!/usr/bin/env python3
"""
Link an existing bot to a user account.

Use this when a bot was already created but not properly linked.

Usage:
    python3 link_existing_bot.py --username ivan_test02 --bot-username e-691072 --user-token <jwt>
"""

import argparse
import sys
import os
import requests
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")


def main():
    parser = argparse.ArgumentParser(description="Link existing bot to user")
    parser.add_argument("--username", required=True, help="Vikunja username (e.g., ivan_test02)")
    parser.add_argument("--bot-username", required=True, help="Bot username (e.g., e-691072)")
    parser.add_argument("--bot-id", type=int, help="Bot's Vikunja user ID (if known)")
    parser.add_argument("--user-token", required=True, help="User's JWT token")
    parser.add_argument("--vikunja-url", default=VIKUNJA_URL, help="Vikunja base URL")

    args = parser.parse_args()

    username = args.username
    bot_username = args.bot_username
    bot_id_override = args.bot_id
    user_token = args.user_token
    vikunja_url = args.vikunja_url
    
    logger.info(f"Linking bot {bot_username} to user {username}")
    
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
        return 1
    
    # Step 2: Get bot's Vikunja ID
    if bot_id_override:
        bot_vikunja_id = bot_id_override
        logger.info(f"Using provided bot ID: {bot_vikunja_id}")
    else:
        logger.info(f"Looking up bot {bot_username}...")
        try:
            search_resp = requests.get(
                f"{vikunja_url}/api/v1/users",
                params={"s": bot_username},
                headers={
                    "Authorization": f"Bearer {user_token}",
                    "Accept": "application/json"
                },
                timeout=10
            )
            search_resp.raise_for_status()
            users = search_resp.json()

            logger.info(f"Search returned: {users}")

            if not users or not isinstance(users, list):
                logger.error(f"Bot {bot_username} not found in Vikunja (search returned: {users})")
                logger.error(f"Try providing --bot-id parameter if you know the bot's Vikunja user ID")
                return 1

            bot_user = next((u for u in users if u.get("username") == bot_username), None)
            if not bot_user:
                logger.error(f"Bot {bot_username} not found in search results")
                logger.error(f"Try providing --bot-id parameter if you know the bot's Vikunja user ID")
                return 1

            bot_vikunja_id = bot_user.get("id")
            logger.info(f"Bot ID: {bot_vikunja_id}")
        except Exception as e:
            logger.error(f"Failed to lookup bot: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Step 3: Find user's Inbox
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
    
    # Step 4: Share Inbox with bot
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
                    "user_id": str(bot_vikunja_id),  # API expects string
                    "right": 1  # read/write
                },
                timeout=10
            )
            share_resp.raise_for_status()
            logger.info(f"✅ Inbox shared with bot!")
        except Exception as e:
            logger.error(f"Failed to share Inbox: {e}")
            logger.error(f"Response: {share_resp.text if 'share_resp' in locals() else 'N/A'}")
    
    # Step 5: Create welcome task
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
                    "title": f"👋 Welcome! Your AI assistant is @{bot_username}",
                    "description": f"""Welcome to Factumerit! 🎉

Your personal AI assistant has been set up and is ready to help you manage tasks.

**Your bot username:** @{bot_username}

**Try these commands:**
- @{bot_username} !help - See all available commands
- @{bot_username} !now - See what's on your plate
- @{bot_username} create task buy milk tomorrow - Add a new task

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
            logger.error(f"Response: {task_resp.text if 'task_resp' in locals() else 'N/A'}")
    
    logger.info(f"\n🎉 Setup complete! Bot @{bot_username} is now linked to {username}")
    logger.info(f"User can now @mention the bot in tasks!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

