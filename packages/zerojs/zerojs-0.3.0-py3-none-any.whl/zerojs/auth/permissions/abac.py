"""Attribute-Based Access Control (ABAC) backend."""

from collections.abc import Awaitable, Callable
from typing import Any


class ABACBackend:
    """Attribute-based access control backend.

    Each permission is defined as an async function that receives
    the user and context, returning True if access is granted.

    Supports wildcards for fallback policies:
    - "resource:*" matches any action on that resource
    - "*" matches any permission (global fallback)

    Example:
        abac = ABACBackend()

        @abac.policy("posts:read")
        async def can_read(user, **ctx):
            return True  # Everyone can read

        @abac.policy("posts:edit")
        async def can_edit(user, resource_id=None, **ctx):
            if user.is_admin:
                return True
            if resource_id:
                post = await posts_repo.get(resource_id)
                return post and post.author_id == user.id
            return False

        @abac.policy("*")
        async def default_policy(user, **ctx):
            return user.is_admin  # Admins can do anything

        configure_permissions(abac)
    """

    def __init__(self, default_deny: bool = True):
        """Initialize the ABAC backend.

        Args:
            default_deny: If True, deny access when no policy matches.
                If False, allow access when no policy matches.
                Default is True (secure by default).
        """
        self._policies: dict[str, Callable[..., Awaitable[bool]]] = {}
        self._default_deny = default_deny

    def policy(self, permission: str) -> Callable[[Callable[..., Awaitable[bool]]], Callable[..., Awaitable[bool]]]:
        """Decorator to define a policy for a permission.

        Args:
            permission: The permission this policy handles.

        Returns:
            Decorator that registers the policy function.

        Example:
            @abac.policy("posts:edit")
            async def can_edit(user, resource_id=None, **ctx):
                return user.id == resource_id
        """

        def decorator(
            fn: Callable[..., Awaitable[bool]],
        ) -> Callable[..., Awaitable[bool]]:
            self._policies[permission] = fn
            return fn

        return decorator

    def define_policy(
        self,
        permission: str,
        check: Callable[..., Awaitable[bool]],
    ) -> "ABACBackend":
        """Define a policy programmatically.

        Args:
            permission: The permission this policy handles.
            check: Async function that checks the permission.

        Returns:
            Self for method chaining.

        Example:
            abac.define_policy(
                "posts:read",
                lambda user, **ctx: True
            )
        """
        self._policies[permission] = check
        return self

    async def can(self, user: Any, permission: str, **context: Any) -> bool:
        """Execute the corresponding policy.

        Tries policies in order:
        1. Exact match (e.g., "posts:edit")
        2. Resource wildcard (e.g., "posts:*")
        3. Global wildcard ("*")
        4. Default (deny if default_deny=True)

        Args:
            user: The user to check.
            permission: The permission to verify.
            **context: Additional context passed to the policy.

        Returns:
            True if access is granted, False otherwise.
        """
        # Try exact match
        policy = self._policies.get(permission)

        # Try resource wildcard
        if policy is None and ":" in permission:
            resource = permission.split(":")[0]
            policy = self._policies.get(f"{resource}:*")

        # Fallback to global wildcard
        if policy is None:
            policy = self._policies.get("*")

        # No policy found
        if policy is None:
            return not self._default_deny

        return await policy(user, **context)
