"""Secure session cookie management with itsdangerous signing."""

import secrets

from itsdangerous import BadSignature, URLSafeTimedSerializer


class SessionCookieManager:
    """Manages signed session cookies using itsdangerous.

    Session IDs are signed with a timestamp, allowing both integrity
    verification and time-based expiration checking.
    """

    def __init__(self, secret_key: str, salt: str = "zerojs.session") -> None:
        """Initialize the cookie manager.

        Args:
            secret_key: Secret key for signing session IDs.
            salt: Salt for the serializer (default: "zerojs.session").
        """
        self._serializer = URLSafeTimedSerializer(secret_key)
        self._salt = salt

    def generate_session_id(self) -> str:
        """Generate a cryptographically secure session ID.

        Returns:
            A URL-safe random string (43 characters).
        """
        return secrets.token_urlsafe(32)

    def sign_session_id(self, session_id: str) -> str:
        """Sign a session ID for cookie storage.

        The signed value includes a timestamp for time-based verification.

        Args:
            session_id: The session ID to sign.

        Returns:
            Signed session ID string (URL-safe).
        """
        return self._serializer.dumps(session_id, salt=self._salt)

    def verify_session_id(self, signed_id: str, max_age: int | None = None) -> str | None:
        """Verify and extract session ID from a signed cookie value.

        Args:
            signed_id: The signed session ID from the cookie.
            max_age: Maximum age in seconds. If provided, signatures older
                     than this will be rejected.

        Returns:
            The original session ID if valid, None if invalid or expired.
        """
        try:
            return self._serializer.loads(signed_id, salt=self._salt, max_age=max_age)
        except BadSignature:
            return None
