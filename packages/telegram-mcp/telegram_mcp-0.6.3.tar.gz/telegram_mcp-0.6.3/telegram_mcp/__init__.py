"""
Telegram MCP - Thin stdio client for Telegram communication.

Enables AI agents to communicate with users via Telegram.
Uses polling for replies to work around proxy timeouts.
"""

import asyncio
import base64
import logging
import os
import sys
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# Configuration
SERVER_URL = os.environ.get("TELEGRAM_SERVER_URL", "https://telegram-mcp.furkankucuk.net")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
POLL_INTERVAL = 5  # seconds between polls


def _build_headers(
    project_name: str,
    session_name: str,
) -> dict[str, str]:
    """Build headers for API requests, including project/session info.
    
    Args:
        project_name: Project/repository name for message header.
        session_name: Current task/session context for message header.
    """
    return {
        "X-Chat-Id": CHAT_ID,
        "X-Agent-Name": project_name,
        "X-Session-Name": session_name,
    }


def _poll_headers() -> dict[str, str]:
    """Build headers for poll requests (only needs chat_id)."""
    return {"X-Chat-Id": CHAT_ID}

# MCP Server
mcp = FastMCP(
    name="Telegram MCP",
    instructions="""
Telegram is your ONLY communication channel with the user. Follow these rules:

1. USE TELEGRAM FOR EVERYTHING
   - All status updates, questions, results go through interact()
   - Never assume the user can see your internal actions

2. ALWAYS END WITH wait_for_reply=True
   - After completing any task: interact(..., "Done! What's next?", wait_for_reply=True)
   - This keeps the conversation alive and lets user give next instructions
   - NEVER just end without asking - the user expects continued interaction

3. ACKNOWLEDGE IMMEDIATELY
   - After receiving a reply, send acknowledgement before doing work
   - Example: "Got it! Working on that now..."

4. USE MEANINGFUL HEADERS
   - project_name: Use the project/repo name (e.g., "telegram-mcp")
   - session_name: Describe current task (e.g., "Fix login bug")
""",
)


async def _poll_for_reply(client: httpx.AsyncClient, request_id: str) -> dict:
    """Poll the server until we get a reply, or until request expires/cancels."""
    while True:
        response = await client.get(
            f"{SERVER_URL}/api/poll",
            headers=_poll_headers(),
            params={"request_id": request_id},
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Poll error: {response.text}")
        
        data = response.json()
        status = data.get("status")
        
        if status == "completed":
            return data.get("reply", {})
        
        if status == "expired":
            raise TimeoutError(data.get("message", "Request expired"))
        
        if status == "cancelled":
            raise RuntimeError(data.get("message", "Request was cancelled"))
        
        if status == "pending":
            await asyncio.sleep(POLL_INTERVAL)
            continue
        
        # Unknown status - treat as error
        if "error" in data:
            raise RuntimeError(data["error"])
        
        # Fallback: unknown status, keep polling
        await asyncio.sleep(POLL_INTERVAL)


def _encode_file(file_path: str) -> tuple[str, str]:
    """Read and base64 encode a local file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    
    return data, path.name


@mcp.tool()
async def interact(
    project_name: str,
    session_name: str,
    message: str | None = None,
    wait_for_reply: bool = False,
    choices: list[str] | None = None,
    media_type: str | None = None,
    media_url: str | None = None,
    media_path: str | None = None,
) -> dict:
    """
    Send a message or media to the user via Telegram.

    Args:
        project_name: Project/repository name (e.g., "my-project"). Shown in message header.
        session_name: Current task/session context (e.g., "Fix login bug"). Shown in message header.
        message: Text message to send. Can be combined with media.
        wait_for_reply: If True, block until user replies.
        choices: Button labels for quick replies.
        media_type: Type of media - "photo", "video", "audio", or "document".
        media_url: URL of the media file to send (for remote files).
        media_path: Local file path to send (for local files).

    Returns:
        For text replies: {"reply": "user's text"}
        For media replies: {"reply": {"text": "caption", "media": {"type": "photo", "url": "..."}}}
        When not waiting: {"reply": None, "message_id": 123}

    IMPORTANT - User Experience Guidelines:
        Telegram is your ONLY communication channel with the user. Follow these rules:

        1. USE TELEGRAM FOR EVERYTHING
        - All status updates, questions, results go through interact()
        - Never assume the user can see your internal actions

        2. ALWAYS END WITH wait_for_reply=True
        - After completing any task: interact(..., "Done! What's next?", wait_for_reply=True)
        - This keeps the conversation alive and lets user give next instructions
        - NEVER just end without asking - the user expects continued interaction

        3. ACKNOWLEDGE IMMEDIATELY
        - After receiving a reply, send acknowledgement before doing work
        - Example: "Got it! Working on that now..."

        4. USE MEANINGFUL HEADERS
        - project_name: Use the project/repo name (e.g., "telegram-mcp")
        - session_name: Describe current task (e.g., "Fix login bug")

    Examples:
        # Simple status update
        interact("my-project", "Deploy to prod", "Working on it...")
        
        # Ask a question and acknowledge the response
        result = interact("my-project", "Code review", "What should I do?", wait_for_reply=True)
        interact("my-project", "Code review", f"Got it! Working on: {result['reply']}")
        # ... then do the actual work
        
        # Yes/No with acknowledgement
        result = interact("my-project", "Cleanup", "Delete?", choices=["Yes", "No"], wait_for_reply=True)
        if result["reply"] == "Yes":
            interact("my-project", "Cleanup", "Deleting now...")
            # ... perform deletion
        
        # Send a photo from URL
        interact("my-project", "Results", "Here's the result:", media_type="photo", media_url="https://...")
        
        # Send a local file
        interact("my-project", "Export", "Generated image:", media_type="photo", media_path="/path/to/image.png")
    """
    if not CHAT_ID:
        raise RuntimeError("TELEGRAM_CHAT_ID environment variable required")
    
    if not message and not media_url and not media_path:
        raise ValueError("Either message, media_url, or media_path must be provided")
    
    if media_url and media_path:
        raise ValueError("Cannot specify both media_url and media_path")

    # Prepare request body
    body = {
        "message": message,
        "wait_for_reply": wait_for_reply,
        "choices": choices,
        "media_type": media_type,
        "media_url": media_url,
    }
    
    # Handle local file upload
    if media_path:
        media_data, media_filename = _encode_file(media_path)
        body["media_data"] = media_data
        body["media_filename"] = media_filename
        
        # Infer media_type from extension if not provided
        if not media_type:
            ext = Path(media_path).suffix.lower()
            type_map = {
                ".jpg": "photo", ".jpeg": "photo", ".png": "photo", ".gif": "photo", ".webp": "photo",
                ".mp4": "video", ".mov": "video", ".avi": "video", ".webm": "video",
                ".mp3": "audio", ".ogg": "audio", ".wav": "audio", ".m4a": "audio",
            }
            body["media_type"] = type_map.get(ext, "document")

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{SERVER_URL}/api/interact",
            headers=_build_headers(project_name, session_name),
            json=body,
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Server error: {response.text}")
        
        data = response.json()
        
        if not wait_for_reply:
            return {"reply": None, "message_id": data.get("message_id")}
        
        request_id = data.get("request_id")
        if not request_id:
            return {"reply": None}
        
        reply = await _poll_for_reply(client, request_id)
        return {"reply": reply}


@mcp.tool()
async def get_messages(limit: int = 10) -> dict:
    """
    Get recent Telegram conversation history.

    Args:
        limit: Number of messages (1-50, default 10).

    Returns:
        messages: List of recent messages with text and media info.
    """
    if not CHAT_ID:
        raise RuntimeError("TELEGRAM_CHAT_ID environment variable required")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{SERVER_URL}/api/messages",
            headers=_poll_headers(),
            params={"limit": limit},
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Server error: {response.text}")
        
        return response.json()


def main():
    """Run the MCP server."""
    if not CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID environment variable required")
        sys.exit(1)
    
    logger.info(f"Starting Telegram MCP (server: {SERVER_URL}, chat_id: {CHAT_ID})")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
