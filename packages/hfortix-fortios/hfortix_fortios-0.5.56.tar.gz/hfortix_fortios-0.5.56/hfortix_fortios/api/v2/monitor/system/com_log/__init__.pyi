"""Type stubs for COM_LOG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .download import Download, DownloadDictMode, DownloadObjectMode
    from .dump import Dump, DumpDictMode, DumpObjectMode
    from .update import Update, UpdateDictMode, UpdateObjectMode

__all__ = [
    "Download",
    "Dump",
    "Update",
    "ComLogDictMode",
    "ComLogObjectMode",
]

class ComLogDictMode:
    """COM_LOG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    download: DownloadDictMode
    dump: DumpDictMode
    update: UpdateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize com_log category with HTTP client."""
        ...


class ComLogObjectMode:
    """COM_LOG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    download: DownloadObjectMode
    dump: DumpObjectMode
    update: UpdateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize com_log category with HTTP client."""
        ...


# Base class for backwards compatibility
class ComLog:
    """COM_LOG API category."""
    
    download: Download
    dump: Dump
    update: Update

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize com_log category with HTTP client."""
        ...
