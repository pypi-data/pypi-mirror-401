"""Tests for user tools."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from meta_threads_mcp.tools.users import threads_get_profile


@pytest.fixture
def mock_profile() -> MagicMock:
    """Create a mock user profile."""
    profile = MagicMock()
    profile.id = "user_123"
    profile.username = "testuser"
    profile.name = "Test User"
    profile.threads_biography = "Hello, I'm a test user!"
    profile.threads_profile_picture_url = "https://example.com/pic.jpg"
    profile.follower_count = 1000
    profile.following_count = 500
    return profile


class TestGetProfile:
    """Tests for threads_get_profile."""

    @pytest.mark.asyncio
    async def test_get_profile_success(
        self, mock_context: MagicMock, mock_profile: MagicMock
    ) -> None:
        """Test successful profile retrieval."""
        with patch(
            "meta_threads_mcp.tools.users.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.users.get_me = AsyncMock(return_value=mock_profile)

            result = await threads_get_profile(mock_context)

            assert result["success"] is True
            assert result["data"]["id"] == "user_123"
            assert result["data"]["username"] == "testuser"
            assert result["data"]["name"] == "Test User"
            assert result["data"]["biography"] == "Hello, I'm a test user!"
            assert (
                result["data"]["profile_picture_url"] == "https://example.com/pic.jpg"
            )
            assert result["data"]["follower_count"] == 1000
            assert result["data"]["following_count"] == 500

    @pytest.mark.asyncio
    async def test_get_profile_no_bio(
        self, mock_context: MagicMock, mock_profile: MagicMock
    ) -> None:
        """Test profile with no biography."""
        mock_profile.threads_biography = None
        with patch(
            "meta_threads_mcp.tools.users.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.users.get_me = AsyncMock(return_value=mock_profile)

            result = await threads_get_profile(mock_context)

            assert result["success"] is True
            assert result["data"]["biography"] is None

    @pytest.mark.asyncio
    async def test_get_profile_error(self, mock_context: MagicMock) -> None:
        """Test profile retrieval error."""
        with patch(
            "meta_threads_mcp.tools.users.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.users.get_me = AsyncMock(
                side_effect=Exception("Authentication failed")
            )

            result = await threads_get_profile(mock_context)

            assert result["success"] is False
            assert "Authentication failed" in result["error"]
