"""Type stubs for LOGDISK category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .format import Format, FormatDictMode, FormatObjectMode

__all__ = [
    "Format",
    "LogdiskDictMode",
    "LogdiskObjectMode",
]

class LogdiskDictMode:
    """LOGDISK API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    format: FormatDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize logdisk category with HTTP client."""
        ...


class LogdiskObjectMode:
    """LOGDISK API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    format: FormatObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize logdisk category with HTTP client."""
        ...


# Base class for backwards compatibility
class Logdisk:
    """LOGDISK API category."""
    
    format: Format

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize logdisk category with HTTP client."""
        ...
