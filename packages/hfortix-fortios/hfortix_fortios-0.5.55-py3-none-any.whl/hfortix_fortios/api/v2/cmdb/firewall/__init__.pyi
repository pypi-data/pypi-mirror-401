"""Type stubs for FIREWALL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .DoS_policy import DosPolicy, DosPolicyDictMode, DosPolicyObjectMode
    from .DoS_policy6 import DosPolicy6, DosPolicy6DictMode, DosPolicy6ObjectMode
    from .access_proxy import AccessProxy, AccessProxyDictMode, AccessProxyObjectMode
    from .access_proxy6 import AccessProxy6, AccessProxy6DictMode, AccessProxy6ObjectMode
    from .access_proxy_ssh_client_cert import AccessProxySshClientCert, AccessProxySshClientCertDictMode, AccessProxySshClientCertObjectMode
    from .access_proxy_virtual_host import AccessProxyVirtualHost, AccessProxyVirtualHostDictMode, AccessProxyVirtualHostObjectMode
    from .address import Address, AddressDictMode, AddressObjectMode
    from .address6 import Address6, Address6DictMode, Address6ObjectMode
    from .address6_template import Address6Template, Address6TemplateDictMode, Address6TemplateObjectMode
    from .addrgrp import Addrgrp, AddrgrpDictMode, AddrgrpObjectMode
    from .addrgrp6 import Addrgrp6, Addrgrp6DictMode, Addrgrp6ObjectMode
    from .auth_portal import AuthPortal, AuthPortalDictMode, AuthPortalObjectMode
    from .central_snat_map import CentralSnatMap, CentralSnatMapDictMode, CentralSnatMapObjectMode
    from .city import City, CityDictMode, CityObjectMode
    from .country import Country, CountryDictMode, CountryObjectMode
    from .decrypted_traffic_mirror import DecryptedTrafficMirror, DecryptedTrafficMirrorDictMode, DecryptedTrafficMirrorObjectMode
    from .dnstranslation import Dnstranslation, DnstranslationDictMode, DnstranslationObjectMode
    from .global_ import Global, GlobalDictMode, GlobalObjectMode
    from .identity_based_route import IdentityBasedRoute, IdentityBasedRouteDictMode, IdentityBasedRouteObjectMode
    from .interface_policy import InterfacePolicy, InterfacePolicyDictMode, InterfacePolicyObjectMode
    from .interface_policy6 import InterfacePolicy6, InterfacePolicy6DictMode, InterfacePolicy6ObjectMode
    from .internet_service import InternetService, InternetServiceDictMode, InternetServiceObjectMode
    from .internet_service_addition import InternetServiceAddition, InternetServiceAdditionDictMode, InternetServiceAdditionObjectMode
    from .internet_service_append import InternetServiceAppend, InternetServiceAppendDictMode, InternetServiceAppendObjectMode
    from .internet_service_botnet import InternetServiceBotnet, InternetServiceBotnetDictMode, InternetServiceBotnetObjectMode
    from .internet_service_custom import InternetServiceCustom, InternetServiceCustomDictMode, InternetServiceCustomObjectMode
    from .internet_service_custom_group import InternetServiceCustomGroup, InternetServiceCustomGroupDictMode, InternetServiceCustomGroupObjectMode
    from .internet_service_definition import InternetServiceDefinition, InternetServiceDefinitionDictMode, InternetServiceDefinitionObjectMode
    from .internet_service_extension import InternetServiceExtension, InternetServiceExtensionDictMode, InternetServiceExtensionObjectMode
    from .internet_service_fortiguard import InternetServiceFortiguard, InternetServiceFortiguardDictMode, InternetServiceFortiguardObjectMode
    from .internet_service_group import InternetServiceGroup, InternetServiceGroupDictMode, InternetServiceGroupObjectMode
    from .internet_service_ipbl_reason import InternetServiceIpblReason, InternetServiceIpblReasonDictMode, InternetServiceIpblReasonObjectMode
    from .internet_service_ipbl_vendor import InternetServiceIpblVendor, InternetServiceIpblVendorDictMode, InternetServiceIpblVendorObjectMode
    from .internet_service_list import InternetServiceList, InternetServiceListDictMode, InternetServiceListObjectMode
    from .internet_service_name import InternetServiceName, InternetServiceNameDictMode, InternetServiceNameObjectMode
    from .internet_service_owner import InternetServiceOwner, InternetServiceOwnerDictMode, InternetServiceOwnerObjectMode
    from .internet_service_reputation import InternetServiceReputation, InternetServiceReputationDictMode, InternetServiceReputationObjectMode
    from .internet_service_sld import InternetServiceSld, InternetServiceSldDictMode, InternetServiceSldObjectMode
    from .internet_service_subapp import InternetServiceSubapp, InternetServiceSubappDictMode, InternetServiceSubappObjectMode
    from .ip_translation import IpTranslation, IpTranslationDictMode, IpTranslationObjectMode
    from .ippool import Ippool, IppoolDictMode, IppoolObjectMode
    from .ippool6 import Ippool6, Ippool6DictMode, Ippool6ObjectMode
    from .ldb_monitor import LdbMonitor, LdbMonitorDictMode, LdbMonitorObjectMode
    from .local_in_policy import LocalInPolicy, LocalInPolicyDictMode, LocalInPolicyObjectMode
    from .local_in_policy6 import LocalInPolicy6, LocalInPolicy6DictMode, LocalInPolicy6ObjectMode
    from .multicast_address import MulticastAddress, MulticastAddressDictMode, MulticastAddressObjectMode
    from .multicast_address6 import MulticastAddress6, MulticastAddress6DictMode, MulticastAddress6ObjectMode
    from .multicast_policy import MulticastPolicy, MulticastPolicyDictMode, MulticastPolicyObjectMode
    from .multicast_policy6 import MulticastPolicy6, MulticastPolicy6DictMode, MulticastPolicy6ObjectMode
    from .network_service_dynamic import NetworkServiceDynamic, NetworkServiceDynamicDictMode, NetworkServiceDynamicObjectMode
    from .on_demand_sniffer import OnDemandSniffer, OnDemandSnifferDictMode, OnDemandSnifferObjectMode
    from .policy import Policy, PolicyDictMode, PolicyObjectMode
    from .profile_group import ProfileGroup, ProfileGroupDictMode, ProfileGroupObjectMode
    from .profile_protocol_options import ProfileProtocolOptions, ProfileProtocolOptionsDictMode, ProfileProtocolOptionsObjectMode
    from .proxy_address import ProxyAddress, ProxyAddressDictMode, ProxyAddressObjectMode
    from .proxy_addrgrp import ProxyAddrgrp, ProxyAddrgrpDictMode, ProxyAddrgrpObjectMode
    from .proxy_policy import ProxyPolicy, ProxyPolicyDictMode, ProxyPolicyObjectMode
    from .region import Region, RegionDictMode, RegionObjectMode
    from .security_policy import SecurityPolicy, SecurityPolicyDictMode, SecurityPolicyObjectMode
    from .shaping_policy import ShapingPolicy, ShapingPolicyDictMode, ShapingPolicyObjectMode
    from .shaping_profile import ShapingProfile, ShapingProfileDictMode, ShapingProfileObjectMode
    from .sniffer import Sniffer, SnifferDictMode, SnifferObjectMode
    from .ssl_server import SslServer, SslServerDictMode, SslServerObjectMode
    from .ssl_ssh_profile import SslSshProfile, SslSshProfileDictMode, SslSshProfileObjectMode
    from .traffic_class import TrafficClass, TrafficClassDictMode, TrafficClassObjectMode
    from .ttl_policy import TtlPolicy, TtlPolicyDictMode, TtlPolicyObjectMode
    from .vendor_mac import VendorMac, VendorMacDictMode, VendorMacObjectMode
    from .vendor_mac_summary import VendorMacSummary, VendorMacSummaryDictMode, VendorMacSummaryObjectMode
    from .vip import Vip, VipDictMode, VipObjectMode
    from .vip6 import Vip6, Vip6DictMode, Vip6ObjectMode
    from .vipgrp import Vipgrp, VipgrpDictMode, VipgrpObjectMode
    from .vipgrp6 import Vipgrp6, Vipgrp6DictMode, Vipgrp6ObjectMode
    from .ipmacbinding import IpmacbindingDictMode, IpmacbindingObjectMode
    from .schedule import ScheduleDictMode, ScheduleObjectMode
    from .service import ServiceDictMode, ServiceObjectMode
    from .shaper import ShaperDictMode, ShaperObjectMode
    from .ssh import SshDictMode, SshObjectMode
    from .ssl import SslDictMode, SslObjectMode
    from .wildcard_fqdn import WildcardFqdn

__all__ = [
    "DosPolicy",
    "DosPolicy6",
    "AccessProxy",
    "AccessProxy6",
    "AccessProxySshClientCert",
    "AccessProxyVirtualHost",
    "Address",
    "Address6",
    "Address6Template",
    "Addrgrp",
    "Addrgrp6",
    "AuthPortal",
    "CentralSnatMap",
    "City",
    "Country",
    "DecryptedTrafficMirror",
    "Dnstranslation",
    "Global",
    "IdentityBasedRoute",
    "InterfacePolicy",
    "InterfacePolicy6",
    "InternetService",
    "InternetServiceAddition",
    "InternetServiceAppend",
    "InternetServiceBotnet",
    "InternetServiceCustom",
    "InternetServiceCustomGroup",
    "InternetServiceDefinition",
    "InternetServiceExtension",
    "InternetServiceFortiguard",
    "InternetServiceGroup",
    "InternetServiceIpblReason",
    "InternetServiceIpblVendor",
    "InternetServiceList",
    "InternetServiceName",
    "InternetServiceOwner",
    "InternetServiceReputation",
    "InternetServiceSld",
    "InternetServiceSubapp",
    "IpTranslation",
    "Ippool",
    "Ippool6",
    "LdbMonitor",
    "LocalInPolicy",
    "LocalInPolicy6",
    "MulticastAddress",
    "MulticastAddress6",
    "MulticastPolicy",
    "MulticastPolicy6",
    "NetworkServiceDynamic",
    "OnDemandSniffer",
    "Policy",
    "ProfileGroup",
    "ProfileProtocolOptions",
    "ProxyAddress",
    "ProxyAddrgrp",
    "ProxyPolicy",
    "Region",
    "SecurityPolicy",
    "ShapingPolicy",
    "ShapingProfile",
    "Sniffer",
    "SslServer",
    "SslSshProfile",
    "TrafficClass",
    "TtlPolicy",
    "VendorMac",
    "VendorMacSummary",
    "Vip",
    "Vip6",
    "Vipgrp",
    "Vipgrp6",
    "FirewallDictMode",
    "FirewallObjectMode",
]

class FirewallDictMode:
    """FIREWALL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ipmacbinding: IpmacbindingDictMode
    schedule: ScheduleDictMode
    service: ServiceDictMode
    shaper: ShaperDictMode
    ssh: SshDictMode
    ssl: SslDictMode
    wildcard_fqdn: WildcardFqdn
    DoS_policy: DosPolicyDictMode
    DoS_policy6: DosPolicy6DictMode
    access_proxy: AccessProxyDictMode
    access_proxy6: AccessProxy6DictMode
    access_proxy_ssh_client_cert: AccessProxySshClientCertDictMode
    access_proxy_virtual_host: AccessProxyVirtualHostDictMode
    address: AddressDictMode
    address6: Address6DictMode
    address6_template: Address6TemplateDictMode
    addrgrp: AddrgrpDictMode
    addrgrp6: Addrgrp6DictMode
    auth_portal: AuthPortalDictMode
    central_snat_map: CentralSnatMapDictMode
    city: CityDictMode
    country: CountryDictMode
    decrypted_traffic_mirror: DecryptedTrafficMirrorDictMode
    dnstranslation: DnstranslationDictMode
    global_: GlobalDictMode
    identity_based_route: IdentityBasedRouteDictMode
    interface_policy: InterfacePolicyDictMode
    interface_policy6: InterfacePolicy6DictMode
    internet_service: InternetServiceDictMode
    internet_service_addition: InternetServiceAdditionDictMode
    internet_service_append: InternetServiceAppendDictMode
    internet_service_botnet: InternetServiceBotnetDictMode
    internet_service_custom: InternetServiceCustomDictMode
    internet_service_custom_group: InternetServiceCustomGroupDictMode
    internet_service_definition: InternetServiceDefinitionDictMode
    internet_service_extension: InternetServiceExtensionDictMode
    internet_service_fortiguard: InternetServiceFortiguardDictMode
    internet_service_group: InternetServiceGroupDictMode
    internet_service_ipbl_reason: InternetServiceIpblReasonDictMode
    internet_service_ipbl_vendor: InternetServiceIpblVendorDictMode
    internet_service_list: InternetServiceListDictMode
    internet_service_name: InternetServiceNameDictMode
    internet_service_owner: InternetServiceOwnerDictMode
    internet_service_reputation: InternetServiceReputationDictMode
    internet_service_sld: InternetServiceSldDictMode
    internet_service_subapp: InternetServiceSubappDictMode
    ip_translation: IpTranslationDictMode
    ippool: IppoolDictMode
    ippool6: Ippool6DictMode
    ldb_monitor: LdbMonitorDictMode
    local_in_policy: LocalInPolicyDictMode
    local_in_policy6: LocalInPolicy6DictMode
    multicast_address: MulticastAddressDictMode
    multicast_address6: MulticastAddress6DictMode
    multicast_policy: MulticastPolicyDictMode
    multicast_policy6: MulticastPolicy6DictMode
    network_service_dynamic: NetworkServiceDynamicDictMode
    on_demand_sniffer: OnDemandSnifferDictMode
    policy: PolicyDictMode
    profile_group: ProfileGroupDictMode
    profile_protocol_options: ProfileProtocolOptionsDictMode
    proxy_address: ProxyAddressDictMode
    proxy_addrgrp: ProxyAddrgrpDictMode
    proxy_policy: ProxyPolicyDictMode
    region: RegionDictMode
    security_policy: SecurityPolicyDictMode
    shaping_policy: ShapingPolicyDictMode
    shaping_profile: ShapingProfileDictMode
    sniffer: SnifferDictMode
    ssl_server: SslServerDictMode
    ssl_ssh_profile: SslSshProfileDictMode
    traffic_class: TrafficClassDictMode
    ttl_policy: TtlPolicyDictMode
    vendor_mac: VendorMacDictMode
    vendor_mac_summary: VendorMacSummaryDictMode
    vip: VipDictMode
    vip6: Vip6DictMode
    vipgrp: VipgrpDictMode
    vipgrp6: Vipgrp6DictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firewall category with HTTP client."""
        ...


class FirewallObjectMode:
    """FIREWALL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ipmacbinding: IpmacbindingObjectMode
    schedule: ScheduleObjectMode
    service: ServiceObjectMode
    shaper: ShaperObjectMode
    ssh: SshObjectMode
    ssl: SslObjectMode
    wildcard_fqdn: WildcardFqdn
    DoS_policy: DosPolicyObjectMode
    DoS_policy6: DosPolicy6ObjectMode
    access_proxy: AccessProxyObjectMode
    access_proxy6: AccessProxy6ObjectMode
    access_proxy_ssh_client_cert: AccessProxySshClientCertObjectMode
    access_proxy_virtual_host: AccessProxyVirtualHostObjectMode
    address: AddressObjectMode
    address6: Address6ObjectMode
    address6_template: Address6TemplateObjectMode
    addrgrp: AddrgrpObjectMode
    addrgrp6: Addrgrp6ObjectMode
    auth_portal: AuthPortalObjectMode
    central_snat_map: CentralSnatMapObjectMode
    city: CityObjectMode
    country: CountryObjectMode
    decrypted_traffic_mirror: DecryptedTrafficMirrorObjectMode
    dnstranslation: DnstranslationObjectMode
    global_: GlobalObjectMode
    identity_based_route: IdentityBasedRouteObjectMode
    interface_policy: InterfacePolicyObjectMode
    interface_policy6: InterfacePolicy6ObjectMode
    internet_service: InternetServiceObjectMode
    internet_service_addition: InternetServiceAdditionObjectMode
    internet_service_append: InternetServiceAppendObjectMode
    internet_service_botnet: InternetServiceBotnetObjectMode
    internet_service_custom: InternetServiceCustomObjectMode
    internet_service_custom_group: InternetServiceCustomGroupObjectMode
    internet_service_definition: InternetServiceDefinitionObjectMode
    internet_service_extension: InternetServiceExtensionObjectMode
    internet_service_fortiguard: InternetServiceFortiguardObjectMode
    internet_service_group: InternetServiceGroupObjectMode
    internet_service_ipbl_reason: InternetServiceIpblReasonObjectMode
    internet_service_ipbl_vendor: InternetServiceIpblVendorObjectMode
    internet_service_list: InternetServiceListObjectMode
    internet_service_name: InternetServiceNameObjectMode
    internet_service_owner: InternetServiceOwnerObjectMode
    internet_service_reputation: InternetServiceReputationObjectMode
    internet_service_sld: InternetServiceSldObjectMode
    internet_service_subapp: InternetServiceSubappObjectMode
    ip_translation: IpTranslationObjectMode
    ippool: IppoolObjectMode
    ippool6: Ippool6ObjectMode
    ldb_monitor: LdbMonitorObjectMode
    local_in_policy: LocalInPolicyObjectMode
    local_in_policy6: LocalInPolicy6ObjectMode
    multicast_address: MulticastAddressObjectMode
    multicast_address6: MulticastAddress6ObjectMode
    multicast_policy: MulticastPolicyObjectMode
    multicast_policy6: MulticastPolicy6ObjectMode
    network_service_dynamic: NetworkServiceDynamicObjectMode
    on_demand_sniffer: OnDemandSnifferObjectMode
    policy: PolicyObjectMode
    profile_group: ProfileGroupObjectMode
    profile_protocol_options: ProfileProtocolOptionsObjectMode
    proxy_address: ProxyAddressObjectMode
    proxy_addrgrp: ProxyAddrgrpObjectMode
    proxy_policy: ProxyPolicyObjectMode
    region: RegionObjectMode
    security_policy: SecurityPolicyObjectMode
    shaping_policy: ShapingPolicyObjectMode
    shaping_profile: ShapingProfileObjectMode
    sniffer: SnifferObjectMode
    ssl_server: SslServerObjectMode
    ssl_ssh_profile: SslSshProfileObjectMode
    traffic_class: TrafficClassObjectMode
    ttl_policy: TtlPolicyObjectMode
    vendor_mac: VendorMacObjectMode
    vendor_mac_summary: VendorMacSummaryObjectMode
    vip: VipObjectMode
    vip6: Vip6ObjectMode
    vipgrp: VipgrpObjectMode
    vipgrp6: Vipgrp6ObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firewall category with HTTP client."""
        ...


# Base class for backwards compatibility
class Firewall:
    """FIREWALL API category."""
    
    ipmacbinding: Ipmacbinding
    schedule: Schedule
    service: Service
    shaper: Shaper
    ssh: Ssh
    ssl: Ssl
    wildcard_fqdn: WildcardFqdn
    DoS_policy: DosPolicy
    DoS_policy6: DosPolicy6
    access_proxy: AccessProxy
    access_proxy6: AccessProxy6
    access_proxy_ssh_client_cert: AccessProxySshClientCert
    access_proxy_virtual_host: AccessProxyVirtualHost
    address: Address
    address6: Address6
    address6_template: Address6Template
    addrgrp: Addrgrp
    addrgrp6: Addrgrp6
    auth_portal: AuthPortal
    central_snat_map: CentralSnatMap
    city: City
    country: Country
    decrypted_traffic_mirror: DecryptedTrafficMirror
    dnstranslation: Dnstranslation
    global_: Global
    identity_based_route: IdentityBasedRoute
    interface_policy: InterfacePolicy
    interface_policy6: InterfacePolicy6
    internet_service: InternetService
    internet_service_addition: InternetServiceAddition
    internet_service_append: InternetServiceAppend
    internet_service_botnet: InternetServiceBotnet
    internet_service_custom: InternetServiceCustom
    internet_service_custom_group: InternetServiceCustomGroup
    internet_service_definition: InternetServiceDefinition
    internet_service_extension: InternetServiceExtension
    internet_service_fortiguard: InternetServiceFortiguard
    internet_service_group: InternetServiceGroup
    internet_service_ipbl_reason: InternetServiceIpblReason
    internet_service_ipbl_vendor: InternetServiceIpblVendor
    internet_service_list: InternetServiceList
    internet_service_name: InternetServiceName
    internet_service_owner: InternetServiceOwner
    internet_service_reputation: InternetServiceReputation
    internet_service_sld: InternetServiceSld
    internet_service_subapp: InternetServiceSubapp
    ip_translation: IpTranslation
    ippool: Ippool
    ippool6: Ippool6
    ldb_monitor: LdbMonitor
    local_in_policy: LocalInPolicy
    local_in_policy6: LocalInPolicy6
    multicast_address: MulticastAddress
    multicast_address6: MulticastAddress6
    multicast_policy: MulticastPolicy
    multicast_policy6: MulticastPolicy6
    network_service_dynamic: NetworkServiceDynamic
    on_demand_sniffer: OnDemandSniffer
    policy: Policy
    profile_group: ProfileGroup
    profile_protocol_options: ProfileProtocolOptions
    proxy_address: ProxyAddress
    proxy_addrgrp: ProxyAddrgrp
    proxy_policy: ProxyPolicy
    region: Region
    security_policy: SecurityPolicy
    shaping_policy: ShapingPolicy
    shaping_profile: ShapingProfile
    sniffer: Sniffer
    ssl_server: SslServer
    ssl_ssh_profile: SslSshProfile
    traffic_class: TrafficClass
    ttl_policy: TtlPolicy
    vendor_mac: VendorMac
    vendor_mac_summary: VendorMacSummary
    vip: Vip
    vip6: Vip6
    vipgrp: Vipgrp
    vipgrp6: Vipgrp6

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firewall category with HTTP client."""
        ...
