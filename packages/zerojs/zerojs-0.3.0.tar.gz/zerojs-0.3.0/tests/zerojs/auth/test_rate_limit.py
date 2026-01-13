"""Tests for LoginRateLimiter module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

from zerojs.auth import LoginRateLimiter, RateLimitConfig
from zerojs.auth.session_adapter import AuthSessionAdapter
from zerojs.session import MemorySessionStore


class MockRequest:
    """Mock Starlette request for testing."""

    def __init__(
        self,
        client_host: str = "192.168.1.1",
        forwarded_for: str | None = None,
    ):
        self.client = MagicMock()
        self.client.host = client_host
        self.headers: dict[str, str] = {}
        if forwarded_for:
            self.headers["x-forwarded-for"] = forwarded_for


# --- RateLimitConfig Tests ---


class TestRateLimitConfig:
    """Tests for RateLimitConfig dataclass."""

    def test_default_values(self) -> None:
        """RateLimitConfig has sensible defaults."""
        config = RateLimitConfig()

        assert config.ip_limit == "10/minute"
        assert config.identifier_limit == "5/minute"
        assert config.combined_limit == "3/minute"
        assert config.ip_key_prefix == "login:ip"
        assert config.identifier_key_prefix == "login:id"
        assert config.combined_key_prefix == "login:combined"

    def test_custom_values(self) -> None:
        """RateLimitConfig accepts custom values."""
        config = RateLimitConfig(
            ip_limit="20/minute",
            identifier_limit="10/minute",
            combined_limit="5/minute",
            ip_key_prefix="auth:ip",
        )

        assert config.ip_limit == "20/minute"
        assert config.identifier_limit == "10/minute"
        assert config.combined_limit == "5/minute"
        assert config.ip_key_prefix == "auth:ip"


# --- Key Generation Tests ---


class TestLoginRateLimiterKeys:
    """Tests for key generation methods."""

    def test_ip_key_from_client(self) -> None:
        """ip_key extracts IP from request.client."""
        limiter = LoginRateLimiter()
        request = MockRequest(client_host="10.0.0.1")

        key = limiter.ip_key(request)

        assert key == "login:ip:10.0.0.1"

    def test_ip_key_from_forwarded_header(self) -> None:
        """ip_key uses X-Forwarded-For header when trust_proxy is enabled."""
        config = RateLimitConfig(trust_proxy=True)
        limiter = LoginRateLimiter(config=config)
        request = MockRequest(
            client_host="127.0.0.1",
            forwarded_for="203.0.113.50, 70.41.3.18",
        )

        key = limiter.ip_key(request)

        assert key == "login:ip:203.0.113.50"

    def test_identifier_key_is_hashed(self) -> None:
        """identifier_key hashes the identifier."""
        limiter = LoginRateLimiter()

        key = limiter.identifier_key("user@example.com")

        assert key.startswith("login:id:")
        assert "user@example.com" not in key
        assert len(key.split(":")[2]) == 16  # SHA256 truncated to 16 chars

    def test_identifier_key_case_insensitive(self) -> None:
        """identifier_key produces same hash for different cases."""
        limiter = LoginRateLimiter()

        key1 = limiter.identifier_key("User@Example.com")
        key2 = limiter.identifier_key("user@example.com")

        assert key1 == key2

    def test_combined_key_format(self) -> None:
        """combined_key includes IP and hashed identifier."""
        limiter = LoginRateLimiter()
        request = MockRequest(client_host="192.168.1.100")

        key = limiter.combined_key(request, "admin@test.com")

        assert key.startswith("login:combined:192.168.1.100:")
        assert "admin@test.com" not in key

    def test_custom_key_prefix(self) -> None:
        """Keys use custom prefix from config."""
        config = RateLimitConfig(
            ip_key_prefix="myapp:ip",
            identifier_key_prefix="myapp:user",
            combined_key_prefix="myapp:combo",
        )
        limiter = LoginRateLimiter(config=config)
        request = MockRequest()

        assert limiter.ip_key(request).startswith("myapp:ip:")
        assert limiter.identifier_key("test").startswith("myapp:user:")
        assert limiter.combined_key(request, "test").startswith("myapp:combo:")


# --- Standalone Mode Tests ---


class TestLoginRateLimiterStandalone:
    """Tests for standalone mode (without slowapi)."""

    def test_is_limited_returns_false_initially(self) -> None:
        """is_limited returns False when no attempts recorded."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        limiter = LoginRateLimiter(session_adapter=sessions)

        request = MockRequest()
        result = limiter.is_limited(request, "user@test.com")

        assert result is False

    def test_is_limited_without_session_adapter(self) -> None:
        """is_limited returns False when no session adapter configured."""
        limiter = LoginRateLimiter()  # No session adapter

        request = MockRequest()
        result = limiter.is_limited(request, "user@test.com")

        assert result is False

    def test_record_attempt_increments_counters(self) -> None:
        """record_attempt increments all three counters."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        limiter = LoginRateLimiter(session_adapter=sessions)

        request = MockRequest(client_host="10.0.0.1")
        limiter.record_attempt(request, "user@test.com")

        # Check counters were incremented
        assert sessions.get_counter_raw(limiter.ip_key(request)) == 1
        assert sessions.get_counter_raw(limiter.identifier_key("user@test.com")) == 1
        assert sessions.get_counter_raw(limiter.combined_key(request, "user@test.com")) == 1

    def test_is_limited_by_ip(self) -> None:
        """is_limited returns True when IP limit exceeded."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        config = RateLimitConfig(ip_limit="3/minute")
        limiter = LoginRateLimiter(session_adapter=sessions, config=config)

        request = MockRequest(client_host="10.0.0.1")

        # Record 3 attempts (reaches limit)
        for _ in range(3):
            limiter.record_attempt(request, "user@test.com")

        result = limiter.is_limited(request, "different@user.com")
        assert result is True

    def test_is_limited_by_identifier(self) -> None:
        """is_limited returns True when identifier limit exceeded."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        config = RateLimitConfig(identifier_limit="2/minute")
        limiter = LoginRateLimiter(session_adapter=sessions, config=config)

        # Different IPs, same identifier
        request1 = MockRequest(client_host="10.0.0.1")
        request2 = MockRequest(client_host="10.0.0.2")

        limiter.record_attempt(request1, "target@user.com")
        limiter.record_attempt(request2, "target@user.com")

        # New IP should still be limited for same identifier
        request3 = MockRequest(client_host="10.0.0.3")
        result = limiter.is_limited(request3, "target@user.com")
        assert result is True

    def test_is_limited_by_combined(self) -> None:
        """is_limited returns True when combined limit exceeded."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        config = RateLimitConfig(
            ip_limit="100/minute",
            identifier_limit="100/minute",
            combined_limit="2/minute",
        )
        limiter = LoginRateLimiter(session_adapter=sessions, config=config)

        request = MockRequest(client_host="10.0.0.1")

        # Record 2 attempts from same IP for same user
        limiter.record_attempt(request, "user@test.com")
        limiter.record_attempt(request, "user@test.com")

        result = limiter.is_limited(request, "user@test.com")
        assert result is True

        # Different user from same IP should not be limited
        result2 = limiter.is_limited(request, "other@test.com")
        assert result2 is False

    def test_clear_limits(self) -> None:
        """clear_limits removes rate limit counters."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        limiter = LoginRateLimiter(session_adapter=sessions)

        request = MockRequest()
        identifier = "user@test.com"

        # Record some attempts
        limiter.record_attempt(request, identifier)
        limiter.record_attempt(request, identifier)

        # Clear all limits
        limiter.clear_limits(request, identifier)

        # Verify counters are cleared
        assert sessions.get_counter_raw(limiter.ip_key(request)) == 0
        assert sessions.get_counter_raw(limiter.identifier_key(identifier)) == 0
        assert sessions.get_counter_raw(limiter.combined_key(request, identifier)) == 0

    def test_clear_limits_partial(self) -> None:
        """clear_limits can clear only specific limits."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        limiter = LoginRateLimiter(session_adapter=sessions)

        request = MockRequest()
        identifier = "user@test.com"

        limiter.record_attempt(request, identifier)

        # Clear only identifier
        limiter.clear_limits(identifier=identifier)

        # IP should still have count
        assert sessions.get_counter_raw(limiter.ip_key(request)) == 1
        # Identifier should be cleared
        assert sessions.get_counter_raw(limiter.identifier_key(identifier)) == 0

    def test_get_remaining(self) -> None:
        """get_remaining shows remaining attempts for each limit."""
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        config = RateLimitConfig(
            ip_limit="10/minute",
            identifier_limit="5/minute",
            combined_limit="3/minute",
        )
        limiter = LoginRateLimiter(session_adapter=sessions, config=config)

        request = MockRequest()
        identifier = "user@test.com"

        # Initially all at max
        remaining = limiter.get_remaining(request, identifier)
        assert remaining == {"ip": 10, "identifier": 5, "combined": 3}

        # After one attempt
        limiter.record_attempt(request, identifier)
        remaining = limiter.get_remaining(request, identifier)
        assert remaining == {"ip": 9, "identifier": 4, "combined": 2}

    def test_get_remaining_without_session(self) -> None:
        """get_remaining returns -1 when no session adapter."""
        limiter = LoginRateLimiter()  # No session adapter
        request = MockRequest()

        remaining = limiter.get_remaining(request, "user@test.com")

        assert remaining == {"ip": -1, "identifier": -1, "combined": -1}


# --- Limit Parsing Tests ---


class TestLoginRateLimiterParsing:
    """Tests for limit string parsing."""

    def test_parse_limit_minute(self) -> None:
        """_parse_limit extracts count from limit string."""
        limiter = LoginRateLimiter()

        assert limiter._parse_limit("10/minute") == 10
        assert limiter._parse_limit("5/minute") == 5
        assert limiter._parse_limit("100/hour") == 100

    def test_parse_ttl_minute(self) -> None:
        """_parse_ttl converts unit to seconds."""
        limiter = LoginRateLimiter()

        assert limiter._parse_ttl("10/second") == 1
        assert limiter._parse_ttl("10/minute") == 60
        assert limiter._parse_ttl("10/hour") == 3600
        assert limiter._parse_ttl("10/day") == 86400

    def test_parse_ttl_unknown_defaults_to_minute(self) -> None:
        """_parse_ttl defaults to 60 for unknown units."""
        limiter = LoginRateLimiter()

        assert limiter._parse_ttl("10/unknown") == 60


# --- Custom IP Function Tests ---


class TestLoginRateLimiterCustomIP:
    """Tests for custom IP extraction function."""

    def test_custom_get_ip_function(self) -> None:
        """LoginRateLimiter uses custom get_ip function."""

        def custom_get_ip(request: Any) -> str:
            return "custom-ip-from-header"

        limiter = LoginRateLimiter(get_ip=custom_get_ip)
        request = MockRequest(client_host="10.0.0.1")

        key = limiter.ip_key(request)

        assert key == "login:ip:custom-ip-from-header"


# --- Decorator Mode Tests ---


class TestLoginRateLimiterDecorator:
    """Tests for decorator mode (with slowapi)."""

    def test_limit_requires_limiter(self) -> None:
        """limit() raises RuntimeError if no slowapi limiter configured."""
        limiter = LoginRateLimiter()  # No slowapi limiter

        try:
            limiter.limit()
            raise AssertionError("Expected RuntimeError")
        except RuntimeError as e:
            assert "slowapi Limiter required" in str(e)
