"""Session-related type definitions."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from agi.types.shared import EventType, MessageType, SessionStatus

# Request Models


class CreateSessionRequest(BaseModel):
    """Request to create a new session."""

    agent_name: str = Field(default="agi-0", description="Agent model to use")
    webhook_url: str | None = Field(
        default=None, description="Webhook URL for session event notifications"
    )
    goal: str | None = Field(default=None, description="Task goal (optional, can be set later)")
    max_steps: int = Field(default=100, description="Maximum number of agent steps")
    restore_from_environment_id: str | None = Field(
        default=None, description="Environment UUID to restore from"
    )


class SendMessageRequest(BaseModel):
    """Request to send a message to the agent."""

    message: str = Field(..., description="Message content")
    start_url: str | None = Field(default=None, description="Optional starting URL")
    config_updates: dict[str, Any] | None = Field(
        default=None, description="Optional configuration updates"
    )


class NavigateRequest(BaseModel):
    """Request to navigate browser to a URL."""

    url: str = Field(..., description="URL to navigate to")


# Response Models


class SessionResponse(BaseModel):
    """Response containing session information."""

    session_id: str = Field(..., description="Session UUID")
    vnc_url: str | None = Field(None, description="VNC URL for browser access")
    agent_url: str | None = Field(None, description="Agent service URL (desktop mode)")
    agent_name: str = Field(..., description="Agent name")
    status: str = Field(..., description="Session status")
    created_at: datetime = Field(..., description="Session creation timestamp")
    environment_id: str | None = Field(None, description="Environment UUID for restore")
    goal: str | None = Field(None, description="Task goal")


class ExecuteStatusResponse(BaseModel):
    """Response containing task execution status."""

    status: SessionStatus = Field(..., description="Current execution status")


class MessageResponse(BaseModel):
    """Single message from agent."""

    id: int = Field(..., description="Message ID")
    type: MessageType = Field(..., description="Message type")
    content: str | dict[str, Any] | list[dict[str, Any]] = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO timestamp")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class MessagesResponse(BaseModel):
    """Response containing message stream and status."""

    messages: list[MessageResponse] = Field(default_factory=list, description="List of messages")
    status: str = Field(..., description="Current execution status")
    has_agent: bool = Field(True, description="Whether agent is connected")


class SSEEvent(BaseModel):
    """Server-Sent Event from real-time stream."""

    id: str | None = Field(None, description="Event ID")
    event: EventType = Field(..., description="Event type")
    data: dict[str, Any] = Field(..., description="Event data")


class NavigateResponse(BaseModel):
    """Response from navigation request."""

    current_url: str = Field(..., description="Current URL after navigation")


class ScreenshotResponse(BaseModel):
    """Response containing screenshot data."""

    screenshot: str = Field(..., description="Base64-encoded JPEG data URL")
    url: str = Field(..., description="Current page URL")
    title: str = Field(..., description="Current page title")


class SuccessResponse(BaseModel):
    """Generic success response."""

    success: bool = Field(True, description="Operation success")
    message: str = Field(..., description="Success message")


class DeleteResponse(BaseModel):
    """Response from delete operation."""

    success: bool = Field(True, description="Operation success")
    deleted: bool = Field(True, description="Whether resource was deleted")
    message: str = Field(..., description="Response message")
