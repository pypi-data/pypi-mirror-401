"""Type stubs for WEB_UI category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom_language import CustomLanguage
    from .language import LanguageDictMode, LanguageObjectMode

__all__ = [
    "WebUiDictMode",
    "WebUiObjectMode",
]

class WebUiDictMode:
    """WEB_UI API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    custom_language: CustomLanguage
    language: LanguageDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize web_ui category with HTTP client."""
        ...


class WebUiObjectMode:
    """WEB_UI API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    custom_language: CustomLanguage
    language: LanguageObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize web_ui category with HTTP client."""
        ...


# Base class for backwards compatibility
class WebUi:
    """WEB_UI API category."""
    
    custom_language: CustomLanguage
    language: Language

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize web_ui category with HTTP client."""
        ...
