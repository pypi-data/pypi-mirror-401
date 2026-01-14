"""Type stubs for SESSION6 category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .close_multiple import CloseMultiple, CloseMultipleDictMode, CloseMultipleObjectMode

__all__ = [
    "CloseMultiple",
    "Session6DictMode",
    "Session6ObjectMode",
]

class Session6DictMode:
    """SESSION6 API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    close_multiple: CloseMultipleDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session6 category with HTTP client."""
        ...


class Session6ObjectMode:
    """SESSION6 API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    close_multiple: CloseMultipleObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session6 category with HTTP client."""
        ...


# Base class for backwards compatibility
class Session6:
    """SESSION6 API category."""
    
    close_multiple: CloseMultiple

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session6 category with HTTP client."""
        ...
