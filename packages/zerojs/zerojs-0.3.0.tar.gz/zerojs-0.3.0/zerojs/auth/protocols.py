"""Authentication protocols (abstract interfaces).

These protocols define the contracts that users must implement
to integrate with the auth system.
"""

from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class UserProvider(Protocol[T]):
    """Protocol for user retrieval.

    Implement this with your user model and database.

    Example:
        class SQLAlchemyUserProvider:
            def __init__(self, session: AsyncSession):
                self.session = session

            async def get_by_identifier(self, identifier: str) -> User | None:
                stmt = select(User).where(
                    (User.email == identifier) | (User.username == identifier)
                )
                result = await self.session.execute(stmt)
                return result.scalar_one_or_none()

            async def get_by_id(self, user_id: int) -> User | None:
                return await self.session.get(User, user_id)
    """

    async def get_by_identifier(self, identifier: str) -> T | None:
        """Find user by email, username, phone, or any identifier.

        Args:
            identifier: The identifier to search for.

        Returns:
            User object if found, None otherwise.
        """
        ...

    async def get_by_id(self, user_id: Any) -> T | None:
        """Find user by ID.

        Args:
            user_id: The user's unique identifier.

        Returns:
            User object if found, None otherwise.
        """
        ...

    async def is_active(self, user: T) -> bool:
        """Check if user account is active and allowed to login.

        Override to implement account suspension, email verification
        requirements, or other activation checks.

        Default implementation returns True (all users are active).

        Args:
            user: The user object to check.

        Returns:
            True if user can login, False otherwise.
        """
        return True


class CredentialVerifier(Protocol[T]):  # type: ignore[misc]
    """Protocol for credential verification.

    Method-agnostic: can verify passwords, magic links, API keys, etc.

    Example (password-based):
        class PasswordVerifier:
            def __init__(self, hasher: PasswordHasher):
                self.hasher = hasher

            async def verify(self, user: User, credential: str) -> bool:
                return self.hasher.verify(credential, user.password_hash)

    Example (magic link):
        class MagicLinkVerifier:
            def __init__(self, token_store: TokenStore):
                self.tokens = token_store

            async def verify(self, user: User, credential: str) -> bool:
                stored = await self.tokens.get(f"magic:{user.id}")
                if stored and secrets.compare_digest(stored, credential):
                    await self.tokens.delete(f"magic:{user.id}")
                    return True
                return False
    """

    async def verify(self, user: T, credential: Any) -> bool:
        """Verify credential against user.

        Args:
            user: The user to verify against.
            credential: The credential to verify (password, token, etc.)

        Returns:
            True if credential is valid, False otherwise.
        """
        ...


class TokenProvider(Protocol):
    """Protocol for token generation and validation.

    Supports JWT, opaque tokens, or any custom token format.

    Example (JWT):
        class JWTTokenProvider:
            def __init__(self, secret: str, algorithm: str = "HS256"):
                self.secret = secret
                self.algorithm = algorithm

            def create(self, payload: dict) -> str:
                return jwt.encode(payload, self.secret, algorithm=self.algorithm)

            def verify(self, token: str) -> dict | None:
                try:
                    return jwt.decode(token, self.secret, algorithms=[self.algorithm])
                except jwt.InvalidTokenError:
                    return None
    """

    def create(self, payload: dict) -> str:
        """Create a token with the given payload.

        Args:
            payload: Data to encode in the token.

        Returns:
            The encoded token string.
        """
        ...

    def verify(self, token: str) -> dict | None:
        """Verify and decode token.

        Args:
            token: The token to verify.

        Returns:
            Decoded payload if valid, None if invalid.
        """
        ...

    def refresh(self, token: str) -> str | None:
        """Refresh a token.

        Args:
            token: The token to refresh.

        Returns:
            New token if renewable, None otherwise.
        """
        ...


class MFAProvider(Protocol[T]):  # type: ignore[misc]
    """Protocol for multi-factor authentication.

    Implement this to add MFA support (TOTP, SMS, email, etc.)

    Example:
        class TOTPProvider:
            async def is_enabled(self, user: User) -> bool:
                return user.totp_secret is not None

            async def get_methods(self, user: User) -> list[str]:
                methods = []
                if user.totp_secret:
                    methods.append("totp")
                if user.phone:
                    methods.append("sms")
                return methods

            async def send_challenge(self, user: User, method: str) -> bool:
                if method == "sms":
                    return await send_sms(user.phone, generate_code())
                return True  # TOTP doesn't need sending

            async def verify(self, user: User, method: str, code: str) -> bool:
                if method == "totp":
                    return pyotp.TOTP(user.totp_secret).verify(code)
                return await verify_sms_code(user.phone, code)
    """

    async def is_enabled(self, user: T) -> bool:
        """Check if user has MFA enabled.

        Args:
            user: The user to check.

        Returns:
            True if MFA is enabled for this user.
        """
        ...

    async def get_methods(self, user: T) -> list[str]:
        """Get available MFA methods for user.

        Args:
            user: The user to check.

        Returns:
            List of method names (e.g., ["totp", "sms", "email"]).
        """
        ...

    async def send_challenge(self, user: T, method: str) -> bool:
        """Send challenge code via SMS/email if applicable.

        For TOTP, this is a no-op that returns True.

        Args:
            user: The user to send challenge to.
            method: The MFA method to use.

        Returns:
            True if challenge was sent successfully.
        """
        ...

    async def verify(self, user: T, method: str, code: str) -> bool:
        """Verify the MFA code.

        Args:
            user: The user to verify.
            method: The MFA method used.
            code: The code entered by the user.

        Returns:
            True if code is valid.
        """
        ...
