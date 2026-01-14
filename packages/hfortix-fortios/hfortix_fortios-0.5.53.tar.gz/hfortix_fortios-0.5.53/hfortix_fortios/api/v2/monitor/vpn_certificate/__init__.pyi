"""Type stubs for VPN_CERTIFICATE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .cert_name_available import CertNameAvailable, CertNameAvailableDictMode, CertNameAvailableObjectMode
    from .ca import CaDictMode, CaObjectMode
    from .crl import CrlDictMode, CrlObjectMode
    from .csr import CsrDictMode, CsrObjectMode
    from .local import LocalDictMode, LocalObjectMode
    from .remote import RemoteDictMode, RemoteObjectMode

__all__ = [
    "CertNameAvailable",
    "VpnCertificateDictMode",
    "VpnCertificateObjectMode",
]

class VpnCertificateDictMode:
    """VPN_CERTIFICATE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ca: CaDictMode
    crl: CrlDictMode
    csr: CsrDictMode
    local: LocalDictMode
    remote: RemoteDictMode
    cert_name_available: CertNameAvailableDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn_certificate category with HTTP client."""
        ...


class VpnCertificateObjectMode:
    """VPN_CERTIFICATE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ca: CaObjectMode
    crl: CrlObjectMode
    csr: CsrObjectMode
    local: LocalObjectMode
    remote: RemoteObjectMode
    cert_name_available: CertNameAvailableObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn_certificate category with HTTP client."""
        ...


# Base class for backwards compatibility
class VpnCertificate:
    """VPN_CERTIFICATE API category."""
    
    ca: Ca
    crl: Crl
    csr: Csr
    local: Local
    remote: Remote
    cert_name_available: CertNameAvailable

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vpn_certificate category with HTTP client."""
        ...
