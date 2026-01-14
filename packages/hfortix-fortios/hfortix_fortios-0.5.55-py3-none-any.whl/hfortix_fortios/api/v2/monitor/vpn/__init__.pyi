"""Type stubs for VPN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .ike import IkeDictMode, IkeObjectMode
    from .ipsec import Ipsec
    from .ssl import Ssl

__all__ = [
    "VpnDictMode",
    "VpnObjectMode",
]

class VpnDictMode:
    """VPN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ike: IkeDictMode
    ipsec: Ipsec
    ssl: Ssl

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn category with HTTP client."""
        ...


class VpnObjectMode:
    """VPN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ike: IkeObjectMode
    ipsec: Ipsec
    ssl: Ssl

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn category with HTTP client."""
        ...


# Base class for backwards compatibility
class Vpn:
    """VPN API category."""
    
    ike: Ike
    ipsec: Ipsec
    ssl: Ssl

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn category with HTTP client."""
        ...
