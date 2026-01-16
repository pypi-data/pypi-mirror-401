"""Exit codes and exceptions for Shortwing CLI."""

# Exit codes as constants
EXIT_SUCCESS = 0
EXIT_QUERY_ERROR = 1
EXIT_CONFIG_ERROR = 2


class ShortwingError(Exception):
    """Base exception for Shortwing."""

    exit_code: int = EXIT_QUERY_ERROR


class ConfigurationError(ShortwingError):
    """Raised when configuration/authentication fails."""

    exit_code = EXIT_CONFIG_ERROR


class QueryError(ShortwingError):
    """Raised when query execution fails."""

    exit_code = EXIT_QUERY_ERROR
