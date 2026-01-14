"""
FortiOS LOG API - Search

Log query endpoints for search logs.

Note: LOG endpoints are read-only (GET only) and return log data.
They accept path parameters that are represented as nested classes.

Example Usage:
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient


class Search:
    """Search log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize Search endpoint."""
        self._client = client
        self.status = SearchStatus(client)


class SearchStatus:
    """SearchStatus log operations."""

    def __init__(self, client: "IHTTPClient"):
        """Initialize SearchStatus."""
        self._client = client
