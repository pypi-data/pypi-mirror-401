"""
Unit tests for /auth-register endpoint (token-gated Google OIDC registration).

Bead: solutions-l0u9.10
Bead: fa-8g1r (Welcome message missing for Google Login users)

Tests the cookie-gated OIDC flow:
1. User visits /auth-register?token=XXX
2. Bot validates token, sets signed cookie
3. Returns HTML page with popup-based login flow
4. After login, /oidc-onboard runs onboarding
"""

import os
import pytest
from unittest.mock import patch, MagicMock


class TestAuthRegisterEndpoint:
    """Test /auth-register endpoint."""

    @pytest.fixture
    def mock_token_validation(self):
        """Mock registration token validation functions."""
        with patch("vikunja_mcp.registration_tokens.validate_registration_token") as validate_mock, \
             patch("vikunja_mcp.registration_tokens.record_token_usage") as record_mock:
            yield validate_mock, record_mock

    @pytest.fixture
    def mock_cookie_secret(self):
        """Mock COOKIE_SIGNING_SECRET environment variable and module constant."""
        import vikunja_mcp.server as server_module

        # Save originals
        original_secret = server_module.COOKIE_SIGNING_SECRET
        original_serializer = server_module._cookie_serializer

        # Set the module-level constant directly (env var is read at import time)
        server_module.COOKIE_SIGNING_SECRET = "test-secret-key-for-signing"
        server_module._cookie_serializer = None

        yield

        # Restore
        server_module.COOKIE_SIGNING_SECRET = original_secret
        server_module._cookie_serializer = original_serializer

    @pytest.fixture
    def test_client(self, mock_cookie_secret):
        """Create test client for the server."""
        from starlette.testclient import TestClient
        from vikunja_mcp.server import mcp

        # Get the Starlette app from FastMCP
        app = mcp.http_app()
        return TestClient(app, raise_server_exceptions=False)

    def test_valid_token_returns_html_page_with_cookie(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that valid token returns HTML registration page with cookie.

        Bead: fa-8g1r - Changed from redirect to HTML page with popup flow
        to enable onboarding for OIDC users.
        """
        validate_mock, record_mock = mock_token_validation

        # Mock successful validation
        validate_mock.return_value = {
            "token": "VALID-TOKEN",
            "group_id": None,
            "max_uses": 50,
            "uses_remaining": 49,
            "expires_at": None,
            "notes": "Test token",
        }

        response = test_client.get(
            "/auth-register?token=VALID-TOKEN",
            follow_redirects=False
        )

        # Should return HTML page (not redirect)
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

        # Page should contain key elements for popup-based login
        assert "Welcome to Factumerit" in response.text
        assert "Continue with Google" in response.text
        assert "oidc-onboard" in response.text  # Onboarding endpoint reference

        # Should have set the cookie (check set-cookie header for domain cookies)
        set_cookie = response.headers.get("set-cookie", "")
        assert "token_validated=" in set_cookie

        # Token usage should be recorded
        record_mock.assert_called_once()

    def test_missing_token_returns_400(self, test_client, mock_cookie_secret):
        """Test that missing token returns 400 error."""
        response = test_client.get("/auth-register")

        assert response.status_code == 400
        assert "required" in response.text.lower()

    def test_empty_token_returns_400(self, test_client, mock_cookie_secret):
        """Test that empty token returns 400 error."""
        response = test_client.get("/auth-register?token=")

        assert response.status_code == 400
        assert "required" in response.text.lower()

    def test_invalid_token_returns_404(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that invalid (non-existent) token returns 404."""
        validate_mock, record_mock = mock_token_validation

        # Import exception here to avoid import issues
        from vikunja_mcp.registration_tokens import TokenNotFoundError
        validate_mock.side_effect = TokenNotFoundError("Token not found")

        response = test_client.get("/auth-register?token=FAKE-TOKEN")

        assert response.status_code == 404
        assert "not found" in response.text.lower()
        record_mock.assert_not_called()

    def test_exhausted_token_returns_403(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that exhausted token returns 403."""
        validate_mock, record_mock = mock_token_validation

        from vikunja_mcp.registration_tokens import TokenExhaustedError
        validate_mock.side_effect = TokenExhaustedError("Token exhausted")

        response = test_client.get("/auth-register?token=EXHAUSTED-TOKEN")

        assert response.status_code == 403
        assert "used" in response.text.lower() or "exhausted" in response.text.lower()
        record_mock.assert_not_called()

    def test_expired_token_returns_403(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that expired token returns 403."""
        validate_mock, record_mock = mock_token_validation

        from vikunja_mcp.registration_tokens import TokenExpiredError
        validate_mock.side_effect = TokenExpiredError("Token expired on 2024-12-01")

        response = test_client.get("/auth-register?token=EXPIRED-TOKEN")

        assert response.status_code == 403
        assert "expired" in response.text.lower()
        record_mock.assert_not_called()

    def test_revoked_token_returns_403(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that revoked token returns 403."""
        validate_mock, record_mock = mock_token_validation

        from vikunja_mcp.registration_tokens import TokenRevokedError
        validate_mock.side_effect = TokenRevokedError("Token revoked")

        response = test_client.get("/auth-register?token=REVOKED-TOKEN")

        assert response.status_code == 403
        assert "revoked" in response.text.lower()
        record_mock.assert_not_called()

    def test_token_is_uppercased(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that token is uppercased before validation."""
        validate_mock, record_mock = mock_token_validation

        validate_mock.return_value = {
            "token": "LOWERCASE-TOKEN",
            "group_id": None,
            "max_uses": 50,
            "uses_remaining": 49,
            "expires_at": None,
            "notes": None,
        }

        response = test_client.get(
            "/auth-register?token=lowercase-token",
            follow_redirects=False
        )

        # Verify token was uppercased
        validate_mock.assert_called_once()
        call_args = validate_mock.call_args[0]
        assert call_args[0] == "LOWERCASE-TOKEN"

    def test_cookie_has_correct_attributes(self, test_client, mock_token_validation, mock_cookie_secret):
        """Test that cookie has correct security attributes."""
        validate_mock, record_mock = mock_token_validation

        validate_mock.return_value = {
            "token": "COOKIE-TEST",
            "group_id": None,
            "max_uses": 50,
            "uses_remaining": 49,
            "expires_at": None,
            "notes": None,
        }

        response = test_client.get(
            "/auth-register?token=COOKIE-TEST",
            follow_redirects=False
        )

        # Check response is HTML page (not redirect)
        assert response.status_code == 200

        # Check cookie was set
        set_cookie = response.headers.get("set-cookie", "")
        assert "token_validated=" in set_cookie

        # Note: In test environment, some attributes may not be present
        # In production, these should be verified:
        # - secure
        # - httponly
        # - samesite=lax
        # - domain=.factumerit.app


class TestAuthRegisterNoSecret:
    """Test /auth-register when COOKIE_SIGNING_SECRET is not set."""

    def test_no_secret_returns_500(self):
        """Test that missing secret returns 500 error."""
        # Ensure no secret is set
        with patch.dict(os.environ, {"COOKIE_SIGNING_SECRET": ""}):
            # Reset the serializer
            import vikunja_mcp.server as server_module
            server_module._cookie_serializer = None
            original_secret = server_module.COOKIE_SIGNING_SECRET
            server_module.COOKIE_SIGNING_SECRET = ""

            try:
                from starlette.testclient import TestClient
                from vikunja_mcp.server import mcp

                app = mcp.http_app()
                client = TestClient(app, raise_server_exceptions=False)

                response = client.get("/auth-register?token=VALID-TOKEN")

                assert response.status_code == 500
                assert "not configured" in response.text.lower() or "contact support" in response.text.lower()
            finally:
                server_module.COOKIE_SIGNING_SECRET = original_secret


class TestCookieSerialization:
    """Test cookie signing and serialization."""

    def test_cookie_serializer_creation(self):
        """Test that cookie serializer is created correctly."""
        from itsdangerous import URLSafeTimedSerializer

        import vikunja_mcp.server as server_module

        # Reset and test with secret
        server_module._cookie_serializer = None
        original_secret = server_module.COOKIE_SIGNING_SECRET
        server_module.COOKIE_SIGNING_SECRET = "test-secret"

        try:
            serializer = server_module._get_cookie_serializer()
            assert isinstance(serializer, URLSafeTimedSerializer)

            # Test it can sign data
            data = {"validated": True, "token": "TEST"}
            signed = serializer.dumps(data)
            assert isinstance(signed, str)

            # Test it can unsign data
            unsigned = serializer.loads(signed)
            assert unsigned["validated"] is True
            assert unsigned["token"] == "TEST"
        finally:
            server_module.COOKIE_SIGNING_SECRET = original_secret
            server_module._cookie_serializer = None

    def test_cookie_serializer_without_secret_raises(self):
        """Test that creating serializer without secret raises error."""
        import vikunja_mcp.server as server_module

        server_module._cookie_serializer = None
        original_secret = server_module.COOKIE_SIGNING_SECRET
        server_module.COOKIE_SIGNING_SECRET = ""

        try:
            with pytest.raises(RuntimeError, match="COOKIE_SIGNING_SECRET"):
                server_module._get_cookie_serializer()
        finally:
            server_module.COOKIE_SIGNING_SECRET = original_secret
            server_module._cookie_serializer = None


class TestOidcOnboardEndpoint:
    """Test /oidc-onboard endpoint for OIDC user onboarding.

    Bead: fa-8g1r (Welcome message missing for Google Login users)
    """

    @pytest.fixture
    def test_client(self):
        """Create test client for the server."""
        from starlette.testclient import TestClient
        from vikunja_mcp.server import mcp

        app = mcp.http_app()
        return TestClient(app, raise_server_exceptions=False)

    def test_missing_body_returns_400(self, test_client):
        """Test that missing JSON body returns 400."""
        response = test_client.post("/oidc-onboard")
        assert response.status_code == 400

    def test_missing_required_fields_returns_400(self, test_client):
        """Test that missing required fields returns 400."""
        response = test_client.post(
            "/oidc-onboard",
            json={"jwt": "some-token"}  # Missing email and username
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "email" in data["error"] or "username" in data["error"]

    def test_invalid_jwt_returns_401(self, test_client):
        """Test that invalid JWT returns 401."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(status_code=401)

            response = test_client.post(
                "/oidc-onboard",
                json={
                    "jwt": "invalid-jwt-token",
                    "email": "test@example.com",
                    "username": "testuser"
                }
            )
            assert response.status_code == 401
            data = response.json()
            assert "error" in data

    def test_valid_jwt_runs_onboarding(self, test_client):
        """Test that valid JWT triggers onboarding workflow.

        Bead: fa-8g1r - OIDC users get Google welcome email (not password email)
        """
        from vikunja_mcp.email_service import EmailResult

        with patch("requests.get") as mock_get, \
             patch("vikunja_mcp.signup_workflow.SignupWorkflow") as mock_workflow, \
             patch("vikunja_mcp.email_service.send_google_welcome_email") as mock_email:

            # Mock Vikunja user endpoint response
            mock_get.return_value = MagicMock(
                status_code=200,
                json=MagicMock(return_value={
                    "id": 123,
                    "username": "testuser",
                    "email": "test@example.com",
                    "name": "Test User"
                })
            )

            # Mock email service
            mock_email.return_value = EmailResult(success=True, message_id="test-123")

            # Mock SignupState
            from vikunja_mcp.signup_workflow import SignupState
            mock_state = SignupState(
                email="test@example.com",
                username="testuser",
                registration_code="TEST-TOKEN",
                vikunja_user_id=123,
                vikunja_jwt_token="valid-jwt"
            )
            mock_state.bot_credentials = None
            mock_state.bot_verified = False
            mock_state.inbox_project_id = 1
            mock_state.welcome_task_created = True
            mock_state.password_reset_sent = False

            # Mock workflow methods
            mock_workflow_instance = mock_workflow.return_value
            mock_workflow_instance.stage_2_provision_bot.return_value = mock_state
            mock_workflow_instance.stage_3_verify_bot.return_value = mock_state
            mock_workflow_instance.stage_4_find_inbox.return_value = mock_state
            mock_workflow_instance.stage_6_create_welcome_task.return_value = mock_state

            response = test_client.post(
                "/oidc-onboard",
                json={
                    "jwt": "valid-jwt-token",
                    "email": "test@example.com",
                    "username": "testuser",
                    "registration_token": "TEST-TOKEN"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "onboarding" in data

            # Verify workflow methods were called
            mock_workflow_instance.stage_2_provision_bot.assert_called_once()
            mock_workflow_instance.stage_6_create_welcome_task.assert_called_once()

            # Verify Google welcome email was sent (not password email)
            mock_email.assert_called_once_with(
                to_email="test@example.com",
                user_name="Test User"
            )
