"""Shared test fixtures."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_context() -> MagicMock:
    """Create a mock FastMCP context."""
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_auth_headers():
    """Patch get_http_headers to return test credentials for all tests."""
    with patch("meta_threads_mcp.auth.get_http_headers") as mock_headers:
        mock_headers.return_value = {"authorization": "Bearer test_token:user_123"}
        yield mock_headers
