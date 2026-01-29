"""
Webhook signature verification utilities.

Usage:
    >>> from playvideo.webhook import verify_signature, construct_event
    >>>
    >>> # Verify a signature
    >>> is_valid = verify_signature(payload, signature, timestamp, secret)
    >>>
    >>> # Construct and verify an event
    >>> event = construct_event(payload, signature, timestamp, secret)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

from playvideo.errors import WebhookSignatureError


def verify_signature(
    payload: str | bytes | dict[str, Any],
    signature: str,
    timestamp: str | int,
    secret: str,
    tolerance: int = 300,
) -> bool:
    """
    Verify a webhook signature.

    Args:
        payload: The raw webhook payload (string, bytes, or dict)
        signature: The X-PlayVideo-Signature header value
        timestamp: The X-PlayVideo-Timestamp header value
        secret: Your webhook secret (whsec_xxx)
        tolerance: Maximum age of the webhook in seconds (default: 300)

    Returns:
        True if the signature is valid

    Raises:
        WebhookSignatureError: If the signature is invalid
    """
    if not signature or not timestamp or not secret:
        raise WebhookSignatureError("Missing required parameters for signature verification")

    # Parse timestamp
    try:
        ts = int(timestamp)
    except (ValueError, TypeError) as e:
        raise WebhookSignatureError("Invalid timestamp") from e

    # Check timestamp tolerance
    now = int(time.time() * 1000)
    age = abs(now - ts) / 1000
    if age > tolerance:
        raise WebhookSignatureError(f"Webhook timestamp too old ({int(age)}s > {tolerance}s)")

    # Extract signature value (format: sha256=xxx)
    sig_parts = signature.split("=")
    if len(sig_parts) != 2 or sig_parts[0] != "sha256":
        raise WebhookSignatureError("Invalid signature format")
    expected_sig = sig_parts[1]

    # Prepare payload string
    if isinstance(payload, bytes):
        payload_str = payload.decode("utf-8")
    elif isinstance(payload, dict):
        payload_str = json.dumps(payload, separators=(",", ":"))
    else:
        payload_str = payload

    # Compute signature
    signed_payload = f"{ts}.{payload_str}"
    computed_sig = hmac.new(
        secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison
    if not hmac.compare_digest(expected_sig, computed_sig):
        raise WebhookSignatureError("Signature mismatch")

    return True


def construct_event(
    payload: str | bytes | dict[str, Any],
    signature: str,
    timestamp: str | int,
    secret: str,
    tolerance: int = 300,
) -> dict[str, Any]:
    """
    Construct and verify a webhook event.

    Args:
        payload: The raw webhook payload
        signature: The X-PlayVideo-Signature header
        timestamp: The X-PlayVideo-Timestamp header
        secret: Your webhook secret
        tolerance: Maximum age in seconds

    Returns:
        The parsed webhook event with keys: event, timestamp, data

    Raises:
        WebhookSignatureError: If the signature is invalid
    """
    verify_signature(payload, signature, timestamp, secret, tolerance)

    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        try:
            parsed: dict[str, Any] = json.loads(payload)
            return parsed
        except json.JSONDecodeError as e:
            raise WebhookSignatureError(f"Invalid JSON payload: {e}") from e

    # payload is already a dict
    return dict(payload)
