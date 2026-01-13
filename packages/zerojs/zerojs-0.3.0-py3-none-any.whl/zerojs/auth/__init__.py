"""ZeroJS Authentication System.

An agnostic authentication and authorization system that provides
well-defined abstractions and reusable primitives, allowing developers
to connect the pieces without the framework being opinionated about
database, login method, or authorization strategy.
"""

from .authenticator import AuthConfig, Authenticator, AuthResult
from .context import AuthContext
from .decorators import requires_auth
from .events import AuthEvent, AuthEventEmitter, ListenerConfig
from .exceptions import (
    AccountLocked,
    AuthenticationError,
    AuthError,
    InvalidCredentials,
    MFARequired,
    PermissionDenied,
)
from .handlers import register_auth_exception_handlers
from .mfa import MFAChallenge, MFAConfig, MFAManager, MFAResult
from .middleware import AuthMiddleware
from .passwords import Argon2Hasher, BcryptHasher, PasswordHasher
from .permissions import (
    ABACBackend,
    PermissionBackend,
    RBACBackend,
    RoleProvider,
    check_permission,
    configure_permissions,
    get_backend,
    require_permission,
    requires_permission,
)
from .protocols import CredentialVerifier, MFAProvider, TokenProvider, UserProvider
from .rate_limit import LoginRateLimiter, RateLimitConfig
from .session_adapter import AuthSessionAdapter
from .testing import (
    MockCredentialVerifier,
    MockMFAProvider,
    MockRoleProvider,
    MockSessionStore,
    MockUser,
    MockUserProvider,
    mock_impersonation,
    mock_user,
)
from .tokens import SecureToken

__all__ = [
    # Authenticator
    "Authenticator",
    "AuthConfig",
    "AuthResult",
    # Context
    "AuthContext",
    # Decorators
    "requires_auth",
    # Events
    "AuthEvent",
    "AuthEventEmitter",
    "ListenerConfig",
    # Handlers
    "register_auth_exception_handlers",
    # Middleware
    "AuthMiddleware",
    # MFA
    "MFAManager",
    "MFAConfig",
    "MFAChallenge",
    "MFAResult",
    # Exceptions
    "AuthError",
    "AuthenticationError",
    "PermissionDenied",
    "InvalidCredentials",
    "AccountLocked",
    "MFARequired",
    # Protocols
    "UserProvider",
    "CredentialVerifier",
    "TokenProvider",
    "MFAProvider",
    # Passwords
    "PasswordHasher",
    "Argon2Hasher",
    "BcryptHasher",
    # Tokens
    "SecureToken",
    # Session
    "AuthSessionAdapter",
    # Permissions
    "PermissionBackend",
    "RBACBackend",
    "RoleProvider",
    "ABACBackend",
    "configure_permissions",
    "get_backend",
    "requires_permission",
    "check_permission",
    "require_permission",
    # Rate Limiting
    "LoginRateLimiter",
    "RateLimitConfig",
    # Testing Utilities
    "MockUser",
    "MockUserProvider",
    "MockCredentialVerifier",
    "MockSessionStore",
    "MockMFAProvider",
    "MockRoleProvider",
    "mock_user",
    "mock_impersonation",
]
