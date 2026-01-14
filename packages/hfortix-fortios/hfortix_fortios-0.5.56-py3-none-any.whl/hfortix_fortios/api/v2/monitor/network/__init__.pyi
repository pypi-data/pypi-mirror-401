"""Type stubs for NETWORK category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .arp import Arp, ArpDictMode, ArpObjectMode
    from .reverse_ip_lookup import ReverseIpLookup, ReverseIpLookupDictMode, ReverseIpLookupObjectMode
    from .ddns import DdnsDictMode, DdnsObjectMode
    from .debug_flow import DebugFlow
    from .dns import DnsDictMode, DnsObjectMode
    from .fortiguard import FortiguardDictMode, FortiguardObjectMode
    from .lldp import LldpDictMode, LldpObjectMode

__all__ = [
    "Arp",
    "ReverseIpLookup",
    "NetworkDictMode",
    "NetworkObjectMode",
]

class NetworkDictMode:
    """NETWORK API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ddns: DdnsDictMode
    debug_flow: DebugFlow
    dns: DnsDictMode
    fortiguard: FortiguardDictMode
    lldp: LldpDictMode
    arp: ArpDictMode
    reverse_ip_lookup: ReverseIpLookupDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize network category with HTTP client."""
        ...


class NetworkObjectMode:
    """NETWORK API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ddns: DdnsObjectMode
    debug_flow: DebugFlow
    dns: DnsObjectMode
    fortiguard: FortiguardObjectMode
    lldp: LldpObjectMode
    arp: ArpObjectMode
    reverse_ip_lookup: ReverseIpLookupObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize network category with HTTP client."""
        ...


# Base class for backwards compatibility
class Network:
    """NETWORK API category."""
    
    ddns: Ddns
    debug_flow: DebugFlow
    dns: Dns
    fortiguard: Fortiguard
    lldp: Lldp
    arp: Arp
    reverse_ip_lookup: ReverseIpLookup

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize network category with HTTP client."""
        ...
