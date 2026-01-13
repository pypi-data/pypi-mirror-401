"""Sessions API resource."""

from __future__ import annotations

import builtins
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from agi.types.sessions import (
    DeleteResponse,
    ExecuteStatusResponse,
    MessagesResponse,
    NavigateResponse,
    ScreenshotResponse,
    SessionResponse,
    SSEEvent,
    SuccessResponse,
)
from agi.types.shared import SnapshotMode

if TYPE_CHECKING:
    from agi._http import HTTPClient


class SessionsResource:
    """Sessions API resource providing all session-related operations."""

    def __init__(self, http: HTTPClient):
        """Initialize sessions resource.

        Args:
            http: HTTP client instance
        """
        self._http = http

    # ===== SESSION MANAGEMENT (5 endpoints) =====

    def create(
        self,
        agent_name: str = "agi-0",
        webhook_url: str | None = None,
        goal: str | None = None,
        max_steps: int = 100,
        restore_from_environment_id: str | None = None,
    ) -> SessionResponse:
        """Create a new agent session.

        Args:
            agent_name: Agent model to use (e.g., "agi-0", "agi-0-fast")
            webhook_url: URL for session event notifications
            goal: Task goal (optional, can be set later via send_message)
            max_steps: Maximum number of agent steps (default: 100)
            restore_from_environment_id: Environment UUID to restore from

        Returns:
            SessionResponse with session_id, vnc_url, status, etc.

        Example:
            >>> session = client.sessions.create(
            ...     agent_name="agi-0",
            ...     goal="Find cheapest iPhone 15 on Amazon"
            ... )
            >>> print(session.session_id)
        """
        payload = {
            "agent_name": agent_name,
            "max_steps": max_steps,
        }

        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        if goal is not None:
            payload["goal"] = goal
        if restore_from_environment_id is not None:
            payload["restore_from_environment_id"] = restore_from_environment_id

        response = self._http.request("POST", "/v1/sessions", json=payload)
        return SessionResponse(**response.json())

    def list(self) -> list[SessionResponse]:
        """List all sessions for the authenticated user.

        Returns:
            List of SessionResponse objects

        Example:
            >>> sessions = client.sessions.list()
            >>> for session in sessions:
            ...     print(f"{session.session_id}: {session.status}")
        """
        response = self._http.request("GET", "/v1/sessions")
        return [SessionResponse(**s) for s in response.json()]

    def get(self, session_id: str) -> SessionResponse:
        """Get details for a specific session.

        Args:
            session_id: Session UUID

        Returns:
            SessionResponse with session details

        Raises:
            NotFoundError: If session doesn't exist

        Example:
            >>> session = client.sessions.get("123e4567-e89b-12d3-a456-426614174000")
            >>> print(session.status)
        """
        response = self._http.request("GET", f"/v1/sessions/{session_id}")
        return SessionResponse(**response.json())

    def delete(
        self,
        session_id: str,
        save_snapshot_mode: SnapshotMode = "none",
    ) -> DeleteResponse:
        """Delete a session and cleanup its resources.

        Args:
            session_id: Session UUID
            save_snapshot_mode: Snapshot mode - "none", "memory", or "filesystem"

        Returns:
            DeleteResponse confirming deletion

        Example:
            >>> client.sessions.delete("123e4567-e89b-12d3-a456-426614174000")
        """
        response = self._http.request(
            "DELETE",
            f"/v1/sessions/{session_id}",
            params={"save_snapshot_mode": save_snapshot_mode},
        )
        return DeleteResponse(**response.json())

    def delete_all(self) -> DeleteResponse:
        """Delete all sessions for the authenticated user.

        Returns:
            DeleteResponse with count of deleted sessions

        Example:
            >>> result = client.sessions.delete_all()
            >>> print(result.message)
        """
        response = self._http.request("DELETE", "/v1/sessions")
        return DeleteResponse(**response.json())

    # ===== AGENT INTERACTION (4 endpoints) =====

    def send_message(
        self,
        session_id: str,
        message: str,
        start_url: str | None = None,
        config_updates: dict[str, Any] | None = None,
    ) -> SuccessResponse:
        """Send a message to the agent to start a task or respond to questions.

        Args:
            session_id: Session UUID
            message: Message content (task instruction or response)
            start_url: Optional starting URL for the task
            config_updates: Optional configuration updates

        Returns:
            SuccessResponse confirming message was sent

        Example:
            >>> client.sessions.send_message(
            ...     session_id="123...",
            ...     message="Find flights from SFO to JFK under $450"
            ... )
        """
        payload: dict[str, Any] = {"message": message}

        if start_url is not None:
            payload["start_url"] = start_url
        if config_updates is not None:
            payload["config_updates"] = config_updates

        response = self._http.request(
            "POST",
            f"/v1/sessions/{session_id}/message",
            json=payload,
        )
        return SuccessResponse(**response.json())

    def get_status(self, session_id: str) -> ExecuteStatusResponse:
        """Get the current execution status of a session.

        Args:
            session_id: Session UUID

        Returns:
            ExecuteStatusResponse with status ("running", "finished", etc.)

        Example:
            >>> status = client.sessions.get_status("123...")
            >>> if status.status == "finished":
            ...     print("Task completed!")
        """
        response = self._http.request("GET", f"/v1/sessions/{session_id}/status")
        return ExecuteStatusResponse(**response.json())

    def get_messages(
        self,
        session_id: str,
        after_id: int = 0,
        sanitize: bool = True,
    ) -> MessagesResponse:
        """Poll for messages and updates from the agent.

        Args:
            session_id: Session UUID
            after_id: Return messages with ID > after_id (for polling)
            sanitize: Filter out system messages, prompts, and images

        Returns:
            MessagesResponse with messages list and status

        Example:
            >>> messages = client.sessions.get_messages("123...", after_id=0)
            >>> for msg in messages.messages:
            ...     print(f"[{msg.type}] {msg.content}")
        """
        response = self._http.request(
            "GET",
            f"/v1/sessions/{session_id}/messages",
            params={"after_id": after_id, "sanitize": sanitize},
        )
        return MessagesResponse(**response.json())

    def stream_events(
        self,
        session_id: str,
        event_types: builtins.list[str] | None = None,
        sanitize: bool = True,
        include_history: bool = True,
    ) -> Iterator[SSEEvent]:
        """Stream real-time events from the session via Server-Sent Events.

        Args:
            session_id: Session UUID
            event_types: Filter specific event types (e.g., ["thought", "done"])
            sanitize: Filter out system messages
            include_history: Include historical messages on connection

        Yields:
            SSEEvent objects with id, event type, and data

        Example:
            >>> for event in client.sessions.stream_events("123..."):
            ...     if event.event == "thought":
            ...         print(f"Agent: {event.data}")
            ...     elif event.event == "done":
            ...         print(f"Result: {event.data}")
            ...         break
        """
        from agi._sse import SSEClient

        sse = SSEClient(self._http)
        params: dict[str, Any] = {
            "sanitize": sanitize,
            "include_history": include_history,
        }

        if event_types:
            params["event_types"] = ",".join(event_types)

        yield from sse.stream(f"/v1/sessions/{session_id}/events", params=params)

    # ===== SESSION CONTROL (3 endpoints) =====

    def pause(self, session_id: str) -> SuccessResponse:
        """Temporarily pause task execution.

        Args:
            session_id: Session UUID

        Returns:
            SuccessResponse confirming pause

        Example:
            >>> client.sessions.pause("123...")
        """
        response = self._http.request("POST", f"/v1/sessions/{session_id}/pause")
        return SuccessResponse(**response.json())

    def resume(self, session_id: str) -> SuccessResponse:
        """Resume a paused task.

        Args:
            session_id: Session UUID

        Returns:
            SuccessResponse confirming resume

        Example:
            >>> client.sessions.resume("123...")
        """
        response = self._http.request("POST", f"/v1/sessions/{session_id}/resume")
        return SuccessResponse(**response.json())

    def cancel(self, session_id: str) -> SuccessResponse:
        """Cancel task execution.

        Args:
            session_id: Session UUID

        Returns:
            SuccessResponse confirming cancellation

        Example:
            >>> client.sessions.cancel("123...")
        """
        response = self._http.request("POST", f"/v1/sessions/{session_id}/cancel")
        return SuccessResponse(**response.json())

    # ===== BROWSER CONTROL (2 endpoints) =====

    def navigate(self, session_id: str, url: str) -> NavigateResponse:
        """Navigate the browser to a specific URL.

        Args:
            session_id: Session UUID
            url: URL to navigate to

        Returns:
            NavigateResponse with current URL

        Example:
            >>> client.sessions.navigate("123...", "https://amazon.com")
        """
        response = self._http.request(
            "POST",
            f"/v1/sessions/{session_id}/navigate",
            json={"url": url},
        )
        return NavigateResponse(**response.json())

    def screenshot(self, session_id: str) -> ScreenshotResponse:
        """Get a screenshot of the browser.

        Args:
            session_id: Session UUID

        Returns:
            ScreenshotResponse with base64-encoded image, URL, and title

        Example:
            >>> screenshot = client.sessions.screenshot("123...")
            >>> print(screenshot.url)
            >>> # screenshot.screenshot contains base64 JPEG data
        """
        response = self._http.request("GET", f"/v1/sessions/{session_id}/screenshot")
        return ScreenshotResponse(**response.json())
