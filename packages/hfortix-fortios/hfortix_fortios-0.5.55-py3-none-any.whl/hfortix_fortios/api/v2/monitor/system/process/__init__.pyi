"""Type stubs for PROCESS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .kill import Kill, KillDictMode, KillObjectMode

__all__ = [
    "Kill",
    "ProcessDictMode",
    "ProcessObjectMode",
]

class ProcessDictMode:
    """PROCESS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    kill: KillDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize process category with HTTP client."""
        ...


class ProcessObjectMode:
    """PROCESS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    kill: KillObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize process category with HTTP client."""
        ...


# Base class for backwards compatibility
class Process:
    """PROCESS API category."""
    
    kill: Kill

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize process category with HTTP client."""
        ...
