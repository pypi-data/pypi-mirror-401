"""AGI SDK exceptions."""


class AGIError(Exception):
    """Base exception for all AGI SDK errors."""

    pass


class AuthenticationError(AGIError):
    """401 - Invalid API key."""

    pass


class PermissionError(AGIError):
    """403 - Insufficient permissions."""

    pass


class NotFoundError(AGIError):
    """404 - Resource not found."""

    pass


class RateLimitError(AGIError):
    """429 - Rate limit exceeded."""

    pass


class APIError(AGIError):
    """5xx - Server error."""

    pass


class AgentExecutionError(AGIError):
    """Agent task execution failed."""

    pass
