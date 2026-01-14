"""Type stubs for NETWORK category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .connect import Connect, ConnectDictMode, ConnectObjectMode
    from .list import List, ListDictMode, ListObjectMode
    from .scan import Scan, ScanDictMode, ScanObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode

__all__ = [
    "Connect",
    "List",
    "Scan",
    "Status",
    "NetworkDictMode",
    "NetworkObjectMode",
]

class NetworkDictMode:
    """NETWORK API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    connect: ConnectDictMode
    list: ListDictMode
    scan: ScanDictMode
    status: StatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize network category with HTTP client."""
        ...


class NetworkObjectMode:
    """NETWORK API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    connect: ConnectObjectMode
    list: ListObjectMode
    scan: ScanObjectMode
    status: StatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize network category with HTTP client."""
        ...


# Base class for backwards compatibility
class Network:
    """NETWORK API category."""
    
    connect: Connect
    list: List
    scan: Scan
    status: Status

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize network category with HTTP client."""
        ...
