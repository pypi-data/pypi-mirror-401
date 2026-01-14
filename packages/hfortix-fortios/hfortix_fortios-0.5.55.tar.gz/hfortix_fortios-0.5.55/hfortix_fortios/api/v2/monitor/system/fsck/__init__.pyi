"""Type stubs for FSCK category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .start import Start, StartDictMode, StartObjectMode

__all__ = [
    "Start",
    "FsckDictMode",
    "FsckObjectMode",
]

class FsckDictMode:
    """FSCK API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    start: StartDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fsck category with HTTP client."""
        ...


class FsckObjectMode:
    """FSCK API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    start: StartObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fsck category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fsck:
    """FSCK API category."""
    
    start: Start

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fsck category with HTTP client."""
        ...
