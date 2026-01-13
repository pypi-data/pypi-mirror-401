"""Tests for authentication event system."""

import asyncio
import logging

import pytest

from zerojs.auth.events import AuthEvent, AuthEventEmitter


class TestAuthEvent:
    """Tests for AuthEvent enum."""

    def test_has_login_events(self) -> None:
        """AuthEvent has login-related events."""
        assert AuthEvent.LOGIN_SUCCESS
        assert AuthEvent.LOGIN_FAILED
        assert AuthEvent.LOGOUT

    def test_has_password_events(self) -> None:
        """AuthEvent has password-related events."""
        assert AuthEvent.PASSWORD_CHANGED
        assert AuthEvent.PASSWORD_RESET_REQUESTED
        assert AuthEvent.PASSWORD_RESET_COMPLETED

    def test_has_session_events(self) -> None:
        """AuthEvent has session-related events."""
        assert AuthEvent.SESSION_EXPIRED
        assert AuthEvent.SESSION_ROTATED

    def test_has_mfa_events(self) -> None:
        """AuthEvent has MFA-related events."""
        assert AuthEvent.MFA_ENABLED
        assert AuthEvent.MFA_DISABLED
        assert AuthEvent.MFA_CHALLENGE_SENT
        assert AuthEvent.MFA_CHALLENGE_PASSED
        assert AuthEvent.MFA_CHALLENGE_FAILED

    def test_has_impersonation_events(self) -> None:
        """AuthEvent has impersonation-related events."""
        assert AuthEvent.IMPERSONATION_START
        assert AuthEvent.IMPERSONATION_END

    def test_has_permission_events(self) -> None:
        """AuthEvent has permission-related events."""
        assert AuthEvent.PERMISSION_DENIED


class TestAuthEventEmitterDecorator:
    """Tests for @on() decorator."""

    def test_on_registers_listener(self) -> None:
        """@on() registers a listener."""
        emitter = AuthEventEmitter()

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def handler(**ctx) -> None:
            pass

        assert emitter.listener_count(AuthEvent.LOGIN_SUCCESS) == 1

    def test_on_returns_original_function(self) -> None:
        """@on() returns the original function."""
        emitter = AuthEventEmitter()

        async def original(**ctx) -> None:
            pass

        decorated = emitter.on(AuthEvent.LOGIN_SUCCESS)(original)
        assert decorated is original

    def test_multiple_decorators_for_same_event(self) -> None:
        """Multiple listeners can be registered for the same event."""
        emitter = AuthEventEmitter()

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def handler1(**ctx) -> None:
            pass

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def handler2(**ctx) -> None:
            pass

        assert emitter.listener_count(AuthEvent.LOGIN_SUCCESS) == 2


class TestAuthEventEmitterAddListener:
    """Tests for add_listener()."""

    def test_add_listener_registers(self) -> None:
        """add_listener() registers a listener."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        emitter.add_listener(AuthEvent.LOGOUT, handler)
        assert emitter.listener_count(AuthEvent.LOGOUT) == 1

    def test_add_same_listener_twice(self) -> None:
        """Same listener can be added multiple times."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        emitter.add_listener(AuthEvent.LOGOUT, handler)
        emitter.add_listener(AuthEvent.LOGOUT, handler)
        assert emitter.listener_count(AuthEvent.LOGOUT) == 2


class TestAuthEventEmitterRemoveListener:
    """Tests for remove_listener()."""

    def test_remove_listener_removes(self) -> None:
        """remove_listener() removes the listener."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        emitter.add_listener(AuthEvent.LOGOUT, handler)
        assert emitter.listener_count(AuthEvent.LOGOUT) == 1

        result = emitter.remove_listener(AuthEvent.LOGOUT, handler)
        assert result is True
        assert emitter.listener_count(AuthEvent.LOGOUT) == 0

    def test_remove_nonexistent_listener(self) -> None:
        """remove_listener() returns False for nonexistent listener."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        result = emitter.remove_listener(AuthEvent.LOGOUT, handler)
        assert result is False

    def test_remove_from_nonexistent_event(self) -> None:
        """remove_listener() returns False for nonexistent event."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        result = emitter.remove_listener(AuthEvent.LOGOUT, handler)
        assert result is False


class TestAuthEventEmitterClearListeners:
    """Tests for clear_listeners()."""

    def test_clear_specific_event(self) -> None:
        """clear_listeners(event) clears only that event's listeners."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)
        emitter.add_listener(AuthEvent.LOGOUT, handler)

        emitter.clear_listeners(AuthEvent.LOGIN_SUCCESS)

        assert emitter.listener_count(AuthEvent.LOGIN_SUCCESS) == 0
        assert emitter.listener_count(AuthEvent.LOGOUT) == 1

    def test_clear_all_listeners(self) -> None:
        """clear_listeners() with no argument clears all listeners."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)
        emitter.add_listener(AuthEvent.LOGOUT, handler)
        emitter.add_listener(AuthEvent.MFA_ENABLED, handler)

        emitter.clear_listeners()

        assert emitter.listener_count(AuthEvent.LOGIN_SUCCESS) == 0
        assert emitter.listener_count(AuthEvent.LOGOUT) == 0
        assert emitter.listener_count(AuthEvent.MFA_ENABLED) == 0


class TestAuthEventEmitterEmit:
    """Tests for emit()."""

    def test_emit_calls_listener(self) -> None:
        """emit() calls registered listeners."""
        emitter = AuthEventEmitter()
        called = []

        async def handler(**ctx) -> None:
            called.append(ctx)

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)

        asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user_id=123, ip="1.2.3.4"))

        assert len(called) == 1
        assert called[0] == {"user_id": 123, "ip": "1.2.3.4"}

    def test_emit_calls_all_listeners(self) -> None:
        """emit() calls all registered listeners."""
        emitter = AuthEventEmitter()
        results = []

        async def handler1(**ctx) -> None:
            results.append("handler1")

        async def handler2(**ctx) -> None:
            results.append("handler2")

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler1)
        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler2)

        asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS))

        assert "handler1" in results
        assert "handler2" in results

    def test_emit_does_nothing_without_listeners(self) -> None:
        """emit() does nothing if no listeners registered."""
        emitter = AuthEventEmitter()
        # Should not raise
        asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user_id=123))

    def test_emit_passes_kwargs_to_listeners(self) -> None:
        """emit() passes all kwargs to listeners."""
        emitter = AuthEventEmitter()
        received = {}

        async def handler(user, ip, user_agent, **extra) -> None:
            received["user"] = user
            received["ip"] = ip
            received["user_agent"] = user_agent
            received["extra"] = extra

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)

        asyncio.run(
            emitter.emit(
                AuthEvent.LOGIN_SUCCESS,
                user="john",
                ip="1.2.3.4",
                user_agent="Mozilla",
                custom="value",
            )
        )

        assert received["user"] == "john"
        assert received["ip"] == "1.2.3.4"
        assert received["user_agent"] == "Mozilla"
        assert received["extra"] == {"custom": "value"}

    def test_emit_continues_on_listener_error(self, caplog) -> None:
        """emit() continues calling listeners even if one fails."""
        emitter = AuthEventEmitter()
        results = []

        async def failing_handler(**ctx) -> None:
            raise ValueError("Test error")

        async def success_handler(**ctx) -> None:
            results.append("success")

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, failing_handler)
        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, success_handler)

        with caplog.at_level(logging.ERROR, logger="zerojs.auth.events"):
            asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS))

        # Second handler should still be called
        assert "success" in results

        # Error should be logged
        assert "Error in LOGIN_SUCCESS listener failing_handler" in caplog.text

    def test_emit_only_calls_matching_event_listeners(self) -> None:
        """emit() only calls listeners for the emitted event."""
        emitter = AuthEventEmitter()
        results = []

        async def login_handler(**ctx) -> None:
            results.append("login")

        async def logout_handler(**ctx) -> None:
            results.append("logout")

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, login_handler)
        emitter.add_listener(AuthEvent.LOGOUT, logout_handler)

        asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS))

        assert results == ["login"]


class TestAuthEventEmitterListenerCount:
    """Tests for listener_count()."""

    def test_listener_count_zero_for_no_listeners(self) -> None:
        """listener_count() returns 0 when no listeners."""
        emitter = AuthEventEmitter()
        assert emitter.listener_count(AuthEvent.LOGIN_SUCCESS) == 0

    def test_listener_count_returns_correct_count(self) -> None:
        """listener_count() returns correct count."""
        emitter = AuthEventEmitter()

        async def handler(**ctx) -> None:
            pass

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)
        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)
        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, handler)

        assert emitter.listener_count(AuthEvent.LOGIN_SUCCESS) == 3


class TestAuthEventEmitterIntegration:
    """Integration tests for common use cases."""

    def test_audit_logging_pattern(self) -> None:
        """Test audit logging pattern."""
        emitter = AuthEventEmitter()
        audit_log: list[str] = []

        @emitter.on(AuthEvent.LOGIN_FAILED)
        async def log_failed(identifier: str, ip: str, **ctx) -> None:
            audit_log.append(f"Failed login: {identifier} from {ip}")

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def log_success(user_id: int, ip: str, **ctx) -> None:
            audit_log.append(f"Successful login: user {user_id} from {ip}")

        # Simulate failed then successful login
        asyncio.run(emitter.emit(AuthEvent.LOGIN_FAILED, identifier="user@example.com", ip="1.2.3.4"))
        asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user_id=123, ip="1.2.3.4"))

        assert len(audit_log) == 2
        assert "Failed login: user@example.com from 1.2.3.4" in audit_log
        assert "Successful login: user 123 from 1.2.3.4" in audit_log

    def test_impersonation_tracking(self) -> None:
        """Test impersonation tracking pattern."""
        emitter = AuthEventEmitter()
        impersonation_log: list[dict] = []

        @emitter.on(AuthEvent.IMPERSONATION_START)
        async def log_impersonation_start(admin_id: int, target_id: int, **ctx) -> None:
            impersonation_log.append({"action": "start", "admin": admin_id, "target": target_id})

        @emitter.on(AuthEvent.IMPERSONATION_END)
        async def log_impersonation_end(admin_id: int, target_id: int, **ctx) -> None:
            impersonation_log.append({"action": "end", "admin": admin_id, "target": target_id})

        asyncio.run(emitter.emit(AuthEvent.IMPERSONATION_START, admin_id=1, target_id=100))
        asyncio.run(emitter.emit(AuthEvent.IMPERSONATION_END, admin_id=1, target_id=100))

        assert len(impersonation_log) == 2
        assert impersonation_log[0]["action"] == "start"
        assert impersonation_log[1]["action"] == "end"


class TestCriticalEventListeners:
    """Tests for critical event listener functionality."""

    def test_critical_listener_error_propagates(self) -> None:
        """Critical listener errors are re-raised."""
        emitter = AuthEventEmitter()

        @emitter.on(AuthEvent.LOGIN_SUCCESS, critical=True)
        async def critical_handler(**ctx) -> None:
            raise ValueError("Critical failure")

        with pytest.raises(ValueError, match="Critical failure"):
            asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user="test"))

    def test_non_critical_listener_error_is_suppressed(self) -> None:
        """Non-critical listener errors are logged but suppressed."""
        emitter = AuthEventEmitter()
        results = []

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def failing_handler(**ctx) -> None:
            raise ValueError("Non-critical failure")

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def success_handler(**ctx) -> None:
            results.append("success")

        # Should not raise, and second handler should still run
        asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user="test"))
        assert "success" in results

    def test_critical_via_add_listener(self) -> None:
        """Critical flag works with add_listener."""
        emitter = AuthEventEmitter()

        async def critical_handler(**ctx) -> None:
            raise RuntimeError("Must not fail")

        emitter.add_listener(AuthEvent.LOGIN_SUCCESS, critical_handler, critical=True)

        with pytest.raises(RuntimeError, match="Must not fail"):
            asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user="test"))

    def test_mixed_critical_and_non_critical(self) -> None:
        """Non-critical runs first, then critical failure propagates."""
        emitter = AuthEventEmitter()
        results = []

        @emitter.on(AuthEvent.LOGIN_SUCCESS)
        async def non_critical_handler(**ctx) -> None:
            results.append("non_critical")

        @emitter.on(AuthEvent.LOGIN_SUCCESS, critical=True)
        async def critical_handler(**ctx) -> None:
            results.append("critical_before_error")
            raise ValueError("Critical failure")

        with pytest.raises(ValueError, match="Critical failure"):
            asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user="test"))

        # Both handlers were called before error propagated
        assert "non_critical" in results
        assert "critical_before_error" in results

    def test_critical_listener_logs_before_raising(self, caplog) -> None:
        """Critical listener errors are logged before being re-raised."""
        emitter = AuthEventEmitter()

        @emitter.on(AuthEvent.LOGIN_SUCCESS, critical=True)
        async def critical_handler(**ctx) -> None:
            raise ValueError("Logged and raised")

        with caplog.at_level(logging.ERROR, logger="zerojs.auth.events"):
            with pytest.raises(ValueError):
                asyncio.run(emitter.emit(AuthEvent.LOGIN_SUCCESS, user="test"))

        assert "Error in LOGIN_SUCCESS listener critical_handler" in caplog.text
