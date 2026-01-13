"""Session context manager for high-level API."""

from __future__ import annotations

import time
from collections.abc import Iterator
from datetime import datetime
from typing import TYPE_CHECKING, Any

from agi.exceptions import AgentExecutionError
from agi.types.results import Screenshot, TaskMetadata, TaskResult

if TYPE_CHECKING:
    from agi.client import AGIClient
    from agi.types.sessions import (
        ExecuteStatusResponse,
        MessagesResponse,
        NavigateResponse,
        SSEEvent,
        SuccessResponse,
    )


class SessionContext:
    """High-level session context manager matching docs pattern.

    This provides the simple API shown in documentation:
        with client.session("agi-0") as session:
            result = session.run_task("Find cheapest iPhone 15...")

    Example:
        >>> from agi import AGIClient
        >>> client = AGIClient(api_key="...")
        >>>
        >>> with client.session("agi-0") as session:
        ...     result = session.run_task("Find flights SFO→JFK under $450")
        ...     print(result)
    """

    def __init__(
        self,
        client: AGIClient,
        agent_name: str = "agi-0",
        **create_kwargs: Any,
    ):
        """Initialize session context.

        Args:
            client: AGIClient instance
            agent_name: Agent model to use
            **create_kwargs: Additional arguments for session creation
                (webhook_url, goal, max_steps, restore_from_environment_id)
        """
        self._client = client
        self._agent_name = agent_name
        self._create_kwargs = create_kwargs
        self.session_id: str | None = None
        self.vnc_url: str | None = None
        self.agent_url: str | None = None

    def __enter__(self) -> SessionContext:
        """Create session on context entry.

        Returns:
            SessionContext instance
        """
        response = self._client.sessions.create(
            agent_name=self._agent_name,
            **self._create_kwargs,
        )
        self.session_id = response.session_id
        self.vnc_url = response.vnc_url
        self.agent_url = response.agent_url
        return self

    def __exit__(self, *args: Any) -> None:
        """Delete session on context exit."""
        if self.session_id:
            try:
                self._client.sessions.delete(self.session_id)
            except Exception:
                pass

    def run_task(
        self,
        task: str,
        start_url: str | None = None,
        timeout: int = 600,
        poll_interval: float = 3.0,
    ) -> TaskResult:
        """Send task and wait for completion using polling.

        This is the primary method matching the docs example.
        It sends the task message and polls for completion status.

        Args:
            task: Natural language task description
            start_url: Optional starting URL for the task
            timeout: Maximum time to wait in seconds (default: 600)
            poll_interval: Polling interval in seconds (default: 3.0)

        Returns:
            TaskResult with data and metadata

        Raises:
            AgentExecutionError: If task fails or times out
            ValueError: If session not created

        Example:
            >>> with client.session("agi-0") as session:
            ...     result = session.run_task(
            ...         "Find three nonstop SFO→JFK flights next month under $450"
            ...     )
            ...     print(result.data)
            ...     print(f"Duration: {result.metadata.duration}s")
        """
        if not self.session_id:
            raise ValueError("Session not created. Use context manager 'with' statement.")

        self._client.sessions.send_message(
            self.session_id,
            message=task,
            start_url=start_url,
        )

        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise AgentExecutionError(
                    f"Task exceeded timeout of {timeout}s (elapsed: {elapsed:.1f}s)"
                )

            status_response = self._client.sessions.get_status(self.session_id)

            if status_response.status in ("finished", "waiting_for_input"):
                messages_response = self._client.sessions.get_messages(self.session_id)
                messages = messages_response.messages

                # Find DONE or QUESTION message
                done_msg = None
                for msg in messages:
                    if msg.type in ("DONE", "QUESTION"):
                        done_msg = msg
                        break

                if not done_msg:
                    raise AgentExecutionError(
                        f"Task status '{status_response.status}' but no DONE/QUESTION message found."
                    )

                # Extract task data
                content = done_msg.content
                if isinstance(content, dict):
                    data = content
                else:
                    data = {"content": content} if content else {}

                duration = time.time() - start_time
                steps = sum(1 for msg in messages if msg.type in ("THOUGHT", "QUESTION", "DONE"))

                metadata = TaskMetadata(
                    task_id=done_msg.id,
                    session_id=self.session_id,
                    duration=duration,
                    cost=0.0,
                    timestamp=datetime.now(),
                    steps=steps,
                    success=True,
                )

                return TaskResult(data=data, metadata=metadata)

            if status_response.status == "error":
                messages_response = self._client.sessions.get_messages(self.session_id)

                error_details = "Unknown error"
                for msg in messages_response.messages:
                    if msg.type == "ERROR":
                        if isinstance(msg.content, str):
                            error_details = msg.content if msg.content else "Unknown error"
                        else:
                            error_details = str(msg.content)
                        break

                raise AgentExecutionError(f"Task failed: {error_details}")

            time.sleep(poll_interval)

    def pause(self) -> SuccessResponse:
        """Pause task execution.

        Returns:
            SuccessResponse confirming pause
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.pause(self.session_id)

    def resume(self) -> SuccessResponse:
        """Resume paused task.

        Returns:
            SuccessResponse confirming resume
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.resume(self.session_id)

    def cancel(self) -> SuccessResponse:
        """Cancel task execution.

        Returns:
            SuccessResponse confirming cancellation
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.cancel(self.session_id)

    def navigate(self, url: str) -> NavigateResponse:
        """Navigate browser to URL.

        Args:
            url: URL to navigate to

        Returns:
            NavigateResponse with current URL
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.navigate(self.session_id, url)

    def screenshot(self) -> Screenshot:
        """Get browser screenshot.

        Returns:
            Screenshot with decoded image data and save() method

        Example:
            >>> screenshot = session.screenshot()
            >>> screenshot.save("page.png")
            >>> print(f"Size: {screenshot.width}x{screenshot.height}")
        """
        if not self.session_id:
            raise ValueError("Session not created")

        response = self._client.sessions.screenshot(self.session_id)
        return Screenshot.from_base64(
            base64_data=response.screenshot, url=response.url, title=response.title
        )

    def send_message(
        self,
        message: str,
        start_url: str | None = None,
        config_updates: dict[str, Any] | None = None,
    ) -> SuccessResponse:
        """Send message to agent to start a task or respond to questions.

        Args:
            message: Message content (task instruction or response)
            start_url: Optional starting URL for the task
            config_updates: Optional configuration updates

        Returns:
            SuccessResponse confirming message sent

        Example:
            >>> with client.session("agi-0") as session:
            ...     session.send_message("Find flights from SFO to JFK under $450")
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.send_message(
            self.session_id, message, start_url, config_updates
        )

    def get_status(self) -> ExecuteStatusResponse:
        """Get current execution status of the session.

        Returns:
            ExecuteStatusResponse with status ("running", "finished", etc.)

        Example:
            >>> with client.session("agi-0") as session:
            ...     session.send_message("Research topic...")
            ...     status = session.get_status()
            ...     print(status.status)
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.get_status(self.session_id)

    def get_messages(self, after_id: int = 0, sanitize: bool = True) -> MessagesResponse:
        """Get messages from the session.

        Args:
            after_id: Return messages with ID > after_id (for polling)
            sanitize: Filter out system messages, prompts, and images

        Returns:
            MessagesResponse with messages list and status

        Example:
            >>> with client.session("agi-0") as session:
            ...     messages = session.get_messages(after_id=0)
            ...     for msg in messages.messages:
            ...         print(f"[{msg.type}] {msg.content}")
        """
        if not self.session_id:
            raise ValueError("Session not created")
        return self._client.sessions.get_messages(self.session_id, after_id, sanitize)

    def stream_events(
        self,
        event_types: list[str] | None = None,
        sanitize: bool = True,
        include_history: bool = True,
    ) -> Iterator[SSEEvent]:
        """Stream real-time events from the session via Server-Sent Events.

        Args:
            event_types: Filter specific event types (e.g., ["thought", "done"])
            sanitize: Filter out system messages
            include_history: Include historical messages on connection

        Yields:
            SSEEvent objects with id, event type, and data

        Example:
            >>> with client.session("agi-0") as session:
            ...     session.send_message("Research company XYZ")
            ...     for event in session.stream_events():
            ...         if event.event == "thought":
            ...             print(f"Agent: {event.data}")
            ...         elif event.event == "done":
            ...             print(f"Result: {event.data}")
            ...             break
        """
        if not self.session_id:
            raise ValueError("Session not created")
        yield from self._client.sessions.stream_events(
            self.session_id, event_types, sanitize, include_history
        )
