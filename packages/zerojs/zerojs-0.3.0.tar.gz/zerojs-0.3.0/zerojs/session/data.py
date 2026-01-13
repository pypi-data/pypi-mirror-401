"""Session data structures."""

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionData:
    """Session data with timestamps for TTL management.

    Similar to CacheEntry but includes accessed_at for sliding expiration
    and arbitrary dict data storage.
    """

    data: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    accessed_at: float = field(default_factory=time.time)

    def touch(self) -> None:
        """Update accessed_at timestamp for sliding expiration."""
        self.accessed_at = time.time()

    def is_expired(self, ttl: int) -> bool:
        """Check if session has expired based on accessed_at (sliding expiration).

        Args:
            ttl: Time-to-live in seconds.

        Returns:
            True if session has expired, False otherwise.
        """
        return (time.time() - self.accessed_at) >= ttl

    def is_absolutely_expired(self, absolute_lifetime: int) -> bool:
        """Check if session exceeded absolute lifetime from creation.

        Unlike sliding expiration (is_expired), this checks against created_at
        and cannot be renewed by activity.

        Args:
            absolute_lifetime: Max seconds since created_at. 0 = disabled.

        Returns:
            True if session is too old, False otherwise.
        """
        if absolute_lifetime <= 0:
            return False
        return (time.time() - self.created_at) >= absolute_lifetime

    def should_rotate(self) -> bool:
        """Check and clear the rotation flag.

        Returns:
            True if session should rotate its ID, False otherwise.
        """
        return self.data.pop("_rotate", False)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for JSON storage.

        Returns:
            Dictionary representation of session data.
        """
        return {
            "data": self.data,
            "created_at": self.created_at,
            "accessed_at": self.accessed_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SessionData":
        """Deserialize from dictionary.

        Args:
            d: Dictionary with session data.

        Returns:
            SessionData instance.
        """
        return cls(
            data=d.get("data", {}),
            created_at=d.get("created_at", time.time()),
            accessed_at=d.get("accessed_at", time.time()),
        )
