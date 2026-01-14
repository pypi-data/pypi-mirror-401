"""Type stubs for AVATAR category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .download import Download, DownloadDictMode, DownloadObjectMode

__all__ = [
    "Download",
    "AvatarDictMode",
    "AvatarObjectMode",
]

class AvatarDictMode:
    """AVATAR API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    download: DownloadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize avatar category with HTTP client."""
        ...


class AvatarObjectMode:
    """AVATAR API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    download: DownloadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize avatar category with HTTP client."""
        ...


# Base class for backwards compatibility
class Avatar:
    """AVATAR API category."""
    
    download: Download

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize avatar category with HTTP client."""
        ...
