"""Type stubs for CHANGE_PASSWORD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .select import Select, SelectDictMode, SelectObjectMode

__all__ = [
    "Select",
    "ChangePasswordDictMode",
    "ChangePasswordObjectMode",
]

class ChangePasswordDictMode:
    """CHANGE_PASSWORD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    select: SelectDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize change_password category with HTTP client."""
        ...


class ChangePasswordObjectMode:
    """CHANGE_PASSWORD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    select: SelectObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize change_password category with HTTP client."""
        ...


# Base class for backwards compatibility
class ChangePassword:
    """CHANGE_PASSWORD API category."""
    
    select: Select

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize change_password category with HTTP client."""
        ...
