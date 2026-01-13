"""Authentication middleware.

Loads user from session and sets it in AuthContext for the duration
of each request.
"""

from typing import Any

from starlette.types import ASGIApp, Receive, Scope, Send

from .context import AuthContext
from .protocols import UserProvider


class AuthMiddleware:
    """Authentication middleware.

    Loads user from session and sets it in AuthContext.
    Must come AFTER SessionMiddleware in MIDDLEWARE list.

    Settings:
        AUTH_USER_PROVIDER: Dotted path to class implementing UserProvider
        AUTH_SESSION_KEY: Session key for user_id (default: "user_id")
        AUTH_IMPERSONATOR_KEY: Key for impersonation (default: "impersonator_id")

    Example:
        # settings.py
        MIDDLEWARE = [
            "zerojs.session.SessionMiddleware",
            "zerojs.auth.AuthMiddleware",  # Must come AFTER SessionMiddleware
        ]

        AUTH_USER_PROVIDER = "myapp.auth.MyUserProvider"
        AUTH_SESSION_KEY = "user_id"
        AUTH_IMPERSONATOR_KEY = "impersonator_id"
    """

    def __init__(
        self,
        app: ASGIApp,
        user_provider: UserProvider[Any],
        session_key: str = "user_id",
        impersonator_key: str = "impersonator_id",
    ):
        """Initialize the middleware.

        Args:
            app: The ASGI application.
            user_provider: Provider for loading users by ID.
            session_key: Session key containing the user ID.
            impersonator_key: Session key for impersonator ID.
        """
        self.app = app
        self.user_provider = user_provider
        self.session_key = session_key
        self.impersonator_key = impersonator_key

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        """Process the request.

        Loads user from session and sets AuthContext for the request duration.
        """
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        # Get session from previous middleware
        state = scope.get("state", {})
        session = getattr(state, "session", None) or state.get("session")

        user = None
        impersonator = None

        if session:
            # Load user
            user_id = session.get(self.session_key)
            if user_id is not None:
                user = await self.user_provider.get_by_id(user_id)

            # Check impersonation
            if user:
                impersonator_id = session.get(self.impersonator_key)
                if impersonator_id is not None:
                    impersonator = await self.user_provider.get_by_id(impersonator_id)

        # Use context managers to ensure cleanup
        if impersonator and user:
            with AuthContext.impersonating(impersonator, user):
                await self.app(scope, receive, send)
        elif user:
            with AuthContext.as_user(user):
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
