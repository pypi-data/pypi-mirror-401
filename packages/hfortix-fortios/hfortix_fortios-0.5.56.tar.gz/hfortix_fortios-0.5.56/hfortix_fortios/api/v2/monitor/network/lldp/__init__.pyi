"""Type stubs for LLDP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .neighbors import Neighbors, NeighborsDictMode, NeighborsObjectMode
    from .ports import Ports, PortsDictMode, PortsObjectMode

__all__ = [
    "Neighbors",
    "Ports",
    "LldpDictMode",
    "LldpObjectMode",
]

class LldpDictMode:
    """LLDP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    neighbors: NeighborsDictMode
    ports: PortsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lldp category with HTTP client."""
        ...


class LldpObjectMode:
    """LLDP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    neighbors: NeighborsObjectMode
    ports: PortsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lldp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Lldp:
    """LLDP API category."""
    
    neighbors: Neighbors
    ports: Ports

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lldp category with HTTP client."""
        ...
