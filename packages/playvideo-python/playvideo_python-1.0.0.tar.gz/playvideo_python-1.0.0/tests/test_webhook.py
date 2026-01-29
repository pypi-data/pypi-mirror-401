"""Tests for webhook signature verification."""

import hashlib
import hmac
import json
import time

import pytest

from playvideo.errors import WebhookSignatureError
from playvideo.webhook import construct_event, verify_signature


def compute_signature(payload: str, timestamp: int, secret: str) -> str:
    """Compute HMAC-SHA256 signature for testing."""
    signed_payload = f"{timestamp}.{payload}"
    return hmac.new(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()


class TestVerifySignature:
    """Tests for verify_signature function."""

    def test_valid_signature(self):
        """Test verification of valid signature."""
        secret = "whsec_test_secret_key"
        payload = json.dumps({"event": "video.completed", "data": {"videoId": "vid1"}})
        timestamp = int(time.time() * 1000)
        signature = compute_signature(payload, timestamp, secret)

        # Should not raise
        verify_signature(payload, f"sha256={signature}", str(timestamp), secret)

    def test_valid_signature_with_int_timestamp(self):
        """Test verification with integer timestamp."""
        secret = "whsec_test_secret_key"
        payload = json.dumps({"event": "video.completed"})
        timestamp = int(time.time() * 1000)
        signature = compute_signature(payload, timestamp, secret)

        verify_signature(payload, f"sha256={signature}", timestamp, secret)

    def test_missing_signature(self):
        """Test error on missing signature."""
        with pytest.raises(WebhookSignatureError, match="Missing"):
            verify_signature("payload", "", "123456", "secret")

    def test_missing_timestamp(self):
        """Test error on missing timestamp."""
        with pytest.raises(WebhookSignatureError, match="Missing"):
            verify_signature("payload", "sha256=abc", "", "secret")

    def test_missing_secret(self):
        """Test error on missing secret."""
        with pytest.raises(WebhookSignatureError, match="Missing"):
            verify_signature("payload", "sha256=abc", "123456", "")

    def test_invalid_timestamp(self):
        """Test error on invalid timestamp format."""
        with pytest.raises(WebhookSignatureError, match="Invalid timestamp"):
            verify_signature("payload", "sha256=abc", "not-a-number", "secret")

    def test_old_timestamp(self):
        """Test error on old timestamp."""
        secret = "whsec_test_secret_key"
        payload = json.dumps({"event": "video.completed"})
        old_timestamp = int((time.time() - 400) * 1000)  # 400 seconds ago
        signature = compute_signature(payload, old_timestamp, secret)

        with pytest.raises(WebhookSignatureError, match="too old"):
            verify_signature(
                payload, f"sha256={signature}", str(old_timestamp), secret, tolerance=300
            )

    def test_future_timestamp(self):
        """Test error on future timestamp beyond tolerance."""
        secret = "whsec_test_secret_key"
        payload = json.dumps({"event": "video.completed"})
        future_timestamp = int((time.time() + 400) * 1000)  # 400 seconds in future
        signature = compute_signature(payload, future_timestamp, secret)

        with pytest.raises(WebhookSignatureError, match="too old"):
            verify_signature(
                payload, f"sha256={signature}", str(future_timestamp), secret, tolerance=300
            )

    def test_custom_tolerance(self):
        """Test custom tolerance is respected."""
        secret = "whsec_test_secret_key"
        payload = json.dumps({"event": "video.completed"})
        old_timestamp = int((time.time() - 500) * 1000)  # 500 seconds ago
        signature = compute_signature(payload, old_timestamp, secret)

        # Should fail with 5 minute tolerance
        with pytest.raises(WebhookSignatureError):
            verify_signature(
                payload, f"sha256={signature}", str(old_timestamp), secret, tolerance=300
            )

        # Should pass with 10 minute tolerance
        verify_signature(payload, f"sha256={signature}", str(old_timestamp), secret, tolerance=600)

    def test_invalid_signature_format(self):
        """Test error on invalid signature format."""
        timestamp = int(time.time() * 1000)
        with pytest.raises(WebhookSignatureError):
            verify_signature("payload", "invalid_format", str(timestamp), "secret")

    def test_non_sha256_algorithm(self):
        """Test error on non-sha256 algorithm."""
        timestamp = int(time.time() * 1000)
        with pytest.raises(WebhookSignatureError):
            verify_signature("payload", "md5=abc123", str(timestamp), "secret")

    def test_signature_mismatch(self):
        """Test error on signature mismatch."""
        timestamp = int(time.time() * 1000)
        with pytest.raises(WebhookSignatureError, match="Signature mismatch"):
            verify_signature("payload", "sha256=invalid_signature", str(timestamp), "secret")

    def test_tampered_payload(self):
        """Test error on tampered payload."""
        secret = "whsec_test_secret_key"
        original_payload = json.dumps({"event": "video.completed", "data": {"videoId": "vid1"}})
        tampered_payload = json.dumps({"event": "video.completed", "data": {"videoId": "vid2"}})
        timestamp = int(time.time() * 1000)
        signature = compute_signature(original_payload, timestamp, secret)

        with pytest.raises(WebhookSignatureError, match="Signature mismatch"):
            verify_signature(tampered_payload, f"sha256={signature}", str(timestamp), secret)

    def test_wrong_secret(self):
        """Test error on wrong secret."""
        secret = "whsec_test_secret_key"
        payload = json.dumps({"event": "video.completed"})
        timestamp = int(time.time() * 1000)
        signature = compute_signature(payload, timestamp, secret)

        with pytest.raises(WebhookSignatureError, match="Signature mismatch"):
            verify_signature(payload, f"sha256={signature}", str(timestamp), "wrong_secret")


class TestConstructEvent:
    """Tests for construct_event function."""

    def test_construct_valid_event(self):
        """Test constructing a valid event."""
        secret = "whsec_test_secret_key"
        event_data = {
            "event": "video.completed",
            "timestamp": int(time.time() * 1000),
            "data": {
                "videoId": "vid123",
                "playlistUrl": "https://cdn.example.com/vid123/playlist.m3u8",
            },
        }
        payload = json.dumps(event_data)
        timestamp = int(time.time() * 1000)
        signature = compute_signature(payload, timestamp, secret)

        event = construct_event(payload, f"sha256={signature}", str(timestamp), secret)

        assert event["event"] == "video.completed"
        assert event["data"]["videoId"] == "vid123"

    def test_construct_event_with_bytes(self):
        """Test constructing event from bytes payload."""
        secret = "whsec_test_secret_key"
        event_data = {
            "event": "video.failed",
            "timestamp": int(time.time() * 1000),
            "data": {"videoId": "vid456", "error": "Transcoding failed"},
        }
        payload = json.dumps(event_data)
        timestamp = int(time.time() * 1000)
        signature = compute_signature(payload, timestamp, secret)

        event = construct_event(payload.encode(), f"sha256={signature}", str(timestamp), secret)

        assert event["event"] == "video.failed"
        assert event["data"]["error"] == "Transcoding failed"

    def test_construct_event_invalid_signature(self):
        """Test error on invalid signature."""
        timestamp = int(time.time() * 1000)
        with pytest.raises(WebhookSignatureError):
            construct_event(
                '{"event": "video.completed"}',
                "sha256=invalid",
                str(timestamp),
                "secret",
            )

    def test_construct_event_invalid_json(self):
        """Test error on invalid JSON payload."""
        secret = "whsec_test_secret_key"
        payload = "not valid json"
        timestamp = int(time.time() * 1000)
        signature = compute_signature(payload, timestamp, secret)

        with pytest.raises(WebhookSignatureError, match="Invalid JSON"):
            construct_event(payload, f"sha256={signature}", str(timestamp), secret)


class TestWebhookSignatureError:
    """Tests for WebhookSignatureError."""

    def test_error_message(self):
        """Test error has correct message."""
        error = WebhookSignatureError("Test message")
        assert "Test message" in str(error)

    def test_error_is_exception(self):
        """Test error is an Exception."""
        error = WebhookSignatureError("Test")
        assert isinstance(error, Exception)
