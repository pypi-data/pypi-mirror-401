"""Tests for RedisSessionStore."""

from unittest.mock import patch

import pytest
import time_machine

from zerojs.session import RedisSessionStore, SessionData, SessionStorageError


class MockRedisPipeline:
    """Mock Redis pipeline for testing."""

    def __init__(self, redis: "MockRedis") -> None:
        self._redis = redis
        self._commands: list[tuple[str, tuple]] = []

    def incrby(self, key: str, amount: int) -> "MockRedisPipeline":
        self._commands.append(("incrby", (key, amount)))
        return self

    def expire(self, key: str, ttl: int) -> "MockRedisPipeline":
        self._commands.append(("expire", (key, ttl)))
        return self

    def execute(self) -> list:
        results = []
        for cmd, args in self._commands:
            if cmd == "incrby":
                key, amount = args
                results.append(self._redis.incrby(key, amount))
            elif cmd == "expire":
                key, ttl = args
                results.append(self._redis.expire(key, ttl))
        return results


class MockRedis:
    """Mock Redis client for testing."""

    def __init__(self) -> None:
        self._data: dict[str, tuple[str, int | None]] = {}
        self._counters: dict[str, int] = {}

    def get(self, key: str) -> str | None:
        # Check counters first
        if key in self._counters:
            return str(self._counters[key])
        entry = self._data.get(key)
        return entry[0] if entry else None

    def setex(self, key: str, ttl: int, value: str) -> None:
        self._data[key] = (value, ttl)

    def delete(self, *keys: str) -> int:
        count = 0
        for key in keys:
            if key in self._data:
                del self._data[key]
                count += 1
            if key in self._counters:
                del self._counters[key]
                count += 1
        return count

    def exists(self, key: str) -> int:
        return 1 if key in self._data or key in self._counters else 0

    def scan(self, cursor: int, match: str | None = None, count: int = 100) -> tuple[int, list[str]]:
        if match and match.endswith("*"):
            prefix = match[:-1]
            keys = [k for k in self._data.keys() if k.startswith(prefix)]
        else:
            keys = list(self._data.keys())
        return (0, keys)

    def incrby(self, key: str, amount: int) -> int:
        if key not in self._counters:
            self._counters[key] = 0
        self._counters[key] += amount
        return self._counters[key]

    def expire(self, key: str, ttl: int) -> bool:
        return key in self._counters or key in self._data

    def pipeline(self) -> MockRedisPipeline:
        return MockRedisPipeline(self)


class TestRedisSessionStore:
    """Tests for RedisSessionStore."""

    @pytest.fixture
    def mock_redis(self) -> MockRedis:
        """Create mock Redis client."""
        return MockRedis()

    @pytest.fixture
    def store(self, mock_redis: MockRedis) -> RedisSessionStore:
        """Create store with mock Redis."""
        store = RedisSessionStore()
        store._client = mock_redis
        return store

    def test_set_and_get(self, store: RedisSessionStore) -> None:
        """set() and get() work correctly."""
        data = SessionData(data={"user": 1})

        store.set("session1", data, ttl=3600)
        result = store.get("session1")

        assert result is not None
        assert result.data == {"user": 1}

    def test_get_nonexistent_returns_none(self, store: RedisSessionStore) -> None:
        """get() returns None for nonexistent session."""
        assert store.get("nonexistent") is None

    def test_delete_removes_session(self, store: RedisSessionStore) -> None:
        """delete() removes session."""
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        store.delete("session1")
        assert store.get("session1") is None

    def test_exists_returns_true_for_valid_session(self, store: RedisSessionStore) -> None:
        """exists() returns True for valid session."""
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        assert store.exists("session1") is True

    def test_exists_returns_false_for_nonexistent(self, store: RedisSessionStore) -> None:
        """exists() returns False for nonexistent session."""
        assert store.exists("nonexistent") is False

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_touch_updates_accessed_at(self, store: RedisSessionStore) -> None:
        """touch() updates accessed_at timestamp."""
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)
        original_accessed_at = data.accessed_at

        with time_machine.travel("2024-01-01 12:05:00", tick=False):
            result = store.touch("session1", ttl=3600)
            assert result is True
            updated = store.get("session1")
            assert updated is not None
            assert updated.accessed_at > original_accessed_at

    def test_touch_returns_false_for_nonexistent(self, store: RedisSessionStore) -> None:
        """touch() returns False for nonexistent session."""
        assert store.touch("nonexistent", ttl=3600) is False

    def test_clear_removes_all_sessions(self, store: RedisSessionStore, mock_redis: MockRedis) -> None:
        """clear() removes all sessions with prefix."""
        store.set("session1", SessionData(data={"a": 1}), ttl=3600)
        store.set("session2", SessionData(data={"b": 2}), ttl=3600)

        mock_redis._data["other:key"] = ('{"other": true}', None)

        store.clear()

        assert store.get("session1") is None
        assert store.get("session2") is None
        assert "other:key" in mock_redis._data

    def test_key_prefix(self, store: RedisSessionStore, mock_redis: MockRedis) -> None:
        """Keys use configured prefix."""
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        assert "zerojs:session:session1" in mock_redis._data

    def test_custom_key_prefix(self, mock_redis: MockRedis) -> None:
        """Custom key prefix is used."""
        store = RedisSessionStore(key_prefix="myapp:sess:")
        store._client = mock_redis

        store.set("session1", SessionData(data={"user": 1}), ttl=3600)
        assert "myapp:sess:session1" in mock_redis._data

    def test_corrupted_data_is_deleted(self, store: RedisSessionStore, mock_redis: MockRedis) -> None:
        """Corrupted session data is deleted on read."""
        mock_redis._data["zerojs:session:corrupt"] = ("invalid json {{{", None)

        result = store.get("corrupt")
        assert result is None
        assert "zerojs:session:corrupt" not in mock_redis._data

    def test_missing_redis_package_raises_error(self) -> None:
        """Missing redis package raises informative error."""
        store = RedisSessionStore()
        store._client = None

        with patch.dict("sys.modules", {"redis": None}):
            with pytest.raises(SessionStorageError, match="redis package not installed"):
                store._get_client()

    def test_lazy_connection(self) -> None:
        """Redis connection is lazy."""
        store = RedisSessionStore()
        assert store._client is None

    def test_setex_called_with_ttl(self, store: RedisSessionStore, mock_redis: MockRedis) -> None:
        """SETEX is called with correct TTL."""
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=7200)

        _, ttl = mock_redis._data["zerojs:session:session1"]
        assert ttl == 7200

    def test_increment_creates_new_counter(self, store: RedisSessionStore) -> None:
        """increment() creates counter if not exists."""
        result = store.increment("counter1")
        assert result == 1

    def test_increment_increments_existing(self, store: RedisSessionStore) -> None:
        """increment() increments existing counter."""
        store.increment("counter1")
        store.increment("counter1")
        result = store.increment("counter1")
        assert result == 3

    def test_increment_with_amount(self, store: RedisSessionStore) -> None:
        """increment() respects amount parameter."""
        result = store.increment("counter1", amount=5)
        assert result == 5
        result = store.increment("counter1", amount=3)
        assert result == 8

    def test_get_counter_returns_value(self, store: RedisSessionStore) -> None:
        """get_counter() returns current value."""
        store.increment("counter1", amount=5)
        assert store.get_counter("counter1") == 5

    def test_get_counter_returns_zero_if_not_exists(self, store: RedisSessionStore) -> None:
        """get_counter() returns 0 for nonexistent counter."""
        assert store.get_counter("nonexistent") == 0

    def test_counter_uses_prefix(self, store: RedisSessionStore, mock_redis: MockRedis) -> None:
        """Counter keys use counter: prefix."""
        store.increment("counter1")
        assert "zerojs:session:counter:counter1" in mock_redis._counters
