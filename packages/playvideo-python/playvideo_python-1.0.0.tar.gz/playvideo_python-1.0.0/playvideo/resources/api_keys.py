"""API Keys resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from playvideo.types import ApiKey, ApiKeyWithKey

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_api_key(data: dict[str, Any]) -> ApiKey:
    """Parse API key from API response."""
    return ApiKey(
        id=data["id"],
        name=data["name"],
        key_prefix=data["keyPrefix"],
        last_used_at=data.get("lastUsedAt"),
        expires_at=data.get("expiresAt"),
        created_at=data["createdAt"],
    )


class SyncApiKeys:
    """Synchronous API keys resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def list(self) -> list[ApiKey]:
        """List all API keys."""
        data = self._http.get("/api-keys")
        return [_parse_api_key(k) for k in data.get("apiKeys", [])]

    def create(self, name: str) -> ApiKeyWithKey:
        """Create a new API key.

        Note: The full key is only returned once. Store it securely.
        """
        data = self._http.post("/api-keys", json={"name": name})
        key_data = data["apiKey"]
        return ApiKeyWithKey(
            id=key_data["id"],
            name=key_data["name"],
            key_prefix=key_data["keyPrefix"],
            last_used_at=key_data.get("lastUsedAt"),
            expires_at=key_data.get("expiresAt"),
            created_at=key_data["createdAt"],
            key=key_data["key"],
        )

    def delete(self, key_id: str) -> dict[str, str]:
        """Delete an API key."""
        return self._http.delete(f"/api-keys/{quote(key_id)}")


class AsyncApiKeys:
    """Asynchronous API keys resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> list[ApiKey]:
        """List all API keys."""
        data = await self._http.get("/api-keys")
        return [_parse_api_key(k) for k in data.get("apiKeys", [])]

    async def create(self, name: str) -> ApiKeyWithKey:
        """Create a new API key."""
        data = await self._http.post("/api-keys", json={"name": name})
        key_data = data["apiKey"]
        return ApiKeyWithKey(
            id=key_data["id"],
            name=key_data["name"],
            key_prefix=key_data["keyPrefix"],
            last_used_at=key_data.get("lastUsedAt"),
            expires_at=key_data.get("expiresAt"),
            created_at=key_data["createdAt"],
            key=key_data["key"],
        )

    async def delete(self, key_id: str) -> dict[str, str]:
        """Delete an API key."""
        return await self._http.delete(f"/api-keys/{quote(key_id)}")
