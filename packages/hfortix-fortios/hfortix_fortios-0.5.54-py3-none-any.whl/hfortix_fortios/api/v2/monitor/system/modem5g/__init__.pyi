"""Type stubs for MODEM5G category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status, StatusDictMode, StatusObjectMode

__all__ = [
    "Status",
    "Modem5gDictMode",
    "Modem5gObjectMode",
]

class Modem5gDictMode:
    """MODEM5G API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    status: StatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize modem5g category with HTTP client."""
        ...


class Modem5gObjectMode:
    """MODEM5G API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    status: StatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize modem5g category with HTTP client."""
        ...


# Base class for backwards compatibility
class Modem5g:
    """MODEM5G API category."""
    
    status: Status

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize modem5g category with HTTP client."""
        ...
