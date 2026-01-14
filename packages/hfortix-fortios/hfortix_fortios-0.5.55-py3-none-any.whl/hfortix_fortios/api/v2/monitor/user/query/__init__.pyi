"""Type stubs for QUERY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .abort import Abort, AbortDictMode, AbortObjectMode

__all__ = [
    "Abort",
    "QueryDictMode",
    "QueryObjectMode",
]

class QueryDictMode:
    """QUERY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    abort: AbortDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize query category with HTTP client."""
        ...


class QueryObjectMode:
    """QUERY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    abort: AbortObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize query category with HTTP client."""
        ...


# Base class for backwards compatibility
class Query:
    """QUERY API category."""
    
    abort: Abort

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize query category with HTTP client."""
        ...
