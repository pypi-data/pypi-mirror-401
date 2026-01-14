"""Type stubs for PACFILE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .download import Download, DownloadDictMode, DownloadObjectMode
    from .upload import Upload, UploadDictMode, UploadObjectMode

__all__ = [
    "Download",
    "Upload",
    "PacfileDictMode",
    "PacfileObjectMode",
]

class PacfileDictMode:
    """PACFILE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    download: DownloadDictMode
    upload: UploadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize pacfile category with HTTP client."""
        ...


class PacfileObjectMode:
    """PACFILE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    download: DownloadObjectMode
    upload: UploadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize pacfile category with HTTP client."""
        ...


# Base class for backwards compatibility
class Pacfile:
    """PACFILE API category."""
    
    download: Download
    upload: Upload

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize pacfile category with HTTP client."""
        ...
