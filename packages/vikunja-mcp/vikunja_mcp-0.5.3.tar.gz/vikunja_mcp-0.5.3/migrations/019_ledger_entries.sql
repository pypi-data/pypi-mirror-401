-- Double-entry accounting ledger for API spending
-- Bead: fa-tn5s
--
-- Every transaction creates balanced debit/credit entries.
-- Sum of all debits must equal sum of all credits.
--
-- Chart of accounts:
--   user:{user_id}     - User balance (liability - what we owe them)
--   expense:api        - API costs (Anthropic spending)
--   equity:grants      - Admin credit grants
--   equity:initial     - Initial signup credit
--   equity:purchases   - (future) Paid credit purchases

CREATE TABLE IF NOT EXISTS ledger_entries (
    id SERIAL PRIMARY KEY,

    -- Transaction grouping (UUID links debit/credit pair)
    transaction_id UUID NOT NULL,

    -- Account being affected
    account TEXT NOT NULL,

    -- Only one of these should be non-zero per entry
    debit_cents INT NOT NULL DEFAULT 0,
    credit_cents INT NOT NULL DEFAULT 0,

    -- Metadata
    description TEXT,
    reference_type TEXT,  -- 'llm_call', 'admin_credit', 'initial', etc.
    reference_id TEXT,    -- optional: task_id, admin_id, etc.

    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Constraints
    CONSTRAINT positive_amounts CHECK (debit_cents >= 0 AND credit_cents >= 0),
    CONSTRAINT has_amount CHECK (debit_cents > 0 OR credit_cents > 0),
    CONSTRAINT single_side CHECK (NOT (debit_cents > 0 AND credit_cents > 0))
);

-- Indexes for common queries
CREATE INDEX idx_ledger_transaction ON ledger_entries(transaction_id);
CREATE INDEX idx_ledger_account ON ledger_entries(account);
CREATE INDEX idx_ledger_account_time ON ledger_entries(account, created_at DESC);
CREATE INDEX idx_ledger_reference ON ledger_entries(reference_type, reference_id)
    WHERE reference_id IS NOT NULL;

-- View: Account balances (credits - debits for each account)
CREATE OR REPLACE VIEW account_balances AS
SELECT
    account,
    SUM(credit_cents) - SUM(debit_cents) AS balance_cents,
    SUM(debit_cents) AS total_debits,
    SUM(credit_cents) AS total_credits,
    COUNT(*) AS entry_count
FROM ledger_entries
GROUP BY account;

-- View: User balances only (for quick lookup)
CREATE OR REPLACE VIEW user_ledger_balances AS
SELECT
    SUBSTRING(account FROM 6) AS user_id,  -- strip 'user:' prefix
    SUM(credit_cents) - SUM(debit_cents) AS balance_cents
FROM ledger_entries
WHERE account LIKE 'user:%'
GROUP BY account;

-- View: Integrity check (should always return 0)
CREATE OR REPLACE VIEW ledger_integrity AS
SELECT
    SUM(debit_cents) AS total_debits,
    SUM(credit_cents) AS total_credits,
    SUM(debit_cents) - SUM(credit_cents) AS imbalance
FROM ledger_entries;

COMMENT ON TABLE ledger_entries IS 'Double-entry accounting ledger for API spending (fa-tn5s)';
COMMENT ON VIEW account_balances IS 'Current balance for each account';
COMMENT ON VIEW user_ledger_balances IS 'Current balance for user accounts only';
COMMENT ON VIEW ledger_integrity IS 'Integrity check - imbalance should always be 0';
