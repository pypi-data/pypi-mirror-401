"""Type stubs for SHAPER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .per_ip_shaper import PerIpShaper, PerIpShaperDictMode, PerIpShaperObjectMode
    from .traffic_shaper import TrafficShaper, TrafficShaperDictMode, TrafficShaperObjectMode

__all__ = [
    "PerIpShaper",
    "TrafficShaper",
    "ShaperDictMode",
    "ShaperObjectMode",
]

class ShaperDictMode:
    """SHAPER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    per_ip_shaper: PerIpShaperDictMode
    traffic_shaper: TrafficShaperDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize shaper category with HTTP client."""
        ...


class ShaperObjectMode:
    """SHAPER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    per_ip_shaper: PerIpShaperObjectMode
    traffic_shaper: TrafficShaperObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize shaper category with HTTP client."""
        ...


# Base class for backwards compatibility
class Shaper:
    """SHAPER API category."""
    
    per_ip_shaper: PerIpShaper
    traffic_shaper: TrafficShaper

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize shaper category with HTTP client."""
        ...
