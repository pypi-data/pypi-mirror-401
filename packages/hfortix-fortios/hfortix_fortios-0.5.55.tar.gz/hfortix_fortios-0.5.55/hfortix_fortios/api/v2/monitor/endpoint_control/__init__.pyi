"""Type stubs for ENDPOINT_CONTROL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .record_list import RecordList, RecordListDictMode, RecordListObjectMode
    from .summary import Summary, SummaryDictMode, SummaryObjectMode
    from .avatar import AvatarDictMode, AvatarObjectMode
    from .ems import EmsDictMode, EmsObjectMode
    from .installer import Installer

__all__ = [
    "RecordList",
    "Summary",
    "EndpointControlDictMode",
    "EndpointControlObjectMode",
]

class EndpointControlDictMode:
    """ENDPOINT_CONTROL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    avatar: AvatarDictMode
    ems: EmsDictMode
    installer: Installer
    record_list: RecordListDictMode
    summary: SummaryDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize endpoint_control category with HTTP client."""
        ...


class EndpointControlObjectMode:
    """ENDPOINT_CONTROL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    avatar: AvatarObjectMode
    ems: EmsObjectMode
    installer: Installer
    record_list: RecordListObjectMode
    summary: SummaryObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize endpoint_control category with HTTP client."""
        ...


# Base class for backwards compatibility
class EndpointControl:
    """ENDPOINT_CONTROL API category."""
    
    avatar: Avatar
    ems: Ems
    installer: Installer
    record_list: RecordList
    summary: Summary

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize endpoint_control category with HTTP client."""
        ...
