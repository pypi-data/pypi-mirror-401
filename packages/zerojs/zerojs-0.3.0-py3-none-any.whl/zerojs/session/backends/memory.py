"""In-memory session storage backend."""

import threading
import time

from ..data import SessionData


class MemorySessionStore:
    """In-memory session storage using dict.

    Suitable for development and single-process deployments.
    Sessions are lost on restart.

    Implements lazy cleanup of expired sessions on access,
    similar to HTMLCache TTL strategy.
    """

    def __init__(self, cleanup_interval: int = 300) -> None:
        """Initialize memory store.

        Args:
            cleanup_interval: Seconds between automatic cleanup runs.
        """
        self._sessions: dict[str, tuple[SessionData, int]] = {}
        self._counters: dict[str, tuple[int, float]] = {}  # value, expires_at
        self._lock = threading.RLock()
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()

    def get(self, session_id: str) -> SessionData | None:
        """Retrieve session data by ID.

        Args:
            session_id: The unique session identifier.

        Returns:
            SessionData if found and not expired, None otherwise.
        """
        self._maybe_cleanup()
        with self._lock:
            entry = self._sessions.get(session_id)
            if entry is None:
                return None
            session_data, ttl = entry
            if session_data.is_expired(ttl):
                del self._sessions[session_id]
                return None
            return session_data

    def set(self, session_id: str, data: SessionData, ttl: int) -> None:
        """Store session data.

        Args:
            session_id: The unique session identifier.
            data: The session data to store.
            ttl: Time-to-live in seconds.
        """
        with self._lock:
            self._sessions[session_id] = (data, ttl)

    def delete(self, session_id: str) -> None:
        """Delete session data or counter.

        Args:
            session_id: The unique session identifier or counter key.
        """
        with self._lock:
            self._sessions.pop(session_id, None)
            self._counters.pop(session_id, None)

    def exists(self, session_id: str) -> bool:
        """Check if session exists and is not expired.

        Args:
            session_id: The unique session identifier.

        Returns:
            True if session exists and is valid, False otherwise.
        """
        return self.get(session_id) is not None

    def touch(self, session_id: str, ttl: int) -> bool:
        """Update session accessed_at timestamp (sliding expiration).

        Args:
            session_id: The unique session identifier.
            ttl: New TTL in seconds.

        Returns:
            True if session was touched, False if not found.
        """
        with self._lock:
            entry = self._sessions.get(session_id)
            if entry is None:
                return False
            session_data, _ = entry
            if session_data.is_expired(ttl):
                del self._sessions[session_id]
                return False
            session_data.touch()
            self._sessions[session_id] = (session_data, ttl)
            return True

    def clear(self) -> None:
        """Clear all sessions."""
        with self._lock:
            self._sessions.clear()

    def _maybe_cleanup(self) -> None:
        """Perform lazy cleanup of expired sessions."""
        now = time.time()
        if (now - self._last_cleanup) < self._cleanup_interval:
            return

        with self._lock:
            self._last_cleanup = now
            expired = [sid for sid, (data, ttl) in self._sessions.items() if data.is_expired(ttl)]
            for sid in expired:
                del self._sessions[sid]

            # Clean up expired counters
            expired_counters = [
                key for key, (_, expires_at) in self._counters.items() if expires_at > 0 and now >= expires_at
            ]
            for key in expired_counters:
                del self._counters[key]

    def increment(self, key: str, amount: int = 1, ttl: int = 0) -> int:
        """Atomically increment a counter.

        Args:
            key: The counter key.
            amount: Amount to increment by.
            ttl: Time-to-live in seconds. 0 = no expiration.

        Returns:
            The new counter value.
        """
        now = time.time()
        expires_at = now + ttl if ttl > 0 else 0

        with self._lock:
            if key in self._counters:
                current_value, current_expires = self._counters[key]
                # Check if expired
                if current_expires > 0 and now >= current_expires:
                    # Expired, start fresh
                    new_value = amount
                else:
                    new_value = current_value + amount
                    # Keep original expiration unless new ttl is set
                    if ttl == 0:
                        expires_at = current_expires
            else:
                new_value = amount

            self._counters[key] = (new_value, expires_at)
            return new_value

    def get_counter(self, key: str) -> int:
        """Get current counter value.

        Args:
            key: The counter key.

        Returns:
            Current value, or 0 if not exists or expired.
        """
        now = time.time()
        with self._lock:
            if key not in self._counters:
                return 0
            value, expires_at = self._counters[key]
            if expires_at > 0 and now >= expires_at:
                del self._counters[key]
                return 0
            return value
