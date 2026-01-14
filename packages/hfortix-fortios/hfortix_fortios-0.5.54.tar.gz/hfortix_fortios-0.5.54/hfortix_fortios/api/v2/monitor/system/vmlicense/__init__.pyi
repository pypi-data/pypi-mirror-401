"""Type stubs for VMLICENSE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .download import Download, DownloadDictMode, DownloadObjectMode
    from .download_eval import DownloadEval, DownloadEvalDictMode, DownloadEvalObjectMode
    from .upload import Upload, UploadDictMode, UploadObjectMode

__all__ = [
    "Download",
    "DownloadEval",
    "Upload",
    "VmlicenseDictMode",
    "VmlicenseObjectMode",
]

class VmlicenseDictMode:
    """VMLICENSE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    download: DownloadDictMode
    download_eval: DownloadEvalDictMode
    upload: UploadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vmlicense category with HTTP client."""
        ...


class VmlicenseObjectMode:
    """VMLICENSE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    download: DownloadObjectMode
    download_eval: DownloadEvalObjectMode
    upload: UploadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vmlicense category with HTTP client."""
        ...


# Base class for backwards compatibility
class Vmlicense:
    """VMLICENSE API category."""
    
    download: Download
    download_eval: DownloadEval
    upload: Upload

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vmlicense category with HTTP client."""
        ...
