"""Type stubs for OBJECT category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .usage import Usage, UsageDictMode, UsageObjectMode

__all__ = [
    "Usage",
    "ObjectDictMode",
    "ObjectObjectMode",
]

class ObjectDictMode:
    """OBJECT API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    usage: UsageDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize object category with HTTP client."""
        ...


class ObjectObjectMode:
    """OBJECT API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    usage: UsageObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize object category with HTTP client."""
        ...


# Base class for backwards compatibility
class Object:
    """OBJECT API category."""
    
    usage: Usage

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize object category with HTTP client."""
        ...
