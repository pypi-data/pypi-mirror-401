"""Tests for configuration module."""

import pytest

from shortwing.config import DEFAULT_ENDPOINT, read_dsl_ini, resolve_credentials
from shortwing.exceptions import ConfigurationError


class TestResolveCredentials:
    """Tests for resolve_credentials function."""

    def test_reads_from_environment(self, mock_env_key, mock_env_endpoint):
        """Should read credentials from environment variables."""
        key, endpoint = resolve_credentials()
        assert key == "test-api-key"
        assert endpoint == "https://test.endpoint.com"

    def test_flags_override_environment(self, mock_env_key, mock_env_endpoint):
        """CLI flags should override environment variables."""
        key, endpoint = resolve_credentials(
            key="override-key", endpoint="https://override.endpoint.com"
        )
        assert key == "override-key"
        assert endpoint == "https://override.endpoint.com"

    def test_default_endpoint(self, mock_env_key):
        """Should use default endpoint when not specified."""
        key, endpoint = resolve_credentials()
        assert endpoint == DEFAULT_ENDPOINT

    def test_missing_key_raises_error(self, clean_env):
        """Should raise ConfigurationError when key is missing."""
        with pytest.raises(ConfigurationError) as exc_info:
            resolve_credentials()
        assert "dsl.ini" in str(exc_info.value)

    def test_reads_from_dsl_ini(self, clean_env, tmp_path, monkeypatch):
        """Should read credentials from dsl.ini file."""
        # Create a dsl.ini file in a temp directory
        ini_content = """[instance.live]
url=https://ini.dimensions.ai
key=ini-api-key
"""
        ini_file = tmp_path / "dsl.ini"
        ini_file.write_text(ini_content)

        # Change to temp directory so dsl.ini is found
        monkeypatch.chdir(tmp_path)

        key, endpoint = resolve_credentials()
        assert key == "ini-api-key"
        assert endpoint == "https://ini.dimensions.ai"

    def test_env_overrides_dsl_ini(self, mock_env_key, tmp_path, monkeypatch):
        """Environment variables should override dsl.ini."""
        ini_content = """[instance.live]
url=https://ini.dimensions.ai
key=ini-api-key
"""
        ini_file = tmp_path / "dsl.ini"
        ini_file.write_text(ini_content)
        monkeypatch.chdir(tmp_path)

        key, endpoint = resolve_credentials()
        assert key == "test-api-key"  # From env, not ini
        assert endpoint == "https://ini.dimensions.ai"  # From ini (no env endpoint set)

    def test_flags_override_dsl_ini(self, clean_env, tmp_path, monkeypatch):
        """CLI flags should override dsl.ini."""
        ini_content = """[instance.live]
url=https://ini.dimensions.ai
key=ini-api-key
"""
        ini_file = tmp_path / "dsl.ini"
        ini_file.write_text(ini_content)
        monkeypatch.chdir(tmp_path)

        key, endpoint = resolve_credentials(
            key="flag-key", endpoint="https://flag.endpoint.com"
        )
        assert key == "flag-key"
        assert endpoint == "https://flag.endpoint.com"

    def test_instance_parameter(self, clean_env, tmp_path, monkeypatch):
        """Should read from specified instance in dsl.ini."""
        ini_content = """[instance.live]
url=https://live.dimensions.ai
key=live-key

[instance.test]
url=https://test.dimensions.ai
key=test-key
"""
        ini_file = tmp_path / "dsl.ini"
        ini_file.write_text(ini_content)
        monkeypatch.chdir(tmp_path)

        key, endpoint = resolve_credentials(instance="test")
        assert key == "test-key"
        assert endpoint == "https://test.dimensions.ai"


class TestReadDslIni:
    """Tests for read_dsl_ini function."""

    def test_returns_none_when_no_file(self, tmp_path, monkeypatch):
        """Should return None, None when no dsl.ini exists."""
        monkeypatch.chdir(tmp_path)
        key, endpoint = read_dsl_ini()
        assert key is None
        assert endpoint is None

    def test_returns_none_for_missing_instance(self, tmp_path, monkeypatch):
        """Should return None, None when instance section not found."""
        ini_content = """[instance.live]
url=https://live.dimensions.ai
key=live-key
"""
        ini_file = tmp_path / "dsl.ini"
        ini_file.write_text(ini_content)
        monkeypatch.chdir(tmp_path)

        key, endpoint = read_dsl_ini(instance="nonexistent")
        assert key is None
        assert endpoint is None

    def test_handles_empty_values(self, tmp_path, monkeypatch):
        """Should handle empty key/url values gracefully."""
        ini_content = """[instance.live]
url=
key=
"""
        ini_file = tmp_path / "dsl.ini"
        ini_file.write_text(ini_content)
        monkeypatch.chdir(tmp_path)

        key, endpoint = read_dsl_ini()
        assert key is None
        assert endpoint is None
