"""Type stubs for CERTIFICATE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .download import Download, DownloadDictMode, DownloadObjectMode
    from .read_info import ReadInfo, ReadInfoDictMode, ReadInfoObjectMode

__all__ = [
    "Download",
    "ReadInfo",
    "CertificateDictMode",
    "CertificateObjectMode",
]

class CertificateDictMode:
    """CERTIFICATE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    download: DownloadDictMode
    read_info: ReadInfoDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize certificate category with HTTP client."""
        ...


class CertificateObjectMode:
    """CERTIFICATE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    download: DownloadObjectMode
    read_info: ReadInfoObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize certificate category with HTTP client."""
        ...


# Base class for backwards compatibility
class Certificate:
    """CERTIFICATE API category."""
    
    download: Download
    read_info: ReadInfo

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize certificate category with HTTP client."""
        ...
