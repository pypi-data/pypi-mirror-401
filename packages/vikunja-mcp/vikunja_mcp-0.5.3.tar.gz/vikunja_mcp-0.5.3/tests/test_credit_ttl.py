"""
Tests for Credit TTL expiration (fa-i5cv).

TDD: These tests define the expected behavior before implementation.
"""
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

# These imports will fail until implementation exists
# That's the point of TDD - tests first!


class TestCreditTTL:
    """Test credit expiration based on TTL."""

    def test_token_with_ttl_creates_expiring_credit(self):
        """Token with --ttl 7 creates credit that expires 7 days after signup."""
        from vikunja_mcp.budget_service import ensure_user_budget, get_user_budget

        # Mock: User signs up with a token that has ttl_days=7
        user_id = "test:ttl_user"
        initial_credit = 100  # $1.00
        ttl_days = 7

        # When user signs up, promo_expires_at should be set
        budget = ensure_user_budget(
            user_id,
            initial_credit_cents=initial_credit,
            promo_ttl_days=ttl_days,
            override_headroom_check=True
        )

        assert budget.balance_cents == initial_credit
        assert budget.promo_expires_at is not None

        # Should expire ~7 days from now
        expected_expiry = datetime.now(timezone.utc) + timedelta(days=7)
        assert abs((budget.promo_expires_at - expected_expiry).total_seconds()) < 60

    def test_token_without_ttl_creates_permanent_credit(self):
        """Token without TTL creates credit that never expires."""
        from vikunja_mcp.budget_service import ensure_user_budget

        user_id = "test:permanent_user"
        initial_credit = 100

        budget = ensure_user_budget(
            user_id,
            initial_credit_cents=initial_credit,
            promo_ttl_days=None,  # No TTL
            override_headroom_check=True
        )

        assert budget.balance_cents == initial_credit
        assert budget.promo_expires_at is None  # Never expires

    def test_expired_promo_credit_is_forfeited(self):
        """When promo credit expires, balance should be zeroed."""
        from vikunja_mcp.budget_service import (
            ensure_user_budget,
            check_and_expire_promo,
            get_user_budget
        )

        user_id = "test:expired_user"

        # Create budget with already-expired promo
        with patch('vikunja_mcp.budget_service.datetime') as mock_dt:
            # Set "now" to 8 days ago when creating
            past = datetime.now(timezone.utc) - timedelta(days=8)
            mock_dt.now.return_value = past
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

            budget = ensure_user_budget(
                user_id,
                initial_credit_cents=100,
                promo_ttl_days=7,
                override_headroom_check=True
            )

        # Now check - promo should be expired
        result = check_and_expire_promo(user_id)

        assert result['expired'] is True
        assert result['forfeited_cents'] == 100

        # Balance should now be 0
        budget = get_user_budget(user_id)
        assert budget.balance_cents == 0

    def test_check_budget_blocks_expired_promo(self):
        """check_budget returns False for expired promo credit."""
        from vikunja_mcp.budget_service import check_budget

        # User with expired promo should be blocked
        # (This requires mocking the expiration check)
        pass  # Implementation will flesh this out

    def test_deduct_credit_fails_for_expired_promo(self):
        """Cannot deduct from expired promo credit."""
        from vikunja_mcp.budget_service import (
            ensure_user_budget,
            deduct_credit,
            InsufficientCreditError
        )

        user_id = "test:expired_deduct"

        # Create budget with expired promo (in the past)
        # Then try to deduct - should raise InsufficientCreditError
        pass  # Implementation will flesh this out

    def test_expired_promo_recorded_in_ledger(self):
        """Expired promo forfeiture is recorded in double-entry ledger."""
        from vikunja_mcp.budget_service import (
            ensure_user_budget,
            check_and_expire_promo,
            get_account_balance
        )

        user_id = "test:ledger_forfeit"

        # Create and expire promo
        # Check that equity:expired account received the forfeited amount
        pass  # Implementation will flesh this out


class TestWalletCLI:
    """Test wallet CLI --ttl parameter."""

    def test_wallet_create_with_ttl(self):
        """wallet create --ttl 7 sets ttl_days on token."""
        # This tests the CLI/database layer
        pass

    def test_token_ttl_propagates_to_signup(self):
        """When user signs up with TTL token, promo_expires_at is set."""
        pass


class TestRegistrationTokenTTL:
    """Test registration token TTL field."""

    def test_validate_token_returns_ttl_days(self):
        """validate_registration_token returns ttl_days in token data."""
        from vikunja_mcp.registration_tokens import validate_registration_token

        # Token with TTL should return ttl_days in result
        pass

    def test_token_without_ttl_returns_none(self):
        """Token without TTL returns None for ttl_days."""
        pass
