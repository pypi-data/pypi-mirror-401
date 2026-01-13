"""Tests for AuthContext."""

import pytest

from zerojs.auth import AuthContext, AuthenticationError
from zerojs.auth.testing import MockUser


class TestAuthContextBasic:
    """Tests for basic AuthContext methods."""

    def test_user_default_is_none(self) -> None:
        """user() returns None by default."""
        # Reset context to ensure clean state
        with AuthContext.as_user(None):
            assert AuthContext.user() is None

    def test_set_user_and_get(self) -> None:
        """set_user() and user() work together."""
        user = MockUser(id=1, email="alice@test.com")
        token = AuthContext.set_user(user)
        try:
            assert AuthContext.user() == user
        finally:
            AuthContext.reset(token)

    def test_reset_restores_previous(self) -> None:
        """reset() restores previous user."""
        user1 = MockUser(id=1, email="alice@test.com")
        user2 = MockUser(id=2, email="bob@test.com")

        token1 = AuthContext.set_user(user1)
        token2 = AuthContext.set_user(user2)

        assert AuthContext.user() == user2
        AuthContext.reset(token2)
        assert AuthContext.user() == user1
        AuthContext.reset(token1)

    def test_is_authenticated_true(self) -> None:
        """is_authenticated() returns True when user is set."""
        user = MockUser(id=1, email="alice@test.com")
        with AuthContext.as_user(user):
            assert AuthContext.is_authenticated() is True

    def test_is_authenticated_false(self) -> None:
        """is_authenticated() returns False when no user."""
        with AuthContext.as_user(None):
            assert AuthContext.is_authenticated() is False

    def test_require_user_returns_user(self) -> None:
        """require_user() returns user when authenticated."""
        user = MockUser(id=1, email="alice@test.com")
        with AuthContext.as_user(user):
            assert AuthContext.require_user() == user

    def test_require_user_raises_when_no_user(self) -> None:
        """require_user() raises AuthenticationError when no user."""
        with AuthContext.as_user(None):
            with pytest.raises(AuthenticationError, match="Authentication required"):
                AuthContext.require_user()


class TestAuthContextAsUser:
    """Tests for as_user() context manager."""

    def test_as_user_sets_user(self) -> None:
        """as_user() sets user in context."""
        user = MockUser(id=1, email="alice@test.com")
        with AuthContext.as_user(user):
            assert AuthContext.user() == user

    def test_as_user_restores_on_exit(self) -> None:
        """as_user() restores previous user on exit."""
        user1 = MockUser(id=1, email="alice@test.com")
        user2 = MockUser(id=2, email="bob@test.com")

        with AuthContext.as_user(user1):
            assert AuthContext.user() == user1
            with AuthContext.as_user(user2):
                assert AuthContext.user() == user2
            assert AuthContext.user() == user1

    def test_as_user_restores_on_exception(self) -> None:
        """as_user() restores on exception."""
        user = MockUser(id=1, email="alice@test.com")

        with AuthContext.as_user(None):
            try:
                with AuthContext.as_user(user):
                    assert AuthContext.user() == user
                    raise ValueError("test error")
            except ValueError:
                pass
            assert AuthContext.user() is None

    def test_as_user_with_none(self) -> None:
        """as_user(None) clears user."""
        user = MockUser(id=1, email="alice@test.com")
        with AuthContext.as_user(user):
            with AuthContext.as_user(None):
                assert AuthContext.user() is None
            assert AuthContext.user() == user


class TestAuthContextImpersonation:
    """Tests for impersonation features."""

    def test_impersonating_sets_both_users(self) -> None:
        """impersonating() sets current and real user."""
        admin = MockUser(id=1, email="admin@test.com")
        target = MockUser(id=2, email="target@test.com")

        with AuthContext.impersonating(admin, target):
            assert AuthContext.user() == target
            assert AuthContext.real_user() == admin
            assert AuthContext.is_impersonating() is True

    def test_impersonating_restores_on_exit(self) -> None:
        """impersonating() restores both users on exit."""
        admin = MockUser(id=1, email="admin@test.com")
        target = MockUser(id=2, email="target@test.com")
        original = MockUser(id=3, email="original@test.com")

        with AuthContext.as_user(original):
            assert AuthContext.user() == original
            assert AuthContext.is_impersonating() is False

            with AuthContext.impersonating(admin, target):
                assert AuthContext.user() == target
                assert AuthContext.real_user() == admin

            assert AuthContext.user() == original
            assert AuthContext.is_impersonating() is False

    def test_real_user_without_impersonation(self) -> None:
        """real_user() returns current user when not impersonating."""
        user = MockUser(id=1, email="alice@test.com")
        with AuthContext.as_user(user):
            assert AuthContext.real_user() == user
            assert AuthContext.is_impersonating() is False

    def test_real_user_none_without_user(self) -> None:
        """real_user() returns None when no user."""
        with AuthContext.as_user(None):
            assert AuthContext.real_user() is None

    def test_is_impersonating_false_by_default(self) -> None:
        """is_impersonating() is False by default."""
        with AuthContext.as_user(None):
            assert AuthContext.is_impersonating() is False

    def test_nested_impersonation(self) -> None:
        """Nested impersonation works correctly."""
        admin1 = MockUser(id=1, email="admin1@test.com")
        admin2 = MockUser(id=2, email="admin2@test.com")
        target1 = MockUser(id=3, email="target1@test.com")
        target2 = MockUser(id=4, email="target2@test.com")

        with AuthContext.impersonating(admin1, target1):
            assert AuthContext.user() == target1
            assert AuthContext.real_user() == admin1

            with AuthContext.impersonating(admin2, target2):
                assert AuthContext.user() == target2
                assert AuthContext.real_user() == admin2

            assert AuthContext.user() == target1
            assert AuthContext.real_user() == admin1


class TestAuthContextIsolation:
    """Tests for context isolation."""

    def test_contexts_are_isolated(self) -> None:
        """Different contexts are isolated."""
        from concurrent.futures import ThreadPoolExecutor

        user1 = MockUser(id=1, email="user1@test.com")
        user2 = MockUser(id=2, email="user2@test.com")
        results: dict[str, MockUser | None] = {}

        def set_and_get_user(name: str, user: MockUser) -> None:
            with AuthContext.as_user(user):
                # Simulate some async work
                import time

                time.sleep(0.01)
                results[name] = AuthContext.user()

        # Run in threads to test isolation
        with ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(set_and_get_user, "thread1", user1)
            f2 = executor.submit(set_and_get_user, "thread2", user2)
            f1.result()
            f2.result()

        # Each thread should see its own user
        assert results["thread1"] == user1
        assert results["thread2"] == user2

    def test_async_contexts_are_isolated(self) -> None:
        """Async contexts are properly isolated."""
        import asyncio

        user1 = MockUser(id=1, email="user1@test.com")
        user2 = MockUser(id=2, email="user2@test.com")
        results: dict[str, MockUser | None] = {}

        async def set_and_get_user(name: str, user: MockUser) -> None:
            with AuthContext.as_user(user):
                await asyncio.sleep(0.01)
                results[name] = AuthContext.user()

        async def run_both() -> None:
            await asyncio.gather(
                set_and_get_user("task1", user1),
                set_and_get_user("task2", user2),
            )

        asyncio.run(run_both())

        # Each task should see its own user
        assert results["task1"] == user1
        assert results["task2"] == user2
