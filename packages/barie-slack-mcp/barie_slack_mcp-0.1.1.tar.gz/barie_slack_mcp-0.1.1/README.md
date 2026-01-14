# Barie Slack MCP

A Model Context Protocol (MCP) server for interacting with Slack workspaces. This package provides a comprehensive set of tools for managing Slack channels, messages, users, and files.

## Installation

Install via `uvx`:

```bash
uvx barie-slack-mcp
```

Or install via pip:

```bash
pip install barie-slack-mcp
```

## Usage

Run the MCP server:

```bash
barie-slack-mcp --api-token <your-slack-token> --file-storage-path <path-to-files>
```

### Required Arguments

- `--api-token`: Your Slack API token (xoxb-...)
- `--file-storage-path`: Path to directory where files are stored for uploads

### Optional Arguments

- `--workspace-id`: Optional workspace ID

## Features

The server provides the following tools:

- **Channel Management**: List, create, archive, and manage channels
- **Message Operations**: Send, update, delete, and search messages
- **User Management**: List and get user information
- **File Uploads**: Upload files to channels
- **Block Kit Support**: Send rich formatted messages using Slack Block Kit
- **Team Information**: Get workspace/team details

## Requirements

- Python 3.9+
- Slack API token with appropriate scopes

## License

MIT
