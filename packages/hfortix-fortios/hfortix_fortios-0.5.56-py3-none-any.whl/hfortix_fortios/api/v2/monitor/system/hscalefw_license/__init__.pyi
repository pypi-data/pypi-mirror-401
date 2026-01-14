"""Type stubs for HSCALEFW_LICENSE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .upload import Upload, UploadDictMode, UploadObjectMode

__all__ = [
    "Upload",
    "HscalefwLicenseDictMode",
    "HscalefwLicenseObjectMode",
]

class HscalefwLicenseDictMode:
    """HSCALEFW_LICENSE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    upload: UploadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize hscalefw_license category with HTTP client."""
        ...


class HscalefwLicenseObjectMode:
    """HSCALEFW_LICENSE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    upload: UploadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize hscalefw_license category with HTTP client."""
        ...


# Base class for backwards compatibility
class HscalefwLicense:
    """HSCALEFW_LICENSE API category."""
    
    upload: Upload

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize hscalefw_license category with HTTP client."""
        ...
