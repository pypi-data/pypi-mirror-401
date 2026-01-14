"""Type stubs for NAC_DEVICE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .stats import Stats, StatsDictMode, StatsObjectMode

__all__ = [
    "Stats",
    "NacDeviceDictMode",
    "NacDeviceObjectMode",
]

class NacDeviceDictMode:
    """NAC_DEVICE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    stats: StatsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize nac_device category with HTTP client."""
        ...


class NacDeviceObjectMode:
    """NAC_DEVICE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    stats: StatsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize nac_device category with HTTP client."""
        ...


# Base class for backwards compatibility
class NacDevice:
    """NAC_DEVICE API category."""
    
    stats: Stats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize nac_device category with HTTP client."""
        ...
