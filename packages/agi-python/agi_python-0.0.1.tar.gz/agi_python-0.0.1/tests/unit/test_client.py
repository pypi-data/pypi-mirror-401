"""Tests for AGIClient."""

import pytest

from agi import AGIClient


@pytest.mark.unit
def test_client_initialization_with_api_key():
    """Test client can be initialized with API key."""
    client = AGIClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.sessions is not None


@pytest.mark.unit
def test_client_initialization_with_env_var(monkeypatch):
    """Test client falls back to environment variable."""
    monkeypatch.setenv("AGI_API_KEY", "env_key")
    client = AGIClient()
    assert client.api_key == "env_key"


@pytest.mark.unit
def test_client_initialization_without_api_key(monkeypatch):
    """Test client raises error without API key."""
    monkeypatch.delenv("AGI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="api_key is required"):
        AGIClient()


@pytest.mark.unit
def test_client_has_sessions_resource():
    """Test client has sessions resource."""
    client = AGIClient(api_key="test")
    assert hasattr(client, "sessions")
    assert client.sessions is not None


@pytest.mark.unit
def test_client_session_context_manager():
    """Test client.session() returns SessionContext."""
    client = AGIClient(api_key="test")
    context = client.session("agi-0")
    assert context is not None
    assert context._agent_name == "agi-0"


@pytest.mark.unit
def test_client_as_context_manager():
    """Test client can be used as context manager."""
    with AGIClient(api_key="test") as client:
        assert client.api_key == "test"
