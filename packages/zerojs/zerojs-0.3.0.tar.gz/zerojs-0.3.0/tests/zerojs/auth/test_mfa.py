"""Tests for MFA module."""

from __future__ import annotations

import asyncio
from typing import Any

from zerojs.auth import MFAChallenge, MFAConfig, MFAManager, MFAResult
from zerojs.auth.session_adapter import AuthSessionAdapter
from zerojs.session import MemorySessionStore


class MockUser:
    """Mock user for testing."""

    def __init__(
        self,
        user_id: int,
        name: str = "Test User",
        mfa_enabled: bool = True,
        totp_secret: str | None = "JBSWY3DPEHPK3PXP",
    ):
        self.id = user_id
        self.name = name
        self.mfa_enabled = mfa_enabled
        self.totp_secret = totp_secret


class MockMFAProvider:
    """Mock MFA provider for testing."""

    def __init__(
        self,
        valid_code: str = "123456",
        methods: list[str] | None = None,
    ):
        self.valid_code = valid_code
        self._methods = methods if methods is not None else ["totp"]
        self.challenges_sent: list[tuple[Any, str]] = []

    async def is_enabled(self, user: MockUser) -> bool:
        return user.mfa_enabled

    async def get_methods(self, user: MockUser) -> list[str]:
        return self._methods.copy()

    async def send_challenge(self, user: MockUser, method: str) -> bool:
        self.challenges_sent.append((user, method))
        return True

    async def verify(self, user: MockUser, method: str, code: str) -> bool:
        return code == self.valid_code


class MockUserProvider:
    """Mock user provider for testing."""

    def __init__(self, users: dict[int, MockUser] | None = None):
        self.users = users or {}

    async def get_by_id(self, user_id: int) -> MockUser | None:
        return self.users.get(user_id)

    async def get_by_identifier(self, identifier: str) -> MockUser | None:
        for user in self.users.values():
            if user.name == identifier:
                return user
        return None


# --- MFAChallenge Tests ---


class TestMFAChallenge:
    """Tests for MFAChallenge dataclass."""

    def test_create_challenge(self) -> None:
        """MFAChallenge can be created with all fields."""
        challenge = MFAChallenge(
            token="test-token",
            method="totp",
            available_methods=["totp", "sms"],
            expires_in=300,
        )

        assert challenge.token == "test-token"
        assert challenge.method == "totp"
        assert challenge.available_methods == ["totp", "sms"]
        assert challenge.expires_in == 300


# --- MFAResult Tests ---


class TestMFAResult:
    """Tests for MFAResult dataclass."""

    def test_successful_result(self) -> None:
        """MFAResult can represent success."""
        user = MockUser(1)
        result: MFAResult[MockUser] = MFAResult(success=True, user=user)

        assert result.success is True
        assert result.user is user
        assert result.error is None

    def test_failed_result(self) -> None:
        """MFAResult can represent failure."""
        result: MFAResult[MockUser] = MFAResult(success=False, error="invalid_code")

        assert result.success is False
        assert result.user is None
        assert result.error == "invalid_code"


# --- MFAManager Tests ---


class TestMFAManagerCreateChallenge:
    """Tests for MFAManager.create_challenge()."""

    def test_creates_challenge_with_token(self) -> None:
        """create_challenge returns MFAChallenge with token."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user)

            assert isinstance(challenge, MFAChallenge)
            assert len(challenge.token) > 0
            assert challenge.method == "totp"
            assert challenge.available_methods == ["totp"]
            assert challenge.expires_in == 300

        asyncio.run(run_test())

    def test_stores_token_in_session(self) -> None:
        """create_challenge stores token data in session."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user)

            # Verify token was stored
            data = sessions.get_raw(f"mfa:{challenge.token}")
            assert data is not None
            assert data["user_id"] == 1
            assert data["method"] == "totp"

        asyncio.run(run_test())

    def test_uses_specified_method(self) -> None:
        """create_challenge uses specified method if available."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["totp", "sms", "email"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user, method="sms")

            assert challenge.method == "sms"
            assert challenge.available_methods == ["totp", "sms", "email"]

        asyncio.run(run_test())

    def test_falls_back_to_first_method(self) -> None:
        """create_challenge falls back to first method if specified unavailable."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["totp"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user, method="sms")  # Not available

            assert challenge.method == "totp"

        asyncio.run(run_test())

    def test_sends_challenge_for_sms(self) -> None:
        """create_challenge sends challenge for SMS method."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["sms"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            await mfa.create_challenge(user)

            assert len(provider.challenges_sent) == 1
            assert provider.challenges_sent[0] == (user, "sms")

        asyncio.run(run_test())

    def test_sends_challenge_for_email(self) -> None:
        """create_challenge sends challenge for email method."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["email"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            await mfa.create_challenge(user)

            assert len(provider.challenges_sent) == 1
            assert provider.challenges_sent[0] == (user, "email")

        asyncio.run(run_test())

    def test_no_send_for_totp(self) -> None:
        """create_challenge does not send challenge for TOTP."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["totp"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            await mfa.create_challenge(user)

            assert len(provider.challenges_sent) == 0

        asyncio.run(run_test())

    def test_raises_for_no_methods(self) -> None:
        """create_challenge raises ValueError if no methods available."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=[])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            try:
                await mfa.create_challenge(user)
                raise AssertionError("Expected ValueError to be raised")
            except ValueError as e:
                assert "No MFA methods" in str(e)

        asyncio.run(run_test())

    def test_custom_token_ttl(self) -> None:
        """create_challenge respects custom token TTL."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            config = MFAConfig(token_ttl=600)
            mfa = MFAManager(provider, sessions, config=config)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user)

            assert challenge.expires_in == 600

        asyncio.run(run_test())


class TestMFAManagerVerifyChallenge:
    """Tests for MFAManager.verify_challenge()."""

    def test_verifies_valid_code(self) -> None:
        """verify_challenge returns success for valid code."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(valid_code="654321")
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            result = await mfa.verify_challenge(challenge.token, "654321", users)

            assert result.success is True
            assert result.user is user
            assert result.error is None

        asyncio.run(run_test())

    def test_rejects_invalid_code(self) -> None:
        """verify_challenge returns failure for invalid code."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(valid_code="654321")
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            result = await mfa.verify_challenge(challenge.token, "000000", users)

            assert result.success is False
            assert result.error == "invalid_code"

        asyncio.run(run_test())

    def test_rejects_expired_token(self) -> None:
        """verify_challenge returns failure for expired/invalid token."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            users = MockUserProvider({})

            result = await mfa.verify_challenge("invalid-token", "123456", users)

            assert result.success is False
            assert result.error == "mfa_token_expired"

        asyncio.run(run_test())

    def test_rejects_when_user_not_found(self) -> None:
        """verify_challenge returns failure when user no longer exists."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user)

            # User provider without the user
            users = MockUserProvider({})

            result = await mfa.verify_challenge(challenge.token, "123456", users)

            assert result.success is False
            assert result.error == "user_not_found"

        asyncio.run(run_test())

    def test_clears_token_on_success(self) -> None:
        """verify_challenge clears token after successful verification."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            await mfa.verify_challenge(challenge.token, "123456", users)

            # Token should be deleted
            data = sessions.get_raw(f"mfa:{challenge.token}")
            assert data is None

        asyncio.run(run_test())

    def test_keeps_token_on_failure(self) -> None:
        """verify_challenge keeps token after failed verification."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            await mfa.verify_challenge(challenge.token, "wrong-code", users)

            # Token should still exist
            data = sessions.get_raw(f"mfa:{challenge.token}")
            assert data is not None

        asyncio.run(run_test())


class TestMFAManagerResendChallenge:
    """Tests for MFAManager.resend_challenge()."""

    def test_resends_challenge(self) -> None:
        """resend_challenge creates new challenge for same user."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["sms"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge1 = await mfa.create_challenge(user)
            challenge2 = await mfa.resend_challenge(challenge1.token, users)

            assert challenge2 is not None
            assert challenge2.token != challenge1.token
            assert challenge2.method == "sms"

            # Old token should be deleted
            data = sessions.get_raw(f"mfa:{challenge1.token}")
            assert data is None

            # Should have sent two challenges
            assert len(provider.challenges_sent) == 2

        asyncio.run(run_test())

    def test_switches_method(self) -> None:
        """resend_challenge can switch to different method."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["totp", "sms"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge1 = await mfa.create_challenge(user, method="totp")
            challenge2 = await mfa.resend_challenge(challenge1.token, users, method="sms")

            assert challenge2 is not None
            assert challenge2.method == "sms"

        asyncio.run(run_test())

    def test_returns_none_for_invalid_token(self) -> None:
        """resend_challenge returns None for invalid token."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            users = MockUserProvider({})

            result = await mfa.resend_challenge("invalid-token", users)

            assert result is None

        asyncio.run(run_test())


class TestMFAManagerHelperMethods:
    """Tests for MFAManager helper methods."""

    def test_get_challenge_info(self) -> None:
        """get_challenge_info returns info about existing challenge."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["totp", "sms"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user, method="totp")
            info = await mfa.get_challenge_info(challenge.token, users)

            assert info is not None
            assert info.token == challenge.token
            assert info.method == "totp"
            assert info.available_methods == ["totp", "sms"]

        asyncio.run(run_test())

    def test_get_challenge_info_returns_none_for_invalid(self) -> None:
        """get_challenge_info returns None for invalid token."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            users = MockUserProvider({})

            info = await mfa.get_challenge_info("invalid-token", users)

            assert info is None

        asyncio.run(run_test())

    def test_invalidate_challenge(self) -> None:
        """invalidate_challenge removes token from storage."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            challenge = await mfa.create_challenge(user)

            mfa.invalidate_challenge(challenge.token)

            data = sessions.get_raw(f"mfa:{challenge.token}")
            assert data is None

        asyncio.run(run_test())

    def test_get_user_methods(self) -> None:
        """get_user_methods returns available methods."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(methods=["totp", "sms", "email"])
            mfa = MFAManager(provider, sessions)

            user = MockUser(1)
            methods = await mfa.get_user_methods(user)

            assert methods == ["totp", "sms", "email"]

        asyncio.run(run_test())

    def test_is_mfa_enabled(self) -> None:
        """is_mfa_enabled checks if MFA is enabled for user."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider()
            mfa = MFAManager(provider, sessions)

            user_with_mfa = MockUser(1, mfa_enabled=True)
            user_without_mfa = MockUser(2, mfa_enabled=False)

            assert await mfa.is_mfa_enabled(user_with_mfa) is True
            assert await mfa.is_mfa_enabled(user_without_mfa) is False

        asyncio.run(run_test())


# --- MFA Rate Limiting Tests ---


class TestMFARateLimiting:
    """Tests for MFA rate limiting."""

    def test_mfa_blocks_after_max_attempts(self) -> None:
        """MFA blocks after max_attempts failed attempts."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(valid_code="123456")
            config = MFAConfig(token_ttl=300, max_attempts=3)
            mfa = MFAManager(provider, sessions, config=config)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            token = challenge.token

            # Make max_attempts (3) failed attempts
            for _ in range(3):
                result = await mfa.verify_challenge(token, "000000", users)
                assert result.success is False
                assert result.error == "invalid_code"

            # Next attempt should fail with too_many_attempts
            result = await mfa.verify_challenge(token, "000000", users)
            assert result.success is False
            assert result.error == "too_many_attempts"

        asyncio.run(run_test())

    def test_mfa_token_invalidated_after_max_attempts(self) -> None:
        """MFA token is invalidated after max attempts."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(valid_code="123456")
            config = MFAConfig(token_ttl=300, max_attempts=3)
            mfa = MFAManager(provider, sessions, config=config)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            token = challenge.token

            # Exhaust attempts
            for _ in range(3):
                await mfa.verify_challenge(token, "000000", users)

            # Trigger invalidation
            await mfa.verify_challenge(token, "000000", users)

            # Even with correct code, token is now invalid
            result = await mfa.verify_challenge(token, "123456", users)
            assert result.success is False
            assert result.error == "mfa_token_expired"

        asyncio.run(run_test())

    def test_mfa_counter_cleared_on_success(self) -> None:
        """Attempts counter is cleared after successful verification."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(valid_code="123456")
            config = MFAConfig(token_ttl=300, max_attempts=3)
            mfa = MFAManager(provider, sessions, config=config)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)
            token = challenge.token

            # Make 2 failed attempts (doesn't reach max_attempts=3)
            for _ in range(2):
                await mfa.verify_challenge(token, "000000", users)

            # Verify with correct code
            result = await mfa.verify_challenge(token, "123456", users)
            assert result.success is True
            assert result.user == user

            # Counter should be cleared
            attempts_key = f"mfa_attempts:{token}"
            assert sessions.get_counter_raw(attempts_key) == 0

        asyncio.run(run_test())

    def test_mfa_success_without_failed_attempts(self) -> None:
        """Successful verification without prior failed attempts."""

        async def run_test() -> None:
            store = MemorySessionStore()
            sessions = AuthSessionAdapter(store)
            provider = MockMFAProvider(valid_code="123456")
            config = MFAConfig(token_ttl=300, max_attempts=3)
            mfa = MFAManager(provider, sessions, config=config)

            user = MockUser(1)
            users = MockUserProvider({1: user})

            challenge = await mfa.create_challenge(user)

            result = await mfa.verify_challenge(challenge.token, "123456", users)
            assert result.success is True
            assert result.user == user

        asyncio.run(run_test())
