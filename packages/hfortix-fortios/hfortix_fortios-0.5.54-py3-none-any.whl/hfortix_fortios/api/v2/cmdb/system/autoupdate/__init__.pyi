"""Type stubs for AUTOUPDATE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .schedule import Schedule, ScheduleDictMode, ScheduleObjectMode

__all__ = [
    "Schedule",
    "AutoupdateDictMode",
    "AutoupdateObjectMode",
]

class AutoupdateDictMode:
    """AUTOUPDATE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    schedule: ScheduleDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize autoupdate category with HTTP client."""
        ...


class AutoupdateObjectMode:
    """AUTOUPDATE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    schedule: ScheduleObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize autoupdate category with HTTP client."""
        ...


# Base class for backwards compatibility
class Autoupdate:
    """AUTOUPDATE API category."""
    
    schedule: Schedule

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize autoupdate category with HTTP client."""
        ...
