"""Unit tests for exception hierarchy and error handling."""

import pytest

from agi.exceptions import (
    AgentExecutionError,
    AGIError,
    APIError,
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)


@pytest.mark.unit
class TestExceptionHierarchy:
    """Tests for exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_agi_error(self):
        """Test that all custom exceptions inherit from AGIError."""
        assert issubclass(AuthenticationError, AGIError)
        assert issubclass(PermissionError, AGIError)
        assert issubclass(NotFoundError, AGIError)
        assert issubclass(RateLimitError, AGIError)
        assert issubclass(APIError, AGIError)
        assert issubclass(AgentExecutionError, AGIError)

    def test_authentication_error_instantiation(self):
        """Test that AuthenticationError can be instantiated and raised."""
        error = AuthenticationError("Invalid API key")
        assert str(error) == "Invalid API key"
        assert isinstance(error, AGIError)

    def test_not_found_error_instantiation(self):
        """Test that NotFoundError can be instantiated and raised."""
        error = NotFoundError("Session not found")
        assert str(error) == "Session not found"
        assert isinstance(error, AGIError)

    def test_rate_limit_error_instantiation(self):
        """Test that RateLimitError can be instantiated and raised."""
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert isinstance(error, AGIError)

    def test_api_error_instantiation(self):
        """Test that APIError can be instantiated and raised."""
        error = APIError("Server error")
        assert str(error) == "Server error"
        assert isinstance(error, AGIError)

    def test_agent_execution_error_instantiation(self):
        """Test that AgentExecutionError can be instantiated and raised."""
        error = AgentExecutionError("Task failed")
        assert str(error) == "Task failed"
        assert isinstance(error, AGIError)

    def test_catching_base_exception(self):
        """Test that catching AGIError catches all custom exceptions."""
        with pytest.raises(AGIError):
            raise AuthenticationError("Test")

        with pytest.raises(AGIError):
            raise NotFoundError("Test")

        with pytest.raises(AGIError):
            raise RateLimitError("Test")

        with pytest.raises(AGIError):
            raise APIError("Test")

    def test_exception_message_preserved(self):
        """Test that exception messages are preserved correctly."""
        message = "Custom error message with details"

        error = AuthenticationError(message)
        assert str(error) == message

        error = NotFoundError(message)
        assert str(error) == message

        error = APIError(message)
        assert str(error) == message


@pytest.mark.unit
class TestErrorRaising:
    """Tests for raising and catching exceptions."""

    def test_raise_authentication_error(self):
        """Test raising and catching AuthenticationError."""
        with pytest.raises(AuthenticationError, match="Invalid"):
            raise AuthenticationError("Invalid API key")

    def test_raise_not_found_error(self):
        """Test raising and catching NotFoundError."""
        with pytest.raises(NotFoundError, match="not found"):
            raise NotFoundError("Resource not found")

    def test_raise_rate_limit_error(self):
        """Test raising and catching RateLimitError."""
        with pytest.raises(RateLimitError, match="exceeded"):
            raise RateLimitError("Rate limit exceeded")

    def test_raise_api_error(self):
        """Test raising and catching APIError."""
        with pytest.raises(APIError, match="Server"):
            raise APIError("Server error")

    def test_catch_with_base_class(self):
        """Test that specific errors can be caught with base AGIError."""
        try:
            raise NotFoundError("Not found")
        except AGIError as e:
            assert isinstance(e, NotFoundError)
            assert isinstance(e, AGIError)


@pytest.mark.unit
class TestExceptionTypes:
    """Tests for exception type checking."""

    def test_exception_types_are_distinct(self):
        """Test that exception types are distinct classes."""
        assert AuthenticationError is not NotFoundError
        assert NotFoundError is not APIError
        assert RateLimitError is not AuthenticationError

    def test_exception_isinstance_checks(self):
        """Test isinstance checks work correctly."""
        auth_error = AuthenticationError("Test")
        assert isinstance(auth_error, AuthenticationError)
        assert isinstance(auth_error, AGIError)
        assert not isinstance(auth_error, NotFoundError)

        not_found = NotFoundError("Test")
        assert isinstance(not_found, NotFoundError)
        assert isinstance(not_found, AGIError)
        assert not isinstance(not_found, AuthenticationError)
