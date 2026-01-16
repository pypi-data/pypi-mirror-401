"""Pytest fixtures for Shortwing tests."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_env_key(monkeypatch):
    """Set DIMENSIONS_KEY environment variable."""
    monkeypatch.setenv("DIMENSIONS_KEY", "test-api-key")


@pytest.fixture
def mock_env_endpoint(monkeypatch):
    """Set DIMENSIONS_ENDPOINT environment variable."""
    monkeypatch.setenv("DIMENSIONS_ENDPOINT", "https://test.endpoint.com")


@pytest.fixture
def clean_env(monkeypatch):
    """Remove all DIMENSIONS_* environment variables."""
    monkeypatch.delenv("DIMENSIONS_KEY", raising=False)
    monkeypatch.delenv("DIMENSIONS_ENDPOINT", raising=False)


@pytest.fixture
def mock_dimcli():
    """Mock dimcli.Dsl and dimcli.login."""
    with patch("shortwing.core.dimcli") as mock:
        mock_dsl_instance = MagicMock()
        mock_dsl_instance.query.return_value.json = {
            "researchers": [{"id": "ur.123", "first_name": "Test"}],
            "_stats": {"total_count": 1},
        }
        mock.Dsl.return_value = mock_dsl_instance
        yield mock


@pytest.fixture
def mock_dimcli_error():
    """Mock dimcli to return an error response."""
    with patch("shortwing.core.dimcli") as mock:
        mock_dsl_instance = MagicMock()
        mock_dsl_instance.query.return_value.json = {
            "error": {"message": "Invalid DSL syntax", "code": 400}
        }
        mock.Dsl.return_value = mock_dsl_instance
        yield mock


@pytest.fixture
def runner():
    """Create a Click test runner."""
    from click.testing import CliRunner

    return CliRunner()


@pytest.fixture
def mock_all_dimcli():
    """Mock all dimcli interactions for CLI tests."""
    with (
        patch("shortwing.config.dimcli") as config_mock,
        patch("shortwing.core.dimcli") as core_mock,
    ):
        mock_dsl_instance = MagicMock()
        mock_dsl_instance.query.return_value.json = {
            "researchers": [{"id": "test"}],
            "_stats": {"total_count": 1},
        }
        core_mock.Dsl.return_value = mock_dsl_instance
        yield core_mock
