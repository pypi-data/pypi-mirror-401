"""Redis session storage backend."""

import json
import time
from typing import Any

from ..data import SessionData
from ..exceptions import SessionSerializationError, SessionStorageError


class RedisSessionStore:
    """Redis-based session storage.

    Uses redis-py with automatic connection pooling (lazy connection).
    Sessions are stored as JSON strings with Redis TTL for expiration.

    Suitable for production multi-server deployments.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        key_prefix: str = "zerojs:session:",
        socket_timeout: float = 5.0,
        socket_connect_timeout: float = 5.0,
        **redis_kwargs: Any,
    ) -> None:
        """Initialize Redis store.

        Connection is lazy - created on first use.

        Args:
            host: Redis server hostname.
            port: Redis server port.
            db: Redis database number.
            password: Redis password (optional).
            key_prefix: Prefix for all session keys.
            socket_timeout: Socket timeout in seconds.
            socket_connect_timeout: Connection timeout in seconds.
            **redis_kwargs: Additional kwargs for redis.Redis().
        """
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._key_prefix = key_prefix
        self._socket_timeout = socket_timeout
        self._socket_connect_timeout = socket_connect_timeout
        self._redis_kwargs = redis_kwargs
        self._client: Any = None

    def _get_client(self) -> Any:
        """Get or create Redis client with connection pooling."""
        if self._client is None:
            try:
                import redis
            except ImportError as e:
                raise SessionStorageError("redis package not installed. Install with: pip install redis") from e

            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                db=self._db,
                password=self._password,
                socket_timeout=self._socket_timeout,
                socket_connect_timeout=self._socket_connect_timeout,
                decode_responses=True,
                **self._redis_kwargs,
            )
        return self._client

    def _make_key(self, session_id: str) -> str:
        """Create Redis key from session ID."""
        return f"{self._key_prefix}{session_id}"

    def get(self, session_id: str) -> SessionData | None:
        """Retrieve session data by ID.

        Args:
            session_id: The unique session identifier.

        Returns:
            SessionData if found and not expired, None otherwise.
        """
        client = self._get_client()
        key = self._make_key(session_id)

        try:
            raw = client.get(key)
            if raw is None:
                return None

            data_dict = json.loads(raw)
            return SessionData.from_dict(data_dict)

        except json.JSONDecodeError:
            client.delete(key)
            return None
        except Exception as e:
            raise SessionStorageError(f"Redis get failed: {e}") from e

    def set(self, session_id: str, data: SessionData, ttl: int) -> None:
        """Store session data.

        Args:
            session_id: The unique session identifier.
            data: The session data to store.
            ttl: Time-to-live in seconds.
        """
        client = self._get_client()
        key = self._make_key(session_id)

        try:
            serialized = json.dumps(data.to_dict())
            client.setex(key, ttl, serialized)

        except (TypeError, ValueError) as e:
            raise SessionSerializationError(f"Failed to serialize: {e}") from e
        except Exception as e:
            raise SessionStorageError(f"Redis set failed: {e}") from e

    def delete(self, session_id: str) -> None:
        """Delete session data.

        Args:
            session_id: The unique session identifier.
        """
        client = self._get_client()
        key = self._make_key(session_id)

        try:
            client.delete(key)
        except Exception as e:
            raise SessionStorageError(f"Redis delete failed: {e}") from e

    def exists(self, session_id: str) -> bool:
        """Check if session exists and is not expired.

        Args:
            session_id: The unique session identifier.

        Returns:
            True if session exists and is valid, False otherwise.
        """
        client = self._get_client()
        key = self._make_key(session_id)

        try:
            return bool(client.exists(key))
        except Exception as e:
            raise SessionStorageError(f"Redis exists failed: {e}") from e

    def touch(self, session_id: str, ttl: int) -> bool:
        """Update session timestamp and refresh TTL.

        Uses GETEX (Redis 6.2+) for atomic get+expire, with fallback
        to GET+SETEX for older versions.

        Args:
            session_id: The unique session identifier.
            ttl: New TTL in seconds.

        Returns:
            True if session was touched, False if not found.
        """
        client = self._get_client()
        key = self._make_key(session_id)

        try:
            if hasattr(client, "getex"):
                raw = client.getex(key, ex=ttl)
                if raw is None:
                    return False
                data_dict = json.loads(raw)
                data_dict["accessed_at"] = time.time()
                client.setex(key, ttl, json.dumps(data_dict))
                return True

            raw = client.get(key)
            if raw is None:
                return False

            data_dict = json.loads(raw)
            data_dict["accessed_at"] = time.time()
            client.setex(key, ttl, json.dumps(data_dict))
            return True

        except json.JSONDecodeError:
            client.delete(key)
            return False
        except Exception as e:
            raise SessionStorageError(f"Redis touch failed: {e}") from e

    def clear(self) -> None:
        """Delete all sessions with this prefix.

        Warning: Uses SCAN which may be slow on large datasets.
        """
        client = self._get_client()
        pattern = f"{self._key_prefix}*"

        try:
            cursor = 0
            while True:
                cursor, keys = client.scan(cursor, match=pattern, count=100)
                if keys:
                    client.delete(*keys)
                if cursor == 0:
                    break
        except Exception as e:
            raise SessionStorageError(f"Redis clear failed: {e}") from e

    def _make_counter_key(self, key: str) -> str:
        """Create Redis key for a counter."""
        return f"{self._key_prefix}counter:{key}"

    def increment(self, key: str, amount: int = 1, ttl: int = 0) -> int:
        """Atomically increment a counter using Redis INCRBY.

        Args:
            key: The counter key.
            amount: Amount to increment by.
            ttl: Time-to-live in seconds. 0 = no expiration.

        Returns:
            The new counter value.
        """
        client = self._get_client()
        redis_key = self._make_counter_key(key)

        try:
            # Use pipeline for atomic INCRBY + EXPIRE
            pipe = client.pipeline()
            pipe.incrby(redis_key, amount)
            if ttl > 0:
                pipe.expire(redis_key, ttl)
            results = pipe.execute()
            return results[0]  # INCRBY result

        except Exception as e:
            raise SessionStorageError(f"Redis increment failed: {e}") from e

    def get_counter(self, key: str) -> int:
        """Get current counter value.

        Args:
            key: The counter key.

        Returns:
            Current value, or 0 if not exists.
        """
        client = self._get_client()
        redis_key = self._make_counter_key(key)

        try:
            value = client.get(redis_key)
            return int(value) if value else 0
        except Exception as e:
            raise SessionStorageError(f"Redis get_counter failed: {e}") from e
