"""
Data conversion and cleaning helpers for FortiOS API.

Provides utilities for:
- Type conversion (bool to enable/disable)
- Data filtering and cleaning
"""

from typing import Any


def convert_boolean_to_str(value: bool | str | int | None) -> str | None:
    """
    Convert Python boolean to FortiOS enable/disable string.

    FortiOS API typically uses 'enable'/'disable' instead of true/false.

    Args:
        value: Boolean, string, or None

    Returns:
        'enable', 'disable', the original string, or None
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return "enable" if value else "disable"
    return str(value)


def filter_empty_values(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Remove None values and empty collections from payload.

    Useful for cleaning up payloads before sending to FortiOS API,
    which may reject empty lists or None values in certain contexts.

    Args:
        payload: Dictionary to clean

    Returns:
        Dictionary with None and empty values removed
    """
    cleaned: dict[str, Any] = {}

    for key, value in payload.items():
        # Skip None values
        if value is None:
            continue

        # Skip empty lists and dicts
        if isinstance(value, (list, dict)) and not value:
            continue

        cleaned[key] = value

    return cleaned
