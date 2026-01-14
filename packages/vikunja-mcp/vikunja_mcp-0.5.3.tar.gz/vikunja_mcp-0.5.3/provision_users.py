#!/usr/bin/env python3
"""
Provision bots for jmuggli and mariaman24.

This script will:
1. Create personal bots for each user
2. Store credentials in the database
3. Enable service_needed for each user
4. Create welcome task in their Inbox with bot credentials
"""
import sys
import os
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vikunja_mcp.bot_provisioning import (
    provision_personal_bot,
    store_bot_credentials,
    set_service_needed,
    execute,
)

VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app")

def provision_user(username: str, vikunja_user_id: int, bot_username: str):
    """Provision a bot for a user."""
    user_id = f"vikunja:{username}"

    print(f"\n{'='*60}")
    print(f"Provisioning bot for {user_id} (@{bot_username})")
    print(f"{'='*60}")

    # Step 1: Create user in factumerit_users if not exists
    print(f"1. Creating user in factumerit_users...")
    execute(
        """
        INSERT INTO factumerit_users (user_id, platform, is_active, service_needed, service_reason)
        VALUES (%s, 'vikunja', TRUE, TRUE, 'initial_setup')
        ON CONFLICT (user_id) DO UPDATE SET
            is_active = TRUE,
            service_needed = TRUE,
            service_reason = 'initial_setup'
        """,
        (user_id,),
    )
    print(f"   ✅ User created/updated")

    # Step 2: Check if bot already exists
    print(f"2. Checking if bot already exists...")
    existing_bot = None
    try:
        result = execute(
            "SELECT bot_username, bot_vikunja_user_id FROM personal_bots WHERE user_id = %s",
            (user_id,),
            fetch=True
        )
        if result:
            existing_bot = {"username": result[0], "vikunja_user_id": result[1]}
            print(f"   ✅ Bot already exists: @{existing_bot['username']}")
    except Exception as e:
        print(f"   ⚠️  Error checking for existing bot: {e}")

    # Step 3: Provision personal bot (if needed)
    if existing_bot:
        print(f"3. Skipping bot creation (already exists)")
        # Create a credentials object from existing data
        from vikunja_mcp.bot_provisioning import BotCredentials
        credentials = BotCredentials(
            username=existing_bot["username"],
            password="<existing>",  # Don't have password for existing bots
            email=f"{existing_bot['username']}@bot.factumerit.app",
            vikunja_user_id=existing_bot["vikunja_user_id"]
        )
    else:
        print(f"3. Provisioning personal bot @{bot_username}...")
        credentials = provision_personal_bot(
            username=username,
            display_name=bot_username,
            bot_username=bot_username,
        )
        print(f"   ✅ Bot created: {credentials.username}")
        print(f"   - Vikunja user ID: {credentials.vikunja_user_id}")
        print(f"   - Email: {credentials.email}")
        print(f"   - Password: {credentials.password}")

        # Step 4: Store credentials
        print(f"4. Storing bot credentials...")
        store_bot_credentials(
            user_id=user_id,
            credentials=credentials,
            owner_vikunja_user_id=vikunja_user_id,
        )
        print(f"   ✅ Credentials stored")

    # Step 5: Get user's Vikunja JWT token to create welcome task
    print(f"5. Getting user's Vikunja token...")
    user_token = None
    try:
        # Get user's token from personal_bots table (owner_vikunja_token)
        result = execute(
            "SELECT owner_vikunja_token FROM personal_bots WHERE user_id = %s",
            (user_id,),
            fetch=True
        )
        if result and result[0]:
            user_token = result[0]
            print(f"   ✅ User token retrieved")
        else:
            print(f"   ⚠️  No user token found (will skip welcome task)")
    except Exception as e:
        print(f"   ⚠️  Failed to get user token: {e}")

    # Step 6: Find user's Inbox project
    inbox_id = None
    if user_token:
        print(f"6. Finding user's Inbox...")
        try:
            projects_resp = requests.get(
                f"{VIKUNJA_URL}/api/v1/projects",
                headers={"Authorization": f"Bearer {user_token}"},
                timeout=10
            )
            if projects_resp.status_code == 200:
                projects = projects_resp.json()
                for project in projects:
                    if project.get("title") == "Inbox":
                        inbox_id = project["id"]
                        print(f"   ✅ Found Inbox (ID: {inbox_id})")
                        break
                if not inbox_id:
                    print(f"   ⚠️  Inbox not found")
            else:
                print(f"   ⚠️  Failed to get projects: {projects_resp.status_code}")
        except Exception as e:
            print(f"   ⚠️  Error finding Inbox: {e}")

    # Step 7: Create welcome task with bot credentials
    if user_token and inbox_id:
        print(f"7. Creating welcome task...")
        try:
            description_html = f"""<p>👋 <strong>Your personal AI assistant is ready!</strong></p>

<p>Your bot has been provisioned with the username <strong>@{credentials.username}</strong></p>

<h3>🚀 Getting Started</h3>

<ol>
<li><strong>Share this Inbox with your bot:</strong>
   <ul>
   <li>Click the "Share" button above</li>
   <li>Search for <code>@{credentials.username}</code></li>
   <li>Give it "Read & Write" permission</li>
   </ul>
</li>

<li><strong>Try a command:</strong>
   <ul>
   <li>Create a new task or comment</li>
   <li>Type: <code>@{credentials.username} !help</code></li>
   <li>Your bot will respond!</li>
   </ul>
</li>

<li><strong>Enable EARS mode (optional):</strong>
   <ul>
   <li>Type: <code>@{credentials.username} !ears on</code></li>
   <li>Now you can skip the @ and just say "!weather" or "!help"</li>
   </ul>
</li>
</ol>

<h3>📚 Useful Commands</h3>
<ul>
<li><code>!help</code> - See all commands</li>
<li><code>!weather [city]</code> - Get weather</li>
<li><code>!now</code> - See what's on your plate</li>
<li><code>!bal</code> - Check your credit balance</li>
</ul>

<p style="font-size: 14px; color: #666;">Questions? Email hello@factumerit.app</p>"""

            task_resp = requests.put(
                f"{VIKUNJA_URL}/api/v1/projects/{inbox_id}/tasks",
                headers={"Authorization": f"Bearer {user_token}"},
                json={
                    "title": f"🤖 Your AI assistant @{credentials.username} is ready!",
                    "description": description_html,
                    "priority": 5  # High priority so it shows up first
                },
                timeout=10
            )

            if task_resp.status_code == 201:
                print(f"   ✅ Welcome task created")
            else:
                print(f"   ⚠️  Failed to create welcome task: {task_resp.status_code}")
                print(f"       Response: {task_resp.text[:200]}")
        except Exception as e:
            print(f"   ⚠️  Error creating welcome task: {e}")

    print(f"\n✅ {user_id} provisioned successfully!")
    print(f"   Bot username: @{credentials.username}")
    print(f"   Bot password: {credentials.password}")
    print(f"   Vikunja user ID: {credentials.vikunja_user_id}")

    return credentials

if __name__ == "__main__":
    print("Provisioning bots for jmuggli, mariaman24, and ivan...")

    # Vikunja user IDs from database query:
    # sqlite3 /db/vikunja.db "SELECT id, username FROM users WHERE username IN ('jmuggli', 'mariaman24', 'ivan');"
    # 11|jmuggli
    # 8|mariaman24
    # 1|ivan

    users = [
        ("jmuggli", 11, "eij"),      # Jim gets @eij
        ("mariaman24", 8, "eim"),    # Maria gets @eim
        ("ivan", 1, "eis"),          # Ivan gets @eis (already exists, will create welcome task)
    ]

    for username, vikunja_user_id, bot_username in users:
        try:
            provision_user(username, vikunja_user_id, bot_username)
        except Exception as e:
            print(f"\n❌ Failed to provision {username}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("Done!")
    print("="*60)

