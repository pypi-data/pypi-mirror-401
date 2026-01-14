"""Type stubs for LOCAL_REPORT category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .delete import Delete, DeleteDictMode, DeleteObjectMode
    from .download import Download, DownloadDictMode, DownloadObjectMode

__all__ = [
    "Delete",
    "Download",
    "LocalReportDictMode",
    "LocalReportObjectMode",
]

class LocalReportDictMode:
    """LOCAL_REPORT API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    delete: DeleteDictMode
    download: DownloadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local_report category with HTTP client."""
        ...


class LocalReportObjectMode:
    """LOCAL_REPORT API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    delete: DeleteObjectMode
    download: DownloadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local_report category with HTTP client."""
        ...


# Base class for backwards compatibility
class LocalReport:
    """LOCAL_REPORT API category."""
    
    delete: Delete
    download: Download

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local_report category with HTTP client."""
        ...
