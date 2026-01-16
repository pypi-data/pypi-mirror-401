"""CLI integration tests."""

from unittest.mock import MagicMock, patch

import pytest

from shortwing.cli import main
from shortwing.exceptions import EXIT_CONFIG_ERROR, EXIT_QUERY_ERROR, EXIT_SUCCESS


class TestCLIHelp:
    """Tests for CLI help and version."""

    def test_help_option(self, runner):
        """--help should show usage information."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Shortwing" in result.output

    def test_version_option(self, runner):
        """--version should show version."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "shortwing" in result.output


class TestCLIInput:
    """Tests for query input handling."""

    def test_query_from_argument(self, runner, mock_all_dimcli):
        """Should accept query as positional argument."""
        result = runner.invoke(
            main, ["search grants"], env={"DIMENSIONS_KEY": "test-key"}
        )
        assert result.exit_code == EXIT_SUCCESS

    def test_query_from_stdin(self, runner, mock_all_dimcli):
        """Should accept query from stdin."""
        result = runner.invoke(
            main, [], input="search grants\n", env={"DIMENSIONS_KEY": "test-key"}
        )
        assert result.exit_code == EXIT_SUCCESS

    def test_stdin_takes_precedence(self, runner, mock_all_dimcli):
        """Stdin should take precedence over argument."""
        result = runner.invoke(
            main,
            ["argument query"],
            input="stdin query\n",
            env={"DIMENSIONS_KEY": "test-key"},
        )
        mock_all_dimcli.Dsl.return_value.query.assert_called_with("stdin query")

    def test_whitespace_trimmed(self, runner, mock_all_dimcli):
        """Leading/trailing whitespace should be trimmed."""
        result = runner.invoke(
            main,
            [],
            input="  \n  search grants  \n  ",
            env={"DIMENSIONS_KEY": "test-key"},
        )
        mock_all_dimcli.Dsl.return_value.query.assert_called_with("search grants")


class TestCLIAuth:
    """Tests for authentication handling."""

    def test_missing_key_exits_code_2(self, runner):
        """Missing API key should exit with code 2."""
        result = runner.invoke(main, ["search grants"], env={})
        assert result.exit_code == EXIT_CONFIG_ERROR
        assert "DIMENSIONS_KEY" in result.output

    def test_key_flag_overrides_env(self, runner):
        """--key flag should override environment variable."""
        with (
            patch("shortwing.config.dimcli") as config_mock,
            patch("shortwing.core.dimcli") as core_mock,
        ):
            mock_dsl = MagicMock()
            mock_dsl.query.return_value.json = {"test": "data"}
            core_mock.Dsl.return_value = mock_dsl

            result = runner.invoke(
                main,
                ["--key", "flag-key", "search grants"],
                env={"DIMENSIONS_KEY": "env-key"},
            )
            config_mock.login.assert_called_once()
            call_kwargs = config_mock.login.call_args[1]
            assert call_kwargs["key"] == "flag-key"


class TestCLIOutput:
    """Tests for output formatting."""

    def test_pretty_output_default(self, runner, mock_all_dimcli):
        """Default output should be pretty-printed."""
        result = runner.invoke(
            main, ["search grants"], env={"DIMENSIONS_KEY": "test-key"}
        )
        assert "\n" in result.output
        assert "  " in result.output  # Indentation

    def test_compact_output(self, runner, mock_all_dimcli):
        """--compact should produce single-line JSON."""
        result = runner.invoke(
            main, ["--compact", "search grants"], env={"DIMENSIONS_KEY": "test-key"}
        )
        # Output should be single line (plus trailing newline from echo)
        lines = result.output.strip().split("\n")
        assert len(lines) == 1


class TestCLISubcommand:
    """Tests for query subcommand."""

    def test_query_subcommand_works(self, runner, mock_all_dimcli):
        """'shortwing query' subcommand should work."""
        result = runner.invoke(
            main, ["query", "search grants"], env={"DIMENSIONS_KEY": "test-key"}
        )
        assert result.exit_code == EXIT_SUCCESS

    def test_query_subcommand_with_options(self, runner, mock_all_dimcli):
        """'shortwing query --compact' should work."""
        result = runner.invoke(
            main,
            ["query", "--compact", "search grants"],
            env={"DIMENSIONS_KEY": "test-key"},
        )
        assert result.exit_code == EXIT_SUCCESS
        lines = result.output.strip().split("\n")
        assert len(lines) == 1


class TestCLIErrors:
    """Tests for error handling."""

    def test_api_error_exits_code_1(self, runner):
        """API error should exit with code 1 and output error JSON."""
        with (
            patch("shortwing.config.dimcli"),
            patch("shortwing.core.dimcli") as core_mock,
        ):
            mock_dsl = MagicMock()
            mock_dsl.query.return_value.json = {
                "error": {"message": "Invalid syntax", "code": 400}
            }
            core_mock.Dsl.return_value = mock_dsl

            result = runner.invoke(
                main, ["bad query"], env={"DIMENSIONS_KEY": "test-key"}
            )
            assert result.exit_code == EXIT_QUERY_ERROR
            assert "error" in result.output

    def test_no_query_shows_usage_error(self, runner):
        """No query provided should show usage error."""
        result = runner.invoke(main, [], env={"DIMENSIONS_KEY": "test-key"})
        assert result.exit_code != EXIT_SUCCESS
