"""Type stubs for SNIFFER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .delete import Delete, DeleteDictMode, DeleteObjectMode
    from .download import Download, DownloadDictMode, DownloadObjectMode
    from .list import List, ListDictMode, ListObjectMode
    from .meta import Meta, MetaDictMode, MetaObjectMode
    from .start import Start, StartDictMode, StartObjectMode
    from .stop import Stop, StopDictMode, StopObjectMode

__all__ = [
    "Delete",
    "Download",
    "List",
    "Meta",
    "Start",
    "Stop",
    "SnifferDictMode",
    "SnifferObjectMode",
]

class SnifferDictMode:
    """SNIFFER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    delete: DeleteDictMode
    download: DownloadDictMode
    list: ListDictMode
    meta: MetaDictMode
    start: StartDictMode
    stop: StopDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sniffer category with HTTP client."""
        ...


class SnifferObjectMode:
    """SNIFFER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    delete: DeleteObjectMode
    download: DownloadObjectMode
    list: ListObjectMode
    meta: MetaObjectMode
    start: StartObjectMode
    stop: StopObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sniffer category with HTTP client."""
        ...


# Base class for backwards compatibility
class Sniffer:
    """SNIFFER API category."""
    
    delete: Delete
    download: Download
    list: List
    meta: Meta
    start: Start
    stop: Stop

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sniffer category with HTTP client."""
        ...
