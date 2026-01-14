"""Type stubs for UPGRADE_REPORT category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .current import Current, CurrentDictMode, CurrentObjectMode
    from .exists import Exists, ExistsDictMode, ExistsObjectMode
    from .saved import Saved, SavedDictMode, SavedObjectMode

__all__ = [
    "Current",
    "Exists",
    "Saved",
    "UpgradeReportDictMode",
    "UpgradeReportObjectMode",
]

class UpgradeReportDictMode:
    """UPGRADE_REPORT API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    current: CurrentDictMode
    exists: ExistsDictMode
    saved: SavedDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize upgrade_report category with HTTP client."""
        ...


class UpgradeReportObjectMode:
    """UPGRADE_REPORT API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    current: CurrentObjectMode
    exists: ExistsObjectMode
    saved: SavedObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize upgrade_report category with HTTP client."""
        ...


# Base class for backwards compatibility
class UpgradeReport:
    """UPGRADE_REPORT API category."""
    
    current: Current
    exists: Exists
    saved: Saved

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize upgrade_report category with HTTP client."""
        ...
