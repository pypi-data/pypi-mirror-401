"""Shared type definitions."""

from typing import Literal

# Session status types
SessionStatus = Literal["ready", "running", "waiting_for_input", "paused", "finished", "error"]

# Message types
MessageType = Literal["THOUGHT", "QUESTION", "USER", "DONE", "ERROR", "LOG"]

# SSE Event types
EventType = Literal[
    "step",
    "thought",
    "question",
    "done",
    "error",
    "log",
    "paused",
    "resumed",
    "heartbeat",
    "user",  # User message events
]

# Snapshot mode types
SnapshotMode = Literal["none", "memory", "filesystem"]
