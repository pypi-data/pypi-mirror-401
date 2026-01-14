"""Type stubs for CONFIG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .backup import Backup, BackupDictMode, BackupObjectMode
    from .restore import Restore, RestoreDictMode, RestoreObjectMode
    from .restore_status import RestoreStatus, RestoreStatusDictMode, RestoreStatusObjectMode
    from .usb_filelist import UsbFilelist, UsbFilelistDictMode, UsbFilelistObjectMode

__all__ = [
    "Backup",
    "Restore",
    "RestoreStatus",
    "UsbFilelist",
    "ConfigDictMode",
    "ConfigObjectMode",
]

class ConfigDictMode:
    """CONFIG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    backup: BackupDictMode
    restore: RestoreDictMode
    restore_status: RestoreStatusDictMode
    usb_filelist: UsbFilelistDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize config category with HTTP client."""
        ...


class ConfigObjectMode:
    """CONFIG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    backup: BackupObjectMode
    restore: RestoreObjectMode
    restore_status: RestoreStatusObjectMode
    usb_filelist: UsbFilelistObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize config category with HTTP client."""
        ...


# Base class for backwards compatibility
class Config:
    """CONFIG API category."""
    
    backup: Backup
    restore: Restore
    restore_status: RestoreStatus
    usb_filelist: UsbFilelist

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize config category with HTTP client."""
        ...
