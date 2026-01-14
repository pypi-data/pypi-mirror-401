"""Type stubs for SDWAN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .routes import Routes, RoutesDictMode, RoutesObjectMode
    from .routes6 import Routes6, Routes6DictMode, Routes6ObjectMode
    from .routes_statistics import RoutesStatistics, RoutesStatisticsDictMode, RoutesStatisticsObjectMode

__all__ = [
    "Routes",
    "Routes6",
    "RoutesStatistics",
    "SdwanDictMode",
    "SdwanObjectMode",
]

class SdwanDictMode:
    """SDWAN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    routes: RoutesDictMode
    routes6: Routes6DictMode
    routes_statistics: RoutesStatisticsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdwan category with HTTP client."""
        ...


class SdwanObjectMode:
    """SDWAN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    routes: RoutesObjectMode
    routes6: Routes6ObjectMode
    routes_statistics: RoutesStatisticsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdwan category with HTTP client."""
        ...


# Base class for backwards compatibility
class Sdwan:
    """SDWAN API category."""
    
    routes: Routes
    routes6: Routes6
    routes_statistics: RoutesStatistics

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdwan category with HTTP client."""
        ...
