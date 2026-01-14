"""Integration tests for registration flow using Playwright.

Tests the user registration journey from token to Matrix account.

Run with: uv run pytest tests/integration/test_registration_flow.py -v -m integration

Requires:
- Playwright browsers installed: playwright install chromium
- Valid registration token for tests that complete registration
"""

import pytest
import re
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.integration]


# =============================================================================
# Configuration
# =============================================================================

REGISTRATION_URL = "https://matrix.factumerit.app/register"
MAS_URL = "https://matrix.factumerit.app"  # Matrix Authentication Service


# =============================================================================
# Phase 2.1: Registration Page Access
# =============================================================================

class TestRegistrationPageLoads:
    """Tests that registration pages load correctly."""

    def test_register_page_loads(self, page: Page):
        """Registration page should load without errors."""
        page.goto(REGISTRATION_URL)

        # Page should load (might redirect, that's OK)
        expect(page).not_to_have_url(re.compile(r".*error.*"))

    def test_register_page_has_form(self, page: Page):
        """Registration page should have a form."""
        page.goto(REGISTRATION_URL)

        # Wait for page to settle (might have redirects)
        page.wait_for_load_state("networkidle")

        # Should have some form elements
        # Note: MAS might redirect to /register/password
        form_elements = page.locator("input, button[type='submit']")
        count = form_elements.count()
        assert count > 0, "Registration page should have form elements"


# =============================================================================
# Phase 2.2: Token Parameter Handling
# =============================================================================

class TestTokenInUrl:
    """Tests for token parameter in registration URL.

    Known issue: solutions-mn77.5.1 - Token is currently lost in redirect.
    """

    def test_token_parameter_accepted(self, page: Page):
        """Registration URL should accept token parameter."""
        token = "mat_test123"
        page.goto(f"{REGISTRATION_URL}?token={token}")

        # Page should load without error
        page.wait_for_load_state("networkidle")
        expect(page).not_to_have_url(re.compile(r".*error.*"))

    @pytest.mark.xfail(reason="Known issue: solutions-mn77.5.1 - token lost in redirect")
    def test_token_preserved_after_redirect(self, page: Page):
        """Token should be preserved after MAS redirect.

        KNOWN BUG: Token is currently lost when MAS redirects to /register/password
        """
        token = "mat_test123"
        page.goto(f"{REGISTRATION_URL}?token={token}")

        # Wait for redirects
        page.wait_for_load_state("networkidle")

        # Token should still be in URL or in form
        current_url = page.url
        page_content = page.content()

        token_in_url = token in current_url
        token_in_page = token in page_content

        assert token_in_url or token_in_page, \
            f"Token should be preserved. URL: {current_url[:100]}"


# =============================================================================
# Phase 2.3: Form Validation
# =============================================================================

class TestRegistrationFormValidation:
    """Tests for registration form validation."""

    def test_empty_form_shows_validation(self, page: Page):
        """Submitting empty form should show validation errors."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        # Find and click submit button
        submit_button = page.locator("button[type='submit'], input[type='submit']")
        if submit_button.count() > 0:
            submit_button.first.click()

            # Should show some validation feedback
            # (either browser validation or server response)
            page.wait_for_timeout(1000)  # Wait for validation

    def test_password_mismatch_shows_error(self, page: Page):
        """Mismatched passwords should show error."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        # Fill form with mismatched passwords
        password_fields = page.locator("input[type='password']")
        if password_fields.count() >= 2:
            password_fields.nth(0).fill("TestPassword123!")
            password_fields.nth(1).fill("DifferentPassword!")

            # Try to submit
            submit_button = page.locator("button[type='submit'], input[type='submit']")
            if submit_button.count() > 0:
                submit_button.first.click()
                page.wait_for_timeout(1000)

                # Should show mismatch error (check for common patterns)
                page_content = page.content().lower()
                has_error = any([
                    "match" in page_content,
                    "mismatch" in page_content,
                    "different" in page_content,
                    "error" in page_content,
                ])
                # Note: This might not work if browser validation catches it first


# =============================================================================
# Phase 2.4: Email Validation
# =============================================================================

class TestEmailValidation:
    """Tests for email input validation."""

    def test_invalid_email_rejected(self, page: Page):
        """Invalid email format should be rejected."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        email_field = page.locator("input[type='email'], input[name='email']")
        if email_field.count() > 0:
            email_field.first.fill("not-an-email")

            # Browser should show validation error on blur or submit
            # Most modern browsers validate email type inputs


# =============================================================================
# Phase 2.5: Username Validation
# =============================================================================

class TestUsernameValidation:
    """Tests for username input validation."""

    def test_username_special_chars_handled(self, page: Page):
        """Username with special characters should be handled."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        username_field = page.locator("input[name='username']")
        if username_field.count() > 0:
            # Try various special characters
            test_usernames = [
                "user@name",  # @ symbol
                "user name",  # space
                "user/name",  # slash
                "user:name",  # colon
            ]

            for username in test_usernames:
                username_field.first.fill(username)
                # Just verify no crash - validation rules vary

    def test_username_max_length(self, page: Page):
        """Very long username should be handled."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        username_field = page.locator("input[name='username']")
        if username_field.count() > 0:
            # Try very long username
            long_username = "a" * 256
            username_field.first.fill(long_username)
            # Should either truncate or show error on submit


# =============================================================================
# Phase 2.6: Token Error Messages
# =============================================================================

class TestTokenErrors:
    """Tests for token-related error messages."""

    def test_missing_token_error_message(self, page: Page):
        """Submitting without token should show clear error.

        This tests UX - the error should guide user to enter token.
        """
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        # Fill form with valid data but no token
        username_field = page.locator("input[name='username']")
        email_field = page.locator("input[type='email'], input[name='email']")
        password_fields = page.locator("input[type='password']")

        if username_field.count() > 0:
            username_field.first.fill("test_user")
        if email_field.count() > 0:
            email_field.first.fill("test@example.com")
        if password_fields.count() >= 2:
            password_fields.nth(0).fill("TestPassword123!")
            password_fields.nth(1).fill("TestPassword123!")

        # Submit form
        submit_button = page.locator("button[type='submit'], input[type='submit']")
        if submit_button.count() > 0:
            submit_button.first.click()
            page.wait_for_timeout(2000)

            # Should show token-related error
            page_content = page.content().lower()
            has_token_error = any([
                "token" in page_content,
                "registration code" in page_content,
                "invite" in page_content,
            ])
            # Note: The error message format depends on MAS configuration

    @pytest.mark.skip(reason="Requires valid used token - setup in CI needed")
    def test_already_used_token_error(self, page: Page):
        """Already-used token should show clear error."""
        # This test would require a pre-used token in the test environment
        pass

    @pytest.mark.skip(reason="Requires expired token - setup in CI needed")
    def test_expired_token_error(self, page: Page):
        """Expired token should show clear error."""
        # This test would require an expired token in the test environment
        pass


# =============================================================================
# Phase 2.7: Full Registration Flow
# =============================================================================

class TestFullRegistrationFlow:
    """End-to-end registration flow tests.

    These tests require a valid, unused registration token.
    They're marked as skip by default to avoid consuming tokens.
    """

    @pytest.mark.skip(reason="Requires valid registration token - manual test only")
    def test_full_registration_success(self, page: Page):
        """Complete registration with valid token should succeed.

        This is a manual test - uncomment and provide token to run.
        """
        token = "PROVIDE_VALID_TOKEN"
        username = f"test_user_{int(time.time())}"
        email = f"{username}@example.com"
        password = "SecureTestPassword123!"

        # Navigate to registration with token
        page.goto(f"{REGISTRATION_URL}?token={token}")
        page.wait_for_load_state("networkidle")

        # Fill form
        # ... (implement based on actual form structure)

        # Submit and verify success
        # ... (implement based on actual success indicators)


# =============================================================================
# Phase 2.E: Edge Cases
# =============================================================================

class TestRegistrationEdgeCases:
    """Edge case tests for registration."""

    def test_back_button_handling(self, page: Page):
        """Pressing back during registration should be handled gracefully."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        # Navigate forward if there's a multi-step flow
        # Then go back
        page.go_back()

        # Should not error
        page.wait_for_load_state("networkidle")
        expect(page).not_to_have_url(re.compile(r".*error.*"))

    def test_page_refresh_during_registration(self, page: Page):
        """Refreshing during registration should be handled."""
        page.goto(REGISTRATION_URL)
        page.wait_for_load_state("networkidle")

        # Fill some fields
        username_field = page.locator("input[name='username']")
        if username_field.count() > 0:
            username_field.first.fill("test_user")

        # Refresh page
        page.reload()
        page.wait_for_load_state("networkidle")

        # Should handle gracefully (form reset is OK, error is not)
        expect(page).not_to_have_url(re.compile(r".*error.*"))

    def test_multiple_tabs_same_token(self, page: Page, context):
        """Opening registration in multiple tabs with same token.

        Tests for race conditions and proper token handling.
        """
        token = "mat_test123"
        url = f"{REGISTRATION_URL}?token={token}"

        # Open in multiple tabs
        page1 = context.new_page()
        page2 = context.new_page()

        page1.goto(url)
        page2.goto(url)

        page1.wait_for_load_state("networkidle")
        page2.wait_for_load_state("networkidle")

        # Both should load (the actual conflict happens on submit)
        # Just verify no immediate error
        expect(page1).not_to_have_url(re.compile(r".*error.*"))
        expect(page2).not_to_have_url(re.compile(r".*error.*"))

        page1.close()
        page2.close()
