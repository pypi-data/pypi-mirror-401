"""Type stubs for LINK_MONITOR_METRICS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .report import Report, ReportDictMode, ReportObjectMode

__all__ = [
    "Report",
    "LinkMonitorMetricsDictMode",
    "LinkMonitorMetricsObjectMode",
]

class LinkMonitorMetricsDictMode:
    """LINK_MONITOR_METRICS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    report: ReportDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize link_monitor_metrics category with HTTP client."""
        ...


class LinkMonitorMetricsObjectMode:
    """LINK_MONITOR_METRICS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    report: ReportObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize link_monitor_metrics category with HTTP client."""
        ...


# Base class for backwards compatibility
class LinkMonitorMetrics:
    """LINK_MONITOR_METRICS API category."""
    
    report: Report

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize link_monitor_metrics category with HTTP client."""
        ...
