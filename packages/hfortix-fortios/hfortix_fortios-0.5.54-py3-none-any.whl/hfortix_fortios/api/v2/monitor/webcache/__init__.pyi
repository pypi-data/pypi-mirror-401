"""Type stubs for WEBCACHE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .stats import Stats

__all__ = [
    "WebcacheDictMode",
    "WebcacheObjectMode",
]

class WebcacheDictMode:
    """WEBCACHE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    stats: Stats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webcache category with HTTP client."""
        ...


class WebcacheObjectMode:
    """WEBCACHE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    stats: Stats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webcache category with HTTP client."""
        ...


# Base class for backwards compatibility
class Webcache:
    """WEBCACHE API category."""
    
    stats: Stats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webcache category with HTTP client."""
        ...
