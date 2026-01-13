"""Tests for permission decorators and helper functions."""

import asyncio

import pytest

from zerojs.auth import AuthContext, AuthenticationError, PermissionDenied
from zerojs.auth.permissions import (
    RBACBackend,
    check_permission,
    configure_permissions,
    get_backend,
    require_permission,
    requires_permission,
)
from zerojs.auth.testing import MockRoleProvider, MockUser


@pytest.fixture
def rbac() -> RBACBackend:
    """Create and configure RBAC backend."""
    rbac = RBACBackend(MockRoleProvider())
    rbac.define_roles(
        {
            "admin": ["*"],
            "editor": ["posts:edit", "posts:create"],
            "viewer": ["posts:read"],
        }
    )
    configure_permissions(rbac)
    return rbac


class TestConfigurePermissions:
    """Tests for configure_permissions and get_backend."""

    def test_get_backend_raises_without_config(self) -> None:
        """get_backend raises RuntimeError if not configured."""
        # Clear the backend
        from zerojs.auth.permissions.backend import _permission_backend

        _permission_backend.set(None)

        with pytest.raises(RuntimeError, match="Permission backend not configured"):
            get_backend()

    def test_get_backend_returns_configured(self, rbac: RBACBackend) -> None:
        """get_backend returns configured backend."""
        assert get_backend() is rbac


class TestRequiresPermissionDecorator:
    """Tests for @requires_permission decorator."""

    def test_allows_with_permission(self, rbac: RBACBackend) -> None:
        """Decorator allows access when user has permission."""

        async def check() -> None:
            @requires_permission("posts:read")
            async def view_posts() -> str:
                return "success"

            user = MockUser(id=1, email="viewer@test.com", roles=["viewer"])
            with AuthContext.as_user(user):
                result = await view_posts()
                assert result == "success"

        asyncio.run(check())

    def test_denies_without_permission(self, rbac: RBACBackend) -> None:
        """Decorator denies access when user lacks permission."""

        async def check() -> None:
            @requires_permission("posts:edit")
            async def edit_posts() -> str:
                return "success"

            user = MockUser(id=1, email="viewer@test.com", roles=["viewer"])
            with AuthContext.as_user(user):
                with pytest.raises(PermissionDenied) as exc_info:
                    await edit_posts()
                assert exc_info.value.permission == "posts:edit"

        asyncio.run(check())

    def test_requires_authentication(self, rbac: RBACBackend) -> None:
        """Decorator raises AuthenticationError when no user."""

        async def check() -> None:
            @requires_permission("posts:read")
            async def view_posts() -> str:
                return "success"

            with AuthContext.as_user(None):
                with pytest.raises(AuthenticationError):
                    await view_posts()

        asyncio.run(check())

    def test_multiple_permissions_all_mode(self, rbac: RBACBackend) -> None:
        """mode='all' requires all permissions."""

        async def check() -> None:
            @requires_permission("posts:edit", "posts:create", mode="all")
            async def edit_and_create() -> str:
                return "success"

            editor = MockUser(id=1, email="editor@test.com", roles=["editor"])
            viewer = MockUser(id=2, email="viewer@test.com", roles=["viewer"])

            with AuthContext.as_user(editor):
                result = await edit_and_create()
                assert result == "success"

            with AuthContext.as_user(viewer):
                with pytest.raises(PermissionDenied):
                    await edit_and_create()

        asyncio.run(check())

    def test_multiple_permissions_any_mode(self, rbac: RBACBackend) -> None:
        """mode='any' requires at least one permission."""

        async def check() -> None:
            @requires_permission("posts:edit", "posts:read", mode="any")
            async def edit_or_read() -> str:
                return "success"

            editor = MockUser(id=1, email="editor@test.com", roles=["editor"])
            viewer = MockUser(id=2, email="viewer@test.com", roles=["viewer"])
            nobody = MockUser(id=3, email="nobody@test.com", roles=[])

            with AuthContext.as_user(editor):
                result = await edit_or_read()
                assert result == "success"

            with AuthContext.as_user(viewer):
                result = await edit_or_read()
                assert result == "success"

            with AuthContext.as_user(nobody):
                with pytest.raises(PermissionDenied) as exc_info:
                    await edit_or_read()
                assert exc_info.value.mode == "any"

        asyncio.run(check())

    def test_resource_param_passes_context(self, rbac: RBACBackend) -> None:
        """resource_param passes parameter as resource_id in context."""

        async def check() -> None:
            received_ctx: dict = {}

            # Create ABAC backend to capture context
            from zerojs.auth.permissions import ABACBackend

            abac = ABACBackend()

            @abac.policy("posts:edit")
            async def can_edit(user, resource_id=None, **ctx) -> bool:
                received_ctx["resource_id"] = resource_id
                return True

            configure_permissions(abac)

            @requires_permission("posts:edit", resource_param="post_id")
            async def edit_post(post_id: int) -> str:
                return "success"

            user = MockUser(id=1, email="user@test.com")
            with AuthContext.as_user(user):
                await edit_post(post_id=123)
                assert received_ctx["resource_id"] == 123

        asyncio.run(check())

    def test_preserves_function_metadata(self, rbac: RBACBackend) -> None:
        """Decorator preserves function name and docstring."""

        @requires_permission("posts:read")
        async def view_posts() -> str:
            """View all posts."""
            return "success"

        assert view_posts.__name__ == "view_posts"
        assert view_posts.__doc__ == "View all posts."


class TestCheckPermission:
    """Tests for check_permission helper."""

    def test_returns_true_with_permission(self, rbac: RBACBackend) -> None:
        """check_permission returns True when user has permission."""

        async def check() -> None:
            user = MockUser(id=1, email="editor@test.com", roles=["editor"])
            assert await check_permission(user, "posts:edit") is True

        asyncio.run(check())

    def test_returns_false_without_permission(self, rbac: RBACBackend) -> None:
        """check_permission returns False when user lacks permission."""

        async def check() -> None:
            user = MockUser(id=1, email="viewer@test.com", roles=["viewer"])
            assert await check_permission(user, "posts:edit") is False

        asyncio.run(check())

    def test_passes_context(self, rbac: RBACBackend) -> None:
        """check_permission passes context to backend."""

        async def check() -> None:
            from zerojs.auth.permissions import ABACBackend

            abac = ABACBackend()

            @abac.policy("posts:edit")
            async def can_edit(user, resource_id=None, **ctx) -> bool:
                return resource_id == 123

            configure_permissions(abac)

            user = MockUser(id=1, email="user@test.com")
            assert await check_permission(user, "posts:edit", resource_id=123) is True
            assert await check_permission(user, "posts:edit", resource_id=456) is False

        asyncio.run(check())


class TestRequirePermission:
    """Tests for require_permission helper."""

    def test_passes_with_permission(self, rbac: RBACBackend) -> None:
        """require_permission passes when user has permission."""

        async def check() -> None:
            user = MockUser(id=1, email="editor@test.com", roles=["editor"])
            await require_permission(user, "posts:edit")  # Should not raise

        asyncio.run(check())

    def test_raises_without_permission(self, rbac: RBACBackend) -> None:
        """require_permission raises PermissionDenied when user lacks permission."""

        async def check() -> None:
            user = MockUser(id=1, email="viewer@test.com", roles=["viewer"])
            with pytest.raises(PermissionDenied) as exc_info:
                await require_permission(user, "posts:edit")
            assert exc_info.value.permission == "posts:edit"
            assert exc_info.value.user_id == 1

        asyncio.run(check())

    def test_passes_context(self, rbac: RBACBackend) -> None:
        """require_permission passes context to backend."""

        async def check() -> None:
            from zerojs.auth.permissions import ABACBackend

            abac = ABACBackend()

            @abac.policy("posts:edit")
            async def can_edit(user, resource_id=None, **ctx) -> bool:
                return resource_id == 123

            configure_permissions(abac)

            user = MockUser(id=1, email="user@test.com")
            await require_permission(user, "posts:edit", resource_id=123)  # Should pass

            with pytest.raises(PermissionDenied):
                await require_permission(user, "posts:edit", resource_id=456)

        asyncio.run(check())
