"""Type stubs for EXTENDER_CONTROLLER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .extender import Extender

__all__ = [
    "ExtenderControllerDictMode",
    "ExtenderControllerObjectMode",
]

class ExtenderControllerDictMode:
    """EXTENDER_CONTROLLER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    extender: Extender

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extender_controller category with HTTP client."""
        ...


class ExtenderControllerObjectMode:
    """EXTENDER_CONTROLLER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    extender: Extender

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extender_controller category with HTTP client."""
        ...


# Base class for backwards compatibility
class ExtenderController:
    """EXTENDER_CONTROLLER API category."""
    
    extender: Extender

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extender_controller category with HTTP client."""
        ...
