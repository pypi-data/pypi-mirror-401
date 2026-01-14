"""Type stubs for CRASH_LOG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .clear import Clear, ClearDictMode, ClearObjectMode
    from .download import Download, DownloadDictMode, DownloadObjectMode

__all__ = [
    "Clear",
    "Download",
    "CrashLogDictMode",
    "CrashLogObjectMode",
]

class CrashLogDictMode:
    """CRASH_LOG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    clear: ClearDictMode
    download: DownloadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize crash_log category with HTTP client."""
        ...


class CrashLogObjectMode:
    """CRASH_LOG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    clear: ClearObjectMode
    download: DownloadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize crash_log category with HTTP client."""
        ...


# Base class for backwards compatibility
class CrashLog:
    """CRASH_LOG API category."""
    
    clear: Clear
    download: Download

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize crash_log category with HTTP client."""
        ...
