"""Type stubs for RESOURCE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .usage import Usage, UsageDictMode, UsageObjectMode

__all__ = [
    "Usage",
    "ResourceDictMode",
    "ResourceObjectMode",
]

class ResourceDictMode:
    """RESOURCE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    usage: UsageDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize resource category with HTTP client."""
        ...


class ResourceObjectMode:
    """RESOURCE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    usage: UsageObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize resource category with HTTP client."""
        ...


# Base class for backwards compatibility
class Resource:
    """RESOURCE API category."""
    
    usage: Usage

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize resource category with HTTP client."""
        ...
