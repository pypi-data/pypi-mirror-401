"""Type stubs for IKE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .clear import Clear, ClearDictMode, ClearObjectMode

__all__ = [
    "Clear",
    "IkeDictMode",
    "IkeObjectMode",
]

class IkeDictMode:
    """IKE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    clear: ClearDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ike category with HTTP client."""
        ...


class IkeObjectMode:
    """IKE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    clear: ClearObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ike category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ike:
    """IKE API category."""
    
    clear: Clear

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ike category with HTTP client."""
        ...
