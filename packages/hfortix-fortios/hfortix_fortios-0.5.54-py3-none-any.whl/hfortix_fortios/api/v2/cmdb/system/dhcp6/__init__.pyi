"""Type stubs for DHCP6 category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .server import Server, ServerDictMode, ServerObjectMode

__all__ = [
    "Server",
    "Dhcp6DictMode",
    "Dhcp6ObjectMode",
]

class Dhcp6DictMode:
    """DHCP6 API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    server: ServerDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dhcp6 category with HTTP client."""
        ...


class Dhcp6ObjectMode:
    """DHCP6 API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    server: ServerObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dhcp6 category with HTTP client."""
        ...


# Base class for backwards compatibility
class Dhcp6:
    """DHCP6 API category."""
    
    server: Server

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dhcp6 category with HTTP client."""
        ...
