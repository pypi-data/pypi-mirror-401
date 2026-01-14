"""Type stubs for AZURE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .application_list import ApplicationList

__all__ = [
    "AzureDictMode",
    "AzureObjectMode",
]

class AzureDictMode:
    """AZURE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    application_list: ApplicationList

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize azure category with HTTP client."""
        ...


class AzureObjectMode:
    """AZURE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    application_list: ApplicationList

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize azure category with HTTP client."""
        ...


# Base class for backwards compatibility
class Azure:
    """AZURE API category."""
    
    application_list: ApplicationList

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize azure category with HTTP client."""
        ...
