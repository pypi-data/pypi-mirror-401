"""Permission backend protocol and configuration."""

from contextvars import ContextVar
from typing import Any, Protocol


class PermissionBackend(Protocol):
    """Common interface for permission verification.

    Implement this protocol to create custom permission backends.
    The framework provides RBACBackend and ABACBackend implementations.

    Example:
        class MyBackend:
            async def can(self, user: Any, permission: str, **context: Any) -> bool:
                return permission in user.permissions
    """

    async def can(self, user: Any, permission: str, **context: Any) -> bool:
        """Check if user has the permission.

        Args:
            user: The user to check permissions for.
            permission: The permission to check (e.g., "posts:edit").
            **context: Additional context (e.g., resource_id).

        Returns:
            True if user has the permission, False otherwise.
        """
        ...


# Global permission backend (set once at startup)
_permission_backend: ContextVar[PermissionBackend | None] = ContextVar("permission_backend", default=None)


def configure_permissions(backend: PermissionBackend) -> None:
    """Configure the permission backend.

    Call once at application startup before handling requests.

    Example:
        from zerojs.auth.permissions import configure_permissions, RBACBackend

        rbac = RBACBackend(MyRoleProvider())
        rbac.define_roles({"admin": ["*"], "user": ["posts:read"]})
        configure_permissions(rbac)

    Args:
        backend: The permission backend to use.
    """
    _permission_backend.set(backend)


def get_backend() -> PermissionBackend:
    """Get the configured permission backend.

    Raises:
        RuntimeError: If no backend has been configured.

    Returns:
        The configured permission backend.
    """
    backend = _permission_backend.get()
    if backend is None:
        raise RuntimeError("Permission backend not configured. Call configure_permissions() at startup.")
    return backend
