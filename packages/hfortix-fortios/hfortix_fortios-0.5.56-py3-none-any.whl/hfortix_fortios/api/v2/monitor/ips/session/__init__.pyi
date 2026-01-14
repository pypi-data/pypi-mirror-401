"""Type stubs for SESSION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .performance import Performance, PerformanceDictMode, PerformanceObjectMode

__all__ = [
    "Performance",
    "SessionDictMode",
    "SessionObjectMode",
]

class SessionDictMode:
    """SESSION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    performance: PerformanceDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session category with HTTP client."""
        ...


class SessionObjectMode:
    """SESSION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    performance: PerformanceObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session category with HTTP client."""
        ...


# Base class for backwards compatibility
class Session:
    """SESSION API category."""
    
    performance: Performance

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize session category with HTTP client."""
        ...
