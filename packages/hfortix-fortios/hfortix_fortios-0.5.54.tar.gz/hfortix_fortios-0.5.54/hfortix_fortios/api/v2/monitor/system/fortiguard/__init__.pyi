"""Type stubs for FORTIGUARD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .clear_statistics import ClearStatistics, ClearStatisticsDictMode, ClearStatisticsObjectMode
    from .manual_update import ManualUpdate, ManualUpdateDictMode, ManualUpdateObjectMode
    from .server_info import ServerInfo, ServerInfoDictMode, ServerInfoObjectMode
    from .test_availability import TestAvailability, TestAvailabilityDictMode, TestAvailabilityObjectMode
    from .update import Update, UpdateDictMode, UpdateObjectMode

__all__ = [
    "ClearStatistics",
    "ManualUpdate",
    "ServerInfo",
    "TestAvailability",
    "Update",
    "FortiguardDictMode",
    "FortiguardObjectMode",
]

class FortiguardDictMode:
    """FORTIGUARD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    clear_statistics: ClearStatisticsDictMode
    manual_update: ManualUpdateDictMode
    server_info: ServerInfoDictMode
    test_availability: TestAvailabilityDictMode
    update: UpdateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


class FortiguardObjectMode:
    """FORTIGUARD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    clear_statistics: ClearStatisticsObjectMode
    manual_update: ManualUpdateObjectMode
    server_info: ServerInfoObjectMode
    test_availability: TestAvailabilityObjectMode
    update: UpdateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fortiguard:
    """FORTIGUARD API category."""
    
    clear_statistics: ClearStatistics
    manual_update: ManualUpdate
    server_info: ServerInfo
    test_availability: TestAvailability
    update: Update

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...
