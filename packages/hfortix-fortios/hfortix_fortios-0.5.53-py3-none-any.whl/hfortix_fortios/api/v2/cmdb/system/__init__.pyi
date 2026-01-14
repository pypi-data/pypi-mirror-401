"""Type stubs for SYSTEM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .accprofile import Accprofile, AccprofileDictMode, AccprofileObjectMode
    from .acme import Acme, AcmeDictMode, AcmeObjectMode
    from .admin import Admin, AdminDictMode, AdminObjectMode
    from .affinity_interrupt import AffinityInterrupt, AffinityInterruptDictMode, AffinityInterruptObjectMode
    from .affinity_packet_redistribution import AffinityPacketRedistribution, AffinityPacketRedistributionDictMode, AffinityPacketRedistributionObjectMode
    from .alarm import Alarm, AlarmDictMode, AlarmObjectMode
    from .alias import Alias, AliasDictMode, AliasObjectMode
    from .api_user import ApiUser, ApiUserDictMode, ApiUserObjectMode
    from .arp_table import ArpTable, ArpTableDictMode, ArpTableObjectMode
    from .auto_install import AutoInstall, AutoInstallDictMode, AutoInstallObjectMode
    from .auto_script import AutoScript, AutoScriptDictMode, AutoScriptObjectMode
    from .automation_action import AutomationAction, AutomationActionDictMode, AutomationActionObjectMode
    from .automation_condition import AutomationCondition, AutomationConditionDictMode, AutomationConditionObjectMode
    from .automation_destination import AutomationDestination, AutomationDestinationDictMode, AutomationDestinationObjectMode
    from .automation_stitch import AutomationStitch, AutomationStitchDictMode, AutomationStitchObjectMode
    from .automation_trigger import AutomationTrigger, AutomationTriggerDictMode, AutomationTriggerObjectMode
    from .central_management import CentralManagement, CentralManagementDictMode, CentralManagementObjectMode
    from .cloud_service import CloudService, CloudServiceDictMode, CloudServiceObjectMode
    from .console import Console, ConsoleDictMode, ConsoleObjectMode
    from .csf import Csf, CsfDictMode, CsfObjectMode
    from .custom_language import CustomLanguage, CustomLanguageDictMode, CustomLanguageObjectMode
    from .ddns import Ddns, DdnsDictMode, DdnsObjectMode
    from .dedicated_mgmt import DedicatedMgmt, DedicatedMgmtDictMode, DedicatedMgmtObjectMode
    from .device_upgrade import DeviceUpgrade, DeviceUpgradeDictMode, DeviceUpgradeObjectMode
    from .device_upgrade_exemptions import DeviceUpgradeExemptions, DeviceUpgradeExemptionsDictMode, DeviceUpgradeExemptionsObjectMode
    from .dns import Dns, DnsDictMode, DnsObjectMode
    from .dns64 import Dns64, Dns64DictMode, Dns64ObjectMode
    from .dns_database import DnsDatabase, DnsDatabaseDictMode, DnsDatabaseObjectMode
    from .dns_server import DnsServer, DnsServerDictMode, DnsServerObjectMode
    from .dscp_based_priority import DscpBasedPriority, DscpBasedPriorityDictMode, DscpBasedPriorityObjectMode
    from .email_server import EmailServer, EmailServerDictMode, EmailServerObjectMode
    from .evpn import Evpn, EvpnDictMode, EvpnObjectMode
    from .external_resource import ExternalResource, ExternalResourceDictMode, ExternalResourceObjectMode
    from .fabric_vpn import FabricVpn, FabricVpnDictMode, FabricVpnObjectMode
    from .federated_upgrade import FederatedUpgrade, FederatedUpgradeDictMode, FederatedUpgradeObjectMode
    from .fips_cc import FipsCc, FipsCcDictMode, FipsCcObjectMode
    from .fortiguard import Fortiguard, FortiguardDictMode, FortiguardObjectMode
    from .fortisandbox import Fortisandbox, FortisandboxDictMode, FortisandboxObjectMode
    from .fsso_polling import FssoPolling, FssoPollingDictMode, FssoPollingObjectMode
    from .ftm_push import FtmPush, FtmPushDictMode, FtmPushObjectMode
    from .geneve import Geneve, GeneveDictMode, GeneveObjectMode
    from .geoip_country import GeoipCountry, GeoipCountryDictMode, GeoipCountryObjectMode
    from .geoip_override import GeoipOverride, GeoipOverrideDictMode, GeoipOverrideObjectMode
    from .global_ import Global, GlobalDictMode, GlobalObjectMode
    from .gre_tunnel import GreTunnel, GreTunnelDictMode, GreTunnelObjectMode
    from .ha import Ha, HaDictMode, HaObjectMode
    from .ha_monitor import HaMonitor, HaMonitorDictMode, HaMonitorObjectMode
    from .health_check_fortiguard import HealthCheckFortiguard, HealthCheckFortiguardDictMode, HealthCheckFortiguardObjectMode
    from .ike import Ike, IkeDictMode, IkeObjectMode
    from .interface import Interface, InterfaceDictMode, InterfaceObjectMode
    from .ipam import Ipam, IpamDictMode, IpamObjectMode
    from .ipip_tunnel import IpipTunnel, IpipTunnelDictMode, IpipTunnelObjectMode
    from .ips import Ips, IpsDictMode, IpsObjectMode
    from .ips_urlfilter_dns import IpsUrlfilterDns, IpsUrlfilterDnsDictMode, IpsUrlfilterDnsObjectMode
    from .ips_urlfilter_dns6 import IpsUrlfilterDns6, IpsUrlfilterDns6DictMode, IpsUrlfilterDns6ObjectMode
    from .ipsec_aggregate import IpsecAggregate, IpsecAggregateDictMode, IpsecAggregateObjectMode
    from .ipv6_neighbor_cache import Ipv6NeighborCache, Ipv6NeighborCacheDictMode, Ipv6NeighborCacheObjectMode
    from .ipv6_tunnel import Ipv6Tunnel, Ipv6TunnelDictMode, Ipv6TunnelObjectMode
    from .link_monitor import LinkMonitor, LinkMonitorDictMode, LinkMonitorObjectMode
    from .lte_modem import LteModem, LteModemDictMode, LteModemObjectMode
    from .mac_address_table import MacAddressTable, MacAddressTableDictMode, MacAddressTableObjectMode
    from .mobile_tunnel import MobileTunnel, MobileTunnelDictMode, MobileTunnelObjectMode
    from .modem import Modem, ModemDictMode, ModemObjectMode
    from .nd_proxy import NdProxy, NdProxyDictMode, NdProxyObjectMode
    from .netflow import Netflow, NetflowDictMode, NetflowObjectMode
    from .network_visibility import NetworkVisibility, NetworkVisibilityDictMode, NetworkVisibilityObjectMode
    from .ngfw_settings import NgfwSettings, NgfwSettingsDictMode, NgfwSettingsObjectMode
    from .np6xlite import Np6xlite, Np6xliteDictMode, Np6xliteObjectMode
    from .npu import Npu, NpuDictMode, NpuObjectMode
    from .ntp import Ntp, NtpDictMode, NtpObjectMode
    from .object_tagging import ObjectTagging, ObjectTaggingDictMode, ObjectTaggingObjectMode
    from .password_policy import PasswordPolicy, PasswordPolicyDictMode, PasswordPolicyObjectMode
    from .password_policy_guest_admin import PasswordPolicyGuestAdmin, PasswordPolicyGuestAdminDictMode, PasswordPolicyGuestAdminObjectMode
    from .pcp_server import PcpServer, PcpServerDictMode, PcpServerObjectMode
    from .physical_switch import PhysicalSwitch, PhysicalSwitchDictMode, PhysicalSwitchObjectMode
    from .pppoe_interface import PppoeInterface, PppoeInterfaceDictMode, PppoeInterfaceObjectMode
    from .probe_response import ProbeResponse, ProbeResponseDictMode, ProbeResponseObjectMode
    from .proxy_arp import ProxyArp, ProxyArpDictMode, ProxyArpObjectMode
    from .ptp import Ptp, PtpDictMode, PtpObjectMode
    from .replacemsg_group import ReplacemsgGroup, ReplacemsgGroupDictMode, ReplacemsgGroupObjectMode
    from .replacemsg_image import ReplacemsgImage, ReplacemsgImageDictMode, ReplacemsgImageObjectMode
    from .resource_limits import ResourceLimits, ResourceLimitsDictMode, ResourceLimitsObjectMode
    from .saml import Saml, SamlDictMode, SamlObjectMode
    from .sdn_connector import SdnConnector, SdnConnectorDictMode, SdnConnectorObjectMode
    from .sdn_proxy import SdnProxy, SdnProxyDictMode, SdnProxyObjectMode
    from .sdn_vpn import SdnVpn, SdnVpnDictMode, SdnVpnObjectMode
    from .sdwan import Sdwan, SdwanDictMode, SdwanObjectMode
    from .session_helper import SessionHelper, SessionHelperDictMode, SessionHelperObjectMode
    from .session_ttl import SessionTtl, SessionTtlDictMode, SessionTtlObjectMode
    from .settings import Settings, SettingsDictMode, SettingsObjectMode
    from .sflow import Sflow, SflowDictMode, SflowObjectMode
    from .sit_tunnel import SitTunnel, SitTunnelDictMode, SitTunnelObjectMode
    from .sms_server import SmsServer, SmsServerDictMode, SmsServerObjectMode
    from .sov_sase import SovSase, SovSaseDictMode, SovSaseObjectMode
    from .speed_test_schedule import SpeedTestSchedule, SpeedTestScheduleDictMode, SpeedTestScheduleObjectMode
    from .speed_test_server import SpeedTestServer, SpeedTestServerDictMode, SpeedTestServerObjectMode
    from .speed_test_setting import SpeedTestSetting, SpeedTestSettingDictMode, SpeedTestSettingObjectMode
    from .ssh_config import SshConfig, SshConfigDictMode, SshConfigObjectMode
    from .sso_admin import SsoAdmin, SsoAdminDictMode, SsoAdminObjectMode
    from .sso_forticloud_admin import SsoForticloudAdmin, SsoForticloudAdminDictMode, SsoForticloudAdminObjectMode
    from .sso_fortigate_cloud_admin import SsoFortigateCloudAdmin, SsoFortigateCloudAdminDictMode, SsoFortigateCloudAdminObjectMode
    from .standalone_cluster import StandaloneCluster, StandaloneClusterDictMode, StandaloneClusterObjectMode
    from .storage import Storage, StorageDictMode, StorageObjectMode
    from .stp import Stp, StpDictMode, StpObjectMode
    from .switch_interface import SwitchInterface, SwitchInterfaceDictMode, SwitchInterfaceObjectMode
    from .timezone import Timezone, TimezoneDictMode, TimezoneObjectMode
    from .tos_based_priority import TosBasedPriority, TosBasedPriorityDictMode, TosBasedPriorityObjectMode
    from .vdom import Vdom, VdomDictMode, VdomObjectMode
    from .vdom_dns import VdomDns, VdomDnsDictMode, VdomDnsObjectMode
    from .vdom_exception import VdomException, VdomExceptionDictMode, VdomExceptionObjectMode
    from .vdom_link import VdomLink, VdomLinkDictMode, VdomLinkObjectMode
    from .vdom_netflow import VdomNetflow, VdomNetflowDictMode, VdomNetflowObjectMode
    from .vdom_property import VdomProperty, VdomPropertyDictMode, VdomPropertyObjectMode
    from .vdom_radius_server import VdomRadiusServer, VdomRadiusServerDictMode, VdomRadiusServerObjectMode
    from .vdom_sflow import VdomSflow, VdomSflowDictMode, VdomSflowObjectMode
    from .virtual_switch import VirtualSwitch, VirtualSwitchDictMode, VirtualSwitchObjectMode
    from .virtual_wire_pair import VirtualWirePair, VirtualWirePairDictMode, VirtualWirePairObjectMode
    from .vne_interface import VneInterface, VneInterfaceDictMode, VneInterfaceObjectMode
    from .vxlan import Vxlan, VxlanDictMode, VxlanObjectMode
    from .wccp import Wccp, WccpDictMode, WccpObjectMode
    from .zone import Zone, ZoneDictMode, ZoneObjectMode
    from .autoupdate import AutoupdateDictMode, AutoupdateObjectMode
    from .dhcp import DhcpDictMode, DhcpObjectMode
    from .dhcp6 import Dhcp6DictMode, Dhcp6ObjectMode
    from .lldp import LldpDictMode, LldpObjectMode
    from .modem3g import Modem3gDictMode, Modem3gObjectMode
    from .replacemsg import ReplacemsgDictMode, ReplacemsgObjectMode
    from .security_rating import SecurityRating
    from .snmp import SnmpDictMode, SnmpObjectMode

__all__ = [
    "Accprofile",
    "Acme",
    "Admin",
    "AffinityInterrupt",
    "AffinityPacketRedistribution",
    "Alarm",
    "Alias",
    "ApiUser",
    "ArpTable",
    "AutoInstall",
    "AutoScript",
    "AutomationAction",
    "AutomationCondition",
    "AutomationDestination",
    "AutomationStitch",
    "AutomationTrigger",
    "CentralManagement",
    "CloudService",
    "Console",
    "Csf",
    "CustomLanguage",
    "Ddns",
    "DedicatedMgmt",
    "DeviceUpgrade",
    "DeviceUpgradeExemptions",
    "Dns",
    "Dns64",
    "DnsDatabase",
    "DnsServer",
    "DscpBasedPriority",
    "EmailServer",
    "Evpn",
    "ExternalResource",
    "FabricVpn",
    "FederatedUpgrade",
    "FipsCc",
    "Fortiguard",
    "Fortisandbox",
    "FssoPolling",
    "FtmPush",
    "Geneve",
    "GeoipCountry",
    "GeoipOverride",
    "Global",
    "GreTunnel",
    "Ha",
    "HaMonitor",
    "HealthCheckFortiguard",
    "Ike",
    "Interface",
    "Ipam",
    "IpipTunnel",
    "Ips",
    "IpsUrlfilterDns",
    "IpsUrlfilterDns6",
    "IpsecAggregate",
    "Ipv6NeighborCache",
    "Ipv6Tunnel",
    "LinkMonitor",
    "LteModem",
    "MacAddressTable",
    "MobileTunnel",
    "Modem",
    "NdProxy",
    "Netflow",
    "NetworkVisibility",
    "NgfwSettings",
    "Np6xlite",
    "Npu",
    "Ntp",
    "ObjectTagging",
    "PasswordPolicy",
    "PasswordPolicyGuestAdmin",
    "PcpServer",
    "PhysicalSwitch",
    "PppoeInterface",
    "ProbeResponse",
    "ProxyArp",
    "Ptp",
    "ReplacemsgGroup",
    "ReplacemsgImage",
    "ResourceLimits",
    "Saml",
    "SdnConnector",
    "SdnProxy",
    "SdnVpn",
    "Sdwan",
    "SessionHelper",
    "SessionTtl",
    "Settings",
    "Sflow",
    "SitTunnel",
    "SmsServer",
    "SovSase",
    "SpeedTestSchedule",
    "SpeedTestServer",
    "SpeedTestSetting",
    "SshConfig",
    "SsoAdmin",
    "SsoForticloudAdmin",
    "SsoFortigateCloudAdmin",
    "StandaloneCluster",
    "Storage",
    "Stp",
    "SwitchInterface",
    "Timezone",
    "TosBasedPriority",
    "Vdom",
    "VdomDns",
    "VdomException",
    "VdomLink",
    "VdomNetflow",
    "VdomProperty",
    "VdomRadiusServer",
    "VdomSflow",
    "VirtualSwitch",
    "VirtualWirePair",
    "VneInterface",
    "Vxlan",
    "Wccp",
    "Zone",
    "SystemDictMode",
    "SystemObjectMode",
]

class SystemDictMode:
    """SYSTEM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    autoupdate: AutoupdateDictMode
    dhcp: DhcpDictMode
    dhcp6: Dhcp6DictMode
    lldp: LldpDictMode
    modem3g: Modem3gDictMode
    replacemsg: ReplacemsgDictMode
    security_rating: SecurityRating
    snmp: SnmpDictMode
    accprofile: AccprofileDictMode
    acme: AcmeDictMode
    admin: AdminDictMode
    affinity_interrupt: AffinityInterruptDictMode
    affinity_packet_redistribution: AffinityPacketRedistributionDictMode
    alarm: AlarmDictMode
    alias: AliasDictMode
    api_user: ApiUserDictMode
    arp_table: ArpTableDictMode
    auto_install: AutoInstallDictMode
    auto_script: AutoScriptDictMode
    automation_action: AutomationActionDictMode
    automation_condition: AutomationConditionDictMode
    automation_destination: AutomationDestinationDictMode
    automation_stitch: AutomationStitchDictMode
    automation_trigger: AutomationTriggerDictMode
    central_management: CentralManagementDictMode
    cloud_service: CloudServiceDictMode
    console: ConsoleDictMode
    csf: CsfDictMode
    custom_language: CustomLanguageDictMode
    ddns: DdnsDictMode
    dedicated_mgmt: DedicatedMgmtDictMode
    device_upgrade: DeviceUpgradeDictMode
    device_upgrade_exemptions: DeviceUpgradeExemptionsDictMode
    dns: DnsDictMode
    dns64: Dns64DictMode
    dns_database: DnsDatabaseDictMode
    dns_server: DnsServerDictMode
    dscp_based_priority: DscpBasedPriorityDictMode
    email_server: EmailServerDictMode
    evpn: EvpnDictMode
    external_resource: ExternalResourceDictMode
    fabric_vpn: FabricVpnDictMode
    federated_upgrade: FederatedUpgradeDictMode
    fips_cc: FipsCcDictMode
    fortiguard: FortiguardDictMode
    fortisandbox: FortisandboxDictMode
    fsso_polling: FssoPollingDictMode
    ftm_push: FtmPushDictMode
    geneve: GeneveDictMode
    geoip_country: GeoipCountryDictMode
    geoip_override: GeoipOverrideDictMode
    global_: GlobalDictMode
    gre_tunnel: GreTunnelDictMode
    ha: HaDictMode
    ha_monitor: HaMonitorDictMode
    health_check_fortiguard: HealthCheckFortiguardDictMode
    ike: IkeDictMode
    interface: InterfaceDictMode
    ipam: IpamDictMode
    ipip_tunnel: IpipTunnelDictMode
    ips: IpsDictMode
    ips_urlfilter_dns: IpsUrlfilterDnsDictMode
    ips_urlfilter_dns6: IpsUrlfilterDns6DictMode
    ipsec_aggregate: IpsecAggregateDictMode
    ipv6_neighbor_cache: Ipv6NeighborCacheDictMode
    ipv6_tunnel: Ipv6TunnelDictMode
    link_monitor: LinkMonitorDictMode
    lte_modem: LteModemDictMode
    mac_address_table: MacAddressTableDictMode
    mobile_tunnel: MobileTunnelDictMode
    modem: ModemDictMode
    nd_proxy: NdProxyDictMode
    netflow: NetflowDictMode
    network_visibility: NetworkVisibilityDictMode
    ngfw_settings: NgfwSettingsDictMode
    np6xlite: Np6xliteDictMode
    npu: NpuDictMode
    ntp: NtpDictMode
    object_tagging: ObjectTaggingDictMode
    password_policy: PasswordPolicyDictMode
    password_policy_guest_admin: PasswordPolicyGuestAdminDictMode
    pcp_server: PcpServerDictMode
    physical_switch: PhysicalSwitchDictMode
    pppoe_interface: PppoeInterfaceDictMode
    probe_response: ProbeResponseDictMode
    proxy_arp: ProxyArpDictMode
    ptp: PtpDictMode
    replacemsg_group: ReplacemsgGroupDictMode
    replacemsg_image: ReplacemsgImageDictMode
    resource_limits: ResourceLimitsDictMode
    saml: SamlDictMode
    sdn_connector: SdnConnectorDictMode
    sdn_proxy: SdnProxyDictMode
    sdn_vpn: SdnVpnDictMode
    sdwan: SdwanDictMode
    session_helper: SessionHelperDictMode
    session_ttl: SessionTtlDictMode
    settings: SettingsDictMode
    sflow: SflowDictMode
    sit_tunnel: SitTunnelDictMode
    sms_server: SmsServerDictMode
    sov_sase: SovSaseDictMode
    speed_test_schedule: SpeedTestScheduleDictMode
    speed_test_server: SpeedTestServerDictMode
    speed_test_setting: SpeedTestSettingDictMode
    ssh_config: SshConfigDictMode
    sso_admin: SsoAdminDictMode
    sso_forticloud_admin: SsoForticloudAdminDictMode
    sso_fortigate_cloud_admin: SsoFortigateCloudAdminDictMode
    standalone_cluster: StandaloneClusterDictMode
    storage: StorageDictMode
    stp: StpDictMode
    switch_interface: SwitchInterfaceDictMode
    timezone: TimezoneDictMode
    tos_based_priority: TosBasedPriorityDictMode
    vdom: VdomDictMode
    vdom_dns: VdomDnsDictMode
    vdom_exception: VdomExceptionDictMode
    vdom_link: VdomLinkDictMode
    vdom_netflow: VdomNetflowDictMode
    vdom_property: VdomPropertyDictMode
    vdom_radius_server: VdomRadiusServerDictMode
    vdom_sflow: VdomSflowDictMode
    virtual_switch: VirtualSwitchDictMode
    virtual_wire_pair: VirtualWirePairDictMode
    vne_interface: VneInterfaceDictMode
    vxlan: VxlanDictMode
    wccp: WccpDictMode
    zone: ZoneDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...


class SystemObjectMode:
    """SYSTEM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    autoupdate: AutoupdateObjectMode
    dhcp: DhcpObjectMode
    dhcp6: Dhcp6ObjectMode
    lldp: LldpObjectMode
    modem3g: Modem3gObjectMode
    replacemsg: ReplacemsgObjectMode
    security_rating: SecurityRating
    snmp: SnmpObjectMode
    accprofile: AccprofileObjectMode
    acme: AcmeObjectMode
    admin: AdminObjectMode
    affinity_interrupt: AffinityInterruptObjectMode
    affinity_packet_redistribution: AffinityPacketRedistributionObjectMode
    alarm: AlarmObjectMode
    alias: AliasObjectMode
    api_user: ApiUserObjectMode
    arp_table: ArpTableObjectMode
    auto_install: AutoInstallObjectMode
    auto_script: AutoScriptObjectMode
    automation_action: AutomationActionObjectMode
    automation_condition: AutomationConditionObjectMode
    automation_destination: AutomationDestinationObjectMode
    automation_stitch: AutomationStitchObjectMode
    automation_trigger: AutomationTriggerObjectMode
    central_management: CentralManagementObjectMode
    cloud_service: CloudServiceObjectMode
    console: ConsoleObjectMode
    csf: CsfObjectMode
    custom_language: CustomLanguageObjectMode
    ddns: DdnsObjectMode
    dedicated_mgmt: DedicatedMgmtObjectMode
    device_upgrade: DeviceUpgradeObjectMode
    device_upgrade_exemptions: DeviceUpgradeExemptionsObjectMode
    dns: DnsObjectMode
    dns64: Dns64ObjectMode
    dns_database: DnsDatabaseObjectMode
    dns_server: DnsServerObjectMode
    dscp_based_priority: DscpBasedPriorityObjectMode
    email_server: EmailServerObjectMode
    evpn: EvpnObjectMode
    external_resource: ExternalResourceObjectMode
    fabric_vpn: FabricVpnObjectMode
    federated_upgrade: FederatedUpgradeObjectMode
    fips_cc: FipsCcObjectMode
    fortiguard: FortiguardObjectMode
    fortisandbox: FortisandboxObjectMode
    fsso_polling: FssoPollingObjectMode
    ftm_push: FtmPushObjectMode
    geneve: GeneveObjectMode
    geoip_country: GeoipCountryObjectMode
    geoip_override: GeoipOverrideObjectMode
    global_: GlobalObjectMode
    gre_tunnel: GreTunnelObjectMode
    ha: HaObjectMode
    ha_monitor: HaMonitorObjectMode
    health_check_fortiguard: HealthCheckFortiguardObjectMode
    ike: IkeObjectMode
    interface: InterfaceObjectMode
    ipam: IpamObjectMode
    ipip_tunnel: IpipTunnelObjectMode
    ips: IpsObjectMode
    ips_urlfilter_dns: IpsUrlfilterDnsObjectMode
    ips_urlfilter_dns6: IpsUrlfilterDns6ObjectMode
    ipsec_aggregate: IpsecAggregateObjectMode
    ipv6_neighbor_cache: Ipv6NeighborCacheObjectMode
    ipv6_tunnel: Ipv6TunnelObjectMode
    link_monitor: LinkMonitorObjectMode
    lte_modem: LteModemObjectMode
    mac_address_table: MacAddressTableObjectMode
    mobile_tunnel: MobileTunnelObjectMode
    modem: ModemObjectMode
    nd_proxy: NdProxyObjectMode
    netflow: NetflowObjectMode
    network_visibility: NetworkVisibilityObjectMode
    ngfw_settings: NgfwSettingsObjectMode
    np6xlite: Np6xliteObjectMode
    npu: NpuObjectMode
    ntp: NtpObjectMode
    object_tagging: ObjectTaggingObjectMode
    password_policy: PasswordPolicyObjectMode
    password_policy_guest_admin: PasswordPolicyGuestAdminObjectMode
    pcp_server: PcpServerObjectMode
    physical_switch: PhysicalSwitchObjectMode
    pppoe_interface: PppoeInterfaceObjectMode
    probe_response: ProbeResponseObjectMode
    proxy_arp: ProxyArpObjectMode
    ptp: PtpObjectMode
    replacemsg_group: ReplacemsgGroupObjectMode
    replacemsg_image: ReplacemsgImageObjectMode
    resource_limits: ResourceLimitsObjectMode
    saml: SamlObjectMode
    sdn_connector: SdnConnectorObjectMode
    sdn_proxy: SdnProxyObjectMode
    sdn_vpn: SdnVpnObjectMode
    sdwan: SdwanObjectMode
    session_helper: SessionHelperObjectMode
    session_ttl: SessionTtlObjectMode
    settings: SettingsObjectMode
    sflow: SflowObjectMode
    sit_tunnel: SitTunnelObjectMode
    sms_server: SmsServerObjectMode
    sov_sase: SovSaseObjectMode
    speed_test_schedule: SpeedTestScheduleObjectMode
    speed_test_server: SpeedTestServerObjectMode
    speed_test_setting: SpeedTestSettingObjectMode
    ssh_config: SshConfigObjectMode
    sso_admin: SsoAdminObjectMode
    sso_forticloud_admin: SsoForticloudAdminObjectMode
    sso_fortigate_cloud_admin: SsoFortigateCloudAdminObjectMode
    standalone_cluster: StandaloneClusterObjectMode
    storage: StorageObjectMode
    stp: StpObjectMode
    switch_interface: SwitchInterfaceObjectMode
    timezone: TimezoneObjectMode
    tos_based_priority: TosBasedPriorityObjectMode
    vdom: VdomObjectMode
    vdom_dns: VdomDnsObjectMode
    vdom_exception: VdomExceptionObjectMode
    vdom_link: VdomLinkObjectMode
    vdom_netflow: VdomNetflowObjectMode
    vdom_property: VdomPropertyObjectMode
    vdom_radius_server: VdomRadiusServerObjectMode
    vdom_sflow: VdomSflowObjectMode
    virtual_switch: VirtualSwitchObjectMode
    virtual_wire_pair: VirtualWirePairObjectMode
    vne_interface: VneInterfaceObjectMode
    vxlan: VxlanObjectMode
    wccp: WccpObjectMode
    zone: ZoneObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...


# Base class for backwards compatibility
class System:
    """SYSTEM API category."""
    
    autoupdate: Autoupdate
    dhcp: Dhcp
    dhcp6: Dhcp6
    lldp: Lldp
    modem3g: Modem3g
    replacemsg: Replacemsg
    security_rating: SecurityRating
    snmp: Snmp
    accprofile: Accprofile
    acme: Acme
    admin: Admin
    affinity_interrupt: AffinityInterrupt
    affinity_packet_redistribution: AffinityPacketRedistribution
    alarm: Alarm
    alias: Alias
    api_user: ApiUser
    arp_table: ArpTable
    auto_install: AutoInstall
    auto_script: AutoScript
    automation_action: AutomationAction
    automation_condition: AutomationCondition
    automation_destination: AutomationDestination
    automation_stitch: AutomationStitch
    automation_trigger: AutomationTrigger
    central_management: CentralManagement
    cloud_service: CloudService
    console: Console
    csf: Csf
    custom_language: CustomLanguage
    ddns: Ddns
    dedicated_mgmt: DedicatedMgmt
    device_upgrade: DeviceUpgrade
    device_upgrade_exemptions: DeviceUpgradeExemptions
    dns: Dns
    dns64: Dns64
    dns_database: DnsDatabase
    dns_server: DnsServer
    dscp_based_priority: DscpBasedPriority
    email_server: EmailServer
    evpn: Evpn
    external_resource: ExternalResource
    fabric_vpn: FabricVpn
    federated_upgrade: FederatedUpgrade
    fips_cc: FipsCc
    fortiguard: Fortiguard
    fortisandbox: Fortisandbox
    fsso_polling: FssoPolling
    ftm_push: FtmPush
    geneve: Geneve
    geoip_country: GeoipCountry
    geoip_override: GeoipOverride
    global_: Global
    gre_tunnel: GreTunnel
    ha: Ha
    ha_monitor: HaMonitor
    health_check_fortiguard: HealthCheckFortiguard
    ike: Ike
    interface: Interface
    ipam: Ipam
    ipip_tunnel: IpipTunnel
    ips: Ips
    ips_urlfilter_dns: IpsUrlfilterDns
    ips_urlfilter_dns6: IpsUrlfilterDns6
    ipsec_aggregate: IpsecAggregate
    ipv6_neighbor_cache: Ipv6NeighborCache
    ipv6_tunnel: Ipv6Tunnel
    link_monitor: LinkMonitor
    lte_modem: LteModem
    mac_address_table: MacAddressTable
    mobile_tunnel: MobileTunnel
    modem: Modem
    nd_proxy: NdProxy
    netflow: Netflow
    network_visibility: NetworkVisibility
    ngfw_settings: NgfwSettings
    np6xlite: Np6xlite
    npu: Npu
    ntp: Ntp
    object_tagging: ObjectTagging
    password_policy: PasswordPolicy
    password_policy_guest_admin: PasswordPolicyGuestAdmin
    pcp_server: PcpServer
    physical_switch: PhysicalSwitch
    pppoe_interface: PppoeInterface
    probe_response: ProbeResponse
    proxy_arp: ProxyArp
    ptp: Ptp
    replacemsg_group: ReplacemsgGroup
    replacemsg_image: ReplacemsgImage
    resource_limits: ResourceLimits
    saml: Saml
    sdn_connector: SdnConnector
    sdn_proxy: SdnProxy
    sdn_vpn: SdnVpn
    sdwan: Sdwan
    session_helper: SessionHelper
    session_ttl: SessionTtl
    settings: Settings
    sflow: Sflow
    sit_tunnel: SitTunnel
    sms_server: SmsServer
    sov_sase: SovSase
    speed_test_schedule: SpeedTestSchedule
    speed_test_server: SpeedTestServer
    speed_test_setting: SpeedTestSetting
    ssh_config: SshConfig
    sso_admin: SsoAdmin
    sso_forticloud_admin: SsoForticloudAdmin
    sso_fortigate_cloud_admin: SsoFortigateCloudAdmin
    standalone_cluster: StandaloneCluster
    storage: Storage
    stp: Stp
    switch_interface: SwitchInterface
    timezone: Timezone
    tos_based_priority: TosBasedPriority
    vdom: Vdom
    vdom_dns: VdomDns
    vdom_exception: VdomException
    vdom_link: VdomLink
    vdom_netflow: VdomNetflow
    vdom_property: VdomProperty
    vdom_radius_server: VdomRadiusServer
    vdom_sflow: VdomSflow
    virtual_switch: VirtualSwitch
    virtual_wire_pair: VirtualWirePair
    vne_interface: VneInterface
    vxlan: Vxlan
    wccp: Wccp
    zone: Zone

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...
