"""Comprehensive test suite for agi SDK - Testing all features in depth."""

import os
import time

import pytest

from agi import (
    AGIClient,
    AuthenticationError,
    NotFoundError,
)


@pytest.mark.unit
class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_init_with_key(self):
        """Test creating client with explicit API key."""
        client = AGIClient(api_key="test_key_12345")
        assert client.api_key == "test_key_12345"
        assert client.sessions is not None

    def test_client_init_from_env(self):
        """Test creating client from AGI_API_KEY env var."""
        if not os.getenv("AGI_API_KEY"):
            pytest.skip("AGI_API_KEY not set")

        client = AGIClient()
        assert client.api_key == os.getenv("AGI_API_KEY")

    def test_client_init_no_key(self, monkeypatch):
        """Test that client fails without API key."""
        monkeypatch.delenv("AGI_API_KEY", raising=False)

        with pytest.raises(ValueError, match="api_key is required"):
            AGIClient()

    def test_client_as_context_manager(self):
        """Test using client as context manager."""
        with AGIClient(api_key="test") as client:
            assert client.api_key is not None


@pytest.mark.integration
class TestSessionManagement:
    """Tests for session management APIs."""

    def test_create_session(self, client):
        """Test creating a new session."""
        session = client.sessions.create(agent_name="agi-0")

        assert session.session_id is not None
        assert session.vnc_url is not None
        assert session.status in ["ready", "running"]
        assert session.agent_name == "agi-0"

        # Clean up
        client.sessions.delete(session.session_id)

    def test_create_session_with_params(self, client):
        """Test creating session with custom parameters."""
        session = client.sessions.create(
            agent_name="agi-0-fast",
            goal="Test goal for comprehensive testing",
            max_steps=50,
        )

        assert session.session_id is not None
        assert session.agent_name == "agi-0-fast"

        # Clean up
        client.sessions.delete(session.session_id)

    def test_list_sessions(self, client):
        """Test listing all sessions."""
        session = client.sessions.create(agent_name="agi-0")

        try:
            # List sessions
            sessions = client.sessions.list()
            assert isinstance(sessions, list)
            assert len(sessions) > 0

            session_ids = [s.session_id for s in sessions]
            assert session.session_id in session_ids
        finally:
            # Clean up
            client.sessions.delete(session.session_id)

    def test_get_session(self, client):
        """Test getting specific session details."""
        created = client.sessions.create(agent_name="agi-0")

        try:
            # Get session details
            session = client.sessions.get(created.session_id)

            assert session.session_id == created.session_id
            assert session.status is not None
        finally:
            # Clean up
            client.sessions.delete(session.session_id)

    def test_delete_session(self, client):
        """Test deleting a session."""
        session = client.sessions.create(agent_name="agi-0")
        session_id = session.session_id

        # Delete it
        result = client.sessions.delete(session_id)
        assert result.message is not None or result.success is True

        time.sleep(2)

        with pytest.raises(NotFoundError):
            client.sessions.get(session_id)

    def test_delete_all_sessions(self, client):
        """Test deleting all sessions."""
        client.sessions.create(agent_name="agi-0")
        client.sessions.create(agent_name="agi-0")

        # Delete all
        result = client.sessions.delete_all()
        assert result.message is not None

        sessions = client.sessions.list()
        assert len(sessions) == 0


@pytest.mark.integration
class TestSessionContext:
    """Tests for SessionContext high-level API."""

    def test_session_context_basic(self, client):
        """Test SessionContext with context manager."""
        with client.session("agi-0") as session:
            assert session.session_id is not None
            assert session.vnc_url is not None
            session_id = session.session_id

        time.sleep(1)
        with pytest.raises(NotFoundError):
            client.sessions.get(session_id)

    def test_session_context_send_message(self, client):
        """Test sending message through SessionContext."""
        with client.session("agi-0") as session:
            result = session.send_message("What is 2+2?")
            assert result is not None

    def test_session_context_get_status(self, client):
        """Test getting status through SessionContext."""
        with client.session("agi-0") as session:
            status = session.get_status()
            assert status.status in ["ready", "running", "waiting_for_input", "paused", "finished"]

    def test_session_context_stream_events(self, client):
        """Test streaming events through SessionContext."""
        with client.session("agi-0") as session:
            session.send_message("What is the capital of France?")

            # Stream events
            event_count = 0
            event_types = set()

            for event in session.stream_events():
                event_count += 1
                event_types.add(event.event)

                if event.event in ["done", "error"]:
                    break

                if event_count >= 20:  # Safety limit
                    break

            assert event_count > 0
            assert len(event_types) > 0

    def test_session_context_run_task(self, client):
        """Test run_task - the primary high-level method."""
        with client.session("agi-0") as session:
            result = session.run_task("What is 2+2?")
            assert result is not None


@pytest.mark.integration
class TestSessionControl:
    """Tests for pause, resume, cancel operations."""

    def test_session_pause(self, client):
        """Test pausing a session."""
        with client.session("agi-0") as session:
            session.send_message("Count to 100 slowly")
            time.sleep(2)

            # Pause
            result = session.pause()
            assert result is not None

            status = session.get_status()

            assert status.status is not None

    def test_session_resume(self, client):
        """Test resuming a paused session."""
        with client.session("agi-0") as session:
            session.send_message("Count to 100")
            time.sleep(1)
            session.pause()
            time.sleep(1)

            # Resume
            result = session.resume()
            assert result is not None

            status = session.get_status()
            assert status.status is not None

    def test_session_cancel(self, client):
        """Test canceling a session."""
        with client.session("agi-0") as session:
            session.send_message("Long running task...")
            time.sleep(1)

            # Cancel
            result = session.cancel()
            assert result is not None


@pytest.mark.integration
class TestBrowserControl:
    """Tests for browser control operations."""

    def test_session_navigate(self, client):
        """Test navigating to a URL."""
        with client.session("agi-0") as session:
            result = session.navigate("https://example.com")

            assert result.current_url is not None

    def test_session_screenshot(self, client):
        """Test taking a screenshot."""
        with client.session("agi-0") as session:
            session.navigate("https://example.com")
            time.sleep(2)

            # Take screenshot
            screenshot = session.screenshot()

            assert screenshot.url is not None
            assert screenshot.screenshot is not None  # base64 data
            assert len(screenshot.screenshot) > 100  # Has meaningful content


@pytest.mark.integration
class TestErrorHandling:
    """Tests for error handling and exceptions."""

    def test_auth_error(self):
        """Test authentication error handling."""
        client = AGIClient(api_key="invalid_key_12345")

        with pytest.raises(AuthenticationError):
            client.sessions.create(agent_name="agi-0")

    def test_not_found_error(self, client):
        """Test NotFoundError handling."""
        with pytest.raises(NotFoundError):
            client.sessions.get("00000000-0000-0000-0000-000000000000")


@pytest.mark.integration
class TestAdvancedFeatures:
    """Tests for advanced SDK features."""

    def test_get_messages(self, client):
        """Test getting messages from a session."""
        with client.session("agi-0") as session:
            session.send_message("Hello, what is 2+2?")
            time.sleep(2)

            # Get messages
            messages = session.get_messages()
            assert messages is not None

    def test_low_level_send_message(self, client):
        """Test low-level session API."""
        session = client.sessions.create(agent_name="agi-0")
        try:
            client.sessions.send_message(session.session_id, "Test message")

            status = client.sessions.get_status(session.session_id)
            assert status.status is not None

        finally:
            client.sessions.delete(session.session_id)

    def test_low_level_stream(self, client):
        """Test low-level streaming API."""
        session = client.sessions.create(agent_name="agi-0")
        try:
            # Send message
            client.sessions.send_message(session.session_id, "What is 2+2?")

            # Stream events
            event_count = 0
            for event in client.sessions.stream_events(session.session_id):
                event_count += 1

                if event.event in ["done", "error"]:
                    break

                if event_count >= 10:
                    break

            assert event_count > 0

        finally:
            client.sessions.delete(session.session_id)


# Standalone execution for backward compatibility
if __name__ == "__main__":
    print("=" * 80)
    print("COMPREHENSIVE agi SDK TEST SUITE")
    print("=" * 80)
    print()
    print("This test file has been converted to pytest format.")
    print("   Run with: pytest tests/integration/test_comprehensive.py -v")
    print()
    print("   Run specific sections:")
    print("     pytest tests/integration/test_comprehensive.py::TestClientInitialization -v")
    print("     pytest tests/integration/test_comprehensive.py::TestSessionManagement -v")
    print("=" * 80)
