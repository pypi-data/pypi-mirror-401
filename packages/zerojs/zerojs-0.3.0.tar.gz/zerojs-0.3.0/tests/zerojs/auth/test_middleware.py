"""Tests for auth middleware."""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from zerojs.auth import AuthContext, AuthMiddleware
from zerojs.auth.testing import MockUser, MockUserProvider


def test_middleware_skips_non_http_scope() -> None:
    """Middleware passes through non-http scopes without processing."""

    async def run_test() -> None:
        app = AsyncMock()
        provider = MockUserProvider()
        middleware = AuthMiddleware(app, provider)

        scope: dict[str, Any] = {"type": "lifespan"}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        app.assert_called_once_with(scope, receive, send)

    asyncio.run(run_test())


def test_middleware_no_session_no_user() -> None:
    """When no session exists, request proceeds without user."""

    async def run_test() -> None:
        app = AsyncMock()
        provider = MockUserProvider()
        middleware = AuthMiddleware(app, provider)

        scope: dict[str, Any] = {"type": "http", "state": {}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        app.assert_called_once()
        # User should not be set in context
        assert AuthContext.user() is None

    asyncio.run(run_test())


def test_middleware_loads_user_from_session() -> None:
    """Middleware loads user from session and sets context."""

    async def run_test() -> None:
        user = MockUser(id=1, email="alice@test.com")
        provider = MockUserProvider([user])

        captured_user = None

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user
            captured_user = AuthContext.user()

        middleware = AuthMiddleware(capture_app, provider)

        session = MagicMock()
        session.get.side_effect = lambda key: 1 if key == "user_id" else None

        state = MagicMock()
        state.session = session

        scope: dict[str, Any] = {"type": "http", "state": state}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        assert captured_user is user

    asyncio.run(run_test())


def test_middleware_loads_user_from_dict_session() -> None:
    """Middleware loads user when session is in dict format."""

    async def run_test() -> None:
        user = MockUser(id=1, email="bob@test.com")
        provider = MockUserProvider([user])

        captured_user = None

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user
            captured_user = AuthContext.user()

        middleware = AuthMiddleware(capture_app, provider)

        session = {"user_id": 1}
        scope: dict[str, Any] = {"type": "http", "state": {"session": session}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        assert captured_user is user

    asyncio.run(run_test())


def test_middleware_handles_missing_user() -> None:
    """When session has user_id but user not found, proceeds without user."""

    async def run_test() -> None:
        provider = MockUserProvider()  # Empty provider

        captured_user = "not_set"

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user
            captured_user = AuthContext.user()

        middleware = AuthMiddleware(capture_app, provider)

        session = {"user_id": 999}  # User doesn't exist
        scope: dict[str, Any] = {"type": "http", "state": {"session": session}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        assert captured_user is None

    asyncio.run(run_test())


def test_middleware_handles_impersonation() -> None:
    """Middleware sets up impersonation context when impersonator_id present."""

    async def run_test() -> None:
        admin = MockUser(id=1, email="admin@test.com")
        target_user = MockUser(id=2, email="target@test.com")
        provider = MockUserProvider([admin, target_user])

        captured_user = None
        captured_real_user = None
        captured_is_impersonating = None

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user, captured_real_user, captured_is_impersonating
            captured_user = AuthContext.user()
            captured_real_user = AuthContext.real_user()
            captured_is_impersonating = AuthContext.is_impersonating()

        middleware = AuthMiddleware(capture_app, provider)

        session = MagicMock()
        session.get.side_effect = lambda key: {
            "user_id": 2,  # Target user
            "impersonator_id": 1,  # Admin impersonating
        }.get(key)

        state = MagicMock()
        state.session = session

        scope: dict[str, Any] = {"type": "http", "state": state}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        assert captured_user is target_user
        assert captured_real_user is admin
        assert captured_is_impersonating is True

    asyncio.run(run_test())


def test_middleware_custom_session_key() -> None:
    """Middleware uses custom session key when configured."""

    async def run_test() -> None:
        user = MockUser(id=1, email="custom@test.com")
        provider = MockUserProvider([user])

        captured_user = None

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user
            captured_user = AuthContext.user()

        middleware = AuthMiddleware(capture_app, provider, session_key="uid")

        session = {"uid": 1, "user_id": 999}  # Should use uid, not user_id
        scope: dict[str, Any] = {"type": "http", "state": {"session": session}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        assert captured_user is user

    asyncio.run(run_test())


def test_middleware_websocket_support() -> None:
    """Middleware works with websocket scope type."""

    async def run_test() -> None:
        user = MockUser(id=1, email="websocket@test.com")
        provider = MockUserProvider([user])

        captured_user = None

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user
            captured_user = AuthContext.user()

        middleware = AuthMiddleware(capture_app, provider)

        session = {"user_id": 1}
        scope: dict[str, Any] = {"type": "websocket", "state": {"session": session}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        assert captured_user is user

    asyncio.run(run_test())


def test_middleware_context_cleanup() -> None:
    """Context is cleaned up after request completes."""

    async def run_test() -> None:
        user = MockUser(id=1, email="cleanup@test.com")
        provider = MockUserProvider([user])

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            assert AuthContext.user() is user

        middleware = AuthMiddleware(capture_app, provider)

        session = {"user_id": 1}
        scope: dict[str, Any] = {"type": "http", "state": {"session": session}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        # After middleware completes, context should be cleared
        assert AuthContext.user() is None

    asyncio.run(run_test())


def test_middleware_impersonation_without_user() -> None:
    """Impersonation is ignored if target user not found."""

    async def run_test() -> None:
        admin = MockUser(id=1, email="admin@test.com")
        provider = MockUserProvider([admin])  # No user 2

        captured_user = None
        captured_is_impersonating = None

        async def capture_app(scope: dict[str, Any], receive: Any, send: Any) -> None:
            nonlocal captured_user, captured_is_impersonating
            captured_user = AuthContext.user()
            captured_is_impersonating = AuthContext.is_impersonating()

        middleware = AuthMiddleware(capture_app, provider)

        session = {"user_id": 2, "impersonator_id": 1}  # User 2 doesn't exist
        scope: dict[str, Any] = {"type": "http", "state": {"session": session}}
        receive = AsyncMock()
        send = AsyncMock()

        await middleware(scope, receive, send)

        # Neither should be set since user 2 doesn't exist
        assert captured_user is None
        assert captured_is_impersonating is False

    asyncio.run(run_test())
