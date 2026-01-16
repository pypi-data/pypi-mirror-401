"""Tests for output formatting module."""

from shortwing.output import format_json


class TestFormatJson:
    """Tests for format_json function."""

    def test_pretty_format_default(self):
        """Default format should be pretty-printed."""
        data = {"key": "value"}
        result = format_json(data)
        assert result == '{\n  "key": "value"\n}'

    def test_compact_format(self):
        """Compact format should have no whitespace."""
        data = {"key": "value", "nested": {"a": 1}}
        result = format_json(data, compact=True)
        assert result == '{"key":"value","nested":{"a":1}}'
        assert "\n" not in result
        assert "  " not in result

    def test_empty_dict(self):
        """Should handle empty dictionaries."""
        assert format_json({}) == "{}"
        assert format_json({}, compact=True) == "{}"

    def test_list_values(self):
        """Should handle list values."""
        data = {"items": [1, 2, 3]}
        result = format_json(data, compact=True)
        assert result == '{"items":[1,2,3]}'
