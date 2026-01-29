"""Account resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from playvideo.types import Account

if TYPE_CHECKING:
    from playvideo._internal.http import AsyncHttpClient, SyncHttpClient


def _parse_account(data: dict[str, Any]) -> Account:
    """Parse account from API response."""
    return Account(
        id=data["id"],
        email=data["email"],
        name=data.get("name"),
        plan=data["plan"],
        allowed_domains=data.get("allowedDomains", []),
        allow_localhost=data.get("allowLocalhost", False),
        r2_bucket_name=data.get("r2BucketName"),
        r2_bucket_region=data.get("r2BucketRegion"),
        created_at=data["createdAt"],
    )


class SyncAccount:
    """Synchronous account resource."""

    def __init__(self, http: SyncHttpClient) -> None:
        self._http = http

    def get(self) -> Account:
        """Get account information."""
        data = self._http.get("/account")
        return _parse_account(data)

    def update(
        self,
        *,
        allowed_domains: list[str] | None = None,
        allow_localhost: bool | None = None,
    ) -> Account:
        """Update account settings."""
        payload: dict[str, Any] = {}
        if allowed_domains is not None:
            payload["allowedDomains"] = allowed_domains
        if allow_localhost is not None:
            payload["allowLocalhost"] = allow_localhost

        data = self._http.patch("/account", json=payload)
        return _parse_account(data.get("account", data))


class AsyncAccount:
    """Asynchronous account resource."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> Account:
        """Get account information."""
        data = await self._http.get("/account")
        return _parse_account(data)

    async def update(
        self,
        *,
        allowed_domains: list[str] | None = None,
        allow_localhost: bool | None = None,
    ) -> Account:
        """Update account settings."""
        payload: dict[str, Any] = {}
        if allowed_domains is not None:
            payload["allowedDomains"] = allowed_domains
        if allow_localhost is not None:
            payload["allowLocalhost"] = allow_localhost

        data = await self._http.patch("/account", json=payload)
        return _parse_account(data.get("account", data))
