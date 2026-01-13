"""Authentication and authorization exceptions."""

from typing import Any


class AuthError(Exception):
    """Base for authentication/authorization errors."""

    pass


class AuthenticationError(AuthError):
    """User not authenticated."""

    pass


class PermissionDenied(AuthError):
    """Permission denied.

    Attributes:
        permission: The permission(s) that were denied.
        user_id: ID of the user who was denied.
        mode: "all" or "any" for multiple permissions.
    """

    def __init__(
        self,
        permission: str | tuple[str, ...],
        user_id: Any = None,
        mode: str = "all",
    ):
        self.permission = permission
        self.user_id = user_id
        self.mode = mode

        if isinstance(permission, tuple):
            perm_str = f" {mode.upper()} ".join(permission)
            super().__init__(f"Permission denied: ({perm_str})")
        else:
            super().__init__(f"Permission denied: {permission}")


class InvalidCredentials(AuthError):
    """Invalid credentials provided."""

    pass


class AccountLocked(AuthError):
    """Account locked due to too many failed attempts.

    Attributes:
        unlock_at: Unix timestamp when the account will be unlocked.
    """

    def __init__(self, unlock_at: float | None = None):
        self.unlock_at = unlock_at
        super().__init__("Account locked due to too many failed attempts")


class MFARequired(AuthError):
    """MFA verification required to complete authentication.

    Attributes:
        mfa_token: Token to use for MFA verification.
        methods: Available MFA methods (e.g., ["totp", "sms"]).
    """

    def __init__(self, mfa_token: str, methods: list[str]):
        self.mfa_token = mfa_token
        self.methods = methods
        super().__init__("MFA verification required")
