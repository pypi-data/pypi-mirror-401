"""Quick smoke test - validates all SDK features work correctly."""

import time

import pytest

from agi import (
    AGIClient,
    AuthenticationError,
    NotFoundError,
)


@pytest.mark.integration
class TestSmoke:
    """Smoke tests for core SDK functionality."""

    def test_client_initialization(self, client):
        """Test client can be initialized."""
        assert client.api_key is not None
        assert client.sessions is not None

    def test_authentication_error(self):
        """Test authentication error handling with invalid key."""
        client = AGIClient(api_key="invalid_key")
        with pytest.raises(AuthenticationError):
            client.sessions.list()

    def test_create_session(self, client):
        """Test creating a new session."""
        session = client.sessions.create(agent_name="agi-0")
        assert session.session_id is not None
        assert session.vnc_url is not None

        client.sessions.delete(session.session_id)

    def test_list_sessions(self, client):
        """Test listing sessions."""
        session = client.sessions.create(agent_name="agi-0")

        try:
            sessions = client.sessions.list()
            assert isinstance(sessions, list)
            assert len(sessions) > 0
        finally:
            client.sessions.delete(session.session_id)

    def test_get_session(self, client):
        """Test getting session details."""
        session = client.sessions.create(agent_name="agi-0")

        try:
            retrieved = client.sessions.get(session.session_id)
            assert retrieved.session_id == session.session_id
        finally:
            client.sessions.delete(session.session_id)

    def test_send_message_lowlevel(self, client):
        """Test low-level send_message API."""
        session = client.sessions.create(agent_name="agi-0")

        try:
            result = client.sessions.send_message(session.session_id, "Hello, test message")
            assert result is not None
        finally:
            client.sessions.delete(session.session_id)

    def test_get_status_lowlevel(self, client):
        """Test low-level get_status API."""
        session = client.sessions.create(agent_name="agi-0")

        try:
            status = client.sessions.get_status(session.session_id)
            assert status.status is not None
        finally:
            client.sessions.delete(session.session_id)

    def test_session_context_manager(self, client):
        """Test SessionContext with context manager."""
        with client.session("agi-0") as session:
            assert session.session_id is not None
            assert session.vnc_url is not None

    def test_session_context_send_message(self, client):
        """Test SessionContext.send_message()."""
        with client.session("agi-0") as session:
            result = session.send_message("Test from SessionContext")
            assert result is not None

    def test_session_context_get_status(self, client):
        """Test SessionContext.get_status()."""
        with client.session("agi-0") as session:
            status = session.get_status()
            assert status.status is not None

    def test_navigate(self, client):
        """Test navigate to URL."""
        with client.session("agi-0") as session:
            result = session.navigate("https://example.com")
            assert result.current_url is not None

    def test_screenshot(self, client):
        """Test taking screenshot."""
        with client.session("agi-0") as session:
            session.navigate("https://example.com")
            time.sleep(2)
            screenshot = session.screenshot()
            assert screenshot.data is not None
            assert len(screenshot.data) > 0

    def test_pause(self, client):
        """Test pausing session."""
        with client.session("agi-0") as session:
            session.send_message("Count to 100")
            time.sleep(1)
            result = session.pause()
            assert result is not None

    def test_resume(self, client):
        """Test resuming paused session."""
        with client.session("agi-0") as session:
            session.send_message("Test task")
            time.sleep(1)
            session.pause()
            time.sleep(1)
            result = session.resume()
            assert result is not None

    def test_cancel(self, client):
        """Test canceling session."""
        with client.session("agi-0") as session:
            session.send_message("Long task")
            time.sleep(1)
            result = session.cancel()
            assert result is not None

    def test_not_found_error(self, client):
        """Test NotFoundError for non-existent session."""
        with pytest.raises(NotFoundError):
            client.sessions.get("00000000-0000-0000-0000-000000000000")

    def test_delete_session(self, client):
        """Test deleting a session."""
        session = client.sessions.create(agent_name="agi-0")
        session_id = session.session_id

        result = client.sessions.delete(session_id)
        assert result.message is not None or result.success is True

    def test_delete_all_sessions(self, client):
        """Test deleting all sessions."""
        client.sessions.create(agent_name="agi-0")
        client.sessions.create(agent_name="agi-0")

        result = client.sessions.delete_all()
        assert result.message is not None


if __name__ == "__main__":
    print("=" * 80)
    print("PYAGI SDK SMOKE TEST - Quick Feature Validation")
    print("=" * 80)
    print()
    print("This test file has been converted to pytest format.")
    print("Run with: pytest tests/integration/test_smoke.py -v")
    print()
    print("Or run directly: python -m pytest tests/integration/test_smoke.py -v")
    print("=" * 80)
