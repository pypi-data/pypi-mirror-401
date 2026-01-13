"""Tests for insight tools."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from meta_threads_mcp.tools.insights import (
    threads_get_media_insights,
    threads_get_user_insights,
)


@pytest.fixture
def mock_media_insights() -> MagicMock:
    """Create mock media insights."""
    insights = MagicMock()
    insights.views = 1500
    insights.likes = 120
    insights.replies = 25
    insights.reposts = 10
    insights.quotes = 5
    return insights


@pytest.fixture
def mock_user_insights() -> MagicMock:
    """Create mock user insights."""
    insights = MagicMock()
    insights.get_metric = MagicMock(
        side_effect=lambda m: {"views": 50000, "followers_count": 10000}.get(m)
    )
    return insights


class TestGetMediaInsights:
    """Tests for threads_get_media_insights."""

    @pytest.mark.asyncio
    async def test_get_media_insights_success(
        self, mock_context: MagicMock, mock_media_insights: MagicMock
    ) -> None:
        """Test successful media insights retrieval."""
        with patch(
            "meta_threads_mcp.tools.insights.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.insights.get_media_insights = AsyncMock(
                return_value=mock_media_insights
            )

            result = await threads_get_media_insights(mock_context, "media_123")

            assert result["success"] is True
            assert result["data"]["media_id"] == "media_123"
            assert result["data"]["metrics"]["views"] == 1500
            assert result["data"]["metrics"]["likes"] == 120
            assert result["data"]["metrics"]["replies"] == 25
            assert result["data"]["metrics"]["reposts"] == 10
            assert result["data"]["metrics"]["quotes"] == 5

    @pytest.mark.asyncio
    async def test_get_media_insights_error(self, mock_context: MagicMock) -> None:
        """Test media insights retrieval error."""
        with patch(
            "meta_threads_mcp.tools.insights.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.insights.get_media_insights = AsyncMock(
                side_effect=Exception("Insights not available")
            )

            result = await threads_get_media_insights(mock_context, "media_123")

            assert result["success"] is False
            assert "Insights not available" in result["error"]


class TestGetUserInsights:
    """Tests for threads_get_user_insights."""

    @pytest.mark.asyncio
    async def test_get_user_insights_success(
        self, mock_context: MagicMock, mock_user_insights: MagicMock
    ) -> None:
        """Test successful user insights retrieval."""
        with patch(
            "meta_threads_mcp.tools.insights.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.insights.get_user_insights = AsyncMock(
                return_value=mock_user_insights
            )

            result = await threads_get_user_insights(mock_context)

            assert result["success"] is True
            assert result["data"]["user_id"] == "user_123"
            assert result["data"]["metrics"]["views"] == 50000
            assert result["data"]["metrics"]["followers_count"] == 10000

    @pytest.mark.asyncio
    async def test_get_user_insights_error(self, mock_context: MagicMock) -> None:
        """Test user insights retrieval error."""
        with patch(
            "meta_threads_mcp.tools.insights.AsyncThreadsClient"
        ) as mock_client_cls:
            client = AsyncMock()
            mock_client_cls.return_value.__aenter__.return_value = client
            client.insights.get_user_insights = AsyncMock(
                side_effect=Exception("User insights unavailable")
            )

            result = await threads_get_user_insights(mock_context)

            assert result["success"] is False
            assert "User insights unavailable" in result["error"]
