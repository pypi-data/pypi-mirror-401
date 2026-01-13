"""User-related MCP tools."""

from typing import Any

from fastmcp import Context
from threads import AsyncThreadsClient

from meta_threads_mcp.auth import parse_bearer_token


async def threads_get_profile(ctx: Context) -> dict[str, Any]:
    """Get the authenticated user's profile.

    Args:
        ctx: FastMCP request context
    """
    try:
        creds = parse_bearer_token(ctx)
        async with AsyncThreadsClient(access_token=creds.access_token) as client:
            profile = await client.users.get_me()
            return {
                "success": True,
                "data": {
                    "id": profile.id,
                    "username": profile.username,
                    "name": profile.name,
                    "biography": profile.threads_biography,
                    "profile_picture_url": profile.threads_profile_picture_url,
                    "follower_count": profile.follower_count,
                    "following_count": profile.following_count,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
