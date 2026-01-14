"""Type stubs for IPAM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .list import List, ListDictMode, ListObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode
    from .utilization import Utilization, UtilizationDictMode, UtilizationObjectMode

__all__ = [
    "List",
    "Status",
    "Utilization",
    "IpamDictMode",
    "IpamObjectMode",
]

class IpamDictMode:
    """IPAM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    list: ListDictMode
    status: StatusDictMode
    utilization: UtilizationDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipam category with HTTP client."""
        ...


class IpamObjectMode:
    """IPAM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    list: ListObjectMode
    status: StatusObjectMode
    utilization: UtilizationObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipam category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ipam:
    """IPAM API category."""
    
    list: List
    status: Status
    utilization: Utilization

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipam category with HTTP client."""
        ...
