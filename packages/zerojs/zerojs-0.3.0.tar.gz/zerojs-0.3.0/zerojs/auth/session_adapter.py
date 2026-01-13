"""Authentication session adapter.

Wraps the existing SessionStore to provide authentication-specific
operations like creating authenticated sessions, managing MFA tokens,
and rate limiting counters.
"""

import secrets
import time
from typing import Any

from zerojs.session.data import SessionData
from zerojs.session.storage import SessionStore


class AuthSessionAdapter:
    """Adapts existing SessionStore for authentication use.

    Provides a higher-level interface for authentication operations
    while using the existing session infrastructure.

    Example:
        from zerojs.session import MemorySessionStore
        from zerojs.auth import AuthSessionAdapter

        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)

        # Create authenticated session
        session_id = sessions.create(user_id=123)

        # Get user from session
        user_id = sessions.get_user_id(session_id)

        # Store MFA token
        sessions.set_raw("mfa:token123", {"user_id": 123}, ttl=300)

        # Rate limiting
        attempts = sessions.increment_raw("rate:user@example.com", ttl=300)
    """

    def __init__(
        self,
        store: SessionStore,
        default_ttl: int = 86400,
    ):
        """Initialize the session adapter.

        Args:
            store: The underlying session store.
            default_ttl: Default session TTL in seconds (default: 24 hours).
        """
        self._store = store
        self._default_ttl = default_ttl

    def create(
        self,
        user_id: Any,
        data: dict[str, Any] | None = None,
        ttl: int | None = None,
    ) -> str:
        """Create an authenticated session.

        Generates a secure session ID and stores user data.

        Args:
            user_id: The user's identifier.
            data: Additional data to store in the session.
            ttl: Session TTL in seconds (uses default_ttl if not specified).

        Returns:
            The generated session ID.
        """
        session_id = secrets.token_urlsafe(32)
        session_data = SessionData(
            data={
                **(data or {}),
                # Reserved keys last - always win over user data
                "user_id": user_id,
                "authenticated_at": time.time(),
            }
        )
        self._store.set(session_id, session_data, ttl or self._default_ttl)
        return session_id

    def get_user_id(self, session_id: str) -> Any | None:
        """Get user_id from a session.

        Args:
            session_id: The session ID.

        Returns:
            The user_id if session exists, None otherwise.
        """
        if data := self._store.get(session_id):
            return data.data.get("user_id")
        return None

    def get_data(self, session_id: str) -> dict[str, Any] | None:
        """Get all data from a session.

        Args:
            session_id: The session ID.

        Returns:
            Session data dictionary if session exists, None otherwise.
        """
        if data := self._store.get(session_id):
            return data.data
        return None

    def destroy(self, session_id: str) -> None:
        """Destroy a session.

        Args:
            session_id: The session ID to destroy.
        """
        self._store.delete(session_id)

    def refresh(self, session_id: str, ttl: int | None = None) -> bool:
        """Renew session TTL.

        Args:
            session_id: The session ID.
            ttl: New TTL in seconds (uses default_ttl if not specified).

        Returns:
            True if session was refreshed, False if not found.
        """
        return self._store.touch(session_id, ttl or self._default_ttl)

    # --- Raw operations for arbitrary keys (MFA tokens, etc.) ---

    def set_raw(self, key: str, data: dict[str, Any], ttl: int) -> None:
        """Store data with an arbitrary key.

        Use this for temporary tokens like MFA challenges.

        Args:
            key: Storage key.
            data: Data to store.
            ttl: TTL in seconds.

        Example:
            sessions.set_raw("mfa:abc123", {"user_id": 1, "method": "totp"}, 300)
        """
        self._store.set(key, SessionData(data=data), ttl)

    def get_raw(self, key: str) -> dict[str, Any] | None:
        """Get data by arbitrary key.

        For counters created with increment_raw(), use get_counter_raw() instead.

        Args:
            key: Storage key.

        Returns:
            Stored data dictionary if key exists, None otherwise.
        """
        if session_data := self._store.get(key):
            return session_data.data
        return None

    def delete_raw(self, key: str) -> None:
        """Delete data by arbitrary key.

        Args:
            key: Storage key to delete.
        """
        self._store.delete(key)

    def increment_raw(self, key: str, amount: int = 1, ttl: int = 0) -> int:
        """Atomically increment a counter.

        Uses Redis INCR for atomic distributed counting.
        For non-Redis backends, the operation is still atomic for
        single-worker development but not for distributed systems.

        Args:
            key: Counter key.
            amount: Amount to increment (default 1).
            ttl: TTL in seconds (0 = no expiration).

        Returns:
            New counter value after increment.

        Example:
            # Rate limiting
            attempts = sessions.increment_raw("rate:user@example.com", ttl=300)
            if attempts > 5:
                raise TooManyAttempts()
        """
        return self._store.increment(key, amount, ttl)

    def get_counter_raw(self, key: str) -> int:
        """Get counter value created with increment_raw().

        Returns 0 if counter doesn't exist.
        For arbitrary data, use get_raw() instead.

        Args:
            key: Counter key.

        Returns:
            Counter value, or 0 if not found.
        """
        return self._store.get_counter(key)
