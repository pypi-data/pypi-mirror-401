-- =============================================================================
-- Migration: User LLM Budgets
-- Date: 2025-12-31
-- Bead: solutions-rb74
-- =============================================================================
-- Per-user LLM credit system. Users get initial credit, LLM calls deduct.
-- When $0, LLM commands stop but ! commands still work.
--
-- Run with: psql $DATABASE_URL -f migrations/010_user_budgets.sql
-- =============================================================================

BEGIN;

-- User LLM budgets
-- References factumerit_users to avoid collision with Matrix Synapse's users table
CREATE TABLE IF NOT EXISTS user_budgets (
    user_id TEXT PRIMARY KEY REFERENCES factumerit_users(user_id),
    balance_cents INTEGER NOT NULL DEFAULT 100,  -- $1.00 initial credit
    total_spent_cents INTEGER NOT NULL DEFAULT 0,
    total_added_cents INTEGER NOT NULL DEFAULT 100,  -- Track total credits given
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Budget transaction log (for auditing)
CREATE TABLE IF NOT EXISTS budget_transactions (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES factumerit_users(user_id),
    amount_cents INTEGER NOT NULL,  -- Positive = credit, Negative = debit
    balance_after INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,  -- 'initial', 'llm_call', 'admin_credit', 'refund'
    description TEXT,  -- e.g., "LLM call: 1234 tokens" or "Admin credit from ivan"
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for user transaction history
CREATE INDEX IF NOT EXISTS idx_budget_transactions_user
    ON budget_transactions (user_id, created_at DESC);

-- Give all existing users $1.00 initial credit
INSERT INTO user_budgets (user_id, balance_cents, total_added_cents)
SELECT user_id, 100, 100
FROM factumerit_users
WHERE is_active = TRUE
ON CONFLICT (user_id) DO NOTHING;

-- Log initial credit for existing users
INSERT INTO budget_transactions (user_id, amount_cents, balance_after, transaction_type, description)
SELECT user_id, 100, 100, 'initial', 'Migration: initial $1.00 credit'
FROM factumerit_users
WHERE is_active = TRUE
  AND user_id NOT IN (SELECT user_id FROM budget_transactions);

-- Record this migration
INSERT INTO token_broker_migrations (version, description)
VALUES (10, 'User LLM budgets with transaction log')
ON CONFLICT (version) DO NOTHING;

COMMIT;
