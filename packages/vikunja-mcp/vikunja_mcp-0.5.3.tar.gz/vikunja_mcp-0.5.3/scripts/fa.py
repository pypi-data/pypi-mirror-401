#!/usr/bin/env python3
"""
Factumerit Admin CLI (fa).

Admin commands for managing Factumerit users, bots, tokens, and workspaces.

Bead: fa-letl

Usage:
    fa vikunja delete-user <email> [--dry-run] [--force]
    fa vikunja list-users
    fa tokens list
    fa tokens show <token>
    fa tokens extend <token> --days 30
    fa tokens create <token> --uses 50 --notes "Beta batch"
    fa tokens delete <token> [--force]
    fa workspaces list <email>
    fa workspaces link <email> <user_id> [--name NAME] [--primary]
    fa workspaces set-primary <email> <user_id>
    fa workspaces unlink <user_id> [--force]
    fa workspaces show-all

Environment:
    DATABASE_URL: PostgreSQL connection string
    VIKUNJA_URL: Vikunja instance URL (default: https://vikunja.factumerit.app)
    VIKUNJA_USER: Admin username for JWT auth
    VIKUNJA_PASSWORD: Admin password for JWT auth
"""
import argparse
import os
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def vikunja_delete_user(args):
    """Delete a user completely from Factumerit and Vikunja."""
    from vikunja_mcp.bot_provisioning import delete_user, get_user_by_email, ProvisioningError
    from vikunja_mcp.token_broker import execute

    email = args.email
    dry_run = args.dry_run
    force = args.force

    # First, look up the user to show what will be deleted
    user = get_user_by_email(email)
    if not user:
        print(f"Error: No user found with email: {email}")
        sys.exit(1)

    # Get bot info too
    bot_rows = execute(
        """
        SELECT bot_username, vikunja_user_id
        FROM personal_bots
        WHERE user_id = %s
        """,
        (user["user_id"],),
    )
    bot_info = bot_rows[0] if bot_rows else (None, None)

    # Show what will be deleted
    print(f"\n⚠️  WARNING: This will permanently delete:")
    print(f"  User email: {email}")
    print(f"  User ID: {user['user_id']}")
    print(f"  Platform: {user['platform']}")
    if bot_info[0]:
        print(f"  Bot username: {bot_info[0]}")
        print(f"  Bot Vikunja ID: {bot_info[1]}")
    print()
    print("  This includes:")
    print("    - User's Vikunja account and all their projects/tasks")
    print("    - Bot's Vikunja account")
    print("    - Factumerit registration record")
    print()
    print("  💡 TIP: Export user data first with 'fa vikunja export-user <email>'")
    print()

    if dry_run:
        print("[DRY RUN] No changes made.")
        return

    # Require confirmation unless --force
    if not force:
        confirm = input("Type 'DELETE' to confirm: ")
        if confirm != "DELETE":
            print("Aborted.")
            sys.exit(1)

    try:
        result = delete_user(email=email, dry_run=False)

        print(f"\nDelete result for: {email}")
        print(f"  user_id: {result.user_id}")
        print(f"  owner_vikunja_id: {result.owner_vikunja_id or 'N/A'}")
        print(f"  bot_username: {result.bot_username or 'N/A'}")
        print(f"  bot_vikunja_id: {result.bot_vikunja_id or 'N/A'}")
        print()
        print(f"  vikunja_user_deleted: {'yes' if result.vikunja_user_deleted else 'no'}")
        print(f"  vikunja_bot_deleted: {'yes' if result.vikunja_bot_deleted else 'no'}")
        print(f"  bot_record_deleted: {'yes' if result.bot_record_deleted else 'no'}")
        print(f"  factumerit_deleted: {'yes' if result.factumerit_deleted else 'no'}")
        if result.balance_forfeited_cents > 0:
            print(f"  balance_forfeited: ${result.balance_forfeited_cents/100:.2f}")

        if result.errors:
            print(f"\nErrors:")
            for err in result.errors:
                print(f"  - {err}")
            sys.exit(1)
        else:
            if dry_run:
                print(f"\n[DRY RUN] No changes made. Run without --dry-run to delete.")
            else:
                print(f"\nUser deleted successfully.")

    except ProvisioningError as e:
        print(f"Error: {e}")
        sys.exit(1)


# =============================================================================
# LEDGER COMMANDS (fa-tn5s)
# =============================================================================

def ledger_balances(args):
    """Show all account balances from double-entry ledger."""
    from vikunja_mcp.token_broker import execute

    rows = execute("""
        SELECT
            account,
            SUM(credit_cents) - SUM(debit_cents) AS balance_cents,
            SUM(debit_cents) AS total_debits,
            SUM(credit_cents) AS total_credits,
            COUNT(*) AS entries
        FROM ledger_entries
        GROUP BY account
        ORDER BY account
    """)

    if not rows:
        print("No ledger entries found")
        return

    print(f"\n{'Account':<40} {'Balance':>12} {'Debits':>12} {'Credits':>12} {'Entries':>8}")
    print("-" * 90)

    for row in rows:
        account, balance, debits, credits, entries = row
        print(f"{account:<40} ${balance/100:>10.2f} ${debits/100:>10.2f} ${credits/100:>10.2f} {entries:>8}")

    print("-" * 90)

    # Show totals
    totals = execute("SELECT * FROM ledger_integrity")[0]
    total_debits, total_credits, imbalance = totals
    total_debits = total_debits or 0
    total_credits = total_credits or 0
    imbalance = imbalance or 0

    status = "✓ BALANCED" if imbalance == 0 else f"⚠️  IMBALANCE: ${imbalance/100:.2f}"
    print(f"{'TOTALS':<40} {'':<12} ${total_debits/100:>10.2f} ${total_credits/100:>10.2f}")
    print(f"\n{status}")


def ledger_user(args):
    """Show ledger entries for a specific user."""
    from vikunja_mcp.token_broker import execute

    user_id = args.user_id
    account = f"user:{user_id}"
    limit = args.limit or 50

    rows = execute("""
        SELECT
            transaction_id,
            debit_cents,
            credit_cents,
            description,
            reference_type,
            created_at
        FROM ledger_entries
        WHERE account = %s
        ORDER BY created_at DESC
        LIMIT %s
    """, (account, limit))

    if not rows:
        print(f"No ledger entries for {account}")
        return

    # Get balance
    balance_row = execute("""
        SELECT SUM(credit_cents) - SUM(debit_cents) AS balance
        FROM ledger_entries WHERE account = %s
    """, (account,))[0]
    balance = balance_row[0] or 0

    print(f"\nLedger: {account}")
    print(f"Balance: ${balance/100:.2f}")
    print()
    print(f"{'Date':<20} {'Type':<15} {'Debit':>10} {'Credit':>10} {'Description'}")
    print("-" * 80)

    for row in rows:
        txn_id, debit, credit, desc, ref_type, created = row
        date_str = created.strftime("%Y-%m-%d %H:%M") if created else ""
        debit_str = f"${debit/100:.2f}" if debit else ""
        credit_str = f"${credit/100:.2f}" if credit else ""
        ref = ref_type or ""
        desc = (desc or "")[:30]
        print(f"{date_str:<20} {ref:<15} {debit_str:>10} {credit_str:>10} {desc}")


def ledger_integrity(args):
    """Check ledger integrity (debits must equal credits)."""
    from vikunja_mcp.budget_service import check_ledger_integrity

    result = check_ledger_integrity()

    print(f"\nLedger Integrity Check")
    print("-" * 40)
    print(f"Total Debits:  ${result['total_debits']/100:.2f}")
    print(f"Total Credits: ${result['total_credits']/100:.2f}")
    print(f"Imbalance:     ${result['imbalance']/100:.2f}")
    print()

    if result['is_balanced']:
        print("✓ Ledger is BALANCED")
    else:
        print("⚠️  Ledger is UNBALANCED - investigate immediately!")
        sys.exit(1)


def ledger_summary(args):
    """Show summary by account type."""
    from vikunja_mcp.token_broker import execute

    # Get summary by account prefix
    rows = execute("""
        SELECT
            SPLIT_PART(account, ':', 1) AS account_type,
            COUNT(DISTINCT account) AS num_accounts,
            SUM(debit_cents) AS total_debits,
            SUM(credit_cents) AS total_credits,
            COUNT(*) AS entries
        FROM ledger_entries
        GROUP BY SPLIT_PART(account, ':', 1)
        ORDER BY account_type
    """)

    print(f"\n{'Type':<15} {'Accounts':>10} {'Debits':>15} {'Credits':>15} {'Net':>15}")
    print("-" * 75)

    for row in rows:
        acct_type, num_accounts, debits, credits, entries = row
        debits = debits or 0
        credits = credits or 0
        net = credits - debits
        print(f"{acct_type:<15} {num_accounts:>10} ${debits/100:>13.2f} ${credits/100:>13.2f} ${net/100:>13.2f}")


def ledger_headroom(args):
    """Show available Anthropic credit headroom for new signups."""
    from vikunja_mcp.budget_service import get_anthropic_headroom

    headroom = get_anthropic_headroom()
    available = headroom['available_cents']

    print(f"\nAnthropic Credit Headroom")
    print("-" * 40)
    print(f"Anthropic asset:     ${headroom['asset_cents']/100:>10.2f}")
    print(f"User liabilities:    ${headroom['liability_cents']/100:>10.2f}")
    print(f"Available headroom:  ${available/100:>10.2f}")
    print()

    if available > 0:
        print(f"✓ Can provision new users up to ${available/100:.2f} total")
    elif available == 0:
        print(f"⚠ No headroom - fully allocated")
        print(f"  Purchase more Anthropic credits to enable signups")
    else:
        print(f"✗ Overcommitted by ${-available/100:.2f}")
        print(f"  Purchase more Anthropic credits or reduce user balances")


def ledger_purchase(args):
    """Record an Anthropic credit purchase."""
    import uuid
    from vikunja_mcp.token_broker import get_db

    amount = args.amount
    tax_rate = args.tax_rate / 100  # Convert percentage to decimal
    invoice_id = args.invoice or ""

    # Calculate amounts (round to nearest cent)
    credit_cents = round(amount * 100)
    tax_cents = round(amount * tax_rate * 100)
    total_cents = credit_cents + tax_cents

    print(f"\nRecording Anthropic credit purchase:")
    print(f"  Credit amount:  ${amount:.2f}")
    print(f"  Tax ({args.tax_rate}%):      ${tax_cents/100:.2f}")
    print(f"  Total paid:     ${total_cents/100:.2f}")
    if invoice_id:
        print(f"  Invoice:        {invoice_id}")
    print()

    if args.dry_run:
        print("[DRY RUN] No changes made.")
        return

    txn_id = str(uuid.uuid4())

    with get_db() as conn:
        with conn.cursor() as cur:
            # DEBIT equity:capital (owner invests)
            cur.execute("""
                INSERT INTO ledger_entries
                (transaction_id, account, debit_cents, credit_cents, description, reference_type, reference_id)
                VALUES (%s, 'equity:capital', %s, 0, %s, 'purchase', %s)
            """, (txn_id, total_cents, f"API credit purchase ${amount:.2f}", invoice_id or None))

            # CREDIT asset:anthropic (we gain credits)
            cur.execute("""
                INSERT INTO ledger_entries
                (transaction_id, account, debit_cents, credit_cents, description, reference_type, reference_id)
                VALUES (%s, 'asset:anthropic', 0, %s, %s, 'purchase', %s)
            """, (txn_id, credit_cents, f"API credit purchase ${amount:.2f}", invoice_id or None))

            # CREDIT expense:sales_tax (tax paid)
            if tax_cents > 0:
                cur.execute("""
                    INSERT INTO ledger_entries
                    (transaction_id, account, debit_cents, credit_cents, description, reference_type, reference_id)
                    VALUES (%s, 'expense:sales_tax', 0, %s, %s, 'purchase', %s)
                """, (txn_id, tax_cents, f"Sales tax on ${amount:.2f} purchase", invoice_id or None))

            conn.commit()

    print(f"✓ Purchase recorded (txn: {txn_id[:8]}...)")


# =============================================================================
# TOKEN COMMANDS
# =============================================================================


def tokens_list(args):
    """List all registration tokens."""
    from vikunja_mcp.token_broker import execute
    from datetime import datetime, timezone

    rows = execute("""
        SELECT token, state, max_uses, uses_remaining, expires_at, notes, initial_credit_cents, ttl_days
        FROM registration_tokens
        ORDER BY expires_at DESC NULLS LAST, token
    """)

    if not rows:
        print("No registration tokens found")
        return

    now = datetime.now(timezone.utc)

    print(f"\n{'Token':<35} {'State':<10} {'Uses':<10} {'Expires':<12} {'Credit':<8} {'Notes'}")
    print("-" * 110)

    for row in rows:
        token, state, max_uses, uses_remaining, expires_at, notes, credit_cents, ttl_days = row
        used = max_uses - uses_remaining
        uses_str = f"{used}/{max_uses}"

        if expires_at:
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if now > expires_at:
                exp_str = f"EXPIRED {expires_at.date()}"
            else:
                days_left = (expires_at - now).days
                exp_str = f"{expires_at.date()} ({days_left}d)"
        else:
            exp_str = "never"

        credit_str = f"${credit_cents/100:.0f}" if credit_cents else "-"
        notes_str = (notes or "")[:30]

        print(f"{token:<35} {state:<10} {uses_str:<10} {exp_str:<12} {credit_str:<8} {notes_str}")

    print(f"\nTotal: {len(rows)} tokens")


def tokens_show(args):
    """Show details for a specific registration token."""
    from vikunja_mcp.registration_tokens import get_token_stats, TokenNotFoundError
    from datetime import datetime, timezone

    try:
        stats = get_token_stats(args.token)
    except TokenNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    now = datetime.now(timezone.utc)

    print(f"\nToken: {stats['token']}")
    print(f"  State: {stats['state']}")
    print(f"  Max uses: {stats['max_uses']}")
    print(f"  Uses remaining: {stats['uses_remaining']}")
    print(f"  Used so far: {stats['used_count']}")

    if stats['expires_at']:
        expires_at = stats['expires_at']
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if now > expires_at:
            print(f"  Expires at: {expires_at} (EXPIRED)")
        else:
            days_left = (expires_at - now).days
            print(f"  Expires at: {expires_at} ({days_left} days left)")
    else:
        print(f"  Expires at: never")

    print(f"  Initial credit: ${stats['initial_credit_cents']/100:.2f}")
    if stats['ttl_days']:
        print(f"  Credit TTL: {stats['ttl_days']} days after signup")
    print(f"  Notes: {stats['notes'] or '-'}")

    if stats['recent_signups']:
        print(f"\n  Recent signups:")
        for signup in stats['recent_signups']:
            print(f"    - {signup['user_id']} ({signup['used_at']})")


def tokens_extend(args):
    """Extend a registration token's expiration date."""
    from vikunja_mcp.token_broker import get_db
    from vikunja_mcp.registration_tokens import get_token_stats, TokenNotFoundError
    from datetime import datetime, timezone, timedelta

    try:
        stats = get_token_stats(args.token)
    except TokenNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    now = datetime.now(timezone.utc)
    days = args.days

    # Calculate new expiration
    if args.from_now:
        # Extend from now
        new_expires = now + timedelta(days=days)
    else:
        # Extend from current expiration (or from now if already expired/no expiration)
        if stats['expires_at']:
            current = stats['expires_at']
            if current.tzinfo is None:
                current = current.replace(tzinfo=timezone.utc)
            if current < now:
                # Already expired, extend from now
                new_expires = now + timedelta(days=days)
            else:
                # Still valid, add days to current
                new_expires = current + timedelta(days=days)
        else:
            # No expiration set, extend from now
            new_expires = now + timedelta(days=days)

    print(f"\nExtending token: {args.token}")
    print(f"  Current expiration: {stats['expires_at'] or 'never'}")
    print(f"  New expiration: {new_expires}")
    print(f"  Days added: {days}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    with get_db() as conn:
        with conn.cursor() as cur:
            # Also reset state to 'active' if it was expired but has uses remaining
            cur.execute("""
                UPDATE registration_tokens
                SET expires_at = %s,
                    state = CASE
                        WHEN uses_remaining > 0 THEN 'active'
                        ELSE state
                    END
                WHERE token = %s
            """, (new_expires, args.token))
            conn.commit()

    print(f"\n✓ Token extended to {new_expires.date()}")


def tokens_delete(args):
    """Delete a registration token."""
    from vikunja_mcp.token_broker import get_db
    from vikunja_mcp.registration_tokens import get_token_stats, TokenNotFoundError

    try:
        stats = get_token_stats(args.token)
    except TokenNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\nDeleting token: {args.token}")
    print(f"  State: {stats['state']}")
    print(f"  Uses: {stats['used_count']}/{stats['max_uses']}")
    if stats['used_count'] > 0:
        print(f"  ⚠️  Warning: {stats['used_count']} signups used this token")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    if not args.force and stats['used_count'] > 0:
        confirm = input("\nThis token has been used. Type 'DELETE' to confirm: ")
        if confirm != "DELETE":
            print("Aborted.")
            sys.exit(1)

    with get_db() as conn:
        with conn.cursor() as cur:
            # Delete usage records first (foreign key)
            cur.execute("DELETE FROM token_usage WHERE token = %s", (args.token,))
            # Delete the token
            cur.execute("DELETE FROM registration_tokens WHERE token = %s", (args.token,))
            conn.commit()

    print(f"\n✓ Token deleted: {args.token}")


def tokens_create(args):
    """Create a new registration token."""
    from vikunja_mcp.token_broker import get_db
    from datetime import datetime, timezone, timedelta

    token = args.token
    max_uses = args.uses
    notes = args.notes or ""
    credit_dollars = args.credit
    ttl_days = args.ttl_days
    expires_days = args.expires_days

    credit_cents = int(credit_dollars * 100) if credit_dollars else 0
    expires_at = None
    if expires_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days)

    print(f"\nCreating registration token:")
    print(f"  Token: {token}")
    print(f"  Max uses: {max_uses}")
    print(f"  Initial credit: ${credit_cents/100:.2f}")
    print(f"  Credit TTL: {ttl_days} days" if ttl_days else "  Credit TTL: permanent")
    print(f"  Expires: {expires_at}" if expires_at else "  Expires: never")
    print(f"  Notes: {notes}" if notes else "  Notes: -")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO registration_tokens
                (token, state, max_uses, uses_remaining, expires_at, notes, initial_credit_cents, ttl_days)
                VALUES (%s, 'active', %s, %s, %s, %s, %s, %s)
            """, (token, max_uses, max_uses, expires_at, notes or None, credit_cents, ttl_days))
            conn.commit()

    print(f"\n✓ Token created: {token}")


def ledger_reconcile(args):
    """Reconcile asset:anthropic to actual Anthropic balance."""
    import uuid
    from vikunja_mcp.token_broker import get_db
    from vikunja_mcp.budget_service import get_account_balance

    target_cents = int(args.balance * 100)
    current_cents = get_account_balance("asset:anthropic")

    print(f"\nReconciling Anthropic asset:")
    print(f"  Current ledger:   ${current_cents/100:.2f}")
    print(f"  Actual balance:   ${target_cents/100:.2f}")

    diff_cents = current_cents - target_cents

    if diff_cents == 0:
        print(f"\n✓ Already in sync, no adjustment needed.")
        return

    if diff_cents > 0:
        # We've consumed more than recorded - write down
        print(f"  Adjustment:       -${diff_cents/100:.2f} (consumption)")
    else:
        # We have more than recorded - unusual, maybe refund?
        print(f"  Adjustment:       +${-diff_cents/100:.2f} (credit)")
        print(f"  ⚠️  Unusual: balance increased. Refund or correction?")

    print()

    if args.dry_run:
        print("[DRY RUN] No changes made.")
        return

    txn_id = str(uuid.uuid4())
    reason = args.reason or f"Monthly reconciliation to ${args.balance:.2f}"

    with get_db() as conn:
        with conn.cursor() as cur:
            if diff_cents > 0:
                # Write down: DEBIT asset (reduce), CREDIT expense (cost)
                cur.execute("""
                    INSERT INTO ledger_entries
                    (transaction_id, account, debit_cents, credit_cents, description, reference_type)
                    VALUES (%s, 'asset:anthropic', %s, 0, %s, 'reconcile')
                """, (txn_id, diff_cents, reason))
                cur.execute("""
                    INSERT INTO ledger_entries
                    (transaction_id, account, debit_cents, credit_cents, description, reference_type)
                    VALUES (%s, 'expense:anthropic', 0, %s, %s, 'reconcile')
                """, (txn_id, diff_cents, reason))
            else:
                # Credit adjustment: CREDIT asset (increase), DEBIT equity (correction)
                cur.execute("""
                    INSERT INTO ledger_entries
                    (transaction_id, account, debit_cents, credit_cents, description, reference_type)
                    VALUES (%s, 'asset:anthropic', 0, %s, %s, 'reconcile')
                """, (txn_id, -diff_cents, reason))
                cur.execute("""
                    INSERT INTO ledger_entries
                    (transaction_id, account, debit_cents, credit_cents, description, reference_type)
                    VALUES (%s, 'equity:adjustments', %s, 0, %s, 'reconcile')
                """, (txn_id, -diff_cents, reason))

            conn.commit()

    # Verify
    new_balance = get_account_balance("asset:anthropic")
    print(f"✓ Reconciled (txn: {txn_id[:8]}...)")
    print(f"  New ledger balance: ${new_balance/100:.2f}")


def vikunja_list_users(args):
    """List all Factumerit users with their bots."""
    from vikunja_mcp.token_broker import execute

    rows = execute(
        """
        SELECT
            fu.user_id,
            fu.email,
            fu.platform,
            fu.is_active,
            pb.bot_username,
            pb.vikunja_user_id
        FROM factumerit_users fu
        LEFT JOIN personal_bots pb ON fu.user_id = pb.user_id
        ORDER BY fu.registered_at DESC
        """
    )

    if not rows:
        print("No users found")
        return

    print(f"\n{'Email':<40} {'User ID':<30} {'Bot':<20} {'Active'}")
    print("-" * 100)

    for row in rows:
        user_id, email, platform, is_active, bot_username, vikunja_user_id = row
        email_display = (email or "")[:38]
        user_display = user_id[:28]
        bot_display = (bot_username or "-")[:18]
        active = "yes" if is_active else "no"
        print(f"{email_display:<40} {user_display:<30} {bot_display:<20} {active}")

    print(f"\nTotal: {len(rows)} users")


# =============================================================================
# Workspace Management Commands
# =============================================================================

def workspaces_list(args):
    """List all workspaces for a Google identity."""
    from vikunja_mcp.token_broker import get_user_workspaces, get_canonical_email

    email = args.email
    canonical = get_canonical_email(email)

    workspaces = get_user_workspaces(canonical)

    if not workspaces:
        print(f"\nNo workspaces found for: {canonical}")
        print("\nTo link existing accounts:")
        print(f"  fa workspaces link {canonical} vikunja:username --name 'My Workspace'")
        return

    print(f"\nWorkspaces for: {canonical}")
    print(f"\n{'User ID':<30} {'Workspace':<20} {'Primary':<10} {'Email'}")
    print("-" * 90)

    for ws in workspaces:
        primary = "★" if ws["is_primary"] else ""
        email_display = (ws["email"] or "-")[:30]
        print(f"{ws['user_id']:<30} {ws['workspace_name']:<20} {primary:<10} {email_display}")

    print(f"\nTotal: {len(workspaces)} workspace(s)")


def workspaces_link(args):
    """Link an existing Vikunja account to a Google identity."""
    from vikunja_mcp.token_broker import link_workspace, get_canonical_email, execute

    email = args.email
    user_id = args.user_id
    canonical = get_canonical_email(email)
    workspace_name = args.name
    is_primary = args.primary

    # Verify the user exists
    rows = execute(
        "SELECT user_id, email, is_active FROM factumerit_users WHERE user_id = %s",
        (user_id,)
    )

    if not rows:
        print(f"Error: User '{user_id}' not found in factumerit_users")
        print("\nAvailable users:")
        all_users = execute("SELECT user_id, email FROM factumerit_users WHERE is_active = TRUE ORDER BY user_id")
        for row in (all_users or []):
            print(f"  {row[0]:<30} {row[1] or '-'}")
        sys.exit(1)

    existing_email = rows[0][1]
    is_active = rows[0][2]

    if not is_active:
        print(f"Warning: User '{user_id}' is deactivated")

    print(f"\nLinking workspace:")
    print(f"  Google identity: {canonical}")
    print(f"  User ID: {user_id}")
    print(f"  Existing email: {existing_email or '-'}")
    print(f"  Workspace name: {workspace_name or 'Default'}")
    print(f"  Primary: {'yes' if is_primary else 'no'}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    success = link_workspace(canonical, user_id, workspace_name, is_primary)

    if success:
        print(f"\n✓ Linked {user_id} to {canonical}")
    else:
        print(f"\n✗ Failed to link workspace")
        sys.exit(1)


def workspaces_set_primary(args):
    """Set a workspace as primary for a Google identity."""
    from vikunja_mcp.token_broker import set_primary_workspace, get_canonical_email, get_user_workspaces

    email = args.email
    user_id = args.user_id
    canonical = get_canonical_email(email)

    # Verify user is linked to this identity
    workspaces = get_user_workspaces(canonical)
    linked_ids = [ws["user_id"] for ws in workspaces]

    if user_id not in linked_ids:
        print(f"Error: {user_id} is not linked to {canonical}")
        print(f"\nLinked workspaces:")
        for ws in workspaces:
            print(f"  {ws['user_id']}")
        sys.exit(1)

    current_primary = next((ws for ws in workspaces if ws["is_primary"]), None)

    print(f"\nSetting primary workspace:")
    print(f"  Google identity: {canonical}")
    print(f"  Current primary: {current_primary['user_id'] if current_primary else 'none'}")
    print(f"  New primary: {user_id}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    success = set_primary_workspace(canonical, user_id)

    if success:
        print(f"\n✓ Set {user_id} as primary for {canonical}")
    else:
        print(f"\n✗ Failed to set primary workspace")
        sys.exit(1)


def workspaces_unlink(args):
    """Unlink a workspace from its Google identity."""
    from vikunja_mcp.token_broker import execute, get_db

    user_id = args.user_id

    # Get current state
    rows = execute(
        "SELECT google_identity, workspace_name, is_primary FROM factumerit_users WHERE user_id = %s",
        (user_id,)
    )

    if not rows:
        print(f"Error: User '{user_id}' not found")
        sys.exit(1)

    google_identity, workspace_name, is_primary = rows[0]

    if not google_identity:
        print(f"User '{user_id}' is not linked to any Google identity")
        return

    print(f"\nUnlinking workspace:")
    print(f"  User ID: {user_id}")
    print(f"  Google identity: {google_identity}")
    print(f"  Workspace name: {workspace_name or 'Default'}")
    print(f"  Was primary: {'yes' if is_primary else 'no'}")

    if is_primary:
        print("\n⚠️  Warning: This is the primary workspace!")
        print("  External shares will no longer route to any workspace for this identity.")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    if not args.force:
        confirm = input("\nType 'unlink' to confirm: ")
        if confirm != "unlink":
            print("Cancelled.")
            return

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE factumerit_users SET google_identity = NULL, is_primary = FALSE WHERE user_id = %s",
                (user_id,)
            )
            conn.commit()

    print(f"\n✓ Unlinked {user_id} from {google_identity}")


def workspaces_show_all(args):
    """Show all users with their workspace info."""
    from vikunja_mcp.token_broker import execute

    rows = execute(
        """
        SELECT user_id, email, google_identity, workspace_name, is_primary, is_active
        FROM factumerit_users
        WHERE platform = 'vikunja'
        ORDER BY google_identity NULLS LAST, is_primary DESC, user_id
        """
    )

    if not rows:
        print("No vikunja users found")
        return

    print(f"\n{'User ID':<25} {'Workspace':<15} {'Google Identity':<30} {'Primary':<8} {'Active'}")
    print("-" * 100)

    current_identity = None
    for row in rows:
        user_id, email, google_identity, workspace_name, is_primary, is_active = row

        # Visual grouping by identity
        if google_identity != current_identity:
            if current_identity is not None:
                print()  # Blank line between groups
            current_identity = google_identity

        primary = "★" if is_primary else ""
        active = "yes" if is_active else "no"
        identity_display = (google_identity or "(unlinked)")[:28]
        workspace_display = (workspace_name or "Default")[:13]

        print(f"{user_id:<25} {workspace_display:<15} {identity_display:<30} {primary:<8} {active}")

    print(f"\nTotal: {len(rows)} users")


def main():
    parser = argparse.ArgumentParser(
        description="Factumerit Admin CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command group")

    # vikunja subcommand
    vikunja_parser = subparsers.add_parser("vikunja", help="Vikunja user management")
    vikunja_subparsers = vikunja_parser.add_subparsers(dest="vikunja_command")

    # vikunja delete-user
    delete_parser = vikunja_subparsers.add_parser(
        "delete-user", help="Delete a user completely (Vikunja + Factumerit)"
    )
    delete_parser.add_argument("email", help="User's email address")
    delete_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting",
    )
    delete_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Skip confirmation prompt (dangerous!)",
    )
    delete_parser.set_defaults(func=vikunja_delete_user)

    # vikunja list-users
    list_parser = vikunja_subparsers.add_parser(
        "list-users", help="List all users and their bots"
    )
    list_parser.set_defaults(func=vikunja_list_users)

    # ledger subcommand (fa-tn5s)
    ledger_parser = subparsers.add_parser("ledger", help="Double-entry ledger commands")
    ledger_subparsers = ledger_parser.add_subparsers(dest="ledger_command")

    # ledger balances
    balances_parser = ledger_subparsers.add_parser(
        "balances", help="Show all account balances"
    )
    balances_parser.set_defaults(func=ledger_balances)

    # ledger user
    user_parser = ledger_subparsers.add_parser(
        "user", help="Show ledger entries for a user"
    )
    user_parser.add_argument("user_id", help="User ID (e.g., vikunja:alice)")
    user_parser.add_argument("--limit", "-n", type=int, default=50, help="Max entries")
    user_parser.set_defaults(func=ledger_user)

    # ledger integrity
    integrity_parser = ledger_subparsers.add_parser(
        "integrity", help="Check ledger integrity (debits = credits)"
    )
    integrity_parser.set_defaults(func=ledger_integrity)

    # ledger summary
    summary_parser = ledger_subparsers.add_parser(
        "summary", help="Show summary by account type"
    )
    summary_parser.set_defaults(func=ledger_summary)

    # ledger headroom
    headroom_parser = ledger_subparsers.add_parser(
        "headroom", help="Show available Anthropic credit headroom for signups"
    )
    headroom_parser.set_defaults(func=ledger_headroom)

    # ledger purchase
    purchase_parser = ledger_subparsers.add_parser(
        "purchase", help="Record an Anthropic credit purchase"
    )
    purchase_parser.add_argument("amount", type=float, help="Credit amount in dollars (before tax)")
    purchase_parser.add_argument("--tax-rate", type=float, default=10.55, help="Tax rate %% (default: 10.55 for Seattle)")
    purchase_parser.add_argument("--invoice", help="Invoice ID for reference")
    purchase_parser.add_argument("--dry-run", action="store_true", help="Show what would be recorded")
    purchase_parser.set_defaults(func=ledger_purchase)

    # ledger reconcile
    reconcile_parser = ledger_subparsers.add_parser(
        "reconcile", help="Reconcile ledger to actual Anthropic balance"
    )
    reconcile_parser.add_argument("balance", type=float, help="Actual Anthropic balance in dollars")
    reconcile_parser.add_argument("--reason", help="Reason for reconciliation")
    reconcile_parser.add_argument("--dry-run", action="store_true", help="Show what would be adjusted")
    reconcile_parser.set_defaults(func=ledger_reconcile)

    # tokens subcommand
    tokens_parser = subparsers.add_parser("tokens", help="Registration token management")
    tokens_subparsers = tokens_parser.add_subparsers(dest="tokens_command")

    # tokens list
    tokens_list_parser = tokens_subparsers.add_parser(
        "list", help="List all registration tokens"
    )
    tokens_list_parser.set_defaults(func=tokens_list)

    # tokens show
    tokens_show_parser = tokens_subparsers.add_parser(
        "show", help="Show details for a specific token"
    )
    tokens_show_parser.add_argument("token", help="Registration token (e.g., TRAVEL-ADVENTURE-SEATTLE-2026)")
    tokens_show_parser.set_defaults(func=tokens_show)

    # tokens extend
    tokens_extend_parser = tokens_subparsers.add_parser(
        "extend", help="Extend a token's expiration date"
    )
    tokens_extend_parser.add_argument("token", help="Registration token to extend")
    tokens_extend_parser.add_argument("--days", "-d", type=int, required=True, help="Days to extend")
    tokens_extend_parser.add_argument("--from-now", action="store_true", help="Extend from now (not from current expiration)")
    tokens_extend_parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    tokens_extend_parser.set_defaults(func=tokens_extend)

    # tokens create
    tokens_create_parser = tokens_subparsers.add_parser(
        "create", help="Create a new registration token"
    )
    tokens_create_parser.add_argument("token", help="Token code (e.g., TINKERERS-JAN-2026)")
    tokens_create_parser.add_argument("--uses", "-u", type=int, default=50, help="Max uses (default: 50)")
    tokens_create_parser.add_argument("--credit", "-c", type=float, default=0, help="Initial credit in dollars (default: 0)")
    tokens_create_parser.add_argument("--ttl-days", type=int, help="Days until credit expires after signup")
    tokens_create_parser.add_argument("--expires-days", type=int, help="Days until token expires (default: never)")
    tokens_create_parser.add_argument("--notes", help="Notes about this token")
    tokens_create_parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    tokens_create_parser.set_defaults(func=tokens_create)

    # tokens delete
    tokens_delete_parser = tokens_subparsers.add_parser(
        "delete", help="Delete a registration token"
    )
    tokens_delete_parser.add_argument("token", help="Token to delete")
    tokens_delete_parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation for used tokens")
    tokens_delete_parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    tokens_delete_parser.set_defaults(func=tokens_delete)

    # workspaces subcommand (multi-account support)
    workspaces_parser = subparsers.add_parser("workspaces", help="Multi-account workspace management")
    workspaces_subparsers = workspaces_parser.add_subparsers(dest="workspaces_command")

    # workspaces list
    ws_list_parser = workspaces_subparsers.add_parser(
        "list", help="List workspaces for a Google identity"
    )
    ws_list_parser.add_argument("email", help="Google email (canonical or with +alias)")
    ws_list_parser.set_defaults(func=workspaces_list)

    # workspaces link
    ws_link_parser = workspaces_subparsers.add_parser(
        "link", help="Link an existing Vikunja account to a Google identity"
    )
    ws_link_parser.add_argument("email", help="Google email (canonical identity)")
    ws_link_parser.add_argument("user_id", help="Vikunja user ID (e.g., vikunja:ivan-personal)")
    ws_link_parser.add_argument("--name", "-n", help="Workspace display name")
    ws_link_parser.add_argument("--primary", "-p", action="store_true", help="Set as primary workspace")
    ws_link_parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    ws_link_parser.set_defaults(func=workspaces_link)

    # workspaces set-primary
    ws_primary_parser = workspaces_subparsers.add_parser(
        "set-primary", help="Set a workspace as primary for a Google identity"
    )
    ws_primary_parser.add_argument("email", help="Google email")
    ws_primary_parser.add_argument("user_id", help="User ID to make primary")
    ws_primary_parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    ws_primary_parser.set_defaults(func=workspaces_set_primary)

    # workspaces unlink
    ws_unlink_parser = workspaces_subparsers.add_parser(
        "unlink", help="Unlink a workspace from its Google identity"
    )
    ws_unlink_parser.add_argument("user_id", help="User ID to unlink")
    ws_unlink_parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation")
    ws_unlink_parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    ws_unlink_parser.set_defaults(func=workspaces_unlink)

    # workspaces show-all
    ws_all_parser = workspaces_subparsers.add_parser(
        "show-all", help="Show all users with their workspace info"
    )
    ws_all_parser.set_defaults(func=workspaces_show_all)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "vikunja" and not args.vikunja_command:
        vikunja_parser.print_help()
        sys.exit(1)

    if args.command == "ledger" and not args.ledger_command:
        ledger_parser.print_help()
        sys.exit(1)

    if args.command == "tokens" and not args.tokens_command:
        tokens_parser.print_help()
        sys.exit(1)

    if args.command == "workspaces" and not args.workspaces_command:
        workspaces_parser.print_help()
        sys.exit(1)

    # Check DATABASE_URL is set
    if not os.environ.get("DATABASE_URL"):
        print("Error: DATABASE_URL environment variable not set")
        print("Set it with: export DATABASE_URL='postgresql://...'")
        sys.exit(1)

    # Run the command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
