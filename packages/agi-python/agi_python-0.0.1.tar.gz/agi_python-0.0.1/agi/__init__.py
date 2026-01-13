"""Official Python SDK for AGI.tech API.

The agi package provides a complete Python SDK for the AGI.tech API,
enabling developers to create and manage AI agent sessions that can perform
complex web tasks.

Example:
    >>> from agi import AGIClient
    >>>
    >>> client = AGIClient(api_key="your_api_key")
    >>>
    >>> with client.session("agi-0") as session:
    ...     result = session.run_task(
    ...         "Find three nonstop SFO→JFK flights next month under $450"
    ...     )
    ...     print(result)
"""

from agi.client import AGIClient
from agi.exceptions import (
    AgentExecutionError,
    AGIError,
    APIError,
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)
from agi.types.results import Screenshot, TaskMetadata, TaskResult
from agi.types.sessions import (
    DeleteResponse,
    ExecuteStatusResponse,
    MessageResponse,
    MessagesResponse,
    NavigateResponse,
    ScreenshotResponse,
    SessionResponse,
    SSEEvent,
    SuccessResponse,
)
from agi.types.shared import EventType, MessageType, SessionStatus, SnapshotMode

__version__ = "0.0.1"

__all__ = [
    "AGIClient",
    "AGIError",
    "APIError",
    "AgentExecutionError",
    "AuthenticationError",
    "NotFoundError",
    "PermissionError",
    "RateLimitError",
    "SessionResponse",
    "SSEEvent",
    "MessageResponse",
    "MessagesResponse",
    "ExecuteStatusResponse",
    "DeleteResponse",
    "NavigateResponse",
    "Screenshot",
    "ScreenshotResponse",
    "SuccessResponse",
    "TaskResult",
    "TaskMetadata",
    "EventType",
    "MessageType",
    "SessionStatus",
    "SnapshotMode",
]
