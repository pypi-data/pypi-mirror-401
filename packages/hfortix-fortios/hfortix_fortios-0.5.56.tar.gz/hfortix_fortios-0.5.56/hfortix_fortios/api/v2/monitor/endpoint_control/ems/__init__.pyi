"""Type stubs for EMS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .cert_status import CertStatus, CertStatusDictMode, CertStatusObjectMode
    from .malware_hash import MalwareHash, MalwareHashDictMode, MalwareHashObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode
    from .status_summary import StatusSummary, StatusSummaryDictMode, StatusSummaryObjectMode
    from .unverify_cert import UnverifyCert, UnverifyCertDictMode, UnverifyCertObjectMode
    from .verify_cert import VerifyCert, VerifyCertDictMode, VerifyCertObjectMode

__all__ = [
    "CertStatus",
    "MalwareHash",
    "Status",
    "StatusSummary",
    "UnverifyCert",
    "VerifyCert",
    "EmsDictMode",
    "EmsObjectMode",
]

class EmsDictMode:
    """EMS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    cert_status: CertStatusDictMode
    malware_hash: MalwareHashDictMode
    status: StatusDictMode
    status_summary: StatusSummaryDictMode
    unverify_cert: UnverifyCertDictMode
    verify_cert: VerifyCertDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ems category with HTTP client."""
        ...


class EmsObjectMode:
    """EMS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    cert_status: CertStatusObjectMode
    malware_hash: MalwareHashObjectMode
    status: StatusObjectMode
    status_summary: StatusSummaryObjectMode
    unverify_cert: UnverifyCertObjectMode
    verify_cert: VerifyCertObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ems category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ems:
    """EMS API category."""
    
    cert_status: CertStatus
    malware_hash: MalwareHash
    status: Status
    status_summary: StatusSummary
    unverify_cert: UnverifyCert
    verify_cert: VerifyCert

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ems category with HTTP client."""
        ...
