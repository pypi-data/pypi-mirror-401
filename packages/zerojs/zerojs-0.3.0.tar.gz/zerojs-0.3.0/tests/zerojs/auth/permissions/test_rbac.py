"""Tests for RBACBackend."""

import asyncio

import pytest

from zerojs.auth.permissions import RBACBackend
from zerojs.auth.testing import MockRoleProvider, MockUser


class TestRBACBackendBasic:
    """Tests for basic RBAC functionality."""

    @pytest.fixture
    def rbac(self) -> RBACBackend:
        """Create RBAC backend with basic roles."""
        rbac = RBACBackend(MockRoleProvider())
        rbac.define_roles(
            {
                "admin": ["*"],
                "editor": ["posts:*", "media:upload"],
                "author": ["posts:create", "posts:edit", "posts:read"],
                "viewer": ["posts:read"],
            }
        )
        return rbac

    def test_admin_has_all_permissions(self, rbac: RBACBackend) -> None:
        """Admin with '*' has all permissions."""

        async def check() -> None:
            admin = MockUser(id=1, email="admin@test.com", roles=["admin"])
            assert await rbac.can(admin, "posts:edit") is True
            assert await rbac.can(admin, "users:delete") is True
            assert await rbac.can(admin, "anything:here") is True

        asyncio.run(check())

    def test_editor_has_posts_wildcard(self, rbac: RBACBackend) -> None:
        """Editor with 'posts:*' has all posts permissions."""

        async def check() -> None:
            editor = MockUser(id=2, email="editor@test.com", roles=["editor"])
            assert await rbac.can(editor, "posts:create") is True
            assert await rbac.can(editor, "posts:edit") is True
            assert await rbac.can(editor, "posts:delete") is True
            assert await rbac.can(editor, "media:upload") is True
            assert await rbac.can(editor, "users:delete") is False

        asyncio.run(check())

    def test_author_has_specific_permissions(self, rbac: RBACBackend) -> None:
        """Author has only specific permissions."""

        async def check() -> None:
            author = MockUser(id=3, email="author@test.com", roles=["author"])
            assert await rbac.can(author, "posts:create") is True
            assert await rbac.can(author, "posts:edit") is True
            assert await rbac.can(author, "posts:read") is True
            assert await rbac.can(author, "posts:delete") is False

        asyncio.run(check())

    def test_viewer_has_read_only(self, rbac: RBACBackend) -> None:
        """Viewer has only read permission."""

        async def check() -> None:
            viewer = MockUser(id=4, email="viewer@test.com", roles=["viewer"])
            assert await rbac.can(viewer, "posts:read") is True
            assert await rbac.can(viewer, "posts:edit") is False
            assert await rbac.can(viewer, "posts:create") is False

        asyncio.run(check())

    def test_no_roles_has_no_permissions(self, rbac: RBACBackend) -> None:
        """User with no roles has no permissions."""

        async def check() -> None:
            user = MockUser(id=5, email="noroles@test.com", roles=[])
            assert await rbac.can(user, "posts:read") is False

        asyncio.run(check())

    def test_unknown_role_has_no_permissions(self, rbac: RBACBackend) -> None:
        """User with unknown role has no permissions."""

        async def check() -> None:
            user = MockUser(id=6, email="unknown@test.com", roles=["unknown"])
            assert await rbac.can(user, "posts:read") is False

        asyncio.run(check())

    def test_multiple_roles_combine(self, rbac: RBACBackend) -> None:
        """User with multiple roles has combined permissions."""

        async def check() -> None:
            user = MockUser(id=7, email="multi@test.com", roles=["viewer", "author"])
            # Has viewer permissions
            assert await rbac.can(user, "posts:read") is True
            # Has author permissions
            assert await rbac.can(user, "posts:create") is True
            assert await rbac.can(user, "posts:edit") is True

        asyncio.run(check())


class TestRBACBackendDefineRole:
    """Tests for role definition methods."""

    def test_define_role_returns_self(self) -> None:
        """define_role returns self for chaining."""
        rbac = RBACBackend(MockRoleProvider())
        result = rbac.define_role("test", ["perm1"])
        assert result is rbac

    def test_define_roles_returns_self(self) -> None:
        """define_roles returns self for chaining."""
        rbac = RBACBackend(MockRoleProvider())
        result = rbac.define_roles({"test": ["perm1"]})
        assert result is rbac

    def test_chaining(self) -> None:
        """Methods can be chained."""
        rbac = (
            RBACBackend(MockRoleProvider())
            .define_role("role1", ["perm1"])
            .define_role("role2", ["perm2"])
            .define_roles({"role3": ["perm3"]})
        )
        assert rbac._role_permissions["role1"] == frozenset(["perm1"])
        assert rbac._role_permissions["role2"] == frozenset(["perm2"])
        assert rbac._role_permissions["role3"] == frozenset(["perm3"])

    def test_redefining_role_overwrites(self) -> None:
        """Redefining a role overwrites previous permissions."""

        async def check() -> None:
            rbac = RBACBackend(MockRoleProvider())
            rbac.define_role("test", ["perm1", "perm2"])
            rbac.define_role("test", ["perm3"])

            user = MockUser(id=1, email="test@test.com", roles=["test"])
            assert await rbac.can(user, "perm1") is False
            assert await rbac.can(user, "perm3") is True

        asyncio.run(check())


class TestRBACBackendCaching:
    """Tests for permission caching."""

    def test_cache_is_cleared_on_define_role(self) -> None:
        """Cache is cleared when roles are defined."""

        async def check() -> None:
            rbac = RBACBackend(MockRoleProvider())
            rbac.define_role("test", ["perm1"])

            user = MockUser(id=1, email="test@test.com", roles=["test"])

            # First check populates cache
            assert await rbac.can(user, "perm1") is True
            assert await rbac.can(user, "perm2") is False

            # Redefine role
            rbac.define_role("test", ["perm2"])

            # Cache should be cleared
            assert await rbac.can(user, "perm1") is False
            assert await rbac.can(user, "perm2") is True

        asyncio.run(check())

    def test_cache_is_cleared_on_define_roles(self) -> None:
        """Cache is cleared when multiple roles are defined."""

        async def check() -> None:
            rbac = RBACBackend(MockRoleProvider())
            rbac.define_roles({"test": ["perm1"]})

            user = MockUser(id=1, email="test@test.com", roles=["test"])
            assert await rbac.can(user, "perm1") is True

            rbac.define_roles({"test": ["perm2"]})
            assert await rbac.can(user, "perm1") is False
            assert await rbac.can(user, "perm2") is True

        asyncio.run(check())
