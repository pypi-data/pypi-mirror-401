"""Type stubs for WIRELESS_CONTROLLER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .access_control_list import AccessControlList, AccessControlListDictMode, AccessControlListObjectMode
    from .ap_status import ApStatus, ApStatusDictMode, ApStatusObjectMode
    from .apcfg_profile import ApcfgProfile, ApcfgProfileDictMode, ApcfgProfileObjectMode
    from .arrp_profile import ArrpProfile, ArrpProfileDictMode, ArrpProfileObjectMode
    from .ble_profile import BleProfile, BleProfileDictMode, BleProfileObjectMode
    from .bonjour_profile import BonjourProfile, BonjourProfileDictMode, BonjourProfileObjectMode
    from .global_ import Global, GlobalDictMode, GlobalObjectMode
    from .inter_controller import InterController, InterControllerDictMode, InterControllerObjectMode
    from .log import Log, LogDictMode, LogObjectMode
    from .lw_profile import LwProfile, LwProfileDictMode, LwProfileObjectMode
    from .mpsk_profile import MpskProfile, MpskProfileDictMode, MpskProfileObjectMode
    from .nac_profile import NacProfile, NacProfileDictMode, NacProfileObjectMode
    from .qos_profile import QosProfile, QosProfileDictMode, QosProfileObjectMode
    from .region import Region, RegionDictMode, RegionObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode
    from .snmp import Snmp, SnmpDictMode, SnmpObjectMode
    from .ssid_policy import SsidPolicy, SsidPolicyDictMode, SsidPolicyObjectMode
    from .syslog_profile import SyslogProfile, SyslogProfileDictMode, SyslogProfileObjectMode
    from .timers import Timers, TimersDictMode, TimersObjectMode
    from .utm_profile import UtmProfile, UtmProfileDictMode, UtmProfileObjectMode
    from .vap import Vap, VapDictMode, VapObjectMode
    from .vap_group import VapGroup, VapGroupDictMode, VapGroupObjectMode
    from .wag_profile import WagProfile, WagProfileDictMode, WagProfileObjectMode
    from .wids_profile import WidsProfile, WidsProfileDictMode, WidsProfileObjectMode
    from .wtp import Wtp, WtpDictMode, WtpObjectMode
    from .wtp_group import WtpGroup, WtpGroupDictMode, WtpGroupObjectMode
    from .wtp_profile import WtpProfile, WtpProfileDictMode, WtpProfileObjectMode
    from .hotspot20 import Hotspot20DictMode, Hotspot20ObjectMode

__all__ = [
    "AccessControlList",
    "ApStatus",
    "ApcfgProfile",
    "ArrpProfile",
    "BleProfile",
    "BonjourProfile",
    "Global",
    "InterController",
    "Log",
    "LwProfile",
    "MpskProfile",
    "NacProfile",
    "QosProfile",
    "Region",
    "Setting",
    "Snmp",
    "SsidPolicy",
    "SyslogProfile",
    "Timers",
    "UtmProfile",
    "Vap",
    "VapGroup",
    "WagProfile",
    "WidsProfile",
    "Wtp",
    "WtpGroup",
    "WtpProfile",
    "WirelessControllerDictMode",
    "WirelessControllerObjectMode",
]

class WirelessControllerDictMode:
    """WIRELESS_CONTROLLER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    hotspot20: Hotspot20DictMode
    access_control_list: AccessControlListDictMode
    ap_status: ApStatusDictMode
    apcfg_profile: ApcfgProfileDictMode
    arrp_profile: ArrpProfileDictMode
    ble_profile: BleProfileDictMode
    bonjour_profile: BonjourProfileDictMode
    global_: GlobalDictMode
    inter_controller: InterControllerDictMode
    log: LogDictMode
    lw_profile: LwProfileDictMode
    mpsk_profile: MpskProfileDictMode
    nac_profile: NacProfileDictMode
    qos_profile: QosProfileDictMode
    region: RegionDictMode
    setting: SettingDictMode
    snmp: SnmpDictMode
    ssid_policy: SsidPolicyDictMode
    syslog_profile: SyslogProfileDictMode
    timers: TimersDictMode
    utm_profile: UtmProfileDictMode
    vap: VapDictMode
    vap_group: VapGroupDictMode
    wag_profile: WagProfileDictMode
    wids_profile: WidsProfileDictMode
    wtp: WtpDictMode
    wtp_group: WtpGroupDictMode
    wtp_profile: WtpProfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wireless_controller category with HTTP client."""
        ...


class WirelessControllerObjectMode:
    """WIRELESS_CONTROLLER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    hotspot20: Hotspot20ObjectMode
    access_control_list: AccessControlListObjectMode
    ap_status: ApStatusObjectMode
    apcfg_profile: ApcfgProfileObjectMode
    arrp_profile: ArrpProfileObjectMode
    ble_profile: BleProfileObjectMode
    bonjour_profile: BonjourProfileObjectMode
    global_: GlobalObjectMode
    inter_controller: InterControllerObjectMode
    log: LogObjectMode
    lw_profile: LwProfileObjectMode
    mpsk_profile: MpskProfileObjectMode
    nac_profile: NacProfileObjectMode
    qos_profile: QosProfileObjectMode
    region: RegionObjectMode
    setting: SettingObjectMode
    snmp: SnmpObjectMode
    ssid_policy: SsidPolicyObjectMode
    syslog_profile: SyslogProfileObjectMode
    timers: TimersObjectMode
    utm_profile: UtmProfileObjectMode
    vap: VapObjectMode
    vap_group: VapGroupObjectMode
    wag_profile: WagProfileObjectMode
    wids_profile: WidsProfileObjectMode
    wtp: WtpObjectMode
    wtp_group: WtpGroupObjectMode
    wtp_profile: WtpProfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wireless_controller category with HTTP client."""
        ...


# Base class for backwards compatibility
class WirelessController:
    """WIRELESS_CONTROLLER API category."""
    
    hotspot20: Hotspot20
    access_control_list: AccessControlList
    ap_status: ApStatus
    apcfg_profile: ApcfgProfile
    arrp_profile: ArrpProfile
    ble_profile: BleProfile
    bonjour_profile: BonjourProfile
    global_: Global
    inter_controller: InterController
    log: Log
    lw_profile: LwProfile
    mpsk_profile: MpskProfile
    nac_profile: NacProfile
    qos_profile: QosProfile
    region: Region
    setting: Setting
    snmp: Snmp
    ssid_policy: SsidPolicy
    syslog_profile: SyslogProfile
    timers: Timers
    utm_profile: UtmProfile
    vap: Vap
    vap_group: VapGroup
    wag_profile: WagProfile
    wids_profile: WidsProfile
    wtp: Wtp
    wtp_group: WtpGroup
    wtp_profile: WtpProfile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wireless_controller category with HTTP client."""
        ...
