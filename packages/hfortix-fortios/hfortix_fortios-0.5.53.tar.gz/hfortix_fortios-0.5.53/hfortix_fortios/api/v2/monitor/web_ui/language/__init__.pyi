"""Type stubs for LANGUAGE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .import_ import Import, ImportDictMode, ImportObjectMode

__all__ = [
    "Import",
    "LanguageDictMode",
    "LanguageObjectMode",
]

class LanguageDictMode:
    """LANGUAGE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    import_: ImportDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize language category with HTTP client."""
        ...


class LanguageObjectMode:
    """LANGUAGE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    import_: ImportObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize language category with HTTP client."""
        ...


# Base class for backwards compatibility
class Language:
    """LANGUAGE API category."""
    
    import_: Import

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize language category with HTTP client."""
        ...
