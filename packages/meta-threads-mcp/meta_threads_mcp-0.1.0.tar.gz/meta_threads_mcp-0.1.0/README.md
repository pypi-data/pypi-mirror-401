# meta-threads-mcp

Unofficial MCP server for Meta's Threads API. Enables LLMs like Claude to publish posts, manage replies, and track insights through the Model Context Protocol.

[![PyPI version](https://badge.fury.io/py/meta-threads-mcp.svg)](https://badge.fury.io/py/meta-threads-mcp)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Full Threads API coverage via MCP tools
- Create text, image, and video posts
- Reply management (reply, hide/unhide, get conversation)
- Post and user insights/metrics
- Publishing quota tracking
- Built on [meta-threads-sdk](https://github.com/MetaThreads/meta-threads-sdk) and [FastMCP](https://github.com/jlowin/fastmcp)

## Installation

```bash
pip install meta-threads-mcp
```

Or with uv:

```bash
uv add meta-threads-mcp
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "threads": {
      "command": "meta-threads-mcp"
    }
  }
}
```

### Authentication

The server expects a bearer token in the format:

```
<access_token>:<user_id>
```

The client passes this token via the request context when calling tools.

## Available Tools

### Posts

| Tool | Description | Parameters |
|------|-------------|------------|
| `threads_create_post` | Create and publish a text post | `text` (required), `reply_control` (optional) |
| `threads_create_image_post` | Create post with image | `image_url` (required), `text` (optional) |
| `threads_create_video_post` | Create post with video | `video_url` (required), `text` (optional) |
| `threads_get_post` | Get a post by ID | `post_id` (required) |
| `threads_get_user_posts` | Get user's recent posts | `limit` (optional, default 10) |
| `threads_delete_post` | Delete a post | `post_id` (required) |
| `threads_get_publishing_limit` | Check remaining quota | none |

### Replies

| Tool | Description | Parameters |
|------|-------------|------------|
| `threads_reply_to_post` | Reply to a post | `post_id` (required), `text` (required) |
| `threads_get_replies` | Get replies to a post | `post_id` (required) |
| `threads_get_conversation` | Get full conversation thread | `post_id` (required) |
| `threads_hide_reply` | Hide a reply | `reply_id` (required) |
| `threads_unhide_reply` | Unhide a reply | `reply_id` (required) |

### Insights

| Tool | Description | Parameters |
|------|-------------|------------|
| `threads_get_media_insights` | Get metrics for a post | `media_id` (required) |
| `threads_get_user_insights` | Get user-level metrics | none |

### User

| Tool | Description | Parameters |
|------|-------------|------------|
| `threads_get_profile` | Get current user's profile | none |

## Reply Control Options

When creating posts, you can control who can reply:

- `EVERYONE` (default) - Anyone can reply
- `ACCOUNTS_YOU_FOLLOW` - Only accounts you follow can reply
- `MENTIONED_ONLY` - Only mentioned accounts can reply

## Rate Limits

- 250 posts per 24 hours
- 1000 replies per 24 hours

Use `threads_get_publishing_limit` to check your current quota.

## Development

### Setup

```bash
git clone https://github.com/MetaThreads/meta-threads-mcp.git
cd meta-threads-mcp
uv sync --dev
```

### Running Tests

```bash
uv run pytest
```

### Linting & Type Checking

```bash
uv run ruff check src tests
uv run ruff format src tests
uv run mypy src
```

### Testing with FastMCP CLI

```bash
fastmcp dev src/meta_threads_mcp/server.py
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- [meta-threads-sdk](https://github.com/MetaThreads/meta-threads-sdk) - Python SDK for Meta's Threads API
- [FastMCP](https://github.com/jlowin/fastmcp) - Simple MCP server framework
