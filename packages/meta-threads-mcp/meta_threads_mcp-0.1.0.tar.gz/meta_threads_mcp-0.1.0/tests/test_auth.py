"""Tests for the MCP server."""

from unittest.mock import MagicMock, patch

import pytest

from meta_threads_mcp.auth import Credentials, get_credentials, parse_bearer_token


class TestCredentials:
    """Tests for the Credentials dataclass."""

    def test_credentials_immutable(self) -> None:
        """Test that credentials are immutable."""
        creds = Credentials(access_token="token", user_id="123")
        with pytest.raises(AttributeError):
            creds.access_token = "new_token"  # type: ignore[misc]

    def test_credentials_slots(self) -> None:
        """Test that credentials use slots for memory efficiency."""
        creds = Credentials(access_token="token", user_id="123")
        assert not hasattr(creds, "__dict__")


class TestGetCredentialsFromHeader:
    """Tests for HTTP header authentication."""

    def test_valid_header(self) -> None:
        """Test parsing a valid bearer token from header."""
        with patch("meta_threads_mcp.auth.get_http_headers") as mock_headers:
            mock_headers.return_value = {
                "authorization": "Bearer access_token_123:user_456"
            }
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "access_token_123"
            assert creds.user_id == "user_456"

    def test_token_with_colon_in_user_id(self) -> None:
        """Test parsing token where user_id contains colons."""
        with patch("meta_threads_mcp.auth.get_http_headers") as mock_headers:
            mock_headers.return_value = {
                "authorization": "Bearer token:user:with:colons"
            }
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "token"
            assert creds.user_id == "user:with:colons"

    def test_header_takes_priority_over_env(self) -> None:
        """Test that HTTP header is preferred over environment variables."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict(
                "os.environ",
                {"THREADS_ACCESS_TOKEN": "env_token", "THREADS_USER_ID": "env_user"},
            ),
        ):
            mock_headers.return_value = {
                "authorization": "Bearer header_token:header_user"
            }
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "header_token"
            assert creds.user_id == "header_user"


class TestGetCredentialsFromEnv:
    """Tests for environment variable authentication."""

    def test_valid_env_vars(self) -> None:
        """Test getting credentials from environment variables."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict(
                "os.environ",
                {"THREADS_ACCESS_TOKEN": "env_token", "THREADS_USER_ID": "env_user"},
            ),
        ):
            mock_headers.return_value = {}
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "env_token"
            assert creds.user_id == "env_user"

    def test_env_fallback_when_header_invalid(self) -> None:
        """Test fallback to env vars when header is invalid."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict(
                "os.environ",
                {"THREADS_ACCESS_TOKEN": "env_token", "THREADS_USER_ID": "env_user"},
            ),
        ):
            mock_headers.return_value = {"authorization": "Bearer invalid_no_colon"}
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "env_token"
            assert creds.user_id == "env_user"

    def test_env_fallback_when_header_exception(self) -> None:
        """Test fallback to env vars when get_http_headers raises."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict(
                "os.environ",
                {"THREADS_ACCESS_TOKEN": "env_token", "THREADS_USER_ID": "env_user"},
            ),
        ):
            mock_headers.side_effect = Exception("No HTTP context")
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "env_token"
            assert creds.user_id == "env_user"

    def test_env_vars_stripped(self) -> None:
        """Test that environment variables are stripped of whitespace."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict(
                "os.environ",
                {"THREADS_ACCESS_TOKEN": "  token  ", "THREADS_USER_ID": "  user  "},
            ),
        ):
            mock_headers.return_value = {}
            ctx = MagicMock()

            creds = get_credentials(ctx)

            assert creds.access_token == "token"
            assert creds.user_id == "user"


class TestGetCredentialsMissing:
    """Tests for missing credentials."""

    def test_no_credentials_raises(self) -> None:
        """Test that missing credentials raises ValueError with helpful message."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict("os.environ", {}, clear=True),
        ):
            mock_headers.return_value = {}
            ctx = MagicMock()

            with pytest.raises(ValueError, match="Missing credentials"):
                get_credentials(ctx)

    def test_partial_env_missing_token_raises(self) -> None:
        """Test that partial env vars (missing token) raises ValueError."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict("os.environ", {"THREADS_USER_ID": "user"}, clear=True),
        ):
            mock_headers.return_value = {}
            ctx = MagicMock()

            with pytest.raises(ValueError, match="Missing credentials"):
                get_credentials(ctx)

    def test_partial_env_missing_user_raises(self) -> None:
        """Test that partial env vars (missing user) raises ValueError."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict("os.environ", {"THREADS_ACCESS_TOKEN": "token"}, clear=True),
        ):
            mock_headers.return_value = {}
            ctx = MagicMock()

            with pytest.raises(ValueError, match="Missing credentials"):
                get_credentials(ctx)

    def test_empty_env_vars_raises(self) -> None:
        """Test that empty env vars raises ValueError."""
        with (
            patch("meta_threads_mcp.auth.get_http_headers") as mock_headers,
            patch.dict(
                "os.environ",
                {"THREADS_ACCESS_TOKEN": "", "THREADS_USER_ID": ""},
                clear=True,
            ),
        ):
            mock_headers.return_value = {}
            ctx = MagicMock()

            with pytest.raises(ValueError, match="Missing credentials"):
                get_credentials(ctx)


class TestBackwardsCompatibility:
    """Tests for backwards compatibility."""

    def test_parse_bearer_token_alias(self) -> None:
        """Test that parse_bearer_token is an alias for get_credentials."""
        assert parse_bearer_token is get_credentials
