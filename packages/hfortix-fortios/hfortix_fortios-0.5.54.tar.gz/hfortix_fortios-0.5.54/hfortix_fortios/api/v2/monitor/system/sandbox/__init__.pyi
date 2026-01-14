"""Type stubs for SANDBOX category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .cloud_regions import CloudRegions, CloudRegionsDictMode, CloudRegionsObjectMode
    from .connection import Connection, ConnectionDictMode, ConnectionObjectMode
    from .detect import Detect, DetectDictMode, DetectObjectMode
    from .stats import Stats, StatsDictMode, StatsObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode

__all__ = [
    "CloudRegions",
    "Connection",
    "Detect",
    "Stats",
    "Status",
    "SandboxDictMode",
    "SandboxObjectMode",
]

class SandboxDictMode:
    """SANDBOX API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    cloud_regions: CloudRegionsDictMode
    connection: ConnectionDictMode
    detect: DetectDictMode
    stats: StatsDictMode
    status: StatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sandbox category with HTTP client."""
        ...


class SandboxObjectMode:
    """SANDBOX API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    cloud_regions: CloudRegionsObjectMode
    connection: ConnectionObjectMode
    detect: DetectObjectMode
    stats: StatsObjectMode
    status: StatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sandbox category with HTTP client."""
        ...


# Base class for backwards compatibility
class Sandbox:
    """SANDBOX API category."""
    
    cloud_regions: CloudRegions
    connection: Connection
    detect: Detect
    stats: Stats
    status: Status

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sandbox category with HTTP client."""
        ...
