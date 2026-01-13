"""Tests for MemorySessionStore."""

import threading

import time_machine

from zerojs.session import MemorySessionStore, SessionData


class TestMemorySessionStore:
    """Tests for MemorySessionStore."""

    def test_set_and_get(self) -> None:
        """set() and get() work correctly."""
        store = MemorySessionStore()
        data = SessionData(data={"user": 1})

        store.set("session1", data, ttl=3600)
        result = store.get("session1")

        assert result is not None
        assert result.data == {"user": 1}

    def test_get_nonexistent_returns_none(self) -> None:
        """get() returns None for nonexistent session."""
        store = MemorySessionStore()
        assert store.get("nonexistent") is None

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_get_expired_returns_none(self) -> None:
        """get() returns None for expired session."""
        store = MemorySessionStore()
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            assert store.get("session1") is None

    def test_delete_removes_session(self) -> None:
        """delete() removes session."""
        store = MemorySessionStore()
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        store.delete("session1")
        assert store.get("session1") is None

    def test_delete_nonexistent_does_not_raise(self) -> None:
        """delete() does not raise for nonexistent session."""
        store = MemorySessionStore()
        store.delete("nonexistent")

    def test_exists_returns_true_for_valid_session(self) -> None:
        """exists() returns True for valid session."""
        store = MemorySessionStore()
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        assert store.exists("session1") is True

    def test_exists_returns_false_for_nonexistent(self) -> None:
        """exists() returns False for nonexistent session."""
        store = MemorySessionStore()
        assert store.exists("nonexistent") is False

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_touch_updates_accessed_at(self) -> None:
        """touch() updates accessed_at timestamp."""
        store = MemorySessionStore()
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)
        original_accessed_at = data.accessed_at

        with time_machine.travel("2024-01-01 12:05:00", tick=False):
            result = store.touch("session1", ttl=3600)
            assert result is True
            updated = store.get("session1")
            assert updated is not None
            assert updated.accessed_at > original_accessed_at

    def test_touch_returns_false_for_nonexistent(self) -> None:
        """touch() returns False for nonexistent session."""
        store = MemorySessionStore()
        assert store.touch("nonexistent", ttl=3600) is False

    def test_clear_removes_all_sessions(self) -> None:
        """clear() removes all sessions."""
        store = MemorySessionStore()
        store.set("session1", SessionData(data={"a": 1}), ttl=3600)
        store.set("session2", SessionData(data={"b": 2}), ttl=3600)

        store.clear()

        assert store.get("session1") is None
        assert store.get("session2") is None

    def test_thread_safety(self) -> None:
        """Store is thread-safe for concurrent access."""
        store = MemorySessionStore()
        errors: list[Exception] = []

        def worker(thread_id: int) -> None:
            try:
                for i in range(100):
                    session_id = f"session_{thread_id}_{i}"
                    store.set(session_id, SessionData(data={"i": i}), ttl=3600)
                    store.get(session_id)
                    store.touch(session_id, ttl=3600)
                    store.delete(session_id)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_lazy_cleanup_removes_expired(self) -> None:
        """Lazy cleanup removes expired sessions."""
        store = MemorySessionStore(cleanup_interval=0)
        store.set("session1", SessionData(data={"a": 1}), ttl=60)
        store.set("session2", SessionData(data={"b": 2}), ttl=3600)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            store.get("session2")
            assert "session1" not in store._sessions
            assert "session2" in store._sessions

    def test_increment_creates_new_counter(self) -> None:
        """increment() creates counter if not exists."""
        store = MemorySessionStore()
        result = store.increment("counter1")
        assert result == 1

    def test_increment_increments_existing(self) -> None:
        """increment() increments existing counter."""
        store = MemorySessionStore()
        store.increment("counter1")
        store.increment("counter1")
        result = store.increment("counter1")
        assert result == 3

    def test_increment_with_amount(self) -> None:
        """increment() respects amount parameter."""
        store = MemorySessionStore()
        result = store.increment("counter1", amount=5)
        assert result == 5
        result = store.increment("counter1", amount=3)
        assert result == 8

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_increment_with_ttl(self) -> None:
        """increment() respects TTL."""
        store = MemorySessionStore()
        store.increment("counter1", ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            # Counter expired, should start fresh
            result = store.increment("counter1", ttl=60)
            assert result == 1

    def test_get_counter_returns_value(self) -> None:
        """get_counter() returns current value."""
        store = MemorySessionStore()
        store.increment("counter1", amount=5)
        assert store.get_counter("counter1") == 5

    def test_get_counter_returns_zero_if_not_exists(self) -> None:
        """get_counter() returns 0 for nonexistent counter."""
        store = MemorySessionStore()
        assert store.get_counter("nonexistent") == 0

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_get_counter_returns_zero_if_expired(self) -> None:
        """get_counter() returns 0 for expired counter."""
        store = MemorySessionStore()
        store.increment("counter1", ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            assert store.get_counter("counter1") == 0

    def test_increment_thread_safety(self) -> None:
        """increment() is thread-safe."""
        store = MemorySessionStore()
        errors: list[Exception] = []

        def worker() -> None:
            try:
                for _ in range(100):
                    store.increment("counter1")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert store.get_counter("counter1") == 1000
