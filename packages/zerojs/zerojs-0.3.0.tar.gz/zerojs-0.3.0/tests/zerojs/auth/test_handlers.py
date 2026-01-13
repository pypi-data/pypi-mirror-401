"""Tests for HTTP exception handlers."""

import time

from starlette.requests import Request

from zerojs.auth.exceptions import (
    AccountLocked,
    AuthenticationError,
    InvalidCredentials,
    MFARequired,
    PermissionDenied,
)
from zerojs.auth.handlers import (
    account_locked_handler,
    authentication_error_handler,
    invalid_credentials_handler,
    mfa_required_handler,
    permission_denied_handler,
    register_auth_exception_handlers,
)


class TestAuthenticationErrorHandler:
    """Tests for authentication_error_handler."""

    def test_returns_401(self):
        """Handler returns 401 status code."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = AuthenticationError("Not authenticated")

        response = authentication_error_handler(request, exc)

        assert response.status_code == 401

    def test_response_body(self):
        """Handler returns correct error body."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = AuthenticationError("Login required")

        response = authentication_error_handler(request, exc)
        body = response.body.decode()

        assert "authentication_required" in body
        assert "Login required" in body


class TestPermissionDeniedHandler:
    """Tests for permission_denied_handler."""

    def test_returns_403(self):
        """Handler returns 403 status code."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = PermissionDenied("posts:delete", user_id=1)

        response = permission_denied_handler(request, exc)

        assert response.status_code == 403

    def test_response_includes_permission(self):
        """Handler includes permission in response."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = PermissionDenied("posts:delete", user_id=1)

        response = permission_denied_handler(request, exc)
        body = response.body.decode()

        assert "permission_denied" in body
        assert "posts:delete" in body


class TestInvalidCredentialsHandler:
    """Tests for invalid_credentials_handler."""

    def test_returns_401(self):
        """Handler returns 401 status code."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = InvalidCredentials("Wrong password")

        response = invalid_credentials_handler(request, exc)

        assert response.status_code == 401

    def test_response_body(self):
        """Handler returns correct error body."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = InvalidCredentials("Wrong password")

        response = invalid_credentials_handler(request, exc)
        body = response.body.decode()

        assert "invalid_credentials" in body


class TestAccountLockedHandler:
    """Tests for account_locked_handler."""

    def test_returns_429(self):
        """Handler returns 429 status code."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = AccountLocked()

        response = account_locked_handler(request, exc)

        assert response.status_code == 429

    def test_includes_retry_after_header(self):
        """Handler includes Retry-After header when unlock_at is set."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        unlock_at = time.time() + 300  # 5 minutes from now
        exc = AccountLocked(unlock_at=unlock_at)

        response = account_locked_handler(request, exc)

        assert "Retry-After" in response.headers
        retry_after = int(response.headers["Retry-After"])
        assert 298 <= retry_after <= 302  # ~300 seconds

    def test_no_retry_after_when_past(self):
        """Handler doesn't include Retry-After when unlock_at is in past."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        unlock_at = time.time() - 60  # 1 minute ago
        exc = AccountLocked(unlock_at=unlock_at)

        response = account_locked_handler(request, exc)

        assert "Retry-After" not in response.headers

    def test_response_includes_unlock_at(self):
        """Handler includes unlock_at in response body."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        unlock_at = time.time() + 300
        exc = AccountLocked(unlock_at=unlock_at)

        response = account_locked_handler(request, exc)
        body = response.body.decode()

        assert "account_locked" in body
        assert str(int(unlock_at)) in body


class TestMFARequiredHandler:
    """Tests for mfa_required_handler."""

    def test_returns_401(self):
        """Handler returns 401 status code."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = MFARequired(mfa_token="abc123", methods=["totp", "sms"])

        response = mfa_required_handler(request, exc)

        assert response.status_code == 401

    def test_response_includes_mfa_token(self):
        """Handler includes MFA token in response."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = MFARequired(mfa_token="abc123", methods=["totp", "sms"])

        response = mfa_required_handler(request, exc)
        body = response.body.decode()

        assert "mfa_required" in body
        assert "abc123" in body

    def test_response_includes_methods(self):
        """Handler includes available methods in response."""
        request = Request(scope={"type": "http", "method": "GET", "path": "/"})
        exc = MFARequired(mfa_token="abc123", methods=["totp", "sms"])

        response = mfa_required_handler(request, exc)
        body = response.body.decode()

        assert "totp" in body
        assert "sms" in body


class TestRegisterAuthExceptionHandlers:
    """Tests for register_auth_exception_handlers."""

    def test_registers_all_handlers(self):
        """Function registers all exception handlers."""
        from starlette.applications import Starlette

        app = Starlette()
        register_auth_exception_handlers(app)

        # Check that handlers were registered
        assert AuthenticationError in app.exception_handlers
        assert PermissionDenied in app.exception_handlers
        assert InvalidCredentials in app.exception_handlers
        assert AccountLocked in app.exception_handlers
        assert MFARequired in app.exception_handlers
