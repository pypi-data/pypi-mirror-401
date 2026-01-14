"""Barie Slack MCP Server - A Model Context Protocol server for Slack."""

__version__ = "0.1.1"

from slack_mcp.client import SlackClient
from slack_mcp.blockkit import BlockKitBuilder
from slack_mcp.server import cli_main

__all__ = ["SlackClient", "BlockKitBuilder", "cli_main"]
