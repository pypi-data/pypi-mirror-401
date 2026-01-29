"""
Synchronous PlayVideo client.
"""

from __future__ import annotations

from playvideo._internal.http import SyncHttpClient
from playvideo.resources import (
    SyncAccount,
    SyncApiKeys,
    SyncCollections,
    SyncEmbed,
    SyncUsage,
    SyncVideos,
    SyncWebhooks,
)


class PlayVideo:
    """
    Synchronous PlayVideo API client.

    Example:
        >>> from playvideo import PlayVideo
        >>> client = PlayVideo("play_live_xxx")
        >>> collections = client.collections.list()
        >>> video = client.videos.upload("./video.mp4", "my-collection")

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

        self._http = SyncHttpClient(api_key, base_url, timeout)

        # Initialize resources
        self.collections = SyncCollections(self._http)
        self.videos = SyncVideos(self._http)
        self.webhooks = SyncWebhooks(self._http)
        self.embed = SyncEmbed(self._http)
        self.api_keys = SyncApiKeys(self._http)
        self.account = SyncAccount(self._http)
        self.usage = SyncUsage(self._http)

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._http.close()

    def __enter__(self) -> PlayVideo:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
