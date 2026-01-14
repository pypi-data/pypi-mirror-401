"""Type stubs for CERTIFICATE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .ca import Ca, CaDictMode, CaObjectMode
    from .crl import Crl, CrlDictMode, CrlObjectMode
    from .hsm_local import HsmLocal, HsmLocalDictMode, HsmLocalObjectMode
    from .local import Local, LocalDictMode, LocalObjectMode
    from .ocsp_server import OcspServer, OcspServerDictMode, OcspServerObjectMode
    from .remote import Remote, RemoteDictMode, RemoteObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Ca",
    "Crl",
    "HsmLocal",
    "Local",
    "OcspServer",
    "Remote",
    "Setting",
    "CertificateDictMode",
    "CertificateObjectMode",
]

class CertificateDictMode:
    """CERTIFICATE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ca: CaDictMode
    crl: CrlDictMode
    hsm_local: HsmLocalDictMode
    local: LocalDictMode
    ocsp_server: OcspServerDictMode
    remote: RemoteDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize certificate category with HTTP client."""
        ...


class CertificateObjectMode:
    """CERTIFICATE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ca: CaObjectMode
    crl: CrlObjectMode
    hsm_local: HsmLocalObjectMode
    local: LocalObjectMode
    ocsp_server: OcspServerObjectMode
    remote: RemoteObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize certificate category with HTTP client."""
        ...


# Base class for backwards compatibility
class Certificate:
    """CERTIFICATE API category."""
    
    ca: Ca
    crl: Crl
    hsm_local: HsmLocal
    local: Local
    ocsp_server: OcspServer
    remote: Remote
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize certificate category with HTTP client."""
        ...
