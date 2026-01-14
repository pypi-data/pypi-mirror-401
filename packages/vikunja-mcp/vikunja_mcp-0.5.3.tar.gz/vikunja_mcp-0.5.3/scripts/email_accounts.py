#!/usr/bin/env python3
"""
Email Account Management CLI

Manage email routing rules for factumerit.app inbound email.

Usage:
    python scripts/email_accounts.py list
    python scripts/email_accounts.py add help forward ivan@ivantohelpyou.com
    python scripts/email_accounts.py add sales forward sales@company.com
    python scripts/email_accounts.py add spam drop
    python scripts/email_accounts.py delete help
    python scripts/email_accounts.py stats

Bead: fa-4mda.1
"""

import argparse
import sys
from pathlib import Path

import yaml

# Config file location
CONFIG_PATH = Path(__file__).parent.parent / "config" / "email_routing.yaml"


def load_config() -> dict:
    """Load email routing configuration."""
    if not CONFIG_PATH.exists():
        return {"routes": {}}
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f) or {"routes": {}}


def save_config(config: dict) -> None:
    """Save email routing configuration."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def cmd_list(args) -> None:
    """List all email routes."""
    config = load_config()
    routes = config.get("routes", {})

    if not routes:
        print("No email routes configured.")
        print("\nAdd one with:")
        print("  python scripts/email_accounts.py add help forward you@example.com")
        return

    print(f"{'Address':<25} {'Action':<10} {'Destination':<35} {'Description'}")
    print("-" * 100)

    for local_part, route in routes.items():
        addr = f"{local_part}@factumerit.app"
        action = route.get("action", "?")
        dest = route.get("destination", "-")
        desc = route.get("description", "")
        print(f"{addr:<25} {action:<10} {dest:<35} {desc}")


def cmd_add(args) -> None:
    """Add an email route."""
    config = load_config()
    routes = config.setdefault("routes", {})

    local_part = args.address.lower().replace("@factumerit.app", "")
    action = args.action.lower()

    if action not in ("forward", "eis", "drop"):
        print(f"Error: Invalid action '{action}'. Use: forward, eis, drop")
        sys.exit(1)

    if action == "forward" and not args.destination:
        print("Error: forward action requires a destination email")
        print("  python scripts/email_accounts.py add help forward you@example.com")
        sys.exit(1)

    route = {"action": action}
    if args.destination:
        route["destination"] = args.destination
    if args.description:
        route["description"] = args.description

    routes[local_part] = route
    save_config(config)

    print(f"Added: {local_part}@factumerit.app -> {action}", end="")
    if args.destination:
        print(f" -> {args.destination}")
    else:
        print()


def cmd_delete(args) -> None:
    """Delete an email route."""
    config = load_config()
    routes = config.get("routes", {})

    local_part = args.address.lower().replace("@factumerit.app", "")

    if local_part not in routes:
        print(f"Error: No route for {local_part}@factumerit.app")
        sys.exit(1)

    del routes[local_part]
    save_config(config)
    print(f"Deleted: {local_part}@factumerit.app")


def cmd_stats(args) -> None:
    """Show email routing statistics."""
    config = load_config()
    routes = config.get("routes", {})

    # Count by action type
    by_action = {}
    for route in routes.values():
        action = route.get("action", "unknown")
        by_action[action] = by_action.get(action, 0) + 1

    print("Email Routing Statistics")
    print("-" * 40)
    print(f"Total routes: {len(routes)}")
    print()
    print("By action:")
    for action, count in sorted(by_action.items()):
        print(f"  {action}: {count}")

    # TODO: Add actual email stats from logs/database
    print()
    print("(Delivery stats require log analysis - not yet implemented)")


def main():
    parser = argparse.ArgumentParser(
        description="Manage email routing for factumerit.app",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                                    # Show all routes
  %(prog)s add help forward ivan@example.com       # Forward help@ to ivan
  %(prog)s add eis eis                             # Route to @eis AI
  %(prog)s add spam drop                           # Silently drop spam@
  %(prog)s delete help                             # Remove help@ route
  %(prog)s stats                                   # Show statistics
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="List all email routes")

    # add
    add_parser = subparsers.add_parser("add", help="Add an email route")
    add_parser.add_argument("address", help="Local part (e.g., 'help' for help@factumerit.app)")
    add_parser.add_argument("action", choices=["forward", "eis", "drop"], help="Action to take")
    add_parser.add_argument("destination", nargs="?", help="Destination email (for forward)")
    add_parser.add_argument("-d", "--description", help="Optional description")

    # delete
    del_parser = subparsers.add_parser("delete", help="Delete an email route")
    del_parser.add_argument("address", help="Local part to delete")

    # stats
    subparsers.add_parser("stats", help="Show routing statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "list": cmd_list,
        "add": cmd_add,
        "delete": cmd_delete,
        "stats": cmd_stats,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
