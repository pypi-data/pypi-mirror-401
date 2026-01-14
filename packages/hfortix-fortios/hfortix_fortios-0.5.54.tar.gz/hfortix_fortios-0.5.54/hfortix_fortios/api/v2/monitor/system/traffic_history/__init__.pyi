"""Type stubs for TRAFFIC_HISTORY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .enable_app_bandwidth_tracking import EnableAppBandwidthTracking, EnableAppBandwidthTrackingDictMode, EnableAppBandwidthTrackingObjectMode
    from .interface import Interface, InterfaceDictMode, InterfaceObjectMode
    from .top_applications import TopApplications, TopApplicationsDictMode, TopApplicationsObjectMode

__all__ = [
    "EnableAppBandwidthTracking",
    "Interface",
    "TopApplications",
    "TrafficHistoryDictMode",
    "TrafficHistoryObjectMode",
]

class TrafficHistoryDictMode:
    """TRAFFIC_HISTORY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    enable_app_bandwidth_tracking: EnableAppBandwidthTrackingDictMode
    interface: InterfaceDictMode
    top_applications: TopApplicationsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize traffic_history category with HTTP client."""
        ...


class TrafficHistoryObjectMode:
    """TRAFFIC_HISTORY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    enable_app_bandwidth_tracking: EnableAppBandwidthTrackingObjectMode
    interface: InterfaceObjectMode
    top_applications: TopApplicationsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize traffic_history category with HTTP client."""
        ...


# Base class for backwards compatibility
class TrafficHistory:
    """TRAFFIC_HISTORY API category."""
    
    enable_app_bandwidth_tracking: EnableAppBandwidthTracking
    interface: Interface
    top_applications: TopApplications

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize traffic_history category with HTTP client."""
        ...
