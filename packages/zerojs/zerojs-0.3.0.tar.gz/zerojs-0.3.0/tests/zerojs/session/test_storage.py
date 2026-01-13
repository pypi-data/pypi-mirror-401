"""Tests for storage_from_uri factory function."""

import pytest

from zerojs.session import (
    FileSessionStore,
    MemorySessionStore,
    RedisSessionStore,
    storage_from_uri,
)


class TestStorageFromUri:
    """Tests for storage_from_uri factory."""

    def test_memory_scheme(self) -> None:
        """memory:// creates MemorySessionStore."""
        store = storage_from_uri("memory://")
        assert isinstance(store, MemorySessionStore)

    def test_file_scheme_with_path(self, tmp_path) -> None:
        """file:// creates FileSessionStore with path."""
        store = storage_from_uri(f"file://{tmp_path}/sessions")
        assert isinstance(store, FileSessionStore)
        assert store._base_path == tmp_path / "sessions"

    def test_file_scheme_default_path(self) -> None:
        """file:// without path creates secure temp directory."""
        store = storage_from_uri("file://")
        assert isinstance(store, FileSessionStore)
        # Should create a unique temp directory with secure prefix
        assert "zerojs_sessions_" in str(store._base_path)
        assert store._base_path.exists()

    def test_redis_scheme_default(self) -> None:
        """redis:// creates RedisSessionStore with defaults."""
        store = storage_from_uri("redis://")
        assert isinstance(store, RedisSessionStore)
        assert store._host == "localhost"
        assert store._port == 6379
        assert store._db == 0
        assert store._password is None

    def test_redis_scheme_with_host_port(self) -> None:
        """redis://host:port parses correctly."""
        store = storage_from_uri("redis://myredis:6380")
        assert isinstance(store, RedisSessionStore)
        assert store._host == "myredis"
        assert store._port == 6380

    def test_redis_scheme_with_db(self) -> None:
        """redis://host:port/db parses correctly."""
        store = storage_from_uri("redis://localhost:6379/2")
        assert isinstance(store, RedisSessionStore)
        assert store._db == 2

    def test_redis_scheme_with_password(self) -> None:
        """redis://:password@host parses correctly."""
        store = storage_from_uri("redis://:secret@localhost:6379/0")
        assert isinstance(store, RedisSessionStore)
        assert store._password == "secret"

    def test_unsupported_scheme_raises_error(self) -> None:
        """Unsupported scheme raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported session storage scheme"):
            storage_from_uri("postgresql://localhost/db")

    def test_invalid_uri_raises_error(self) -> None:
        """Invalid URI raises ValueError."""
        with pytest.raises(ValueError):
            storage_from_uri("not-a-valid-uri")
