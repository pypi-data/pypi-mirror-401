# MCP Configuration for Barie Slack MCP

## Claude Desktop Configuration

Add this to your Claude Desktop MCP configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "barie-slack-mcp": {
      "command": "uvx",
      "args": [
        "barie-slack-mcp",
        "--api-token",
        "xoxb-your-slack-token-here",
        "--file-storage-path",
        "/path/to/your/file/storage"
      ]
    }
  }
}
```

## Environment Variables (Alternative)

You can also use environment variables:

```json
{
  "mcpServers": {
    "barie-slack-mcp": {
      "command": "uvx",
      "args": [
        "barie-slack-mcp",
        "--api-token",
        "${SLACK_API_TOKEN}",
        "--file-storage-path",
        "${SLACK_FILE_STORAGE_PATH}"
      ],
      "env": {
        "SLACK_API_TOKEN": "xoxb-your-token-here",
        "SLACK_FILE_STORAGE_PATH": "/path/to/file/storage"
      }
    }
  }
}
```

## Optional Workspace ID

If you need to specify a workspace ID:

```json
{
  "mcpServers": {
    "barie-slack-mcp": {
      "command": "uvx",
      "args": [
        "barie-slack-mcp",
        "--api-token",
        "xoxb-your-slack-token-here",
        "--file-storage-path",
        "/path/to/your/file/storage",
        "--workspace-id",
        "T1234567890"
      ]
    }
  }
}
```

## Getting Your Slack API Token

1. Go to https://api.slack.com/apps
2. Create a new app or select an existing one
3. Go to "OAuth & Permissions"
4. Install the app to your workspace
5. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

## Required Slack Scopes

Your Slack app needs the following scopes:
- `channels:read` - List channels
- `channels:write` - Create/manage channels
- `chat:write` - Send messages
- `chat:write.public` - Send messages to public channels
- `files:write` - Upload files
- `users:read` - List users
- `search:read` - Search messages
- `team:read` - Get team info

## File Storage Path

The `--file-storage-path` should point to a directory where files to be uploaded are stored. Make sure this directory exists and is accessible.

Example:
- macOS/Linux: `/Users/username/slack-files` or `~/slack-files`
- Windows: `C:\Users\username\slack-files`
