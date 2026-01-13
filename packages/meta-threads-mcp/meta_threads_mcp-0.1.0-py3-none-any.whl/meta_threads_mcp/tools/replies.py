"""Reply-related MCP tools."""

from typing import Any

from fastmcp import Context
from threads import AsyncThreadsClient

from meta_threads_mcp.auth import parse_bearer_token


async def threads_reply_to_post(
    ctx: Context, post_id: str, text: str
) -> dict[str, Any]:
    """Reply to an existing Threads post.

    Args:
        ctx: FastMCP request context
        post_id: The ID of the post to reply to
        text: The text content of the reply
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            reply = await client.posts.create_and_publish(
                user_id=creds.user_id,
                text=text,
                reply_to_id=post_id,
            )
            return {
                "success": True,
                "data": {
                    "id": reply.id,
                    "permalink": reply.permalink,
                    "text": reply.text,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_get_replies(ctx: Context, post_id: str) -> dict[str, Any]:
    """Get replies to a Threads post.

    Args:
        ctx: FastMCP request context
        post_id: The ID of the post to get replies for
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            replies = await client.replies.get_replies(post_id)
            return {
                "success": True,
                "data": {
                    "replies": [
                        {
                            "id": r.id,
                            "text": r.text,
                            "media_type": r.media_type,
                            "permalink": r.permalink,
                            "timestamp": r.timestamp.isoformat()
                            if r.timestamp
                            else None,
                        }
                        for r in replies
                    ]
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_get_conversation(ctx: Context, post_id: str) -> dict[str, Any]:
    """Get the full conversation thread for a post.

    Args:
        ctx: FastMCP request context
        post_id: The ID of the post to get the conversation for
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            conversation = await client.replies.get_conversation(post_id)
            return {
                "success": True,
                "data": {
                    "posts": [
                        {
                            "id": p.id,
                            "text": p.text,
                            "media_type": p.media_type,
                            "permalink": p.permalink,
                            "timestamp": p.timestamp.isoformat()
                            if p.timestamp
                            else None,
                        }
                        for p in conversation
                    ]
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_hide_reply(ctx: Context, reply_id: str) -> dict[str, Any]:
    """Hide a reply to your post.

    Args:
        ctx: FastMCP request context
        reply_id: The ID of the reply to hide
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            await client.replies.hide(reply_id)
            return {
                "success": True,
                "data": {"hidden": True, "reply_id": reply_id},
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_unhide_reply(ctx: Context, reply_id: str) -> dict[str, Any]:
    """Unhide a previously hidden reply.

    Args:
        ctx: FastMCP request context
        reply_id: The ID of the reply to unhide
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            await client.replies.unhide(reply_id)
            return {
                "success": True,
                "data": {"hidden": False, "reply_id": reply_id},
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
