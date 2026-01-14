"""Type stubs for ICAP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .server import Server, ServerDictMode, ServerObjectMode
    from .server_group import ServerGroup, ServerGroupDictMode, ServerGroupObjectMode

__all__ = [
    "Profile",
    "Server",
    "ServerGroup",
    "IcapDictMode",
    "IcapObjectMode",
]

class IcapDictMode:
    """ICAP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    profile: ProfileDictMode
    server: ServerDictMode
    server_group: ServerGroupDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize icap category with HTTP client."""
        ...


class IcapObjectMode:
    """ICAP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    profile: ProfileObjectMode
    server: ServerObjectMode
    server_group: ServerGroupObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize icap category with HTTP client."""
        ...


# Base class for backwards compatibility
class Icap:
    """ICAP API category."""
    
    profile: Profile
    server: Server
    server_group: ServerGroup

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize icap category with HTTP client."""
        ...
