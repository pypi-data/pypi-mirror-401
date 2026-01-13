"""Post-related MCP tools."""

from typing import Any

from fastmcp import Context
from threads import AsyncThreadsClient
from threads.constants import ReplyControl

from meta_threads_mcp.auth import parse_bearer_token


async def threads_create_post(
    ctx: Context,
    text: str,
    reply_control: ReplyControl = ReplyControl.EVERYONE,
) -> dict[str, Any]:
    """Create and publish a text post to Threads.

    Args:
        ctx: FastMCP request context
        text: The text content of the post
        reply_control: Who can reply - EVERYONE, ACCOUNTS_YOU_FOLLOW, or MENTIONED_ONLY
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            post = await client.posts.create_and_publish(
                user_id=creds.user_id,
                text=text,
                reply_control=reply_control,
            )
            return {
                "success": True,
                "data": {
                    "id": post.id,
                    "permalink": post.permalink,
                    "text": post.text,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_create_image_post(
    ctx: Context,
    image_url: str,
    text: str = "",
    reply_control: ReplyControl = ReplyControl.EVERYONE,
) -> dict[str, Any]:
    """Create and publish a post with an image to Threads.

    Args:
        ctx: FastMCP request context
        image_url: URL of the image to post
        text: Optional text content of the post
        reply_control: Who can reply - EVERYONE, ACCOUNTS_YOU_FOLLOW, or MENTIONED_ONLY
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            post = await client.posts.create_and_publish(
                user_id=creds.user_id,
                text=text if text else None,
                image_url=image_url,
                reply_control=reply_control,
            )
            return {
                "success": True,
                "data": {
                    "id": post.id,
                    "permalink": post.permalink,
                    "text": post.text,
                    "media_type": post.media_type,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_create_video_post(
    ctx: Context,
    video_url: str,
    text: str = "",
    reply_control: ReplyControl = ReplyControl.EVERYONE,
) -> dict[str, Any]:
    """Create and publish a post with a video to Threads.

    Args:
        ctx: FastMCP request context
        video_url: URL of the video to post
        text: Optional text content of the post
        reply_control: Who can reply - EVERYONE, ACCOUNTS_YOU_FOLLOW, or MENTIONED_ONLY
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            post = await client.posts.create_and_publish(
                user_id=creds.user_id,
                text=text if text else None,
                video_url=video_url,
                reply_control=reply_control,
            )
            return {
                "success": True,
                "data": {
                    "id": post.id,
                    "permalink": post.permalink,
                    "text": post.text,
                    "media_type": post.media_type,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_get_post(ctx: Context, post_id: str) -> dict[str, Any]:
    """Get a Threads post by ID.

    Args:
        ctx: FastMCP request context
        post_id: The ID of the post to retrieve
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            post = await client.posts.get(post_id)
            return {
                "success": True,
                "data": {
                    "id": post.id,
                    "text": post.text,
                    "media_type": post.media_type,
                    "permalink": post.permalink,
                    "timestamp": post.timestamp.isoformat() if post.timestamp else None,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_get_user_posts(ctx: Context, limit: int = 10) -> dict[str, Any]:
    """Get the authenticated user's recent posts.

    Args:
        ctx: FastMCP request context
        limit: Maximum number of posts to return (default 10)
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            posts = await client.posts.get_user_posts(creds.user_id, limit=limit)
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
                        for p in posts
                    ]
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_delete_post(ctx: Context, post_id: str) -> dict[str, Any]:
    """Delete a Threads post.

    Args:
        ctx: FastMCP request context
        post_id: The ID of the post to delete
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            await client.posts.delete(post_id)
            return {
                "success": True,
                "data": {"deleted": True, "post_id": post_id},
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_get_publishing_limit(ctx: Context) -> dict[str, Any]:
    """Check remaining publishing quota (250 posts/day, 1000 replies/day).

    Args:
        ctx: FastMCP request context
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            limit = await client.posts.get_publishing_limit(creds.user_id)
            return {
                "success": True,
                "data": {
                    "posts_used": limit.quota_usage,
                    "posts_total": limit.quota_total,
                    "posts_remaining": limit.remaining_posts,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
