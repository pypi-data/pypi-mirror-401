"""Type stubs for MONITORING category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .npu_hpe import NpuHpe, NpuHpeDictMode, NpuHpeObjectMode

__all__ = [
    "NpuHpe",
    "MonitoringDictMode",
    "MonitoringObjectMode",
]

class MonitoringDictMode:
    """MONITORING API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    npu_hpe: NpuHpeDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize monitoring category with HTTP client."""
        ...


class MonitoringObjectMode:
    """MONITORING API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    npu_hpe: NpuHpeObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize monitoring category with HTTP client."""
        ...


# Base class for backwards compatibility
class Monitoring:
    """MONITORING API category."""
    
    npu_hpe: NpuHpe

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize monitoring category with HTTP client."""
        ...
