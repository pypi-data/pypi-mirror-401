#!/usr/bin/env python3
"""
Fix user_id format mismatch in factumerit_users table.

Normalizes 3-element user_ids (vikunja:user:id) to 2-element (vikunja:user).

Bead: fa-ixfk (depends on fa-0x9x)

Usage:
    # Dry run (shows what would be changed)
    uv run python scripts/fix_user_id_format.py --dry-run

    # Actually fix the data
    uv run python scripts/fix_user_id_format.py

    # Verify after fix
    uv run python scripts/fix_user_id_format.py --verify
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vikunja_mcp.token_broker import execute


def find_mismatched_user_ids():
    """Find user_ids with 3-element format."""
    rows = execute(
        """
        SELECT user_id FROM factumerit_users
        WHERE user_id ~ '^vikunja:[^:]+:[0-9]+$'
        ORDER BY user_id
        """
    )
    return [row[0] for row in rows] if rows else []


def normalize_user_id(user_id: str) -> str:
    """Normalize vikunja:user:id to vikunja:user."""
    parts = user_id.split(":")
    if len(parts) == 3 and parts[0] == "vikunja":
        return f"{parts[0]}:{parts[1]}"
    return user_id


def fix_user_ids(dry_run: bool = True):
    """Fix all 3-element user_ids in factumerit_users."""
    mismatched = find_mismatched_user_ids()

    if not mismatched:
        print("No mismatched user_ids found. Database is clean.")
        return 0

    print(f"Found {len(mismatched)} mismatched user_id(s):")
    for user_id in mismatched:
        normalized = normalize_user_id(user_id)
        print(f"  {user_id} -> {normalized}")

    if dry_run:
        print("\nDry run - no changes made. Use without --dry-run to fix.")
        return len(mismatched)

    # Actually fix the data
    print("\nFixing...")
    execute(
        """
        UPDATE factumerit_users
        SET user_id = regexp_replace(user_id, '^(vikunja:[^:]+):[0-9]+$', '\\1')
        WHERE user_id ~ '^vikunja:[^:]+:[0-9]+$'
        """
    )

    # Verify
    remaining = find_mismatched_user_ids()
    if remaining:
        print(f"ERROR: {len(remaining)} mismatched user_ids remain!")
        return 1

    print(f"Fixed {len(mismatched)} user_id(s). Database is now clean.")
    return 0


def verify():
    """Verify no mismatched user_ids exist."""
    mismatched = find_mismatched_user_ids()
    if mismatched:
        print(f"FAIL: {len(mismatched)} mismatched user_id(s) found:")
        for user_id in mismatched:
            print(f"  {user_id}")
        return 1
    print("OK: No mismatched user_ids found.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Fix user_id format mismatch in factumerit_users"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify no mismatched user_ids exist",
    )
    args = parser.parse_args()

    if args.verify:
        return verify()
    return fix_user_ids(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
