"""Authentication utilities for the MCP server."""

import os
from dataclasses import dataclass

from fastmcp import Context
from fastmcp.server.dependencies import get_http_headers


@dataclass(frozen=True, slots=True)
class Credentials:
    """Parsed credentials for Threads API."""

    access_token: str
    user_id: str


def _get_credentials_from_env() -> Credentials | None:
    """Get credentials from environment variables.

    Environment variables:
        THREADS_ACCESS_TOKEN: The Threads API access token
        THREADS_USER_ID: The Threads user ID

    Returns:
        Credentials if both env vars are set, None otherwise
    """
    access_token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
    user_id = os.environ.get("THREADS_USER_ID", "").strip()

    if access_token and user_id:
        return Credentials(access_token=access_token, user_id=user_id)
    return None


def _get_credentials_from_header() -> Credentials | None:
    """Get credentials from HTTP Authorization header.

    Header format: Authorization: Bearer <access_token>:<user_id>

    Returns:
        Credentials if valid header is present, None otherwise
    """
    try:
        headers = get_http_headers()
    except Exception:
        return None

    auth_header = headers.get("authorization", "")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return None

    parts = token.split(":", 1)
    if len(parts) != 2:
        return None

    access_token, user_id = parts
    if not access_token or not user_id:
        return None

    return Credentials(access_token=access_token, user_id=user_id)


def get_credentials(ctx: Context) -> Credentials:
    """Get credentials from HTTP header or environment variables.

    Tries HTTP Authorization header first (for SSE/HTTP transport),
    then falls back to environment variables (for stdio transport).

    Args:
        ctx: FastMCP request context

    Returns:
        Credentials with access_token and user_id

    Raises:
        ValueError: If no valid credentials are found
    """
    # Try HTTP header first (SSE/HTTP transport)
    creds = _get_credentials_from_header()
    if creds:
        return creds

    # Fall back to environment variables (stdio transport)
    creds = _get_credentials_from_env()
    if creds:
        return creds

    raise ValueError(
        "Missing credentials. Provide either:\n"
        "  - HTTP header: Authorization: Bearer <access_token>:<user_id>\n"
        "  - Environment variables: THREADS_ACCESS_TOKEN and THREADS_USER_ID"
    )


# Backwards compatibility alias
parse_bearer_token = get_credentials
