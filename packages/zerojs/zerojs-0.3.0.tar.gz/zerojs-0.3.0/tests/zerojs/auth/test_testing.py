"""Tests for testing utilities."""

import pytest

from zerojs.auth.context import AuthContext
from zerojs.auth.testing import (
    MockCredentialVerifier,
    MockMFAProvider,
    MockRoleProvider,
    MockSessionStore,
    MockUser,
    MockUserProvider,
    mock_impersonation,
    mock_user,
)


class TestMockUser:
    """Tests for MockUser dataclass."""

    def test_default_values(self):
        """MockUser has sensible defaults."""
        user = MockUser(id=1, email="test@example.com")

        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.username is None
        assert user.is_active is True
        assert user.roles == []
        assert user.permissions == set()

    def test_custom_values(self):
        """MockUser accepts custom values."""
        user = MockUser(
            id=1,
            email="admin@example.com",
            username="admin",
            is_active=False,
            roles=["admin", "editor"],
            permissions={"users.delete"},
        )

        assert user.username == "admin"
        assert user.is_active is False
        assert "admin" in user.roles
        assert "users.delete" in user.permissions


class TestMockUserProvider:
    """Tests for MockUserProvider."""

    @pytest.fixture
    def provider(self):
        """Create provider with test users."""
        users = [
            MockUser(id=1, email="user@test.com"),
            MockUser(id=2, email="admin@test.com", username="admin"),
        ]
        return MockUserProvider(users)

    @pytest.mark.anyio
    async def test_get_by_identifier_email(self, provider):
        """Can find user by email."""
        user = await provider.get_by_identifier("user@test.com")
        assert user is not None
        assert user.id == 1

    @pytest.mark.anyio
    async def test_get_by_identifier_username(self, provider):
        """Can find user by username."""
        user = await provider.get_by_identifier("admin")
        assert user is not None
        assert user.id == 2

    @pytest.mark.anyio
    async def test_get_by_identifier_case_insensitive(self, provider):
        """Identifier lookup is case-insensitive."""
        user = await provider.get_by_identifier("USER@TEST.COM")
        assert user is not None
        assert user.id == 1

    @pytest.mark.anyio
    async def test_get_by_identifier_not_found(self, provider):
        """Returns None for unknown identifier."""
        user = await provider.get_by_identifier("unknown@test.com")
        assert user is None

    @pytest.mark.anyio
    async def test_get_by_id(self, provider):
        """Can find user by ID."""
        user = await provider.get_by_id(1)
        assert user is not None
        assert user.email == "user@test.com"

    @pytest.mark.anyio
    async def test_get_by_id_not_found(self, provider):
        """Returns None for unknown ID."""
        user = await provider.get_by_id(999)
        assert user is None

    @pytest.mark.anyio
    async def test_is_active(self, provider):
        """Returns user's is_active status."""
        user = await provider.get_by_id(1)
        assert await provider.is_active(user) is True

    @pytest.mark.anyio
    async def test_is_active_inactive_user(self):
        """Returns False for inactive user."""
        user = MockUser(id=1, email="inactive@test.com", is_active=False)
        provider = MockUserProvider([user])
        assert await provider.is_active(user) is False

    @pytest.mark.anyio
    async def test_add_user(self):
        """Can add users after initialization."""
        provider = MockUserProvider()
        user = MockUser(id=3, email="new@test.com")
        provider.add_user(user)

        # Verify user was added
        result = await provider.get_by_id(3)
        assert result is not None

    @pytest.mark.anyio
    async def test_remove_user(self):
        """Can remove users."""
        user = MockUser(id=1, email="remove@test.com")
        provider = MockUserProvider([user])
        provider.remove_user(1)

        result = await provider.get_by_id(1)
        assert result is None


class TestMockCredentialVerifier:
    """Tests for MockCredentialVerifier."""

    @pytest.mark.anyio
    async def test_default_password(self):
        """Default password is 'password'."""
        verifier = MockCredentialVerifier()
        user = MockUser(id=1, email="test@test.com")

        assert await verifier.verify(user, "password") is True
        assert await verifier.verify(user, "wrong") is False

    @pytest.mark.anyio
    async def test_custom_password(self):
        """Can set custom valid password."""
        verifier = MockCredentialVerifier(valid_password="secret123")
        user = MockUser(id=1, email="test@test.com")

        assert await verifier.verify(user, "secret123") is True
        assert await verifier.verify(user, "password") is False

    @pytest.mark.anyio
    async def test_per_user_passwords(self):
        """Can set different passwords per user."""
        verifier = MockCredentialVerifier(passwords={1: "pass1", 2: "pass2"})
        user1 = MockUser(id=1, email="user1@test.com")
        user2 = MockUser(id=2, email="user2@test.com")

        assert await verifier.verify(user1, "pass1") is True
        assert await verifier.verify(user1, "pass2") is False
        assert await verifier.verify(user2, "pass2") is True


class TestMockSessionStore:
    """Tests for MockSessionStore."""

    @pytest.fixture
    def store(self):
        """Create a fresh store."""
        return MockSessionStore()

    def test_set_and_get(self, store):
        """Can set and retrieve data."""
        store.set("key1", {"value": 1}, ttl=3600)
        assert store.get("key1") == {"value": 1}

    def test_get_nonexistent(self, store):
        """Returns None for nonexistent key."""
        assert store.get("nonexistent") is None

    def test_delete(self, store):
        """Can delete data."""
        store.set("key1", {"value": 1}, ttl=3600)
        store.delete("key1")
        assert store.get("key1") is None

    def test_exists(self, store):
        """Can check if key exists."""
        store.set("key1", {"value": 1}, ttl=3600)
        assert store.exists("key1") is True
        assert store.exists("key2") is False

    def test_touch(self, store):
        """Touch returns True for existing keys."""
        store.set("key1", {"value": 1}, ttl=3600)
        assert store.touch("key1", ttl=7200) is True
        assert store.touch("nonexistent", ttl=7200) is False

    def test_clear(self, store):
        """Clear removes all data."""
        store.set("key1", {"value": 1}, ttl=3600)
        store.set("key2", {"value": 2}, ttl=3600)
        store.clear()
        assert store.get("key1") is None
        assert store.get("key2") is None

    def test_increment(self, store):
        """Can increment counters."""
        assert store.increment("counter1") == 1
        assert store.increment("counter1") == 2
        assert store.increment("counter1", amount=5) == 7

    def test_get_counter(self, store):
        """Can get counter value."""
        store.increment("counter1", amount=5)
        assert store.get_counter("counter1") == 5
        assert store.get_counter("nonexistent") == 0


class TestMockMFAProvider:
    """Tests for MockMFAProvider."""

    @pytest.fixture
    def provider(self):
        """Create provider with MFA enabled for user 1."""
        return MockMFAProvider(enabled_users={1}, valid_code="123456")

    @pytest.mark.anyio
    async def test_is_enabled(self, provider):
        """Returns True for enabled users."""
        user = MockUser(id=1, email="test@test.com")
        assert await provider.is_enabled(user) is True

    @pytest.mark.anyio
    async def test_is_not_enabled(self, provider):
        """Returns False for non-enabled users."""
        user = MockUser(id=2, email="test@test.com")
        assert await provider.is_enabled(user) is False

    @pytest.mark.anyio
    async def test_get_methods(self, provider):
        """Returns configured methods."""
        user = MockUser(id=1, email="test@test.com")
        methods = await provider.get_methods(user)
        assert "totp" in methods

    @pytest.mark.anyio
    async def test_send_challenge(self, provider):
        """Records sent challenges."""
        user = MockUser(id=1, email="test@test.com")
        result = await provider.send_challenge(user, "sms")
        assert result is True
        assert (1, "sms") in provider._challenges_sent

    @pytest.mark.anyio
    async def test_verify_valid_code(self, provider):
        """Accepts valid code."""
        user = MockUser(id=1, email="test@test.com")
        assert await provider.verify(user, "totp", "123456") is True

    @pytest.mark.anyio
    async def test_verify_invalid_code(self, provider):
        """Rejects invalid code."""
        user = MockUser(id=1, email="test@test.com")
        assert await provider.verify(user, "totp", "000000") is False


class TestMockRoleProvider:
    """Tests for MockRoleProvider."""

    @pytest.mark.anyio
    async def test_get_roles_from_list(self):
        """Gets roles from user.roles list."""
        provider = MockRoleProvider()
        user = MockUser(id=1, email="test@test.com", roles=["admin", "editor"])
        roles = await provider.get_roles(user)
        assert roles == {"admin", "editor"}

    @pytest.mark.anyio
    async def test_get_roles_empty(self):
        """Returns empty set for user without roles."""
        provider = MockRoleProvider()
        user = MockUser(id=1, email="test@test.com")
        roles = await provider.get_roles(user)
        assert roles == set()


class TestMockUserContextManager:
    """Tests for mock_user context manager."""

    def test_sets_user_in_context(self):
        """Sets user in AuthContext."""
        user = MockUser(id=1, email="test@test.com")

        with mock_user(user):
            assert AuthContext.user() == user
            assert AuthContext.is_authenticated() is True

    def test_restores_context_on_exit(self):
        """Restores context on exit."""
        user = MockUser(id=1, email="test@test.com")

        with mock_user(user):
            pass

        assert AuthContext.user() is None

    def test_yields_user(self):
        """Yields the user object."""
        user = MockUser(id=1, email="test@test.com")

        with mock_user(user) as u:
            assert u == user

    def test_sets_permissions(self):
        """Can set permissions on user."""
        user = MockUser(id=1, email="test@test.com")

        with mock_user(user, permissions={"posts.delete"}):
            assert "posts.delete" in user.permissions


class TestMockImpersonationContextManager:
    """Tests for mock_impersonation context manager."""

    def test_sets_impersonation(self):
        """Sets impersonation in AuthContext."""
        admin = MockUser(id=1, email="admin@test.com")
        target = MockUser(id=2, email="user@test.com")

        with mock_impersonation(admin, target):
            assert AuthContext.user() == target
            assert AuthContext.real_user() == admin
            assert AuthContext.is_impersonating() is True

    def test_restores_context_on_exit(self):
        """Restores context on exit."""
        admin = MockUser(id=1, email="admin@test.com")
        target = MockUser(id=2, email="user@test.com")

        with mock_impersonation(admin, target):
            pass

        assert AuthContext.user() is None
        assert AuthContext.is_impersonating() is False

    def test_yields_both_users(self):
        """Yields admin and target users."""
        admin = MockUser(id=1, email="admin@test.com")
        target = MockUser(id=2, email="user@test.com")

        with mock_impersonation(admin, target) as (a, t):
            assert a == admin
            assert t == target
