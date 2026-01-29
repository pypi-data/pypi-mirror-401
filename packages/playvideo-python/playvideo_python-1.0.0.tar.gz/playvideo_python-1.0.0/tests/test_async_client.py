"""Tests for the asynchronous PlayVideo client."""

import pytest
from pytest_httpx import HTTPXMock

from playvideo import AsyncPlayVideo
from playvideo.errors import (
    AuthenticationError,
    NotFoundError,
)

# Import mock helpers from test_client
from .test_client import mock_account, mock_collection, mock_video, mock_webhook


class TestAsyncPlayVideoClient:
    """Tests for AsyncPlayVideo client."""

    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client can be initialized with API key."""
        client = AsyncPlayVideo("play_test_xxx")
        assert client is not None
        await client.close()

    @pytest.mark.asyncio
    async def test_client_context_manager(self, httpx_mock: HTTPXMock):
        """Test client works as async context manager."""
        async with AsyncPlayVideo("play_test_xxx") as client:
            assert client is not None


class TestAsyncCollections:
    """Tests for async Collections resource."""

    @pytest.mark.asyncio
    async def test_list_collections(self, httpx_mock: HTTPXMock):
        """Test listing collections asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/collections",
            json={"collections": [mock_collection()]},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.collections.list()

        assert len(result) == 1
        assert result[0].slug == "test"

    @pytest.mark.asyncio
    async def test_create_collection(self, httpx_mock: HTTPXMock):
        """Test creating a collection asynchronously."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/collections",
            json=mock_collection(name="My Videos", slug="my-videos"),
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.collections.create(name="My Videos")

        assert result.slug == "my-videos"

    @pytest.mark.asyncio
    async def test_get_collection(self, httpx_mock: HTTPXMock):
        """Test getting a collection asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/collections/test",
            json={**mock_collection(), "videos": []},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.collections.get("test")

        assert result.slug == "test"


class TestAsyncVideos:
    """Tests for async Videos resource."""

    @pytest.mark.asyncio
    async def test_list_videos(self, httpx_mock: HTTPXMock):
        """Test listing videos asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos",
            json={"videos": [mock_video()]},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.videos.list()

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_video(self, httpx_mock: HTTPXMock):
        """Test getting a video asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos/vid1",
            json=mock_video(),
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.videos.get("vid1")

        assert result.id == "vid1"


class TestAsyncWebhooks:
    """Tests for async Webhooks resource."""

    @pytest.mark.asyncio
    async def test_list_webhooks(self, httpx_mock: HTTPXMock):
        """Test listing webhooks asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/webhooks",
            json={"webhooks": [], "availableEvents": ["video.completed"]},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            webhooks, events = await client.webhooks.list()

        assert webhooks == []

    @pytest.mark.asyncio
    async def test_create_webhook(self, httpx_mock: HTTPXMock):
        """Test creating a webhook asynchronously."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/webhooks",
            json={
                "message": "Webhook created",
                "webhook": {**mock_webhook(), "secret": "whsec_test123"},
            },
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.webhooks.create(
                url="https://example.com/webhook", events=["video.completed"]
            )

        assert result.secret == "whsec_test123"


class TestAsyncEmbed:
    """Tests for async Embed resource."""

    @pytest.mark.asyncio
    async def test_get_settings(self, httpx_mock: HTTPXMock):
        """Test getting embed settings asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/embed/settings",
            json={"allowedDomains": ["example.com"], "primaryColor": "#FF0000"},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.embed.get_settings()

        assert result.primary_color == "#FF0000"

    @pytest.mark.asyncio
    async def test_sign_embed(self, httpx_mock: HTTPXMock):
        """Test signing embed URL asynchronously."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.playvideo.dev/api/v1/embed/sign",
            json={
                "videoId": "vid1",
                "signature": "sig123",
                "embedUrl": "https://embed.playvideo.dev/vid1",
                "embedCode": {"responsive": "", "fixed": ""},
            },
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.embed.sign(video_id="vid1")

        assert result.signature == "sig123"


class TestAsyncApiKeys:
    """Tests for async API Keys resource."""

    @pytest.mark.asyncio
    async def test_list_api_keys(self, httpx_mock: HTTPXMock):
        """Test listing API keys asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/api-keys",
            json={"apiKeys": []},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.api_keys.list()

        assert result == []


class TestAsyncAccount:
    """Tests for async Account resource."""

    @pytest.mark.asyncio
    async def test_get_account(self, httpx_mock: HTTPXMock):
        """Test getting account info asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/account",
            json=mock_account(),
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.account.get()

        assert result.email == "user@example.com"


class TestAsyncUsage:
    """Tests for async Usage resource."""

    @pytest.mark.asyncio
    async def test_get_usage(self, httpx_mock: HTTPXMock):
        """Test getting usage info asynchronously."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/usage",
            json={
                "plan": "PRO",
                "usage": {"videosThisMonth": 50, "videosLimit": 500},
                "limits": {"maxFileSizeMB": 500},
            },
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            result = await client.usage.get()

        assert result.plan == "PRO"


class TestAsyncErrorHandling:
    """Tests for async error handling."""

    @pytest.mark.asyncio
    async def test_authentication_error(self, httpx_mock: HTTPXMock):
        """Test 401 raises AuthenticationError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/collections",
            status_code=401,
            json={"error": "Unauthorized"},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            with pytest.raises(AuthenticationError):
                await client.collections.list()

    @pytest.mark.asyncio
    async def test_not_found_error(self, httpx_mock: HTTPXMock):
        """Test 404 raises NotFoundError."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.playvideo.dev/api/v1/videos/nonexistent",
            status_code=404,
            json={"error": "Not Found"},
        )

        async with AsyncPlayVideo("play_test_xxx") as client:
            with pytest.raises(NotFoundError):
                await client.videos.get("nonexistent")
