# Double-Entry Accounting Ledger

Factumerit uses a double-entry accounting system to track LLM API spending. Every transaction creates balanced debit and credit entries - the sum of all debits always equals the sum of all credits.

## Chart of Accounts

| Account | Type | Description |
|---------|------|-------------|
| `user:{user_id}` | Liability | What we owe the user (their credit balance) |
| `asset:anthropic` | Asset | Prepaid API credits from Anthropic |
| `expense:api` | Expense | API costs attributed to users |
| `expense:anthropic` | Expense | Real API costs (Anthropic consumption) |
| `expense:sales_tax` | Expense | Sales tax on credit purchases |
| `equity:initial` | Equity | Initial signup credit granted |
| `equity:grants` | Equity | Admin-granted credit |
| `equity:forfeit` | Equity | Reclaimed from deleted accounts |
| `equity:capital` | Equity | Owner contributions (credit purchases) |

## Transaction Types

### 1. New User Signup (Initial Credit)

When a user account is created with initial credit (configurable, default $0):

```
DEBIT  equity:initial     $X.XX   (we give away value)
CREDIT user:{user_id}     $X.XX   (we owe them credit)
```

The amount is specified via `initial_credit_cents` parameter. Test accounts can be created with $0 initial credit. Production accounts typically receive credit during registration.

**Code**: `ensure_user_budget(user_id, initial_credit_cents=100)` in `budget_service.py`

### 2. LLM API Call (Spending)

When a user's bot makes an LLM call, the cost is deducted from their balance.

```
DEBIT  user:{user_id}     $0.05   (reduce what we owe them)
CREDIT expense:api        $0.05   (record the cost)
```

**Code**: `deduct_credit()` in `budget_service.py`

### 3. Admin Credit Grant

When an admin adds credit to a user's account.

```
DEBIT  equity:grants      $5.00   (we give away value)
CREDIT user:{user_id}     $5.00   (we owe them more credit)
```

**Code**: `add_credit()` in `budget_service.py`

### 4. Owner Purchases API Credits

When the owner buys Anthropic credits (including sales tax).

```
DEBIT  equity:capital      $27.59   (owner invests capital)
CREDIT asset:anthropic     $25.00   (API credits received)
CREDIT expense:sales_tax    $2.59   (non-recoverable tax)
```

**Code**: Manual entry via SQL (opening balances)

### 5. Anthropic Credit Consumption (Write-down)

Periodic reconciliation to match actual Anthropic balance.

```
DEBIT  asset:anthropic      $X.XX   (asset consumed)
CREDIT expense:anthropic    $X.XX   (real cost incurred)
```

**Code**: Manual entry via SQL (reconciliation)

### 6. User Account Deletion (Forfeit)

When a user account is deleted, any unspent balance is forfeited.

```
DEBIT  user:{user_id}       $0.50   (zero out liability)
CREDIT equity:forfeit       $0.50   (reclaim unused grant)
```

The asset is NOT touched - we never consumed those Anthropic credits.

**Code**: `forfeit_balance()` in `budget_service.py`, called by `delete_user()`

## Understanding the Entries

### Why User Accounts are Liabilities

User balances represent what Factumerit "owes" users in API access. When users have credit, we have a liability to provide that service.

- **Credit to user account** = Balance increases (we owe them more)
- **Debit to user account** = Balance decreases (they spent some)

### Balance Calculation

For any account: `Balance = Sum(Credits) - Sum(Debits)`

- **User accounts**: Positive balance = credit remaining
- **Expense accounts**: Positive balance = total costs incurred
- **Equity accounts**: Negative balance = value given away (normal for equity)

## CLI Commands

```bash
# View all account balances
fa ledger balances

# View a specific user's transactions
fa ledger user vikunja:alice

# Verify ledger integrity (debits must equal credits)
fa ledger integrity

# Summary by account type
fa ledger summary

# Check signup headroom (Anthropic credits vs user liabilities)
fa ledger headroom
```

## Signup Provisioning Check

Before granting initial credit to new users, the system checks:

```
Available = asset:anthropic - sum(user:* balances)
Can signup = Available >= requested_initial_credit
```

If insufficient Anthropic credits for the requested amount, signup is blocked with `InsufficientAnthropicCreditsError`. Use `override_headroom_check=True` for testing only.

Accounts created with `initial_credit_cents=0` skip the headroom check entirely.

## Database Schema

```sql
CREATE TABLE ledger_entries (
    id SERIAL PRIMARY KEY,
    transaction_id UUID NOT NULL,      -- Groups debit/credit pair
    account TEXT NOT NULL,             -- e.g., 'user:vikunja:alice'
    debit_cents INT DEFAULT 0,
    credit_cents INT DEFAULT 0,
    description TEXT,
    reference_type TEXT,               -- 'llm_call', 'admin_credit', 'initial'
    reference_id TEXT,                 -- Optional: task_id, admin_id
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Constraints**:
- Only debit OR credit can be non-zero (not both)
- At least one must be non-zero
- Both must be non-negative

## Views

| View | Purpose |
|------|---------|
| `account_balances` | Current balance for each account |
| `user_ledger_balances` | Balances for user accounts only |
| `ledger_integrity` | Sum of debits, credits, and imbalance (should be 0) |

## Integrity

The ledger must always balance. Check with:

```bash
fa ledger integrity
```

If `imbalance != 0`, something is broken - investigate immediately.

## Migration from Legacy System

The legacy `user_budgets` and `budget_transactions` tables continue to work alongside the ledger. Both are updated on each transaction for backwards compatibility.

Transactions that occurred before the ledger was implemented (pre-migration 019) only exist in the legacy tables. The ledger starts empty and accumulates entries going forward.
