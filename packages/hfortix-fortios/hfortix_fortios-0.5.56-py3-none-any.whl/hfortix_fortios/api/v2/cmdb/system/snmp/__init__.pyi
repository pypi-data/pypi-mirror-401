"""Type stubs for SNMP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .community import Community, CommunityDictMode, CommunityObjectMode
    from .mib_view import MibView, MibViewDictMode, MibViewObjectMode
    from .rmon_stat import RmonStat, RmonStatDictMode, RmonStatObjectMode
    from .sysinfo import Sysinfo, SysinfoDictMode, SysinfoObjectMode
    from .user import User, UserDictMode, UserObjectMode

__all__ = [
    "Community",
    "MibView",
    "RmonStat",
    "Sysinfo",
    "User",
    "SnmpDictMode",
    "SnmpObjectMode",
]

class SnmpDictMode:
    """SNMP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    community: CommunityDictMode
    mib_view: MibViewDictMode
    rmon_stat: RmonStatDictMode
    sysinfo: SysinfoDictMode
    user: UserDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize snmp category with HTTP client."""
        ...


class SnmpObjectMode:
    """SNMP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    community: CommunityObjectMode
    mib_view: MibViewObjectMode
    rmon_stat: RmonStatObjectMode
    sysinfo: SysinfoObjectMode
    user: UserObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize snmp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Snmp:
    """SNMP API category."""
    
    community: Community
    mib_view: MibView
    rmon_stat: RmonStat
    sysinfo: Sysinfo
    user: User

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize snmp category with HTTP client."""
        ...
