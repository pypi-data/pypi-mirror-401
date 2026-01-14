"""Type stubs for SDWAN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .link_monitor_metrics import LinkMonitorMetrics

__all__ = [
    "SdwanDictMode",
    "SdwanObjectMode",
]

class SdwanDictMode:
    """SDWAN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    link_monitor_metrics: LinkMonitorMetrics

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdwan category with HTTP client."""
        ...


class SdwanObjectMode:
    """SDWAN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    link_monitor_metrics: LinkMonitorMetrics

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdwan category with HTTP client."""
        ...


# Base class for backwards compatibility
class Sdwan:
    """SDWAN API category."""
    
    link_monitor_metrics: LinkMonitorMetrics

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdwan category with HTTP client."""
        ...
