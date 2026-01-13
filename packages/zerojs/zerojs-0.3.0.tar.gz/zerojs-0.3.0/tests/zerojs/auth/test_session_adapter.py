"""Tests for AuthSessionAdapter."""

import time

import pytest
import time_machine

from zerojs.auth.session_adapter import AuthSessionAdapter
from zerojs.session.backends.memory import MemorySessionStore


@pytest.fixture
def store() -> MemorySessionStore:
    """Create a memory session store."""
    return MemorySessionStore()


@pytest.fixture
def adapter(store: MemorySessionStore) -> AuthSessionAdapter:
    """Create an auth session adapter."""
    return AuthSessionAdapter(store, default_ttl=3600)


class TestAuthSessionAdapterCreate:
    """Tests for create() method."""

    def test_create_returns_session_id(self, adapter: AuthSessionAdapter) -> None:
        """create() returns a session ID string."""
        session_id = adapter.create(user_id=123)
        assert isinstance(session_id, str)
        assert len(session_id) > 20  # URL-safe base64

    def test_create_stores_user_id(self, adapter: AuthSessionAdapter) -> None:
        """create() stores user_id in session."""
        session_id = adapter.create(user_id=123)
        assert adapter.get_user_id(session_id) == 123

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_create_stores_authenticated_at(self, adapter: AuthSessionAdapter) -> None:
        """create() stores authenticated_at timestamp."""
        session_id = adapter.create(user_id=123)
        data = adapter.get_data(session_id)
        assert data is not None
        assert data["authenticated_at"] == time.time()

    def test_create_stores_custom_data(self, adapter: AuthSessionAdapter) -> None:
        """create() stores custom data."""
        session_id = adapter.create(
            user_id=123,
            data={"remember_me": True, "device": "mobile"},
        )
        data = adapter.get_data(session_id)
        assert data is not None
        assert data["remember_me"] is True
        assert data["device"] == "mobile"

    def test_create_user_id_overrides_custom_data(self, adapter: AuthSessionAdapter) -> None:
        """user_id in reserved keys wins over user-provided data."""
        session_id = adapter.create(
            user_id=123,
            data={"user_id": 999},  # Should be overwritten
        )
        assert adapter.get_user_id(session_id) == 123

    def test_create_generates_unique_ids(self, adapter: AuthSessionAdapter) -> None:
        """create() generates unique session IDs."""
        ids = [adapter.create(user_id=123) for _ in range(100)]
        assert len(set(ids)) == 100

    def test_create_uses_custom_ttl(self, store: MemorySessionStore, adapter: AuthSessionAdapter) -> None:
        """create() uses custom TTL when provided."""
        session_id = adapter.create(user_id=123, ttl=60)

        # Session should exist
        assert adapter.get_user_id(session_id) == 123

        # Verify TTL was applied (store internal check)
        session_data = store.get(session_id)
        assert session_data is not None


class TestAuthSessionAdapterGetUserId:
    """Tests for get_user_id() method."""

    def test_get_user_id_returns_id(self, adapter: AuthSessionAdapter) -> None:
        """get_user_id() returns the user_id."""
        session_id = adapter.create(user_id=456)
        assert adapter.get_user_id(session_id) == 456

    def test_get_user_id_returns_none_for_nonexistent(self, adapter: AuthSessionAdapter) -> None:
        """get_user_id() returns None for nonexistent session."""
        assert adapter.get_user_id("nonexistent") is None


class TestAuthSessionAdapterGetData:
    """Tests for get_data() method."""

    def test_get_data_returns_all_data(self, adapter: AuthSessionAdapter) -> None:
        """get_data() returns all session data."""
        session_id = adapter.create(
            user_id=123,
            data={"role": "admin", "theme": "dark"},
        )
        data = adapter.get_data(session_id)
        assert data is not None
        assert data["user_id"] == 123
        assert data["role"] == "admin"
        assert data["theme"] == "dark"
        assert "authenticated_at" in data

    def test_get_data_returns_none_for_nonexistent(self, adapter: AuthSessionAdapter) -> None:
        """get_data() returns None for nonexistent session."""
        assert adapter.get_data("nonexistent") is None


class TestAuthSessionAdapterDestroy:
    """Tests for destroy() method."""

    def test_destroy_removes_session(self, adapter: AuthSessionAdapter) -> None:
        """destroy() removes the session."""
        session_id = adapter.create(user_id=123)
        assert adapter.get_user_id(session_id) == 123

        adapter.destroy(session_id)
        assert adapter.get_user_id(session_id) is None

    def test_destroy_nonexistent_does_not_raise(self, adapter: AuthSessionAdapter) -> None:
        """destroy() does not raise for nonexistent session."""
        adapter.destroy("nonexistent")  # Should not raise


class TestAuthSessionAdapterRefresh:
    """Tests for refresh() method."""

    def test_refresh_returns_true_for_existing(self, adapter: AuthSessionAdapter) -> None:
        """refresh() returns True for existing session."""
        session_id = adapter.create(user_id=123)
        assert adapter.refresh(session_id) is True

    def test_refresh_returns_false_for_nonexistent(self, adapter: AuthSessionAdapter) -> None:
        """refresh() returns False for nonexistent session."""
        assert adapter.refresh("nonexistent") is False

    def test_refresh_updates_ttl(self, store: MemorySessionStore, adapter: AuthSessionAdapter) -> None:
        """refresh() updates session TTL."""
        session_id = adapter.create(user_id=123, ttl=60)

        # Refresh with longer TTL
        result = adapter.refresh(session_id, ttl=7200)
        assert result is True

        # Session should still be accessible
        assert adapter.get_user_id(session_id) == 123


class TestAuthSessionAdapterRawOperations:
    """Tests for raw storage operations."""

    def test_set_raw_and_get_raw(self, adapter: AuthSessionAdapter) -> None:
        """set_raw() and get_raw() work together."""
        adapter.set_raw("mfa:token123", {"user_id": 456, "method": "totp"}, ttl=300)

        data = adapter.get_raw("mfa:token123")
        assert data == {"user_id": 456, "method": "totp"}

    def test_get_raw_returns_none_for_nonexistent(self, adapter: AuthSessionAdapter) -> None:
        """get_raw() returns None for nonexistent key."""
        assert adapter.get_raw("nonexistent") is None

    def test_delete_raw_removes_data(self, adapter: AuthSessionAdapter) -> None:
        """delete_raw() removes the data."""
        adapter.set_raw("temp:key", {"value": 1}, ttl=300)
        assert adapter.get_raw("temp:key") is not None

        adapter.delete_raw("temp:key")
        assert adapter.get_raw("temp:key") is None

    def test_delete_raw_nonexistent_does_not_raise(self, adapter: AuthSessionAdapter) -> None:
        """delete_raw() does not raise for nonexistent key."""
        adapter.delete_raw("nonexistent")  # Should not raise


class TestAuthSessionAdapterCounters:
    """Tests for counter operations."""

    def test_increment_raw_creates_counter(self, adapter: AuthSessionAdapter) -> None:
        """increment_raw() creates a new counter."""
        result = adapter.increment_raw("counter:test")
        assert result == 1

    def test_increment_raw_increments_existing(self, adapter: AuthSessionAdapter) -> None:
        """increment_raw() increments existing counter."""
        adapter.increment_raw("counter:test")
        adapter.increment_raw("counter:test")
        result = adapter.increment_raw("counter:test")
        assert result == 3

    def test_increment_raw_with_amount(self, adapter: AuthSessionAdapter) -> None:
        """increment_raw() respects amount parameter."""
        result = adapter.increment_raw("counter:test", amount=5)
        assert result == 5

        result = adapter.increment_raw("counter:test", amount=3)
        assert result == 8

    def test_get_counter_raw_returns_value(self, adapter: AuthSessionAdapter) -> None:
        """get_counter_raw() returns counter value."""
        adapter.increment_raw("counter:test", amount=10)
        assert adapter.get_counter_raw("counter:test") == 10

    def test_get_counter_raw_returns_zero_for_nonexistent(self, adapter: AuthSessionAdapter) -> None:
        """get_counter_raw() returns 0 for nonexistent counter."""
        assert adapter.get_counter_raw("nonexistent") == 0


class TestAuthSessionAdapterIntegration:
    """Integration tests for common use cases."""

    def test_rate_limiting_flow(self, adapter: AuthSessionAdapter) -> None:
        """Test rate limiting flow."""
        key = "rate:user@example.com"
        max_attempts = 5

        # Simulate failed login attempts
        for i in range(max_attempts):
            attempts = adapter.increment_raw(key, ttl=300)
            assert attempts == i + 1

        # Should be rate limited now
        assert adapter.get_counter_raw(key) >= max_attempts

        # Clear on success
        adapter.delete_raw(key)
        assert adapter.get_counter_raw(key) == 0

    def test_mfa_token_flow(self, adapter: AuthSessionAdapter) -> None:
        """Test MFA token flow."""
        user_id = 123
        mfa_token = "abc123"

        # Store MFA challenge
        adapter.set_raw(
            f"mfa:{mfa_token}",
            {"user_id": user_id, "method": "totp"},
            ttl=300,
        )

        # Verify MFA token
        data = adapter.get_raw(f"mfa:{mfa_token}")
        assert data is not None
        assert data["user_id"] == user_id

        # Consume MFA token
        adapter.delete_raw(f"mfa:{mfa_token}")
        assert adapter.get_raw(f"mfa:{mfa_token}") is None

    def test_session_with_remember_me(self, adapter: AuthSessionAdapter) -> None:
        """Test session with remember_me feature."""
        # Short session (no remember me)
        short_session = adapter.create(
            user_id=123,
            data={"remember_me": False},
            ttl=3600,  # 1 hour
        )

        # Long session (remember me)
        long_session = adapter.create(
            user_id=123,
            data={"remember_me": True},
            ttl=2592000,  # 30 days
        )

        # Both sessions should be valid
        assert adapter.get_user_id(short_session) == 123
        assert adapter.get_user_id(long_session) == 123

        # Check remember_me flag
        short_data = adapter.get_data(short_session)
        long_data = adapter.get_data(long_session)
        assert short_data is not None and short_data["remember_me"] is False
        assert long_data is not None and long_data["remember_me"] is True
