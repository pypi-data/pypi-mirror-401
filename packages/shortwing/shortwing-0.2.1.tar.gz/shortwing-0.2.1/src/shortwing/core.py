"""Async core query execution logic."""

from typing import Any

import httpx

from shortwing.exceptions import QueryError

# Module-level token cache
_cached_token: str | None = None
_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    """Get or create async HTTP client singleton."""
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
        )
    return _client


async def authenticate(api_key: str, endpoint: str) -> str:
    """
    Authenticate with Dimensions API and get JWT token.

    Caches token in module-level variable for reuse.
    Token is valid for ~2 hours.

    Args:
        api_key: The API key
        endpoint: Base API endpoint (e.g., https://app.dimensions.ai)

    Returns:
        JWT token string

    Raises:
        QueryError: If authentication fails
    """
    global _cached_token

    # Return cached token if available
    # TODO: Add token expiry tracking (tokens valid ~2 hours)
    if _cached_token:
        return _cached_token

    client = await get_client()
    auth_url = f"{endpoint.rstrip('/')}/api/auth"

    try:
        response = await client.post(
            auth_url,
            json={"key": api_key},
        )
        response.raise_for_status()
        data = response.json()
        _cached_token = data["token"]
        return _cached_token
    except Exception as e:
        raise QueryError(f"Authentication failed: {e}") from e


async def execute_query(query: str, api_key: str, endpoint: str) -> dict[str, Any]:
    """
    Execute a DSL query using async HTTP.

    Args:
        query: The DSL query string
        api_key: API key for authentication
        endpoint: Base API endpoint

    Returns:
        The raw JSON response dictionary

    Raises:
        QueryError: If the query fails
    """
    try:
        # Get JWT token
        token = await authenticate(api_key, endpoint)

        # Execute query
        client = await get_client()
        query_url = f"{endpoint.rstrip('/')}/api/dsl/v2"

        response = await client.post(
            query_url,
            content=query.encode("utf-8"),
            headers={
                "Authorization": f"JWT {token}",
                "Content-Type": "text/plain",
            },
        )
        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        # Try to extract error from response JSON
        try:
            error_data = e.response.json()
            if "error" in error_data:
                return error_data  # Return error JSON for consistent handling
        except Exception:
            pass
        raise QueryError(f"HTTP {e.response.status_code}: {e}") from e
    except Exception as e:
        raise QueryError(str(e)) from e


async def close_client():
    """Close the async HTTP client. Call on shutdown."""
    global _client
    if _client:
        await _client.aclose()
        _client = None
