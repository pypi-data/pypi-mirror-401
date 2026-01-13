"""Role-Based Access Control (RBAC) backend."""

from functools import lru_cache
from typing import Any, Protocol


class RoleProvider(Protocol):
    """Protocol for providing user roles.

    Implement this to connect RBAC to your user model.

    Example:
        class MyRoleProvider:
            async def get_roles(self, user) -> set[str]:
                return set(user.roles)
    """

    async def get_roles(self, user: Any) -> set[str]:
        """Get roles for a user.

        Args:
            user: The user to get roles for.

        Returns:
            Set of role names the user has.
        """
        ...


class RBACBackend:
    """Role-based access control backend.

    Permissions are assigned to roles, users have roles.
    Supports wildcards: "*" (all), "resource:*" (all actions on resource).

    Example:
        class MyRoleProvider:
            async def get_roles(self, user) -> set[str]:
                return set(user.roles)

        rbac = RBACBackend(MyRoleProvider())
        rbac.define_roles({
            "admin": ["*"],
            "editor": ["posts:*", "media:upload"],
            "author": ["posts:create", "posts:edit", "posts:read"],
            "viewer": ["posts:read"],
        })
        configure_permissions(rbac)

        # Check permission
        if await rbac.can(user, "posts:edit"):
            ...
    """

    def __init__(self, role_provider: RoleProvider):
        """Initialize the RBAC backend.

        Args:
            role_provider: Provider that returns user roles.
        """
        self.role_provider = role_provider
        self._role_permissions: dict[str, frozenset[str]] = {}

    def define_role(self, role: str, permissions: list[str]) -> "RBACBackend":
        """Define permissions for a role.

        Args:
            role: The role name.
            permissions: List of permissions for this role.

        Returns:
            Self for method chaining.
        """
        self._role_permissions[role] = frozenset(permissions)
        self._clear_cache()
        return self

    def define_roles(self, roles: dict[str, list[str]]) -> "RBACBackend":
        """Define multiple roles at once.

        Args:
            roles: Dictionary mapping role names to permission lists.

        Returns:
            Self for method chaining.

        Example:
            rbac.define_roles({
                "admin": ["*"],
                "editor": ["posts:*"],
                "viewer": ["posts:read"],
            })
        """
        for role, permissions in roles.items():
            self._role_permissions[role] = frozenset(permissions)
        self._clear_cache()
        return self

    async def can(self, user: Any, permission: str, **context: Any) -> bool:
        """Check if user has permission via their roles.

        Args:
            user: The user to check.
            permission: The permission to verify.
            **context: Additional context (ignored by RBAC).

        Returns:
            True if user has the permission, False otherwise.
        """
        user_roles = await self.role_provider.get_roles(user)

        for role in user_roles:
            if self._check_permission_cached(role, permission):
                return True
        return False

    @lru_cache(maxsize=1024)
    def _check_permission_cached(self, role: str, permission: str) -> bool:
        """Check permission with cache and wildcard support.

        Args:
            role: The role to check.
            permission: The permission to verify.

        Returns:
            True if role has the permission.
        """
        perms = self._role_permissions.get(role, frozenset())

        # Exact match
        if permission in perms:
            return True

        # Full wildcard ("*" grants all)
        if "*" in perms:
            return True

        # Resource wildcard: "posts:*" matches "posts:edit"
        if ":" in permission:
            resource = permission.split(":")[0]
            if f"{resource}:*" in perms:
                return True

        return False

    def _clear_cache(self) -> None:
        """Clear permission cache when roles are modified."""
        self._check_permission_cached.cache_clear()
