"""Tests for SessionCookieManager."""

import time_machine

from zerojs.session import SessionCookieManager


class TestSessionCookieManager:
    """Tests for SessionCookieManager."""

    def test_generate_session_id_is_unique(self) -> None:
        """generate_session_id() creates unique IDs."""
        manager = SessionCookieManager("secret-key")
        ids = {manager.generate_session_id() for _ in range(100)}
        assert len(ids) == 100

    def test_generate_session_id_is_url_safe(self) -> None:
        """generate_session_id() creates URL-safe strings."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        # URL-safe base64 uses only alphanumeric, -, and _
        assert all(c.isalnum() or c in "-_" for c in session_id)

    def test_sign_session_id_returns_string(self) -> None:
        """sign_session_id() returns a signed string."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        signed = manager.sign_session_id(session_id)
        assert isinstance(signed, str)
        assert signed != session_id

    def test_verify_session_id_returns_original(self) -> None:
        """verify_session_id() returns the original session ID."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        signed = manager.sign_session_id(session_id)
        verified = manager.verify_session_id(signed)
        assert verified == session_id

    def test_verify_session_id_rejects_tampered(self) -> None:
        """verify_session_id() returns None for tampered values."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        signed = manager.sign_session_id(session_id)
        # Tamper with the signature part (after the last dot)
        parts = signed.rsplit(".", 1)
        if len(parts) == 2:
            tampered = parts[0] + ".TAMPERED"
        else:
            tampered = "TAMPERED"
        assert manager.verify_session_id(tampered) is None

    def test_verify_session_id_rejects_invalid(self) -> None:
        """verify_session_id() returns None for invalid values."""
        manager = SessionCookieManager("secret-key")
        assert manager.verify_session_id("invalid") is None
        assert manager.verify_session_id("") is None
        assert manager.verify_session_id("not.a.signed.value") is None

    def test_verify_session_id_rejects_wrong_key(self) -> None:
        """verify_session_id() returns None when signed with different key."""
        manager1 = SessionCookieManager("secret-key-1")
        manager2 = SessionCookieManager("secret-key-2")
        session_id = manager1.generate_session_id()
        signed = manager1.sign_session_id(session_id)
        assert manager2.verify_session_id(signed) is None

    def test_verify_session_id_rejects_wrong_salt(self) -> None:
        """verify_session_id() returns None when signed with different salt."""
        manager1 = SessionCookieManager("secret-key", salt="salt1")
        manager2 = SessionCookieManager("secret-key", salt="salt2")
        session_id = manager1.generate_session_id()
        signed = manager1.sign_session_id(session_id)
        assert manager2.verify_session_id(signed) is None

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_verify_session_id_with_max_age(self) -> None:
        """verify_session_id() respects max_age parameter."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        signed = manager.sign_session_id(session_id)

        # Should be valid immediately
        assert manager.verify_session_id(signed, max_age=60) == session_id

        # Should be invalid after max_age
        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            assert manager.verify_session_id(signed, max_age=60) is None

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_verify_session_id_without_max_age(self) -> None:
        """verify_session_id() ignores age when max_age is None."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        signed = manager.sign_session_id(session_id)

        # Should still be valid after time passes (no max_age)
        with time_machine.travel("2024-01-01 13:00:00", tick=False):
            assert manager.verify_session_id(signed) == session_id

    def test_signed_value_is_url_safe(self) -> None:
        """Signed values are URL-safe for cookie storage."""
        manager = SessionCookieManager("secret-key")
        session_id = manager.generate_session_id()
        signed = manager.sign_session_id(session_id)
        # URL-safe base64 uses only alphanumeric, -, _, and .
        assert all(c.isalnum() or c in "-_." for c in signed)
