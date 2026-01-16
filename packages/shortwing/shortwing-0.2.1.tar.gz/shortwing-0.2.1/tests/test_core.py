"""Tests for core query execution module."""

import pytest

from shortwing.core import execute_query
from shortwing.exceptions import QueryError


class TestExecuteQuery:
    """Tests for execute_query function."""

    @pytest.mark.asyncio
    async def test_returns_json_response(self, mock_httpx_success):
        """Should return the raw JSON from API response."""
        result = await execute_query(
            "search grants return grants",
            "test-api-key",
            "https://app.dimensions.ai",
        )
        assert "researchers" in result
        assert "_stats" in result

    @pytest.mark.asyncio
    async def test_authenticates_with_jwt(self, mock_httpx_success):
        """Should authenticate and get JWT token."""
        await execute_query(
            "search grants", "test-api-key", "https://app.dimensions.ai"
        )

        # Verify auth endpoint was called
        calls = mock_httpx_success.post.call_args_list
        auth_call = calls[0]
        assert "/api/auth" in auth_call[0][0]
        assert auth_call[1]["json"] == {"key": "test-api-key"}

    @pytest.mark.asyncio
    async def test_sends_query_to_dsl_endpoint(self, mock_httpx_success):
        """Should send query to DSL endpoint with JWT token."""
        query = "search grants return grants"
        await execute_query(query, "test-api-key", "https://app.dimensions.ai")

        # Verify query endpoint was called
        calls = mock_httpx_success.post.call_args_list
        query_call = calls[1]
        assert "/api/dsl/v2" in query_call[0][0]
        assert query_call[1]["content"] == query.encode("utf-8")
        assert query_call[1]["headers"]["Authorization"] == "JWT test-jwt-token"

    @pytest.mark.asyncio
    async def test_preserves_error_response(self, mock_httpx_error):
        """Should return error response as-is."""
        result = await execute_query(
            "bad query", "test-api-key", "https://app.dimensions.ai"
        )
        assert "error" in result
        assert result["error"]["code"] == 400
