"""Type stubs for WEBPROXY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .pacfile import PacfileDictMode, PacfileObjectMode

__all__ = [
    "WebproxyDictMode",
    "WebproxyObjectMode",
]

class WebproxyDictMode:
    """WEBPROXY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    pacfile: PacfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webproxy category with HTTP client."""
        ...


class WebproxyObjectMode:
    """WEBPROXY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    pacfile: PacfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webproxy category with HTTP client."""
        ...


# Base class for backwards compatibility
class Webproxy:
    """WEBPROXY API category."""
    
    pacfile: Pacfile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webproxy category with HTTP client."""
        ...
