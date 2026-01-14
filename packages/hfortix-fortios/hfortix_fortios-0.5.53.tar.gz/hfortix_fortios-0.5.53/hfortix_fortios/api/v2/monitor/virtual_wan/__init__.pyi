"""Type stubs for VIRTUAL_WAN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .health_check import HealthCheck, HealthCheckDictMode, HealthCheckObjectMode
    from .interface_log import InterfaceLog, InterfaceLogDictMode, InterfaceLogObjectMode
    from .members import Members, MembersDictMode, MembersObjectMode
    from .sla_log import SlaLog, SlaLogDictMode, SlaLogObjectMode
    from .sladb import Sladb, SladbDictMode, SladbObjectMode

__all__ = [
    "HealthCheck",
    "InterfaceLog",
    "Members",
    "SlaLog",
    "Sladb",
    "VirtualWanDictMode",
    "VirtualWanObjectMode",
]

class VirtualWanDictMode:
    """VIRTUAL_WAN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    health_check: HealthCheckDictMode
    interface_log: InterfaceLogDictMode
    members: MembersDictMode
    sla_log: SlaLogDictMode
    sladb: SladbDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize virtual_wan category with HTTP client."""
        ...


class VirtualWanObjectMode:
    """VIRTUAL_WAN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    health_check: HealthCheckObjectMode
    interface_log: InterfaceLogObjectMode
    members: MembersObjectMode
    sla_log: SlaLogObjectMode
    sladb: SladbObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize virtual_wan category with HTTP client."""
        ...


# Base class for backwards compatibility
class VirtualWan:
    """VIRTUAL_WAN API category."""
    
    health_check: HealthCheck
    interface_log: InterfaceLog
    members: Members
    sla_log: SlaLog
    sladb: Sladb

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize virtual_wan category with HTTP client."""
        ...
