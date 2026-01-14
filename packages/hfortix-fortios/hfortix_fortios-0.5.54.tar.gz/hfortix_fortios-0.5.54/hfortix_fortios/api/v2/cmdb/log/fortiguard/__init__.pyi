"""Type stubs for FORTIGUARD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .filter import Filter, FilterDictMode, FilterObjectMode
    from .override_filter import OverrideFilter, OverrideFilterDictMode, OverrideFilterObjectMode
    from .override_setting import OverrideSetting, OverrideSettingDictMode, OverrideSettingObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Filter",
    "OverrideFilter",
    "OverrideSetting",
    "Setting",
    "FortiguardDictMode",
    "FortiguardObjectMode",
]

class FortiguardDictMode:
    """FORTIGUARD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    filter: FilterDictMode
    override_filter: OverrideFilterDictMode
    override_setting: OverrideSettingDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


class FortiguardObjectMode:
    """FORTIGUARD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    filter: FilterObjectMode
    override_filter: OverrideFilterObjectMode
    override_setting: OverrideSettingObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fortiguard:
    """FORTIGUARD API category."""
    
    filter: Filter
    override_filter: OverrideFilter
    override_setting: OverrideSetting
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...
