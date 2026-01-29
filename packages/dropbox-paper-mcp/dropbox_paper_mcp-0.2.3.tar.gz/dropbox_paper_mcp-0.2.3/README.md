# Dropbox Paper MCP Server

MCP server for Dropbox Paper built with [FastMCP](https://gofastmcp.com).

## Features

| Tool | Description |
|------|-------------|
| `paper_search` | Search Paper documents |
| `paper_get_content` | Get Paper content (Markdown format) with optional character limit |
| `paper_get_metadata` | Get Paper metadata |
| `paper_create` | Create new Paper from Markdown |
| `paper_list` | List all Paper documents |
| `list_folder` | List files and folders in a directory |
| `oauth_get_auth_url` | Start OAuth flow (get authorization URL) |
| `oauth_exchange_code` | Exchange auth code for refresh token |

## Configuration

### Option 1: Refresh Token (Recommended)

Refresh tokens don't expire and the SDK auto-refreshes access tokens.

1. Get your app credentials from [Dropbox Developers](https://www.dropbox.com/developers/apps)

2. Use the OAuth tools to get a refresh token:
   - Call `oauth_get_auth_url` with your app key
   - Open the URL in browser and authorize
   - Call `oauth_exchange_code` with the authorization code

3. Create a `.env` file:
```bash
DROPBOX_REFRESH_TOKEN=your_refresh_token
DROPBOX_APP_KEY=your_app_key
DROPBOX_APP_SECRET=your_app_secret
# Optional: Set default character limit for paper_get_content (default: 10000)
PAPER_CONTENT_DEFAULT_LIMIT=10000
```

### Option 2: Access Token (Legacy)

Short-lived tokens expire in ~4 hours.

```bash
DROPBOX_ACCESS_TOKEN=your_access_token
# Optional: Set default character limit for paper_get_content (default: 10000)
PAPER_CONTENT_DEFAULT_LIMIT=10000
```

## Installation

```bash
uv sync
```

## Running

### Using uvx (after publishing)
```bash
uvx dropbox-paper-mcp
```

### Local development
```bash
uv run dropbox-paper-mcp
```

## MCP Client Configuration

Add to Claude Desktop or other MCP clients:

```json
{
  "mcpServers": {
    "dropbox-paper": {
      "command": "uvx",
      "args": ["dropbox-paper-mcp"],
      "env": {
        "DROPBOX_REFRESH_TOKEN": "your_refresh_token",
        "DROPBOX_APP_KEY": "your_app_key",
        "DROPBOX_APP_SECRET": "your_app_secret",
        "PAPER_CONTENT_DEFAULT_LIMIT": "10000"
      }
    }
  }
}
```

## API Permissions Required

- `files.metadata.read` - Search and metadata
- `files.content.read` - Get document content
- `files.content.write` - Create new documents (optional)
- `sharing.read` - Resolve shared links (required for using shared links as input)
