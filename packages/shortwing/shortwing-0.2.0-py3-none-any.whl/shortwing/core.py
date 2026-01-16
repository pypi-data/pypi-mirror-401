"""Core query execution logic."""

from typing import Any

import dimcli

from shortwing.exceptions import QueryError


def execute_query(query: str) -> dict[str, Any]:
    """
    Execute a DSL query and return the JSON response.

    Args:
        query: The DSL query string (passed verbatim)

    Returns:
        The raw JSON response dictionary

    Raises:
        QueryError: If the query fails
    """
    try:
        dsl = dimcli.Dsl()
        result = dsl.query(query)
        return result.json
    except Exception as e:
        raise QueryError(str(e)) from e
