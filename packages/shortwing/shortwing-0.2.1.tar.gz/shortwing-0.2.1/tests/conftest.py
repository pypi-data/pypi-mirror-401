"""Pytest fixtures for Shortwing tests."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def reset_core_cache():
    """Reset module-level cache in core.py before each test."""
    import shortwing.core

    shortwing.core._cached_token = None
    shortwing.core._client = None
    yield
    # Clean up after test
    shortwing.core._cached_token = None
    shortwing.core._client = None


@pytest.fixture
def mock_env_key(monkeypatch):
    """Set DIMENSIONS_KEY environment variable."""
    monkeypatch.setenv("DIMENSIONS_KEY", "test-api-key")


@pytest.fixture
def mock_env_endpoint(monkeypatch):
    """Set DIMENSIONS_ENDPOINT environment variable."""
    monkeypatch.setenv("DIMENSIONS_ENDPOINT", "https://test.endpoint.com")


@pytest.fixture
def clean_env(monkeypatch, tmp_path):
    """Remove all DIMENSIONS_* environment variables and isolate from real config files."""
    monkeypatch.delenv("DIMENSIONS_KEY", raising=False)
    monkeypatch.delenv("DIMENSIONS_ENDPOINT", raising=False)
    # Change to temp directory to prevent finding ./dsl.ini
    monkeypatch.chdir(tmp_path)
    # Patch the USER_CONFIG_FILE_PATH to point to non-existent file
    import shortwing.config
    monkeypatch.setattr(
        shortwing.config,
        "USER_CONFIG_FILE_PATH",
        str(tmp_path / ".dimensions" / "dsl.ini"),
    )


@pytest.fixture
def mock_httpx_success():
    """Mock httpx.AsyncClient for successful query."""
    with patch("shortwing.core.httpx.AsyncClient") as mock_client_class:
        # Create mock client instance
        mock_client = AsyncMock()

        # Mock auth response
        mock_auth_response = MagicMock()
        mock_auth_response.json.return_value = {"token": "test-jwt-token"}
        mock_auth_response.raise_for_status = MagicMock()

        # Mock query response
        mock_query_response = MagicMock()
        mock_query_response.json.return_value = {
            "researchers": [{"id": "ur.123", "first_name": "Test"}],
            "_stats": {"total_count": 1},
        }
        mock_query_response.raise_for_status = MagicMock()

        # Configure mock client to return appropriate responses
        async def mock_post(url, **kwargs):
            if "/api/auth" in url:
                return mock_auth_response
            elif "/api/dsl" in url:
                return mock_query_response
            raise ValueError(f"Unexpected URL: {url}")

        mock_client.post = AsyncMock(side_effect=mock_post)
        mock_client.aclose = AsyncMock()

        # Make AsyncClient() return our mock client
        mock_client_class.return_value = mock_client

        yield mock_client


@pytest.fixture
def mock_httpx_error():
    """Mock httpx.AsyncClient to return an error response."""
    with patch("shortwing.core.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()

        # Mock auth response (successful)
        mock_auth_response = MagicMock()
        mock_auth_response.json.return_value = {"token": "test-jwt-token"}
        mock_auth_response.raise_for_status = MagicMock()

        # Mock query response (error)
        mock_error_response = MagicMock()
        mock_error_response.json.return_value = {
            "error": {"message": "Invalid DSL syntax", "code": 400}
        }
        mock_error_response.raise_for_status = MagicMock()

        async def mock_post(url, **kwargs):
            if "/api/auth" in url:
                return mock_auth_response
            elif "/api/dsl" in url:
                return mock_error_response
            raise ValueError(f"Unexpected URL: {url}")

        mock_client.post = AsyncMock(side_effect=mock_post)
        mock_client.aclose = AsyncMock()

        mock_client_class.return_value = mock_client

        yield mock_client


@pytest.fixture
def runner():
    """Create a Click test runner."""
    from click.testing import CliRunner

    return CliRunner()


# Alias for backward compatibility with existing tests
@pytest.fixture
def mock_all_dimcli(mock_httpx_success):
    """Alias for mock_httpx_success for backward compatibility."""
    return mock_httpx_success
