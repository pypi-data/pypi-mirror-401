"""Pytest configuration and shared fixtures."""

import os
from datetime import datetime
from typing import Any

import pytest

from agi import AGIClient


@pytest.fixture
def api_key():
    """Get API key from environment for integration tests."""
    key = os.getenv("AGI_API_KEY")
    if not key:
        pytest.skip("AGI_API_KEY not set")
    return key


@pytest.fixture
def mock_api_key():
    """Mock API key for unit tests (UUID format)."""
    return "12345678-1234-1234-1234-123456789abc"


@pytest.fixture
def mock_client(mock_api_key):
    """Create mock AGIClient for unit tests."""
    from unittest.mock import Mock

    from agi import AGIClient

    client = Mock(spec=AGIClient)
    client.api_key = mock_api_key
    client.sessions = Mock()
    return client


@pytest.fixture
def client(api_key):
    """Create AGIClient with automatic cleanup."""
    client = AGIClient(api_key=api_key)
    yield client
    try:
        # Clean up all sessions
        client.sessions.delete_all()
    except Exception:
        pass


@pytest.fixture
def session_create_response() -> dict[str, Any]:
    """Mock response for session creation."""
    return {
        "session_id": "sess_test_1234567890",
        "vnc_url": "https://vnc.agi.tech/sess_test_1234567890",
        "status": "ready",
        "created_at": datetime.now().isoformat(),
    }


@pytest.fixture
def session_status_response() -> dict[str, Any]:
    """Mock response for session status check."""
    return {
        "status": "running",
        "current_url": "https://example.com",
        "step_count": 5,
    }


@pytest.fixture
def session_finished_response() -> dict[str, Any]:
    """Mock response for completed session."""
    return {
        "status": "finished",
        "current_url": "https://example.com",
        "step_count": 10,
    }


@pytest.fixture
def messages_response() -> dict[str, Any]:
    """Mock response for session messages."""
    return {
        "messages": [
            {
                "id": "msg_1",
                "role": "assistant",
                "content": "Navigating to the page...",
                "timestamp": "2025-01-01T00:00:00Z",
            },
            {
                "id": "msg_2",
                "role": "assistant",
                "content": "Task completed successfully",
                "timestamp": "2025-01-01T00:00:05Z",
            },
        ]
    }


@pytest.fixture
def sessions_list_response() -> dict[str, Any]:
    """Mock response for listing sessions."""
    return {
        "sessions": [
            {
                "session_id": "session-1",
                "status": "running",
                "created_at": "2025-01-01T00:00:00Z",
                "agent_name": "agi-0",
            },
            {
                "session_id": "session-2",
                "status": "finished",
                "created_at": "2025-01-01T00:00:00Z",
                "agent_name": "agi-0-fast",
            },
        ]
    }


@pytest.fixture
def delete_all_response() -> dict[str, Any]:
    """Mock response for deleting all sessions."""
    return {"deleted_count": 3, "message": "All sessions deleted"}


@pytest.fixture
def http_error_response() -> dict[str, Any]:
    """Mock error response from API."""
    return {
        "error": "Invalid API key",
        "code": "authentication_error",
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires API key)"
    )
    config.addinivalue_line("markers", "unit: mark test as unit test (no external dependencies)")
