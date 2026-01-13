"""Telegram Bot MCP Server - Model Context Protocol server for Telegram Bot operations.

This package provides an MCP server that enables AI assistants to publish, edit,
search, and manage messages in Telegram channels.
"""

from telegram_bot_mcp.telegram_bot.client import TelegramBotClient
from telegram_bot_mcp.server import mcp

from importlib.metadata import version

__version__ = version("telegram-bot-mcp")

__all__ = [
    "TelegramBotClient",
    "mcp",
]
