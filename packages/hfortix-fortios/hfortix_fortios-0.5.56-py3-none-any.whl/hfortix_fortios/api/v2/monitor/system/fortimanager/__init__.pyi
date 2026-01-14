"""Type stubs for FORTIMANAGER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .backup_action import BackupAction, BackupActionDictMode, BackupActionObjectMode
    from .backup_details import BackupDetails, BackupDetailsDictMode, BackupDetailsObjectMode
    from .backup_summary import BackupSummary, BackupSummaryDictMode, BackupSummaryObjectMode

__all__ = [
    "BackupAction",
    "BackupDetails",
    "BackupSummary",
    "FortimanagerDictMode",
    "FortimanagerObjectMode",
]

class FortimanagerDictMode:
    """FORTIMANAGER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    backup_action: BackupActionDictMode
    backup_details: BackupDetailsDictMode
    backup_summary: BackupSummaryDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortimanager category with HTTP client."""
        ...


class FortimanagerObjectMode:
    """FORTIMANAGER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    backup_action: BackupActionObjectMode
    backup_details: BackupDetailsObjectMode
    backup_summary: BackupSummaryObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortimanager category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fortimanager:
    """FORTIMANAGER API category."""
    
    backup_action: BackupAction
    backup_details: BackupDetails
    backup_summary: BackupSummary

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortimanager category with HTTP client."""
        ...
