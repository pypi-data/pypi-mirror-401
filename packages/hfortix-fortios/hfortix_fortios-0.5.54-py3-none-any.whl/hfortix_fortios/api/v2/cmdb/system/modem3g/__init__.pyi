"""Type stubs for MODEM3G category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom import Custom, CustomDictMode, CustomObjectMode

__all__ = [
    "Custom",
    "Modem3gDictMode",
    "Modem3gObjectMode",
]

class Modem3gDictMode:
    """MODEM3G API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    custom: CustomDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize modem3g category with HTTP client."""
        ...


class Modem3gObjectMode:
    """MODEM3G API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    custom: CustomObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize modem3g category with HTTP client."""
        ...


# Base class for backwards compatibility
class Modem3g:
    """MODEM3G API category."""
    
    custom: Custom

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize modem3g category with HTTP client."""
        ...
