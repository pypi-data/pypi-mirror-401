"""Result types for task execution."""

from __future__ import annotations

import base64
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_serializer

T = TypeVar("T")


class Screenshot(BaseModel):
    """
    Browser screenshot with image data and metadata.

    Capture the current browser state as an image. Use session.screenshot()
    to obtain a screenshot, then save it to disk with the save() method.

    Example:
        >>> screenshot = session.screenshot()
        >>> screenshot.save("screenshot.png")
        >>> print(f"Size: {screenshot.width}x{screenshot.height}")
        >>> print(f"URL: {screenshot.url}")
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: bytes = Field(description="Screenshot image data")
    format: str = Field(default="png", description="Image format (png, jpg)")
    timestamp: datetime = Field(description="Screenshot timestamp")
    width: int = Field(description="Image width in pixels")
    height: int = Field(description="Image height in pixels")
    url: str = Field(description="Current page URL")
    title: str = Field(description="Current page title")

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime, _info: Any) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()

    @field_serializer("data")
    def serialize_data(self, value: bytes, _info: Any) -> str:
        """Serialize bytes to hex string."""
        return value.hex()

    def save(self, path: str) -> None:
        """Save screenshot to file.

        Args:
            path: File path to save to (e.g., "screenshot.png")

        Example:
            >>> screenshot = session.screenshot()
            >>> screenshot.save("page.png")
        """
        with open(path, "wb") as f:
            f.write(self.data)

    @classmethod
    def from_base64(
        cls, base64_data: str, url: str, title: str, timestamp: datetime | None = None
    ) -> Screenshot:
        """Create Screenshot from base64 data URL.

        Args:
            base64_data: Base64-encoded data URL (e.g., "data:image/jpeg;base64,...")
            url: Current page URL
            title: Current page title
            timestamp: Screenshot timestamp (defaults to now)

        Returns:
            Screenshot instance with decoded image data
        """
        # Parse data URL format: "data:image/jpeg;base64,..."
        if "," in base64_data:
            header, encoded = base64_data.split(",", 1)
        else:
            # Assume it's just base64 without header
            encoded = base64_data
            header = "data:image/png;base64"

        # Decode base64 to bytes
        image_data = base64.b64decode(encoded)

        # Determine format from header
        if "jpeg" in header.lower() or "jpg" in header.lower():
            fmt = "jpg"
        else:
            fmt = "png"

        # Extract image dimensions
        width, height = cls._get_image_dimensions(image_data, fmt)

        return cls(
            data=image_data,
            format=fmt,
            timestamp=timestamp or datetime.now(),
            width=width,
            height=height,
            url=url,
            title=title,
        )

    @staticmethod
    def _get_image_dimensions(data: bytes, fmt: str) -> tuple[int, int]:
        """Extract width and height from image data.

        Args:
            data: Raw image bytes
            fmt: Image format (png, jpg)

        Returns:
            Tuple of (width, height)
        """
        try:
            if fmt == "png":
                # PNG: width/height at bytes 16-24
                if len(data) >= 24:
                    width = int.from_bytes(data[16:20], byteorder="big")
                    height = int.from_bytes(data[20:24], byteorder="big")
                    return width, height
            elif fmt in ("jpg", "jpeg"):
                # JPEG: scan for SOF0 marker (0xFFC0)
                i = 0
                while i < len(data) - 9:
                    if data[i] == 0xFF and data[i + 1] == 0xC0:
                        height = int.from_bytes(data[i + 5 : i + 7], byteorder="big")
                        width = int.from_bytes(data[i + 7 : i + 9], byteorder="big")
                        return width, height
                    i += 1
        except Exception:
            pass

        # Fallback if parsing fails
        return 0, 0


class TaskMetadata(BaseModel):
    """
    Task execution metadata and performance metrics.

    Contains information about how the task was executed, including duration,
    number of steps, and success status. Access via result.metadata.

    Example:
        >>> result = session.run_task("Find hotels in Paris")
        >>> print(f"Duration: {result.metadata.duration}s")
        >>> print(f"Steps taken: {result.metadata.steps}")
        >>> print(f"Success: {result.metadata.success}")
    """

    task_id: str | int = Field(description="Unique task identifier")
    session_id: str | None = Field(default=None, description="Session ID if applicable")
    duration: float = Field(description="Execution time in seconds")
    cost: float = Field(default=0.0, description="Task cost in USD (not yet provided by API)")
    timestamp: datetime = Field(description="Task completion timestamp")
    steps: int = Field(description="Number of steps executed")
    success: bool = Field(description="Whether task succeeded")

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime, _info: Any) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()


class TaskResult(BaseModel, Generic[T]):
    """
    Result of task execution.

    The data field contains the task output, typically as a dictionary.
    Metadata provides execution information like duration and steps.

    Example:
        >>> result = session.run_task("Compare flight prices from NYC to London")
        >>> print(result.data)  # Dict with flight comparison data
        >>> print(f"Duration: {result.metadata.duration}s")
        >>> print(f"Steps: {result.metadata.steps}")
    """

    data: T = Field(description="Task output data")
    metadata: TaskMetadata = Field(description="Execution metadata")
