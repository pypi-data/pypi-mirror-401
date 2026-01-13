"""Tests for auth decorators."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from zerojs.auth import AuthContext, AuthenticationError, requires_auth
from zerojs.auth.testing import MockUser


def test_requires_auth_allows_authenticated_user() -> None:
    """Decorated function executes when user is authenticated."""

    async def run_test() -> None:
        @requires_auth
        async def protected_endpoint() -> str:
            return "success"

        user = MockUser(id=1, email="alice@test.com")

        with AuthContext.as_user(user):
            result = await protected_endpoint()
            assert result == "success"

    asyncio.run(run_test())


def test_requires_auth_raises_for_unauthenticated() -> None:
    """Decorated function raises AuthenticationError when no user."""

    async def run_test() -> None:
        @requires_auth
        async def protected_endpoint() -> str:
            return "success"

        with pytest.raises(AuthenticationError):
            await protected_endpoint()

    asyncio.run(run_test())


def test_requires_auth_passes_arguments() -> None:
    """Decorated function receives all arguments correctly."""

    async def run_test() -> None:
        @requires_auth
        async def protected_endpoint(arg1: str, arg2: int, *, kwarg1: str = "default") -> dict[str, Any]:
            return {"arg1": arg1, "arg2": arg2, "kwarg1": kwarg1}

        user = MockUser(id=1, email="test@test.com")

        with AuthContext.as_user(user):
            result = await protected_endpoint("hello", 42, kwarg1="custom")
            assert result == {"arg1": "hello", "arg2": 42, "kwarg1": "custom"}

    asyncio.run(run_test())


def test_requires_auth_preserves_function_metadata() -> None:
    """Decorator preserves original function's metadata."""

    @requires_auth
    async def documented_function() -> None:
        """This is a documented function."""
        pass

    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "This is a documented function."


def test_requires_auth_with_class_method() -> None:
    """Decorator works with class methods."""

    async def run_test() -> None:
        class MyService:
            @requires_auth
            async def protected_method(self, value: int) -> int:
                return value * 2

        service = MyService()
        user = MockUser(id=1, email="test@test.com")

        with AuthContext.as_user(user):
            result = await service.protected_method(21)
            assert result == 42

    asyncio.run(run_test())


def test_requires_auth_with_impersonation() -> None:
    """Decorator allows access during impersonation."""

    async def run_test() -> None:
        @requires_auth
        async def protected_endpoint() -> tuple[Any, Any, bool]:
            return AuthContext.user(), AuthContext.real_user(), AuthContext.is_impersonating()

        admin = MockUser(id=1, email="admin@test.com")
        target = MockUser(id=2, email="target@test.com")

        with AuthContext.impersonating(admin, target):
            user, real_user, is_impersonating = await protected_endpoint()
            assert user is target
            assert real_user is admin
            assert is_impersonating is True

    asyncio.run(run_test())


def test_requires_auth_raises_correct_error_type() -> None:
    """Decorator raises AuthenticationError specifically."""

    async def run_test() -> None:
        @requires_auth
        async def protected_endpoint() -> str:
            return "success"

        with pytest.raises(AuthenticationError) as exc_info:
            await protected_endpoint()

        assert "authentication required" in str(exc_info.value).lower()

    asyncio.run(run_test())


def test_requires_auth_multiple_decorators() -> None:
    """requires_auth can be combined with other decorators."""

    async def run_test() -> None:
        def logger(fn: Any) -> Any:
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = await fn(*args, **kwargs)
                return f"logged: {result}"

            return wrapper

        @logger
        @requires_auth
        async def protected_endpoint() -> str:
            return "success"

        user = MockUser(id=1, email="test@test.com")

        with AuthContext.as_user(user):
            result = await protected_endpoint()
            assert result == "logged: success"

    asyncio.run(run_test())


def test_requires_auth_context_available_in_function() -> None:
    """User context is available inside decorated function."""

    async def run_test() -> None:
        @requires_auth
        async def protected_endpoint() -> str:
            user = AuthContext.user()
            assert user is not None
            return f"Hello, {user.username}"

        user = MockUser(id=1, email="charlie@test.com", username="Charlie")

        with AuthContext.as_user(user):
            result = await protected_endpoint()
            assert result == "Hello, Charlie"

    asyncio.run(run_test())
