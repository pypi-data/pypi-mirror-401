"""Type stubs for SWITCH_CONTROLLER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom_command import CustomCommand, CustomCommandDictMode, CustomCommandObjectMode
    from .dynamic_port_policy import DynamicPortPolicy, DynamicPortPolicyDictMode, DynamicPortPolicyObjectMode
    from .flow_tracking import FlowTracking, FlowTrackingDictMode, FlowTrackingObjectMode
    from .fortilink_settings import FortilinkSettings, FortilinkSettingsDictMode, FortilinkSettingsObjectMode
    from .global_ import Global, GlobalDictMode, GlobalObjectMode
    from .igmp_snooping import IgmpSnooping, IgmpSnoopingDictMode, IgmpSnoopingObjectMode
    from .ip_source_guard_log import IpSourceGuardLog, IpSourceGuardLogDictMode, IpSourceGuardLogObjectMode
    from .lldp_profile import LldpProfile, LldpProfileDictMode, LldpProfileObjectMode
    from .lldp_settings import LldpSettings, LldpSettingsDictMode, LldpSettingsObjectMode
    from .location import Location, LocationDictMode, LocationObjectMode
    from .mac_policy import MacPolicy, MacPolicyDictMode, MacPolicyObjectMode
    from .managed_switch import ManagedSwitch, ManagedSwitchDictMode, ManagedSwitchObjectMode
    from .network_monitor_settings import NetworkMonitorSettings, NetworkMonitorSettingsDictMode, NetworkMonitorSettingsObjectMode
    from .remote_log import RemoteLog, RemoteLogDictMode, RemoteLogObjectMode
    from .sflow import Sflow, SflowDictMode, SflowObjectMode
    from .snmp_community import SnmpCommunity, SnmpCommunityDictMode, SnmpCommunityObjectMode
    from .snmp_sysinfo import SnmpSysinfo, SnmpSysinfoDictMode, SnmpSysinfoObjectMode
    from .snmp_trap_threshold import SnmpTrapThreshold, SnmpTrapThresholdDictMode, SnmpTrapThresholdObjectMode
    from .snmp_user import SnmpUser, SnmpUserDictMode, SnmpUserObjectMode
    from .storm_control import StormControl, StormControlDictMode, StormControlObjectMode
    from .storm_control_policy import StormControlPolicy, StormControlPolicyDictMode, StormControlPolicyObjectMode
    from .stp_instance import StpInstance, StpInstanceDictMode, StpInstanceObjectMode
    from .stp_settings import StpSettings, StpSettingsDictMode, StpSettingsObjectMode
    from .switch_group import SwitchGroup, SwitchGroupDictMode, SwitchGroupObjectMode
    from .switch_interface_tag import SwitchInterfaceTag, SwitchInterfaceTagDictMode, SwitchInterfaceTagObjectMode
    from .switch_log import SwitchLog, SwitchLogDictMode, SwitchLogObjectMode
    from .switch_profile import SwitchProfile, SwitchProfileDictMode, SwitchProfileObjectMode
    from .system import System, SystemDictMode, SystemObjectMode
    from .traffic_policy import TrafficPolicy, TrafficPolicyDictMode, TrafficPolicyObjectMode
    from .traffic_sniffer import TrafficSniffer, TrafficSnifferDictMode, TrafficSnifferObjectMode
    from .virtual_port_pool import VirtualPortPool, VirtualPortPoolDictMode, VirtualPortPoolObjectMode
    from .vlan_policy import VlanPolicy, VlanPolicyDictMode, VlanPolicyObjectMode
    from .x802_1x_settings import X8021xSettings, X8021xSettingsDictMode, X8021xSettingsObjectMode
    from .acl import AclDictMode, AclObjectMode
    from .auto_config import AutoConfig
    from .initial_config import InitialConfig
    from .ptp import PtpDictMode, PtpObjectMode
    from .qos import QosDictMode, QosObjectMode
    from .security_policy import SecurityPolicy

__all__ = [
    "CustomCommand",
    "DynamicPortPolicy",
    "FlowTracking",
    "FortilinkSettings",
    "Global",
    "IgmpSnooping",
    "IpSourceGuardLog",
    "LldpProfile",
    "LldpSettings",
    "Location",
    "MacPolicy",
    "ManagedSwitch",
    "NetworkMonitorSettings",
    "RemoteLog",
    "Sflow",
    "SnmpCommunity",
    "SnmpSysinfo",
    "SnmpTrapThreshold",
    "SnmpUser",
    "StormControl",
    "StormControlPolicy",
    "StpInstance",
    "StpSettings",
    "SwitchGroup",
    "SwitchInterfaceTag",
    "SwitchLog",
    "SwitchProfile",
    "System",
    "TrafficPolicy",
    "TrafficSniffer",
    "VirtualPortPool",
    "VlanPolicy",
    "X8021xSettings",
    "SwitchControllerDictMode",
    "SwitchControllerObjectMode",
]

class SwitchControllerDictMode:
    """SWITCH_CONTROLLER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    acl: AclDictMode
    auto_config: AutoConfig
    initial_config: InitialConfig
    ptp: PtpDictMode
    qos: QosDictMode
    security_policy: SecurityPolicy
    custom_command: CustomCommandDictMode
    dynamic_port_policy: DynamicPortPolicyDictMode
    flow_tracking: FlowTrackingDictMode
    fortilink_settings: FortilinkSettingsDictMode
    global_: GlobalDictMode
    igmp_snooping: IgmpSnoopingDictMode
    ip_source_guard_log: IpSourceGuardLogDictMode
    lldp_profile: LldpProfileDictMode
    lldp_settings: LldpSettingsDictMode
    location: LocationDictMode
    mac_policy: MacPolicyDictMode
    managed_switch: ManagedSwitchDictMode
    network_monitor_settings: NetworkMonitorSettingsDictMode
    remote_log: RemoteLogDictMode
    sflow: SflowDictMode
    snmp_community: SnmpCommunityDictMode
    snmp_sysinfo: SnmpSysinfoDictMode
    snmp_trap_threshold: SnmpTrapThresholdDictMode
    snmp_user: SnmpUserDictMode
    storm_control: StormControlDictMode
    storm_control_policy: StormControlPolicyDictMode
    stp_instance: StpInstanceDictMode
    stp_settings: StpSettingsDictMode
    switch_group: SwitchGroupDictMode
    switch_interface_tag: SwitchInterfaceTagDictMode
    switch_log: SwitchLogDictMode
    switch_profile: SwitchProfileDictMode
    system: SystemDictMode
    traffic_policy: TrafficPolicyDictMode
    traffic_sniffer: TrafficSnifferDictMode
    virtual_port_pool: VirtualPortPoolDictMode
    vlan_policy: VlanPolicyDictMode
    x802_1x_settings: X8021xSettingsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize switch_controller category with HTTP client."""
        ...


class SwitchControllerObjectMode:
    """SWITCH_CONTROLLER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    acl: AclObjectMode
    auto_config: AutoConfig
    initial_config: InitialConfig
    ptp: PtpObjectMode
    qos: QosObjectMode
    security_policy: SecurityPolicy
    custom_command: CustomCommandObjectMode
    dynamic_port_policy: DynamicPortPolicyObjectMode
    flow_tracking: FlowTrackingObjectMode
    fortilink_settings: FortilinkSettingsObjectMode
    global_: GlobalObjectMode
    igmp_snooping: IgmpSnoopingObjectMode
    ip_source_guard_log: IpSourceGuardLogObjectMode
    lldp_profile: LldpProfileObjectMode
    lldp_settings: LldpSettingsObjectMode
    location: LocationObjectMode
    mac_policy: MacPolicyObjectMode
    managed_switch: ManagedSwitchObjectMode
    network_monitor_settings: NetworkMonitorSettingsObjectMode
    remote_log: RemoteLogObjectMode
    sflow: SflowObjectMode
    snmp_community: SnmpCommunityObjectMode
    snmp_sysinfo: SnmpSysinfoObjectMode
    snmp_trap_threshold: SnmpTrapThresholdObjectMode
    snmp_user: SnmpUserObjectMode
    storm_control: StormControlObjectMode
    storm_control_policy: StormControlPolicyObjectMode
    stp_instance: StpInstanceObjectMode
    stp_settings: StpSettingsObjectMode
    switch_group: SwitchGroupObjectMode
    switch_interface_tag: SwitchInterfaceTagObjectMode
    switch_log: SwitchLogObjectMode
    switch_profile: SwitchProfileObjectMode
    system: SystemObjectMode
    traffic_policy: TrafficPolicyObjectMode
    traffic_sniffer: TrafficSnifferObjectMode
    virtual_port_pool: VirtualPortPoolObjectMode
    vlan_policy: VlanPolicyObjectMode
    x802_1x_settings: X8021xSettingsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize switch_controller category with HTTP client."""
        ...


# Base class for backwards compatibility
class SwitchController:
    """SWITCH_CONTROLLER API category."""
    
    acl: Acl
    auto_config: AutoConfig
    initial_config: InitialConfig
    ptp: Ptp
    qos: Qos
    security_policy: SecurityPolicy
    custom_command: CustomCommand
    dynamic_port_policy: DynamicPortPolicy
    flow_tracking: FlowTracking
    fortilink_settings: FortilinkSettings
    global_: Global
    igmp_snooping: IgmpSnooping
    ip_source_guard_log: IpSourceGuardLog
    lldp_profile: LldpProfile
    lldp_settings: LldpSettings
    location: Location
    mac_policy: MacPolicy
    managed_switch: ManagedSwitch
    network_monitor_settings: NetworkMonitorSettings
    remote_log: RemoteLog
    sflow: Sflow
    snmp_community: SnmpCommunity
    snmp_sysinfo: SnmpSysinfo
    snmp_trap_threshold: SnmpTrapThreshold
    snmp_user: SnmpUser
    storm_control: StormControl
    storm_control_policy: StormControlPolicy
    stp_instance: StpInstance
    stp_settings: StpSettings
    switch_group: SwitchGroup
    switch_interface_tag: SwitchInterfaceTag
    switch_log: SwitchLog
    switch_profile: SwitchProfile
    system: System
    traffic_policy: TrafficPolicy
    traffic_sniffer: TrafficSniffer
    virtual_port_pool: VirtualPortPool
    vlan_policy: VlanPolicy
    x802_1x_settings: X8021xSettings

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize switch_controller category with HTTP client."""
        ...
