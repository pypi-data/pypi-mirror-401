"""Type stubs for ROUTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .charts import Charts, ChartsDictMode, ChartsObjectMode
    from .ipv4 import Ipv4, Ipv4DictMode, Ipv4ObjectMode
    from .ipv6 import Ipv6, Ipv6DictMode, Ipv6ObjectMode
    from .lookup_policy import LookupPolicy, LookupPolicyDictMode, LookupPolicyObjectMode
    from .policy import Policy, PolicyDictMode, PolicyObjectMode
    from .policy6 import Policy6, Policy6DictMode, Policy6ObjectMode
    from .statistics import Statistics, StatisticsDictMode, StatisticsObjectMode
    from .bgp import BgpDictMode, BgpObjectMode
    from .lookup import Lookup
    from .ospf import OspfDictMode, OspfObjectMode
    from .sdwan import SdwanDictMode, SdwanObjectMode

__all__ = [
    "Charts",
    "Ipv4",
    "Ipv6",
    "LookupPolicy",
    "Policy",
    "Policy6",
    "Statistics",
    "RouterDictMode",
    "RouterObjectMode",
]

class RouterDictMode:
    """ROUTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    bgp: BgpDictMode
    lookup: Lookup
    ospf: OspfDictMode
    sdwan: SdwanDictMode
    charts: ChartsDictMode
    ipv4: Ipv4DictMode
    ipv6: Ipv6DictMode
    lookup_policy: LookupPolicyDictMode
    policy: PolicyDictMode
    policy6: Policy6DictMode
    statistics: StatisticsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize router category with HTTP client."""
        ...


class RouterObjectMode:
    """ROUTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    bgp: BgpObjectMode
    lookup: Lookup
    ospf: OspfObjectMode
    sdwan: SdwanObjectMode
    charts: ChartsObjectMode
    ipv4: Ipv4ObjectMode
    ipv6: Ipv6ObjectMode
    lookup_policy: LookupPolicyObjectMode
    policy: PolicyObjectMode
    policy6: Policy6ObjectMode
    statistics: StatisticsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize router category with HTTP client."""
        ...


# Base class for backwards compatibility
class Router:
    """ROUTER API category."""
    
    bgp: Bgp
    lookup: Lookup
    ospf: Ospf
    sdwan: Sdwan
    charts: Charts
    ipv4: Ipv4
    ipv6: Ipv6
    lookup_policy: LookupPolicy
    policy: Policy
    policy6: Policy6
    statistics: Statistics

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize router category with HTTP client."""
        ...
