"""Advanced rate limiting for login endpoints.

Provides LoginRateLimiter for combined IP + identifier rate limiting,
integrating with slowapi for fine-grained control.

For basic rate limiting, use the built-in rate limiting in Authenticator.
This module is for advanced use cases requiring IP-based or combined limits.
"""

from __future__ import annotations

import hashlib
import ipaddress
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from starlette.requests import Request


def _is_valid_ip(ip: str) -> bool:
    """Check if string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def _is_ip_in_trusted_proxies(
    client_ip: str,
    trusted_proxies: list[str],
) -> bool:
    """Check if client IP is in the list of trusted proxies."""
    try:
        client_addr = ipaddress.ip_address(client_ip)
    except ValueError:
        return False

    for proxy in trusted_proxies:
        if _matches_proxy(client_ip, client_addr, proxy):
            return True
    return False


def _matches_proxy(
    client_ip: str,
    client_addr: ipaddress.IPv4Address | ipaddress.IPv6Address,
    proxy: str,
) -> bool:
    """Check if client address matches a proxy specification (IP or CIDR)."""
    try:
        if "/" in proxy:
            network = ipaddress.ip_network(proxy, strict=False)
            return client_addr in network
        return client_ip == proxy
    except ValueError:
        return False


def _extract_forwarded_ip(request: Request, fallback: str) -> str:
    """Extract and validate IP from X-Forwarded-For header."""
    forwarded = request.headers.get("x-forwarded-for")
    if not forwarded:
        return fallback

    forwarded_ip = forwarded.split(",")[0].strip()
    return forwarded_ip if _is_valid_ip(forwarded_ip) else fallback


def _get_remote_address(
    request: Request,
    trust_proxy: bool = False,
    trusted_proxies: list[str] | None = None,
) -> str:
    """Get client IP address from request.

    Args:
        request: The Starlette request.
        trust_proxy: Whether to trust X-Forwarded-For header.
        trusted_proxies: List of trusted proxy IPs/CIDRs.

    Returns:
        Client IP address string.

    Security Note:
        Only set trust_proxy=True if your application is behind a
        trusted reverse proxy (nginx, AWS ALB, Cloudflare, etc.)
        that overwrites the X-Forwarded-For header.
    """
    client_ip = request.client.host if request.client else "unknown"

    if client_ip != "unknown" and not _is_valid_ip(client_ip):
        return "invalid"

    if not trust_proxy:
        return client_ip

    if trusted_proxies and not _is_ip_in_trusted_proxies(client_ip, trusted_proxies):
        return client_ip

    return _extract_forwarded_ip(request, client_ip)


@dataclass
class RateLimitConfig:
    """Configuration for LoginRateLimiter.

    Attributes:
        ip_limit: Rate limit string for IP-based limiting (e.g., "10/minute").
        identifier_limit: Rate limit string for identifier-based limiting.
        combined_limit: Rate limit for combined IP+identifier key.
        ip_key_prefix: Prefix for IP-based rate limit keys.
        identifier_key_prefix: Prefix for identifier-based keys.
        combined_key_prefix: Prefix for combined keys.
        trust_proxy: Whether to trust X-Forwarded-For header.
        trusted_proxies: List of trusted proxy IPs/CIDRs (e.g., ["10.0.0.0/8"]).
    """

    ip_limit: str = "10/minute"
    identifier_limit: str = "5/minute"
    combined_limit: str = "3/minute"
    ip_key_prefix: str = "login:ip"
    identifier_key_prefix: str = "login:id"
    combined_key_prefix: str = "login:combined"
    trust_proxy: bool = False
    trusted_proxies: list[str] = field(default_factory=list)


class LoginRateLimiter:
    """Advanced rate limiter for login endpoints.

    Provides three levels of rate limiting:
    1. IP-based: Limits total attempts from an IP address
    2. Identifier-based: Limits attempts per account (email/username)
    3. Combined: Limits attempts for specific IP+account combination

    Integrates with slowapi for production-ready rate limiting.

    Example with slowapi:
        from slowapi import Limiter
        from slowapi.util import get_remote_address
        from zerojs.auth import LoginRateLimiter, RateLimitConfig

        limiter = Limiter(key_func=get_remote_address)

        login_limiter = LoginRateLimiter(
            limiter=limiter,
            config=RateLimitConfig(
                ip_limit="20/minute",
                identifier_limit="5/minute",
                combined_limit="3/minute",
            ),
        )

        @app.post("/login")
        @login_limiter.limit()
        async def login(request: Request, email: str, password: str):
            # Rate limited by IP, email, and IP+email combination
            result = await auth.authenticate(email, password)
            return result

    Example without slowapi (standalone):
        from zerojs.auth import LoginRateLimiter, AuthSessionAdapter
        from zerojs.session import MemorySessionStore

        store = MemorySessionStore()
        sessions = AuthSessionAdapter(store)

        login_limiter = LoginRateLimiter(session_adapter=sessions)

        # Check before authenticating
        if login_limiter.is_limited(request, email):
            return {"error": "too_many_attempts"}

        result = await auth.authenticate(email, password)

        if not result.success:
            login_limiter.record_attempt(request, email)
    """

    def __init__(
        self,
        limiter: Any | None = None,
        session_adapter: Any | None = None,
        config: RateLimitConfig | None = None,
        get_ip: Callable[[Request], str] | None = None,
    ):
        """Initialize the rate limiter.

        Args:
            limiter: Optional slowapi Limiter instance for decorator-based limiting.
            session_adapter: Optional AuthSessionAdapter for standalone mode.
            config: Rate limit configuration.
            get_ip: Custom function to extract IP from request.
        """
        self.limiter = limiter
        self.sessions = session_adapter
        self.config = config or RateLimitConfig()

        if get_ip:
            self.get_ip = get_ip
        else:
            self.get_ip = lambda req: _get_remote_address(
                req,
                trust_proxy=self.config.trust_proxy,
                trusted_proxies=self.config.trusted_proxies,
            )

    def _hash_identifier(self, identifier: str) -> str:
        """Hash identifier to avoid PII in storage keys.

        Args:
            identifier: The user identifier (email, username, etc.)

        Returns:
            Hashed identifier (first 16 chars of SHA256).
        """
        # SHA256 is intentionally used here for identifier anonymization,
        # NOT for password hashing. Passwords use Argon2id in passwords.py.
        # nosec B324: SHA256 is appropriate for PII obfuscation in storage keys
        return hashlib.sha256(identifier.lower().encode()).hexdigest()[:16]

    def ip_key(self, request: Request) -> str:
        """Generate rate limit key for IP address.

        Args:
            request: The Starlette request.

        Returns:
            Rate limit key string.
        """
        ip = self.get_ip(request)
        return f"{self.config.ip_key_prefix}:{ip}"

    def identifier_key(self, identifier: str) -> str:
        """Generate rate limit key for identifier.

        Args:
            identifier: User identifier (email, username, etc.)

        Returns:
            Rate limit key string.
        """
        hashed = self._hash_identifier(identifier)
        return f"{self.config.identifier_key_prefix}:{hashed}"

    def combined_key(self, request: Request, identifier: str) -> str:
        """Generate combined IP+identifier rate limit key.

        This provides the strictest limiting - prevents an attacker
        from trying many passwords on one account from one IP.

        Args:
            request: The Starlette request.
            identifier: User identifier.

        Returns:
            Combined rate limit key string.
        """
        ip = self.get_ip(request)
        hashed = self._hash_identifier(identifier)
        return f"{self.config.combined_key_prefix}:{ip}:{hashed}"

    def limit(
        self,
        identifier_param: str = "email",
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to apply rate limiting to login endpoint.

        Requires slowapi Limiter to be configured.

        Args:
            identifier_param: Name of parameter containing user identifier.

        Returns:
            Decorator function.

        Raises:
            RuntimeError: If slowapi limiter is not configured.

        Example:
            @login_limiter.limit(identifier_param="email")
            async def login(request: Request, email: str, password: str):
                ...
        """
        if self.limiter is None:
            raise RuntimeError(
                "slowapi Limiter required for decorator mode. Pass limiter to LoginRateLimiter or use standalone mode."
            )

        # Store reference for closure (helps mypy understand it's not None)
        limiter = self.limiter

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            # Apply IP limit
            ip_limited = limiter.limit(
                self.config.ip_limit,
                key_func=self.get_ip,
            )(fn)

            @wraps(fn)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Get request and identifier from kwargs
                request = kwargs.get("request")
                identifier = kwargs.get(identifier_param)

                if request and identifier and self.sessions:
                    # Check combined limit using session adapter
                    combined_key = self.combined_key(request, identifier)
                    count = self.sessions.get_counter_raw(combined_key)

                    # Parse limit (e.g., "3/minute" -> 3)
                    max_attempts = int(self.config.combined_limit.split("/")[0])
                    if count >= max_attempts:
                        from starlette.responses import JSONResponse

                        return JSONResponse(
                            {"error": "too_many_attempts", "type": "combined"},
                            status_code=429,
                        )

                return await ip_limited(*args, **kwargs)

            return wrapper

        return decorator

    def is_limited(
        self,
        request: Request,
        identifier: str,
    ) -> bool:
        """Check if request is rate limited (standalone mode).

        Checks all three limits: IP, identifier, and combined.

        Args:
            request: The Starlette request.
            identifier: User identifier.

        Returns:
            True if any limit is exceeded.
        """
        if not self.sessions:
            return False

        # Parse limits
        ip_max = self._parse_limit(self.config.ip_limit)
        id_max = self._parse_limit(self.config.identifier_limit)
        combined_max = self._parse_limit(self.config.combined_limit)

        # Check IP limit
        ip_count = self.sessions.get_counter_raw(self.ip_key(request))
        if ip_count >= ip_max:
            return True

        # Check identifier limit
        id_count = self.sessions.get_counter_raw(self.identifier_key(identifier))
        if id_count >= id_max:
            return True

        # Check combined limit
        combined_count = self.sessions.get_counter_raw(self.combined_key(request, identifier))
        if combined_count >= combined_max:
            return True

        return False

    def record_attempt(
        self,
        request: Request,
        identifier: str,
    ) -> None:
        """Record a failed login attempt (standalone mode).

        Increments all three counters: IP, identifier, and combined.

        Args:
            request: The Starlette request.
            identifier: User identifier.
        """
        if not self.sessions:
            return

        # Get TTL from limit string (e.g., "10/minute" -> 60 seconds)
        ip_ttl = self._parse_ttl(self.config.ip_limit)
        id_ttl = self._parse_ttl(self.config.identifier_limit)
        combined_ttl = self._parse_ttl(self.config.combined_limit)

        # Increment all counters
        self.sessions.increment_raw(self.ip_key(request), 1, ip_ttl)
        self.sessions.increment_raw(self.identifier_key(identifier), 1, id_ttl)
        self.sessions.increment_raw(self.combined_key(request, identifier), 1, combined_ttl)

    def clear_limits(
        self,
        request: Request | None = None,
        identifier: str | None = None,
    ) -> None:
        """Clear rate limits after successful login (standalone mode).

        Args:
            request: The Starlette request (clears IP and combined limits).
            identifier: User identifier (clears identifier and combined limits).
        """
        if not self.sessions:
            return

        if identifier:
            self.sessions.delete_raw(self.identifier_key(identifier))

        if request:
            self.sessions.delete_raw(self.ip_key(request))

        if request and identifier:
            self.sessions.delete_raw(self.combined_key(request, identifier))

    def _parse_limit(self, limit_string: str) -> int:
        """Parse max attempts from limit string.

        Args:
            limit_string: Rate limit string (e.g., "10/minute").

        Returns:
            Maximum number of attempts.
        """
        return int(limit_string.split("/")[0])

    def _parse_ttl(self, limit_string: str) -> int:
        """Parse TTL in seconds from limit string.

        Args:
            limit_string: Rate limit string (e.g., "10/minute").

        Returns:
            TTL in seconds.
        """
        unit = limit_string.split("/")[1].lower()
        ttl_map = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
        }
        return ttl_map.get(unit, 60)

    def get_remaining(
        self,
        request: Request,
        identifier: str,
    ) -> dict[str, int]:
        """Get remaining attempts for each limit type.

        Args:
            request: The Starlette request.
            identifier: User identifier.

        Returns:
            Dictionary with remaining attempts for each limit type.
        """
        if not self.sessions:
            return {"ip": -1, "identifier": -1, "combined": -1}

        ip_max = self._parse_limit(self.config.ip_limit)
        id_max = self._parse_limit(self.config.identifier_limit)
        combined_max = self._parse_limit(self.config.combined_limit)

        ip_count = self.sessions.get_counter_raw(self.ip_key(request))
        id_count = self.sessions.get_counter_raw(self.identifier_key(identifier))
        combined_count = self.sessions.get_counter_raw(self.combined_key(request, identifier))

        return {
            "ip": max(0, ip_max - ip_count),
            "identifier": max(0, id_max - id_count),
            "combined": max(0, combined_max - combined_count),
        }
