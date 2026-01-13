"""Unit tests for SessionContext."""

from unittest.mock import Mock

import pytest

from agi._session_context import SessionContext


@pytest.mark.unit
def test_session_context_send_message(mock_client):
    """Test send_message delegates to client.sessions.send_message."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.send_message.return_value = Mock(success=True)

    result = context.send_message("test message")

    mock_client.sessions.send_message.assert_called_once_with(
        "test-session", "test message", None, None
    )
    assert result.success is True


@pytest.mark.unit
def test_session_context_send_message_with_params(mock_client):
    """Test send_message with optional parameters."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.send_message.return_value = Mock(success=True)

    context.send_message("test", start_url="https://example.com", config_updates={"foo": "bar"})

    mock_client.sessions.send_message.assert_called_once_with(
        "test-session", "test", "https://example.com", {"foo": "bar"}
    )


@pytest.mark.unit
def test_session_context_send_message_without_session(mock_client):
    """Test send_message raises error when session not created."""
    context = SessionContext(mock_client, "agi-0")
    # No session_id set

    with pytest.raises(ValueError, match="Session not created"):
        context.send_message("test")


@pytest.mark.unit
def test_session_context_get_status(mock_client):
    """Test get_status delegates to client.sessions.get_status."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.get_status.return_value = Mock(status="running")

    result = context.get_status()

    mock_client.sessions.get_status.assert_called_once_with("test-session")
    assert result.status == "running"


@pytest.mark.unit
def test_session_context_get_status_without_session(mock_client):
    """Test get_status raises error when session not created."""
    context = SessionContext(mock_client, "agi-0")

    with pytest.raises(ValueError, match="Session not created"):
        context.get_status()


@pytest.mark.unit
def test_session_context_get_messages(mock_client):
    """Test get_messages delegates to client.sessions.get_messages."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_messages = Mock(messages=[Mock(content="test")])
    mock_client.sessions.get_messages.return_value = mock_messages

    result = context.get_messages(after_id=5, sanitize=False)

    mock_client.sessions.get_messages.assert_called_once_with("test-session", 5, False)
    assert result == mock_messages


@pytest.mark.unit
def test_session_context_get_messages_defaults(mock_client):
    """Test get_messages with default parameters."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.get_messages.return_value = Mock()

    context.get_messages()

    mock_client.sessions.get_messages.assert_called_once_with("test-session", 0, True)


@pytest.mark.unit
def test_session_context_stream_events(mock_client):
    """Test stream_events delegates to client.sessions.stream_events."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_events = [Mock(event="test")]
    mock_client.sessions.stream_events.return_value = iter(mock_events)

    result = list(context.stream_events())

    assert len(result) == 1
    mock_client.sessions.stream_events.assert_called_once_with("test-session", None, True, True)


@pytest.mark.unit
def test_session_context_stream_events_with_filters(mock_client):
    """Test stream_events with event type filters."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_events = [Mock(event="thought"), Mock(event="done")]
    mock_client.sessions.stream_events.return_value = iter(mock_events)

    result = list(
        context.stream_events(
            event_types=["thought", "done"], sanitize=False, include_history=False
        )
    )

    assert len(result) == 2
    mock_client.sessions.stream_events.assert_called_once_with(
        "test-session", ["thought", "done"], False, False
    )


@pytest.mark.unit
def test_session_context_pause(mock_client):
    """Test pause delegates correctly."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.pause.return_value = Mock(success=True)

    result = context.pause()

    mock_client.sessions.pause.assert_called_once_with("test-session")
    assert result.success is True


@pytest.mark.unit
def test_session_context_resume(mock_client):
    """Test resume delegates correctly."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.resume.return_value = Mock(success=True)

    result = context.resume()

    mock_client.sessions.resume.assert_called_once_with("test-session")
    assert result.success is True


@pytest.mark.unit
def test_session_context_cancel(mock_client):
    """Test cancel delegates correctly."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.cancel.return_value = Mock(success=True)

    result = context.cancel()

    mock_client.sessions.cancel.assert_called_once_with("test-session")
    assert result.success is True


@pytest.mark.unit
def test_session_context_navigate(mock_client):
    """Test navigate delegates correctly."""
    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    mock_client.sessions.navigate.return_value = Mock(current_url="https://example.com")

    result = context.navigate("https://example.com")

    mock_client.sessions.navigate.assert_called_once_with("test-session", "https://example.com")
    assert result.current_url == "https://example.com"


@pytest.mark.unit
def test_session_context_screenshot(mock_client):
    """Test screenshot delegates correctly."""
    from agi.types.sessions import ScreenshotResponse

    context = SessionContext(mock_client, "agi-0")
    context.session_id = "test-session"

    # Mock with real ScreenshotResponse containing base64 data
    mock_client.sessions.screenshot.return_value = ScreenshotResponse(
        screenshot="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        url="https://example.com",
        title="Test Page",
    )

    result = context.screenshot()

    mock_client.sessions.screenshot.assert_called_once_with("test-session")
    assert result.url == "https://example.com"
    assert result.title == "Test Page"
    assert isinstance(result.data, bytes)
    assert len(result.data) > 0
