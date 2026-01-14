"""Type stubs for WANOPT category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .history import History
    from .peer_stats import PeerStats
    from .webcache import Webcache

__all__ = [
    "WanoptDictMode",
    "WanoptObjectMode",
]

class WanoptDictMode:
    """WANOPT API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    history: History
    peer_stats: PeerStats
    webcache: Webcache

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wanopt category with HTTP client."""
        ...


class WanoptObjectMode:
    """WANOPT API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    history: History
    peer_stats: PeerStats
    webcache: Webcache

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wanopt category with HTTP client."""
        ...


# Base class for backwards compatibility
class Wanopt:
    """WANOPT API category."""
    
    history: History
    peer_stats: PeerStats
    webcache: Webcache

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wanopt category with HTTP client."""
        ...
