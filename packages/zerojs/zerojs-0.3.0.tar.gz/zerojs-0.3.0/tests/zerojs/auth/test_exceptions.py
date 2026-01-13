"""Tests for auth exceptions."""

import pytest

from zerojs.auth import (
    AccountLocked,
    AuthenticationError,
    AuthError,
    InvalidCredentials,
    MFARequired,
    PermissionDenied,
)


class TestAuthError:
    """Tests for AuthError base exception."""

    def test_is_base_exception(self) -> None:
        """AuthError is the base for all auth exceptions."""
        assert issubclass(AuthenticationError, AuthError)
        assert issubclass(PermissionDenied, AuthError)
        assert issubclass(InvalidCredentials, AuthError)
        assert issubclass(AccountLocked, AuthError)
        assert issubclass(MFARequired, AuthError)

    def test_can_be_raised(self) -> None:
        """AuthError can be raised and caught."""
        with pytest.raises(AuthError):
            raise AuthError("test error")


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_message(self) -> None:
        """AuthenticationError preserves message."""
        exc = AuthenticationError("Not logged in")
        assert str(exc) == "Not logged in"

    def test_can_be_caught_as_auth_error(self) -> None:
        """AuthenticationError can be caught as AuthError."""
        with pytest.raises(AuthError):
            raise AuthenticationError("test")


class TestPermissionDenied:
    """Tests for PermissionDenied."""

    def test_single_permission(self) -> None:
        """Single permission is stored correctly."""
        exc = PermissionDenied("posts:edit")
        assert exc.permission == "posts:edit"
        assert exc.user_id is None
        assert exc.mode == "all"
        assert "posts:edit" in str(exc)

    def test_multiple_permissions(self) -> None:
        """Multiple permissions are stored correctly."""
        exc = PermissionDenied(("posts:edit", "posts:delete"), user_id=123, mode="any")
        assert exc.permission == ("posts:edit", "posts:delete")
        assert exc.user_id == 123
        assert exc.mode == "any"
        assert "posts:edit" in str(exc)
        assert "posts:delete" in str(exc)
        assert "ANY" in str(exc)

    def test_all_mode_message(self) -> None:
        """All mode uses AND in message."""
        exc = PermissionDenied(("a", "b"), mode="all")
        assert "ALL" in str(exc)


class TestInvalidCredentials:
    """Tests for InvalidCredentials."""

    def test_message(self) -> None:
        """InvalidCredentials preserves message."""
        exc = InvalidCredentials("Wrong password")
        assert str(exc) == "Wrong password"


class TestAccountLocked:
    """Tests for AccountLocked."""

    def test_default_message(self) -> None:
        """AccountLocked has default message."""
        exc = AccountLocked()
        assert "locked" in str(exc).lower()
        assert exc.unlock_at is None

    def test_with_unlock_time(self) -> None:
        """AccountLocked stores unlock time."""
        exc = AccountLocked(unlock_at=1234567890.0)
        assert exc.unlock_at == 1234567890.0


class TestMFARequired:
    """Tests for MFARequired."""

    def test_stores_mfa_info(self) -> None:
        """MFARequired stores token and methods."""
        exc = MFARequired(mfa_token="abc123", methods=["totp", "sms"])
        assert exc.mfa_token == "abc123"
        assert exc.methods == ["totp", "sms"]
        assert "MFA" in str(exc) or "mfa" in str(exc).lower()
