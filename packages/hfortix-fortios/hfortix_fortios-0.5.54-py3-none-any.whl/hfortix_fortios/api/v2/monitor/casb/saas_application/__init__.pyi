"""Type stubs for SAAS_APPLICATION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .details import Details, DetailsDictMode, DetailsObjectMode

__all__ = [
    "Details",
    "SaasApplicationDictMode",
    "SaasApplicationObjectMode",
]

class SaasApplicationDictMode:
    """SAAS_APPLICATION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    details: DetailsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize saas_application category with HTTP client."""
        ...


class SaasApplicationObjectMode:
    """SAAS_APPLICATION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    details: DetailsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize saas_application category with HTTP client."""
        ...


# Base class for backwards compatibility
class SaasApplication:
    """SAAS_APPLICATION API category."""
    
    details: Details

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize saas_application category with HTTP client."""
        ...
