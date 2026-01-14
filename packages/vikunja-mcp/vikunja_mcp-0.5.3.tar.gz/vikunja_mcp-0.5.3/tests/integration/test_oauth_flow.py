"""Integration tests for OAuth flow using Playwright.

Tests the OAuth connect pages and redirect behavior.

Run with: uv run pytest tests/integration/test_oauth_flow.py -v -m integration

Requires:
- Playwright browsers installed: playwright install chromium
- Environment variables (see conftest.py for details)
"""

import pytest
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.integration]


class TestConnectPageLoads:
    """Tests that OAuth connect pages load correctly."""

    def test_connect_page_loads(self, page: Page, oauth_config):
        """connect.html should load without errors."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}"
        page.goto(url)

        # Page should load
        expect(page).to_have_title(/.+/)  # Any title
        # TODO: Add specific assertions about page content
        # Expected: page contains connect button

    def test_matrix_connect_page_loads(self, page: Page, oauth_config):
        """matrix-connect.html should load without errors."""
        url = f"{oauth_config.base_url}{oauth_config.matrix_connect_page}"
        page.goto(url)

        # Page should load
        expect(page).to_have_title(/.+/)  # Any title
        # TODO: Add specific assertions about page content

    def test_connect_page_has_connect_button(self, page: Page, oauth_config):
        """connect.html should have a connect/authorize button."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}"
        page.goto(url)

        # TODO: Update selector based on actual page structure
        # button = page.locator("button:has-text('Connect')")
        # expect(button).to_be_visible()
        pass  # Scaffold - implement when page structure is known


class TestOAuthLocalStorage:
    """Tests for localStorage handling in OAuth flow."""

    def test_oauth_clears_localstorage_on_load(self, page: Page, oauth_config):
        """OAuth page should clear localStorage on load for security."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}"

        # Set some localStorage before loading
        page.goto(url)
        page.evaluate("localStorage.setItem('test_key', 'test_value')")

        # Reload page
        page.reload()

        # Check if localStorage was cleared
        # TODO: Verify specific behavior
        # value = page.evaluate("localStorage.getItem('test_key')")
        # assert value is None, "localStorage should be cleared on OAuth page load"
        pass  # Scaffold - implement based on actual OAuth page behavior

    def test_token_not_stored_in_localstorage(self, page: Page, oauth_config):
        """Access tokens should not be stored in localStorage."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}"
        page.goto(url)

        # After OAuth flow (if we can test it), verify no tokens in localStorage
        # TODO: This requires completing OAuth flow or mocking
        local_storage = page.evaluate("JSON.stringify(localStorage)")
        assert "access_token" not in local_storage.lower()
        assert "bearer" not in local_storage.lower()


class TestOAuthRedirects:
    """Tests for OAuth redirect behavior."""

    def test_oauth_redirects_to_oidc_provider(self, page: Page, oauth_config):
        """Clicking connect should redirect to OIDC provider."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}"
        page.goto(url)

        # TODO: Update based on actual page structure
        # Click the connect button
        # connect_button = page.locator("button:has-text('Connect')")
        # connect_button.click()

        # Verify redirect to OIDC provider
        # expect(page).to_have_url(re.compile(r".*oauth.*|.*oidc.*"))
        pass  # Scaffold - implement when page structure is known

    def test_oauth_includes_required_params(self, page: Page, oauth_config):
        """OAuth redirect should include required parameters."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}"
        page.goto(url)

        # TODO: Click connect and verify URL params
        # Expected params: client_id, redirect_uri, scope, response_type, state
        pass  # Scaffold


class TestOAuthErrorHandling:
    """Tests for OAuth error handling."""

    def test_oauth_error_displayed(self, page: Page, oauth_config):
        """OAuth errors should be displayed to user."""
        # Simulate error by loading with error params
        url = f"{oauth_config.base_url}{oauth_config.connect_page}?error=access_denied"
        page.goto(url)

        # TODO: Verify error message is shown
        # error_message = page.locator(".error-message")
        # expect(error_message).to_be_visible()
        pass  # Scaffold

    def test_oauth_invalid_state_handled(self, page: Page, oauth_config):
        """Invalid state parameter should show error."""
        url = f"{oauth_config.base_url}{oauth_config.connect_page}?state=invalid"
        page.goto(url)

        # TODO: Verify invalid state handling
        pass  # Scaffold


class TestMatrixConnect:
    """Tests specific to Matrix-Vikunja connection flow."""

    def test_matrix_connect_shows_user_info(self, page: Page, oauth_config):
        """Matrix connect should show user's Matrix ID."""
        url = f"{oauth_config.base_url}{oauth_config.matrix_connect_page}"
        page.goto(url)

        # TODO: Verify Matrix user info display
        pass  # Scaffold

    def test_matrix_connect_link_account(self, page: Page, oauth_config):
        """Matrix connect should have option to link Vikunja account."""
        url = f"{oauth_config.base_url}{oauth_config.matrix_connect_page}"
        page.goto(url)

        # TODO: Verify link account flow
        pass  # Scaffold
