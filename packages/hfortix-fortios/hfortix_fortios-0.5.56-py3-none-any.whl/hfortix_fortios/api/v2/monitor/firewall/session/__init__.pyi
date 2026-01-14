"""Type stubs for SESSION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .close import Close, CloseDictMode, CloseObjectMode
    from .close_all import CloseAll, CloseAllDictMode, CloseAllObjectMode
    from .close_multiple import CloseMultiple, CloseMultipleDictMode, CloseMultipleObjectMode

__all__ = [
    "Close",
    "CloseAll",
    "CloseMultiple",
    "SessionDictMode",
    "SessionObjectMode",
]

class SessionDictMode:
    """SESSION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    close: CloseDictMode
    close_all: CloseAllDictMode
    close_multiple: CloseMultipleDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session category with HTTP client."""
        ...


class SessionObjectMode:
    """SESSION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    close: CloseObjectMode
    close_all: CloseAllObjectMode
    close_multiple: CloseMultipleObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session category with HTTP client."""
        ...


# Base class for backwards compatibility
class Session:
    """SESSION API category."""
    
    close: Close
    close_all: CloseAll
    close_multiple: CloseMultiple

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session category with HTTP client."""
        ...
