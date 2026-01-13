"""Authentication event system.

Provides an event emitter for authentication-related events,
allowing extensibility through listeners for logging, auditing,
notifications, and custom business logic.

Example:
    from zerojs.auth import AuthEvent, AuthEventEmitter

    events = AuthEventEmitter()

    @events.on(AuthEvent.LOGIN_FAILED)
    async def log_failed_attempt(identifier: str, ip: str, **ctx):
        await audit_log.record(f"Failed login: {identifier} from {ip}")

    @events.on(AuthEvent.LOGIN_SUCCESS)
    async def update_last_login(user, ip: str, **ctx):
        user.last_login = datetime.now()
        await user.save()

    # Emit events from your auth code
    await events.emit(AuthEvent.LOGIN_FAILED, identifier="user@example.com", ip="1.2.3.4")
"""

import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

logger = logging.getLogger("zerojs.auth.events")


class AuthEvent(Enum):
    """Authentication events.

    Use these events to hook into authentication lifecycle:

    Login/Logout:
        - LOGIN_SUCCESS: User successfully authenticated
        - LOGIN_FAILED: Authentication attempt failed
        - LOGOUT: User logged out

    Password:
        - PASSWORD_CHANGED: User changed their password
        - PASSWORD_RESET_REQUESTED: Password reset was requested
        - PASSWORD_RESET_COMPLETED: Password reset was completed

    Session:
        - SESSION_EXPIRED: Session expired
        - SESSION_ROTATED: Session ID was rotated

    MFA:
        - MFA_ENABLED: User enabled MFA
        - MFA_DISABLED: User disabled MFA
        - MFA_CHALLENGE_SENT: MFA challenge was sent
        - MFA_CHALLENGE_PASSED: MFA challenge was passed
        - MFA_CHALLENGE_FAILED: MFA challenge failed

    Impersonation:
        - IMPERSONATION_START: Admin started impersonating a user
        - IMPERSONATION_END: Admin stopped impersonating

    Authorization:
        - PERMISSION_DENIED: Permission check failed
    """

    LOGIN_SUCCESS = auto()
    LOGIN_FAILED = auto()
    LOGOUT = auto()
    PASSWORD_CHANGED = auto()
    PASSWORD_RESET_REQUESTED = auto()
    PASSWORD_RESET_COMPLETED = auto()
    SESSION_EXPIRED = auto()
    SESSION_ROTATED = auto()
    MFA_ENABLED = auto()
    MFA_DISABLED = auto()
    MFA_CHALLENGE_SENT = auto()
    MFA_CHALLENGE_PASSED = auto()
    MFA_CHALLENGE_FAILED = auto()
    IMPERSONATION_START = auto()
    IMPERSONATION_END = auto()
    PERMISSION_DENIED = auto()


@dataclass
class ListenerConfig:
    """Configuration for an event listener.

    Attributes:
        fn: The async listener function.
        critical: If True, errors will be re-raised instead of just logged.
    """

    fn: Callable[..., Awaitable[None]]
    critical: bool = False


class AuthEventEmitter:
    """Event emitter for authentication events.

    Allows registering async listeners that are called when events are emitted.
    By default, listener errors are logged but don't propagate - events should
    not break the authentication flow. Use critical=True for listeners that
    must succeed.

    Example:
        events = AuthEventEmitter()

        # Using decorator
        @events.on(AuthEvent.LOGIN_SUCCESS)
        async def on_login(user, ip: str, **ctx):
            await send_login_notification(user.email, ip)

        # Critical listener (errors will propagate)
        @events.on(AuthEvent.LOGIN_SUCCESS, critical=True)
        async def audit_login(user, ip: str, **ctx):
            await audit_log.record(user, ip)  # Must not fail silently

        # Programmatic registration
        events.add_listener(AuthEvent.LOGOUT, my_logout_handler)

        # Emit event
        await events.emit(AuthEvent.LOGIN_SUCCESS, user=user, ip="1.2.3.4")
    """

    def __init__(self) -> None:
        """Initialize the event emitter."""
        self._listeners: dict[AuthEvent, list[ListenerConfig]] = {}

    def on(
        self,
        event: AuthEvent,
        critical: bool = False,
    ) -> Callable[[Callable[..., Awaitable[None]]], Callable[..., Awaitable[None]]]:
        """Decorator to register an event listener.

        Args:
            event: The event to listen for.
            critical: If True, errors in this listener will be re-raised,
                causing the authentication to fail.

        Returns:
            Decorator that registers the function as a listener.

        Example:
            @events.on(AuthEvent.LOGIN_FAILED)
            async def log_failed_attempt(identifier: str, ip: str, **ctx):
                print(f"Failed login: {identifier} from {ip}")

            @events.on(AuthEvent.LOGIN_SUCCESS, critical=True)
            async def audit_login(user, **ctx):
                await audit_log.record(user)  # Must succeed
        """

        def decorator(
            fn: Callable[..., Awaitable[None]],
        ) -> Callable[..., Awaitable[None]]:
            self.add_listener(event, fn, critical=critical)
            return fn

        return decorator

    def add_listener(
        self,
        event: AuthEvent,
        fn: Callable[..., Awaitable[None]],
        critical: bool = False,
    ) -> None:
        """Register a listener programmatically.

        Args:
            event: The event to listen for.
            fn: Async function to call when event is emitted.
            critical: If True, errors in this listener will be re-raised.

        Example:
            async def my_handler(user, **ctx):
                print(f"User logged in: {user.id}")

            events.add_listener(AuthEvent.LOGIN_SUCCESS, my_handler)

            # Critical listener
            events.add_listener(AuthEvent.LOGIN_SUCCESS, audit_handler, critical=True)
        """
        config = ListenerConfig(fn=fn, critical=critical)
        self._listeners.setdefault(event, []).append(config)

    def remove_listener(
        self,
        event: AuthEvent,
        fn: Callable[..., Awaitable[None]],
    ) -> bool:
        """Remove a listener.

        Args:
            event: The event the listener was registered for.
            fn: The listener function to remove.

        Returns:
            True if listener was found and removed, False otherwise.
        """
        if event not in self._listeners:
            return False

        for config in self._listeners[event]:
            if config.fn is fn:
                self._listeners[event].remove(config)
                return True
        return False

    def clear_listeners(self, event: AuthEvent | None = None) -> None:
        """Clear listeners.

        Args:
            event: If provided, clear only listeners for this event.
                If None, clear all listeners.
        """
        if event is None:
            self._listeners.clear()
        elif event in self._listeners:
            self._listeners[event].clear()

    async def emit(self, event: AuthEvent, **data: Any) -> None:
        """Emit an event to all registered listeners.

        Non-critical listener errors are logged but don't propagate.
        Critical listener errors are re-raised after logging.

        Args:
            event: The event to emit.
            **data: Event data passed to listeners as keyword arguments.

        Raises:
            Exception: If a critical listener fails.

        Example:
            await events.emit(
                AuthEvent.LOGIN_SUCCESS,
                user=user,
                ip="1.2.3.4",
                user_agent="Mozilla/5.0...",
            )
        """
        for config in self._listeners.get(event, []):
            try:
                await config.fn(**data)
            except Exception as e:
                logger.exception(f"Error in {event.name} listener {config.fn.__name__}: {e}")
                if config.critical:
                    raise

    def listener_count(self, event: AuthEvent) -> int:
        """Get the number of listeners for an event.

        Args:
            event: The event to check.

        Returns:
            Number of registered listeners.
        """
        return len(self._listeners.get(event, []))
