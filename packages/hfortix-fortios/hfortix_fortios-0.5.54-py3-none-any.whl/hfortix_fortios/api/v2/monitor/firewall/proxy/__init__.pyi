"""Type stubs for PROXY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .sessions import Sessions, SessionsDictMode, SessionsObjectMode

__all__ = [
    "Sessions",
    "ProxyDictMode",
    "ProxyObjectMode",
]

class ProxyDictMode:
    """PROXY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    sessions: SessionsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize proxy category with HTTP client."""
        ...


class ProxyObjectMode:
    """PROXY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    sessions: SessionsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize proxy category with HTTP client."""
        ...


# Base class for backwards compatibility
class Proxy:
    """PROXY API category."""
    
    sessions: Sessions

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize proxy category with HTTP client."""
        ...
