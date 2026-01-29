"""Tests for the synchronous PlayVideo client."""

import pytest
from pytest_httpx import HTTPXMock

from playvideo import PlayVideo
from playvideo.errors import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


# Helpers to create complete mock responses
def mock_collection(id="col1", name="Test", slug="test", video_count=5):
    return {
        "id": id,
        "name": name,
        "slug": slug,
        "description": None,
        "videoCount": video_count,
        "storageUsed": 1024000,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


def mock_video(id="vid1", filename="test.mp4", status="COMPLETED"):
    return {
        "id": id,
        "filename": filename,
        "status": status,
        "duration": 120.5,
        "originalSize": 10000000,
        "processedSize": 5000000,
        "playlistUrl": f"https://cdn.example.com/{id}/playlist.m3u8",
        "thumbnailUrl": f"https://cdn.example.com/{id}/thumb.jpg",
        "previewUrl": f"https://cdn.example.com/{id}/preview.mp4",
        "resolutions": ["1080p", "720p", "480p"],
        "errorMessage": None,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


def mock_webhook(id="wh1", url="https://example.com/webhook"):
    return {
        "id": id,
        "url": url,
        "events": ["video.completed"],
        "isActive": True,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


def mock_api_key(id="key1", name="Production"):
    return {
        "id": id,
        "name": name,
        "keyPrefix": "play_live_abc",
        "lastUsedAt": None,
        "expiresAt": None,
        "createdAt": "2024-01-01T00:00:00Z",
    }


def mock_account(id="acc1", email="user@example.com", plan="PRO"):
    return {
        "id": id,
        "email": email,
        "name": "Test User",
        "plan": plan,
        "allowedDomains": ["example.com"],
        "allowLocalhost": True,
        "r2BucketName": None,
        "r2BucketRegion": None,
        "createdAt": "2024-01-01T00:00:00Z",
    }


class TestPlayVideoClient:
    """Tests for PlayVideo client initialization."""

    def test_client_initialization(self):
        """Test client can be initialized with API key."""
        client = PlayVideo("play_test_xxx")
        assert client is not None
        assert client.collections is not None
        assert client.videos is not None
        assert client.webhooks is not None
        assert client.embed is not None
        assert client.api_keys is not None
        assert client.account is not None
        assert client.usage is not None

    def test_client_custom_base_url(self):
        """Test client accepts custom base URL."""
        client = PlayVideo("play_test_xxx", base_url="https://custom.api.com/v1")
        assert client is not None

    def test_client_custom_timeout(self):
        """Test client accepts custom timeout."""
        client = PlayVideo("play_test_xxx", timeout=60.0)
        assert client is not None

    def test_client_context_manager(self, httpx_mock: HTTPXMock):
        """Test client works as context manager."""
        with PlayVideo("play_test_xxx") as client:
            assert client is not None


class TestCollections:
    """Tests for Collections resource."""

    def test_list_collections(self, httpx_mock: HTTPXMock):
        """Test listing collections."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/collections",
            json={"collections": [mock_collection()]},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.collections.list()

        assert len(result) == 1
        assert result[0].slug == "test"

    def test_create_collection(self, httpx_mock: HTTPXMock):
        """Test creating a collection."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/collections",
            json=mock_collection(name="My Videos", slug="my-videos"),
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.collections.create(name="My Videos", description="Test description")

        assert result.slug == "my-videos"

    def test_get_collection(self, httpx_mock: HTTPXMock):
        """Test getting a collection by slug."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/collections/test",
            json={**mock_collection(), "videos": [mock_video()]},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.collections.get("test")

        assert result.slug == "test"
        assert len(result.videos) == 1

    def test_delete_collection(self, httpx_mock: HTTPXMock):
        """Test deleting a collection."""
        httpx_mock.add_response(
            method="DELETE",
            url="https://api.playvideo.dev/api/v1/collections/test",
            json={"message": "Collection deleted"},
        )

        with PlayVideo("play_test_xxx") as client:
            client.collections.delete("test")


class TestVideos:
    """Tests for Videos resource."""

    def test_list_videos(self, httpx_mock: HTTPXMock):
        """Test listing videos."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos",
            json={"videos": [mock_video()]},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.videos.list()

        assert len(result) == 1

    def test_list_videos_with_filters(self, httpx_mock: HTTPXMock):
        """Test listing videos with filters."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos?collection=my-collection&status=COMPLETED&limit=10",
            json={"videos": []},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.videos.list(collection="my-collection", status="COMPLETED", limit=10)

        assert result == []

    def test_get_video(self, httpx_mock: HTTPXMock):
        """Test getting a video by ID."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos/vid1",
            json=mock_video(),
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.videos.get("vid1")

        assert result.id == "vid1"
        assert result.playlist_url is not None

    def test_delete_video(self, httpx_mock: HTTPXMock):
        """Test deleting a video."""
        httpx_mock.add_response(
            method="DELETE",
            url="https://api.playvideo.dev/api/v1/videos/vid1",
            json={"message": "Video deleted"},
        )

        with PlayVideo("play_test_xxx") as client:
            client.videos.delete("vid1")

    def test_get_embed_info(self, httpx_mock: HTTPXMock):
        """Test getting embed info for a video."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos/vid1/embed",
            json={
                "videoId": "vid1",
                "signature": "sig123",
                "embedPath": "/embed/vid1",
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.videos.get_embed_info("vid1")

        assert result.video_id == "vid1"
        assert result.signature == "sig123"


class TestWebhooks:
    """Tests for Webhooks resource."""

    def test_list_webhooks(self, httpx_mock: HTTPXMock):
        """Test listing webhooks."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/webhooks",
            json={
                "webhooks": [mock_webhook()],
                "availableEvents": ["video.uploaded", "video.completed", "video.failed"],
            },
        )

        with PlayVideo("play_test_xxx") as client:
            webhooks, events = client.webhooks.list()

        assert len(webhooks) == 1
        assert "video.completed" in events

    def test_create_webhook(self, httpx_mock: HTTPXMock):
        """Test creating a webhook."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/webhooks",
            json={
                "message": "Webhook created",
                "webhook": {**mock_webhook(), "secret": "whsec_test123"},
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.webhooks.create(
                url="https://example.com/webhook", events=["video.completed"]
            )

        assert result.secret == "whsec_test123"

    def test_update_webhook(self, httpx_mock: HTTPXMock):
        """Test updating a webhook."""
        httpx_mock.add_response(
            method="PATCH",
            url="https://api.playvideo.dev/api/v1/webhooks/wh1",
            json={**mock_webhook(), "isActive": False},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.webhooks.update(
                "wh1", events=["video.completed", "video.failed"], is_active=False
            )

        assert result.is_active is False

    def test_test_webhook(self, httpx_mock: HTTPXMock):
        """Test sending test event to webhook."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/webhooks/wh1/test",
            json={"message": "Test event sent", "statusCode": 200},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.webhooks.test("wh1")

        assert result["statusCode"] == 200

    def test_delete_webhook(self, httpx_mock: HTTPXMock):
        """Test deleting a webhook."""
        httpx_mock.add_response(
            method="DELETE",
            url="https://api.playvideo.dev/api/v1/webhooks/wh1",
            json={"message": "Webhook deleted"},
        )

        with PlayVideo("play_test_xxx") as client:
            client.webhooks.delete("wh1")


class TestEmbed:
    """Tests for Embed resource."""

    def test_get_settings(self, httpx_mock: HTTPXMock):
        """Test getting embed settings."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/embed/settings",
            json={
                "allowedDomains": ["example.com"],
                "allowLocalhost": True,
                "primaryColor": "#FF0000",
                "autoplay": False,
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.embed.get_settings()

        assert "example.com" in result.allowed_domains
        assert result.primary_color == "#FF0000"

    def test_update_settings(self, httpx_mock: HTTPXMock):
        """Test updating embed settings."""
        httpx_mock.add_response(
            method="PATCH",
            url="https://api.playvideo.dev/api/v1/embed/settings",
            json={
                "message": "Settings updated",
                "settings": {
                    "primaryColor": "#00FF00",
                    "autoplay": True,
                },
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.embed.update_settings(primary_color="#00FF00", autoplay=True)

        assert result.primary_color == "#00FF00"

    def test_sign_embed(self, httpx_mock: HTTPXMock):
        """Test signing an embed URL."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/embed/sign",
            json={
                "videoId": "vid1",
                "signature": "sig123",
                "embedUrl": "https://embed.playvideo.dev/vid1?sig=sig123",
                "embedCode": {
                    "responsive": '<div><iframe src="..."></iframe></div>',
                    "fixed": '<iframe src="..."></iframe>',
                },
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.embed.sign(video_id="vid1")

        assert "vid1" in result.embed_url
        assert result.signature == "sig123"


class TestApiKeys:
    """Tests for API Keys resource."""

    def test_list_api_keys(self, httpx_mock: HTTPXMock):
        """Test listing API keys."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/api-keys",
            json={"apiKeys": [mock_api_key()]},
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.api_keys.list()

        assert len(result) == 1
        assert result[0].key_prefix == "play_live_abc"

    def test_create_api_key(self, httpx_mock: HTTPXMock):
        """Test creating an API key."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/api-keys",
            json={
                "message": "API key created",
                "apiKey": {**mock_api_key(), "key": "play_live_xyz123456789"},
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.api_keys.create(name="New Key")

        assert result.key == "play_live_xyz123456789"

    def test_delete_api_key(self, httpx_mock: HTTPXMock):
        """Test deleting an API key."""
        httpx_mock.add_response(
            method="DELETE",
            url="https://api.playvideo.dev/api/v1/api-keys/key1",
            json={"message": "API key deleted"},
        )

        with PlayVideo("play_test_xxx") as client:
            client.api_keys.delete("key1")


class TestAccount:
    """Tests for Account resource."""

    def test_get_account(self, httpx_mock: HTTPXMock):
        """Test getting account info."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/account",
            json=mock_account(),
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.account.get()

        assert result.email == "user@example.com"
        assert result.plan == "PRO"

    def test_update_account(self, httpx_mock: HTTPXMock):
        """Test updating account."""
        httpx_mock.add_response(
            method="PATCH",
            url="https://api.playvideo.dev/api/v1/account",
            json={
                "message": "Account updated",
                "account": mock_account(),
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.account.update(
                allowed_domains=["example.com", "test.com"], allow_localhost=True
            )

        assert result.email == "user@example.com"


class TestUsage:
    """Tests for Usage resource."""

    def test_get_usage(self, httpx_mock: HTTPXMock):
        """Test getting usage info."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/usage",
            json={
                "plan": "PRO",
                "usage": {
                    "videosThisMonth": 50,
                    "videosLimit": 500,
                    "storageUsedBytes": 1073741824,
                    "storageUsedGB": "1.00",
                    "storageLimitGB": 100,
                },
                "limits": {
                    "maxFileSizeMB": 500,
                    "maxDurationMinutes": 60,
                    "resolutions": ["1080p", "720p", "480p"],
                    "apiAccess": True,
                    "webhooks": True,
                },
            },
        )

        with PlayVideo("play_test_xxx") as client:
            result = client.usage.get()

        assert result.plan == "PRO"
        assert result.usage.videos_this_month == 50
        assert result.limits.api_access is True


class TestErrorHandling:
    """Tests for error handling."""

    def test_authentication_error(self, httpx_mock: HTTPXMock):
        """Test 401 raises AuthenticationError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/collections",
            status_code=401,
            json={"error": "Unauthorized", "message": "Invalid API key"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(AuthenticationError):
                client.collections.list()

    def test_authorization_error(self, httpx_mock: HTTPXMock):
        """Test 403 raises AuthorizationError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/webhooks",
            status_code=403,
            json={"error": "Forbidden", "message": "Insufficient permissions"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(AuthorizationError):
                client.webhooks.list()

    def test_not_found_error(self, httpx_mock: HTTPXMock):
        """Test 404 raises NotFoundError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos/nonexistent",
            status_code=404,
            json={"error": "Not Found", "message": "Video not found"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(NotFoundError):
                client.videos.get("nonexistent")

    def test_validation_error(self, httpx_mock: HTTPXMock):
        """Test 400 raises ValidationError."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/collections",
            status_code=400,
            json={"error": "Bad Request", "message": "Invalid collection name"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(ValidationError):
                client.collections.create(name="")

    def test_rate_limit_error(self, httpx_mock: HTTPXMock):
        """Test 429 raises RateLimitError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos",
            status_code=429,
            json={"error": "Too Many Requests", "message": "Rate limit exceeded"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(RateLimitError):
                client.videos.list()

    def test_server_error(self, httpx_mock: HTTPXMock):
        """Test 500 raises ServerError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/account",
            status_code=500,
            json={"error": "Internal Server Error", "message": "Something went wrong"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(ServerError):
                client.account.get()

    def test_error_includes_request_id(self, httpx_mock: HTTPXMock):
        """Test error includes request ID."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos/nonexistent",
            status_code=404,
            json={"error": "Not Found", "message": "Video not found"},
            headers={"X-Request-ID": "req-abc-123"},
        )

        with PlayVideo("play_test_xxx") as client:
            with pytest.raises(NotFoundError) as exc_info:
                client.videos.get("nonexistent")

        assert exc_info.value.request_id == "req-abc-123"
