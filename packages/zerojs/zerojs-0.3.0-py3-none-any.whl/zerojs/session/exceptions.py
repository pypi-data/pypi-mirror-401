"""Session-specific exceptions."""


class SessionError(Exception):
    """Base exception for session operations."""

    pass


class SessionStorageError(SessionError):
    """Error during storage backend operations."""

    pass


class SessionSerializationError(SessionError):
    """Error during session data serialization/deserialization."""

    pass
