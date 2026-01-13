"""Multi-Factor Authentication manager.

Provides MFAManager for orchestrating MFA flows including
challenge creation, code sending, and verification.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from .protocols import MFAProvider, UserProvider
    from .session_adapter import AuthSessionAdapter

T = TypeVar("T")


@dataclass
class MFAConfig:
    """Configuration for MFA behavior.

    Attributes:
        token_ttl: TTL for MFA tokens in seconds.
        max_attempts: Maximum verification attempts before token invalidation.
    """

    token_ttl: int = 300  # 5 minutes
    max_attempts: int = 5


@dataclass
class MFAChallenge:
    """Pending MFA challenge.

    Attributes:
        token: Temporary token for this MFA challenge.
        method: Selected MFA method (e.g., "totp", "sms", "email").
        available_methods: All available methods for this user.
        expires_in: Seconds until this challenge expires.
    """

    token: str
    method: str
    available_methods: list[str]
    expires_in: int


@dataclass
class MFAResult(Generic[T]):
    """MFA verification result.

    Attributes:
        success: Whether verification succeeded.
        user: The authenticated user (if success).
        error: Error code if verification failed.
    """

    success: bool
    user: T | None = None
    error: str | None = None


class MFAManager(Generic[T]):
    """Manages MFA flow.

    Handles challenge creation, code sending, and verification.

    Example:
        from zerojs.auth import MFAManager, AuthSessionAdapter
        from zerojs.session import MemorySessionStore

        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)

        mfa = MFAManager(
            provider=MyTOTPProvider(),
            session_adapter=sessions,
            token_ttl=300,  # 5 minutes
        )

        # Create challenge after initial login
        challenge = await mfa.create_challenge(user)
        # Returns: MFAChallenge(token="xxx", method="totp", ...)

        # Later, verify the code
        result = await mfa.verify_challenge(
            mfa_token=challenge.token,
            code="123456",
            user_provider=my_user_provider,
        )
        if result.success:
            # Complete login with result.user
            pass
    """

    def __init__(
        self,
        provider: MFAProvider[T],
        session_adapter: AuthSessionAdapter,
        config: MFAConfig | None = None,
    ):
        """Initialize the MFA manager.

        Args:
            provider: MFA provider implementing verification logic.
            session_adapter: Session adapter for storing MFA tokens.
            config: MFA configuration options.
        """
        self.provider = provider
        self.sessions = session_adapter
        self.config = config or MFAConfig()

    async def create_challenge(
        self,
        user: T,
        method: str | None = None,
    ) -> MFAChallenge:
        """Create MFA challenge after initial login.

        Args:
            user: The user requiring MFA.
            method: Preferred MFA method. If None, uses first available.

        Returns:
            MFAChallenge with token and method info.

        Raises:
            ValueError: If no MFA methods are available.
        """
        methods = await self.provider.get_methods(user)
        if not methods:
            raise ValueError("No MFA methods available for user")

        selected = method if method in methods else methods[0]

        # Create temporary token
        mfa_token = secrets.token_urlsafe(32)
        self.sessions.set_raw(
            f"mfa:{mfa_token}",
            {
                "user_id": getattr(user, "id", None),
                "method": selected,
            },
            self.config.token_ttl,
        )

        # Send code if SMS/email (TOTP doesn't need sending)
        if selected in ("sms", "email"):
            await self.provider.send_challenge(user, selected)

        return MFAChallenge(
            token=mfa_token,
            method=selected,
            available_methods=methods,
            expires_in=self.config.token_ttl,
        )

    async def resend_challenge(
        self,
        mfa_token: str,
        user_provider: UserProvider[T],
        method: str | None = None,
    ) -> MFAChallenge | None:
        """Resend MFA challenge or switch to different method.

        Args:
            mfa_token: The existing MFA token.
            user_provider: Provider to load user by ID.
            method: New method to use (optional).

        Returns:
            Updated MFAChallenge, or None if token is invalid.
        """
        data = self.sessions.get_raw(f"mfa:{mfa_token}")
        if not data:
            return None

        user_id = data.get("user_id")
        if not user_id:
            return None

        user = await user_provider.get_by_id(user_id)
        if not user:
            return None

        # Delete old token and create new challenge
        self.sessions.delete_raw(f"mfa:{mfa_token}")
        return await self.create_challenge(user, method)

    async def verify_challenge(
        self,
        mfa_token: str,
        code: str,
        user_provider: UserProvider[T],
    ) -> MFAResult[T]:
        """Verify MFA code.

        Args:
            mfa_token: The MFA token from create_challenge.
            code: The code entered by user.
            user_provider: Provider to load user by ID.

        Returns:
            MFAResult with success status and user if verified.
        """
        data = self.sessions.get_raw(f"mfa:{mfa_token}")
        if not data:
            return MFAResult(success=False, error="mfa_token_expired")

        # Check failed attempts BEFORE any other validation
        attempts_key = f"mfa_attempts:{mfa_token}"
        attempts = self.sessions.get_counter_raw(attempts_key)

        if attempts >= self.config.max_attempts:
            # Invalidate the MFA token completely
            self.sessions.delete_raw(f"mfa:{mfa_token}")
            self.sessions.delete_raw(attempts_key)
            return MFAResult(success=False, error="too_many_attempts")

        user_id = data.get("user_id")
        if not user_id:
            return MFAResult(success=False, error="invalid_mfa_token")

        user = await user_provider.get_by_id(user_id)
        if not user:
            return MFAResult(success=False, error="user_not_found")

        method = data.get("method", "totp")
        if not await self.provider.verify(user, method, code):
            # Increment failed attempts counter
            self.sessions.increment_raw(attempts_key, 1, self.config.token_ttl)
            return MFAResult(success=False, error="invalid_code")

        # Success: clear token and attempts counter
        self.sessions.delete_raw(f"mfa:{mfa_token}")
        self.sessions.delete_raw(attempts_key)

        return MFAResult(success=True, user=user)

    async def get_challenge_info(
        self,
        mfa_token: str,
        user_provider: UserProvider[T],
    ) -> MFAChallenge | None:
        """Get information about an existing challenge.

        Useful for displaying available methods to the user.

        Args:
            mfa_token: The MFA token.
            user_provider: Provider to load user by ID.

        Returns:
            MFAChallenge info, or None if token is invalid.
        """
        data = self.sessions.get_raw(f"mfa:{mfa_token}")
        if not data:
            return None

        user_id = data.get("user_id")
        if not user_id:
            return None

        user = await user_provider.get_by_id(user_id)
        if not user:
            return None

        methods = await self.provider.get_methods(user)
        current_method = data.get("method", "totp")

        return MFAChallenge(
            token=mfa_token,
            method=current_method,
            available_methods=methods,
            expires_in=self.config.token_ttl,  # Approximate, actual may be less
        )

    def invalidate_challenge(self, mfa_token: str) -> None:
        """Invalidate an MFA challenge.

        Use this to cancel a pending MFA challenge.

        Args:
            mfa_token: The MFA token to invalidate.
        """
        self.sessions.delete_raw(f"mfa:{mfa_token}")

    async def get_user_methods(self, user: T) -> list[str]:
        """Get available MFA methods for a user.

        Convenience method to check what methods are available.

        Args:
            user: The user to check.

        Returns:
            List of available method names.
        """
        return await self.provider.get_methods(user)

    async def is_mfa_enabled(self, user: T) -> bool:
        """Check if user has MFA enabled.

        Args:
            user: The user to check.

        Returns:
            True if MFA is enabled for this user.
        """
        return await self.provider.is_enabled(user)


# Re-export MFAProvider for convenience
def __getattr__(name: str) -> Any:
    if name == "MFAProvider":
        from .protocols import MFAProvider

        return MFAProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
