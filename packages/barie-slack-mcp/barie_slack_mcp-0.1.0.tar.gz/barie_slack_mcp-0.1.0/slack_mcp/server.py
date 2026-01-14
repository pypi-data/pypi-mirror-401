"""Slack MCP Server implementation."""

import argparse
import asyncio
import json
import logging
from typing import Optional

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from slack_mcp.client import SlackClient
from slack_mcp.blockkit import BlockKitBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(api_token: str, workspace_id: Optional[str] = None, file_storage_path: str = None):
    """
    Main entry point for Slack MCP server.

    Args:
        api_token: Slack API token (xoxb-...)
        workspace_id: Optional workspace ID
    """
    global slack_client
    logger.warning("Initializing Slack MCP Server...")
    slack_client = SlackClient(api_token=api_token, workspace_id=workspace_id, file_storage_path=file_storage_path)
    logger.warning("Slack client initialized successfully")
    server = Server("slack")
    logger.warning("MCP Server created")

    def get_all_tools() -> list[types.Tool]:
        """Returns all available tools."""
        return [
            types.Tool(
                name="list_channels",
                description=(
                    "List all channels in the Slack workspace that you have access to. "
                    "If you want to get the list of channels you have access to, use all types of channels: "
                    "'public_channel', 'private_channel', 'mpim', and 'im'."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "types": {
                            "type": "string",
                            "description": (
                                "Comma-separated channel types. Options are: "
                                "'public_channel', 'private_channel', 'mpim', 'im'. "
                                "To get all accessible channels, use all these types."
                            ),
                        },
                        "exclude_archived": {
                            "type": "boolean",
                            "description": "Whether to exclude archived channels (default: true)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of channels to return (1-1000, default: 100)",
                        },
                    },
                    "required": [],
                },
            ),
            types.Tool(
                name="get_channel_info",
                description="Get detailed information about a specific Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel_id": {
                            "type": "string",
                            "description": "The ID of the channel",
                        },
                    },
                    "required": ["channel_id"],
                },
            ),
            types.Tool(
                name="list_users",
                description="List all users in the Slack workspace.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of users to return (default: 100)",
                        },
                        "include_locale": {
                            "type": "boolean",
                            "description": "Include locale information for each user (default: false)",
                        },
                    },
                    "required": [],
                },
            ),
            types.Tool(
                name="get_user_info",
                description="Get detailed information about a specific Slack user.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user",
                        },
                    },
                    "required": ["user_id"],
                },
            ),
            types.Tool(
                name="send_message",
                description="Send a message to a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID or name",
                        },
                        "text": {
                            "type": "string",
                            "description": "Message text (fallback text for notifications)",
                        },
                        "thread_ts": {
                            "type": "string",
                            "description": "Thread timestamp for replies",
                        },
                        "blocks": {
                            "type": "string",
                            "description": "JSON string of Block Kit blocks for rich formatting",
                        },
                    },
                    "required": ["channel", "text"],
                },
            ),
            types.Tool(
                name="update_message",
                description="Update an existing Slack message.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID where the message exists",
                        },
                        "ts": {
                            "type": "string",
                            "description": "Timestamp of the message to update",
                        },
                        "text": {
                            "type": "string",
                            "description": "New message text (fallback text for notifications)",
                        },
                        "blocks": {
                            "type": "string",
                            "description": "JSON string of Block Kit blocks for rich formatting",
                        },
                    },
                    "required": ["channel", "ts", "text"],
                },
            ),
            types.Tool(
                name="delete_message",
                description="Delete a message from a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID where the message exists",
                        },
                        "ts": {
                            "type": "string",
                            "description": "Timestamp of the message to delete",
                        },
                    },
                    "required": ["channel", "ts"],
                },
            ),
            types.Tool(
                name="get_channel_history",
                description="Get message history for a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of messages to return (default: 100)",
                        },
                        "oldest": {
                            "type": "string",
                            "description": "Only messages after this timestamp",
                        },
                        "latest": {
                            "type": "string",
                            "description": "Only messages before this timestamp",
                        },
                    },
                    "required": ["channel"],
                },
            ),
            types.Tool(
                name="search_messages",
                description="Search for messages across the Slack workspace.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query",
                        },
                        "sort": {
                            "type": "string",
                            "description": "Sort by 'score' or 'timestamp' (default: timestamp)",
                        },
                        "sort_dir": {
                            "type": "string",
                            "description": "Sort direction 'asc' or 'desc' (default: desc)",
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of results to return (default: 20)",
                        },
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="upload_file",
                description="Upload a file to one or more Slack channels using Slack's modern file upload API. The file is read from the file storage path. Supports both text and binary files. Requires files:write scope.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channels": {
                            "type": "string",
                            "description": "Comma-separated list of channel IDs where the file will be shared",
                        },
                        "file_name": {
                            "type": "string",
                            "description": "Name of the file to upload",
                        },
                        "title": {
                            "type": "string",
                            "description": "Optional title for the file (displayed in Slack). If not provided, the filename will be used.",
                        },
                        "initial_comment": {
                            "type": "string",
                            "description": "message text introducing the file in the channel or any other comment about the file specified by the user.",
                        },
                    },
                    "required": ["channels", "file_name"],
                },
            ),
            types.Tool(
                name="get_team_info",
                description="Get information about the Slack workspace/team.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            types.Tool(
                name="create_channel",
                description="Create a new Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name for the new channel",
                        },
                        "is_private": {
                            "type": "boolean",
                            "description": "Whether the channel should be private (default: false)",
                        },
                    },
                    "required": ["name"],
                },
            ),
            types.Tool(
                name="archive_channel",
                description="Archive a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID to archive",
                        },
                    },
                    "required": ["channel"],
                },
            ),
            types.Tool(
                name="unarchive_channel",
                description="Unarchive a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID to unarchive",
                        },
                    },
                    "required": ["channel"],
                },
            ),
            types.Tool(
                name="invite_to_channel",
                description="Invite users to a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID",
                        },
                        "users": {
                            "type": "string",
                            "description": "Comma-separated list of user IDs",
                        },
                    },
                    "required": ["channel", "users"],
                },
            ),
            types.Tool(
                name="set_channel_topic",
                description="Set the topic for a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID",
                        },
                        "topic": {
                            "type": "string",
                            "description": "New topic text",
                        },
                    },
                    "required": ["channel", "topic"],
                },
            ),
            types.Tool(
                name="set_channel_purpose",
                description="Set the purpose for a Slack channel.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID",
                        },
                        "purpose": {
                            "type": "string",
                            "description": "New purpose text",
                        },
                    },
                    "required": ["channel", "purpose"],
                },
            ),
            types.Tool(
                name="send_formatted_message",
                description="Send a formatted message using Block Kit with common elements.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID or name",
                        },
                        "title": {
                            "type": "string",
                            "description": "Header text (optional)",
                        },
                        "text": {
                            "type": "string",
                            "description": "Main message text (optional)",
                        },
                        "fields": {
                            "type": "string",
                            "description": "Comma-separated fields for side-by-side display (optional)",
                        },
                        "context": {
                            "type": "string",
                            "description": "Context text at bottom (optional)",
                        },
                        "thread_ts": {
                            "type": "string",
                            "description": "Thread timestamp for replies (optional)",
                        },
                    },
                    "required": ["channel"],
                },
            ),
            types.Tool(
                name="send_notification_message",
                description="Send a structured notification message with status indicator.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID or name",
                        },
                        "status": {
                            "type": "string",
                            "description": "Status type (success, warning, error, info)",
                        },
                        "title": {
                            "type": "string",
                            "description": "Notification title",
                        },
                        "description": {
                            "type": "string",
                            "description": "Main description",
                        },
                        "details": {
                            "type": "string",
                            "description": "Additional details (optional)",
                        },
                        "thread_ts": {
                            "type": "string",
                            "description": "Thread timestamp for replies (optional)",
                        },
                    },
                    "required": ["channel", "status", "title", "description"],
                },
            ),
            types.Tool(
                name="send_list_message",
                description="Send a formatted list message.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID or name",
                        },
                        "title": {
                            "type": "string",
                            "description": "List title",
                        },
                        "items": {
                            "type": "string",
                            "description": "Newline or comma-separated list items",
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional description text",
                        },
                        "thread_ts": {
                            "type": "string",
                            "description": "Thread timestamp for replies (optional)",
                        },
                    },
                    "required": ["channel", "title", "items"],
                },
            ),
        ]

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """Returns list of available tools."""
        logger.warning("List tools requested")
        tools = get_all_tools()
        logger.warning(f"Returning {len(tools)} tools")
        return tools

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        
        logger.warning(f"Tool called: {name} with arguments: {arguments}")
        
        if slack_client is None:
            raise RuntimeError("Slack client not initialized")
        
        if arguments is None:
            arguments = {}
        
        try:
            if name == "list_channels":
                types_str = arguments.get("types")
                types_list = types_str.split(",") if types_str else None
                exclude_archived = arguments.get("exclude_archived", True)
                limit = arguments.get("limit", 100)
                result = await slack_client.list_channels(types_list, exclude_archived, limit)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "get_channel_info":
                channel_id = arguments.get("channel_id")
                if not channel_id:
                    raise ValueError("Missing required parameter: channel_id")
                result = await slack_client.get_channel_info(channel_id)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "list_users":
                limit = arguments.get("limit", 100)
                include_locale = arguments.get("include_locale", False)
                result = await slack_client.list_users(limit, include_locale)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "get_user_info":
                user_id = arguments.get("user_id")
                if not user_id:
                    raise ValueError("Missing required parameter: user_id")
                result = await slack_client.get_user_info(user_id)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "send_message":
                channel = arguments.get("channel")
                text = arguments.get("text")
                if not channel or not text:
                    raise ValueError("Missing required parameters: channel, text")
                thread_ts = arguments.get("thread_ts")
                blocks_str = arguments.get("blocks")
                blocks = json.loads(blocks_str) if blocks_str else None
                result = await slack_client.send_message(channel, text, thread_ts, blocks)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "update_message":
                channel = arguments.get("channel")
                ts = arguments.get("ts")
                text = arguments.get("text")
                if not channel or not ts or not text:
                    raise ValueError("Missing required parameters: channel, ts, text")
                blocks_str = arguments.get("blocks")
                blocks = json.loads(blocks_str) if blocks_str else None
                result = await slack_client.update_message(channel, ts, text, blocks)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "delete_message":
                channel = arguments.get("channel")
                ts = arguments.get("ts")
                if not channel or not ts:
                    raise ValueError("Missing required parameters: channel, ts")
                result = await slack_client.delete_message(channel, ts)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "get_channel_history":
                channel = arguments.get("channel")
                if not channel:
                    raise ValueError("Missing required parameter: channel")
                limit = arguments.get("limit", 100)
                oldest = arguments.get("oldest")
                latest = arguments.get("latest")
                result = await slack_client.get_channel_history(channel, limit, oldest, latest)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "search_messages":
                query = arguments.get("query")
                if not query:
                    raise ValueError("Missing required parameter: query")
                sort = arguments.get("sort", "timestamp")
                sort_dir = arguments.get("sort_dir", "desc")
                count = arguments.get("count", 20)
                result = await slack_client.search_messages(query, sort, sort_dir, count)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "upload_file":
                channels = arguments.get("channels")
                file_name = arguments.get("file_name")
                if not channels or not file_name:
                    raise ValueError("Missing required parameters: channels, file_name")
                channels_list = channels.split(",")
                title = arguments.get("title")
                initial_comment = arguments.get("initial_comment")
                result = await slack_client.upload_file(channels_list, file_name, title, initial_comment)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "get_team_info":
                result = await slack_client.get_team_info()
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "create_channel":
                name = arguments.get("name")
                if not name:
                    raise ValueError("Missing required parameter: name")
                is_private = arguments.get("is_private", False)
                result = await slack_client.create_channel(name, is_private)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "archive_channel":
                channel = arguments.get("channel")
                if not channel:
                    raise ValueError("Missing required parameter: channel")
                result = await slack_client.archive_channel(channel)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "unarchive_channel":
                channel = arguments.get("channel")
                if not channel:
                    raise ValueError("Missing required parameter: channel")
                result = await slack_client.unarchive_channel(channel)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "invite_to_channel":
                channel = arguments.get("channel")
                users = arguments.get("users")
                if not channel or not users:
                    raise ValueError("Missing required parameters: channel, users")
                users_list = users.split(",")
                result = await slack_client.invite_to_channel(channel, users_list)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "set_channel_topic":
                channel = arguments.get("channel")
                topic = arguments.get("topic")
                if not channel or not topic:
                    raise ValueError("Missing required parameters: channel, topic")
                result = await slack_client.set_channel_topic(channel, topic)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "set_channel_purpose":
                channel = arguments.get("channel")
                purpose = arguments.get("purpose")
                if not channel or not purpose:
                    raise ValueError("Missing required parameters: channel, purpose")
                result = await slack_client.set_channel_purpose(channel, purpose)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "send_formatted_message":
                channel = arguments.get("channel")
                if not channel:
                    raise ValueError("Missing required parameter: channel")
                title = arguments.get("title")
                text = arguments.get("text")
                fields = arguments.get("fields")
                context = arguments.get("context")
                thread_ts = arguments.get("thread_ts")
                
                blocks = []
                if title:
                    blocks.append(BlockKitBuilder.header(title))
                if text:
                    blocks.append(BlockKitBuilder.section(text))
                if fields:
                    field_list = [field.strip() for field in fields.split(",")]
                    blocks.append(BlockKitBuilder.fields_section(field_list))
                if context:
                    blocks.append(BlockKitBuilder.context([context]))
                
                if not blocks:
                    raise ValueError("At least one of title, text, fields, or context must be provided")
                
                fallback_text = title or text or "Formatted message"
                result = await slack_client.send_message(channel, fallback_text, thread_ts, blocks)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "send_notification_message":
                channel = arguments.get("channel")
                status = arguments.get("status")
                title = arguments.get("title")
                description = arguments.get("description")
                if not channel or not status or not title or not description:
                    raise ValueError("Missing required parameters: channel, status, title, description")
                
                status_config = {
                    "success": {"emoji": "✅", "color": "#28a745"},
                    "warning": {"emoji": "⚠️", "color": "#ffc107"},
                    "error": {"emoji": "❌", "color": "#dc3545"},
                    "info": {"emoji": "ℹ️", "color": "#17a2b8"}
                }
                config = status_config.get(status.lower(), status_config["info"])
                
                blocks = [{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{config['emoji']} *{title}*\n{description}"
                    }
                }]
                
                details = arguments.get("details")
                if details:
                    blocks.append(BlockKitBuilder.divider())
                    blocks.append(BlockKitBuilder.context([details]))
                
                fallback_text = f"{config['emoji']} {title}: {description}"
                result = await slack_client.send_message(channel, fallback_text, arguments.get("thread_ts"), blocks)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "send_list_message":
                channel = arguments.get("channel")
                title = arguments.get("title")
                items = arguments.get("items")
                if not channel or not title or not items:
                    raise ValueError("Missing required parameters: channel, title, items")
                
                blocks = [BlockKitBuilder.header(title)]
                description = arguments.get("description")
                if description:
                    blocks.append(BlockKitBuilder.section(description))
                    blocks.append(BlockKitBuilder.divider())
                
                if "\n" in items:
                    item_list = [item.strip() for item in items.split("\n") if item.strip()]
                else:
                    item_list = [item.strip() for item in items.split(",") if item.strip()]
                
                formatted_items = "\n".join([f"• {item}" for item in item_list])
                blocks.append(BlockKitBuilder.section(formatted_items))
                
                fallback_text = f"{title}: {', '.join(item_list)}"
                result = await slack_client.send_message(channel, fallback_text, arguments.get("thread_ts"), blocks)
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                logger.error(f"Unknown tool: {name}")
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Error calling tool {name}: {str(e)}")
            raise

    logger.warning("Starting MCP server with stdio transport...")
    logger.warning(f"Server capabilities: {server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={})}")
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.warning("Stdio server started, running server...")
            logger.warning("Waiting for client initialization...")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="slack",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
            logger.warning("Server initialization completed")
    except Exception as e:
        logger.error(f"Fatal error in MCP server: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def cli_main():
    """CLI entry point for the Slack MCP server."""
    parser = argparse.ArgumentParser(description='Slack MCP Server')
    parser.add_argument('--api-token',
                        required=True,
                        help='Slack API token (xoxb-...)')
    parser.add_argument('--file-storage-path',
                        required=True,
                        help='File storage path for attachments')                
    parser.add_argument('--workspace-id',
                        required=False,
                        default=None,
                        help='Optional workspace ID')
    
    
    args = parser.parse_args()
    
    asyncio.run(main(
        api_token=args.api_token,
        workspace_id=args.workspace_id,
        file_storage_path=args.file_storage_path
    ))


def main():
    """Main entry point for the Slack MCP server (for use as a module)."""
    return cli_main()


if __name__ == "__main__":
    cli_main()
