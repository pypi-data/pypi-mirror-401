"""Authentication orchestrator.

Coordinates the authentication flow including user lookup, credential
verification, rate limiting, MFA, and session/token management.
"""

from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from .context import AuthContext
from .events import AuthEvent, AuthEventEmitter
from .protocols import CredentialVerifier, MFAProvider, TokenProvider, UserProvider
from .session_adapter import AuthSessionAdapter

if TYPE_CHECKING:
    from zerojs.session.middleware import SessionInterface

T = TypeVar("T")


@dataclass
class AuthConfig:
    """Authenticator configuration.

    Attributes:
        session_ttl: Default session TTL in seconds.
        remember_me_ttl: Session TTL when "remember me" is enabled.
        rate_limit_enabled: Whether to enable built-in rate limiting.
        rate_limit_max_attempts: Max login attempts before lockout.
        rate_limit_window: Window in seconds for counting attempts.
        rate_limit_lockout: Lockout duration in seconds after max attempts.
    """

    session_ttl: int = 86400  # 1 day
    remember_me_ttl: int = 2592000  # 30 days
    rate_limit_enabled: bool = True
    rate_limit_max_attempts: int = 5
    rate_limit_window: int = 300  # 5 minutes
    rate_limit_lockout: int = 900  # 15 minutes

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.session_ttl <= 0:
            raise ValueError("session_ttl must be positive")
        if self.remember_me_ttl < self.session_ttl:
            raise ValueError("remember_me_ttl should be >= session_ttl")
        if self.rate_limit_max_attempts < 1:
            raise ValueError("rate_limit_max_attempts must be >= 1")
        if self.rate_limit_window < 0:
            raise ValueError("rate_limit_window must be non-negative")
        if self.rate_limit_lockout < 0:
            raise ValueError("rate_limit_lockout must be non-negative")


@dataclass
class AuthResult(Generic[T]):
    """Authentication attempt result.

    Attributes:
        success: Whether authentication was successful.
        user: The authenticated user (if success or MFA required).
        session_id: Created session ID (if using sessions).
        token: Created token (if using tokens).
        error: Error code if authentication failed.
        requires_mfa: True if MFA verification is required.
        mfa_token: Token to use for MFA verification.
    """

    success: bool
    user: T | None = None
    session_id: str | None = None
    token: str | None = None
    error: str | None = None
    requires_mfa: bool = False
    mfa_token: str | None = None


class Authenticator(Generic[T]):
    """Orchestrates the authentication flow.

    Handles user lookup, credential verification, rate limiting,
    MFA, and session/token management.

    Rate limiting is enabled by default to prevent brute force attacks.
    To use a custom rate limiter (e.g., slowapi), disable it with
    `config.rate_limit_enabled = False` and apply the rate limit
    decorator to your login endpoint.

    Example:
        from zerojs.auth import Authenticator, AuthConfig, AuthSessionAdapter
        from zerojs.session import MemorySessionStore

        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)

        auth = Authenticator(
            user_provider=MyUserProvider(),
            credential_verifier=MyPasswordVerifier(),
            session_adapter=sessions,
            config=AuthConfig(rate_limit_max_attempts=3),
        )

        result = await auth.authenticate(
            identifier="user@example.com",
            credential="password123",
            context={"ip": request.client.host},
        )

        if result.success:
            # Set session cookie
            response.set_cookie("session", result.session_id)
        elif result.requires_mfa:
            # Return MFA token to client
            return {"mfa_token": result.mfa_token}
        else:
            # Handle error
            return {"error": result.error}
    """

    def __init__(
        self,
        user_provider: UserProvider[T],
        credential_verifier: CredentialVerifier[T],
        session_adapter: AuthSessionAdapter | None = None,
        token_provider: TokenProvider | None = None,
        mfa_provider: MFAProvider[T] | None = None,
        events: AuthEventEmitter | None = None,
        config: AuthConfig | None = None,
    ):
        """Initialize the authenticator.

        Args:
            user_provider: Provider for user lookup.
            credential_verifier: Verifier for credentials.
            session_adapter: Optional session adapter for session-based auth.
            token_provider: Optional token provider for token-based auth.
            mfa_provider: Optional MFA provider.
            events: Event emitter for auth events.
            config: Configuration options.
        """
        self.users = user_provider
        self.verifier = credential_verifier
        self.sessions = session_adapter
        self.tokens = token_provider
        self.mfa = mfa_provider
        self.events = events or AuthEventEmitter()
        self.config = config or AuthConfig()

    async def authenticate(
        self,
        identifier: str,
        credential: Any,
        session: SessionInterface | None = None,
        remember_me: bool = False,
        context: dict[str, Any] | None = None,
    ) -> AuthResult[T]:
        """Authenticate a user.

        Args:
            identifier: User identifier (email, username, etc.).
            credential: User credential (password, token, etc.).
            session: Request session (from request.state.session).
                If provided, session ID is rotated to prevent fixation.
            remember_me: Use extended TTL for session.
            context: Additional context data (ip, user_agent, etc.).

        Returns:
            AuthResult with success status and user/session/token data.
        """
        ctx = context or {}

        # Check rate limit BEFORE any operation
        if self.config.rate_limit_enabled:
            if await self._is_rate_limited(identifier):
                await self.events.emit(
                    AuthEvent.LOGIN_FAILED,
                    identifier=identifier,
                    reason="rate_limited",
                    **ctx,
                )
                return AuthResult(success=False, error="too_many_attempts")

        # Find user
        user = await self.users.get_by_identifier(identifier)
        if user is None:
            # Dummy verification to prevent timing attacks
            if hasattr(self.verifier, "dummy_verify"):
                self.verifier.dummy_verify()

            await self._record_failed_attempt(identifier)
            await self.events.emit(
                AuthEvent.LOGIN_FAILED,
                identifier=identifier,
                reason="user_not_found",
                **ctx,
            )
            return AuthResult(success=False, error="invalid_credentials")

        # Verify credential
        if not await self.verifier.verify(user, credential):
            await self._record_failed_attempt(identifier)
            await self.events.emit(
                AuthEvent.LOGIN_FAILED,
                identifier=identifier,
                user=user,
                reason="invalid_credential",
                **ctx,
            )
            return AuthResult(success=False, error="invalid_credentials")

        # Check if user account is active
        if not await self.users.is_active(user):
            await self.events.emit(
                AuthEvent.LOGIN_FAILED,
                identifier=identifier,
                user=user,
                reason="account_inactive",
                **ctx,
            )
            return AuthResult(success=False, error="account_inactive")

        # Check MFA if enabled
        if self.mfa and await self.mfa.is_enabled(user):
            mfa_token = await self._create_mfa_token(user, identifier)
            return AuthResult(
                success=False,
                user=user,
                requires_mfa=True,
                mfa_token=mfa_token,
            )

        # Create session/token and rotate session ID to prevent fixation
        return await self._complete_authentication(user, remember_me, ctx, identifier, session)

    async def complete_mfa(
        self,
        mfa_token: str,
        code: str,
        session: SessionInterface | None = None,
        method: str | None = None,
        remember_me: bool = False,
        context: dict[str, Any] | None = None,
    ) -> AuthResult[T]:
        """Complete MFA authentication.

        Args:
            mfa_token: Token from initial authentication.
            code: MFA code entered by user.
            session: Request session for rotation.
            method: MFA method to use (defaults to "totp").
            remember_me: Use extended TTL for session.
            context: Additional context data.

        Returns:
            AuthResult with success status and session/token data.
        """
        ctx = context or {}

        # Verify MFA token and get identifier for rate limit clearing
        user, identifier = await self._verify_mfa_token_with_identifier(mfa_token)
        if user is None:
            return AuthResult(success=False, error="mfa_token_expired")

        if self.mfa is None:
            return AuthResult(success=False, error="mfa_not_configured")

        # Verify code
        if not await self.mfa.verify(user, method or "totp", code):
            await self.events.emit(
                AuthEvent.MFA_CHALLENGE_FAILED,
                user=user,
                method=method,
                **ctx,
            )
            return AuthResult(success=False, error="invalid_mfa_code")

        await self.events.emit(
            AuthEvent.MFA_CHALLENGE_PASSED,
            user=user,
            method=method,
            **ctx,
        )

        # Invalidate MFA token
        await self._invalidate_mfa_token(mfa_token)

        return await self._complete_authentication(user, remember_me, ctx, identifier=identifier, session=session)

    async def logout(
        self,
        session_id: str | None = None,
        token: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Log out the current user.

        Args:
            session_id: Session ID to destroy.
            token: Token to invalidate (if token blacklisting is implemented).
            context: Additional context data.
        """
        ctx = context or {}
        user = AuthContext.user()

        if session_id and self.sessions:
            self.sessions.destroy(session_id)

        # Token invalidation would go here if implemented

        await self.events.emit(AuthEvent.LOGOUT, user=user, **ctx)

    async def _complete_authentication(
        self,
        user: T,
        remember_me: bool,
        ctx: dict[str, Any],
        identifier: str | None = None,
        session: SessionInterface | None = None,
    ) -> AuthResult[T]:
        """Complete authentication by creating session/token.

        Args:
            user: The authenticated user.
            remember_me: Whether to use extended TTL.
            ctx: Context data for events.
            identifier: User identifier for rate limit clearing.
            session: Request session to rotate.

        Returns:
            AuthResult with success=True and session/token data.
        """
        session_id = None
        token = None

        # Clear rate limit on successful login
        if identifier and self.config.rate_limit_enabled:
            await self._clear_rate_limit(identifier)

        # Rotate session ID to prevent session fixation attacks
        if session is not None:
            session.rotate()

        if self.sessions:
            ttl = self.config.remember_me_ttl if remember_me else self.config.session_ttl
            session_id = self.sessions.create(
                user_id=getattr(user, "id", None),
                data={"remember_me": remember_me},
                ttl=ttl,
            )

        if self.tokens:
            token = self.tokens.create({"sub": str(getattr(user, "id", None))})

        await self.events.emit(AuthEvent.LOGIN_SUCCESS, user=user, **ctx)

        return AuthResult(
            success=True,
            user=user,
            session_id=session_id,
            token=token,
        )

    # --- MFA helper methods ---

    async def _create_mfa_token(self, user: T, identifier: str) -> str:
        """Create temporary token for MFA flow.

        Args:
            user: The user requiring MFA.
            identifier: The user identifier (for rate limit clearing).

        Returns:
            MFA token string.

        Raises:
            RuntimeError: If session adapter is not configured.
        """
        if not self.sessions:
            raise RuntimeError("Session adapter required for MFA")

        mfa_token = secrets.token_urlsafe(32)
        # Store with short TTL (5 minutes)
        # Include identifier for rate limit clearing after MFA success
        self.sessions.set_raw(
            f"mfa:{mfa_token}",
            {
                "user_id": getattr(user, "id", None),
                "identifier": identifier,
            },
            300,
        )
        return mfa_token

    async def _verify_mfa_token(self, mfa_token: str) -> T | None:
        """Verify MFA token and return associated user.

        Args:
            mfa_token: The MFA token to verify.

        Returns:
            User if token is valid, None otherwise.
        """
        user, _ = await self._verify_mfa_token_with_identifier(mfa_token)
        return user

    async def _verify_mfa_token_with_identifier(self, mfa_token: str) -> tuple[T | None, str | None]:
        """Verify MFA token and return associated user with identifier.

        Args:
            mfa_token: The MFA token to verify.

        Returns:
            Tuple of (user, identifier). Both are None if token is invalid.
        """
        if not self.sessions:
            return None, None

        data = self.sessions.get_raw(f"mfa:{mfa_token}")
        if not data:
            return None, None

        user_id = data.get("user_id")
        if not user_id:
            return None, None

        identifier = data.get("identifier")
        user = await self.users.get_by_id(user_id)
        return user, identifier

    async def _invalidate_mfa_token(self, mfa_token: str) -> None:
        """Invalidate a used MFA token.

        Args:
            mfa_token: The MFA token to invalidate.
        """
        if self.sessions:
            self.sessions.delete_raw(f"mfa:{mfa_token}")

    # --- Rate limiting helper methods ---

    def _rate_limit_key(self, identifier: str) -> str:
        """Generate key for rate limiting.

        Hashes the identifier to prevent email addresses
        or other PII from appearing in storage keys.

        Args:
            identifier: The user identifier.

        Returns:
            Hashed key for rate limiting storage.
        """
        # SHA256 is intentionally used here for identifier anonymization,
        # NOT for password hashing. Passwords use Argon2id in passwords.py.
        # nosec B324: SHA256 is appropriate for PII obfuscation in storage keys
        hashed = hashlib.sha256(identifier.lower().encode()).hexdigest()[:16]
        return f"rate_limit:{hashed}"

    async def _is_rate_limited(self, identifier: str) -> bool:
        """Check if identifier is blocked by rate limit.

        Args:
            identifier: The user identifier.

        Returns:
            True if rate limited, False otherwise.
        """
        if not self.sessions:
            return False

        key = self._rate_limit_key(identifier)

        # Check lockout first
        lockout = self.sessions.get_raw(f"{key}:locked")
        if lockout and lockout.get("until", 0) > time.time():
            return True

        # Check attempt count
        attempts = self.sessions.get_counter_raw(f"{key}:count")
        if attempts >= self.config.rate_limit_max_attempts:
            return True

        return False

    async def _record_failed_attempt(self, identifier: str) -> None:
        """Record failed login attempt using atomic increment.

        Args:
            identifier: The user identifier.
        """
        if not self.sessions:
            return

        key = self._rate_limit_key(identifier)

        # Atomic increment
        attempts = self.sessions.increment_raw(
            f"{key}:count",
            amount=1,
            ttl=self.config.rate_limit_window,
        )

        # If threshold crossed, set lockout
        if attempts >= self.config.rate_limit_max_attempts:
            self.sessions.set_raw(
                f"{key}:locked",
                {"until": time.time() + self.config.rate_limit_lockout},
                self.config.rate_limit_lockout,
            )

    async def _clear_rate_limit(self, identifier: str) -> None:
        """Clear rate limit after successful login.

        Args:
            identifier: The user identifier.
        """
        if self.sessions:
            key = self._rate_limit_key(identifier)
            self.sessions.delete_raw(f"{key}:count")
            self.sessions.delete_raw(f"{key}:locked")
