"""Type stubs for ALERTEMAIL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Setting",
    "AlertemailDictMode",
    "AlertemailObjectMode",
]

class AlertemailDictMode:
    """ALERTEMAIL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize alertemail category with HTTP client."""
        ...


class AlertemailObjectMode:
    """ALERTEMAIL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize alertemail category with HTTP client."""
        ...


# Base class for backwards compatibility
class Alertemail:
    """ALERTEMAIL API category."""
    
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize alertemail category with HTTP client."""
        ...
