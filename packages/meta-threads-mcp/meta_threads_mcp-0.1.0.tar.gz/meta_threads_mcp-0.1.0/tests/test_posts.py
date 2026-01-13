"""Tests for post tools."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from meta_threads_mcp.tools.posts import (
    threads_create_image_post,
    threads_create_post,
    threads_create_video_post,
    threads_delete_post,
    threads_get_post,
    threads_get_publishing_limit,
    threads_get_user_posts,
)


@pytest.fixture
def mock_post() -> MagicMock:
    """Create a mock Post object."""
    post = MagicMock()
    post.id = "post_123"
    post.text = "Test post content"
    post.permalink = "https://threads.net/@user/post/123"
    post.media_type = "TEXT"
    post.timestamp = datetime(2024, 1, 15, 12, 0, 0)
    return post


class TestCreatePost:
    """Tests for threads_create_post."""

    @pytest.mark.asyncio
    async def test_create_post_success(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test successful post creation."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(return_value=mock_post)

            result = await threads_create_post(mock_context, "Hello Threads!")

            assert result["success"] is True
            assert result["data"]["id"] == "post_123"
            assert result["data"]["text"] == "Test post content"

    @pytest.mark.asyncio
    async def test_create_post_with_reply_control(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test post creation with reply control."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(return_value=mock_post)

            from threads.constants import ReplyControl

            result = await threads_create_post(
                mock_context, "Hello!", ReplyControl.MENTIONED_ONLY
            )

            assert result["success"] is True
            client.posts.create_and_publish.assert_called_once()
            call_kwargs = client.posts.create_and_publish.call_args.kwargs
            assert call_kwargs["reply_control"] == ReplyControl.MENTIONED_ONLY

    @pytest.mark.asyncio
    async def test_create_post_error(self, mock_context: MagicMock) -> None:
        """Test post creation error handling."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(
                side_effect=Exception("API Error")
            )

            result = await threads_create_post(mock_context, "Hello!")

            assert result["success"] is False
            assert "API Error" in result["error"]


class TestCreateImagePost:
    """Tests for threads_create_image_post."""

    @pytest.mark.asyncio
    async def test_create_image_post_success(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test successful image post creation."""
        mock_post.media_type = "IMAGE"
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(return_value=mock_post)

            result = await threads_create_image_post(
                mock_context, "https://example.com/image.jpg", "Check this out!"
            )

            assert result["success"] is True
            assert result["data"]["media_type"] == "IMAGE"

    @pytest.mark.asyncio
    async def test_create_image_post_error(self, mock_context: MagicMock) -> None:
        """Test image post creation error handling."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(
                side_effect=Exception("Invalid image URL")
            )

            result = await threads_create_image_post(
                mock_context, "https://example.com/bad.jpg"
            )

            assert result["success"] is False
            assert "Invalid image URL" in result["error"]


class TestCreateVideoPost:
    """Tests for threads_create_video_post."""

    @pytest.mark.asyncio
    async def test_create_video_post_success(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test successful video post creation."""
        mock_post.media_type = "VIDEO"
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(return_value=mock_post)

            result = await threads_create_video_post(
                mock_context, "https://example.com/video.mp4", "Watch this!"
            )

            assert result["success"] is True
            assert result["data"]["media_type"] == "VIDEO"

    @pytest.mark.asyncio
    async def test_create_video_post_error(self, mock_context: MagicMock) -> None:
        """Test video post creation error handling."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(
                side_effect=Exception("Video processing failed")
            )

            result = await threads_create_video_post(
                mock_context, "https://example.com/bad.mp4"
            )

            assert result["success"] is False
            assert "Video processing failed" in result["error"]


class TestGetPost:
    """Tests for threads_get_post."""

    @pytest.mark.asyncio
    async def test_get_post_success(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test successful post retrieval."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get = AsyncMock(return_value=mock_post)

            result = await threads_get_post(mock_context, "post_123")

            assert result["success"] is True
            assert result["data"]["id"] == "post_123"
            assert result["data"]["timestamp"] == "2024-01-15T12:00:00"

    @pytest.mark.asyncio
    async def test_get_post_no_timestamp(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test post retrieval with no timestamp."""
        mock_post.timestamp = None
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get = AsyncMock(return_value=mock_post)

            result = await threads_get_post(mock_context, "post_123")

            assert result["success"] is True
            assert result["data"]["timestamp"] is None

    @pytest.mark.asyncio
    async def test_get_post_not_found(self, mock_context: MagicMock) -> None:
        """Test post not found error."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get = AsyncMock(side_effect=Exception("Post not found"))

            result = await threads_get_post(mock_context, "invalid_id")

            assert result["success"] is False
            assert "Post not found" in result["error"]


class TestGetUserPosts:
    """Tests for threads_get_user_posts."""

    @pytest.mark.asyncio
    async def test_get_user_posts_success(
        self, mock_context: MagicMock, mock_post: MagicMock
    ) -> None:
        """Test successful user posts retrieval."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get_user_posts = AsyncMock(return_value=[mock_post, mock_post])

            result = await threads_get_user_posts(mock_context, limit=5)

            assert result["success"] is True
            assert len(result["data"]["posts"]) == 2

    @pytest.mark.asyncio
    async def test_get_user_posts_empty(self, mock_context: MagicMock) -> None:
        """Test empty user posts."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get_user_posts = AsyncMock(return_value=[])

            result = await threads_get_user_posts(mock_context)

            assert result["success"] is True
            assert result["data"]["posts"] == []

    @pytest.mark.asyncio
    async def test_get_user_posts_error(self, mock_context: MagicMock) -> None:
        """Test user posts retrieval error."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get_user_posts = AsyncMock(
                side_effect=Exception("Rate limit exceeded")
            )

            result = await threads_get_user_posts(mock_context)

            assert result["success"] is False
            assert "Rate limit exceeded" in result["error"]


class TestDeletePost:
    """Tests for threads_delete_post."""

    @pytest.mark.asyncio
    async def test_delete_post_success(self, mock_context: MagicMock) -> None:
        """Test successful post deletion."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.delete = AsyncMock()

            result = await threads_delete_post(mock_context, "post_123")

            assert result["success"] is True
            assert result["data"]["deleted"] is True
            assert result["data"]["post_id"] == "post_123"

    @pytest.mark.asyncio
    async def test_delete_post_error(self, mock_context: MagicMock) -> None:
        """Test post deletion error."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.delete = AsyncMock(side_effect=Exception("Permission denied"))

            result = await threads_delete_post(mock_context, "post_123")

            assert result["success"] is False
            assert "Permission denied" in result["error"]


class TestGetPublishingLimit:
    """Tests for threads_get_publishing_limit."""

    @pytest.mark.asyncio
    async def test_get_publishing_limit_success(self, mock_context: MagicMock) -> None:
        """Test successful publishing limit retrieval."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client

            limit = MagicMock()
            limit.quota_usage = 50
            limit.quota_total = 250
            limit.remaining_posts = 200
            client.posts.get_publishing_limit = AsyncMock(return_value=limit)

            result = await threads_get_publishing_limit(mock_context)

            assert result["success"] is True
            assert result["data"]["posts_used"] == 50
            assert result["data"]["posts_total"] == 250
            assert result["data"]["posts_remaining"] == 200

    @pytest.mark.asyncio
    async def test_get_publishing_limit_error(self, mock_context: MagicMock) -> None:
        """Test publishing limit retrieval error."""
        with patch(
            "meta_threads_mcp.tools.posts.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.get_publishing_limit = AsyncMock(
                side_effect=Exception("API unavailable")
            )

            result = await threads_get_publishing_limit(mock_context)

            assert result["success"] is False
            assert "API unavailable" in result["error"]
