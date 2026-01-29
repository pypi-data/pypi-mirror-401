"""Videos resource."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote, urlencode

from playvideo.types import (
    ProgressCallback,
    ProgressEvent,
    UploadResponse,
    Video,
    VideoEmbedInfo,
    VideoStatus,
)

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_video(data: dict[str, Any]) -> Video:
    """Parse video from API response."""
    return Video(
        id=data["id"],
        filename=data["filename"],
        status=data["status"],
        duration=data.get("duration"),
        original_size=data.get("originalSize", 0),
        processed_size=data.get("processedSize"),
        playlist_url=data.get("playlistUrl"),
        thumbnail_url=data.get("thumbnailUrl"),
        preview_url=data.get("previewUrl"),
        resolutions=data.get("resolutions", []),
        error_message=data.get("errorMessage"),
        created_at=data["createdAt"],
        updated_at=data["updatedAt"],
        collection=data.get("collection"),
    )


class SyncVideos:
    """Synchronous videos resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        collection: str | None = None,
        status: VideoStatus | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Video]:
        """List videos with optional filters."""
        params: dict[str, str] = {}
        if collection:
            params["collection"] = collection
        if status:
            params["status"] = status
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)

        endpoint = "/videos"
        if params:
            endpoint += f"?{urlencode(params)}"

        data = self._http.get(endpoint)
        return [_parse_video(v) for v in data.get("videos", [])]

    def get(self, video_id: str) -> Video:
        """Get a video by ID."""
        data = self._http.get(f"/videos/{quote(video_id)}")
        return _parse_video(data)

    def upload(
        self,
        file_path: str | Path,
        collection: str,
        *,
        on_progress: ProgressCallback | None = None,
    ) -> UploadResponse:
        """Upload a video file."""
        data = self._http.upload("/videos", file_path, collection, on_progress)
        return UploadResponse(
            message=data["message"],
            video=data["video"],
        )

    def delete(self, video_id: str) -> dict[str, str]:
        """Delete a video."""
        return self._http.delete(f"/videos/{quote(video_id)}")

    def get_embed_info(self, video_id: str) -> VideoEmbedInfo:
        """Get embed information for a video."""
        data = self._http.get(f"/videos/{quote(video_id)}/embed")
        return VideoEmbedInfo(
            video_id=data["videoId"],
            signature=data["signature"],
            embed_path=data["embedPath"],
        )

    def watch_progress(self, video_id: str) -> Iterator[ProgressEvent]:
        """Watch video processing progress via SSE.

        Yields progress events as the video is processed.

        Example:
            for event in client.videos.watch_progress("video-id"):
                print(event.stage, event.message)
                if event.stage == "completed":
                    print("Done!", event.playlist_url)
                    break
        """
        yield from self._http.stream_sse(f"/videos/{quote(video_id)}/progress")


class AsyncVideos:
    """Asynchronous videos resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        collection: str | None = None,
        status: VideoStatus | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Video]:
        """List videos with optional filters."""
        params: dict[str, str] = {}
        if collection:
            params["collection"] = collection
        if status:
            params["status"] = status
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)

        endpoint = "/videos"
        if params:
            endpoint += f"?{urlencode(params)}"

        data = await self._http.get(endpoint)
        return [_parse_video(v) for v in data.get("videos", [])]

    async def get(self, video_id: str) -> Video:
        """Get a video by ID."""
        data = await self._http.get(f"/videos/{quote(video_id)}")
        return _parse_video(data)

    async def upload(
        self,
        file_path: str | Path,
        collection: str,
        *,
        on_progress: ProgressCallback | None = None,
    ) -> UploadResponse:
        """Upload a video file."""
        data = await self._http.upload("/videos", file_path, collection, on_progress)
        return UploadResponse(
            message=data["message"],
            video=data["video"],
        )

    async def delete(self, video_id: str) -> dict[str, str]:
        """Delete a video."""
        return await self._http.delete(f"/videos/{quote(video_id)}")

    async def get_embed_info(self, video_id: str) -> VideoEmbedInfo:
        """Get embed information for a video."""
        data = await self._http.get(f"/videos/{quote(video_id)}/embed")
        return VideoEmbedInfo(
            video_id=data["videoId"],
            signature=data["signature"],
            embed_path=data["embedPath"],
        )

    async def watch_progress(self, video_id: str) -> AsyncIterator[ProgressEvent]:
        """Watch video processing progress via SSE.

        Yields progress events as the video is processed.

        Example:
            async for event in client.videos.watch_progress("video-id"):
                print(event.stage, event.message)
                if event.stage == "completed":
                    print("Done!", event.playlist_url)
                    break
        """
        async for event in self._http.stream_sse(f"/videos/{quote(video_id)}/progress"):
            yield event
