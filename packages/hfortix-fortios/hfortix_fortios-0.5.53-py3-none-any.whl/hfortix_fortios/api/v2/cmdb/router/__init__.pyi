"""Type stubs for ROUTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .access_list import AccessList, AccessListDictMode, AccessListObjectMode
    from .access_list6 import AccessList6, AccessList6DictMode, AccessList6ObjectMode
    from .aspath_list import AspathList, AspathListDictMode, AspathListObjectMode
    from .auth_path import AuthPath, AuthPathDictMode, AuthPathObjectMode
    from .bfd import Bfd, BfdDictMode, BfdObjectMode
    from .bfd6 import Bfd6, Bfd6DictMode, Bfd6ObjectMode
    from .bgp import Bgp, BgpDictMode, BgpObjectMode
    from .community_list import CommunityList, CommunityListDictMode, CommunityListObjectMode
    from .extcommunity_list import ExtcommunityList, ExtcommunityListDictMode, ExtcommunityListObjectMode
    from .isis import Isis, IsisDictMode, IsisObjectMode
    from .key_chain import KeyChain, KeyChainDictMode, KeyChainObjectMode
    from .multicast import Multicast, MulticastDictMode, MulticastObjectMode
    from .multicast6 import Multicast6, Multicast6DictMode, Multicast6ObjectMode
    from .multicast_flow import MulticastFlow, MulticastFlowDictMode, MulticastFlowObjectMode
    from .ospf import Ospf, OspfDictMode, OspfObjectMode
    from .ospf6 import Ospf6, Ospf6DictMode, Ospf6ObjectMode
    from .policy import Policy, PolicyDictMode, PolicyObjectMode
    from .policy6 import Policy6, Policy6DictMode, Policy6ObjectMode
    from .prefix_list import PrefixList, PrefixListDictMode, PrefixListObjectMode
    from .prefix_list6 import PrefixList6, PrefixList6DictMode, PrefixList6ObjectMode
    from .rip import Rip, RipDictMode, RipObjectMode
    from .ripng import Ripng, RipngDictMode, RipngObjectMode
    from .route_map import RouteMap, RouteMapDictMode, RouteMapObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode
    from .static import Static, StaticDictMode, StaticObjectMode
    from .static6 import Static6, Static6DictMode, Static6ObjectMode

__all__ = [
    "AccessList",
    "AccessList6",
    "AspathList",
    "AuthPath",
    "Bfd",
    "Bfd6",
    "Bgp",
    "CommunityList",
    "ExtcommunityList",
    "Isis",
    "KeyChain",
    "Multicast",
    "Multicast6",
    "MulticastFlow",
    "Ospf",
    "Ospf6",
    "Policy",
    "Policy6",
    "PrefixList",
    "PrefixList6",
    "Rip",
    "Ripng",
    "RouteMap",
    "Setting",
    "Static",
    "Static6",
    "RouterDictMode",
    "RouterObjectMode",
]

class RouterDictMode:
    """ROUTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    access_list: AccessListDictMode
    access_list6: AccessList6DictMode
    aspath_list: AspathListDictMode
    auth_path: AuthPathDictMode
    bfd: BfdDictMode
    bfd6: Bfd6DictMode
    bgp: BgpDictMode
    community_list: CommunityListDictMode
    extcommunity_list: ExtcommunityListDictMode
    isis: IsisDictMode
    key_chain: KeyChainDictMode
    multicast: MulticastDictMode
    multicast6: Multicast6DictMode
    multicast_flow: MulticastFlowDictMode
    ospf: OspfDictMode
    ospf6: Ospf6DictMode
    policy: PolicyDictMode
    policy6: Policy6DictMode
    prefix_list: PrefixListDictMode
    prefix_list6: PrefixList6DictMode
    rip: RipDictMode
    ripng: RipngDictMode
    route_map: RouteMapDictMode
    setting: SettingDictMode
    static: StaticDictMode
    static6: Static6DictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize router category with HTTP client."""
        ...


class RouterObjectMode:
    """ROUTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    access_list: AccessListObjectMode
    access_list6: AccessList6ObjectMode
    aspath_list: AspathListObjectMode
    auth_path: AuthPathObjectMode
    bfd: BfdObjectMode
    bfd6: Bfd6ObjectMode
    bgp: BgpObjectMode
    community_list: CommunityListObjectMode
    extcommunity_list: ExtcommunityListObjectMode
    isis: IsisObjectMode
    key_chain: KeyChainObjectMode
    multicast: MulticastObjectMode
    multicast6: Multicast6ObjectMode
    multicast_flow: MulticastFlowObjectMode
    ospf: OspfObjectMode
    ospf6: Ospf6ObjectMode
    policy: PolicyObjectMode
    policy6: Policy6ObjectMode
    prefix_list: PrefixListObjectMode
    prefix_list6: PrefixList6ObjectMode
    rip: RipObjectMode
    ripng: RipngObjectMode
    route_map: RouteMapObjectMode
    setting: SettingObjectMode
    static: StaticObjectMode
    static6: Static6ObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize router category with HTTP client."""
        ...


# Base class for backwards compatibility
class Router:
    """ROUTER API category."""
    
    access_list: AccessList
    access_list6: AccessList6
    aspath_list: AspathList
    auth_path: AuthPath
    bfd: Bfd
    bfd6: Bfd6
    bgp: Bgp
    community_list: CommunityList
    extcommunity_list: ExtcommunityList
    isis: Isis
    key_chain: KeyChain
    multicast: Multicast
    multicast6: Multicast6
    multicast_flow: MulticastFlow
    ospf: Ospf
    ospf6: Ospf6
    policy: Policy
    policy6: Policy6
    prefix_list: PrefixList
    prefix_list6: PrefixList6
    rip: Rip
    ripng: Ripng
    route_map: RouteMap
    setting: Setting
    static: Static
    static6: Static6

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize router category with HTTP client."""
        ...
