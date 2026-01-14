"""Type stubs for FTP_PROXY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .explicit import Explicit, ExplicitDictMode, ExplicitObjectMode

__all__ = [
    "Explicit",
    "FtpProxyDictMode",
    "FtpProxyObjectMode",
]

class FtpProxyDictMode:
    """FTP_PROXY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    explicit: ExplicitDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ftp_proxy category with HTTP client."""
        ...


class FtpProxyObjectMode:
    """FTP_PROXY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    explicit: ExplicitObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ftp_proxy category with HTTP client."""
        ...


# Base class for backwards compatibility
class FtpProxy:
    """FTP_PROXY API category."""
    
    explicit: Explicit

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ftp_proxy category with HTTP client."""
        ...
