"""Main AGI API client."""

from __future__ import annotations

import os
from typing import Any

from agi._http import HTTPClient
from agi._session_context import SessionContext
from agi.resources.sessions import SessionsResource


class AGIClient:
    """Official Python client for the AGI.tech API.

    The AGIClient provides access to the AGI API for creating and managing
    AI agent sessions that can perform complex web tasks.

    Example:
        Simple usage with context manager (recommended):

        >>> from agi import AGIClient
        >>> client = AGIClient(api_key="your_api_key")
        >>>
        >>> with client.session("agi-0") as session:
        ...     result = session.run_task("Find cheapest iPhone 15 on Amazon")
        ...     print(result)

        Advanced usage with direct API access:

        >>> session = client.sessions.create(
        ...     agent_name="agi-0",
        ...     webhook_url="https://yourapp.com/webhook"
        ... )
        >>> client.sessions.send_message(session.session_id, "Find flights...")
        >>>
        >>> for event in client.sessions.stream_events(session.session_id):
        ...     if event.event == "thought":
        ...         print(f"Agent: {event.data}")
        ...     elif event.event == "done":
        ...         break
        >>>
        >>> client.sessions.delete(session.session_id)
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.agi.tech",
        timeout: int = 60,
        max_retries: int = 3,
    ):
        """Initialize the AGI API client.

        Args:
            api_key: API key for authentication. If not provided, will look
                for AGI_API_KEY environment variable.
            base_url: Base URL for the API (default: https://api.agi.tech)
            timeout: Request timeout in seconds (default: 60)
            max_retries: Maximum number of retry attempts for 5xx errors (default: 3)

        Raises:
            ValueError: If api_key is not provided and AGI_API_KEY env var is not set

        Example:
            >>> client = AGIClient(api_key="your_api_key")
            >>> # Or use environment variable:
            >>> import os
            >>> os.environ["AGI_API_KEY"] = "your_api_key"
            >>> client = AGIClient()
        """
        self.api_key = api_key or os.getenv("AGI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "api_key is required. Either pass it as a parameter or set "
                "the AGI_API_KEY environment variable."
            )

        self._http = HTTPClient(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.sessions = SessionsResource(self._http)

    def session(
        self,
        agent_name: str = "agi-0",
        **kwargs: Any,
    ) -> SessionContext:
        """Create a session context manager for easy session lifecycle management.

        This is the recommended way to use the SDK, matching the pattern shown
        in the documentation. The context manager automatically creates and
        deletes the session.

        Args:
            agent_name: Agent model to use (e.g., "agi-0", "agi-0-fast")
            **kwargs: Additional session creation parameters:
                - webhook_url (str): URL for session event notifications
                - goal (str): Task goal to set upfront
                - max_steps (int): Maximum number of agent steps (default: 100)
                - restore_from_environment_id (str): Environment UUID to restore

        Returns:
            SessionContext manager

        Example:
            >>> with client.session("agi-0") as session:
            ...     result = session.run_task("Find flights SFO→JFK under $450")
            ...     print(result)
            >>>
            >>> # With webhook
            >>> with client.session(
            ...     "agi-0",
            ...     webhook_url="https://yourapp.com/webhook"
            ... ) as session:
            ...     result = session.run_task("Research company XYZ")
        """
        return SessionContext(self, agent_name=agent_name, **kwargs)

    def close(self) -> None:
        """Close the HTTP client and cleanup resources.

        Note: Usually not needed as the client will cleanup automatically.

        Example:
            >>> client = AGIClient(api_key="...")
            >>> # ... use client ...
            >>> client.close()
        """
        self._http.close()

    def __enter__(self) -> AGIClient:
        """Support using AGIClient as a context manager."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Cleanup when used as context manager."""
        self.close()
