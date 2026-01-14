"""Type stubs for CASB category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .saas_application import SaasApplication

__all__ = [
    "CasbDictMode",
    "CasbObjectMode",
]

class CasbDictMode:
    """CASB API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    saas_application: SaasApplication

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize casb category with HTTP client."""
        ...


class CasbObjectMode:
    """CASB API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    saas_application: SaasApplication

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize casb category with HTTP client."""
        ...


# Base class for backwards compatibility
class Casb:
    """CASB API category."""
    
    saas_application: SaasApplication

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize casb category with HTTP client."""
        ...
