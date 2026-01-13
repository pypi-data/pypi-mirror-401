"""Permission system with RBAC and ABAC backends.

Provides flexible permission checking through pluggable backends.
Supports both Role-Based Access Control (RBAC) and Attribute-Based
Access Control (ABAC).

Example (RBAC):
    from zerojs.auth.permissions import (
        RBACBackend, RoleProvider, configure_permissions, requires_permission
    )

    class MyRoleProvider:
        async def get_roles(self, user) -> set[str]:
            return set(user.roles)

    rbac = RBACBackend(MyRoleProvider())
    rbac.define_roles({
        "admin": ["*"],
        "editor": ["posts:*"],
        "viewer": ["posts:read"],
    })
    configure_permissions(rbac)

    @requires_permission("posts:edit")
    async def edit_post(post_id: int):
        ...

Example (ABAC):
    from zerojs.auth.permissions import ABACBackend, configure_permissions

    abac = ABACBackend()

    @abac.policy("posts:edit")
    async def can_edit(user, resource_id=None, **ctx):
        return user.is_admin or user.id == resource_id

    configure_permissions(abac)
"""

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, Literal

from ..context import AuthContext
from ..exceptions import PermissionDenied
from .abac import ABACBackend
from .backend import PermissionBackend, configure_permissions, get_backend
from .rbac import RBACBackend, RoleProvider

__all__ = [
    # Backend protocol and configuration
    "PermissionBackend",
    "configure_permissions",
    "get_backend",
    # RBAC
    "RBACBackend",
    "RoleProvider",
    # ABAC
    "ABACBackend",
    # Decorator
    "requires_permission",
    # Helper functions
    "check_permission",
    "require_permission",
]


async def _check_all_permissions(
    backend: PermissionBackend,
    user: Any,
    permissions: tuple[str, ...],
    ctx: dict[str, Any],
) -> str | None:
    """Check that user has all permissions. Returns first denied permission or None."""
    for perm in permissions:
        if not await backend.can(user, perm, **ctx):
            return perm
    return None


async def _check_any_permission(
    backend: PermissionBackend,
    user: Any,
    permissions: tuple[str, ...],
    ctx: dict[str, Any],
) -> bool:
    """Check that user has at least one permission. Returns True if any granted."""
    for perm in permissions:
        if await backend.can(user, perm, **ctx):
            return True
    return False


def _build_context(kwargs: dict[str, Any], resource_param: str | None) -> dict[str, Any]:
    """Build permission context from kwargs, adding resource_id if specified."""
    ctx = dict(kwargs)
    if resource_param and resource_param in kwargs:
        ctx["resource_id"] = kwargs[resource_param]
    return ctx


def requires_permission(
    *permissions: str,
    mode: Literal["all", "any"] = "all",
    resource_param: str | None = None,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator to verify permissions using the configured backend.

    Args:
        *permissions: Required permissions to check.
        mode: "all" requires all permissions (AND), "any" requires at least one (OR).
        resource_param: Name of function parameter containing resource_id for context.

    Returns:
        Decorator that wraps the function with permission checking.

    Raises:
        PermissionDenied: If user lacks required permissions.
        AuthenticationError: If no user is authenticated.

    Examples:
        # Single permission
        @requires_permission("posts:edit")
        async def edit_post(post_id: int):
            ...

        # Multiple permissions (AND - all required)
        @requires_permission("posts:edit", "posts:publish")
        async def edit_and_publish():
            ...

        # Multiple permissions (OR - any one sufficient)
        @requires_permission("posts:edit", "posts:admin", mode="any")
        async def manage_post():
            ...

        # With resource context
        @requires_permission("posts:edit", resource_param="post_id")
        async def edit_post(post_id: int):
            # Backend receives resource_id=post_id in context
            ...
    """

    def decorator(
        fn: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            user: Any = AuthContext.require_user()
            backend = get_backend()
            user_id = getattr(user, "id", None)
            ctx = _build_context(kwargs, resource_param)

            if mode == "all":
                denied_perm = await _check_all_permissions(backend, user, permissions, ctx)
                if denied_perm:
                    raise PermissionDenied(denied_perm, user_id)
            else:  # mode == "any"
                if not await _check_any_permission(backend, user, permissions, ctx):
                    raise PermissionDenied(permissions, user_id, mode="any")

            return await fn(*args, **kwargs)

        return wrapper

    return decorator


async def check_permission(
    user: Any,
    permission: str,
    **context: Any,
) -> bool:
    """Check if user has permission without raising an exception.

    Use this for conditional logic where you need to check permissions
    programmatically without decorators.

    Args:
        user: The user to check permissions for.
        permission: The permission to check.
        **context: Additional context (e.g., resource_id).

    Returns:
        True if user has the permission, False otherwise.

    Example:
        if await check_permission(user, "posts:edit", resource_id=post.id):
            show_edit_button = True
    """
    return await get_backend().can(user, permission, **context)


async def require_permission(
    user: Any,
    permission: str,
    **context: Any,
) -> None:
    """Check permission and raise PermissionDenied if denied.

    Use this when you need to check permissions inline without a decorator.

    Args:
        user: The user to check permissions for.
        permission: The permission to check.
        **context: Additional context (e.g., resource_id).

    Raises:
        PermissionDenied: If user lacks the permission.

    Example:
        await require_permission(user, "posts:edit", resource_id=post.id)
        # Continue with edit logic...
    """
    if not await get_backend().can(user, permission, **context):
        raise PermissionDenied(permission, getattr(user, "id", None))
