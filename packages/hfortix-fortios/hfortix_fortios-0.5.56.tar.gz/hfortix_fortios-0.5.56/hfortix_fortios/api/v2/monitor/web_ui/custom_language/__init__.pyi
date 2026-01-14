"""Type stubs for CUSTOM_LANGUAGE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .create import Create, CreateDictMode, CreateObjectMode
    from .download import Download, DownloadDictMode, DownloadObjectMode
    from .update import Update, UpdateDictMode, UpdateObjectMode

__all__ = [
    "Create",
    "Download",
    "Update",
    "CustomLanguageDictMode",
    "CustomLanguageObjectMode",
]

class CustomLanguageDictMode:
    """CUSTOM_LANGUAGE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    create: CreateDictMode
    download: DownloadDictMode
    update: UpdateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize custom_language category with HTTP client."""
        ...


class CustomLanguageObjectMode:
    """CUSTOM_LANGUAGE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    create: CreateObjectMode
    download: DownloadObjectMode
    update: UpdateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize custom_language category with HTTP client."""
        ...


# Base class for backwards compatibility
class CustomLanguage:
    """CUSTOM_LANGUAGE API category."""
    
    create: Create
    download: Download
    update: Update

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize custom_language category with HTTP client."""
        ...
