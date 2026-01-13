"""Tests for SessionData dataclass."""

import time_machine

from zerojs.session import SessionData


class TestSessionData:
    """Tests for SessionData dataclass."""

    def test_default_values(self) -> None:
        """SessionData has sensible defaults."""
        data = SessionData()
        assert data.data == {}
        assert isinstance(data.created_at, float)
        assert isinstance(data.accessed_at, float)

    def test_custom_data(self) -> None:
        """SessionData stores custom data."""
        data = SessionData(data={"user_id": 123, "username": "test"})
        assert data.data["user_id"] == 123
        assert data.data["username"] == "test"

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_touch_updates_accessed_at(self) -> None:
        """touch() updates accessed_at timestamp."""
        data = SessionData()
        original_accessed_at = data.accessed_at

        with time_machine.travel("2024-01-01 12:05:00", tick=False):
            data.touch()
            assert data.accessed_at > original_accessed_at

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_is_expired_returns_false_within_ttl(self) -> None:
        """is_expired() returns False when within TTL."""
        data = SessionData()
        assert data.is_expired(ttl=3600) is False

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_is_expired_returns_true_after_ttl(self) -> None:
        """is_expired() returns True when TTL exceeded."""
        data = SessionData()

        with time_machine.travel("2024-01-01 13:00:01", tick=False):
            assert data.is_expired(ttl=3600) is True

    def test_is_absolutely_expired_disabled(self) -> None:
        """is_absolutely_expired() returns False when disabled (0)."""
        data = SessionData()
        assert data.is_absolutely_expired(0) is False

    def test_is_absolutely_expired_within_lifetime(self) -> None:
        """is_absolutely_expired() returns False within lifetime."""
        data = SessionData()
        assert data.is_absolutely_expired(3600) is False

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_is_absolutely_expired_after_lifetime(self) -> None:
        """is_absolutely_expired() returns True after lifetime exceeded."""
        data = SessionData()

        with time_machine.travel("2024-01-01 13:00:01", tick=False):
            assert data.is_absolutely_expired(3600) is True

    @time_machine.travel("2024-01-01 12:00:00", tick=False)
    def test_is_absolutely_expired_uses_created_at_not_accessed_at(self) -> None:
        """is_absolutely_expired() checks created_at, not accessed_at."""
        data = SessionData()

        # Touch the session to update accessed_at
        with time_machine.travel("2024-01-01 12:30:00", tick=False):
            data.touch()

        # Session should still be absolutely expired based on created_at
        with time_machine.travel("2024-01-01 13:00:01", tick=False):
            assert data.is_absolutely_expired(3600) is True
            # But sliding expiration should be False (based on accessed_at)
            assert data.is_expired(3600) is False

    def test_to_dict_serialization(self) -> None:
        """to_dict() serializes all fields."""
        data = SessionData(data={"key": "value"})
        result = data.to_dict()

        assert "data" in result
        assert "created_at" in result
        assert "accessed_at" in result
        assert result["data"] == {"key": "value"}

    def test_from_dict_deserialization(self) -> None:
        """from_dict() deserializes correctly."""
        raw = {
            "data": {"user": 1},
            "created_at": 1000.0,
            "accessed_at": 2000.0,
        }
        data = SessionData.from_dict(raw)

        assert data.data == {"user": 1}
        assert data.created_at == 1000.0
        assert data.accessed_at == 2000.0

    def test_from_dict_with_missing_fields(self) -> None:
        """from_dict() handles missing fields with defaults."""
        raw = {"data": {"test": True}}
        data = SessionData.from_dict(raw)

        assert data.data == {"test": True}
        assert isinstance(data.created_at, float)
        assert isinstance(data.accessed_at, float)

    def test_round_trip_serialization(self) -> None:
        """to_dict() and from_dict() round-trip correctly."""
        original = SessionData(data={"nested": {"a": 1, "b": [1, 2, 3]}})
        serialized = original.to_dict()
        restored = SessionData.from_dict(serialized)

        assert restored.data == original.data
        assert restored.created_at == original.created_at
        assert restored.accessed_at == original.accessed_at

    def test_should_rotate_returns_and_clears_flag(self) -> None:
        """should_rotate() returns True and clears flag when set."""
        data = SessionData()

        # Initially False
        assert data.should_rotate() is False

        # After setting flag directly (as middleware does)
        data.data["_rotate"] = True
        assert data.should_rotate() is True

        # Flag should be cleared
        assert data.should_rotate() is False
        assert "_rotate" not in data.data

    def test_rotation_flag_is_serialized(self) -> None:
        """Rotation flag is included in serialization (for middleware)."""
        data = SessionData(data={"user": 1})
        data.data["_rotate"] = True

        serialized = data.to_dict()
        # Flag is in data dict, so it will be serialized
        assert serialized["data"]["_rotate"] is True
