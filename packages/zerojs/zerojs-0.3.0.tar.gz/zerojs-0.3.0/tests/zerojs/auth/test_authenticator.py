"""Tests for Authenticator."""

import asyncio
from typing import Any

import pytest

from zerojs.auth.authenticator import AuthConfig, Authenticator, AuthResult
from zerojs.auth.events import AuthEvent, AuthEventEmitter
from zerojs.auth.session_adapter import AuthSessionAdapter
from zerojs.auth.testing import MockCredentialVerifier, MockMFAProvider, MockUser, MockUserProvider
from zerojs.session.backends.memory import MemorySessionStore


class MockTokenProvider:
    """Mock token provider (not in shared testing utilities)."""

    def create(self, payload: dict[str, Any]) -> str:
        return f"token_{payload.get('sub', 'unknown')}"

    def verify(self, token: str) -> dict[str, Any] | None:
        if token.startswith("token_"):
            return {"sub": token[6:]}
        return None

    def refresh(self, token: str) -> str | None:
        return token


class TestAuthConfig:
    """Tests for AuthConfig validation."""

    def test_default_values(self) -> None:
        """AuthConfig has sensible defaults."""
        config = AuthConfig()
        assert config.session_ttl == 86400
        assert config.remember_me_ttl == 2592000
        assert config.rate_limit_enabled is True
        assert config.rate_limit_max_attempts == 5

    def test_session_ttl_must_be_positive(self) -> None:
        """session_ttl must be positive."""
        with pytest.raises(ValueError, match="session_ttl must be positive"):
            AuthConfig(session_ttl=0)

        with pytest.raises(ValueError, match="session_ttl must be positive"):
            AuthConfig(session_ttl=-1)

    def test_remember_me_ttl_must_be_gte_session_ttl(self) -> None:
        """remember_me_ttl must be >= session_ttl."""
        with pytest.raises(ValueError, match="remember_me_ttl should be >= session_ttl"):
            AuthConfig(session_ttl=3600, remember_me_ttl=1800)

    def test_rate_limit_max_attempts_must_be_positive(self) -> None:
        """rate_limit_max_attempts must be >= 1."""
        with pytest.raises(ValueError, match="rate_limit_max_attempts must be >= 1"):
            AuthConfig(rate_limit_max_attempts=0)

    def test_rate_limit_window_must_be_non_negative(self) -> None:
        """rate_limit_window must be non-negative."""
        with pytest.raises(ValueError, match="rate_limit_window must be non-negative"):
            AuthConfig(rate_limit_window=-1)

    def test_rate_limit_lockout_must_be_non_negative(self) -> None:
        """rate_limit_lockout must be non-negative."""
        with pytest.raises(ValueError, match="rate_limit_lockout must be non-negative"):
            AuthConfig(rate_limit_lockout=-1)


class TestAuthResult:
    """Tests for AuthResult."""

    def test_success_result(self) -> None:
        """AuthResult can represent success."""
        user = MockUser(id=1, email="test@example.com")
        result: AuthResult[MockUser] = AuthResult(
            success=True,
            user=user,
            session_id="session123",
        )
        assert result.success is True
        assert result.user == user
        assert result.session_id == "session123"

    def test_failure_result(self) -> None:
        """AuthResult can represent failure."""
        result: AuthResult[MockUser] = AuthResult(success=False, error="invalid_credentials")
        assert result.success is False
        assert result.error == "invalid_credentials"

    def test_mfa_required_result(self) -> None:
        """AuthResult can represent MFA required."""
        user = MockUser(id=1, email="test@example.com")
        result: AuthResult[MockUser] = AuthResult(
            success=False,
            user=user,
            requires_mfa=True,
            mfa_token="mfa_token_123",
        )
        assert result.success is False
        assert result.requires_mfa is True
        assert result.mfa_token == "mfa_token_123"


class TestAuthenticatorBasic:
    """Tests for basic Authenticator functionality."""

    @pytest.fixture
    def user(self) -> MockUser:
        return MockUser(id=1, email="test@example.com")

    @pytest.fixture
    def auth(self, user: MockUser) -> Authenticator[MockUser]:
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        return Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            config=AuthConfig(rate_limit_enabled=False),
        )

    def test_successful_authentication(self, auth: Authenticator, user: MockUser) -> None:
        """Successful authentication returns user and session."""

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is True
            assert result.user == user
            assert result.session_id is not None
            assert result.error is None

        asyncio.run(check())

    def test_wrong_password(self, auth: Authenticator) -> None:
        """Wrong password returns invalid_credentials error."""

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="wrong_password",
            )
            assert result.success is False
            assert result.error == "invalid_credentials"
            assert result.session_id is None

        asyncio.run(check())

    def test_user_not_found(self, auth: Authenticator) -> None:
        """Unknown user returns invalid_credentials error."""

        async def check() -> None:
            result = await auth.authenticate(
                identifier="unknown@example.com",
                credential="password",
            )
            assert result.success is False
            assert result.error == "invalid_credentials"

        asyncio.run(check())

    def test_inactive_user(self, auth: Authenticator, user: MockUser) -> None:
        """Inactive user returns account_inactive error."""
        user.is_active = False

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is False
            assert result.error == "account_inactive"

        asyncio.run(check())

    def test_remember_me_uses_extended_ttl(self, user: MockUser) -> None:
        """remember_me=True uses extended TTL."""
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            config=AuthConfig(
                session_ttl=3600,
                remember_me_ttl=86400,
                rate_limit_enabled=False,
            ),
        )

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
                remember_me=True,
            )
            assert result.success is True
            assert result.session_id is not None

            # Check session data
            data = sessions.get_data(result.session_id)
            assert data is not None
            assert data["remember_me"] is True

        asyncio.run(check())


class TestAuthenticatorRateLimiting:
    """Tests for rate limiting."""

    @pytest.fixture
    def user(self) -> MockUser:
        return MockUser(id=1, email="test@example.com")

    @pytest.fixture
    def auth(self, user: MockUser) -> Authenticator[MockUser]:
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        return Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            config=AuthConfig(
                rate_limit_enabled=True,
                rate_limit_max_attempts=3,
                rate_limit_window=300,
                rate_limit_lockout=60,
            ),
        )

    def test_rate_limit_after_max_attempts(self, auth: Authenticator[MockUser]) -> None:
        """User is rate limited after max failed attempts."""

        async def check() -> None:
            # Make max_attempts failed attempts
            for _ in range(3):
                result = await auth.authenticate(
                    identifier="test@example.com",
                    credential="wrong_password",
                )
                assert result.error == "invalid_credentials"

            # Next attempt should be rate limited
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",  # Even correct password
            )
            assert result.success is False
            assert result.error == "too_many_attempts"

        asyncio.run(check())

    def test_successful_login_clears_rate_limit(self, auth: Authenticator[MockUser]) -> None:
        """Successful login clears rate limit counter."""

        async def check() -> None:
            # Make some failed attempts (but not max)
            for _ in range(2):
                await auth.authenticate(
                    identifier="test@example.com",
                    credential="wrong_password",
                )

            # Successful login
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is True

            # Counter should be cleared - can fail again without rate limit
            for _ in range(2):
                await auth.authenticate(
                    identifier="test@example.com",
                    credential="wrong_password",
                )

            # Should still be able to login (counter was reset)
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is True

        asyncio.run(check())

    def test_rate_limit_is_per_identifier(self, auth: Authenticator[MockUser]) -> None:
        """Rate limit is per identifier, not global."""
        # Add another user
        user2 = MockUser(id=2, email="other@example.com")
        auth.users.add_user(user2)

        async def check() -> None:
            # Rate limit first user
            for _ in range(3):
                await auth.authenticate(
                    identifier="test@example.com",
                    credential="wrong_password",
                )

            # First user is rate limited
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.error == "too_many_attempts"

            # Second user can still login
            result = await auth.authenticate(
                identifier="other@example.com",
                credential="correct_password",
            )
            assert result.success is True

        asyncio.run(check())


class TestAuthenticatorMFA:
    """Tests for MFA flow."""

    @pytest.fixture
    def user(self) -> MockUser:
        return MockUser(id=1, email="test@example.com")

    @pytest.fixture
    def auth(self, user: MockUser) -> Authenticator[MockUser]:
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        mfa = MockMFAProvider(enabled_users={1}, valid_code="123456")
        return Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            mfa_provider=mfa,
            config=AuthConfig(rate_limit_enabled=False),
        )

    def test_mfa_required_when_enabled(self, auth: Authenticator[MockUser], user: MockUser) -> None:
        """MFA is required when user has MFA enabled."""

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is False
            assert result.requires_mfa is True
            assert result.mfa_token is not None
            assert result.user == user

        asyncio.run(check())

    def test_complete_mfa_success(self, auth: Authenticator[MockUser]) -> None:
        """Successful MFA completion returns session."""

        async def check() -> None:
            # Initial authentication
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.requires_mfa is True
            mfa_token = result.mfa_token

            # Complete MFA
            result = await auth.complete_mfa(
                mfa_token=mfa_token,
                code="123456",
            )
            assert result.success is True
            assert result.session_id is not None

        asyncio.run(check())

    def test_complete_mfa_wrong_code(self, auth: Authenticator[MockUser]) -> None:
        """Wrong MFA code returns error."""

        async def check() -> None:
            # Initial authentication
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            mfa_token = result.mfa_token

            # Wrong MFA code
            result = await auth.complete_mfa(
                mfa_token=mfa_token,
                code="000000",
            )
            assert result.success is False
            assert result.error == "invalid_mfa_code"

        asyncio.run(check())

    def test_complete_mfa_expired_token(self, auth: Authenticator[MockUser]) -> None:
        """Expired MFA token returns error."""

        async def check() -> None:
            result = await auth.complete_mfa(
                mfa_token="invalid_token",
                code="123456",
            )
            assert result.success is False
            assert result.error == "mfa_token_expired"

        asyncio.run(check())

    def test_mfa_token_is_invalidated_after_use(self, auth: Authenticator[MockUser]) -> None:
        """MFA token cannot be reused."""

        async def check() -> None:
            # Initial authentication
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            mfa_token = result.mfa_token

            # Complete MFA
            result = await auth.complete_mfa(
                mfa_token=mfa_token,
                code="123456",
            )
            assert result.success is True

            # Try to reuse token
            result = await auth.complete_mfa(
                mfa_token=mfa_token,
                code="123456",
            )
            assert result.success is False
            assert result.error == "mfa_token_expired"

        asyncio.run(check())


class TestAuthenticatorLogout:
    """Tests for logout."""

    @pytest.fixture
    def user(self) -> MockUser:
        return MockUser(id=1, email="test@example.com")

    @pytest.fixture
    def auth(self, user: MockUser) -> Authenticator[MockUser]:
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        return Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            config=AuthConfig(rate_limit_enabled=False),
        )

    def test_logout_destroys_session(self, auth: Authenticator[MockUser]) -> None:
        """Logout destroys the session."""

        async def check() -> None:
            # Login
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            session_id = result.session_id
            assert auth.sessions.get_user_id(session_id) == 1

            # Logout
            await auth.logout(session_id=session_id)

            # Session should be destroyed
            assert auth.sessions.get_user_id(session_id) is None

        asyncio.run(check())


class TestAuthenticatorEvents:
    """Tests for event emission."""

    @pytest.fixture
    def user(self) -> MockUser:
        return MockUser(id=1, email="test@example.com")

    def test_login_success_event(self, user: MockUser) -> None:
        """LOGIN_SUCCESS event is emitted on success."""
        events = AuthEventEmitter()
        emitted: list[dict[str, Any]] = []

        @events.on(AuthEvent.LOGIN_SUCCESS)
        async def handler(**ctx: Any) -> None:
            emitted.append(ctx)

        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            events=events,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
                context={"ip": "1.2.3.4"},
            )
            assert len(emitted) == 1
            assert emitted[0]["user"] == user
            assert emitted[0]["ip"] == "1.2.3.4"

        asyncio.run(check())

    def test_login_failed_event(self, user: MockUser) -> None:
        """LOGIN_FAILED event is emitted on failure."""
        events = AuthEventEmitter()
        emitted: list[dict[str, Any]] = []

        @events.on(AuthEvent.LOGIN_FAILED)
        async def handler(**ctx: Any) -> None:
            emitted.append(ctx)

        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            events=events,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            await auth.authenticate(
                identifier="test@example.com",
                credential="wrong_password",
            )
            assert len(emitted) == 1
            assert emitted[0]["identifier"] == "test@example.com"
            assert emitted[0]["reason"] == "invalid_credential"

        asyncio.run(check())

    def test_logout_event(self, user: MockUser) -> None:
        """LOGOUT event is emitted on logout."""
        events = AuthEventEmitter()
        emitted: list[dict[str, Any]] = []

        @events.on(AuthEvent.LOGOUT)
        async def handler(**ctx: Any) -> None:
            emitted.append(ctx)

        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            session_adapter=sessions,
            events=events,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            await auth.logout(session_id=result.session_id)
            assert len(emitted) == 1

        asyncio.run(check())


class TestAuthenticatorTokens:
    """Tests for token-based authentication."""

    @pytest.fixture
    def user(self) -> MockUser:
        return MockUser(id=1, email="test@example.com")

    def test_creates_token_when_provider_configured(self, user: MockUser) -> None:
        """Token is created when token provider is configured."""
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        tokens = MockTokenProvider()
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            token_provider=tokens,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is True
            assert result.token == "token_1"

        asyncio.run(check())

    def test_no_token_without_provider(self, user: MockUser) -> None:
        """No token is created without token provider."""
        users = MockUserProvider([user])
        verifier = MockCredentialVerifier(valid_password="correct_password")
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct_password",
            )
            assert result.success is True
            assert result.token is None

        asyncio.run(check())


# --- Timing Attack Mitigation Tests ---


class MockCredentialVerifierWithDummy(MockCredentialVerifier):
    """Mock verifier that tracks dummy_verify calls."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dummy_verify_called = False

    def dummy_verify(self) -> None:
        """Track that dummy_verify was called."""
        self.dummy_verify_called = True


class TestTimingAttackMitigation:
    """Tests for timing attack mitigation via dummy_verify."""

    def test_dummy_verify_called_when_user_not_found(self) -> None:
        """dummy_verify() is called when user doesn't exist."""
        users = MockUserProvider([])  # No users
        verifier = MockCredentialVerifierWithDummy(valid_password="password")
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            result = await auth.authenticate(
                identifier="nonexistent@example.com",
                credential="password",
            )
            assert result.success is False
            assert result.error == "invalid_credentials"
            assert verifier.dummy_verify_called is True

        asyncio.run(check())

    def test_dummy_verify_not_called_when_user_exists(self) -> None:
        """dummy_verify() is NOT called when user exists."""
        user = MockUser(id=1, email="test@example.com")
        users = MockUserProvider([user])
        verifier = MockCredentialVerifierWithDummy(valid_password="correct")
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            # Wrong password but user exists
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="wrong_password",
            )
            assert result.success is False
            assert result.error == "invalid_credentials"
            # dummy_verify should NOT be called when user exists
            assert verifier.dummy_verify_called is False

        asyncio.run(check())

    def test_dummy_verify_not_called_on_successful_auth(self) -> None:
        """dummy_verify() is NOT called on successful authentication."""
        user = MockUser(id=1, email="test@example.com")
        users = MockUserProvider([user])
        verifier = MockCredentialVerifierWithDummy(valid_password="correct")
        auth = Authenticator(
            user_provider=users,
            credential_verifier=verifier,
            config=AuthConfig(rate_limit_enabled=False),
        )

        async def check() -> None:
            result = await auth.authenticate(
                identifier="test@example.com",
                credential="correct",
            )
            assert result.success is True
            assert verifier.dummy_verify_called is False

        asyncio.run(check())
