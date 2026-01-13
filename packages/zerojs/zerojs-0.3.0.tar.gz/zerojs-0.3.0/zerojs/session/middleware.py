"""Session middleware with pluggable storage and signed cookies."""

from http.cookies import SimpleCookie
from typing import Any

from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .cookies import SessionCookieManager
from .data import SessionData
from .storage import SessionStore


class SessionInterface(dict):
    """Dict-like interface for session data with rotation support.

    Provides a familiar dict API while tracking modifications and
    supporting session ID rotation.
    """

    def __init__(self, data: dict[str, Any], session_data: SessionData) -> None:
        super().__init__(data)
        self._session_data = session_data
        self._modified = False

    def __setitem__(self, key: str, value: Any) -> None:
        self._modified = True
        super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self._modified = True
        super().__delitem__(key)

    def clear(self) -> None:
        self._modified = True
        super().clear()

    def pop(self, key: str, *args: Any) -> Any:
        self._modified = True
        return super().pop(key, *args)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self._modified = True
        super().update(*args, **kwargs)

    def setdefault(self, key: str, default: Any = None) -> Any:
        if key not in self:
            self._modified = True
        return super().setdefault(key, default)

    def rotate(self) -> None:
        """Mark session for ID rotation.

        Call this after authentication to prevent session fixation attacks.
        """
        self["_rotate"] = True
        self._modified = True

    @property
    def is_modified(self) -> bool:
        """Check if session was modified."""
        return self._modified


class SessionMiddleware:
    """ASGI middleware for session management with pluggable storage.

    Features:
    - Signed session cookies using itsdangerous
    - Pluggable storage backends (memory, file, Redis)
    - Session ID rotation for security
    - Sliding expiration (renews on every request)
    - Absolute expiration (max lifetime from creation)
    """

    def __init__(
        self,
        app: ASGIApp,
        store: SessionStore,
        secret_key: str,
        cookie_name: str = "session",
        max_age: int = 1209600,
        same_site: str = "lax",
        https_only: bool = False,
        path: str = "/",
        salt: str = "zerojs.session",
        absolute_lifetime: int = 0,
    ) -> None:
        """Initialize the session middleware.

        Args:
            app: The ASGI application to wrap.
            store: Session storage backend.
            secret_key: Secret key for signing cookies.
            cookie_name: Name of the session cookie.
            max_age: Session lifetime in seconds (default: 14 days).
            same_site: SameSite cookie attribute ("lax", "strict", "none").
            https_only: Only send cookie over HTTPS.
            path: Cookie path.
            salt: Salt for cookie signing.
            absolute_lifetime: Max session lifetime from creation in seconds.
                0 = disabled (only sliding expiration applies).
        """
        self.app = app
        self.store = store
        self.cookie_manager = SessionCookieManager(secret_key, salt=salt)
        self.cookie_name = cookie_name
        self.max_age = max_age
        self.same_site = same_site
        self.https_only = https_only
        self.path = path
        self.absolute_lifetime = absolute_lifetime

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)

        # Extract and verify session ID from cookie
        session_id, session_data, is_new = self._load_session(connection)

        # Create session interface
        session_interface = SessionInterface(session_data.data.copy(), session_data)

        # Attach to scope state
        scope.setdefault("state", {})
        scope["state"]["session"] = session_interface
        scope["state"]["_session_id"] = session_id
        scope["state"]["_session_is_new"] = is_new

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                # Sync session data back
                session_data.data = dict(session_interface)

                # Handle rotation
                new_session_id = session_id
                if session_data.should_rotate():
                    new_session_id = self._rotate_session(session_id)

                # Save session if modified or new
                if session_interface.is_modified or is_new:
                    session_data.touch()
                    self.store.set(new_session_id, session_data, self.max_age)
                elif not is_new:
                    # Sliding expiration: touch existing sessions on every request
                    self.store.touch(session_id, self.max_age)

                # Set cookie if new session or rotated
                if is_new or new_session_id != session_id:
                    self._set_session_cookie(message, new_session_id)

            await send(message)

        await self.app(scope, receive, send_wrapper)

    def _load_session(self, connection: HTTPConnection) -> tuple[str, SessionData, bool]:
        """Load session from cookie and store.

        Returns:
            Tuple of (session_id, session_data, is_new_session)
        """
        signed_id = connection.cookies.get(self.cookie_name)

        if signed_id:
            session_id = self.cookie_manager.verify_session_id(signed_id, max_age=self.max_age)
            if session_id:
                session_data = self.store.get(session_id)
                if session_data:
                    # Check absolute lifetime
                    if session_data.is_absolutely_expired(self.absolute_lifetime):
                        self.store.delete(session_id)
                    else:
                        return session_id, session_data, False

        # New session
        session_id = self.cookie_manager.generate_session_id()
        session_data = SessionData()
        return session_id, session_data, True

    def _rotate_session(self, old_id: str) -> str:
        """Rotate session ID while preserving data.

        Args:
            old_id: The old session ID to delete.

        Returns:
            New session ID.
        """
        new_id = self.cookie_manager.generate_session_id()
        self.store.delete(old_id)
        return new_id

    def _set_session_cookie(self, message: Message, session_id: str) -> None:
        """Set the session cookie on the response."""
        headers = MutableHeaders(scope=message)
        signed_id = self.cookie_manager.sign_session_id(session_id)

        cookie: SimpleCookie = SimpleCookie()
        cookie[self.cookie_name] = signed_id
        cookie[self.cookie_name]["path"] = self.path
        cookie[self.cookie_name]["max-age"] = str(self.max_age)
        cookie[self.cookie_name]["httponly"] = True
        cookie[self.cookie_name]["samesite"] = self.same_site

        if self.https_only:
            cookie[self.cookie_name]["secure"] = True

        header_value = cookie.output(header="").strip()
        headers.append("set-cookie", header_value)
