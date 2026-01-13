"""HTTP client for AGI API."""

from __future__ import annotations

import time
from typing import Any

import httpx

from agi.exceptions import (
    AGIError,
    APIError,
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)


class HTTPClient:
    """HTTP client with retry logic and error handling."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.agi.tech",
        timeout: int = 60,
        max_retries: int = 3,
    ):
        """Initialize HTTP client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts for 5xx errors
        """
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )
        self._max_retries = max_retries

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path
            **kwargs: Additional arguments for httpx.request()

        Returns:
            HTTP response

        Raises:
            AGIError: On API errors
        """
        last_exception: httpx.HTTPStatusError | None = None

        for attempt in range(self._max_retries):
            try:
                response = self._client.request(method, path, **kwargs)
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self._max_retries - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    last_exception = e
                    continue

                self._handle_error(e.response)
                raise

            except (httpx.RequestError, httpx.TimeoutException) as e:
                if attempt < self._max_retries - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
                raise APIError(f"Request failed: {str(e)}") from e

        if last_exception:
            raise APIError(f"Max retries exceeded: {str(last_exception)}") from last_exception

        raise APIError("Request failed")

    def _handle_error(self, response: httpx.Response) -> None:
        """Map HTTP errors to SDK exceptions.

        Args:
            response: HTTP response with error status

        Raises:
            Specific AGIError subclass based on status code
        """
        status_code = response.status_code

        try:
            error_data = response.json()
            error_message = error_data.get("detail", response.text)
        except Exception:
            error_message = response.text

        if status_code == 401:
            raise AuthenticationError(f"Authentication failed: {error_message}")
        elif status_code == 403:
            raise PermissionError(f"Permission denied: {error_message}")
        elif status_code == 404:
            raise NotFoundError(f"Resource not found: {error_message}")
        elif status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {error_message}")
        elif status_code >= 500:
            raise APIError(f"Server error ({status_code}): {error_message}")
        else:
            raise AGIError(f"API error ({status_code}): {error_message}")

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> HTTPClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
