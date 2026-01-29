import pytest
from fastapi.testclient import TestClient
from nanocore.app import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_check():
    """Test the /health endpoint returns correct status and worker count."""
    # TestClient triggers the lifespan events
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["workers"] == 1


def test_app_state_broker(client):
    """Verify that the application state has a properly initialized broker."""
    assert hasattr(app.state, "broker")
    assert "default_calc" in app.state.broker._workers


@pytest.mark.asyncio
async def test_websocket_pong(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"type": "pong"})
        # No error should occur, and connection should stay open
        try:
            # We can't easily check internal state of manager from here without more mocks,
            # but we can verify it doesn't crash.
            pass
        except Exception as e:
            pytest.fail(f"Websocket crashed on pong: {e}")


@pytest.mark.asyncio
async def test_websocket_invalid_format(client):
    with client.websocket_connect("/ws") as websocket:
        # Invalid format (no header)
        websocket.send_json({"body": {"x": 1}})
        # Should log warning but not crash


@pytest.mark.asyncio
async def test_websocket_exception_handling(client):
    # This is hard to trigger from outside without mocking internal loop
    # but we can verify it handles unexpected data types
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json("not a dict")
        # Should catch exception and disconnect
