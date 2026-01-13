"""Tests for ABACBackend."""

import asyncio
from dataclasses import dataclass

from zerojs.auth.permissions import ABACBackend


@dataclass
class MockUser:
    """Simple user for testing."""

    id: int
    name: str
    is_admin: bool = False


class TestABACBackendBasic:
    """Tests for basic ABAC functionality."""

    def test_exact_policy_match(self) -> None:
        """Exact permission matches policy."""

        async def check() -> None:
            abac = ABACBackend()

            @abac.policy("posts:read")
            async def can_read(user: MockUser, **ctx) -> bool:
                return True

            user = MockUser(id=1, name="Test")
            assert await abac.can(user, "posts:read") is True
            assert await abac.can(user, "posts:edit") is False

        asyncio.run(check())

    def test_policy_receives_context(self) -> None:
        """Policy function receives context kwargs."""

        async def check() -> None:
            abac = ABACBackend()
            received_ctx: dict = {}

            @abac.policy("posts:edit")
            async def can_edit(user: MockUser, **ctx) -> bool:
                received_ctx.update(ctx)
                return ctx.get("resource_id") == 123

            user = MockUser(id=1, name="Test")
            assert await abac.can(user, "posts:edit", resource_id=123) is True
            assert received_ctx == {"resource_id": 123}

            assert await abac.can(user, "posts:edit", resource_id=456) is False

        asyncio.run(check())

    def test_policy_receives_user(self) -> None:
        """Policy function receives user."""

        async def check() -> None:
            abac = ABACBackend()

            @abac.policy("admin:access")
            async def admin_only(user: MockUser, **ctx) -> bool:
                return user.is_admin

            regular = MockUser(id=1, name="Regular", is_admin=False)
            admin = MockUser(id=2, name="Admin", is_admin=True)

            assert await abac.can(regular, "admin:access") is False
            assert await abac.can(admin, "admin:access") is True

        asyncio.run(check())


class TestABACBackendWildcards:
    """Tests for wildcard policies."""

    def test_resource_wildcard(self) -> None:
        """Resource wildcard matches any action on resource."""

        async def check() -> None:
            abac = ABACBackend()

            @abac.policy("posts:*")
            async def posts_policy(user: MockUser, **ctx) -> bool:
                return user.is_admin

            admin = MockUser(id=1, name="Admin", is_admin=True)
            user = MockUser(id=2, name="User", is_admin=False)

            # Admin can do anything with posts
            assert await abac.can(admin, "posts:create") is True
            assert await abac.can(admin, "posts:edit") is True
            assert await abac.can(admin, "posts:delete") is True

            # Regular user cannot
            assert await abac.can(user, "posts:create") is False

            # Other resources are not affected
            assert await abac.can(admin, "users:create") is False

        asyncio.run(check())

    def test_global_wildcard(self) -> None:
        """Global wildcard matches any permission."""

        async def check() -> None:
            abac = ABACBackend()

            @abac.policy("*")
            async def default_policy(user: MockUser, **ctx) -> bool:
                return user.is_admin

            admin = MockUser(id=1, name="Admin", is_admin=True)
            user = MockUser(id=2, name="User", is_admin=False)

            assert await abac.can(admin, "anything:here") is True
            assert await abac.can(admin, "posts:edit") is True
            assert await abac.can(user, "anything:here") is False

        asyncio.run(check())

    def test_exact_takes_precedence_over_wildcard(self) -> None:
        """Exact policy is checked before wildcards."""

        async def check() -> None:
            abac = ABACBackend()

            @abac.policy("posts:read")
            async def can_read(user: MockUser, **ctx) -> bool:
                return True  # Everyone can read

            @abac.policy("posts:*")
            async def posts_policy(user: MockUser, **ctx) -> bool:
                return user.is_admin  # Only admins for other actions

            user = MockUser(id=1, name="User", is_admin=False)

            # Exact match for read
            assert await abac.can(user, "posts:read") is True
            # Wildcard for edit
            assert await abac.can(user, "posts:edit") is False

        asyncio.run(check())

    def test_resource_wildcard_takes_precedence_over_global(self) -> None:
        """Resource wildcard is checked before global wildcard."""

        async def check() -> None:
            abac = ABACBackend()

            @abac.policy("posts:*")
            async def posts_policy(user: MockUser, **ctx) -> bool:
                return True

            @abac.policy("*")
            async def default_policy(user: MockUser, **ctx) -> bool:
                return False

            user = MockUser(id=1, name="User")

            # Resource wildcard matches
            assert await abac.can(user, "posts:edit") is True
            # Global wildcard matches
            assert await abac.can(user, "users:edit") is False

        asyncio.run(check())


class TestABACBackendDefaultDeny:
    """Tests for default deny behavior."""

    def test_default_deny_true(self) -> None:
        """With default_deny=True, unmatched permissions are denied."""

        async def check() -> None:
            abac = ABACBackend(default_deny=True)
            user = MockUser(id=1, name="User")

            # No policies defined
            assert await abac.can(user, "posts:read") is False

        asyncio.run(check())

    def test_default_deny_false(self) -> None:
        """With default_deny=False, unmatched permissions are allowed."""

        async def check() -> None:
            abac = ABACBackend(default_deny=False)
            user = MockUser(id=1, name="User")

            # No policies defined
            assert await abac.can(user, "posts:read") is True

        asyncio.run(check())


class TestABACBackendDefinePolicy:
    """Tests for programmatic policy definition."""

    def test_define_policy(self) -> None:
        """define_policy adds a policy."""

        async def check() -> None:
            abac = ABACBackend()

            async def my_policy(user: MockUser, **ctx) -> bool:
                return True

            abac.define_policy("test:perm", my_policy)

            user = MockUser(id=1, name="User")
            assert await abac.can(user, "test:perm") is True

        asyncio.run(check())

    def test_define_policy_returns_self(self) -> None:
        """define_policy returns self for chaining."""
        abac = ABACBackend()

        async def p1(user, **ctx) -> bool:
            return True

        async def p2(user, **ctx) -> bool:
            return True

        result = abac.define_policy("perm1", p1).define_policy("perm2", p2)
        assert result is abac
