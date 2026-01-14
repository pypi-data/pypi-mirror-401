"""Type stubs for OSPF category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .neighbors import Neighbors, NeighborsDictMode, NeighborsObjectMode

__all__ = [
    "Neighbors",
    "OspfDictMode",
    "OspfObjectMode",
]

class OspfDictMode:
    """OSPF API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    neighbors: NeighborsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ospf category with HTTP client."""
        ...


class OspfObjectMode:
    """OSPF API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    neighbors: NeighborsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ospf category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ospf:
    """OSPF API category."""
    
    neighbors: Neighbors

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ospf category with HTTP client."""
        ...
