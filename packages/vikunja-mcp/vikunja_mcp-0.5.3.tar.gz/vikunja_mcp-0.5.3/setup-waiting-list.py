#!/usr/bin/env python3
"""
Setup Waiting List project in Vikunja Cloud for mcp.factumerit.app/waiting-list

This script:
1. Creates a "Waiting List" project in Vikunja Cloud
2. Outputs the project ID to add to ~/factumerit/backend/.env
3. Creates a test signup to verify it works

Usage:
    cd /home/ivanadamin/spawn-solutions/factumerit
    python3 setup-waiting-list.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add vikunja wrapper to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'development/projects/impl-1131-vikunja/vikunja-api-wrapper/src'))

from vikunja_wrapper import VikunjaClient

# Load credentials from spawn-solutions/.env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

VIKUNJA_TOKEN = os.environ.get('VIKUNJA_API_TOKEN')
VIKUNJA_URL = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

def main():
    if not VIKUNJA_TOKEN:
        print("❌ Error: VIKUNJA_API_TOKEN not found in .env")
        print(f"   Expected: {env_path}")
        sys.exit(1)

    print("=" * 70)
    print("Setting up Waiting List for mcp.factumerit.app")
    print("=" * 70)
    print()

    # Initialize client
    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    # Create Waiting List project
    print("Creating 'Waiting List' project...")
    try:
        project = client.projects.create(
            title="Waiting List",
            description="Signups from https://mcp.factumerit.app/waiting-list"
        )
        print(f"✅ Created project: {project.title}")
        print(f"   Project ID: {project.id}")
        print(f"   URL: {VIKUNJA_URL}/projects/{project.id}")
        print()
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)

    # Create a test task to verify
    print("Creating test signup task...")
    try:
        task = client.tasks.create(
            project_id=project.id,
            title="test@example.com (Test User)",
            description="<b>Name:</b> Test User<br><b>Email:</b> test@example.com<br><b>Source:</b> setup-script<br><br><b>Message:</b><br>This is a test signup to verify the waiting list works.<hr><i>Submitted: 2025-12-30 (setup)</i>"
        )
        print(f"✅ Created test task: {task.title}")
        print(f"   Task ID: {task.id}")
        print()
    except Exception as e:
        print(f"❌ Error creating test task: {e}")
        sys.exit(1)

    # Output configuration instructions
    print("=" * 70)
    print("✅ Setup Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print()
    print("1. Update ~/factumerit/backend/.env:")
    print()
    print(f"   export WAITING_LIST_PROJECT_ID='{project.id}'")
    print()
    print("2. Restart the MCP server (if running locally):")
    print()
    print("   cd ~/factumerit/backend")
    print("   # Stop current server (Ctrl+C)")
    print("   # Restart with: ./run-mcp.sh")
    print()
    print("3. Or update Render environment variables:")
    print()
    print("   https://dashboard.render.com/web/srv-d50p4ns9c44c738capjg/env")
    print(f"   WAITING_LIST_PROJECT_ID = {project.id}")
    print()
    print("4. Test the waiting list:")
    print()
    print("   https://mcp.factumerit.app/waiting-list?source=test")
    print()
    print(f"5. View signups in Vikunja:")
    print()
    print(f"   {VIKUNJA_URL}/projects/{project.id}")
    print()

if __name__ == "__main__":
    main()

