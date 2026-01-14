"""Type stubs for FORTIVIEW category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .historical_statistics import HistoricalStatistics, HistoricalStatisticsDictMode, HistoricalStatisticsObjectMode
    from .realtime_proxy_statistics import RealtimeProxyStatistics, RealtimeProxyStatisticsDictMode, RealtimeProxyStatisticsObjectMode
    from .realtime_statistics import RealtimeStatistics, RealtimeStatisticsDictMode, RealtimeStatisticsObjectMode
    from .session import SessionDictMode, SessionObjectMode

__all__ = [
    "HistoricalStatistics",
    "RealtimeProxyStatistics",
    "RealtimeStatistics",
    "FortiviewDictMode",
    "FortiviewObjectMode",
]

class FortiviewDictMode:
    """FORTIVIEW API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    session: SessionDictMode
    historical_statistics: HistoricalStatisticsDictMode
    realtime_proxy_statistics: RealtimeProxyStatisticsDictMode
    realtime_statistics: RealtimeStatisticsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiview category with HTTP client."""
        ...


class FortiviewObjectMode:
    """FORTIVIEW API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    session: SessionObjectMode
    historical_statistics: HistoricalStatisticsObjectMode
    realtime_proxy_statistics: RealtimeProxyStatisticsObjectMode
    realtime_statistics: RealtimeStatisticsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiview category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fortiview:
    """FORTIVIEW API category."""
    
    session: Session
    historical_statistics: HistoricalStatistics
    realtime_proxy_statistics: RealtimeProxyStatistics
    realtime_statistics: RealtimeStatistics

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiview category with HTTP client."""
        ...
