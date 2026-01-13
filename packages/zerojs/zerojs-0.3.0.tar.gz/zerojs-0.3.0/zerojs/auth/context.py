"""Authentication context using ContextVars.

Provides thread-safe access to the current authenticated user
from anywhere in the code, without passing it explicitly.

Uses Python's contextvars for proper async/await support.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generic, TypeVar

from .exceptions import AuthenticationError

T = TypeVar("T")


class AuthContext(Generic[T]):
    """Access current user from anywhere in the code.

    Uses ContextVars for thread-safe, async-safe user storage.
    Each request gets its own context automatically.

    Basic usage:
        # In middleware - set user
        with AuthContext.as_user(user):
            await app(scope, receive, send)

        # In route handler - get user
        user = AuthContext.user()  # May be None
        user = AuthContext.require_user()  # Raises if None

    Impersonation (admin acting as another user):
        with AuthContext.impersonating(admin, target_user):
            # AuthContext.user() returns target_user
            # AuthContext.real_user() returns admin
            await app(scope, receive, send)
    """

    _current_user: ContextVar[T | None] = ContextVar("current_user", default=None)
    _real_user: ContextVar[T | None] = ContextVar("real_user", default=None)

    # --- Basic methods ---

    @classmethod
    def set_user(cls, user: T | None) -> object:
        """Set current user. Returns token for reset.

        Prefer using `as_user()` context manager instead.

        Args:
            user: User object to set, or None to clear.

        Returns:
            Token that can be passed to reset() to restore previous value.
        """
        return cls._current_user.set(user)

    @classmethod
    def reset(cls, token: object) -> None:
        """Restore previous context.

        Args:
            token: Token returned by set_user().
        """
        cls._current_user.reset(token)  # type: ignore[arg-type]

    @classmethod
    def user(cls) -> T | None:
        """Get effective user (may be impersonated).

        Returns:
            Current user object, or None if not authenticated.
        """
        return cls._current_user.get()

    @classmethod
    def require_user(cls) -> T:
        """Get current user or raise AuthenticationError.

        Returns:
            Current user object.

        Raises:
            AuthenticationError: If no user is authenticated.
        """
        user = cls._current_user.get()
        if user is None:
            raise AuthenticationError("Authentication required")
        return user

    @classmethod
    def is_authenticated(cls) -> bool:
        """Check if user is authenticated.

        Returns:
            True if a user is set in context.
        """
        return cls._current_user.get() is not None

    # --- Context Managers (recommended for middleware) ---

    @classmethod
    @contextmanager
    def as_user(cls, user: T | None) -> Iterator[None]:
        """Context manager to set user temporarily.

        Automatically resets to previous value on exit.

        Example:
            with AuthContext.as_user(user):
                await app(scope, receive, send)

        Args:
            user: User to set for the duration of the context.

        Yields:
            None
        """
        token = cls._current_user.set(user)
        try:
            yield
        finally:
            cls._current_user.reset(token)

    @classmethod
    @contextmanager
    def impersonating(cls, admin: T, target: T) -> Iterator[None]:
        """Context manager for impersonation.

        Sets the effective user to `target` while remembering
        the real user (`admin`) for audit purposes.

        Example:
            with AuthContext.impersonating(admin, target):
                # AuthContext.user() returns target
                # AuthContext.real_user() returns admin
                await app(scope, receive, send)

        Args:
            admin: The real user (admin doing the impersonation).
            target: The user being impersonated.

        Yields:
            None
        """
        admin_token = cls._real_user.set(admin)
        user_token = cls._current_user.set(target)
        try:
            yield
        finally:
            cls._current_user.reset(user_token)
            cls._real_user.reset(admin_token)

    # --- Impersonation (direct methods) ---

    @classmethod
    def real_user(cls) -> T | None:
        """Get real user (admin who is impersonating).

        If not impersonating, returns the current user.

        Returns:
            The real user (admin) if impersonating,
            otherwise the current user.
        """
        return cls._real_user.get() or cls._current_user.get()

    @classmethod
    def is_impersonating(cls) -> bool:
        """Check if impersonation is active.

        Returns:
            True if a real_user is set (admin is impersonating).
        """
        return cls._real_user.get() is not None
