"""Type stubs for AUTOMATION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Setting",
    "AutomationDictMode",
    "AutomationObjectMode",
]

class AutomationDictMode:
    """AUTOMATION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize automation category with HTTP client."""
        ...


class AutomationObjectMode:
    """AUTOMATION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize automation category with HTTP client."""
        ...


# Base class for backwards compatibility
class Automation:
    """AUTOMATION API category."""
    
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize automation category with HTTP client."""
        ...
