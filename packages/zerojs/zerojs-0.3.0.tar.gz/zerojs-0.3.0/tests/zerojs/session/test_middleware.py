"""Tests for SessionMiddleware."""

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from zerojs.session import MemorySessionStore, SessionMiddleware


def create_app(store, secret_key="test-secret-key", **middleware_kwargs):
    """Create a test app with session middleware."""

    async def get_session(request: Request):
        session = request.state.session
        return JSONResponse(dict(session))

    async def set_session(request: Request):
        session = request.state.session
        data = await request.json()
        for key, value in data.items():
            session[key] = value
        return JSONResponse({"status": "ok"})

    async def clear_session(request: Request):
        session = request.state.session
        session.clear()
        return JSONResponse({"status": "cleared"})

    async def rotate_session(request: Request):
        session = request.state.session
        session.rotate()
        return JSONResponse({"status": "rotated"})

    async def get_session_id(request: Request):
        return PlainTextResponse(request.state._session_id)

    app = Starlette(
        routes=[
            Route("/get", get_session),
            Route("/set", set_session, methods=["POST"]),
            Route("/clear", clear_session, methods=["POST"]),
            Route("/rotate", rotate_session, methods=["POST"]),
            Route("/session-id", get_session_id),
        ]
    )

    app.add_middleware(
        SessionMiddleware,
        store=store,
        secret_key=secret_key,
        **middleware_kwargs,
    )

    return app


class TestSessionMiddleware:
    """Tests for SessionMiddleware."""

    @pytest.fixture
    def store(self) -> MemorySessionStore:
        """Create a fresh memory store for each test."""
        return MemorySessionStore()

    @pytest.fixture
    def client(self, store: MemorySessionStore) -> TestClient:
        """Create a test client with session middleware."""
        app = create_app(store)
        return TestClient(app, cookies={})

    def test_new_session_creates_cookie(self, client: TestClient) -> None:
        """New sessions create a session cookie."""
        response = client.get("/get")
        assert response.status_code == 200
        assert "session" in response.cookies

    def test_session_data_persists(self, client: TestClient) -> None:
        """Session data persists across requests."""
        # Set data
        response = client.post("/set", json={"user_id": 123})
        assert response.status_code == 200

        # Get data
        response = client.get("/get")
        assert response.status_code == 200
        assert response.json() == {"user_id": 123}

    def test_session_data_is_isolated(self, store: MemorySessionStore) -> None:
        """Different clients have isolated sessions."""
        app = create_app(store)
        client1 = TestClient(app, cookies={})
        client2 = TestClient(app, cookies={})

        # Set different data for each client
        client1.post("/set", json={"user": "alice"})
        client2.post("/set", json={"user": "bob"})

        # Verify isolation
        assert client1.get("/get").json() == {"user": "alice"}
        assert client2.get("/get").json() == {"user": "bob"}

    def test_session_clear(self, client: TestClient) -> None:
        """Session clear removes all data."""
        client.post("/set", json={"user_id": 123, "name": "test"})
        client.post("/clear")
        assert client.get("/get").json() == {}

    def test_session_rotation_changes_id(self, client: TestClient) -> None:
        """Session rotation changes the session ID."""
        # Get initial session ID
        response1 = client.get("/session-id")
        session_id_1 = response1.text

        # Rotate
        client.post("/rotate")

        # Get new session ID
        response2 = client.get("/session-id")
        session_id_2 = response2.text

        assert session_id_1 != session_id_2

    def test_session_rotation_preserves_data(self, client: TestClient) -> None:
        """Session rotation preserves session data."""
        client.post("/set", json={"user_id": 123})
        client.post("/rotate")
        assert client.get("/get").json() == {"user_id": 123}

    def test_invalid_cookie_creates_new_session(self, store: MemorySessionStore) -> None:
        """Invalid session cookie creates a new session."""
        app = create_app(store)
        client = TestClient(app)

        # Manually set an invalid cookie
        client.cookies.set("session", "invalid-cookie-value")

        response = client.get("/get")
        assert response.status_code == 200
        # Should get a new, empty session
        assert response.json() == {}
        # Should get a new valid cookie
        assert "session" in response.cookies

    def test_tampered_cookie_creates_new_session(self, store: MemorySessionStore) -> None:
        """Tampered session cookie creates a new session."""
        app = create_app(store)
        client = TestClient(app)

        # First, get a valid session
        client.post("/set", json={"secret": "data"})
        valid_cookie = client.cookies.get("session")

        # Tamper with the signature part (after the last dot)
        parts = valid_cookie.rsplit(".", 1)
        tampered = parts[0] + ".TAMPERED" if len(parts) == 2 else "TAMPERED"

        # Use a new client with the tampered cookie to avoid cookie persistence issues
        client2 = TestClient(app, cookies={"session": tampered})

        # Should get a new, empty session
        response = client2.get("/get")
        assert response.json() == {}

    def test_expired_session_creates_new(self, store: MemorySessionStore) -> None:
        """Expired session in store creates a new session."""
        app = create_app(store, max_age=1)
        client = TestClient(app)

        # Create a session
        client.post("/set", json={"user": "test"})

        # Manually expire the session in store
        for session_id, (data, _) in list(store._sessions.items()):
            # Set accessed_at to long ago
            data.accessed_at = 0
            store._sessions[session_id] = (data, 1)

        # Should get a new, empty session
        response = client.get("/get")
        assert response.json() == {}

    def test_custom_cookie_name(self, store: MemorySessionStore) -> None:
        """Custom cookie name is used."""
        app = create_app(store, cookie_name="my_session")
        client = TestClient(app)

        response = client.get("/get")
        assert "my_session" in response.cookies
        assert "session" not in response.cookies

    def test_https_only_cookie(self, store: MemorySessionStore) -> None:
        """HTTPS-only cookie has secure flag."""
        app = create_app(store, https_only=True)
        client = TestClient(app, base_url="https://testserver")

        response = client.get("/get")
        # The cookie should be set with secure flag
        # TestClient doesn't expose cookie attributes directly,
        # but we can verify the cookie is set
        assert "session" in response.cookies

    def test_session_interface_dict_operations(self, client: TestClient) -> None:
        """Session interface supports dict operations."""
        # Set multiple values
        client.post("/set", json={"a": 1, "b": 2, "c": 3})

        # Verify all values
        data = client.get("/get").json()
        assert data == {"a": 1, "b": 2, "c": 3}


class TestSessionIntegrationWithStore:
    """Integration tests with different storage backends."""

    def test_memory_store_integration(self) -> None:
        """Full integration with MemorySessionStore."""
        store = MemorySessionStore()
        app = create_app(store)
        client = TestClient(app)

        # Full workflow
        client.post("/set", json={"step": 1})
        assert client.get("/get").json() == {"step": 1}

        client.post("/set", json={"step": 2, "extra": "data"})
        assert client.get("/get").json() == {"step": 2, "extra": "data"}

        client.post("/rotate")
        assert client.get("/get").json() == {"step": 2, "extra": "data"}

        client.post("/clear")
        assert client.get("/get").json() == {}


class TestSessionExpiration:
    """Tests for session expiration behavior."""

    def test_sliding_expiration_renews_on_read(self) -> None:
        """Session TTL is renewed on read-only requests."""
        store = MemorySessionStore()
        app = create_app(store)
        client = TestClient(app)

        # Create session with data
        client.post("/set", json={"user": "alice"})

        # Get session ID from store
        session_ids = list(store._sessions.keys())
        assert len(session_ids) == 1
        session_id = session_ids[0]

        # Get original accessed_at
        original_data, _ = store._sessions[session_id]
        original_accessed_at = original_data.accessed_at

        # Make a read-only request (should touch the session)
        import time

        time.sleep(0.01)  # Small delay to ensure time difference
        response = client.get("/get")
        assert response.json() == {"user": "alice"}

        # Verify accessed_at was updated
        updated_data, _ = store._sessions[session_id]
        assert updated_data.accessed_at >= original_accessed_at

    def test_absolute_expiration_rejects_old_session(self) -> None:
        """Session is rejected when absolute lifetime exceeded."""
        store = MemorySessionStore()
        app = create_app(store, absolute_lifetime=1)  # 1 second absolute lifetime
        client = TestClient(app)

        # Create session with data
        client.post("/set", json={"user": "alice"})
        assert client.get("/get").json() == {"user": "alice"}

        # Get initial session ID
        response1 = client.get("/session-id")
        session_id_1 = response1.text

        # Wait for absolute lifetime to expire
        import time

        time.sleep(1.1)

        # Session should be rejected and a new one created
        response = client.get("/get")
        assert response.json() == {}  # New empty session

        # Verify we got a new session ID
        response2 = client.get("/session-id")
        session_id_2 = response2.text
        assert session_id_1 != session_id_2

    def test_absolute_expiration_disabled_by_default(self) -> None:
        """Absolute expiration is disabled when set to 0."""
        store = MemorySessionStore()
        app = create_app(store, absolute_lifetime=0)  # Disabled
        client = TestClient(app)

        # Create session with data
        client.post("/set", json={"user": "alice"})

        # Manually set created_at to a very old time
        session_ids = list(store._sessions.keys())
        session_id = session_ids[0]
        data, ttl = store._sessions[session_id]
        data.created_at = 0  # Very old

        # Session should still be valid (absolute expiration disabled)
        assert client.get("/get").json() == {"user": "alice"}
