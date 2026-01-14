"""Type stubs for IPS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .anomaly import Anomaly, AnomalyDictMode, AnomalyObjectMode
    from .hold_signatures import HoldSignatures, HoldSignaturesDictMode, HoldSignaturesObjectMode
    from .metadata import Metadata, MetadataDictMode, MetadataObjectMode
    from .rate_based import RateBased, RateBasedDictMode, RateBasedObjectMode
    from .session import SessionDictMode, SessionObjectMode

__all__ = [
    "Anomaly",
    "HoldSignatures",
    "Metadata",
    "RateBased",
    "IpsDictMode",
    "IpsObjectMode",
]

class IpsDictMode:
    """IPS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    session: SessionDictMode
    anomaly: AnomalyDictMode
    hold_signatures: HoldSignaturesDictMode
    metadata: MetadataDictMode
    rate_based: RateBasedDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ips category with HTTP client."""
        ...


class IpsObjectMode:
    """IPS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    session: SessionObjectMode
    anomaly: AnomalyObjectMode
    hold_signatures: HoldSignaturesObjectMode
    metadata: MetadataObjectMode
    rate_based: RateBasedObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ips category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ips:
    """IPS API category."""
    
    session: Session
    anomaly: Anomaly
    hold_signatures: HoldSignatures
    metadata: Metadata
    rate_based: RateBased

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ips category with HTTP client."""
        ...
