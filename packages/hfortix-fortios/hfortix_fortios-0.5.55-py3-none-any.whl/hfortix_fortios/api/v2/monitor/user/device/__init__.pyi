"""Type stubs for DEVICE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .iot_query import IotQuery, IotQueryDictMode, IotQueryObjectMode
    from .purdue_level import PurdueLevel, PurdueLevelDictMode, PurdueLevelObjectMode
    from .query import Query, QueryDictMode, QueryObjectMode
    from .stats import Stats, StatsDictMode, StatsObjectMode

__all__ = [
    "IotQuery",
    "PurdueLevel",
    "Query",
    "Stats",
    "DeviceDictMode",
    "DeviceObjectMode",
]

class DeviceDictMode:
    """DEVICE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    iot_query: IotQueryDictMode
    purdue_level: PurdueLevelDictMode
    query: QueryDictMode
    stats: StatsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize device category with HTTP client."""
        ...


class DeviceObjectMode:
    """DEVICE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    iot_query: IotQueryObjectMode
    purdue_level: PurdueLevelObjectMode
    query: QueryObjectMode
    stats: StatsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize device category with HTTP client."""
        ...


# Base class for backwards compatibility
class Device:
    """DEVICE API category."""
    
    iot_query: IotQuery
    purdue_level: PurdueLevel
    query: Query
    stats: Stats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize device category with HTTP client."""
        ...
