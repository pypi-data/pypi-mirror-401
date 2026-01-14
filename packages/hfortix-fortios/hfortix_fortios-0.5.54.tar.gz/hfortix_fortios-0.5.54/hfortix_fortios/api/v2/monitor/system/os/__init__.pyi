"""Type stubs for OS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .reboot import Reboot, RebootDictMode, RebootObjectMode
    from .shutdown import Shutdown, ShutdownDictMode, ShutdownObjectMode

__all__ = [
    "Reboot",
    "Shutdown",
    "OsDictMode",
    "OsObjectMode",
]

class OsDictMode:
    """OS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    reboot: RebootDictMode
    shutdown: ShutdownDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize os category with HTTP client."""
        ...


class OsObjectMode:
    """OS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    reboot: RebootObjectMode
    shutdown: ShutdownObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize os category with HTTP client."""
        ...


# Base class for backwards compatibility
class Os:
    """OS API category."""
    
    reboot: Reboot
    shutdown: Shutdown

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize os category with HTTP client."""
        ...
