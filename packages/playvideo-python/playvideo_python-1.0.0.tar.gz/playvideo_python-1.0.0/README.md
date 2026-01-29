# PlayVideo SDK for Python

[![CI](https://github.com/PlayVideo-dev/playvideo-python/actions/workflows/ci.yml/badge.svg)](https://github.com/PlayVideo-dev/playvideo-python/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/playvideo-python.svg)](https://pypi.org/project/playvideo-python/)
[![PyPI downloads](https://img.shields.io/pypi/dm/playvideo-python.svg)](https://pypi.org/project/playvideo-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Official Python SDK for the [PlayVideo](https://playvideo.dev) API - Video hosting for developers.

## Installation

```bash
pip install playvideo
```

**Requirements:** Python 3.10+

## Quick Start

### Synchronous Client

```python
from playvideo import PlayVideo

client = PlayVideo("play_live_xxx")

# List collections
collections = client.collections.list()

# Upload a video
response = client.videos.upload(
    "./video.mp4",
    "my-collection",
    on_progress=lambda p: print(f"{p.percent}%")
)

# Watch processing progress
for event in client.videos.watch_progress(response.video["id"]):
    print(event.stage, event.message)
    if event.stage == "completed":
        print("Video ready:", event.playlist_url)
        break

client.close()
```

### Async Client

```python
from playvideo import AsyncPlayVideo
import asyncio

async def main():
    async with AsyncPlayVideo("play_live_xxx") as client:
        # List collections
        collections = await client.collections.list()
        
        # Upload a video
        response = await client.videos.upload("./video.mp4", "my-collection")
        
        # Watch processing progress
        async for event in client.videos.watch_progress(response.video["id"]):
            print(event.stage)
            if event.stage == "completed":
                break

asyncio.run(main())
```

## Resources

### Collections

```python
# List all collections
collections = client.collections.list()

# Create a collection
collection = client.collections.create("My Videos", description="Tutorial videos")

# Get a collection with videos
collection = client.collections.get("my-videos")

# Delete a collection
client.collections.delete("my-videos")
```

### Videos

```python
# List videos
videos = client.videos.list()

# Filter by collection or status
videos = client.videos.list(collection="my-collection", status="COMPLETED", limit=50)

# Get a video
video = client.videos.get("video-id")

# Upload with progress
def on_progress(progress):
    print(f"{progress.percent}% ({progress.loaded}/{progress.total})")

response = client.videos.upload("./video.mp4", "my-collection", on_progress=on_progress)

# Delete a video
client.videos.delete("video-id")

# Get embed information
embed_info = client.videos.get_embed_info("video-id")

# Watch processing progress
for event in client.videos.watch_progress("video-id"):
    match event.stage:
        case "pending":
            print("Waiting in queue...")
        case "processing":
            print("Transcoding...")
        case "completed":
            print("Done!", event.playlist_url)
        case "failed":
            print("Failed:", event.error)
```

### Webhooks

```python
# List webhooks
webhooks, available_events = client.webhooks.list()

# Create a webhook
webhook = client.webhooks.create(
    url="https://example.com/webhook",
    events=["video.completed", "video.failed"]
)
# Save webhook.secret - only shown once!

# Update a webhook
client.webhooks.update("webhook-id", events=["video.completed"], is_active=False)

# Test a webhook
result = client.webhooks.test("webhook-id")

# Delete a webhook
client.webhooks.delete("webhook-id")
```

### Embed Settings

```python
# Get embed settings
settings = client.embed.get_settings()

# Update embed settings
settings = client.embed.update_settings(
    primary_color="#FF0000",
    autoplay=True,
    muted=True
)

# Generate signed embed URL
embed = client.embed.sign("video-id")
print(embed.embed_url)
print(embed.embed_code["responsive"])
```

### API Keys

```python
# List API keys
api_keys = client.api_keys.list()

# Create an API key
key = client.api_keys.create("My App")
# Save key.key - only shown once!

# Delete an API key
client.api_keys.delete("key-id")
```

### Account

```python
# Get account info
account = client.account.get()

# Update allowed domains
account = client.account.update(
    allowed_domains=["example.com", "app.example.com"],
    allow_localhost=True
)
```

### Usage

```python
# Get usage statistics
usage = client.usage.get()

print(f"Plan: {usage.plan}")
print(f"Videos: {usage.usage.videos_this_month}/{usage.usage.videos_limit}")
print(f"Storage: {usage.usage.storage_used_gb} GB")
```

## Webhook Signature Verification

```python
from playvideo.webhook import verify_signature, construct_event
from playvideo.errors import WebhookSignatureError

# Flask example
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_data()
    signature = request.headers.get("X-PlayVideo-Signature")
    timestamp = request.headers.get("X-PlayVideo-Timestamp")
    
    try:
        event = construct_event(payload, signature, timestamp, "whsec_xxx")
        
        match event["event"]:
            case "video.completed":
                print("Video ready:", event["data"])
            case "video.failed":
                print("Video failed:", event["data"])
        
        return "OK", 200
    except WebhookSignatureError as e:
        print("Invalid signature:", e)
        return "Invalid signature", 400
```

## Error Handling

```python
from playvideo import PlayVideo
from playvideo.errors import (
    PlayVideoError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

client = PlayVideo("play_live_xxx")

try:
    client.videos.get("invalid-id")
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Video not found")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Invalid param: {e.param}")
except PlayVideoError as e:
    print(f"API error: {e.message} (code: {e.code})")
```

### Error Types

| Error | Status | Description |
|-------|--------|-------------|
| `AuthenticationError` | 401 | Invalid or missing API key |
| `AuthorizationError` | 403 | Insufficient permissions |
| `NotFoundError` | 404 | Resource not found |
| `ValidationError` | 400/422 | Invalid parameters |
| `ConflictError` | 409 | Resource conflict |
| `RateLimitError` | 429 | Too many requests |
| `ServerError` | 5xx | Server error |
| `NetworkError` | - | Connection failed |
| `TimeoutError` | - | Request timed out |
| `WebhookSignatureError` | - | Invalid signature |

## Configuration

```python
client = PlayVideo(
    "play_live_xxx",
    # Custom base URL (for self-hosted)
    base_url="https://api.yourdomain.com/api/v1",
    # Request timeout in seconds (default: 30)
    timeout=60.0,
)
```

## Context Managers

Both sync and async clients support context managers:

```python
# Sync
with PlayVideo("play_live_xxx") as client:
    collections = client.collections.list()

# Async
async with AsyncPlayVideo("play_live_xxx") as client:
    collections = await client.collections.list()
```

## Type Hints

The SDK includes full type hints for all methods and data classes:

```python
from playvideo import PlayVideo, Video, Collection, VideoStatus

client = PlayVideo("play_live_xxx")

video: Video = client.videos.get("id")
status: VideoStatus = video.status  # Literal["PENDING", "PROCESSING", "COMPLETED", "FAILED"]
```

## MCP Server

Use the PlayVideo MCP server to connect Claude/Desktop assistants to your account.

```bash
npm install -g @playvideo/playvideo-mcp
```

Repo: https://github.com/PlayVideo-dev/playvideo-mcp

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT - see [LICENSE](LICENSE) for details.

## Links

- [Documentation](https://playvideo.dev/docs)
- [API Reference](https://playvideo.dev/docs/api)
- [Dashboard](https://playvideo.dev/dashboard)
- [GitHub](https://github.com/PlayVideo-dev/playvideo-python)
