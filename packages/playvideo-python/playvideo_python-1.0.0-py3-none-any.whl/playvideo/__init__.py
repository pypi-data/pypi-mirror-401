"""
PlayVideo SDK for Python

Official SDK for the PlayVideo API - Video hosting for developers.

Example:
    >>> from playvideo import PlayVideo
    >>> client = PlayVideo("play_live_xxx")
    >>> collections = client.collections.list()
    >>> video = client.videos.upload("./video.mp4", "my-collection")

For async usage:
    >>> from playvideo import AsyncPlayVideo
    >>> async with AsyncPlayVideo("play_live_xxx") as client:
    ...     collections = await client.collections.list()
"""

from playvideo._async_client import AsyncPlayVideo
from playvideo._client import PlayVideo
from playvideo.errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NetworkError,
    NotFoundError,
    PlayVideoError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
    WebhookSignatureError,
)
from playvideo.types import (
    Account,
    ApiKey,
    Collection,
    EmbedSettings,
    LogoPosition,
    Plan,
    ProgressEvent,
    ProgressStage,
    UploadProgress,
    Usage,
    Video,
    VideoStatus,
    Webhook,
    WebhookEvent,
)

__version__ = "1.0.0"
__all__ = [
    # Clients
    "PlayVideo",
    "AsyncPlayVideo",
    # Errors
    "PlayVideoError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
    "WebhookSignatureError",
    # Types
    "VideoStatus",
    "Plan",
    "LogoPosition",
    "WebhookEvent",
    "Collection",
    "Video",
    "Webhook",
    "EmbedSettings",
    "ApiKey",
    "Account",
    "Usage",
    "UploadProgress",
    "ProgressEvent",
    "ProgressStage",
]
