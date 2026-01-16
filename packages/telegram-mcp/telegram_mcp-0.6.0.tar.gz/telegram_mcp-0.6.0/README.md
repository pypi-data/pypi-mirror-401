# Telegram MCP

MCP server that lets AI agents communicate with users via Telegram.

## Installation

```bash
pip install telegram-mcp
```

## Configuration

Add to your MCP client config (e.g., Antigravity, Claude Desktop):

```json
{
  "telegram": {
    "command": "telegram-mcp",
    "env": {
      "TELEGRAM_CHAT_ID": "your-chat-id"
    }
  }
}
```

**Get your chat ID:** Message [@agent_comm_mcp_bot](https://t.me/agent_comm_mcp_bot) on Telegram and send `/start`.

That's it! No bot token needed - the client connects to our hosted server.

## Tools

### `interact`

Send a message or media to the user via Telegram.

```python
# Simple status update
interact(message="Working on it...")

# Wait for reply and acknowledge
result = interact(message="What's next?", wait_for_reply=True)
interact(f"Got it! Working on: {result['reply']}")  # Always acknowledge!

# Yes/No buttons with acknowledgement
result = interact(message="Delete?", choices=["Yes", "No"], wait_for_reply=True)
if result["reply"] == "Yes":
    interact("Deleting now...")  # Acknowledge before action!

# Send a photo from URL
interact(message="Here's the result:", media_type="photo", media_url="https://...")

# Send a local file
interact(message="Generated image:", media_type="photo", media_path="/path/to/image.png")

# Send a document
interact(media_type="document", media_path="/path/to/report.pdf")
```

**Important**: After receiving a user reply, always send an acknowledgement immediately!

**User Reply Requirement**: When responding to `wait_for_reply` messages, users must **swipe the message** in Telegram to reply. This ensures replies go to the correct request, especially when multiple agents are active.

**Parameters:**
- `message`: Text to send (optional if sending media)
- `wait_for_reply`: Block until user replies (default: False)
- `choices`: Button labels for quick replies
- `media_type`: "photo", "video", "audio", or "document" (auto-detected from extension if not provided)
- `media_url`: URL of remote media to send
- `media_path`: Local file path to upload and send

**Response format:**
```python
# Text reply
{"reply": "user's text message"}

# Media reply (when user sends photo/video/audio/document)
{
    "reply": {
        "text": "caption if any",
        "media": {
            "type": "photo",
            "file_id": "telegram_file_id",
            "url": "https://api.telegram.org/file/..."
        }
    }
}

# No reply (when wait_for_reply=False)
{"reply": None, "message_id": 123}
```

### `get_messages`

Get recent conversation history.

```python
result = get_messages(limit=10)
```

## Self-Hosting

If you prefer to run your own server:

```json
{
  "telegram": {
    "command": "telegram-mcp",
    "env": {
      "TELEGRAM_SERVER_URL": "https://your-server.com",
      "TELEGRAM_CHAT_ID": "your-chat-id"
    }
  }
}
```

See [the GitHub repo](https://github.com/iamkucuk/telegram-mcp-server) for server setup.

## License

MIT
