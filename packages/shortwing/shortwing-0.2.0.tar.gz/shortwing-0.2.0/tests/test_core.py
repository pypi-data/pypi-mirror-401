"""Tests for core query execution module."""

from unittest.mock import MagicMock, patch

import pytest

from shortwing.core import execute_query
from shortwing.exceptions import QueryError


class TestExecuteQuery:
    """Tests for execute_query function."""

    def test_returns_json_response(self, mock_dimcli):
        """Should return the raw JSON from dimcli response."""
        result = execute_query("search grants return grants")
        assert "researchers" in result
        assert "_stats" in result

    def test_passes_query_verbatim(self, mock_dimcli):
        """Query should be passed unchanged to dimcli."""
        query = '  search grants for "test"  '
        execute_query(query)
        mock_dimcli.Dsl.return_value.query.assert_called_once_with(query)

    def test_wraps_exceptions_as_query_error(self):
        """Should wrap dimcli exceptions as QueryError."""
        with patch("shortwing.core.dimcli") as mock:
            mock.Dsl.return_value.query.side_effect = Exception("API Error")
            with pytest.raises(QueryError) as exc_info:
                execute_query("test")
            assert "API Error" in str(exc_info.value)

    def test_preserves_error_response(self, mock_dimcli_error):
        """Should return error response as-is."""
        result = execute_query("bad query")
        assert "error" in result
        assert result["error"]["code"] == 400
