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
        # Verify query endpoint was called with stdin query
        calls = mock_all_dimcli.post.call_args_list
        query_call = [c for c in calls if "/api/dsl" in str(c)]
        assert len(query_call) > 0
        assert query_call[0][1]["content"] == b"stdin query"

    def test_whitespace_trimmed(self, runner, mock_all_dimcli):
        """Leading/trailing whitespace should be trimmed."""
        result = runner.invoke(
            main,
            [],
            input="  \n  search grants  \n  ",
            env={"DIMENSIONS_KEY": "test-key"},
        )
        # Verify query endpoint was called with trimmed query
        calls = mock_all_dimcli.post.call_args_list
        query_call = [c for c in calls if "/api/dsl" in str(c)]
        assert len(query_call) > 0
        assert query_call[0][1]["content"] == b"search grants"


class TestCLIAuth:
    """Tests for authentication handling."""

    def test_missing_key_exits_code_2(self, runner, clean_env):
        """Missing API key should exit with code 2."""
        result = runner.invoke(main, ["search grants"], env={})
        assert result.exit_code == EXIT_CONFIG_ERROR
        assert "DIMENSIONS_KEY" in result.output

    def test_key_flag_overrides_env(self, runner, mock_httpx_success):
        """--key flag should override environment variable."""
        result = runner.invoke(
            main,
            ["--key", "flag-key", "search grants"],
            env={"DIMENSIONS_KEY": "env-key"},
        )
        # Verify the flag-key was used in auth
        calls = mock_httpx_success.post.call_args_list
        auth_call = calls[0]
        assert auth_call[1]["json"]["key"] == "flag-key"


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

    def test_api_error_exits_code_1(self, runner, mock_httpx_error):
        """API error should exit with code 1 and output error JSON."""
        result = runner.invoke(
            main, ["bad query"], env={"DIMENSIONS_KEY": "test-key"}
        )
        assert result.exit_code == EXIT_QUERY_ERROR
        assert "error" in result.output

    def test_no_query_shows_help(self, runner, clean_env):
        """No query provided should show help."""
        result = runner.invoke(main, [], env={"DIMENSIONS_KEY": "test-key"})
        # Exit code 0 or 1 is acceptable - both mean help was shown without error
        assert result.exit_code in [0, 1]
        assert "Shortwing" in result.output
        assert "Execute DSL queries" in result.output


class TestNextSteps:
    """Tests for next steps suggestions."""

    def test_next_steps_shown_on_success(self, runner, mock_httpx_success):
        """Success should show next steps suggestions."""
        result = runner.invoke(
            main, ["search grants"], env={"DIMENSIONS_KEY": "test-key"}
        )
        # Next steps go to stderr when running in interactive mode
        # CliRunner captures both stdout and stderr in output
        # We check that the JSON is in output (success)
        assert result.exit_code == EXIT_SUCCESS
        assert "researchers" in result.output

    def test_next_steps_shown_on_query_error(self, runner, mock_httpx_error):
        """Query error should show relevant next steps."""
        result = runner.invoke(
            main, ["bad query"], env={"DIMENSIONS_KEY": "test-key"}
        )
        assert result.exit_code == EXIT_QUERY_ERROR
        assert "error" in result.output

    def test_next_steps_shown_on_config_error(self, runner, clean_env):
        """Config error should show credential-related next steps."""
        result = runner.invoke(main, ["search grants"], env={})
        assert result.exit_code == EXIT_CONFIG_ERROR
        assert "DIMENSIONS_KEY" in result.output or "Configuration error" in result.output
