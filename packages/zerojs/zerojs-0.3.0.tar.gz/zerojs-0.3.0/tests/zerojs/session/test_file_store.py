"""Tests for FileSessionStore."""

import os
import stat
from pathlib import Path

import time_machine

from zerojs.session import FileSessionStore, SessionData


class TestFileSessionStore:
    """Tests for FileSessionStore."""

    def test_set_and_get(self, tmp_path: Path) -> None:
        """set() and get() work correctly."""
        store = FileSessionStore(base_path=tmp_path)
        data = SessionData(data={"user": 1})

        store.set("session1", data, ttl=3600)
        result = store.get("session1")

        assert result is not None
        assert result.data == {"user": 1}

    def test_get_nonexistent_returns_none(self, tmp_path: Path) -> None:
        """get() returns None for nonexistent session."""
        store = FileSessionStore(base_path=tmp_path)
        assert store.get("nonexistent") is None

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_get_expired_returns_none(self, tmp_path: Path) -> None:
        """get() returns None for expired session."""
        store = FileSessionStore(base_path=tmp_path)
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            assert store.get("session1") is None

    def test_delete_removes_session(self, tmp_path: Path) -> None:
        """delete() removes session."""
        store = FileSessionStore(base_path=tmp_path)
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        store.delete("session1")
        assert store.get("session1") is None

    def test_exists_returns_true_for_valid_session(self, tmp_path: Path) -> None:
        """exists() returns True for valid session."""
        store = FileSessionStore(base_path=tmp_path)
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)

        assert store.exists("session1") is True

    def test_exists_returns_false_for_nonexistent(self, tmp_path: Path) -> None:
        """exists() returns False for nonexistent session."""
        store = FileSessionStore(base_path=tmp_path)
        assert store.exists("nonexistent") is False

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_touch_updates_accessed_at(self, tmp_path: Path) -> None:
        """touch() updates accessed_at timestamp."""
        store = FileSessionStore(base_path=tmp_path)
        data = SessionData(data={"user": 1})
        store.set("session1", data, ttl=3600)
        original_accessed_at = data.accessed_at

        with time_machine.travel("2024-01-01 12:05:00", tick=False):
            result = store.touch("session1", ttl=3600)
            assert result is True
            updated = store.get("session1")
            assert updated is not None
            assert updated.accessed_at > original_accessed_at

    def test_touch_returns_false_for_nonexistent(self, tmp_path: Path) -> None:
        """touch() returns False for nonexistent session."""
        store = FileSessionStore(base_path=tmp_path)
        assert store.touch("nonexistent", ttl=3600) is False

    def test_clear_removes_all_sessions(self, tmp_path: Path) -> None:
        """clear() removes all sessions."""
        store = FileSessionStore(base_path=tmp_path)
        store.set("session1", SessionData(data={"a": 1}), ttl=3600)
        store.set("session2", SessionData(data={"b": 2}), ttl=3600)

        store.clear()

        assert store.get("session1") is None
        assert store.get("session2") is None

    def test_session_file_has_correct_permissions(self, tmp_path: Path) -> None:
        """Session files have 0o600 permissions."""
        store = FileSessionStore(base_path=tmp_path, file_mode=0o600)
        store.set("session1", SessionData(data={"user": 1}), ttl=3600)

        session_files = list(tmp_path.glob("*.json"))
        assert len(session_files) == 1

        file_stat = os.stat(session_files[0])
        permissions = stat.S_IMODE(file_stat.st_mode)
        assert permissions == 0o600

    def test_base_directory_has_correct_permissions(self, tmp_path: Path) -> None:
        """Base directory has 0o700 permissions."""
        session_dir = tmp_path / "sessions"
        FileSessionStore(base_path=session_dir)

        dir_stat = os.stat(session_dir)
        permissions = stat.S_IMODE(dir_stat.st_mode)
        assert permissions == 0o700

    def test_session_id_is_hashed(self, tmp_path: Path) -> None:
        """Session ID is hashed to prevent path traversal."""
        store = FileSessionStore(base_path=tmp_path)
        store.set("session1", SessionData(data={"user": 1}), ttl=3600)

        session_files = list(tmp_path.glob("*.json"))
        assert len(session_files) == 1
        assert "session1" not in session_files[0].name
        assert len(session_files[0].stem) == 64

    def test_malicious_session_id_is_hashed(self, tmp_path: Path) -> None:
        """Malicious session IDs are safely hashed."""
        store = FileSessionStore(base_path=tmp_path)
        malicious_ids = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "/etc/passwd",
            "C:\\Windows\\System32",
            "session\x00.json",
        ]

        for session_id in malicious_ids:
            store.set(session_id, SessionData(data={"test": True}), ttl=3600)
            result = store.get(session_id)
            assert result is not None
            assert result.data == {"test": True}

        session_files = list(tmp_path.glob("*.json"))
        assert len(session_files) == len(malicious_ids)
        for f in session_files:
            assert tmp_path in f.parents or f.parent == tmp_path

    def test_corrupted_file_is_deleted(self, tmp_path: Path) -> None:
        """Corrupted session files are deleted on read."""
        store = FileSessionStore(base_path=tmp_path)
        store.set("session1", SessionData(data={"user": 1}), ttl=3600)

        session_files = list(tmp_path.glob("*.json"))
        session_files[0].write_text("invalid json {{{")

        result = store.get("session1")
        assert result is None
        assert not session_files[0].exists()

    def test_atomic_write(self, tmp_path: Path) -> None:
        """Writes are atomic (use temp file + rename)."""
        store = FileSessionStore(base_path=tmp_path)
        store.set("session1", SessionData(data={"user": 1}), ttl=3600)

        temp_files = list(tmp_path.glob("*.tmp"))
        assert len(temp_files) == 0

        session_files = list(tmp_path.glob("*.json"))
        assert len(session_files) == 1

    def test_increment_creates_new_counter(self, tmp_path: Path) -> None:
        """increment() creates counter if not exists."""
        store = FileSessionStore(base_path=tmp_path)
        result = store.increment("counter1")
        assert result == 1

    def test_increment_increments_existing(self, tmp_path: Path) -> None:
        """increment() increments existing counter."""
        store = FileSessionStore(base_path=tmp_path)
        store.increment("counter1")
        store.increment("counter1")
        result = store.increment("counter1")
        assert result == 3

    def test_increment_with_amount(self, tmp_path: Path) -> None:
        """increment() respects amount parameter."""
        store = FileSessionStore(base_path=tmp_path)
        result = store.increment("counter1", amount=5)
        assert result == 5
        result = store.increment("counter1", amount=3)
        assert result == 8

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_increment_with_ttl(self, tmp_path: Path) -> None:
        """increment() respects TTL."""
        store = FileSessionStore(base_path=tmp_path)
        store.increment("counter1", ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            # Counter expired, should start fresh
            result = store.increment("counter1", ttl=60)
            assert result == 1

    def test_get_counter_returns_value(self, tmp_path: Path) -> None:
        """get_counter() returns current value."""
        store = FileSessionStore(base_path=tmp_path)
        store.increment("counter1", amount=5)
        assert store.get_counter("counter1") == 5

    def test_get_counter_returns_zero_if_not_exists(self, tmp_path: Path) -> None:
        """get_counter() returns 0 for nonexistent counter."""
        store = FileSessionStore(base_path=tmp_path)
        assert store.get_counter("nonexistent") == 0

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_get_counter_returns_zero_if_expired(self, tmp_path: Path) -> None:
        """get_counter() returns 0 for expired counter."""
        store = FileSessionStore(base_path=tmp_path)
        store.increment("counter1", ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            assert store.get_counter("counter1") == 0

    def test_counter_file_uses_different_extension(self, tmp_path: Path) -> None:
        """Counter files use .counter extension."""
        store = FileSessionStore(base_path=tmp_path)
        store.increment("counter1")

        counter_files = list(tmp_path.glob("*.counter"))
        json_files = list(tmp_path.glob("*.json"))
        assert len(counter_files) == 1
        assert len(json_files) == 0
