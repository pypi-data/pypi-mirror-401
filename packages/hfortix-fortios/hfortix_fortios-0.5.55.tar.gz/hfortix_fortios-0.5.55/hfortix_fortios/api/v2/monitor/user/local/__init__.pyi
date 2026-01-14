"""Type stubs for LOCAL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .change_password import ChangePassword, ChangePasswordDictMode, ChangePasswordObjectMode

__all__ = [
    "ChangePassword",
    "LocalDictMode",
    "LocalObjectMode",
]

class LocalDictMode:
    """LOCAL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    change_password: ChangePasswordDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local category with HTTP client."""
        ...


class LocalObjectMode:
    """LOCAL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    change_password: ChangePasswordObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local category with HTTP client."""
        ...


# Base class for backwards compatibility
class Local:
    """LOCAL API category."""
    
    change_password: ChangePassword

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local category with HTTP client."""
        ...
