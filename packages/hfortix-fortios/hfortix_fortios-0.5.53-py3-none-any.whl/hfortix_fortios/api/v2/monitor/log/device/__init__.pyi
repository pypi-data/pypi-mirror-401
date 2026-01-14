"""Type stubs for DEVICE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .state import State, StateDictMode, StateObjectMode

__all__ = [
    "State",
    "DeviceDictMode",
    "DeviceObjectMode",
]

class DeviceDictMode:
    """DEVICE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    state: StateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize device category with HTTP client."""
        ...


class DeviceObjectMode:
    """DEVICE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    state: StateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize device category with HTTP client."""
        ...


# Base class for backwards compatibility
class Device:
    """DEVICE API category."""
    
    state: State

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize device category with HTTP client."""
        ...
