"""Type stubs for DDNS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .lookup import Lookup, LookupDictMode, LookupObjectMode
    from .servers import Servers, ServersDictMode, ServersObjectMode

__all__ = [
    "Lookup",
    "Servers",
    "DdnsDictMode",
    "DdnsObjectMode",
]

class DdnsDictMode:
    """DDNS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    lookup: LookupDictMode
    servers: ServersDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ddns category with HTTP client."""
        ...


class DdnsObjectMode:
    """DDNS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    lookup: LookupObjectMode
    servers: ServersObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ddns category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ddns:
    """DDNS API category."""
    
    lookup: Lookup
    servers: Servers

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ddns category with HTTP client."""
        ...
