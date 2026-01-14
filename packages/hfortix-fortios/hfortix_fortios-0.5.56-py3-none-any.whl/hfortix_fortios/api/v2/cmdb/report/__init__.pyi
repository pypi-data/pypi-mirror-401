"""Type stubs for REPORT category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .layout import Layout, LayoutDictMode, LayoutObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Layout",
    "Setting",
    "ReportDictMode",
    "ReportObjectMode",
]

class ReportDictMode:
    """REPORT API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    layout: LayoutDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize report category with HTTP client."""
        ...


class ReportObjectMode:
    """REPORT API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    layout: LayoutObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize report category with HTTP client."""
        ...


# Base class for backwards compatibility
class Report:
    """REPORT API category."""
    
    layout: Layout
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize report category with HTTP client."""
        ...
