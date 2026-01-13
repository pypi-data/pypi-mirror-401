"""MCP server for Meta's Threads API."""

from fastmcp import FastMCP

from meta_threads_mcp.prompts import (
    analyze_engagement,
    content_ideas,
    reply_strategy,
)
from meta_threads_mcp.tools.insights import (
    threads_get_media_insights,
    threads_get_user_insights,
)
from meta_threads_mcp.tools.posts import (
    threads_create_image_post,
    threads_create_post,
    threads_create_video_post,
    threads_delete_post,
    threads_get_post,
    threads_get_publishing_limit,
    threads_get_user_posts,
)
from meta_threads_mcp.tools.replies import (
    threads_get_conversation,
    threads_get_replies,
    threads_hide_reply,
    threads_reply_to_post,
    threads_unhide_reply,
)
from meta_threads_mcp.tools.users import threads_get_profile

mcp = FastMCP("meta-threads-mcp")

# Register post tools
mcp.tool()(threads_create_post)
mcp.tool()(threads_create_image_post)
mcp.tool()(threads_create_video_post)
mcp.tool()(threads_get_post)
mcp.tool()(threads_get_user_posts)
mcp.tool()(threads_delete_post)
mcp.tool()(threads_get_publishing_limit)

# Register reply tools
mcp.tool()(threads_reply_to_post)
mcp.tool()(threads_get_replies)
mcp.tool()(threads_get_conversation)
mcp.tool()(threads_hide_reply)
mcp.tool()(threads_unhide_reply)

# Register insight tools
mcp.tool()(threads_get_media_insights)
mcp.tool()(threads_get_user_insights)

# Register user tools
mcp.tool()(threads_get_profile)

# Register prompts
mcp.prompt()(reply_strategy)
mcp.prompt()(content_ideas)
mcp.prompt()(analyze_engagement)


def main() -> None:
    """Run the MCP server."""
    import sys
    from typing import Literal

    transport: Literal["stdio", "sse", "streamable-http"] = "stdio"
    if "--sse" in sys.argv:
        transport = "sse"
    elif "--http" in sys.argv:
        transport = "streamable-http"

    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
