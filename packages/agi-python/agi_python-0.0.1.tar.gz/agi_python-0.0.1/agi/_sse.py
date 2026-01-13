"""Server-Sent Events (SSE) streaming client."""

import json
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from agi.types.sessions import SSEEvent

if TYPE_CHECKING:
    from agi._http import HTTPClient


class SSEClient:
    """Client for handling Server-Sent Events streams."""

    def __init__(self, http: "HTTPClient"):
        """Initialize SSE client.

        Args:
            http: HTTP client instance
        """
        self._http = http

    def stream(self, path: str, params: dict[str, Any] | None = None) -> Iterator[SSEEvent]:
        """Connect to SSE endpoint and yield events.

        Args:
            path: API endpoint path
            params: Query parameters

        Yields:
            SSEEvent objects

        Example:
            >>> for event in sse.stream("/v1/sessions/123/events"):
            ...     if event.event == "done":
            ...         break
        """
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        with self._http._client.stream("GET", path, params=clean_params) as response:
            response.raise_for_status()

            event_id: str | None = None
            event_type: str | None = None
            data_lines: list[str] = []

            for line in response.iter_lines():
                line = line.strip()

                if not line:
                    if event_type and data_lines:
                        data_str = "".join(data_lines)
                        try:
                            data = json.loads(data_str)
                        except json.JSONDecodeError:
                            data = {"content": data_str}

                        yield SSEEvent(
                            id=event_id,
                            event=event_type,  # type: ignore
                            data=data,
                        )

                        event_id = None
                        event_type = None
                        data_lines = []
                    continue

                if line.startswith("id:"):
                    event_id = line[3:].strip()
                elif line.startswith("event:"):
                    event_type = line[6:].strip()
                elif line.startswith("data:"):
                    data_lines.append(line[5:].strip())
                elif line.startswith(":"):
                    continue
