"""
User LLM Budget Service.

Tracks per-user LLM credit. Users get initial credit ($1.00),
LLM calls deduct from balance. When $0, LLM commands stop.

Bead: solutions-rb74
"""

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional

from psycopg.rows import dict_row

from .token_broker import get_db

logger = logging.getLogger(__name__)


# =============================================================================
# DOUBLE-ENTRY LEDGER (fa-tn5s)
# =============================================================================
# Every transaction creates balanced debit/credit entries.
# Chart of accounts:
#   user:{user_id}   - User balance (liability)
#   expense:api      - API costs
#   equity:grants    - Admin credit grants
#   equity:initial   - Initial signup credit
# =============================================================================

def _record_ledger_entry(
    cur,
    transaction_id: uuid.UUID,
    debit_account: str,
    credit_account: str,
    amount_cents: int,
    description: str,
    reference_type: str = None,
    reference_id: str = None
) -> None:
    """Record a balanced double-entry transaction.

    Creates two entries: debit to one account, credit to another.
    Sum of debits always equals sum of credits.

    Args:
        cur: Database cursor (must be in a transaction)
        transaction_id: UUID grouping the debit/credit pair
        debit_account: Account to debit (e.g., 'user:alice')
        credit_account: Account to credit (e.g., 'expense:api')
        amount_cents: Amount in cents (must be positive)
        description: Human-readable description
        reference_type: Optional type (llm_call, admin_credit, initial)
        reference_id: Optional reference (task_id, admin_id, etc.)
    """
    if amount_cents <= 0:
        return  # Nothing to record

    # Debit entry
    cur.execute("""
        INSERT INTO ledger_entries
        (transaction_id, account, debit_cents, credit_cents, description, reference_type, reference_id)
        VALUES (%s, %s, %s, 0, %s, %s, %s)
    """, (str(transaction_id), debit_account, amount_cents, description, reference_type, reference_id))

    # Credit entry
    cur.execute("""
        INSERT INTO ledger_entries
        (transaction_id, account, debit_cents, credit_cents, description, reference_type, reference_id)
        VALUES (%s, %s, 0, %s, %s, %s, %s)
    """, (str(transaction_id), credit_account, amount_cents, description, reference_type, reference_id))


def check_ledger_integrity() -> dict:
    """Check that ledger is balanced (sum of debits = sum of credits).

    Returns:
        dict with total_debits, total_credits, imbalance, is_balanced
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM ledger_integrity")
            row = cur.fetchone()
            return {
                "total_debits": row["total_debits"] or 0,
                "total_credits": row["total_credits"] or 0,
                "imbalance": row["imbalance"] or 0,
                "is_balanced": (row["imbalance"] or 0) == 0
            }


def get_account_balance(account: str) -> int:
    """Get current balance for an account from ledger.

    Args:
        account: Account name (e.g., 'user:alice', 'expense:api')

    Returns:
        Balance in cents (credits - debits)
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT COALESCE(SUM(credit_cents) - SUM(debit_cents), 0) AS balance
                FROM ledger_entries
                WHERE account = %s
            """, (account,))
            row = cur.fetchone()
            return row["balance"]


def get_user_ledger_balance(user_id: str) -> int:
    """Get user's balance from ledger (convenience wrapper).

    Args:
        user_id: User identifier (without 'user:' prefix)

    Returns:
        Balance in cents
    """
    return get_account_balance(f"user:{user_id}")


@dataclass
class BudgetInfo:
    """User budget information."""
    user_id: str
    balance_cents: int
    total_spent_cents: int
    total_added_cents: int
    promo_expires_at: Optional[datetime] = None

    @property
    def balance_dollars(self) -> float:
        """Balance in dollars."""
        return self.balance_cents / 100

    @property
    def has_credit(self) -> bool:
        """True if user has any credit remaining."""
        return self.balance_cents > 0

    @property
    def is_promo_expired(self) -> bool:
        """True if promo credit has expired."""
        if self.promo_expires_at is None:
            return False
        now = datetime.now(timezone.utc)
        expires = self.promo_expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return now > expires

    def format_balance(self) -> str:
        """Format balance for display."""
        return f"${self.balance_cents / 100:.2f}"


class InsufficientCreditError(Exception):
    """User has no credit remaining."""
    pass


class InsufficientAnthropicCreditsError(Exception):
    """Not enough Anthropic credits to cover new user signup."""
    pass


def get_anthropic_headroom() -> dict:
    """Get available Anthropic credit headroom.

    Calculates: asset:anthropic - sum(all user liabilities)

    Uses user_budgets table for liabilities (complete history),
    and ledger for asset:anthropic (manually maintained).

    Returns:
        dict with asset_cents, liability_cents, available_cents
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Get Anthropic asset balance from ledger
            cur.execute("""
                SELECT COALESCE(SUM(credit_cents) - SUM(debit_cents), 0) AS balance
                FROM ledger_entries
                WHERE account = 'asset:anthropic'
            """)
            asset_cents = cur.fetchone()["balance"]

            # Get total user liabilities from user_budgets (source of truth)
            cur.execute("""
                SELECT COALESCE(SUM(balance_cents), 0) AS total
                FROM user_budgets
            """)
            liability_cents = cur.fetchone()["total"]

            available_cents = asset_cents - liability_cents

            return {
                "asset_cents": asset_cents,
                "liability_cents": liability_cents,
                "available_cents": available_cents,
            }


def get_user_budget(user_id: str) -> Optional[BudgetInfo]:
    """Get user's current budget.

    Args:
        user_id: User identifier

    Returns:
        BudgetInfo or None if user not found
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT user_id, balance_cents, total_spent_cents, total_added_cents, promo_expires_at
                FROM user_budgets
                WHERE user_id = %s
            """, (user_id,))

            row = cur.fetchone()
            if not row:
                return None

            return BudgetInfo(**row)


def _ensure_user_exists(user_id: str) -> None:
    """Ensure user exists in factumerit_users table.

    Creates the user if they don't exist (auto-registration on first LLM use).

    Args:
        user_id: User identifier (e.g., "vikunja:username")
    """
    # Determine platform from user_id format
    if user_id.startswith("vikunja:"):
        platform = "vikunja"
    elif user_id.startswith("@") and ":" in user_id:
        platform = "matrix"
    else:
        platform = "slack"

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO factumerit_users (user_id, platform, registered_via)
                VALUES (%s, %s, 'auto')
                ON CONFLICT (user_id) DO NOTHING
            """, (user_id, platform))
            conn.commit()


def ensure_user_budget(
    user_id: str,
    initial_credit_cents: int = 0,
    promo_ttl_days: int | None = None,
    override_headroom_check: bool = False
) -> BudgetInfo:
    """Get or create user budget with optional initial credit.

    Args:
        user_id: User identifier
        initial_credit_cents: Initial credit to grant (default 0 for test accounts)
        promo_ttl_days: Days until promo credit expires (None = never expires)
        override_headroom_check: If True, skip Anthropic balance check

    Returns:
        BudgetInfo (existing or newly created)

    Raises:
        InsufficientAnthropicCreditsError: If not enough Anthropic credits to cover
            the initial credit (unless override_headroom_check=True or amount is 0)
    """
    budget = get_user_budget(user_id)
    if budget:
        return budget

    # Check if we have enough Anthropic credits to cover this new user
    if initial_credit_cents > 0 and not override_headroom_check:
        headroom = get_anthropic_headroom()
        if headroom["available_cents"] < initial_credit_cents:
            available = headroom["available_cents"] / 100
            needed = initial_credit_cents / 100
            raise InsufficientAnthropicCreditsError(
                f"Cannot provision user with ${needed:.2f}: insufficient Anthropic credits. "
                f"Available headroom: ${available:.2f}. "
                f"Purchase more Anthropic credits or reduce initial_credit_cents."
            )

    # Ensure user exists in factumerit_users (FK constraint)
    _ensure_user_exists(user_id)

    # Calculate promo expiration if TTL specified
    promo_expires_at = None
    if promo_ttl_days is not None and promo_ttl_days > 0:
        promo_expires_at = datetime.now(timezone.utc) + timedelta(days=promo_ttl_days)

    # Create new budget with initial credit
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Insert budget
            cur.execute("""
                INSERT INTO user_budgets (user_id, balance_cents, total_added_cents, promo_expires_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
                RETURNING user_id, balance_cents, total_spent_cents, total_added_cents, promo_expires_at
            """, (user_id, initial_credit_cents, initial_credit_cents, promo_expires_at))

            row = cur.fetchone()

            if row and initial_credit_cents > 0:
                # Log initial credit (legacy single-entry)
                ttl_note = f" (expires in {promo_ttl_days} days)" if promo_ttl_days else ""
                cur.execute("""
                    INSERT INTO budget_transactions
                    (user_id, amount_cents, balance_after, transaction_type, description)
                    VALUES (%s, %s, %s, 'initial', %s)
                """, (user_id, initial_credit_cents, initial_credit_cents, f"Initial credit{ttl_note}"))

                # Double-entry ledger (fa-tn5s)
                # Initial credit: debit equity (give away value), credit user (owe them)
                txn_id = uuid.uuid4()
                _record_ledger_entry(
                    cur,
                    transaction_id=txn_id,
                    debit_account="equity:initial",
                    credit_account=f"user:{user_id}",
                    amount_cents=initial_credit_cents,
                    description=f"Initial signup credit (${initial_credit_cents/100:.2f}){ttl_note}",
                    reference_type="initial"
                )

            conn.commit()
            if row:
                return BudgetInfo(**row)

            # Race condition: another process created it
            conn.rollback()
            return get_user_budget(user_id)


def check_and_expire_promo(user_id: str) -> dict:
    """Check if user's promo credit has expired and forfeit if so.

    Args:
        user_id: User identifier

    Returns:
        dict with 'expired' (bool) and 'forfeited_cents' (int)
    """
    budget = get_user_budget(user_id)
    if not budget:
        return {"expired": False, "forfeited_cents": 0}

    if not budget.is_promo_expired:
        return {"expired": False, "forfeited_cents": 0}

    # Promo has expired - forfeit remaining balance
    if budget.balance_cents <= 0:
        return {"expired": True, "forfeited_cents": 0}

    amount = budget.balance_cents

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Zero out the balance
            cur.execute("""
                UPDATE user_budgets
                SET balance_cents = 0,
                    updated_at = NOW()
                WHERE user_id = %s
            """, (user_id,))

            # Log transaction
            cur.execute("""
                INSERT INTO budget_transactions
                (user_id, amount_cents, balance_after, transaction_type, description)
                VALUES (%s, %s, 0, 'expire', 'Promo credit expired')
            """, (user_id, -amount))

            # Double-entry ledger: reclaim expired promo
            txn_id = uuid.uuid4()
            _record_ledger_entry(
                cur,
                transaction_id=txn_id,
                debit_account=f"user:{user_id}",
                credit_account="equity:expired",
                amount_cents=amount,
                description=f"Promo credit expired (${amount/100:.2f})",
                reference_type="expire"
            )

            conn.commit()

            logger.info(f"Promo expired: {user_id} forfeited {amount}¢")

    return {"expired": True, "forfeited_cents": amount}


def check_budget(user_id: str) -> bool:
    """Check if user has any credit remaining.

    Also checks for expired promo credits and forfeits them.

    Args:
        user_id: User identifier

    Returns:
        True if user has credit, False otherwise
    """
    # First check for expired promo and forfeit if needed
    check_and_expire_promo(user_id)

    budget = get_user_budget(user_id)
    if not budget:
        # User not in system - allow (will be added on first deduct)
        return True
    return budget.has_credit


def deduct_credit(
    user_id: str,
    amount_cents: int,
    description: str = "LLM call"
) -> BudgetInfo:
    """Deduct credit from user's balance.

    Args:
        user_id: User identifier
        amount_cents: Amount to deduct (in cents)
        description: Transaction description

    Returns:
        Updated BudgetInfo

    Raises:
        InsufficientCreditError: If user has no credit
    """
    if amount_cents <= 0:
        # Free operation, no deduction needed
        return ensure_user_budget(user_id)

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Check current balance
            cur.execute("""
                SELECT balance_cents FROM user_budgets
                WHERE user_id = %s
                FOR UPDATE
            """, (user_id,))

            row = cur.fetchone()

            if not row:
                # Create budget first
                conn.rollback()
                ensure_user_budget(user_id)
                return deduct_credit(user_id, amount_cents, description)

            if row['balance_cents'] <= 0:
                conn.rollback()
                raise InsufficientCreditError(
                    f"No credit remaining. Balance: $0.00"
                )

            # Deduct (allow going negative for this call, but block future calls)
            new_balance = row['balance_cents'] - amount_cents

            cur.execute("""
                UPDATE user_budgets
                SET balance_cents = %s,
                    total_spent_cents = total_spent_cents + %s,
                    updated_at = NOW()
                WHERE user_id = %s
                RETURNING user_id, balance_cents, total_spent_cents, total_added_cents
            """, (new_balance, amount_cents, user_id))

            updated = cur.fetchone()

            # Log transaction (legacy single-entry)
            cur.execute("""
                INSERT INTO budget_transactions
                (user_id, amount_cents, balance_after, transaction_type, description)
                VALUES (%s, %s, %s, 'llm_call', %s)
            """, (user_id, -amount_cents, new_balance, description))

            # Double-entry ledger (fa-tn5s)
            # LLM call: debit user (reduce liability), credit expense (record cost)
            txn_id = uuid.uuid4()
            _record_ledger_entry(
                cur,
                transaction_id=txn_id,
                debit_account=f"user:{user_id}",
                credit_account="expense:api",
                amount_cents=amount_cents,
                description=description,
                reference_type="llm_call"
            )

            # Also consume from Anthropic asset (real cost)
            _record_ledger_entry(
                cur,
                transaction_id=txn_id,
                debit_account="asset:anthropic",
                credit_account="expense:anthropic",
                amount_cents=amount_cents,
                description=description,
                reference_type="llm_call"
            )

            conn.commit()

            logger.info(
                f"Budget deduct: {user_id} -{amount_cents}¢ = {new_balance}¢ ({description})"
            )

            return BudgetInfo(**updated)


def add_credit(
    user_id: str,
    amount_cents: int,
    admin_id: str,
    reason: str = "Admin credit"
) -> BudgetInfo:
    """Add credit to user's balance (admin only).

    Args:
        user_id: User identifier
        amount_cents: Amount to add (in cents)
        admin_id: Admin who added the credit
        reason: Reason for credit

    Returns:
        Updated BudgetInfo
    """
    # Ensure user has a budget row
    ensure_user_budget(user_id)

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                UPDATE user_budgets
                SET balance_cents = balance_cents + %s,
                    total_added_cents = total_added_cents + %s,
                    updated_at = NOW()
                WHERE user_id = %s
                RETURNING user_id, balance_cents, total_spent_cents, total_added_cents
            """, (amount_cents, amount_cents, user_id))

            updated = cur.fetchone()

            # Log transaction (legacy single-entry)
            description = f"{reason} (by {admin_id})"
            cur.execute("""
                INSERT INTO budget_transactions
                (user_id, amount_cents, balance_after, transaction_type, description)
                VALUES (%s, %s, %s, 'admin_credit', %s)
            """, (user_id, amount_cents, updated['balance_cents'], description))

            # Double-entry ledger (fa-tn5s)
            # Admin grant: debit equity (give away value), credit user (owe them more)
            txn_id = uuid.uuid4()
            _record_ledger_entry(
                cur,
                transaction_id=txn_id,
                debit_account="equity:grants",
                credit_account=f"user:{user_id}",
                amount_cents=amount_cents,
                description=description,
                reference_type="admin_credit",
                reference_id=admin_id
            )

            conn.commit()

            logger.info(
                f"Budget credit: {user_id} +{amount_cents}¢ = {updated['balance_cents']}¢ ({description})"
            )

            return BudgetInfo(**updated)


def forfeit_balance(user_id: str, reason: str = "Account deleted") -> int:
    """Forfeit a user's remaining balance (on account deletion).

    Zeros out the user's balance and records the forfeit in the ledger.
    The forfeited amount returns to equity (we no longer owe them).

    Args:
        user_id: User identifier
        reason: Reason for forfeit

    Returns:
        Amount forfeited in cents (0 if no balance)
    """
    budget = get_user_budget(user_id)
    if not budget or budget.balance_cents <= 0:
        return 0

    amount_cents = budget.balance_cents

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Zero out the balance
            cur.execute("""
                UPDATE user_budgets
                SET balance_cents = 0,
                    updated_at = NOW()
                WHERE user_id = %s
            """, (user_id,))

            # Log transaction (legacy single-entry)
            cur.execute("""
                INSERT INTO budget_transactions
                (user_id, amount_cents, balance_after, transaction_type, description)
                VALUES (%s, %s, 0, 'forfeit', %s)
            """, (user_id, -amount_cents, reason))

            # Double-entry ledger
            # Forfeit: debit user (zero out liability), credit equity (reclaim)
            txn_id = uuid.uuid4()
            _record_ledger_entry(
                cur,
                transaction_id=txn_id,
                debit_account=f"user:{user_id}",
                credit_account="equity:forfeit",
                amount_cents=amount_cents,
                description=reason,
                reference_type="forfeit"
            )

            conn.commit()

            logger.info(
                f"Budget forfeit: {user_id} -{amount_cents}¢ ({reason})"
            )

            return amount_cents


def get_transaction_history(user_id: str, limit: int = 20) -> list[dict]:
    """Get recent transactions for a user.

    Args:
        user_id: User identifier
        limit: Max transactions to return

    Returns:
        List of transaction dicts
    """
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT amount_cents, balance_after, transaction_type,
                       description, created_at
                FROM budget_transactions
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, limit))

            return [dict(row) for row in cur.fetchall()]


def estimate_cost_cents(input_tokens: int, output_tokens: int) -> int:
    """Estimate cost of an LLM call in cents.

    Uses Claude Sonnet 4 pricing:
    - Input: $3/1M tokens = $0.000003/token
    - Output: $15/1M tokens = $0.000015/token

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in cents (rounded up)
    """
    # Sonnet pricing per token
    input_cost = input_tokens * 0.000003
    output_cost = output_tokens * 0.000015
    total_dollars = input_cost + output_cost

    # Convert to cents, round up to nearest cent
    import math
    return max(1, math.ceil(total_dollars * 100))
