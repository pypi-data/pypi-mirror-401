"""
HTTP client implementation for PlayVideo SDK.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

from playvideo.errors import (
    NetworkError,
    parse_api_error,
)
from playvideo.errors import (
    TimeoutError as PlayVideoTimeoutError,
)
from playvideo.types import ProgressEvent, UploadProgress

if TYPE_CHECKING:
    from playvideo.types import ProgressCallback

DEFAULT_BASE_URL = "https://api.playvideo.dev/api/v1"
DEFAULT_TIMEOUT = 30.0


class SyncHttpClient:
    """Synchronous HTTP client."""

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or DEFAULT_TIMEOUT

        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle HTTP response and raise appropriate errors."""
        request_id = response.headers.get("x-request-id")

        try:
            data: dict[str, Any] = response.json()
        except Exception:
            data = {}

        if not response.is_success:
            raise parse_api_error(response.status_code, data, request_id)

        return data

    def get(self, endpoint: str) -> dict[str, Any]:
        """Make GET request."""
        try:
            response = self._client.get(endpoint)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    def post(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make POST request."""
        try:
            response = self._client.post(endpoint, json=json)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    def patch(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make PATCH request."""
        try:
            response = self._client.patch(endpoint, json=json)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Make DELETE request."""
        try:
            response = self._client.delete(endpoint)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    def upload(
        self,
        endpoint: str,
        file_path: str | Path,
        collection: str,
        on_progress: ProgressCallback | None = None,
    ) -> dict[str, Any]:
        """Upload a file with optional progress callback."""
        path = Path(file_path)
        file_size = path.stat().st_size

        def progress_wrapper(uploaded: int) -> None:
            if on_progress:
                on_progress(
                    UploadProgress(
                        loaded=uploaded,
                        total=file_size,
                        percent=int((uploaded / file_size) * 100) if file_size > 0 else 0,
                    )
                )

        with open(path, "rb") as f:
            # Track progress manually
            if on_progress:
                progress_wrapper(0)

            files = {"file": (path.name, f, "application/octet-stream")}
            data = {"collection": collection}

            try:
                response = self._client.post(
                    endpoint,
                    files=files,
                    data=data,
                    timeout=600.0,  # 10 minute timeout for uploads
                )

                if on_progress:
                    progress_wrapper(file_size)

                return self._handle_response(response)
            except httpx.TimeoutException as e:
                raise PlayVideoTimeoutError(f"Upload timed out: {e}") from e
            except httpx.NetworkError as e:
                raise NetworkError(f"Network error: {e}") from e

    def stream_sse(self, endpoint: str) -> Iterator[ProgressEvent]:
        """Stream SSE events from an endpoint."""
        try:
            with self._client.stream(
                "GET", endpoint, headers={"Accept": "text/event-stream"}
            ) as response:
                if not response.is_success:
                    data = (
                        response.json()
                        if response.headers.get("content-type", "").startswith("application/json")
                        else {}
                    )
                    raise parse_api_error(
                        response.status_code, data, response.headers.get("x-request-id")
                    )

                buffer = ""
                for chunk in response.iter_text():
                    buffer += chunk
                    lines = buffer.split("\n")
                    buffer = lines.pop()  # Keep incomplete line

                    for line in lines:
                        if line.startswith("data: "):
                            import json

                            try:
                                data = json.loads(line[6:])
                                event = _parse_progress_event(data)
                                yield event

                                if event.stage in ("completed", "failed", "timeout"):
                                    return
                            except json.JSONDecodeError:
                                pass
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"SSE stream timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e


class AsyncHttpClient:
    """Asynchronous HTTP client."""

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or DEFAULT_TIMEOUT

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle HTTP response and raise appropriate errors."""
        request_id = response.headers.get("x-request-id")

        try:
            data: dict[str, Any] = response.json()
        except Exception:
            data = {}

        if not response.is_success:
            raise parse_api_error(response.status_code, data, request_id)

        return data

    async def get(self, endpoint: str) -> dict[str, Any]:
        """Make GET request."""
        try:
            response = await self._client.get(endpoint)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    async def post(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make POST request."""
        try:
            response = await self._client.post(endpoint, json=json)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    async def patch(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make PATCH request."""
        try:
            response = await self._client.patch(endpoint, json=json)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    async def delete(self, endpoint: str) -> dict[str, Any]:
        """Make DELETE request."""
        try:
            response = await self._client.delete(endpoint)
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e

    async def upload(
        self,
        endpoint: str,
        file_path: str | Path,
        collection: str,
        on_progress: ProgressCallback | None = None,
    ) -> dict[str, Any]:
        """Upload a file with optional progress callback."""
        path = Path(file_path)
        file_size = path.stat().st_size

        def progress_wrapper(uploaded: int) -> None:
            if on_progress:
                on_progress(
                    UploadProgress(
                        loaded=uploaded,
                        total=file_size,
                        percent=int((uploaded / file_size) * 100) if file_size > 0 else 0,
                    )
                )

        with open(path, "rb") as f:
            if on_progress:
                progress_wrapper(0)

            files = {"file": (path.name, f, "application/octet-stream")}
            data = {"collection": collection}

            try:
                response = await self._client.post(
                    endpoint,
                    files=files,
                    data=data,
                    timeout=600.0,
                )

                if on_progress:
                    progress_wrapper(file_size)

                return self._handle_response(response)
            except httpx.TimeoutException as e:
                raise PlayVideoTimeoutError(f"Upload timed out: {e}") from e
            except httpx.NetworkError as e:
                raise NetworkError(f"Network error: {e}") from e

    async def stream_sse(self, endpoint: str) -> AsyncIterator[ProgressEvent]:
        """Stream SSE events from an endpoint."""
        try:
            async with self._client.stream(
                "GET", endpoint, headers={"Accept": "text/event-stream"}
            ) as response:
                if not response.is_success:
                    data = (
                        response.json()
                        if response.headers.get("content-type", "").startswith("application/json")
                        else {}
                    )
                    raise parse_api_error(
                        response.status_code, data, response.headers.get("x-request-id")
                    )

                buffer = ""
                async for chunk in response.aiter_text():
                    buffer += chunk
                    lines = buffer.split("\n")
                    buffer = lines.pop()

                    for line in lines:
                        if line.startswith("data: "):
                            import json

                            try:
                                data = json.loads(line[6:])
                                event = _parse_progress_event(data)
                                yield event

                                if event.stage in ("completed", "failed", "timeout"):
                                    return
                            except json.JSONDecodeError:
                                pass
        except httpx.TimeoutException as e:
            raise PlayVideoTimeoutError(f"SSE stream timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e


def _parse_progress_event(data: dict[str, Any]) -> ProgressEvent:
    """Parse a progress event from SSE data."""
    return ProgressEvent(
        stage=data.get("stage", "pending"),
        message=data.get("message"),
        error=data.get("error"),
        playlist_url=data.get("playlistUrl"),
        thumbnail_url=data.get("thumbnailUrl"),
        preview_url=data.get("previewUrl"),
        duration=data.get("duration"),
        processed_size=data.get("processedSize"),
        resolutions=data.get("resolutions"),
    )
