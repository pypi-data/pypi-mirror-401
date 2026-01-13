"""Telegram Bot MCP Server.

This module provides a FastMCP server for interacting with Telegram channels:
- Publishing messages to channels
- Publishing photos with captions
- Editing existing messages
- Editing photo captions
- Searching messages (from cache)
- Deleting messages
- Getting channel information
"""

import logging
from typing import Any, Optional
from importlib.metadata import version

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from telegram.error import TelegramError

from telegram_bot_mcp.telegram_bot.client import TelegramBotClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global client instance for reuse across tool calls
_client: Optional[TelegramBotClient] = None


def _get_client() -> TelegramBotClient:
    """Get or create the global Telegram bot client."""
    global _client
    if _client is None:
        logger.info("Initializing Telegram bot client")
        _client = TelegramBotClient()
    return _client


def _format_message_markdown(result: dict[str, Any]) -> str:
    """Format message result as Markdown."""
    msg_id = result.get("message_id")
    chat_id = result.get("chat_id")
    date = result.get("date", "")
    text = result.get("text", "")
    link = result.get("link", "N/A")

    return f"""✅ Message Published Successfully

**Message ID**: {msg_id}
**Chat ID**: {chat_id}
**Date**: {date}
**Link**: {link}

**Content**:
> {text}
"""


def _format_photo_markdown(result: dict[str, Any]) -> str:
    """Format photo message result as Markdown."""
    msg_id = result.get("message_id")
    chat_id = result.get("chat_id")
    date = result.get("date", "")
    caption = result.get("caption", "")
    link = result.get("link", "N/A")
    photo = result.get("photo", {})

    photo_info = ""
    if photo:
        photo_info = f"\n**Photo Size**: {photo.get('width')}x{photo.get('height')}"
        if photo.get("file_size"):
            photo_info += f" ({photo.get('file_size')} bytes)"

    caption_text = f"\n**Caption**:\n> {caption}" if caption else ""

    return f"""✅ Photo Published Successfully

**Message ID**: {msg_id}
**Chat ID**: {chat_id}
**Date**: {date}
**Link**: {link}{photo_info}{caption_text}
"""


def _format_album_markdown(result: dict[str, Any]) -> str:
    """Format photo album result as Markdown."""
    album_id = result.get("album_id", "N/A")
    message_count = result.get("message_count", 0)
    first_msg_id = result.get("first_message_id")
    chat_id = result.get("chat_id")
    messages = result.get("messages", [])

    photos_list = "\n".join([
        f"{i+1}. Message ID: {msg.get('message_id')} - {msg.get('link', 'No link')}"
        for i, msg in enumerate(messages)
    ])

    return f"""✅ Photo Album Published Successfully

**Album ID**: {album_id}
**Photos Count**: {message_count}
**First Message ID**: {first_msg_id}
**Chat ID**: {chat_id}

**Photos in Album**:
{photos_list}
"""


def _format_edit_markdown(result: dict[str, Any], content_type: str = "text") -> str:
    """Format edit result as Markdown."""
    msg_id = result.get("message_id")
    chat_id = result.get("chat_id")
    edit_date = result.get("edit_date", "")
    link = result.get("link", "N/A")

    if content_type == "caption":
        caption = result.get("caption", "")
        content_display = f"\n**Updated Caption**:\n> {caption}"
    else:
        text = result.get("text", "")
        content_display = f"\n**Updated Text**:\n> {text}"

    return f"""✅ Message Edited Successfully

**Message ID**: {msg_id}
**Chat ID**: {chat_id}
**Edit Date**: {edit_date}
**Link**: {link}{content_display}
"""


def _format_delete_markdown(result: dict[str, Any]) -> str:
    """Format delete result as Markdown."""
    msg_id = result.get("message_id")
    success = result.get("success", False)
    status = result.get("status", "unknown")

    if success:
        return f"""✅ Message Deleted Successfully

**Message ID**: {msg_id}
**Status**: {status}
"""
    else:
        return f"""❌ Failed to Delete Message

**Message ID**: {msg_id}
**Status**: {status}
"""


def _format_search_markdown(result: dict[str, Any]) -> str:
    """Format search results as Markdown."""
    messages = result.get("messages", [])
    count = result.get("count", 0)
    total = result.get("total", 0)
    query = result.get("query", "")
    channel_id = result.get("channel_id", "")
    has_more = result.get("has_more", False)

    query_text = f" matching '{query}'" if query else ""

    if count == 0:
        return f"""🔍 Search Results

**Channel**: {channel_id}
**Query**: {query or "All messages"}
**Found**: No messages found{query_text}
"""

    messages_list = []
    for msg in messages:
        msg_id = msg.get("message_id", "?")
        text = msg.get("text", msg.get("caption", ""))
        date = msg.get("date", "")
        preview = text[:100] + "..." if len(text) > 100 else text
        messages_list.append(f"- **Message {msg_id}** ({date}):\n  > {preview}")

    messages_text = "\n\n".join(messages_list)
    more_text = f"\n\n*({total - count} more messages available)*" if has_more else ""

    return f"""🔍 Search Results

**Channel**: {channel_id}
**Query**: {query or "All messages"}
**Found**: {count} of {total} messages{query_text}

{messages_text}{more_text}
"""


def _format_channel_info_markdown(result: dict[str, Any]) -> str:
    """Format channel info as Markdown."""
    title = result.get("title", "Unknown")
    username = result.get("username", "")
    chat_id = result.get("id", "")
    chat_type = result.get("type", "")
    description = result.get("description", "")
    invite_link = result.get("invite_link", "")
    member_count = result.get("member_count", 0)

    username_text = f"\n**Username**: @{username}" if username else ""
    desc_text = f"\n**Description**: {description}" if description else ""
    link_text = f"\n**Invite Link**: {invite_link}" if invite_link else ""

    return f"""📢 Channel Information

**Title**: {title}{username_text}
**Chat ID**: {chat_id}
**Type**: {chat_type}
**Members**: {member_count}{desc_text}{link_text}
"""


# Create FastMCP server instance
mcp = FastMCP("telegram-bot-mcp")


@mcp.prompt()
def telegram_bot_instructions() -> str:
    """Comprehensive instructions for using the Telegram Bot MCP server.

    This prompt provides AI assistants with detailed guidance on how to effectively
    use the Telegram Bot MCP server tools to interact with Telegram channels.
    """
    return """# Telegram Bot MCP Server Instructions

This MCP server enables AI assistants to publish, edit, search, and manage messages in Telegram channels.

## Quick Reference

| Task | Message Type | Tool to Use |
|------|-------------|-------------|
| Publish a text message | Text | `telegram_publish_message` |
| Publish a photo | Photo | `telegram_publish_photo` |
| Publish multiple photos (album) | Photo Album | `telegram_publish_photo_album` |
| Edit a text-only message | Text | `telegram_edit_message` |
| Edit a photo's caption | Photo | `telegram_edit_message_caption` |
| Delete any message | Any | `telegram_delete_message` |
| Search cached messages | Any | `telegram_search_messages` |
| Get channel info | - | `telegram_get_channel_info` |

## Critical Rules

### Message Type and Editing
**IMPORTANT:** You CANNOT use `edit_message` on photo messages or `edit_message_caption` on text messages!

- **Text messages**: Use `edit_message` (will fail on photo messages)
- **Photo messages**: Use `edit_message_caption` (will fail on text-only messages)
- You cannot change a text message to a photo or vice versa
- The bot can only edit messages it sent itself

### Channel ID Format
- **Public channels**: Use `@channelname` format (e.g., `@mynews`)
- **Private channels**: Use numeric chat ID (e.g., `-1001234567890`)
- To get the chat ID:
  1. Add the bot to the channel
  2. Send a test message
  3. Check: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

### Bot Permissions Required
The bot must be a channel administrator with these permissions:
- Post messages
- Edit messages of others
- Delete messages of others

## Tool Usage Patterns

### Publishing Messages
```
Use telegram_publish_message for:
- Announcements and updates
- Formatted text with Markdown or HTML
- Messages with links (can disable preview)

Use telegram_publish_photo for:
- Single images with captions
- Visual content announcements
- Photos from local files, URLs, or Telegram file_id

Use telegram_publish_photo_album for:
- Multiple photos (2-10) in a single message
- Photo galleries and collections
- Each photo can have its own caption
- Users can swipe through the album
- Photos from local files, URLs, or Telegram file_ids
```

### Editing Messages
```
Before editing, determine message type:
- If it's text only → use telegram_edit_message
- If it has a photo → use telegram_edit_message_caption

Common error: "Message can't be edited"
Reasons:
1. Wrong tool for message type (most common)
2. Bot didn't send the original message
3. Message is older than 48 hours
```

### Search Limitations
**CRITICAL LIMITATION:** The `telegram_search_messages` tool only searches messages cached in the current session.

- ❌ Cannot search historical messages from before server started
- ❌ Cache is cleared when server restarts
- ❌ Cannot fetch arbitrary messages by ID
- ✅ Can still edit/delete messages from previous sessions if you know the message_id
- ✅ All messages published/edited in current session are automatically cached

## Error Handling

### Common Errors and Solutions

1. **"Chat not found"**
   - Verify bot is added to channel as admin
   - Check channel ID format (@username or numeric ID)

2. **"Not enough rights to send messages"**
   - Bot needs admin permissions with "Post messages" enabled

3. **"Message can't be edited"**
   - Check if you're using the correct edit tool for the message type
   - Verify bot sent the original message
   - Check if message is within 48-hour edit window

4. **"Message is not modified"**
   - New content is identical to current content

## Rate Limits

Telegram enforces rate limits on bot API calls. If publishing many messages:
- Add delays between messages
- Monitor for rate limit errors
- Consider using `disable_notification: true` for bulk updates

## Best Practices

1. **Always verify channel permissions** before attempting operations
2. **Store message_id values** from publish operations for later editing/deletion
3. **Use appropriate parse_mode** (Markdown/HTML) for formatted content
4. **Check message type** before choosing edit tool
5. **Handle errors gracefully** - API errors include helpful hints
6. **Use get_channel_info** to verify bot access before operations

## Example Workflows

### Publishing an Announcement
1. Use `telegram_get_channel_info` to verify access
2. Use `telegram_publish_message` with formatted text
3. Store returned `message_id` for potential edits
4. If editing needed, use `telegram_edit_message` with stored `message_id`

### Publishing Photo Update
1. Use `telegram_publish_photo` with image path/URL
2. Store returned `message_id`
3. If caption needs updating, use `telegram_edit_message_caption`

### Publishing Photo Album
1. Prepare list of 2-10 photos with optional captions
2. Use `telegram_publish_photo_album` with the photos list
3. Store returned `first_message_id` and `album_id`
4. All photos are posted as a single swipeable album
5. Each photo's caption can be edited separately using `telegram_edit_message_caption` with its message_id

### Managing Content
1. Use `telegram_search_messages` to find recent messages (current session only)
2. Use `telegram_delete_message` with message_id to remove outdated content
3. Use appropriate edit tool to update existing messages
"""


@mcp.resource("server://info")
def get_server_info() -> str:
    """Get server version and capability information.

    This resource provides metadata about the Telegram Bot MCP server,
    including version, capabilities, and configuration details.
    """
    return f"""# Telegram Bot MCP Server Information

**Server Name:** telegram-bot-mcp
**Version:** {version("telegram-bot-mcp")}
**Protocol:** Model Context Protocol (MCP)
**Framework:** FastMCP

## Capabilities

### Supported Operations
- ✅ Publish text messages to channels
- ✅ Publish photos with captions to channels
- ✅ Publish photo albums (2-10 photos in one message)
- ✅ Edit text messages
- ✅ Edit photo captions
- ✅ Delete messages
- ✅ Search messages (session cache only)
- ✅ Get channel information

### Message Formats
- Markdown formatting
- HTML formatting
- Plain text

### Supported Content Types
- Text messages
- Photo messages with captions
- Links with optional preview control

## Requirements

### Bot Permissions
The Telegram bot must be a channel administrator with:
- Post messages
- Edit messages of others
- Delete messages of others

### Environment Configuration
- `TELEGRAM_BOT_TOKEN`: Required Telegram bot API token

## Technical Details

### Limitations
- Message search only works for messages in current session cache
- Cannot retrieve historical messages through Bot API
- Cannot change message type (text to photo or vice versa)
- Bot can only edit its own messages

### API Rate Limits
Subject to Telegram Bot API rate limits. Consider delays for bulk operations.

## Support
For issues and feature requests, visit the project repository.
"""


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    )
)
async def telegram_publish_message(
    channel_id: str,
    text: str,
    parse_mode: str = "Markdown",
    disable_web_page_preview: bool = False,
    disable_notification: bool = False,
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Publish a message to a Telegram channel.

    Use this tool to post new messages to a Telegram channel where the bot is an admin.
    The bot must have permission to post messages in the channel.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID (e.g., '-1001234567890').
            Use '@' prefix for public channels with username.
        text: The message text to publish. Supports Markdown or HTML formatting based on parse_mode.
        parse_mode: Text formatting mode. Options: 'Markdown', 'HTML', or 'None' for plain text.
            Default is 'Markdown'.
        disable_web_page_preview: If True, disables link preview for URLs in the message.
            Default is False.
        disable_notification: If True, sends the message silently (no notification to users).
            Default is False.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing message_id, chat_id, date, text, and link.
        If response_format='markdown', returns formatted text content.
    """
    try:
        client = _get_client()
        result = await client.publish_message(
            channel_id=channel_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
        )

        # Format response based on response_format
        if response_format.lower() == "json":
            return result
        else:  # markdown
            return {"content": _format_message_markdown(result), "data": result}

    except TelegramError as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": f"Failed to publish message to channel {channel_id}",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Publishing Message**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while publishing message",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    )
)
async def telegram_publish_photo(
    channel_id: str,
    photo: str,
    caption: Optional[str] = None,
    parse_mode: str = "Markdown",
    disable_notification: bool = False,
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Publish a photo to a Telegram channel with an optional caption.

    Use this tool to post photos to a Telegram channel where the bot is an admin.
    The photo can include a text caption with formatting. The bot must have
    permission to post messages in the channel.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID.
        photo: Photo to send. Can be:
            - File path to a local image file (e.g., '/path/to/image.jpg')
            - URL to a remote image (e.g., 'https://example.com/image.png')
            - Telegram file_id of a photo that exists on Telegram servers
        caption: Optional text caption for the photo. Supports Markdown or HTML
            formatting based on parse_mode. Maximum 1024 characters.
        parse_mode: Caption formatting mode. Options: 'Markdown', 'HTML', or 'None' for plain text.
            Default is 'Markdown'.
        disable_notification: If True, sends the photo silently (no notification to users).
            Default is False.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing message_id, chat_id, date, caption, photo info, and link.
        If response_format='markdown', returns formatted text content.
    """
    try:
        client = _get_client()
        result = await client.publish_photo(
            channel_id=channel_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
        )

        if response_format.lower() == "json":
            return result
        else:
            return {"content": _format_photo_markdown(result), "data": result}

    except TelegramError as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": f"Failed to publish photo to channel {channel_id}",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Publishing Photo**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while publishing photo",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    )
)
async def telegram_publish_photo_album(
    channel_id: str,
    photos: list[dict[str, Any]],
    disable_notification: bool = False,
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Publish multiple photos as an album (media group) to a Telegram channel.

    Use this tool to post 2-10 photos in a single message as an album/gallery.
    Users can swipe through the photos. Each photo can have its own caption.
    The bot must have permission to post messages in the channel.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID.
        photos: List of photo objects (2-10 items). Each photo object must contain:
            - photo (required): Photo to send. Can be:
                - File path to a local image file (e.g., '/path/to/image.jpg')
                - URL to a remote image (e.g., 'https://example.com/image.png')
                - Telegram file_id of a photo that exists on Telegram servers
            - caption (optional): Text caption for this specific photo. Maximum 1024 characters.
            - parse_mode (optional): Caption formatting mode ('Markdown', 'HTML', or 'None').
                Default is 'Markdown' if not specified.
        disable_notification: If True, sends the album silently (no notification to users).
            Default is False.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing:
        - album_id: Unique identifier for the media group
        - message_count: Number of photos in the album
        - messages: List of message details for each photo (message_id, caption, photo info, link)
        - first_message_id: ID of the first message in the album
        - chat_id: Channel chat ID
        If response_format='markdown', returns formatted text content.

    Example:
        photos = [
            {
                "photo": "https://example.com/photo1.jpg",
                "caption": "First photo caption",
                "parse_mode": "Markdown"
            },
            {
                "photo": "/path/to/photo2.jpg",
                "caption": "Second photo caption"
            },
            {
                "photo": "AgACAgIAAxkBAAIC...",  # Telegram file_id
                "caption": "Third photo"
            }
        ]
    """
    try:
        client = _get_client()
        result = await client.publish_photo_album(
            channel_id=channel_id,
            photos=photos,
            disable_notification=disable_notification,
        )

        if response_format.lower() == "json":
            return result
        else:
            return {"content": _format_album_markdown(result), "data": result}

    except ValueError as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": f"Invalid photo album parameters: {str(e)}",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Invalid Parameters**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
    except TelegramError as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": f"Failed to publish photo album to channel {channel_id}",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Publishing Album**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while publishing photo album",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    )
)
async def telegram_edit_message(
    channel_id: str,
    message_id: int,
    new_text: str,
    parse_mode: str = "Markdown",
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Edit an existing TEXT message in a Telegram channel.

    Use this tool to modify the content of a previously published TEXT message.
    IMPORTANT: This only works for text messages. If the message contains a photo,
    use edit_message_caption instead.

    The bot must be the original sender of the message and have edit permissions.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID.
            Must be the same channel where the original message was sent.
        message_id: The unique identifier of the message to edit.
            This is returned when you publish a message.
        new_text: The new text to replace the existing message content.
            Supports formatting based on parse_mode.
        parse_mode: Text formatting mode. Options: 'Markdown', 'HTML', or 'None'.
            Default is 'Markdown'.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing message_id, chat_id, date, edit_date, text, and link.
        If response_format='markdown', returns formatted text content.
    """
    try:
        client = _get_client()
        result = await client.edit_message(
            channel_id=channel_id,
            message_id=message_id,
            new_text=new_text,
            parse_mode=parse_mode,
        )

        if response_format.lower() == "json":
            return result
        else:
            return {"content": _format_edit_markdown(result, "text"), "data": result}

    except TelegramError as e:
        error_msg = str(e)
        hint = ""

        # Provide helpful hints based on common errors
        if (
            "message can't be edited" in error_msg.lower()
            or "message to edit not found" in error_msg.lower()
        ):
            hint = " NOTE: If this is a photo message, use telegram_edit_message_caption instead. Also, the bot can only edit messages it sent itself."
        elif "message is not modified" in error_msg.lower():
            hint = " The new text is identical to the current text."

        error_result = {
            "error": error_msg,
            "status": "failed",
            "message": f"Failed to edit message {message_id} in channel {channel_id}.{hint}",
            "telegram_error": error_msg,
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Editing Message**\n\n{error_result['message']}\n\n**Details**: {error_msg}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while editing message",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    )
)
async def telegram_edit_message_caption(
    channel_id: str,
    message_id: int,
    new_caption: str,
    parse_mode: str = "Markdown",
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Edit the caption of an existing photo message in a Telegram channel.

    Use this tool to modify the caption text of a previously published photo message.
    This only works for messages that contain media (photos, videos, etc.).
    You cannot change the photo itself, only the caption text.
    The bot must be the original sender of the message and have edit permissions.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID.
            Must be the same channel where the original message was sent.
        message_id: The unique identifier of the photo message to edit.
            This is returned when you publish a photo.
        new_caption: The new caption text to replace the existing caption.
            Supports formatting based on parse_mode. Maximum 1024 characters.
        parse_mode: Caption formatting mode. Options: 'Markdown', 'HTML', or 'None'.
            Default is 'Markdown'.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing message_id, chat_id, date, edit_date, caption, photo info, and link.
        If response_format='markdown', returns formatted text content.
    """
    try:
        client = _get_client()
        result = await client.edit_message_caption(
            channel_id=channel_id,
            message_id=message_id,
            new_caption=new_caption,
            parse_mode=parse_mode,
        )

        if response_format.lower() == "json":
            return result
        else:
            return {"content": _format_edit_markdown(result, "caption"), "data": result}

    except TelegramError as e:
        error_msg = str(e)
        hint = ""

        # Provide helpful hints based on common errors
        if (
            "message can't be edited" in error_msg.lower()
            or "message to edit not found" in error_msg.lower()
        ):
            hint = " NOTE: If this is a text-only message (no photo), use telegram_edit_message instead. Also, the bot can only edit messages it sent itself."
        elif "message is not modified" in error_msg.lower():
            hint = " The new caption is identical to the current caption."
        elif "message has no caption" in error_msg.lower():
            hint = " This message doesn't have a caption to edit."

        error_result = {
            "error": error_msg,
            "status": "failed",
            "message": f"Failed to edit caption of message {message_id} in channel {channel_id}.{hint}",
            "telegram_error": error_msg,
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Editing Caption**\n\n{error_result['message']}\n\n**Details**: {error_msg}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while editing message caption",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    )
)
async def telegram_delete_message(
    channel_id: str,
    message_id: int,
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Delete a message from a Telegram channel.

    Use this tool to permanently remove a message from a channel.
    The bot must have delete message permissions in the channel.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID.
        message_id: The unique identifier of the message to delete.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing success status, message_id, and operation status.
        If response_format='markdown', returns formatted text content.
    """
    try:
        client = _get_client()
        success = await client.delete_message(
            channel_id=channel_id,
            message_id=message_id,
        )
        result = {
            "success": success,
            "message_id": message_id,
            "status": "deleted" if success else "failed",
        }

        if response_format.lower() == "json":
            return result
        else:
            return {"content": _format_delete_markdown(result), "data": result}

    except TelegramError as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": f"Failed to delete message {message_id} from channel {channel_id}",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Deleting Message**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while deleting message",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    )
)
def telegram_search_messages(
    channel_id: str,
    query: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    response_format: str = "markdown",
) -> dict[str, Any]:
    """Search for messages in a Telegram channel (from local cache ONLY).

    ⚠️ CRITICAL LIMITATIONS - READ CAREFULLY:

    1. **Session-Only Cache**: This tool ONLY searches messages cached in the CURRENT SERVER SESSION.
       - Messages published/edited BEFORE the server started are NOT available
       - Cache is CLEARED when the server restarts
       - This is a Telegram Bot API limitation, not a bug

    2. **Cannot Retrieve Historical Messages**: The Telegram Bot API does not provide
       methods to fetch arbitrary messages or search message history.

    3. **What IS Cached**:
       ✅ Messages published via publish_message in current session
       ✅ Messages edited via edit_message in current session
       ✅ Photos published via publish_photo in current session
       ✅ Photo captions edited via edit_message_caption in current session

    4. **What is NOT Cached**:
       ❌ Messages sent before server started
       ❌ Messages sent by other bots or users
       ❌ Messages sent when server was offline

    5. **You CAN Still**:
       ✅ Edit messages from previous sessions if you have the message_id
       ✅ Delete messages from previous sessions if you have the message_id
       ✅ The message_id is returned when publishing messages - store it if needed later!

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID to search in.
        query: Search query string. Performs case-insensitive search in message text/caption.
            If None or empty, returns all cached messages for the channel.
        limit: Maximum number of results to return. Default is 10.
            Results are sorted by date (newest first).
        offset: Number of results to skip. Use for pagination. Default is 0.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing:
        - messages: List of matching messages (may be empty if nothing cached)
        - count: Number of messages returned in this page
        - total: Total number of matching messages in cache
        - offset: Current offset value
        - limit: Current limit value
        - has_more: Boolean indicating if more results are available
        - next_offset: Offset value for the next page (if has_more is True)
        - query: The search query used
        - channel_id: The channel searched
        - status: Operation status
        If response_format='markdown', returns formatted text content.

    Note: If you need to work with older messages, you must keep track of message_id
    values returned when publishing. There is no way to retrieve message_id for
    historical messages through the Telegram Bot API.
    """
    try:
        logger.info(
            f"Searching messages in channel {channel_id} with query: {query}, limit: {limit}, offset: {offset}"
        )
        client = _get_client()
        result = client.search_messages(
            channel_id=channel_id,
            query=query,
            limit=limit,
            offset=offset,
        )
        logger.info(
            f"Found {result.get('count', 0)} of {result.get('total', 0)} messages matching query in cache"
        )

        if response_format.lower() == "json":
            return {**result, "status": "success"}
        else:
            return {"content": _format_search_markdown(result), "data": result}

    except Exception as e:
        logger.error(f"Error searching messages: {e}", exc_info=True)
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while searching messages",
            "messages": [],
            "count": 0,
            "total": 0,
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Searching Messages**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    )
)
async def telegram_get_channel_info(
    channel_id: str, response_format: str = "markdown"
) -> dict[str, Any]:
    """Get detailed information about a Telegram channel.

    Use this tool to retrieve metadata and statistics about a channel
    where the bot is a member or admin.

    Args:
        channel_id: Channel username (e.g., '@mychannel') or numeric chat ID.
        response_format: Response format. Options: 'json' for structured data, 'markdown' for
            human-readable text. Default is 'markdown'.

    Returns:
        A dictionary containing id, title, username, type, description, invite_link, and member_count.
        If response_format='markdown', returns formatted text content.
    """
    try:
        client = _get_client()
        info = await client.get_channel_info(channel_id=channel_id)
        result = {
            **info,
            "status": "success",
        }

        if response_format.lower() == "json":
            return result
        else:
            return {"content": _format_channel_info_markdown(result), "data": result}

    except TelegramError as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": f"Failed to get info for channel {channel_id}",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Error Getting Channel Info**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed",
            "message": "Unexpected error occurred while getting channel info",
        }
        if response_format.lower() == "json":
            return error_result
        else:
            return {
                "content": f"❌ **Unexpected Error**\n\n{error_result['message']}\n\n**Details**: {str(e)}",
                "data": error_result,
            }
