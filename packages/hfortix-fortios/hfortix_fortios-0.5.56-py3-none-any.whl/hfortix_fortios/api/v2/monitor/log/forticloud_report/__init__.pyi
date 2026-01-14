"""Type stubs for FORTICLOUD_REPORT category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .download import Download, DownloadDictMode, DownloadObjectMode

__all__ = [
    "Download",
    "ForticloudReportDictMode",
    "ForticloudReportObjectMode",
]

class ForticloudReportDictMode:
    """FORTICLOUD_REPORT API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    download: DownloadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticloud_report category with HTTP client."""
        ...


class ForticloudReportObjectMode:
    """FORTICLOUD_REPORT API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    download: DownloadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticloud_report category with HTTP client."""
        ...


# Base class for backwards compatibility
class ForticloudReport:
    """FORTICLOUD_REPORT API category."""
    
    download: Download

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticloud_report category with HTTP client."""
        ...
