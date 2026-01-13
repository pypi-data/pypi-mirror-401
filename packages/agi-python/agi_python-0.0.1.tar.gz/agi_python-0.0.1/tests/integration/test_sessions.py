"""Integration tests for Sessions API."""

import pytest

from agi import AGIClient


@pytest.mark.integration
def test_session_lifecycle(client: AGIClient):
    """Test complete session lifecycle: create, send message, get status, delete."""
    # Create session
    session = client.sessions.create(agent_name="agi-0")
    assert session.session_id is not None
    assert session.vnc_url is not None
    assert session.status in ["ready", "running"]

    session_id = session.session_id

    try:
        # Get session status
        status = client.sessions.get_status(session_id)
        assert status.status in ["ready", "running", "paused"]

        # Send message
        client.sessions.send_message(session_id, "What is 2+2?")

        # Stream events (limit to first 10 for testing)
        event_count = 0
        for event in client.sessions.stream_events(session_id):
            event_count += 1
            assert event.event is not None

            if event.event == "done":
                break
            elif event.event == "error":
                pytest.fail(f"Agent error: {event.data}")

            if event_count >= 10:
                break

    finally:
        # Clean up: delete session
        result = client.sessions.delete(session_id)
        assert result.message is not None


@pytest.mark.integration
def test_session_context_manager(api_key):
    """Test session creation using context manager."""
    client = AGIClient(api_key=api_key)

    with client.session("agi-0") as session:
        assert session.session_id is not None
        assert session.vnc_url is not None

        # Send simple task
        client.sessions.send_message(session.session_id, "What is 2+2?")

        # Stream a few events
        event_count = 0
        for event in client.sessions.stream_events(session.session_id):
            event_count += 1
            assert event.event is not None

            if event.event == "done":
                break
            elif event.event == "error":
                pytest.fail(f"Agent error: {event.data}")

            if event_count >= 10:
                break


@pytest.mark.integration
def test_list_sessions(client: AGIClient):
    """Test listing sessions."""
    # Create a session first
    session = client.sessions.create(agent_name="agi-0")
    session_id = session.session_id

    try:
        # List sessions
        sessions = client.sessions.list()
        assert sessions is not None
        assert len(sessions) > 0

        # Check that our session is in the list
        session_ids = [s.session_id for s in sessions]
        assert session_id in session_ids

    finally:
        # Clean up
        client.sessions.delete(session_id)


@pytest.mark.integration
def test_delete_all_sessions(client: AGIClient):
    """Test deleting all sessions."""
    # Create a couple of sessions
    _session1 = client.sessions.create(agent_name="agi-0")
    _session2 = client.sessions.create(agent_name="agi-0")

    # Delete all sessions
    result = client.sessions.delete_all()
    assert result.message is not None

    # Verify sessions are deleted
    sessions = client.sessions.list()
    assert len(sessions) == 0
