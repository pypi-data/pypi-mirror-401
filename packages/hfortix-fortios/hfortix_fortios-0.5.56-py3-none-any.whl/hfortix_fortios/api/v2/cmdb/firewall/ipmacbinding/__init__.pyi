"""Type stubs for IPMACBINDING category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .setting import Setting, SettingDictMode, SettingObjectMode
    from .table import Table, TableDictMode, TableObjectMode

__all__ = [
    "Setting",
    "Table",
    "IpmacbindingDictMode",
    "IpmacbindingObjectMode",
]

class IpmacbindingDictMode:
    """IPMACBINDING API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    setting: SettingDictMode
    table: TableDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipmacbinding category with HTTP client."""
        ...


class IpmacbindingObjectMode:
    """IPMACBINDING API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    setting: SettingObjectMode
    table: TableObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipmacbinding category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ipmacbinding:
    """IPMACBINDING API category."""
    
    setting: Setting
    table: Table

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ipmacbinding category with HTTP client."""
        ...
