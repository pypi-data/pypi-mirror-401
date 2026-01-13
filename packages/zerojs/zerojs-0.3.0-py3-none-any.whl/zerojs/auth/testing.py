"""Testing utilities for the auth module.

Provides mock implementations and helpers for testing code
that uses the authentication system.

Example:
    from zerojs.auth.testing import mock_user, MockUser, MockUserProvider

    # Test protected endpoint
    def test_protected_endpoint(client):
        user = MockUser(id=1, email="test@example.com")
        with mock_user(user):
            response = client.get("/dashboard")
            assert response.status_code == 200

    # Test with permissions
    def test_delete_requires_permission(client):
        user = MockUser(id=1, email="test@example.com")
        with mock_user(user, permissions={"users.delete"}):
            response = client.delete("/users/123")
            assert response.status_code == 200
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from .context import AuthContext

T = TypeVar("T")


@dataclass
class MockUser:
    """Simple user object for testing.

    Provides a minimal user implementation with common attributes.

    Attributes:
        id: User ID.
        email: User email address.
        username: Optional username.
        is_active: Whether the user account is active.
        roles: List of role names for RBAC testing.
        permissions: Set of direct permissions for testing.

    Example:
        user = MockUser(id=1, email="admin@example.com", roles=["admin"])
        assert user.is_active
        assert "admin" in user.roles
    """

    id: int
    email: str
    username: str | None = None
    is_active: bool = True
    roles: list[str] = field(default_factory=list)
    permissions: set[str] = field(default_factory=set)


class MockUserProvider(Generic[T]):
    """In-memory user provider for testing.

    Stores users in memory and provides lookup by ID or identifier.

    Example:
        users = [
            MockUser(id=1, email="user@test.com"),
            MockUser(id=2, email="admin@test.com", roles=["admin"]),
        ]
        provider = MockUserProvider(users)

        user = await provider.get_by_identifier("user@test.com")
        assert user.id == 1

        admin = await provider.get_by_id(2)
        assert "admin" in admin.roles
    """

    def __init__(self, users: list[T] | None = None):
        """Initialize the mock provider.

        Args:
            users: List of user objects to store.
        """
        self._by_id: dict[Any, T] = {}
        self._by_identifier: dict[str, T] = {}

        for user in users or []:
            self.add_user(user)

    def add_user(self, user: T) -> None:
        """Add a user to the provider.

        Args:
            user: User object to add.
        """
        user_id = getattr(user, "id", None)
        if user_id is not None:
            self._by_id[user_id] = user

        # Index by common identifier fields
        for field_name in ("email", "username", "phone"):
            if identifier := getattr(user, field_name, None):
                self._by_identifier[identifier.lower()] = user

    def remove_user(self, user_id: Any) -> None:
        """Remove a user from the provider.

        Args:
            user_id: ID of the user to remove.
        """
        user = self._by_id.pop(user_id, None)
        if user:
            for field_name in ("email", "username", "phone"):
                if identifier := getattr(user, field_name, None):
                    self._by_identifier.pop(identifier.lower(), None)

    async def get_by_identifier(self, identifier: str) -> T | None:
        """Find user by email, username, or phone.

        Args:
            identifier: The identifier to search for.

        Returns:
            User if found, None otherwise.
        """
        return self._by_identifier.get(identifier.lower())

    async def get_by_id(self, user_id: Any) -> T | None:
        """Find user by ID.

        Args:
            user_id: The user ID to search for.

        Returns:
            User if found, None otherwise.
        """
        return self._by_id.get(user_id)

    async def is_active(self, user: T) -> bool:
        """Check if user account is active.

        Args:
            user: The user to check.

        Returns:
            True if user is active, False otherwise.
        """
        return getattr(user, "is_active", True)


class MockCredentialVerifier:
    """Simple credential verifier for testing.

    Verifies credentials against a predefined password or
    a dictionary of user-specific passwords.

    Example:
        # All passwords are "password" by default
        verifier = MockCredentialVerifier()

        # Or specify valid password
        verifier = MockCredentialVerifier(valid_password="secret123")

        # Or use a dict of user_id -> password
        verifier = MockCredentialVerifier(passwords={1: "pass1", 2: "pass2"})
    """

    def __init__(
        self,
        valid_password: str = "password",
        passwords: dict[Any, str] | None = None,
    ):
        """Initialize the mock verifier.

        Args:
            valid_password: Default password for all users.
            passwords: Optional dict mapping user IDs to passwords.
        """
        self._valid_password = valid_password
        self._passwords = passwords or {}

    async def verify(self, user: Any, credential: str) -> bool:
        """Verify credential against user.

        Args:
            user: The user to verify against.
            credential: The credential (password) to verify.

        Returns:
            True if credential is valid, False otherwise.
        """
        user_id = getattr(user, "id", None)
        if user_id in self._passwords:
            return credential == self._passwords[user_id]
        return credential == self._valid_password


class MockSessionStore:
    """In-memory session store for testing.

    Provides all SessionStore methods including counter operations.
    TTL is tracked but not enforced (items don't expire automatically).

    Example:
        store = MockSessionStore()
        store.set("session:123", {"user_id": 1}, ttl=3600)
        data = store.get("session:123")
        assert data["user_id"] == 1
    """

    def __init__(self) -> None:
        """Initialize the mock store."""
        self._data: dict[str, Any] = {}
        self._counters: dict[str, int] = {}
        self._ttls: dict[str, int] = {}

    def get(self, key: str) -> Any | None:
        """Get data by key.

        Args:
            key: The key to retrieve.

        Returns:
            Stored data or None if not found.
        """
        return self._data.get(key)

    def set(self, key: str, data: Any, ttl: int) -> None:
        """Store data with TTL.

        Args:
            key: The key to store under.
            data: The data to store.
            ttl: Time-to-live in seconds (tracked but not enforced).
        """
        self._data[key] = data
        self._ttls[key] = ttl

    def delete(self, key: str) -> None:
        """Delete data by key.

        Args:
            key: The key to delete.
        """
        self._data.pop(key, None)
        self._counters.pop(key, None)
        self._ttls.pop(key, None)

    def exists(self, key: str) -> bool:
        """Check if key exists.

        Args:
            key: The key to check.

        Returns:
            True if key exists, False otherwise.
        """
        return key in self._data or key in self._counters

    def touch(self, key: str, ttl: int) -> bool:
        """Update TTL for a key.

        Args:
            key: The key to update.
            ttl: New TTL in seconds.

        Returns:
            True if key exists, False otherwise.
        """
        if key in self._data:
            self._ttls[key] = ttl
            return True
        return False

    def clear(self) -> None:
        """Clear all data."""
        self._data.clear()
        self._counters.clear()
        self._ttls.clear()

    def increment(self, key: str, amount: int = 1, ttl: int = 0) -> int:
        """Atomically increment a counter.

        Args:
            key: The counter key.
            amount: Amount to increment by.
            ttl: Optional TTL in seconds.

        Returns:
            New counter value after increment.
        """
        self._counters[key] = self._counters.get(key, 0) + amount
        if ttl > 0:
            self._ttls[key] = ttl
        return self._counters[key]

    def get_counter(self, key: str) -> int:
        """Get counter value.

        Args:
            key: The counter key.

        Returns:
            Counter value or 0 if not found.
        """
        return self._counters.get(key, 0)


class MockMFAProvider(Generic[T]):
    """Mock MFA provider for testing.

    Simulates MFA with configurable behavior.

    Example:
        provider = MockMFAProvider(
            enabled_users={1, 2},
            valid_code="123456",
        )

        # Check if user has MFA enabled
        assert await provider.is_enabled(user_with_id_1)

        # Verify a code
        assert await provider.verify(user, "totp", "123456")
    """

    def __init__(
        self,
        enabled_users: set[Any] | None = None,
        methods: list[str] | None = None,
        valid_code: str = "123456",
    ):
        """Initialize the mock provider.

        Args:
            enabled_users: Set of user IDs with MFA enabled.
            methods: Available MFA methods (default: ["totp"]).
            valid_code: The code that will be accepted as valid.
        """
        self._enabled_users = enabled_users or set()
        self._methods = methods or ["totp"]
        self._valid_code = valid_code
        self._challenges_sent: list[tuple[Any, str]] = []

    async def is_enabled(self, user: T) -> bool:
        """Check if user has MFA enabled.

        Args:
            user: The user to check.

        Returns:
            True if MFA is enabled, False otherwise.
        """
        user_id = getattr(user, "id", None)
        return user_id in self._enabled_users

    async def get_methods(self, user: T) -> list[str]:
        """Get available MFA methods for user.

        Args:
            user: The user to get methods for.

        Returns:
            List of available method names.
        """
        return self._methods.copy()

    async def send_challenge(self, user: T, method: str) -> bool:
        """Send MFA challenge to user.

        Args:
            user: The user to send challenge to.
            method: The MFA method to use.

        Returns:
            True if challenge was sent.
        """
        user_id = getattr(user, "id", None)
        self._challenges_sent.append((user_id, method))
        return True

    async def verify(self, user: T, method: str, code: str) -> bool:
        """Verify MFA code.

        Args:
            user: The user to verify for.
            method: The MFA method used.
            code: The code to verify.

        Returns:
            True if code is valid, False otherwise.
        """
        return code == self._valid_code


class MockRoleProvider:
    """Mock role provider for RBAC testing.

    Example:
        provider = MockRoleProvider()

        user = MockUser(id=1, roles=["admin", "editor"])
        roles = await provider.get_roles(user)
        assert "admin" in roles
    """

    async def get_roles(self, user: Any) -> set[str]:
        """Get roles for a user.

        Args:
            user: The user to get roles for.

        Returns:
            Set of role names.
        """
        roles = getattr(user, "roles", [])
        return set(roles) if isinstance(roles, list) else roles


@contextmanager
def mock_user(user: Any, permissions: set[str] | None = None) -> Iterator[Any]:
    """Context manager to mock an authenticated user in tests.

    Sets the user in AuthContext for the duration of the context.
    Optionally sets direct permissions for the user.

    Args:
        user: The user object to set as current user.
        permissions: Optional set of permission strings.

    Yields:
        The user object.

    Example:
        with mock_user(fake_user):
            response = client.get("/protected")
            assert response.status_code == 200

        with mock_user(admin_user, permissions={"users.delete"}):
            response = client.delete("/users/123")
            assert response.status_code == 200
    """
    # Store original permissions if we're adding them
    if permissions is not None:
        original_permissions = getattr(user, "permissions", None)
        if hasattr(user, "permissions"):
            user.permissions = permissions
        else:
            # For objects that don't have permissions attribute
            object.__setattr__(user, "permissions", permissions)

    token = AuthContext.set_user(user)
    try:
        yield user
    finally:
        AuthContext.reset(token)
        # Restore original permissions
        if permissions is not None and original_permissions is not None:
            user.permissions = original_permissions


@contextmanager
def mock_impersonation(admin: Any, target: Any) -> Iterator[tuple[Any, Any]]:
    """Context manager to mock impersonation in tests.

    Sets both the real user (admin) and current user (target)
    in AuthContext for the duration of the context.

    Args:
        admin: The admin user performing impersonation.
        target: The target user being impersonated.

    Yields:
        Tuple of (admin, target).

    Example:
        with mock_impersonation(admin_user, regular_user):
            assert AuthContext.user() == regular_user
            assert AuthContext.real_user() == admin_user
            assert AuthContext.is_impersonating()
    """
    with AuthContext.impersonating(admin, target):
        yield admin, target
