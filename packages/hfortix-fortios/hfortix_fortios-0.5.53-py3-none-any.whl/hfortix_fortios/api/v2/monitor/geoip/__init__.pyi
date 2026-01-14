"""Type stubs for GEOIP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .geoip_query import GeoipQuery

__all__ = [
    "GeoipDictMode",
    "GeoipObjectMode",
]

class GeoipDictMode:
    """GEOIP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    geoip_query: GeoipQuery

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize geoip category with HTTP client."""
        ...


class GeoipObjectMode:
    """GEOIP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    geoip_query: GeoipQuery

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize geoip category with HTTP client."""
        ...


# Base class for backwards compatibility
class Geoip:
    """GEOIP API category."""
    
    geoip_query: GeoipQuery

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize geoip category with HTTP client."""
        ...
