"""Type stubs for ANTIVIRUS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .stats import Stats, StatsDictMode, StatsObjectMode

__all__ = [
    "Stats",
    "AntivirusDictMode",
    "AntivirusObjectMode",
]

class AntivirusDictMode:
    """ANTIVIRUS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    stats: StatsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize antivirus category with HTTP client."""
        ...


class AntivirusObjectMode:
    """ANTIVIRUS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    stats: StatsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize antivirus category with HTTP client."""
        ...


# Base class for backwards compatibility
class Antivirus:
    """ANTIVIRUS API category."""
    
    stats: Stats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize antivirus category with HTTP client."""
        ...
