#!/usr/bin/env python3
"""
Admin CLI for managing registration tokens.

Bead: solutions-8zly.7

Usage:
    python scripts/manage_tokens.py create --token NSA-NORTHWEST-50 --uses 50 --expires 2026-03-01 --notes "NSA Northwest beta"
    python scripts/manage_tokens.py list
    python scripts/manage_tokens.py stats NSA-NORTHWEST-50
    python scripts/manage_tokens.py revoke NSA-NORTHWEST-50 --reason "Beta ended"

Environment:
    DATABASE_URL: PostgreSQL connection string
"""
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
import secrets
import string

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from psycopg.rows import dict_row

from vikunja_mcp.token_broker import get_db
from vikunja_mcp.registration_tokens import (
    get_token_stats,
    TokenNotFoundError,
)


def generate_token() -> str:
    """Generate random registration token like BETA-X7K9-2025."""
    chars = string.ascii_uppercase + string.digits
    part1 = "BETA"
    part2 = "".join(secrets.choice(chars) for _ in range(4))
    part3 = datetime.now().year
    return f"{part1}-{part2}-{part3}"


def create_token(
    token: str | None,
    uses: int,
    expires: str | None,
    notes: str | None,
    initial_credit_cents: int = 0,
    ttl_days: int | None = None,
    created_by: str = "admin",
) -> str:
    """Create registration token.

    Args:
        token: Token string (auto-generated if not provided)
        uses: Maximum number of signups allowed
        expires: Expiration date (YYYY-MM-DD) - when token can no longer be used
        notes: Notes about this token
        initial_credit_cents: Credit amount for users signing up (default 0)
        ttl_days: Days until promo credit expires after signup (None = never)
        created_by: Admin user who created the token
    """
    if not token:
        token = generate_token()

    # Validate token format (uppercase, alphanumeric + hyphens)
    if not all(c.isupper() or c.isdigit() or c == "-" for c in token):
        raise ValueError("Token must be uppercase alphanumeric with hyphens only")

    expires_at = None
    if expires:
        try:
            expires_at = datetime.fromisoformat(expires)
        except ValueError:
            raise ValueError(f"Invalid date format: {expires}. Use YYYY-MM-DD")

    with get_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO registration_tokens
                    (token, state, max_uses, uses_remaining, expires_at, created_by, notes, initial_credit_cents, ttl_days)
                    VALUES (%s, 'active', %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (token, uses, uses, expires_at, created_by, notes, initial_credit_cents, ttl_days),
                )
                conn.commit()
            except Exception as e:
                conn.rollback()
                if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                    raise ValueError(f"Token '{token}' already exists")
                raise

    print(f"Created token: {token}")
    print(f"   Uses: {uses}")
    print(f"   Initial credit: ${initial_credit_cents/100:.2f}")
    print(f"   Credit TTL: {f'{ttl_days} days' if ttl_days else 'Never expires'}")
    print(f"   Token expires: {expires or 'Never'}")
    print(f"   Notes: {notes or 'None'}")
    print(f"\nSignup link: https://mcp.factumerit.app/beta-signup?code={token}")

    return token


def list_tokens(state_filter: str | None = None):
    """List all registration tokens."""
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            query = """
                SELECT
                    rt.token,
                    rt.state,
                    rt.max_uses,
                    rt.uses_remaining,
                    rt.initial_credit_cents,
                    rt.ttl_days,
                    rt.expires_at,
                    rt.notes,
                    COUNT(tu.id) as used_count
                FROM registration_tokens rt
                LEFT JOIN token_usage tu ON rt.token = tu.token
            """

            if state_filter:
                query += " WHERE rt.state = %s"
                query += " GROUP BY rt.token ORDER BY rt.created_at DESC"
                cur.execute(query, (state_filter,))
            else:
                query += " GROUP BY rt.token ORDER BY rt.created_at DESC"
                cur.execute(query)

            tokens = cur.fetchall()

            if not tokens:
                print("No tokens found")
                return

            print(f"\n{'Token':<30} {'State':<10} {'Uses':<10} {'Credit':<10} {'TTL':<8} {'Expires':<12} {'Notes'}")
            print("-" * 115)

            for t in tokens:
                expires = t["expires_at"].date() if t["expires_at"] else "Never"
                uses = f"{t['used_count']}/{t['max_uses']}"
                credit = f"${t.get('initial_credit_cents', 0)/100:.2f}"
                ttl = f"{t.get('ttl_days')}d" if t.get('ttl_days') else "-"
                notes = (t["notes"] or "")[:25]
                print(f"{t['token']:<30} {t['state']:<10} {uses:<10} {credit:<10} {ttl:<8} {expires:<12} {notes}")


def show_token_stats(token: str):
    """Show detailed statistics for a token."""
    try:
        stats = get_token_stats(token)
    except TokenNotFoundError:
        print(f"Token '{token}' not found")
        sys.exit(1)

    print(f"\nToken: {stats['token']}")
    print(f"State: {stats['state']}")
    print(
        f"Uses: {stats['used_count']}/{stats['max_uses']} "
        f"({stats['uses_remaining']} remaining)"
    )
    initial_credit = stats.get('initial_credit_cents', 0)
    ttl_days = stats.get('ttl_days')
    print(f"Initial credit: ${initial_credit/100:.2f}")
    print(f"Credit TTL: {f'{ttl_days} days' if ttl_days else 'Never expires'}")
    print(f"Token expires: {stats['expires_at'].date() if stats['expires_at'] else 'Never'}")
    print(f"Notes: {stats['notes'] or 'None'}")

    if stats["recent_signups"]:
        print(f"\nRecent signups ({len(stats['recent_signups'])}):")
        for signup in stats["recent_signups"]:
            print(f"  {signup['user_id']:<40} {signup['used_at']}")
    else:
        print("\nNo signups yet")


def revoke_token(token: str, reason: str):
    """Revoke a registration token."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE registration_tokens
                SET state = 'revoked',
                    notes = COALESCE(notes || ' | ', '') || 'Revoked: ' || %s
                WHERE token = %s AND state != 'revoked'
                RETURNING token
                """,
                (reason, token),
            )

            result = cur.fetchone()
            conn.commit()

            if result:
                print(f"Revoked token: {token}")
                print(f"   Reason: {reason}")
            else:
                print(f"Token '{token}' not found or already revoked")
                sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Manage registration tokens")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Create token
    create_parser = subparsers.add_parser("create", help="Create registration token")
    create_parser.add_argument(
        "--token", help="Token string (auto-generated if not provided)"
    )
    create_parser.add_argument(
        "--uses", type=int, required=True, help="Maximum number of uses"
    )
    create_parser.add_argument(
        "--amount", type=float, default=0,
        help="Initial credit in dollars (default: 0). E.g., --amount 1.00 for $1"
    )
    create_parser.add_argument(
        "--ttl", type=int, default=None,
        help="Days until credit expires after signup (default: never). E.g., --ttl 7 for 1 week"
    )
    create_parser.add_argument("--expires", help="Token expiration date (YYYY-MM-DD) - deadline to sign up")
    create_parser.add_argument("--notes", help="Notes about this token")

    # List tokens
    list_parser = subparsers.add_parser("list", help="List all tokens")
    list_parser.add_argument(
        "--state",
        choices=["active", "exhausted", "expired", "revoked"],
        help="Filter by state",
    )

    # Show stats
    stats_parser = subparsers.add_parser("stats", help="Show token statistics")
    stats_parser.add_argument("token", help="Token to show stats for")

    # Revoke token
    revoke_parser = subparsers.add_parser("revoke", help="Revoke a token")
    revoke_parser.add_argument("token", help="Token to revoke")
    revoke_parser.add_argument("--reason", required=True, help="Reason for revocation")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check DATABASE_URL is set
    if not os.environ.get("DATABASE_URL"):
        print("Error: DATABASE_URL environment variable not set")
        print("Set it with: export DATABASE_URL='postgresql://...'")
        sys.exit(1)

    try:
        if args.command == "create":
            initial_credit_cents = round(args.amount * 100)
            create_token(args.token, args.uses, args.expires, args.notes, initial_credit_cents, args.ttl)
        elif args.command == "list":
            list_tokens(args.state)
        elif args.command == "stats":
            show_token_stats(args.token)
        elif args.command == "revoke":
            revoke_token(args.token, args.reason)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Database error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
