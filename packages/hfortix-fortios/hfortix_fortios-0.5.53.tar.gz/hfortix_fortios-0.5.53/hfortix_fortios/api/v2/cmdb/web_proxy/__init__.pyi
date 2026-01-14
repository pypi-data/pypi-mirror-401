"""Type stubs for WEB_PROXY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .debug_url import DebugUrl, DebugUrlDictMode, DebugUrlObjectMode
    from .explicit import Explicit, ExplicitDictMode, ExplicitObjectMode
    from .fast_fallback import FastFallback, FastFallbackDictMode, FastFallbackObjectMode
    from .forward_server import ForwardServer, ForwardServerDictMode, ForwardServerObjectMode
    from .forward_server_group import ForwardServerGroup, ForwardServerGroupDictMode, ForwardServerGroupObjectMode
    from .global_ import Global, GlobalDictMode, GlobalObjectMode
    from .isolator_server import IsolatorServer, IsolatorServerDictMode, IsolatorServerObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .url_match import UrlMatch, UrlMatchDictMode, UrlMatchObjectMode
    from .wisp import Wisp, WispDictMode, WispObjectMode

__all__ = [
    "DebugUrl",
    "Explicit",
    "FastFallback",
    "ForwardServer",
    "ForwardServerGroup",
    "Global",
    "IsolatorServer",
    "Profile",
    "UrlMatch",
    "Wisp",
    "WebProxyDictMode",
    "WebProxyObjectMode",
]

class WebProxyDictMode:
    """WEB_PROXY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    debug_url: DebugUrlDictMode
    explicit: ExplicitDictMode
    fast_fallback: FastFallbackDictMode
    forward_server: ForwardServerDictMode
    forward_server_group: ForwardServerGroupDictMode
    global_: GlobalDictMode
    isolator_server: IsolatorServerDictMode
    profile: ProfileDictMode
    url_match: UrlMatchDictMode
    wisp: WispDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize web_proxy category with HTTP client."""
        ...


class WebProxyObjectMode:
    """WEB_PROXY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    debug_url: DebugUrlObjectMode
    explicit: ExplicitObjectMode
    fast_fallback: FastFallbackObjectMode
    forward_server: ForwardServerObjectMode
    forward_server_group: ForwardServerGroupObjectMode
    global_: GlobalObjectMode
    isolator_server: IsolatorServerObjectMode
    profile: ProfileObjectMode
    url_match: UrlMatchObjectMode
    wisp: WispObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize web_proxy category with HTTP client."""
        ...


# Base class for backwards compatibility
class WebProxy:
    """WEB_PROXY API category."""
    
    debug_url: DebugUrl
    explicit: Explicit
    fast_fallback: FastFallback
    forward_server: ForwardServer
    forward_server_group: ForwardServerGroup
    global_: Global
    isolator_server: IsolatorServer
    profile: Profile
    url_match: UrlMatch
    wisp: Wisp

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize web_proxy category with HTTP client."""
        ...
