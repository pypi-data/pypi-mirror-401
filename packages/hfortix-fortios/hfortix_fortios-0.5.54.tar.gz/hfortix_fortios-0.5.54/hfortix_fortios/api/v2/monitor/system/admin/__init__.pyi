"""Type stubs for ADMIN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .change_vdom_mode import ChangeVdomMode, ChangeVdomModeDictMode, ChangeVdomModeObjectMode

__all__ = [
    "ChangeVdomMode",
    "AdminDictMode",
    "AdminObjectMode",
]

class AdminDictMode:
    """ADMIN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    change_vdom_mode: ChangeVdomModeDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize admin category with HTTP client."""
        ...


class AdminObjectMode:
    """ADMIN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    change_vdom_mode: ChangeVdomModeObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize admin category with HTTP client."""
        ...


# Base class for backwards compatibility
class Admin:
    """ADMIN API category."""
    
    change_vdom_mode: ChangeVdomMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize admin category with HTTP client."""
        ...
