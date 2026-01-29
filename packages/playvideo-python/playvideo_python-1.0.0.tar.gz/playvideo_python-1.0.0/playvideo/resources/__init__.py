"""PlayVideo SDK Resources."""

from playvideo.resources.account import AsyncAccount, SyncAccount
from playvideo.resources.api_keys import AsyncApiKeys, SyncApiKeys
from playvideo.resources.collections import AsyncCollections, SyncCollections
from playvideo.resources.embed import AsyncEmbed, SyncEmbed
from playvideo.resources.usage import AsyncUsage, SyncUsage
from playvideo.resources.videos import AsyncVideos, SyncVideos
from playvideo.resources.webhooks import AsyncWebhooks, SyncWebhooks

__all__ = [
    "SyncCollections",
    "AsyncCollections",
    "SyncVideos",
    "AsyncVideos",
    "SyncWebhooks",
    "AsyncWebhooks",
    "SyncEmbed",
    "AsyncEmbed",
    "SyncApiKeys",
    "AsyncApiKeys",
    "SyncAccount",
    "AsyncAccount",
    "SyncUsage",
    "AsyncUsage",
]
