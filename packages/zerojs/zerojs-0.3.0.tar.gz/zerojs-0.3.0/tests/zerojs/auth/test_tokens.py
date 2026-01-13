"""Tests for SecureToken utilities."""

import time_machine

from zerojs.auth import SecureToken


class TestSecureTokenGenerate:
    """Tests for SecureToken.generate()."""

    def test_returns_string(self) -> None:
        """generate() returns a string."""
        token = SecureToken.generate()
        assert isinstance(token, str)

    def test_default_length(self) -> None:
        """generate() returns URL-safe base64 token."""
        token = SecureToken.generate()
        # 32 bytes = ~43 characters in base64
        assert len(token) >= 32

    def test_custom_length(self) -> None:
        """generate() respects length parameter."""
        short = SecureToken.generate(8)
        long = SecureToken.generate(64)
        assert len(short) < len(long)

    def test_unique_tokens(self) -> None:
        """generate() creates unique tokens."""
        tokens = [SecureToken.generate() for _ in range(100)]
        assert len(set(tokens)) == 100

    def test_url_safe(self) -> None:
        """generate() creates URL-safe tokens."""
        for _ in range(100):
            token = SecureToken.generate()
            # URL-safe base64 uses only these characters
            assert all(c.isalnum() or c in "-_" for c in token)


class TestSecureTokenGenerateNumeric:
    """Tests for SecureToken.generate_numeric()."""

    def test_returns_string(self) -> None:
        """generate_numeric() returns a string."""
        code = SecureToken.generate_numeric()
        assert isinstance(code, str)

    def test_default_length(self) -> None:
        """generate_numeric() defaults to 6 digits."""
        code = SecureToken.generate_numeric()
        assert len(code) == 6

    def test_custom_length(self) -> None:
        """generate_numeric() respects length parameter."""
        code = SecureToken.generate_numeric(8)
        assert len(code) == 8

    def test_only_digits(self) -> None:
        """generate_numeric() returns only digits."""
        for _ in range(100):
            code = SecureToken.generate_numeric()
            assert code.isdigit()

    def test_unique_codes(self) -> None:
        """generate_numeric() creates unique codes (mostly)."""
        codes = [SecureToken.generate_numeric() for _ in range(100)]
        # Allow some collisions with 6 digits (1M possibilities)
        assert len(set(codes)) >= 90


class TestSecureTokenTimed:
    """Tests for SecureToken.generate_timed() and verify_timed()."""

    SECRET = "test-secret-key"

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_generate_returns_string(self) -> None:
        """generate_timed() returns a string."""
        token = SecureToken.generate_timed("data", self.SECRET, ttl=3600)
        assert isinstance(token, str)

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_verify_valid_token(self) -> None:
        """verify_timed() returns data for valid token."""
        token = SecureToken.generate_timed("user123", self.SECRET, ttl=3600)
        result = SecureToken.verify_timed(token, self.SECRET)
        assert result == "user123"

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_verify_expired_token(self) -> None:
        """verify_timed() returns None for expired token."""
        token = SecureToken.generate_timed("data", self.SECRET, ttl=60)

        with time_machine.travel("2024-01-01 12:02:00", tick=False):
            result = SecureToken.verify_timed(token, self.SECRET)
            assert result is None

    def test_verify_wrong_secret(self) -> None:
        """verify_timed() returns None for wrong secret."""
        token = SecureToken.generate_timed("data", "secret1", ttl=3600)
        result = SecureToken.verify_timed(token, "secret2")
        assert result is None

    def test_verify_tampered_token(self) -> None:
        """verify_timed() returns None for tampered token."""
        token = SecureToken.generate_timed("data", self.SECRET, ttl=3600)
        # Tamper with the token
        tampered = token[:-5] + "XXXXX"
        result = SecureToken.verify_timed(tampered, self.SECRET)
        assert result is None

    def test_verify_invalid_token(self) -> None:
        """verify_timed() returns None for invalid token."""
        assert SecureToken.verify_timed("not-a-valid-token", self.SECRET) is None
        assert SecureToken.verify_timed("", self.SECRET) is None

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_data_with_special_characters(self) -> None:
        """generate_timed() handles special characters in data."""
        special_data = 'user@example.com|role:admin|{"key": "value"}'
        token = SecureToken.generate_timed(special_data, self.SECRET, ttl=3600)
        result = SecureToken.verify_timed(token, self.SECRET)
        assert result == special_data

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_token_is_url_safe(self) -> None:
        """generate_timed() creates URL-safe tokens."""
        token = SecureToken.generate_timed("data", self.SECRET, ttl=3600)
        # URL-safe base64 uses only these characters (plus padding =)
        assert all(c.isalnum() or c in "-_=" for c in token)

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_verify_just_before_expiry(self) -> None:
        """verify_timed() works just before expiry."""
        token = SecureToken.generate_timed("data", self.SECRET, ttl=60)

        with time_machine.travel("2024-01-01 12:00:59", tick=False):
            result = SecureToken.verify_timed(token, self.SECRET)
            assert result == "data"

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_verify_just_after_expiry(self) -> None:
        """verify_timed() fails just after expiry."""
        token = SecureToken.generate_timed("data", self.SECRET, ttl=60)

        with time_machine.travel("2024-01-01 12:01:01", tick=False):
            result = SecureToken.verify_timed(token, self.SECRET)
            assert result is None
