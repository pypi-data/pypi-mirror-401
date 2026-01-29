"""
Asynchronous PlayVideo client.
"""

from __future__ import annotations

from playvideo._internal.http import AsyncHttpClient
from playvideo.resources import (
    AsyncAccount,
    AsyncApiKeys,
    AsyncCollections,
    AsyncEmbed,
    AsyncUsage,
    AsyncVideos,
    AsyncWebhooks,
)


class AsyncPlayVideo:
    """
    Asynchronous PlayVideo API client.

    Example:
        >>> from playvideo import AsyncPlayVideo
        >>> async with AsyncPlayVideo("play_live_xxx") as client:
        ...     collections = await client.collections.list()
        ...     video = await client.videos.upload("./video.mp4", "my-collection")

    Args:
        api_key: Your PlayVideo API key (play_live_xxx or play_test_xxx)
        base_url: Custom API base URL (for self-hosted instances)
        timeout: Request timeout in seconds (default: 30)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")

        self._http = AsyncHttpClient(api_key, base_url, timeout)

        # Initialize resources
        self.collections = AsyncCollections(self._http)
        self.videos = AsyncVideos(self._http)
        self.webhooks = AsyncWebhooks(self._http)
        self.embed = AsyncEmbed(self._http)
        self.api_keys = AsyncApiKeys(self._http)
        self.account = AsyncAccount(self._http)
        self.usage = AsyncUsage(self._http)

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._http.close()

    async def __aenter__(self) -> AsyncPlayVideo:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
