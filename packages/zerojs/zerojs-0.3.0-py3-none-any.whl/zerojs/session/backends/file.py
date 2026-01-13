"""File-based session storage backend."""

import fcntl
import hashlib
import json
import os
import random
import tempfile
import time
from pathlib import Path

from ...security import is_safe_path
from ..data import SessionData
from ..exceptions import SessionSerializationError, SessionStorageError


class FileSessionStore:
    """File-based session storage.

    Each session is stored as a JSON file. Uses path traversal
    protection from zerojs.security.

    Suitable for multi-process deployments without Redis.

    Security note: If no base_path is provided, a secure temporary
    directory is created using tempfile.mkdtemp(). For production,
    always specify an explicit path outside of /tmp.
    """

    def __init__(
        self,
        base_path: str | Path | None = None,
        file_mode: int = 0o600,
        cleanup_probability: float = 0.01,
    ) -> None:
        """Initialize file store.

        Args:
            base_path: Directory to store session files. If None, creates
                a secure temporary directory. For production, specify an
                explicit path with restricted permissions.
            file_mode: Permission mode for session files (default: 0o600).
            cleanup_probability: Probability of cleanup on each access (0-1).
        """
        if base_path is None:
            # Create a secure temporary directory (not shared /tmp)
            base_path = tempfile.mkdtemp(prefix="zerojs_sessions_")
        self._base_path = Path(base_path)
        self._file_mode = file_mode
        self._cleanup_probability = cleanup_probability

        self._base_path.mkdir(parents=True, exist_ok=True)
        os.chmod(self._base_path, 0o700)

    def _session_filename(self, session_id: str) -> str:
        """Generate safe filename from session ID using SHA256 hash.

        Hashing prevents path traversal via session ID manipulation
        and ensures valid filesystem names.
        """
        hash_digest = hashlib.sha256(session_id.encode()).hexdigest()
        return f"{hash_digest}.json"

    def _session_path(self, session_id: str) -> Path:
        """Get full path to session file."""
        filename = self._session_filename(session_id)
        return self._base_path / filename

    def _validate_path(self, session_id: str) -> Path:
        """Validate session path is safe and return it.

        Uses is_safe_path from zerojs.security to prevent traversal.
        """
        filename = self._session_filename(session_id)
        if not is_safe_path(self._base_path, filename):
            raise SessionStorageError(f"Invalid session path: {session_id}")
        return self._base_path / filename

    def get(self, session_id: str) -> SessionData | None:
        """Retrieve session data by ID.

        Args:
            session_id: The unique session identifier.

        Returns:
            SessionData if found and not expired, None otherwise.
        """
        self._maybe_cleanup()
        path = self._validate_path(session_id)

        if not path.exists():
            return None

        try:
            with open(path) as f:
                raw = json.load(f)
            session_data = SessionData.from_dict(raw)

            ttl = raw.get("_ttl", 0)
            if session_data.is_expired(ttl):
                path.unlink(missing_ok=True)
                return None

            return session_data

        except (json.JSONDecodeError, KeyError, TypeError):
            path.unlink(missing_ok=True)
            return None
        except OSError as e:
            raise SessionStorageError(f"Failed to read session: {e}") from e

    def set(self, session_id: str, data: SessionData, ttl: int) -> None:
        """Store session data.

        Args:
            session_id: The unique session identifier.
            data: The session data to store.
            ttl: Time-to-live in seconds.
        """
        path = self._validate_path(session_id)

        try:
            serialized = data.to_dict()
            serialized["_ttl"] = ttl

            temp_path = path.with_suffix(".tmp")

            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            flags |= getattr(os, "O_CLOEXEC", 0)

            fd = os.open(temp_path, flags, self._file_mode)
            try:
                with os.fdopen(fd, "w") as f:
                    json.dump(serialized, f)
            except Exception:
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise

            temp_path.rename(path)

        except (TypeError, ValueError) as e:
            raise SessionSerializationError(f"Failed to serialize session: {e}") from e
        except OSError as e:
            raise SessionStorageError(f"Failed to write session: {e}") from e

    def delete(self, session_id: str) -> None:
        """Delete session data or counter.

        Args:
            session_id: The unique session identifier or counter key.
        """
        path = self._validate_path(session_id)
        path.unlink(missing_ok=True)
        # Also delete counter file if it exists
        counter_path = self._counter_path(session_id)
        counter_path.unlink(missing_ok=True)

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
        path = self._validate_path(session_id)

        if not path.exists():
            return False

        try:
            with open(path) as f:
                raw = json.load(f)

            session_data = SessionData.from_dict(raw)
            old_ttl = raw.get("_ttl", ttl)

            if session_data.is_expired(old_ttl):
                path.unlink(missing_ok=True)
                return False

            session_data.touch()
            self.set(session_id, session_data, ttl)
            return True

        except (json.JSONDecodeError, OSError):
            return False

    def clear(self) -> None:
        """Remove all session files."""
        for path in self._base_path.glob("*.json"):
            path.unlink(missing_ok=True)

    def _maybe_cleanup(self) -> None:
        """Probabilistically clean up expired sessions."""
        if random.random() > self._cleanup_probability:
            return

        now = time.time()
        for path in self._base_path.glob("*.json"):
            try:
                with open(path) as f:
                    raw = json.load(f)
                accessed_at = raw.get("accessed_at", 0)
                ttl = raw.get("_ttl", 0)
                if (now - accessed_at) >= ttl:
                    path.unlink(missing_ok=True)
            except (json.JSONDecodeError, OSError):
                path.unlink(missing_ok=True)

        # Clean up expired counters
        for path in self._base_path.glob("*.counter"):
            try:
                with open(path) as f:
                    raw = json.load(f)
                expires_at = raw.get("expires_at", 0)
                if expires_at > 0 and now >= expires_at:
                    path.unlink(missing_ok=True)
            except (json.JSONDecodeError, OSError):
                path.unlink(missing_ok=True)

    def _counter_path(self, key: str) -> Path:
        """Get path for a counter file."""
        hash_digest = hashlib.sha256(key.encode()).hexdigest()
        return self._base_path / f"{hash_digest}.counter"

    def increment(self, key: str, amount: int = 1, ttl: int = 0) -> int:
        """Atomically increment a counter using file locking.

        Args:
            key: The counter key.
            amount: Amount to increment by.
            ttl: Time-to-live in seconds. 0 = no expiration.

        Returns:
            The new counter value.
        """
        path = self._counter_path(key)
        now = time.time()
        expires_at = now + ttl if ttl > 0 else 0

        # Create file if it doesn't exist
        path.touch(exist_ok=True)

        try:
            with open(path, "r+") as f:
                # Acquire exclusive lock
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    content = f.read()
                    if content:
                        data = json.loads(content)
                        current_expires = data.get("expires_at", 0)
                        # Check expiration
                        if current_expires > 0 and now >= current_expires:
                            new_value = amount
                        else:
                            new_value = data.get("value", 0) + amount
                            # Keep original expiration if no new ttl
                            if ttl == 0:
                                expires_at = current_expires
                    else:
                        new_value = amount

                    # Write new value
                    f.seek(0)
                    f.truncate()
                    json.dump({"value": new_value, "expires_at": expires_at}, f)
                    return new_value
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        except (json.JSONDecodeError, OSError) as e:
            raise SessionStorageError(f"Failed to increment counter: {e}") from e

    def get_counter(self, key: str) -> int:
        """Get current counter value.

        Args:
            key: The counter key.

        Returns:
            Current value, or 0 if not exists or expired.
        """
        path = self._counter_path(key)

        if not path.exists():
            return 0

        try:
            with open(path) as f:
                data = json.load(f)
            expires_at = data.get("expires_at", 0)
            if expires_at > 0 and time.time() >= expires_at:
                path.unlink(missing_ok=True)
                return 0
            return data.get("value", 0)
        except (json.JSONDecodeError, OSError):
            return 0
