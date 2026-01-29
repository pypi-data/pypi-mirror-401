"""Embed resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from playvideo.types import EmbedSettings, LogoPosition, SignEmbedResponse

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_embed_settings(data: dict[str, Any]) -> EmbedSettings:
    """Parse embed settings from API response."""
    return EmbedSettings(
        allowed_domains=data.get("allowedDomains", []),
        allow_localhost=data.get("allowLocalhost", False),
        primary_color=data.get("primaryColor", "#FFFFFF"),
        accent_color=data.get("accentColor", "#333333"),
        logo_url=data.get("logoUrl"),
        logo_position=data.get("logoPosition", "top-right"),
        logo_opacity=data.get("logoOpacity", 1.0),
        show_playback_speed=data.get("showPlaybackSpeed", True),
        show_quality_selector=data.get("showQualitySelector", True),
        show_fullscreen=data.get("showFullscreen", True),
        show_volume=data.get("showVolume", True),
        show_progress=data.get("showProgress", True),
        show_time=data.get("showTime", True),
        show_keyboard_hints=data.get("showKeyboardHints", True),
        autoplay=data.get("autoplay", False),
        muted=data.get("muted", False),
        loop=data.get("loop", False),
    )


class SyncEmbed:
    """Synchronous embed resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get_settings(self) -> EmbedSettings:
        """Get current embed settings."""
        data = self._http.get("/embed/settings")
        return _parse_embed_settings(data)

    def update_settings(
        self,
        *,
        allowed_domains: list[str] | None = None,
        allow_localhost: bool | None = None,
        primary_color: str | None = None,
        accent_color: str | None = None,
        logo_url: str | None = None,
        logo_position: LogoPosition | None = None,
        logo_opacity: float | None = None,
        show_playback_speed: bool | None = None,
        show_quality_selector: bool | None = None,
        show_fullscreen: bool | None = None,
        show_volume: bool | None = None,
        show_progress: bool | None = None,
        show_time: bool | None = None,
        show_keyboard_hints: bool | None = None,
        autoplay: bool | None = None,
        muted: bool | None = None,
        loop: bool | None = None,
    ) -> EmbedSettings:
        """Update embed settings."""
        payload: dict[str, Any] = {}

        if allowed_domains is not None:
            payload["allowedDomains"] = allowed_domains
        if allow_localhost is not None:
            payload["allowLocalhost"] = allow_localhost
        if primary_color is not None:
            payload["primaryColor"] = primary_color
        if accent_color is not None:
            payload["accentColor"] = accent_color
        if logo_url is not None:
            payload["logoUrl"] = logo_url
        if logo_position is not None:
            payload["logoPosition"] = logo_position
        if logo_opacity is not None:
            payload["logoOpacity"] = logo_opacity
        if show_playback_speed is not None:
            payload["showPlaybackSpeed"] = show_playback_speed
        if show_quality_selector is not None:
            payload["showQualitySelector"] = show_quality_selector
        if show_fullscreen is not None:
            payload["showFullscreen"] = show_fullscreen
        if show_volume is not None:
            payload["showVolume"] = show_volume
        if show_progress is not None:
            payload["showProgress"] = show_progress
        if show_time is not None:
            payload["showTime"] = show_time
        if show_keyboard_hints is not None:
            payload["showKeyboardHints"] = show_keyboard_hints
        if autoplay is not None:
            payload["autoplay"] = autoplay
        if muted is not None:
            payload["muted"] = muted
        if loop is not None:
            payload["loop"] = loop

        data = self._http.patch("/embed/settings", json=payload)
        return _parse_embed_settings(data.get("settings", data))

    def sign(self, video_id: str, base_url: str | None = None) -> SignEmbedResponse:
        """Generate a signed embed URL for a video."""
        payload: dict[str, Any] = {"videoId": video_id}
        if base_url:
            payload["baseUrl"] = base_url

        data = self._http.post("/embed/sign", json=payload)
        return SignEmbedResponse(
            video_id=data["videoId"],
            signature=data["signature"],
            embed_url=data["embedUrl"],
            embed_code=data["embedCode"],
        )


class AsyncEmbed:
    """Asynchronous embed resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_settings(self) -> EmbedSettings:
        """Get current embed settings."""
        data = await self._http.get("/embed/settings")
        return _parse_embed_settings(data)

    async def update_settings(
        self,
        *,
        allowed_domains: list[str] | None = None,
        allow_localhost: bool | None = None,
        primary_color: str | None = None,
        accent_color: str | None = None,
        logo_url: str | None = None,
        logo_position: LogoPosition | None = None,
        logo_opacity: float | None = None,
        show_playback_speed: bool | None = None,
        show_quality_selector: bool | None = None,
        show_fullscreen: bool | None = None,
        show_volume: bool | None = None,
        show_progress: bool | None = None,
        show_time: bool | None = None,
        show_keyboard_hints: bool | None = None,
        autoplay: bool | None = None,
        muted: bool | None = None,
        loop: bool | None = None,
    ) -> EmbedSettings:
        """Update embed settings."""
        payload: dict[str, Any] = {}

        if allowed_domains is not None:
            payload["allowedDomains"] = allowed_domains
        if allow_localhost is not None:
            payload["allowLocalhost"] = allow_localhost
        if primary_color is not None:
            payload["primaryColor"] = primary_color
        if accent_color is not None:
            payload["accentColor"] = accent_color
        if logo_url is not None:
            payload["logoUrl"] = logo_url
        if logo_position is not None:
            payload["logoPosition"] = logo_position
        if logo_opacity is not None:
            payload["logoOpacity"] = logo_opacity
        if show_playback_speed is not None:
            payload["showPlaybackSpeed"] = show_playback_speed
        if show_quality_selector is not None:
            payload["showQualitySelector"] = show_quality_selector
        if show_fullscreen is not None:
            payload["showFullscreen"] = show_fullscreen
        if show_volume is not None:
            payload["showVolume"] = show_volume
        if show_progress is not None:
            payload["showProgress"] = show_progress
        if show_time is not None:
            payload["showTime"] = show_time
        if show_keyboard_hints is not None:
            payload["showKeyboardHints"] = show_keyboard_hints
        if autoplay is not None:
            payload["autoplay"] = autoplay
        if muted is not None:
            payload["muted"] = muted
        if loop is not None:
            payload["loop"] = loop

        data = await self._http.patch("/embed/settings", json=payload)
        return _parse_embed_settings(data.get("settings", data))

    async def sign(self, video_id: str, base_url: str | None = None) -> SignEmbedResponse:
        """Generate a signed embed URL for a video."""
        payload: dict[str, Any] = {"videoId": video_id}
        if base_url:
            payload["baseUrl"] = base_url

        data = await self._http.post("/embed/sign", json=payload)
        return SignEmbedResponse(
            video_id=data["videoId"],
            signature=data["signature"],
            embed_url=data["embedUrl"],
            embed_code=data["embedCode"],
        )
