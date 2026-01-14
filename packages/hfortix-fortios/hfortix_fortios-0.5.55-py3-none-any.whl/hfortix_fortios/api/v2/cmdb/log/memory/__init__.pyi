"""Type stubs for MEMORY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .filter import Filter, FilterDictMode, FilterObjectMode
    from .global_setting import GlobalSetting, GlobalSettingDictMode, GlobalSettingObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Filter",
    "GlobalSetting",
    "Setting",
    "MemoryDictMode",
    "MemoryObjectMode",
]

class MemoryDictMode:
    """MEMORY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    filter: FilterDictMode
    global_setting: GlobalSettingDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize memory category with HTTP client."""
        ...


class MemoryObjectMode:
    """MEMORY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    filter: FilterObjectMode
    global_setting: GlobalSettingObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize memory category with HTTP client."""
        ...


# Base class for backwards compatibility
class Memory:
    """MEMORY API category."""
    
    filter: Filter
    global_setting: GlobalSetting
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize memory category with HTTP client."""
        ...
