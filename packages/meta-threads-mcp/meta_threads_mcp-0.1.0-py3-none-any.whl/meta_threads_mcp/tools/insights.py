"""Insights-related MCP tools."""

from typing import Any

from fastmcp import Context
from threads import AsyncThreadsClient

from meta_threads_mcp.auth import parse_bearer_token


async def threads_get_media_insights(ctx: Context, media_id: str) -> dict[str, Any]:
    """Get metrics/insights for a specific post.

    Args:
        ctx: FastMCP request context
        media_id: The ID of the media/post to get insights for
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            insights = await client.insights.get_media_insights(media_id)
            return {
                "success": True,
                "data": {
                    "media_id": media_id,
                    "metrics": {
                        "views": insights.views,
                        "likes": insights.likes,
                        "replies": insights.replies,
                        "reposts": insights.reposts,
                        "quotes": insights.quotes,
                    },
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def threads_get_user_insights(ctx: Context) -> dict[str, Any]:
    """Get user-level metrics/insights for the authenticated user.

    Args:
        ctx: FastMCP request context
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            insights = await client.insights.get_user_insights(creds.user_id)
            return {
                "success": True,
                "data": {
                    "user_id": creds.user_id,
                    "metrics": {
                        "views": insights.get_metric("views"),
                        "followers_count": insights.get_metric("followers_count"),
                    },
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
