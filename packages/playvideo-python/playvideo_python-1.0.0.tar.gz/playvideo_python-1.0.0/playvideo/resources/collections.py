"""Collections resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from playvideo.types import Collection, CollectionWithVideos, Video

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_collection(data: dict[str, Any]) -> Collection:
    """Parse collection from API response."""
    return Collection(
        id=data["id"],
        name=data["name"],
        slug=data["slug"],
        description=data.get("description"),
        video_count=data.get("videoCount", 0),
        storage_used=data.get("storageUsed", 0),
        created_at=data["createdAt"],
        updated_at=data["updatedAt"],
    )


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


class SyncCollections:
    """Synchronous collections resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(self) -> list[Collection]:
        """List all collections."""
        data = self._http.get("/collections")
        return [_parse_collection(c) for c in data.get("collections", [])]

    def get(self, slug: str) -> CollectionWithVideos:
        """Get a collection by slug."""
        data = self._http.get(f"/collections/{quote(slug)}")
        collection = _parse_collection(data)
        videos = [_parse_video(v) for v in data.get("videos", [])]
        return CollectionWithVideos(
            id=collection.id,
            name=collection.name,
            slug=collection.slug,
            description=collection.description,
            video_count=collection.video_count,
            storage_used=collection.storage_used,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            videos=videos,
        )

    def create(self, name: str, description: str | None = None) -> Collection:
        """Create a new collection."""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        data = self._http.post("/collections", json=payload)
        return _parse_collection(data)

    def delete(self, slug: str) -> dict[str, str]:
        """Delete a collection."""
        return self._http.delete(f"/collections/{quote(slug)}")


class AsyncCollections:
    """Asynchronous collections resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> list[Collection]:
        """List all collections."""
        data = await self._http.get("/collections")
        return [_parse_collection(c) for c in data.get("collections", [])]

    async def get(self, slug: str) -> CollectionWithVideos:
        """Get a collection by slug."""
        data = await self._http.get(f"/collections/{quote(slug)}")
        collection = _parse_collection(data)
        videos = [_parse_video(v) for v in data.get("videos", [])]
        return CollectionWithVideos(
            id=collection.id,
            name=collection.name,
            slug=collection.slug,
            description=collection.description,
            video_count=collection.video_count,
            storage_used=collection.storage_used,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            videos=videos,
        )

    async def create(self, name: str, description: str | None = None) -> Collection:
        """Create a new collection."""
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        data = await self._http.post("/collections", json=payload)
        return _parse_collection(data)

    async def delete(self, slug: str) -> dict[str, str]:
        """Delete a collection."""
        return await self._http.delete(f"/collections/{quote(slug)}")
