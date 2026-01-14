"""Type stubs for SCHEDULE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .group import Group, GroupDictMode, GroupObjectMode
    from .onetime import Onetime, OnetimeDictMode, OnetimeObjectMode
    from .recurring import Recurring, RecurringDictMode, RecurringObjectMode

__all__ = [
    "Group",
    "Onetime",
    "Recurring",
    "ScheduleDictMode",
    "ScheduleObjectMode",
]

class ScheduleDictMode:
    """SCHEDULE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    group: GroupDictMode
    onetime: OnetimeDictMode
    recurring: RecurringDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize schedule category with HTTP client."""
        ...


class ScheduleObjectMode:
    """SCHEDULE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    group: GroupObjectMode
    onetime: OnetimeObjectMode
    recurring: RecurringObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize schedule category with HTTP client."""
        ...


# Base class for backwards compatibility
class Schedule:
    """SCHEDULE API category."""
    
    group: Group
    onetime: Onetime
    recurring: Recurring

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize schedule category with HTTP client."""
        ...
