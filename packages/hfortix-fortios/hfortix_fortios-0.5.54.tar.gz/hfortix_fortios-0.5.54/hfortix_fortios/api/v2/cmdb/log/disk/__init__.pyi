"""Type stubs for DISK category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .filter import Filter, FilterDictMode, FilterObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Filter",
    "Setting",
    "DiskDictMode",
    "DiskObjectMode",
]

class DiskDictMode:
    """DISK API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    filter: FilterDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize disk category with HTTP client."""
        ...


class DiskObjectMode:
    """DISK API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    filter: FilterObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize disk category with HTTP client."""
        ...


# Base class for backwards compatibility
class Disk:
    """DISK API category."""
    
    filter: Filter
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize disk category with HTTP client."""
        ...
