"""HTTP exception handlers for authentication errors.

Maps authentication exceptions to appropriate HTTP responses.
Register these handlers on your application for automatic
error handling.

Example:
    from zerojs.auth.handlers import register_auth_exception_handlers

    app = ZeroJS()
    register_auth_exception_handlers(app)
"""

from __future__ import annotations

import time
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from .exceptions import (
    AccountLocked,
    AuthenticationError,
    InvalidCredentials,
    MFARequired,
    PermissionDenied,
)


def authentication_error_handler(
    request: Request,
    exc: AuthenticationError,
) -> JSONResponse:
    """Handle unauthenticated requests.

    Returns 401 Unauthorized with error details.

    Args:
        request: The incoming request.
        exc: The AuthenticationError exception.

    Returns:
        JSONResponse with 401 status code.
    """
    return JSONResponse(
        {
            "error": "authentication_required",
            "message": str(exc),
        },
        status_code=401,
    )


def permission_denied_handler(
    request: Request,
    exc: PermissionDenied,
) -> JSONResponse:
    """Handle unauthorized requests.

    Returns 403 Forbidden with permission details.

    Args:
        request: The incoming request.
        exc: The PermissionDenied exception.

    Returns:
        JSONResponse with 403 status code.
    """
    return JSONResponse(
        {
            "error": "permission_denied",
            "permission": exc.permission,
            "message": str(exc),
        },
        status_code=403,
    )


def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentials,
) -> JSONResponse:
    """Handle invalid login credentials.

    Returns 401 Unauthorized with error details.

    Args:
        request: The incoming request.
        exc: The InvalidCredentials exception.

    Returns:
        JSONResponse with 401 status code.
    """
    return JSONResponse(
        {
            "error": "invalid_credentials",
            "message": str(exc),
        },
        status_code=401,
    )


def account_locked_handler(
    request: Request,
    exc: AccountLocked,
) -> JSONResponse:
    """Handle locked accounts (rate limited).

    Returns 429 Too Many Requests with Retry-After header
    if unlock time is available.

    Args:
        request: The incoming request.
        exc: The AccountLocked exception.

    Returns:
        JSONResponse with 429 status code.
    """
    headers: dict[str, str] = {}

    if exc.unlock_at:
        retry_after = int(exc.unlock_at - time.time())
        if retry_after > 0:
            headers["Retry-After"] = str(retry_after)

    return JSONResponse(
        {
            "error": "account_locked",
            "message": str(exc),
            "unlock_at": exc.unlock_at,
        },
        status_code=429,
        headers=headers,
    )


def mfa_required_handler(
    request: Request,
    exc: MFARequired,
) -> JSONResponse:
    """Handle MFA required responses.

    Returns 401 Unauthorized with MFA token and available methods.

    Args:
        request: The incoming request.
        exc: The MFARequired exception.

    Returns:
        JSONResponse with 401 status code and MFA details.
    """
    return JSONResponse(
        {
            "error": "mfa_required",
            "mfa_token": exc.mfa_token,
            "methods": exc.methods,
            "message": str(exc),
        },
        status_code=401,
    )


def register_auth_exception_handlers(app: Any) -> None:
    """Register all auth exception handlers on the app.

    This is a convenience function to register all authentication
    exception handlers at once.

    Args:
        app: The Starlette/FastAPI/ZeroJS application instance.

    Example:
        from zerojs.auth.handlers import register_auth_exception_handlers

        app = ZeroJS()
        register_auth_exception_handlers(app)

    Exception to HTTP mapping:
        - AuthenticationError -> 401 Unauthorized
        - InvalidCredentials -> 401 Unauthorized
        - MFARequired -> 401 Unauthorized (with mfa_token)
        - PermissionDenied -> 403 Forbidden
        - AccountLocked -> 429 Too Many Requests
    """
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(PermissionDenied, permission_denied_handler)
    app.add_exception_handler(InvalidCredentials, invalid_credentials_handler)
    app.add_exception_handler(AccountLocked, account_locked_handler)
    app.add_exception_handler(MFARequired, mfa_required_handler)
