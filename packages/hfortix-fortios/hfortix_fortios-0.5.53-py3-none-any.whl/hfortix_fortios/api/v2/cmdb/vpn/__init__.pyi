"""Type stubs for VPN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .kmip_server import KmipServer, KmipServerDictMode, KmipServerObjectMode
    from .l2tp import L2tp, L2tpDictMode, L2tpObjectMode
    from .pptp import Pptp, PptpDictMode, PptpObjectMode
    from .qkd import Qkd, QkdDictMode, QkdObjectMode
    from .certificate import CertificateDictMode, CertificateObjectMode
    from .ipsec import IpsecDictMode, IpsecObjectMode

__all__ = [
    "KmipServer",
    "L2tp",
    "Pptp",
    "Qkd",
    "VpnDictMode",
    "VpnObjectMode",
]

class VpnDictMode:
    """VPN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    certificate: CertificateDictMode
    ipsec: IpsecDictMode
    kmip_server: KmipServerDictMode
    l2tp: L2tpDictMode
    pptp: PptpDictMode
    qkd: QkdDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn category with HTTP client."""
        ...


class VpnObjectMode:
    """VPN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    certificate: CertificateObjectMode
    ipsec: IpsecObjectMode
    kmip_server: KmipServerObjectMode
    l2tp: L2tpObjectMode
    pptp: PptpObjectMode
    qkd: QkdObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn category with HTTP client."""
        ...


# Base class for backwards compatibility
class Vpn:
    """VPN API category."""
    
    certificate: Certificate
    ipsec: Ipsec
    kmip_server: KmipServer
    l2tp: L2tp
    pptp: Pptp
    qkd: Qkd

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn category with HTTP client."""
        ...
