"""Session storage protocol and factory."""

from typing import Protocol
from urllib.parse import urlparse

from .data import SessionData


class SessionStore(Protocol):
    """Protocol defining session storage interface.

    All methods are synchronous. Async backends should use
    connection pooling with synchronous wrapper calls.
    """

    def get(self, session_id: str) -> SessionData | None:
        """Retrieve session data by ID.

        Args:
            session_id: The unique session identifier.

        Returns:
            SessionData if found and not expired, None otherwise.
        """
        ...

    def set(self, session_id: str, data: SessionData, ttl: int) -> None:
        """Store session data.

        Args:
            session_id: The unique session identifier.
            data: The session data to store.
            ttl: Time-to-live in seconds.
        """
        ...

    def delete(self, session_id: str) -> None:
        """Delete session data.

        Args:
            session_id: The unique session identifier.
        """
        ...

    def exists(self, session_id: str) -> bool:
        """Check if session exists and is not expired.

        Args:
            session_id: The unique session identifier.

        Returns:
            True if session exists and is valid, False otherwise.
        """
        ...

    def touch(self, session_id: str, ttl: int) -> bool:
        """Update session accessed_at timestamp (sliding expiration).

        Args:
            session_id: The unique session identifier.
            ttl: New TTL in seconds (for backends with native expiration).

        Returns:
            True if session was touched, False if not found.
        """
        ...

    def clear(self) -> None:
        """Clear all sessions. Use with caution."""
        ...

    def increment(self, key: str, amount: int = 1, ttl: int = 0) -> int:
        """Atomically increment a counter.

        Used for rate limiting and other atomic counter operations.
        Creates the counter with value `amount` if it doesn't exist.

        Args:
            key: The counter key (not a session ID).
            amount: Amount to increment by (default: 1).
            ttl: Time-to-live in seconds. 0 = no expiration.

        Returns:
            The new counter value after incrementing.
        """
        ...

    def get_counter(self, key: str) -> int:
        """Get current counter value.

        For counters created with increment(). For session data, use get().

        Args:
            key: The counter key.

        Returns:
            Current counter value, or 0 if counter doesn't exist.
        """
        ...


def storage_from_uri(uri: str) -> SessionStore:
    """Create a session store from a URI string.

    Follows the slowapi pattern for storage configuration.

    Args:
        uri: Storage URI in format "scheme://..."
            - "memory://" - In-memory storage (default)
            - "file:///path/to/sessions" - File-based storage
            - "redis://host:port/db" - Redis storage
            - "redis://:password@host:port/db" - Redis with auth

    Returns:
        SessionStore implementation.

    Raises:
        ValueError: If URI scheme is not supported.
    """
    parsed = urlparse(uri)
    scheme = parsed.scheme

    if scheme == "memory":
        from .backends.memory import MemorySessionStore

        return MemorySessionStore()

    if scheme == "file":
        from .backends.file import FileSessionStore

        # Use explicit path if provided, otherwise let FileSessionStore
        # create a secure temporary directory
        path = parsed.path if parsed.path else None
        return FileSessionStore(base_path=path)

    if scheme == "redis":
        from .backends.redis import RedisSessionStore

        host = parsed.hostname or "localhost"
        port = parsed.port or 6379
        db = int(parsed.path.lstrip("/") or "0") if parsed.path else 0
        password = parsed.password
        return RedisSessionStore(
            host=host,
            port=port,
            db=db,
            password=password,
        )

    raise ValueError(f"Unsupported session storage scheme: {scheme}")
