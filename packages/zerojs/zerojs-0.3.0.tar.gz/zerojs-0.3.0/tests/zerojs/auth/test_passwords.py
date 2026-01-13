"""Tests for password hashers."""

import pytest

from zerojs.auth import Argon2Hasher, BcryptHasher, PasswordHasher


class TestPasswordHasherInterface:
    """Tests for PasswordHasher interface."""

    def test_argon2_is_password_hasher(self) -> None:
        """Argon2Hasher is a PasswordHasher."""
        assert issubclass(Argon2Hasher, PasswordHasher)

    def test_bcrypt_is_password_hasher(self) -> None:
        """BcryptHasher is a PasswordHasher."""
        assert issubclass(BcryptHasher, PasswordHasher)


class TestArgon2Hasher:
    """Tests for Argon2Hasher."""

    @pytest.fixture
    def hasher(self) -> Argon2Hasher:
        """Create Argon2Hasher with fast parameters for tests."""
        return Argon2Hasher(time_cost=1, memory_cost=1024, parallelism=1)

    def test_hash_returns_string(self, hasher: Argon2Hasher) -> None:
        """hash() returns a string."""
        result = hasher.hash("password")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_hash_is_different_each_time(self, hasher: Argon2Hasher) -> None:
        """hash() generates unique hashes due to random salt."""
        hash1 = hasher.hash("password")
        hash2 = hasher.hash("password")
        assert hash1 != hash2

    def test_verify_correct_password(self, hasher: Argon2Hasher) -> None:
        """verify() returns True for correct password."""
        hashed = hasher.hash("mypassword")
        assert hasher.verify("mypassword", hashed) is True

    def test_verify_wrong_password(self, hasher: Argon2Hasher) -> None:
        """verify() returns False for wrong password."""
        hashed = hasher.hash("mypassword")
        assert hasher.verify("wrongpassword", hashed) is False

    def test_verify_invalid_hash(self, hasher: Argon2Hasher) -> None:
        """verify() returns False for invalid hash."""
        assert hasher.verify("password", "invalid_hash") is False

    def test_needs_rehash_same_params(self, hasher: Argon2Hasher) -> None:
        """needs_rehash() returns False for same parameters."""
        hashed = hasher.hash("password")
        assert hasher.needs_rehash(hashed) is False

    def test_needs_rehash_different_params(self) -> None:
        """needs_rehash() returns True for different parameters."""
        old_hasher = Argon2Hasher(time_cost=1, memory_cost=1024, parallelism=1)
        new_hasher = Argon2Hasher(time_cost=2, memory_cost=2048, parallelism=1)

        hashed = old_hasher.hash("password")
        assert new_hasher.needs_rehash(hashed) is True

    def test_custom_parameters(self) -> None:
        """Custom parameters are used."""
        hasher = Argon2Hasher(time_cost=2, memory_cost=8192, parallelism=2)
        assert hasher.time_cost == 2
        assert hasher.memory_cost == 8192
        assert hasher.parallelism == 2


class TestBcryptHasher:
    """Tests for BcryptHasher."""

    @pytest.fixture
    def hasher(self) -> BcryptHasher:
        """Create BcryptHasher with fast rounds for tests."""
        return BcryptHasher(rounds=4)

    def test_hash_returns_string(self, hasher: BcryptHasher) -> None:
        """hash() returns a string."""
        result = hasher.hash("password")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_hash_is_different_each_time(self, hasher: BcryptHasher) -> None:
        """hash() generates unique hashes due to random salt."""
        hash1 = hasher.hash("password")
        hash2 = hasher.hash("password")
        assert hash1 != hash2

    def test_verify_correct_password(self, hasher: BcryptHasher) -> None:
        """verify() returns True for correct password."""
        hashed = hasher.hash("mypassword")
        assert hasher.verify("mypassword", hashed) is True

    def test_verify_wrong_password(self, hasher: BcryptHasher) -> None:
        """verify() returns False for wrong password."""
        hashed = hasher.hash("mypassword")
        assert hasher.verify("wrongpassword", hashed) is False

    def test_verify_invalid_hash(self, hasher: BcryptHasher) -> None:
        """verify() returns False for invalid hash."""
        assert hasher.verify("password", "invalid_hash") is False

    def test_needs_rehash_same_rounds(self, hasher: BcryptHasher) -> None:
        """needs_rehash() returns False for same rounds."""
        hashed = hasher.hash("password")
        assert hasher.needs_rehash(hashed) is False

    def test_needs_rehash_fewer_rounds(self) -> None:
        """needs_rehash() returns True when rounds increased."""
        old_hasher = BcryptHasher(rounds=4)
        new_hasher = BcryptHasher(rounds=6)

        hashed = old_hasher.hash("password")
        assert new_hasher.needs_rehash(hashed) is True

    def test_needs_rehash_invalid_hash(self, hasher: BcryptHasher) -> None:
        """needs_rehash() returns True for invalid hash."""
        assert hasher.needs_rehash("invalid") is True

    def test_custom_rounds(self) -> None:
        """Custom rounds are used."""
        hasher = BcryptHasher(rounds=10)
        assert hasher.rounds == 10
