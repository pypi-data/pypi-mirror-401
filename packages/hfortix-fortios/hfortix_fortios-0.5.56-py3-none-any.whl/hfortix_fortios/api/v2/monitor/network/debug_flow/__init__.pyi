"""Type stubs for DEBUG_FLOW category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .start import Start, StartDictMode, StartObjectMode
    from .stop import Stop, StopDictMode, StopObjectMode

__all__ = [
    "Start",
    "Stop",
    "DebugFlowDictMode",
    "DebugFlowObjectMode",
]

class DebugFlowDictMode:
    """DEBUG_FLOW API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    start: StartDictMode
    stop: StopDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize debug_flow category with HTTP client."""
        ...


class DebugFlowObjectMode:
    """DEBUG_FLOW API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    start: StartObjectMode
    stop: StopObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize debug_flow category with HTTP client."""
        ...


# Base class for backwards compatibility
class DebugFlow:
    """DEBUG_FLOW API category."""
    
    start: Start
    stop: Stop

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize debug_flow category with HTTP client."""
        ...
