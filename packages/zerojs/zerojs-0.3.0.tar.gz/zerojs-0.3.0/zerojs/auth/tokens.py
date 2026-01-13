"""Secure token generation utilities.

Provides utilities for generating various types of secure tokens:
- Random URL-safe tokens
- Numeric OTP codes
- Signed timed tokens (for password reset, magic links, etc.)
"""

import base64
import hashlib
import hmac
import json
import secrets
import time


class SecureToken:
    """Utilities for secure token generation.

    All methods are static - no instance needed.

    Example:
        # Random token
        token = SecureToken.generate()

        # Numeric OTP
        otp = SecureToken.generate_numeric(6)  # "847293"

        # Signed token with expiration
        reset_token = SecureToken.generate_timed(
            data=user_id,
            secret=SECRET_KEY,
            ttl=3600,  # 1 hour
        )

        # Verify signed token
        user_id = SecureToken.verify_timed(reset_token, SECRET_KEY)
        if user_id is None:
            # Token invalid or expired
            pass
    """

    @staticmethod
    def generate(length: int = 32) -> str:
        """Generate random URL-safe token.

        Args:
            length: Number of random bytes. Result will be longer
                due to base64 encoding (~1.33x).

        Returns:
            URL-safe base64 encoded random string.
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_numeric(length: int = 6) -> str:
        """Generate numeric code for OTP.

        Args:
            length: Number of digits.

        Returns:
            Numeric string of specified length.
        """
        return "".join(secrets.choice("0123456789") for _ in range(length))

    @staticmethod
    def generate_timed(
        data: str,
        secret: str,
        ttl: int,
    ) -> str:
        """Generate signed token with expiration.

        Use for password reset links, magic links, email verification, etc.

        The token includes:
        - The data (e.g., user ID)
        - Expiration timestamp
        - HMAC-SHA256 signature

        Args:
            data: Data to sign (can contain any character).
            secret: Secret key for signing.
            ttl: Time-to-live in seconds.

        Returns:
            URL-safe base64 encoded signed token.
        """
        expires = int(time.time()) + ttl

        # Create payload and sign it
        payload = json.dumps({"d": data, "e": expires}, separators=(",", ":"))
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Combine payload with signature
        token_data = json.dumps(
            {"d": data, "e": expires, "s": signature},
            separators=(",", ":"),
        )
        return base64.urlsafe_b64encode(token_data.encode()).decode()

    @staticmethod
    def verify_timed(token: str, secret: str) -> str | None:
        """Verify signed token and return data.

        Args:
            token: The token to verify.
            secret: Secret key used for signing.

        Returns:
            Original data if valid and not expired, None otherwise.
        """
        try:
            decoded = base64.urlsafe_b64decode(token.encode()).decode()
            token_data = json.loads(decoded)

            data = token_data.get("d")
            expires = token_data.get("e")
            signature = token_data.get("s")

            # Check required fields
            if not all([data is not None, expires is not None, signature]):
                return None

            # Check expiration
            if time.time() > expires:
                return None

            # Recalculate signature over payload (without signature field)
            payload = json.dumps({"d": data, "e": expires}, separators=(",", ":"))
            expected = hmac.new(
                secret.encode(),
                payload.encode(),
                hashlib.sha256,
            ).hexdigest()

            # Constant-time comparison to prevent timing attacks
            if not secrets.compare_digest(signature, expected):
                return None

            return data
        except ValueError:
            return None
