"""Webhooks resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from playvideo.types import (
    Webhook,
    WebhookDelivery,
    WebhookEvent,
    WebhookWithDeliveries,
    WebhookWithSecret,
)

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_webhook(data: dict[str, Any]) -> Webhook:
    """Parse webhook from API response."""
    return Webhook(
        id=data["id"],
        url=data["url"],
        events=data["events"],
        is_active=data["isActive"],
        created_at=data["createdAt"],
        updated_at=data["updatedAt"],
    )


def _parse_delivery(data: dict[str, Any]) -> WebhookDelivery:
    """Parse webhook delivery from API response."""
    return WebhookDelivery(
        id=data["id"],
        event=data["event"],
        status_code=data.get("statusCode"),
        error=data.get("error"),
        attempt_count=data["attemptCount"],
        delivered_at=data.get("deliveredAt"),
        created_at=data["createdAt"],
    )


class SyncWebhooks:
    """Synchronous webhooks resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(self) -> tuple[builtins.list[Webhook], builtins.list[WebhookEvent]]:
        """List all webhooks.

        Returns:
            Tuple of (webhooks, available_events)
        """
        data = self._http.get("/webhooks")
        webhooks = [_parse_webhook(w) for w in data.get("webhooks", [])]
        return webhooks, data.get("availableEvents", [])

    def get(self, webhook_id: str) -> WebhookWithDeliveries:
        """Get a webhook by ID with recent deliveries."""
        data = self._http.get(f"/webhooks/{quote(webhook_id)}")
        webhook = _parse_webhook(data)
        deliveries = [_parse_delivery(d) for d in data.get("recentDeliveries", [])]
        return WebhookWithDeliveries(
            id=webhook.id,
            url=webhook.url,
            events=webhook.events,
            is_active=webhook.is_active,
            created_at=webhook.created_at,
            updated_at=webhook.updated_at,
            recent_deliveries=deliveries,
        )

    def create(self, url: str, events: builtins.list[WebhookEvent]) -> WebhookWithSecret:
        """Create a new webhook.

        Note: The secret is only returned once. Store it securely.
        """
        data = self._http.post("/webhooks", json={"url": url, "events": events})
        webhook_data = data["webhook"]
        return WebhookWithSecret(
            id=webhook_data["id"],
            url=webhook_data["url"],
            events=webhook_data["events"],
            is_active=webhook_data["isActive"],
            created_at=webhook_data["createdAt"],
            updated_at=webhook_data["updatedAt"],
            secret=webhook_data["secret"],
        )

    def update(
        self,
        webhook_id: str,
        *,
        url: str | None = None,
        events: builtins.list[WebhookEvent] | None = None,
        is_active: bool | None = None,
    ) -> Webhook:
        """Update a webhook."""
        payload: dict[str, Any] = {}
        if url is not None:
            payload["url"] = url
        if events is not None:
            payload["events"] = events
        if is_active is not None:
            payload["isActive"] = is_active

        data = self._http.patch(f"/webhooks/{quote(webhook_id)}", json=payload)
        return _parse_webhook(data)

    def test(self, webhook_id: str) -> dict[str, Any]:
        """Test a webhook by sending a test event."""
        return self._http.post(f"/webhooks/{quote(webhook_id)}/test", json={})

    def delete(self, webhook_id: str) -> dict[str, str]:
        """Delete a webhook."""
        return self._http.delete(f"/webhooks/{quote(webhook_id)}")


class AsyncWebhooks:
    """Asynchronous webhooks resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> tuple[builtins.list[Webhook], builtins.list[WebhookEvent]]:
        """List all webhooks."""
        data = await self._http.get("/webhooks")
        webhooks = [_parse_webhook(w) for w in data.get("webhooks", [])]
        return webhooks, data.get("availableEvents", [])

    async def get(self, webhook_id: str) -> WebhookWithDeliveries:
        """Get a webhook by ID with recent deliveries."""
        data = await self._http.get(f"/webhooks/{quote(webhook_id)}")
        webhook = _parse_webhook(data)
        deliveries = [_parse_delivery(d) for d in data.get("recentDeliveries", [])]
        return WebhookWithDeliveries(
            id=webhook.id,
            url=webhook.url,
            events=webhook.events,
            is_active=webhook.is_active,
            created_at=webhook.created_at,
            updated_at=webhook.updated_at,
            recent_deliveries=deliveries,
        )

    async def create(self, url: str, events: builtins.list[WebhookEvent]) -> WebhookWithSecret:
        """Create a new webhook."""
        data = await self._http.post("/webhooks", json={"url": url, "events": events})
        webhook_data = data["webhook"]
        return WebhookWithSecret(
            id=webhook_data["id"],
            url=webhook_data["url"],
            events=webhook_data["events"],
            is_active=webhook_data["isActive"],
            created_at=webhook_data["createdAt"],
            updated_at=webhook_data["updatedAt"],
            secret=webhook_data["secret"],
        )

    async def update(
        self,
        webhook_id: str,
        *,
        url: str | None = None,
        events: builtins.list[WebhookEvent] | None = None,
        is_active: bool | None = None,
    ) -> Webhook:
        """Update a webhook."""
        payload: dict[str, Any] = {}
        if url is not None:
            payload["url"] = url
        if events is not None:
            payload["events"] = events
        if is_active is not None:
            payload["isActive"] = is_active

        data = await self._http.patch(f"/webhooks/{quote(webhook_id)}", json=payload)
        return _parse_webhook(data)

    async def test(self, webhook_id: str) -> dict[str, Any]:
        """Test a webhook by sending a test event."""
        return await self._http.post(f"/webhooks/{quote(webhook_id)}/test", json={})

    async def delete(self, webhook_id: str) -> dict[str, str]:
        """Delete a webhook."""
        return await self._http.delete(f"/webhooks/{quote(webhook_id)}")
