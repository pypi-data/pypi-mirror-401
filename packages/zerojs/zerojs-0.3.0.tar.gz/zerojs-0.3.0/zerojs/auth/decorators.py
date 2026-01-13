"""Authentication decorators.

Provides decorators for protecting routes and functions with
authentication requirements.
"""

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from .context import AuthContext


def requires_auth(
    fn: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """Decorator that requires an authenticated user.

    Raises AuthenticationError if no user is authenticated.

    Example:
        @requires_auth
        async def protected_endpoint(request: Request):
            user = AuthContext.user()
            return {"message": f"Hello, {user.name}"}

        @requires_auth
        async def get_profile():
            user = AuthContext.require_user()
            return user.profile
    """

    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        AuthContext.require_user()  # Raises AuthenticationError if no user
        return await fn(*args, **kwargs)

    return wrapper
