"""
PlayVideo SDK Errors
"""

from typing import Any


class PlayVideoError(Exception):
    """Base exception for all PlayVideo SDK errors."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        request_id: str | None = None,
        param: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.request_id = request_id
        self.param = param

    def __str__(self) -> str:
        parts = [self.message]
        if self.code:
            parts.append(f"(code: {self.code})")
        if self.request_id:
            parts.append(f"[request_id: {self.request_id}]")
        return " ".join(parts)


class AuthenticationError(PlayVideoError):
    """Authentication failed - invalid or missing API key (401)."""

    def __init__(self, message: str = "Invalid or missing API key", **kwargs: Any) -> None:
        super().__init__(message, status_code=401, **kwargs)


class AuthorizationError(PlayVideoError):
    """Authorization failed - insufficient permissions (403)."""

    def __init__(self, message: str = "Insufficient permissions", **kwargs: Any) -> None:
        super().__init__(message, status_code=403, **kwargs)


class NotFoundError(PlayVideoError):
    """Resource not found (404)."""

    def __init__(self, message: str = "Resource not found", **kwargs: Any) -> None:
        super().__init__(message, status_code=404, **kwargs)


class ValidationError(PlayVideoError):
    """Validation failed - invalid request parameters (400/422)."""

    def __init__(
        self,
        message: str = "Invalid request parameters",
        status_code: int = 400,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=status_code, **kwargs)


class ConflictError(PlayVideoError):
    """Resource conflict (409)."""

    def __init__(self, message: str = "Resource conflict", **kwargs: Any) -> None:
        super().__init__(message, status_code=409, **kwargs)


class RateLimitError(PlayVideoError):
    """Rate limit exceeded (429)."""

    def __init__(
        self,
        message: str = "Too many requests",
        *,
        retry_after: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after


class ServerError(PlayVideoError):
    """Server error (5xx)."""

    def __init__(self, message: str = "Server error", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)


class NetworkError(PlayVideoError):
    """Network connection error."""

    def __init__(self, message: str = "Network error", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)


class TimeoutError(NetworkError):
    """Request timed out."""

    def __init__(self, message: str = "Request timed out", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)


class WebhookSignatureError(PlayVideoError):
    """Webhook signature verification failed."""

    def __init__(self, message: str = "Invalid webhook signature") -> None:
        super().__init__(message, code="webhook_signature_error")


def parse_api_error(
    status_code: int,
    body: dict[str, Any],
    request_id: str | None = None,
) -> PlayVideoError:
    """Parse API error response and return appropriate exception."""
    message = body.get("message") or body.get("error") or f"HTTP {status_code}"
    kwargs: dict[str, Any] = {
        "code": body.get("code"),
        "request_id": request_id,
        "param": body.get("param"),
    }

    if status_code == 401:
        return AuthenticationError(message, **kwargs)
    elif status_code == 403:
        return AuthorizationError(message, **kwargs)
    elif status_code == 404:
        return NotFoundError(message, **kwargs)
    elif status_code == 409:
        return ConflictError(message, **kwargs)
    elif status_code == 429:
        return RateLimitError(message, **kwargs)
    elif status_code in (400, 422):
        return ValidationError(message, status_code=status_code, **kwargs)
    elif status_code >= 500:
        return ServerError(message, status_code=status_code, **kwargs)
    else:
        return PlayVideoError(message, status_code=status_code, **kwargs)
