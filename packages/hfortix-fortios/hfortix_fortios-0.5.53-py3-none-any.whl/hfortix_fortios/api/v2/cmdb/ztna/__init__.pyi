"""Type stubs for ZTNA category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .reverse_connector import ReverseConnector, ReverseConnectorDictMode, ReverseConnectorObjectMode
    from .traffic_forward_proxy import TrafficForwardProxy, TrafficForwardProxyDictMode, TrafficForwardProxyObjectMode
    from .web_portal import WebPortal, WebPortalDictMode, WebPortalObjectMode
    from .web_portal_bookmark import WebPortalBookmark, WebPortalBookmarkDictMode, WebPortalBookmarkObjectMode
    from .web_proxy import WebProxy, WebProxyDictMode, WebProxyObjectMode

__all__ = [
    "ReverseConnector",
    "TrafficForwardProxy",
    "WebPortal",
    "WebPortalBookmark",
    "WebProxy",
    "ZtnaDictMode",
    "ZtnaObjectMode",
]

class ZtnaDictMode:
    """ZTNA API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    reverse_connector: ReverseConnectorDictMode
    traffic_forward_proxy: TrafficForwardProxyDictMode
    web_portal: WebPortalDictMode
    web_portal_bookmark: WebPortalBookmarkDictMode
    web_proxy: WebProxyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ztna category with HTTP client."""
        ...


class ZtnaObjectMode:
    """ZTNA API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    reverse_connector: ReverseConnectorObjectMode
    traffic_forward_proxy: TrafficForwardProxyObjectMode
    web_portal: WebPortalObjectMode
    web_portal_bookmark: WebPortalBookmarkObjectMode
    web_proxy: WebProxyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ztna category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ztna:
    """ZTNA API category."""
    
    reverse_connector: ReverseConnector
    traffic_forward_proxy: TrafficForwardProxy
    web_portal: WebPortal
    web_portal_bookmark: WebPortalBookmark
    web_proxy: WebProxy

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ztna category with HTTP client."""
        ...
