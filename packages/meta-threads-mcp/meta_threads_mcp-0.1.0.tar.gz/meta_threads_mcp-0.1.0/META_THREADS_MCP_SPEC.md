# meta-threads-mcp Specification

Build an MCP (Model Context Protocol) server that exposes the Threads API via the `meta-threads-sdk` Python package.

## Overview

**Goal:** Create an MCP server that allows LLMs (like Claude) to interact with Meta's Threads API through tools.

**Package name:** `meta-threads-mcp`
**Dependencies:**
- `meta-threads-sdk` (the underlying SDK)
- `fastmcp` (FastMCP - simple MCP server framework)

## MCP Basics

MCP servers expose:
- **Tools**: Functions the LLM can call (e.g., `create_post`, `get_replies`)
- **Resources**: Data the LLM can read (optional)

Reference: https://github.com/jlowin/fastmcp

## Authentication

The MCP server accepts a bearer token passed by the client during connection. Token format:

```
<access_token>:<user_id>
```

The server parses the token from the request context:

```python
from fastmcp import Context

def parse_bearer_token(ctx: Context) -> tuple[str, str]:
    """Parse bearer token from request context."""
    token = ctx.request_context.get("bearer_token", "")
    if not token:
        raise ValueError("Missing bearer token")
    access_token, user_id = token.split(":", 1)
    return access_token, user_id
```

## Tools to Implement

### Posts

| Tool | Description | Parameters |
|------|-------------|------------|
| `threads_create_post` | Create and publish a text post | `text` (required), `reply_control` (optional: "EVERYONE", "ACCOUNTS_YOU_FOLLOW", "MENTIONED_ONLY") |
| `threads_create_image_post` | Create post with image | `text`, `image_url` (required) |
| `threads_create_video_post` | Create post with video | `text`, `video_url` (required) |
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

## Tool Response Format

All tools should return JSON-serializable results:

```python
# Success
{
    "success": True,
    "data": { ... }  # Post, insights, etc.
}

# Error
{
    "success": False,
    "error": "Error message here"
}
```

## Example Tool Implementation

```python
from fastmcp import FastMCP, Context
from threads import AsyncThreadsClient

mcp = FastMCP("meta-threads-mcp")


def parse_bearer_token(ctx: Context) -> tuple[str, str]:
    """Parse bearer token from request context."""
    token = ctx.request_context.get("bearer_token", "")
    if not token:
        raise ValueError("Missing bearer token")
    access_token, user_id = token.split(":", 1)
    return access_token, user_id


@mcp.tool()
async def threads_create_post(
    ctx: Context, text: str, reply_control: str = "EVERYONE"
) -> dict:
    """Create and publish a text post to Threads.

    Args:
        text: The text content of the post
        reply_control: Who can reply - EVERYONE, ACCOUNTS_YOU_FOLLOW, or MENTIONED_ONLY
    """
    try:
        access_token, user_id = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=access_token) as client:
            post = await client.posts.create_and_publish(
                user_id=user_id,
                text=text,
                reply_control=reply_control,
            )
            return {
                "success": True,
                "data": {
                    "id": post.id,
                    "permalink": post.permalink,
                    "text": post.text,
                }
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def threads_get_post(ctx: Context, post_id: str) -> dict:
    """Get a Threads post by ID.

    Args:
        post_id: The ID of the post to retrieve
    """
    try:
        access_token, _ = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=access_token) as client:
            post = await client.posts.get(post_id)
            return {
                "success": True,
                "data": {
                    "id": post.id,
                    "text": post.text,
                    "media_type": post.media_type,
                    "permalink": post.permalink,
                    "timestamp": post.timestamp.isoformat() if post.timestamp else None,
                }
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def threads_get_user_posts(ctx: Context, limit: int = 10) -> dict:
    """Get the authenticated user's recent posts.

    Args:
        limit: Maximum number of posts to return (default 10)
    """
    try:
        access_token, user_id = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=access_token) as client:
            posts = await client.posts.get_user_posts(user_id, limit=limit)
            return {
                "success": True,
                "data": {
                    "posts": [
                        {
                            "id": p.id,
                            "text": p.text,
                            "media_type": p.media_type,
                            "permalink": p.permalink,
                            "timestamp": p.timestamp.isoformat() if p.timestamp else None,
                        }
                        for p in posts
                    ]
                }
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def threads_reply_to_post(ctx: Context, post_id: str, text: str) -> dict:
    """Reply to an existing Threads post.

    Args:
        post_id: The ID of the post to reply to
        text: The text content of the reply
    """
    try:
        access_token, user_id = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=access_token) as client:
            reply = await client.posts.create_and_publish(
                user_id=user_id,
                text=text,
                reply_to_id=post_id,
            )
            return {
                "success": True,
                "data": {
                    "id": reply.id,
                    "permalink": reply.permalink,
                    "text": reply.text,
                }
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def threads_get_publishing_limit(ctx: Context) -> dict:
    """Check remaining publishing quota (250 posts/day, 1000 replies/day)."""
    try:
        access_token, user_id = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=access_token) as client:
            limit = await client.posts.get_publishing_limit(user_id)
            return {
                "success": True,
                "data": {
                    "posts_used": limit.quota_usage,
                    "posts_total": limit.quota_total,
                    "posts_remaining": limit.remaining_posts,
                }
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def threads_get_profile(ctx: Context) -> dict:
    """Get the authenticated user's profile."""
    try:
        access_token, _ = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=access_token) as client:
            profile = await client.users.get_me()
            return {
                "success": True,
                "data": {
                    "id": profile.id,
                    "username": profile.username,
                    "biography": profile.biography,
                    "profile_picture_url": profile.threads_profile_picture_url,
                }
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Project Structure

```
meta-threads-mcp/
├── pyproject.toml
├── README.md
└── src/
    └── meta_threads_mcp/
        ├── __init__.py
        └── server.py      # All tools in one file (FastMCP is simple)
```

## pyproject.toml

```toml
[project]
name = "meta-threads-mcp"
version = "0.1.0"
description = "MCP server for Meta's Threads API"
requires-python = ">=3.13"
dependencies = [
    "meta-threads-sdk>=0.1.0",
    "fastmcp>=0.1.0",
]

[project.scripts]
meta-threads-mcp = "meta_threads_mcp.server:main"
```

## server.py Entry Point

```python
# src/meta_threads_mcp/server.py

from fastmcp import FastMCP, Context
from threads import AsyncThreadsClient

mcp = FastMCP("meta-threads-mcp")


def parse_bearer_token(ctx: Context) -> tuple[str, str]:
    """Parse bearer token from request context."""
    token = ctx.request_context.get("bearer_token", "")
    if not token:
        raise ValueError("Missing bearer token")
    access_token, user_id = token.split(":", 1)
    return access_token, user_id


# ... all @mcp.tool() decorated functions ...


def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

## Usage

### Installation

```bash
pip install meta-threads-mcp
```

### Configuration (Claude Desktop)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "threads": {
      "command": "meta-threads-mcp"
    }
  }
}
```

The client passes the bearer token in the request context when calling tools.

### Running standalone

```bash
meta-threads-mcp
```

### Testing with FastMCP CLI

```bash
fastmcp dev src/meta_threads_mcp/server.py
```

## Error Handling

- Catch `ThreadsAPIError` and subclasses from the SDK
- Return user-friendly error messages in the `error` field
- Never expose raw stack traces to the LLM

## Notes

- Uses `AsyncThreadsClient` for native async support with FastMCP
- Bearer token is passed per-request via context (no server-side storage)
- Each tool creates its own client instance for stateless operation
- Rate limits: 250 posts/day, 1000 replies/day
- Video posts require waiting for processing before publishing
- Carousels are complex (multiple containers) - consider adding a simplified `threads_create_carousel` tool later
