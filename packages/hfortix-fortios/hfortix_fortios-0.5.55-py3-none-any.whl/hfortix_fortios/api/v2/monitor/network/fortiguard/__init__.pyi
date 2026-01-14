"""Type stubs for FORTIGUARD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .live_services_latency import LiveServicesLatency, LiveServicesLatencyDictMode, LiveServicesLatencyObjectMode

__all__ = [
    "LiveServicesLatency",
    "FortiguardDictMode",
    "FortiguardObjectMode",
]

class FortiguardDictMode:
    """FORTIGUARD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    live_services_latency: LiveServicesLatencyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


class FortiguardObjectMode:
    """FORTIGUARD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    live_services_latency: LiveServicesLatencyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fortiguard:
    """FORTIGUARD API category."""
    
    live_services_latency: LiveServicesLatency

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...
