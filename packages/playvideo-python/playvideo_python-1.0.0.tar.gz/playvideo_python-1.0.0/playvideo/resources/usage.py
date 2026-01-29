"""Usage resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from playvideo.types import Limits, Usage, UsageInfo

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_usage(data: dict[str, Any]) -> Usage:
    """Parse usage from API response."""
    usage_data = data.get("usage", {})
    limits_data = data.get("limits", {})

    return Usage(
        plan=data["plan"],
        usage=UsageInfo(
            videos_this_month=usage_data.get("videosThisMonth", 0),
            videos_limit=usage_data.get("videosLimit", 0),
            storage_used_bytes=usage_data.get("storageUsedBytes", 0),
            storage_used_gb=usage_data.get("storageUsedGB", "0"),
            storage_limit_gb=usage_data.get("storageLimitGB", 0),
        ),
        limits=Limits(
            max_file_size_mb=limits_data.get("maxFileSizeMB", 0),
            max_duration_minutes=limits_data.get("maxDurationMinutes", 0),
            resolutions=limits_data.get("resolutions", []),
            api_access=limits_data.get("apiAccess", False),
            webhooks=limits_data.get("webhooks", False),
            delivery_gb=limits_data.get("deliveryGB", 0),
        ),
    )


class SyncUsage:
    """Synchronous usage resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self) -> Usage:
        """Get usage statistics and plan limits."""
        data = self._http.get("/usage")
        return _parse_usage(data)


class AsyncUsage:
    """Asynchronous usage resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> Usage:
        """Get usage statistics and plan limits."""
        data = await self._http.get("/usage")
        return _parse_usage(data)
