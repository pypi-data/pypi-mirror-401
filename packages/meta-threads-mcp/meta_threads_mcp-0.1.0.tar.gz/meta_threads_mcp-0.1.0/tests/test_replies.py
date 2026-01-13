"""Tests for reply tools."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from meta_threads_mcp.tools.replies import (
    threads_get_conversation,
    threads_get_replies,
    threads_hide_reply,
    threads_reply_to_post,
    threads_unhide_reply,
)


@pytest.fixture
def mock_reply() -> MagicMock:
    """Create a mock reply object."""
    reply = MagicMock()
    reply.id = "reply_456"
    reply.text = "This is a reply"
    reply.permalink = "https://threads.net/@user/post/456"
    reply.media_type = "TEXT"
    reply.timestamp = datetime(2024, 1, 15, 14, 30, 0)
    return reply


class TestReplyToPost:
    """Tests for threads_reply_to_post."""

    @pytest.mark.asyncio
    async def test_reply_success(
        self, mock_context: MagicMock, mock_reply: MagicMock
    ) -> None:
        """Test successful reply creation."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(return_value=mock_reply)

            result = await threads_reply_to_post(
                mock_context, "post_123", "Great post!"
            )

            assert result["success"] is True
            assert result["data"]["id"] == "reply_456"
            assert result["data"]["text"] == "This is a reply"
            client.posts.create_and_publish.assert_called_once_with(
                user_id="user_123",
                text="Great post!",
                reply_to_id="post_123",
            )

    @pytest.mark.asyncio
    async def test_reply_error(self, mock_context: MagicMock) -> None:
        """Test reply creation error."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.posts.create_and_publish = AsyncMock(
                side_effect=Exception("Reply limit reached")
            )

            result = await threads_reply_to_post(mock_context, "post_123", "My reply")

            assert result["success"] is False
            assert "Reply limit reached" in result["error"]


class TestGetReplies:
    """Tests for threads_get_replies."""

    @pytest.mark.asyncio
    async def test_get_replies_success(
        self, mock_context: MagicMock, mock_reply: MagicMock
    ) -> None:
        """Test successful replies retrieval."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_replies = AsyncMock(return_value=[mock_reply])

            result = await threads_get_replies(mock_context, "post_123")

            assert result["success"] is True
            assert len(result["data"]["replies"]) == 1
            assert result["data"]["replies"][0]["id"] == "reply_456"

    @pytest.mark.asyncio
    async def test_get_replies_empty(self, mock_context: MagicMock) -> None:
        """Test empty replies list."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_replies = AsyncMock(return_value=[])

            result = await threads_get_replies(mock_context, "post_123")

            assert result["success"] is True
            assert result["data"]["replies"] == []

    @pytest.mark.asyncio
    async def test_get_replies_no_timestamp(
        self, mock_context: MagicMock, mock_reply: MagicMock
    ) -> None:
        """Test replies with no timestamp."""
        mock_reply.timestamp = None
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_replies = AsyncMock(return_value=[mock_reply])

            result = await threads_get_replies(mock_context, "post_123")

            assert result["success"] is True
            assert result["data"]["replies"][0]["timestamp"] is None

    @pytest.mark.asyncio
    async def test_get_replies_error(self, mock_context: MagicMock) -> None:
        """Test replies retrieval error."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_replies = AsyncMock(
                side_effect=Exception("Post not found")
            )

            result = await threads_get_replies(mock_context, "invalid_id")

            assert result["success"] is False
            assert "Post not found" in result["error"]


class TestGetConversation:
    """Tests for threads_get_conversation."""

    @pytest.mark.asyncio
    async def test_get_conversation_success(
        self, mock_context: MagicMock, mock_reply: MagicMock
    ) -> None:
        """Test successful conversation retrieval."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_conversation = AsyncMock(
                return_value=[mock_reply, mock_reply]
            )

            result = await threads_get_conversation(mock_context, "post_123")

            assert result["success"] is True
            assert len(result["data"]["posts"]) == 2

    @pytest.mark.asyncio
    async def test_get_conversation_no_timestamp(
        self, mock_context: MagicMock, mock_reply: MagicMock
    ) -> None:
        """Test conversation with no timestamp."""
        mock_reply.timestamp = None
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_conversation = AsyncMock(return_value=[mock_reply])

            result = await threads_get_conversation(mock_context, "post_123")

            assert result["success"] is True
            assert result["data"]["posts"][0]["timestamp"] is None

    @pytest.mark.asyncio
    async def test_get_conversation_error(self, mock_context: MagicMock) -> None:
        """Test conversation retrieval error."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.get_conversation = AsyncMock(
                side_effect=Exception("Conversation not found")
            )

            result = await threads_get_conversation(mock_context, "invalid_id")

            assert result["success"] is False
            assert "Conversation not found" in result["error"]


class TestHideReply:
    """Tests for threads_hide_reply."""

    @pytest.mark.asyncio
    async def test_hide_reply_success(self, mock_context: MagicMock) -> None:
        """Test successful reply hiding."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.hide = AsyncMock()

            result = await threads_hide_reply(mock_context, "reply_456")

            assert result["success"] is True
            assert result["data"]["hidden"] is True
            assert result["data"]["reply_id"] == "reply_456"

    @pytest.mark.asyncio
    async def test_hide_reply_error(self, mock_context: MagicMock) -> None:
        """Test reply hiding error."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.hide = AsyncMock(
                side_effect=Exception("Cannot hide this reply")
            )

            result = await threads_hide_reply(mock_context, "reply_456")

            assert result["success"] is False
            assert "Cannot hide this reply" in result["error"]


class TestUnhideReply:
    """Tests for threads_unhide_reply."""

    @pytest.mark.asyncio
    async def test_unhide_reply_success(self, mock_context: MagicMock) -> None:
        """Test successful reply unhiding."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.unhide = AsyncMock()

            result = await threads_unhide_reply(mock_context, "reply_456")

            assert result["success"] is True
            assert result["data"]["hidden"] is False
            assert result["data"]["reply_id"] == "reply_456"

    @pytest.mark.asyncio
    async def test_unhide_reply_error(self, mock_context: MagicMock) -> None:
        """Test reply unhiding error."""
        with patch(
            "meta_threads_mcp.tools.replies.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.replies.unhide = AsyncMock(side_effect=Exception("Reply not found"))

            result = await threads_unhide_reply(mock_context, "reply_456")

            assert result["success"] is False
            assert "Reply not found" in result["error"]
