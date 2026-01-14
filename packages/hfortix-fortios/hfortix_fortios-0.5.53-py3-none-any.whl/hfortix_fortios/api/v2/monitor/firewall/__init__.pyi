"""Type stubs for FIREWALL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .address6_dynamic import Address6Dynamic, Address6DynamicDictMode, Address6DynamicObjectMode
    from .address_dynamic import AddressDynamic, AddressDynamicDictMode, AddressDynamicObjectMode
    from .address_fqdns import AddressFqdns, AddressFqdnsDictMode, AddressFqdnsObjectMode
    from .address_fqdns6 import AddressFqdns6, AddressFqdns6DictMode, AddressFqdns6ObjectMode
    from .check_addrgrp_exclude_mac_member import CheckAddrgrpExcludeMacMember, CheckAddrgrpExcludeMacMemberDictMode, CheckAddrgrpExcludeMacMemberObjectMode
    from .gtp_runtime_statistics import GtpRuntimeStatistics, GtpRuntimeStatisticsDictMode, GtpRuntimeStatisticsObjectMode
    from .gtp_statistics import GtpStatistics, GtpStatisticsDictMode, GtpStatisticsObjectMode
    from .health import Health, HealthDictMode, HealthObjectMode
    from .internet_service_basic import InternetServiceBasic, InternetServiceBasicDictMode, InternetServiceBasicObjectMode
    from .internet_service_details import InternetServiceDetails, InternetServiceDetailsDictMode, InternetServiceDetailsObjectMode
    from .internet_service_fqdn import InternetServiceFqdn, InternetServiceFqdnDictMode, InternetServiceFqdnObjectMode
    from .internet_service_fqdn_icon_ids import InternetServiceFqdnIconIds, InternetServiceFqdnIconIdsDictMode, InternetServiceFqdnIconIdsObjectMode
    from .internet_service_match import InternetServiceMatch, InternetServiceMatchDictMode, InternetServiceMatchObjectMode
    from .internet_service_reputation import InternetServiceReputation, InternetServiceReputationDictMode, InternetServiceReputationObjectMode
    from .load_balance import LoadBalance, LoadBalanceDictMode, LoadBalanceObjectMode
    from .local_in import LocalIn, LocalInDictMode, LocalInObjectMode
    from .local_in6 import LocalIn6, LocalIn6DictMode, LocalIn6ObjectMode
    from .network_service_dynamic import NetworkServiceDynamic, NetworkServiceDynamicDictMode, NetworkServiceDynamicObjectMode
    from .policy_lookup import PolicyLookup, PolicyLookupDictMode, PolicyLookupObjectMode
    from .saas_application import SaasApplication, SaasApplicationDictMode, SaasApplicationObjectMode
    from .sdn_connector_filters import SdnConnectorFilters, SdnConnectorFiltersDictMode, SdnConnectorFiltersObjectMode
    from .sessions import Sessions, SessionsDictMode, SessionsObjectMode
    from .uuid_list import UuidList, UuidListDictMode, UuidListObjectMode
    from .uuid_type_lookup import UuidTypeLookup, UuidTypeLookupDictMode, UuidTypeLookupObjectMode
    from .vip_overlap import VipOverlap, VipOverlapDictMode, VipOverlapObjectMode
    from .acl import Acl
    from .acl6 import Acl6
    from .central_snat_map import CentralSnatMap
    from .clearpass_address import ClearpassAddress
    from .dnat import Dnat
    from .gtp import Gtp
    from .ippool import Ippool
    from .multicast_policy import MulticastPolicy
    from .multicast_policy6 import MulticastPolicy6
    from .per_ip_shaper import PerIpShaper
    from .policy import Policy
    from .proxy import ProxyDictMode, ProxyObjectMode
    from .proxy_policy import ProxyPolicy
    from .security_policy import SecurityPolicy
    from .session import SessionDictMode, SessionObjectMode
    from .session6 import Session6DictMode, Session6ObjectMode
    from .shaper import Shaper
    from .ztna_firewall_policy import ZtnaFirewallPolicy

__all__ = [
    "Address6Dynamic",
    "AddressDynamic",
    "AddressFqdns",
    "AddressFqdns6",
    "CheckAddrgrpExcludeMacMember",
    "GtpRuntimeStatistics",
    "GtpStatistics",
    "Health",
    "InternetServiceBasic",
    "InternetServiceDetails",
    "InternetServiceFqdn",
    "InternetServiceFqdnIconIds",
    "InternetServiceMatch",
    "InternetServiceReputation",
    "LoadBalance",
    "LocalIn",
    "LocalIn6",
    "NetworkServiceDynamic",
    "PolicyLookup",
    "SaasApplication",
    "SdnConnectorFilters",
    "Sessions",
    "UuidList",
    "UuidTypeLookup",
    "VipOverlap",
    "FirewallDictMode",
    "FirewallObjectMode",
]

class FirewallDictMode:
    """FIREWALL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    acl: Acl
    acl6: Acl6
    central_snat_map: CentralSnatMap
    clearpass_address: ClearpassAddress
    dnat: Dnat
    gtp: Gtp
    ippool: Ippool
    multicast_policy: MulticastPolicy
    multicast_policy6: MulticastPolicy6
    per_ip_shaper: PerIpShaper
    policy: Policy
    proxy: ProxyDictMode
    proxy_policy: ProxyPolicy
    security_policy: SecurityPolicy
    session: SessionDictMode
    session6: Session6DictMode
    shaper: Shaper
    ztna_firewall_policy: ZtnaFirewallPolicy
    address6_dynamic: Address6DynamicDictMode
    address_dynamic: AddressDynamicDictMode
    address_fqdns: AddressFqdnsDictMode
    address_fqdns6: AddressFqdns6DictMode
    check_addrgrp_exclude_mac_member: CheckAddrgrpExcludeMacMemberDictMode
    gtp_runtime_statistics: GtpRuntimeStatisticsDictMode
    gtp_statistics: GtpStatisticsDictMode
    health: HealthDictMode
    internet_service_basic: InternetServiceBasicDictMode
    internet_service_details: InternetServiceDetailsDictMode
    internet_service_fqdn: InternetServiceFqdnDictMode
    internet_service_fqdn_icon_ids: InternetServiceFqdnIconIdsDictMode
    internet_service_match: InternetServiceMatchDictMode
    internet_service_reputation: InternetServiceReputationDictMode
    load_balance: LoadBalanceDictMode
    local_in: LocalInDictMode
    local_in6: LocalIn6DictMode
    network_service_dynamic: NetworkServiceDynamicDictMode
    policy_lookup: PolicyLookupDictMode
    saas_application: SaasApplicationDictMode
    sdn_connector_filters: SdnConnectorFiltersDictMode
    sessions: SessionsDictMode
    uuid_list: UuidListDictMode
    uuid_type_lookup: UuidTypeLookupDictMode
    vip_overlap: VipOverlapDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firewall category with HTTP client."""
        ...


class FirewallObjectMode:
    """FIREWALL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    acl: Acl
    acl6: Acl6
    central_snat_map: CentralSnatMap
    clearpass_address: ClearpassAddress
    dnat: Dnat
    gtp: Gtp
    ippool: Ippool
    multicast_policy: MulticastPolicy
    multicast_policy6: MulticastPolicy6
    per_ip_shaper: PerIpShaper
    policy: Policy
    proxy: ProxyObjectMode
    proxy_policy: ProxyPolicy
    security_policy: SecurityPolicy
    session: SessionObjectMode
    session6: Session6ObjectMode
    shaper: Shaper
    ztna_firewall_policy: ZtnaFirewallPolicy
    address6_dynamic: Address6DynamicObjectMode
    address_dynamic: AddressDynamicObjectMode
    address_fqdns: AddressFqdnsObjectMode
    address_fqdns6: AddressFqdns6ObjectMode
    check_addrgrp_exclude_mac_member: CheckAddrgrpExcludeMacMemberObjectMode
    gtp_runtime_statistics: GtpRuntimeStatisticsObjectMode
    gtp_statistics: GtpStatisticsObjectMode
    health: HealthObjectMode
    internet_service_basic: InternetServiceBasicObjectMode
    internet_service_details: InternetServiceDetailsObjectMode
    internet_service_fqdn: InternetServiceFqdnObjectMode
    internet_service_fqdn_icon_ids: InternetServiceFqdnIconIdsObjectMode
    internet_service_match: InternetServiceMatchObjectMode
    internet_service_reputation: InternetServiceReputationObjectMode
    load_balance: LoadBalanceObjectMode
    local_in: LocalInObjectMode
    local_in6: LocalIn6ObjectMode
    network_service_dynamic: NetworkServiceDynamicObjectMode
    policy_lookup: PolicyLookupObjectMode
    saas_application: SaasApplicationObjectMode
    sdn_connector_filters: SdnConnectorFiltersObjectMode
    sessions: SessionsObjectMode
    uuid_list: UuidListObjectMode
    uuid_type_lookup: UuidTypeLookupObjectMode
    vip_overlap: VipOverlapObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firewall category with HTTP client."""
        ...


# Base class for backwards compatibility
class Firewall:
    """FIREWALL API category."""
    
    acl: Acl
    acl6: Acl6
    central_snat_map: CentralSnatMap
    clearpass_address: ClearpassAddress
    dnat: Dnat
    gtp: Gtp
    ippool: Ippool
    multicast_policy: MulticastPolicy
    multicast_policy6: MulticastPolicy6
    per_ip_shaper: PerIpShaper
    policy: Policy
    proxy: Proxy
    proxy_policy: ProxyPolicy
    security_policy: SecurityPolicy
    session: Session
    session6: Session6
    shaper: Shaper
    ztna_firewall_policy: ZtnaFirewallPolicy
    address6_dynamic: Address6Dynamic
    address_dynamic: AddressDynamic
    address_fqdns: AddressFqdns
    address_fqdns6: AddressFqdns6
    check_addrgrp_exclude_mac_member: CheckAddrgrpExcludeMacMember
    gtp_runtime_statistics: GtpRuntimeStatistics
    gtp_statistics: GtpStatistics
    health: Health
    internet_service_basic: InternetServiceBasic
    internet_service_details: InternetServiceDetails
    internet_service_fqdn: InternetServiceFqdn
    internet_service_fqdn_icon_ids: InternetServiceFqdnIconIds
    internet_service_match: InternetServiceMatch
    internet_service_reputation: InternetServiceReputation
    load_balance: LoadBalance
    local_in: LocalIn
    local_in6: LocalIn6
    network_service_dynamic: NetworkServiceDynamic
    policy_lookup: PolicyLookup
    saas_application: SaasApplication
    sdn_connector_filters: SdnConnectorFilters
    sessions: Sessions
    uuid_list: UuidList
    uuid_type_lookup: UuidTypeLookup
    vip_overlap: VipOverlap

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firewall category with HTTP client."""
        ...
