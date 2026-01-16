"""Output formatting utilities."""

import json
from typing import Any


def format_json(data: dict[str, Any], compact: bool = False) -> str:
    """
    Format JSON data for output.

    Args:
        data: The data to format
        compact: If True, output single-line JSON

    Returns:
        Formatted JSON string
    """
    if compact:
        return json.dumps(data, separators=(",", ":"))
    return json.dumps(data, indent=2)
