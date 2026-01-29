"""
PlayVideo SDK Types
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

# Type aliases
VideoStatus = Literal["PENDING", "PROCESSING", "COMPLETED", "FAILED"]
Plan = Literal["FREE", "PRO", "BUSINESS"]
LogoPosition = Literal["top-left", "top-right", "bottom-left", "bottom-right"]
WebhookEvent = Literal[
    "video.uploaded",
    "video.processing",
    "video.completed",
    "video.failed",
    "collection.created",
    "collection.deleted",
]
ProgressStage = Literal["pending", "processing", "completed", "failed", "timeout"]


@dataclass
class Collection:
    """A video collection."""

    id: str
    name: str
    slug: str
    description: str | None
    video_count: int
    storage_used: int
    created_at: str
    updated_at: str


@dataclass
class CollectionWithVideos(Collection):
    """A collection with its videos."""

    videos: list["Video"]


@dataclass
class Video:
    """A video."""

    id: str
    filename: str
    status: VideoStatus
    duration: float | None
    original_size: int
    processed_size: int | None
    playlist_url: str | None
    thumbnail_url: str | None
    preview_url: str | None
    resolutions: list[str]
    error_message: str | None
    created_at: str
    updated_at: str
    collection: dict[str, str] | None = None


@dataclass
class UploadResponse:
    """Response from video upload."""

    message: str
    video: dict[str, str]


@dataclass
class UploadProgress:
    """Upload progress information."""

    loaded: int
    total: int
    percent: int


@dataclass
class ProgressEvent:
    """Video processing progress event."""

    stage: ProgressStage
    message: str | None = None
    error: str | None = None
    playlist_url: str | None = None
    thumbnail_url: str | None = None
    preview_url: str | None = None
    duration: float | None = None
    processed_size: int | None = None
    resolutions: list[str] | None = None


@dataclass
class Webhook:
    """A webhook configuration."""

    id: str
    url: str
    events: list[WebhookEvent]
    is_active: bool
    created_at: str
    updated_at: str


@dataclass
class WebhookWithSecret(Webhook):
    """A webhook with its secret (only returned on creation)."""

    secret: str


@dataclass
class WebhookDelivery:
    """A webhook delivery record."""

    id: str
    event: WebhookEvent
    status_code: int | None
    error: str | None
    attempt_count: int
    delivered_at: str | None
    created_at: str


@dataclass
class WebhookWithDeliveries(Webhook):
    """A webhook with its recent deliveries."""

    recent_deliveries: list[WebhookDelivery]


@dataclass
class EmbedSettings:
    """Embed player settings."""

    allowed_domains: list[str]
    allow_localhost: bool
    primary_color: str
    accent_color: str
    logo_url: str | None
    logo_position: LogoPosition
    logo_opacity: float
    show_playback_speed: bool
    show_quality_selector: bool
    show_fullscreen: bool
    show_volume: bool
    show_progress: bool
    show_time: bool
    show_keyboard_hints: bool
    autoplay: bool
    muted: bool
    loop: bool


@dataclass
class ApiKey:
    """An API key."""

    id: str
    name: str
    key_prefix: str
    last_used_at: str | None
    expires_at: str | None
    created_at: str


@dataclass
class ApiKeyWithKey(ApiKey):
    """An API key with the full key (only returned on creation)."""

    key: str


@dataclass
class Account:
    """Account information."""

    id: str
    email: str
    name: str | None
    plan: Plan
    allowed_domains: list[str]
    allow_localhost: bool
    r2_bucket_name: str | None
    r2_bucket_region: str | None
    created_at: str


@dataclass
class UsageInfo:
    """Usage statistics."""

    videos_this_month: int
    videos_limit: int | str  # Can be "unlimited"
    storage_used_bytes: int
    storage_used_gb: str
    storage_limit_gb: int


@dataclass
class Limits:
    """Plan limits."""

    max_file_size_mb: int
    max_duration_minutes: int
    resolutions: list[str]
    api_access: bool
    webhooks: bool
    delivery_gb: int


@dataclass
class Usage:
    """Usage and limits information."""

    plan: Plan
    usage: UsageInfo
    limits: Limits


@dataclass
class SignEmbedResponse:
    """Response from signing an embed URL."""

    video_id: str
    signature: str
    embed_url: str
    embed_code: dict[str, str]


@dataclass
class VideoEmbedInfo:
    """Video embed information."""

    video_id: str
    signature: str
    embed_path: str


# Type alias for progress callback
ProgressCallback = Callable[[UploadProgress], None]
