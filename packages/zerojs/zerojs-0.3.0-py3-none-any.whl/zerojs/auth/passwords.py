"""Password hashing utilities.

Provides secure password hashing using Argon2id (recommended) or bcrypt.

Note: These are sync methods because password hashing is CPU-bound.
For high concurrency, run in executor:

    hashed = await asyncio.get_event_loop().run_in_executor(
        None, hasher.hash, password
    )
"""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Abstract base class for password hashers.

    All implementations must provide hash, verify, and needs_rehash.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash the password.

        Args:
            password: Plain text password.

        Returns:
            Hashed password string.
        """
        ...

    @abstractmethod
    def verify(self, password: str, hash: str) -> bool:
        """Verify password against hash.

        Args:
            password: Plain text password to verify.
            hash: Previously hashed password.

        Returns:
            True if password matches hash.
        """
        ...

    @abstractmethod
    def needs_rehash(self, hash: str) -> bool:
        """Check if hash uses outdated parameters.

        Use this to upgrade hashes when parameters change:

            if hasher.needs_rehash(user.password_hash):
                user.password_hash = hasher.hash(password)
                await user.save()

        Args:
            hash: The hash to check.

        Returns:
            True if hash should be regenerated.
        """
        ...

    def dummy_verify(self) -> None:
        """Perform a dummy verification to equalize timing.

        Call this when a user is not found to prevent timing attacks
        that could reveal whether an account exists.

        Default implementation is a no-op. Subclasses should override
        to perform actual dummy hash verification.
        """
        pass


class Argon2Hasher(PasswordHasher):
    """Recommended hasher using Argon2id.

    Argon2id is the winner of the Password Hashing Competition
    and provides excellent resistance against both GPU and
    side-channel attacks.

    Requires: pip install argon2-cffi

    Default parameters follow OWASP recommendations for interactive logins.

    Example:
        hasher = Argon2Hasher()
        hashed = hasher.hash("mypassword")
        assert hasher.verify("mypassword", hashed)
    """

    _dummy_hash: str | None = None

    def __init__(
        self,
        time_cost: int = 3,
        memory_cost: int = 65536,  # 64 MiB
        parallelism: int = 4,
    ):
        """Initialize Argon2 hasher.

        Args:
            time_cost: Number of iterations.
            memory_cost: Memory usage in kibibytes.
            parallelism: Degree of parallelism.
        """
        try:
            import argon2  # type: ignore[import-not-found]
        except ImportError as e:
            raise ImportError("argon2-cffi is required for Argon2Hasher. Install with: pip install argon2-cffi") from e

        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self._hasher = argon2.PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
        )

    def hash(self, password: str) -> str:
        """Hash password using Argon2id."""
        return self._hasher.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        """Verify password against Argon2 hash."""
        import argon2.exceptions  # type: ignore[import-not-found]

        try:
            self._hasher.verify(hash, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        except argon2.exceptions.InvalidHashError:
            return False

    def needs_rehash(self, hash: str) -> bool:
        """Check if hash needs to be regenerated.

        Returns True if the hash was created with different parameters.
        """
        return self._hasher.check_needs_rehash(hash)

    def dummy_verify(self) -> None:
        """Perform dummy verification to prevent timing attacks."""
        import argon2.exceptions  # type: ignore[import-not-found]

        # Lazy init: only compute dummy hash the first time
        if self._dummy_hash is None:
            self._dummy_hash = self.hash("dummy_password_for_timing")
        try:
            self._hasher.verify(self._dummy_hash, "x")
        except argon2.exceptions.VerifyMismatchError:
            pass


class BcryptHasher(PasswordHasher):
    """Alternative hasher using bcrypt.

    Bcrypt is a well-established algorithm that's still secure,
    though Argon2 is generally preferred for new applications.

    Requires: pip install bcrypt

    Example:
        hasher = BcryptHasher(rounds=12)
        hashed = hasher.hash("mypassword")
        assert hasher.verify("mypassword", hashed)
    """

    _dummy_hash: str | None = None

    def __init__(self, rounds: int = 12):
        """Initialize bcrypt hasher.

        Args:
            rounds: Work factor (log2 of iterations). Default 12.
                Higher values are more secure but slower.
                Each increment doubles the computation time.
        """
        try:
            import bcrypt as _bcrypt  # type: ignore[import-not-found]

            self._bcrypt = _bcrypt
        except ImportError as e:
            raise ImportError("bcrypt is required for BcryptHasher. Install with: pip install bcrypt") from e

        self.rounds = rounds

    def hash(self, password: str) -> str:
        """Hash password using bcrypt."""
        return self._bcrypt.hashpw(password.encode(), self._bcrypt.gensalt(rounds=self.rounds)).decode()

    def verify(self, password: str, hash: str) -> bool:
        """Verify password against bcrypt hash."""
        try:
            return self._bcrypt.checkpw(password.encode(), hash.encode())
        except ValueError:
            return False

    def needs_rehash(self, hash: str) -> bool:
        """Check if hash needs to be regenerated.

        Returns True if the hash was created with fewer rounds.
        """
        try:
            # bcrypt hash format: $2b$rounds$salt+hash
            parts = hash.split("$")
            if len(parts) >= 3:
                current_rounds = int(parts[2])
                return current_rounds < self.rounds
        except (ValueError, IndexError):
            pass
        return True  # Invalid hash format, should regenerate

    def dummy_verify(self) -> None:
        """Perform dummy verification to prevent timing attacks."""
        # Lazy init: only compute dummy hash the first time
        if self._dummy_hash is None:
            self._dummy_hash = self.hash("dummy_password_for_timing")
        try:
            self._bcrypt.checkpw(b"x", self._dummy_hash.encode())
        except ValueError:
            pass
