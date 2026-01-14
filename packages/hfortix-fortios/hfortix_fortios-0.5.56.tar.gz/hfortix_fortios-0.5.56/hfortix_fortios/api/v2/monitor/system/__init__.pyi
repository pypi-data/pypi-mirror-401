"""Type stubs for SYSTEM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .acme_certificate_status import AcmeCertificateStatus, AcmeCertificateStatusDictMode, AcmeCertificateStatusObjectMode
    from .acquired_dns import AcquiredDns, AcquiredDnsDictMode, AcquiredDnsObjectMode
    from .available_certificates import AvailableCertificates, AvailableCertificatesDictMode, AvailableCertificatesObjectMode
    from .check_port_availability import CheckPortAvailability, CheckPortAvailabilityDictMode, CheckPortAvailabilityObjectMode
    from .current_admins import CurrentAdmins, CurrentAdminsDictMode, CurrentAdminsObjectMode
    from .global_resources import GlobalResources, GlobalResourcesDictMode, GlobalResourcesObjectMode
    from .global_search import GlobalSearch, GlobalSearchDictMode, GlobalSearchObjectMode
    from .ha_backup_hb_used import HaBackupHbUsed, HaBackupHbUsedDictMode, HaBackupHbUsedObjectMode
    from .ha_checksums import HaChecksums, HaChecksumsDictMode, HaChecksumsObjectMode
    from .ha_history import HaHistory, HaHistoryDictMode, HaHistoryObjectMode
    from .ha_hw_interface import HaHwInterface, HaHwInterfaceDictMode, HaHwInterfaceObjectMode
    from .ha_nonsync_checksums import HaNonsyncChecksums, HaNonsyncChecksumsDictMode, HaNonsyncChecksumsObjectMode
    from .ha_statistics import HaStatistics, HaStatisticsDictMode, HaStatisticsObjectMode
    from .ha_table_checksums import HaTableChecksums, HaTableChecksumsDictMode, HaTableChecksumsObjectMode
    from .interface_connected_admins_info import InterfaceConnectedAdminsInfo, InterfaceConnectedAdminsInfoDictMode, InterfaceConnectedAdminsInfoObjectMode
    from .ipconf import Ipconf, IpconfDictMode, IpconfObjectMode
    from .link_monitor import LinkMonitor, LinkMonitorDictMode, LinkMonitorObjectMode
    from .modem3g import Modem3g, Modem3gDictMode, Modem3gObjectMode
    from .monitor_sensor import MonitorSensor, MonitorSensorDictMode, MonitorSensorObjectMode
    from .resolve_fqdn import ResolveFqdn, ResolveFqdnDictMode, ResolveFqdnObjectMode
    from .running_processes import RunningProcesses, RunningProcessesDictMode, RunningProcessesObjectMode
    from .sensor_info import SensorInfo, SensorInfoDictMode, SensorInfoObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode
    from .storage import Storage, StorageDictMode, StorageObjectMode
    from .timezone import Timezone, TimezoneDictMode, TimezoneObjectMode
    from .trusted_cert_authorities import TrustedCertAuthorities, TrustedCertAuthoritiesDictMode, TrustedCertAuthoritiesObjectMode
    from .vdom_link import VdomLink, VdomLinkDictMode, VdomLinkObjectMode
    from .vdom_resource import VdomResource, VdomResourceDictMode, VdomResourceObjectMode
    from .vm_information import VmInformation, VmInformationDictMode, VmInformationObjectMode
    from .admin import AdminDictMode, AdminObjectMode
    from .api_user import ApiUser
    from .automation_action import AutomationAction
    from .automation_stitch import AutomationStitch
    from .available_interfaces import AvailableInterfaces
    from .botnet import Botnet
    from .botnet_domains import BotnetDomains
    from .central_management import CentralManagement
    from .certificate import CertificateDictMode, CertificateObjectMode
    from .change_password import ChangePassword
    from .cluster import ClusterDictMode, ClusterObjectMode
    from .com_log import ComLog
    from .config import ConfigDictMode, ConfigObjectMode
    from .config_error_log import ConfigErrorLog
    from .config_revision import ConfigRevision
    from .config_script import ConfigScript
    from .config_sync import ConfigSync
    from .crash_log import CrashLog
    from .csf import Csf
    from .debug import DebugDictMode, DebugObjectMode
    from .dhcp import Dhcp
    from .dhcp6 import Dhcp6DictMode, Dhcp6ObjectMode
    from .disconnect_admins import DisconnectAdmins
    from .external_resource import ExternalResource
    from .firmware import Firmware
    from .fortiguard import FortiguardDictMode, FortiguardObjectMode
    from .fortimanager import FortimanagerDictMode, FortimanagerObjectMode
    from .fsck import FsckDictMode, FsckObjectMode
    from .ha_peer import HaPeer
    from .hscalefw_license import HscalefwLicense
    from .interface import Interface
    from .ipam import IpamDictMode, IpamObjectMode
    from .logdisk import LogdiskDictMode, LogdiskObjectMode
    from .lte_modem import LteModem
    from .modem import Modem
    from .modem5g import Modem5gDictMode, Modem5gObjectMode
    from .ntp import NtpDictMode, NtpObjectMode
    from .object import ObjectDictMode, ObjectObjectMode
    from .os import OsDictMode, OsObjectMode
    from .password_policy_conform import PasswordPolicyConform
    from .performance import PerformanceDictMode, PerformanceObjectMode
    from .private_data_encryption import PrivateDataEncryption
    from .process import ProcessDictMode, ProcessObjectMode
    from .resource import ResourceDictMode, ResourceObjectMode
    from .sandbox import SandboxDictMode, SandboxObjectMode
    from .sdn_connector import SdnConnector
    from .time import Time
    from .traffic_history import TrafficHistory
    from .upgrade_report import UpgradeReport
    from .usb_device import UsbDevice
    from .usb_log import UsbLog
    from .vmlicense import VmlicenseDictMode, VmlicenseObjectMode

__all__ = [
    "AcmeCertificateStatus",
    "AcquiredDns",
    "AvailableCertificates",
    "CheckPortAvailability",
    "CurrentAdmins",
    "GlobalResources",
    "GlobalSearch",
    "HaBackupHbUsed",
    "HaChecksums",
    "HaHistory",
    "HaHwInterface",
    "HaNonsyncChecksums",
    "HaStatistics",
    "HaTableChecksums",
    "InterfaceConnectedAdminsInfo",
    "Ipconf",
    "LinkMonitor",
    "Modem3g",
    "MonitorSensor",
    "ResolveFqdn",
    "RunningProcesses",
    "SensorInfo",
    "Status",
    "Storage",
    "Timezone",
    "TrustedCertAuthorities",
    "VdomLink",
    "VdomResource",
    "VmInformation",
    "SystemDictMode",
    "SystemObjectMode",
]

class SystemDictMode:
    """SYSTEM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    admin: AdminDictMode
    api_user: ApiUser
    automation_action: AutomationAction
    automation_stitch: AutomationStitch
    available_interfaces: AvailableInterfaces
    botnet: Botnet
    botnet_domains: BotnetDomains
    central_management: CentralManagement
    certificate: CertificateDictMode
    change_password: ChangePassword
    cluster: ClusterDictMode
    com_log: ComLog
    config: ConfigDictMode
    config_error_log: ConfigErrorLog
    config_revision: ConfigRevision
    config_script: ConfigScript
    config_sync: ConfigSync
    crash_log: CrashLog
    csf: Csf
    debug: DebugDictMode
    dhcp: Dhcp
    dhcp6: Dhcp6DictMode
    disconnect_admins: DisconnectAdmins
    external_resource: ExternalResource
    firmware: Firmware
    fortiguard: FortiguardDictMode
    fortimanager: FortimanagerDictMode
    fsck: FsckDictMode
    ha_peer: HaPeer
    hscalefw_license: HscalefwLicense
    interface: Interface
    ipam: IpamDictMode
    logdisk: LogdiskDictMode
    lte_modem: LteModem
    modem: Modem
    modem5g: Modem5gDictMode
    ntp: NtpDictMode
    object: ObjectDictMode
    os: OsDictMode
    password_policy_conform: PasswordPolicyConform
    performance: PerformanceDictMode
    private_data_encryption: PrivateDataEncryption
    process: ProcessDictMode
    resource: ResourceDictMode
    sandbox: SandboxDictMode
    sdn_connector: SdnConnector
    time: Time
    traffic_history: TrafficHistory
    upgrade_report: UpgradeReport
    usb_device: UsbDevice
    usb_log: UsbLog
    vmlicense: VmlicenseDictMode
    acme_certificate_status: AcmeCertificateStatusDictMode
    acquired_dns: AcquiredDnsDictMode
    available_certificates: AvailableCertificatesDictMode
    check_port_availability: CheckPortAvailabilityDictMode
    current_admins: CurrentAdminsDictMode
    global_resources: GlobalResourcesDictMode
    global_search: GlobalSearchDictMode
    ha_backup_hb_used: HaBackupHbUsedDictMode
    ha_checksums: HaChecksumsDictMode
    ha_history: HaHistoryDictMode
    ha_hw_interface: HaHwInterfaceDictMode
    ha_nonsync_checksums: HaNonsyncChecksumsDictMode
    ha_statistics: HaStatisticsDictMode
    ha_table_checksums: HaTableChecksumsDictMode
    interface_connected_admins_info: InterfaceConnectedAdminsInfoDictMode
    ipconf: IpconfDictMode
    link_monitor: LinkMonitorDictMode
    modem3g: Modem3gDictMode
    monitor_sensor: MonitorSensorDictMode
    resolve_fqdn: ResolveFqdnDictMode
    running_processes: RunningProcessesDictMode
    sensor_info: SensorInfoDictMode
    status: StatusDictMode
    storage: StorageDictMode
    timezone: TimezoneDictMode
    trusted_cert_authorities: TrustedCertAuthoritiesDictMode
    vdom_link: VdomLinkDictMode
    vdom_resource: VdomResourceDictMode
    vm_information: VmInformationDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...


class SystemObjectMode:
    """SYSTEM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    admin: AdminObjectMode
    api_user: ApiUser
    automation_action: AutomationAction
    automation_stitch: AutomationStitch
    available_interfaces: AvailableInterfaces
    botnet: Botnet
    botnet_domains: BotnetDomains
    central_management: CentralManagement
    certificate: CertificateObjectMode
    change_password: ChangePassword
    cluster: ClusterObjectMode
    com_log: ComLog
    config: ConfigObjectMode
    config_error_log: ConfigErrorLog
    config_revision: ConfigRevision
    config_script: ConfigScript
    config_sync: ConfigSync
    crash_log: CrashLog
    csf: Csf
    debug: DebugObjectMode
    dhcp: Dhcp
    dhcp6: Dhcp6ObjectMode
    disconnect_admins: DisconnectAdmins
    external_resource: ExternalResource
    firmware: Firmware
    fortiguard: FortiguardObjectMode
    fortimanager: FortimanagerObjectMode
    fsck: FsckObjectMode
    ha_peer: HaPeer
    hscalefw_license: HscalefwLicense
    interface: Interface
    ipam: IpamObjectMode
    logdisk: LogdiskObjectMode
    lte_modem: LteModem
    modem: Modem
    modem5g: Modem5gObjectMode
    ntp: NtpObjectMode
    object: ObjectObjectMode
    os: OsObjectMode
    password_policy_conform: PasswordPolicyConform
    performance: PerformanceObjectMode
    private_data_encryption: PrivateDataEncryption
    process: ProcessObjectMode
    resource: ResourceObjectMode
    sandbox: SandboxObjectMode
    sdn_connector: SdnConnector
    time: Time
    traffic_history: TrafficHistory
    upgrade_report: UpgradeReport
    usb_device: UsbDevice
    usb_log: UsbLog
    vmlicense: VmlicenseObjectMode
    acme_certificate_status: AcmeCertificateStatusObjectMode
    acquired_dns: AcquiredDnsObjectMode
    available_certificates: AvailableCertificatesObjectMode
    check_port_availability: CheckPortAvailabilityObjectMode
    current_admins: CurrentAdminsObjectMode
    global_resources: GlobalResourcesObjectMode
    global_search: GlobalSearchObjectMode
    ha_backup_hb_used: HaBackupHbUsedObjectMode
    ha_checksums: HaChecksumsObjectMode
    ha_history: HaHistoryObjectMode
    ha_hw_interface: HaHwInterfaceObjectMode
    ha_nonsync_checksums: HaNonsyncChecksumsObjectMode
    ha_statistics: HaStatisticsObjectMode
    ha_table_checksums: HaTableChecksumsObjectMode
    interface_connected_admins_info: InterfaceConnectedAdminsInfoObjectMode
    ipconf: IpconfObjectMode
    link_monitor: LinkMonitorObjectMode
    modem3g: Modem3gObjectMode
    monitor_sensor: MonitorSensorObjectMode
    resolve_fqdn: ResolveFqdnObjectMode
    running_processes: RunningProcessesObjectMode
    sensor_info: SensorInfoObjectMode
    status: StatusObjectMode
    storage: StorageObjectMode
    timezone: TimezoneObjectMode
    trusted_cert_authorities: TrustedCertAuthoritiesObjectMode
    vdom_link: VdomLinkObjectMode
    vdom_resource: VdomResourceObjectMode
    vm_information: VmInformationObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...


# Base class for backwards compatibility
class System:
    """SYSTEM API category."""
    
    admin: Admin
    api_user: ApiUser
    automation_action: AutomationAction
    automation_stitch: AutomationStitch
    available_interfaces: AvailableInterfaces
    botnet: Botnet
    botnet_domains: BotnetDomains
    central_management: CentralManagement
    certificate: Certificate
    change_password: ChangePassword
    cluster: Cluster
    com_log: ComLog
    config: Config
    config_error_log: ConfigErrorLog
    config_revision: ConfigRevision
    config_script: ConfigScript
    config_sync: ConfigSync
    crash_log: CrashLog
    csf: Csf
    debug: Debug
    dhcp: Dhcp
    dhcp6: Dhcp6
    disconnect_admins: DisconnectAdmins
    external_resource: ExternalResource
    firmware: Firmware
    fortiguard: Fortiguard
    fortimanager: Fortimanager
    fsck: Fsck
    ha_peer: HaPeer
    hscalefw_license: HscalefwLicense
    interface: Interface
    ipam: Ipam
    logdisk: Logdisk
    lte_modem: LteModem
    modem: Modem
    modem5g: Modem5g
    ntp: Ntp
    object: Object
    os: Os
    password_policy_conform: PasswordPolicyConform
    performance: Performance
    private_data_encryption: PrivateDataEncryption
    process: Process
    resource: Resource
    sandbox: Sandbox
    sdn_connector: SdnConnector
    time: Time
    traffic_history: TrafficHistory
    upgrade_report: UpgradeReport
    usb_device: UsbDevice
    usb_log: UsbLog
    vmlicense: Vmlicense
    acme_certificate_status: AcmeCertificateStatus
    acquired_dns: AcquiredDns
    available_certificates: AvailableCertificates
    check_port_availability: CheckPortAvailability
    current_admins: CurrentAdmins
    global_resources: GlobalResources
    global_search: GlobalSearch
    ha_backup_hb_used: HaBackupHbUsed
    ha_checksums: HaChecksums
    ha_history: HaHistory
    ha_hw_interface: HaHwInterface
    ha_nonsync_checksums: HaNonsyncChecksums
    ha_statistics: HaStatistics
    ha_table_checksums: HaTableChecksums
    interface_connected_admins_info: InterfaceConnectedAdminsInfo
    ipconf: Ipconf
    link_monitor: LinkMonitor
    modem3g: Modem3g
    monitor_sensor: MonitorSensor
    resolve_fqdn: ResolveFqdn
    running_processes: RunningProcesses
    sensor_info: SensorInfo
    status: Status
    storage: Storage
    timezone: Timezone
    trusted_cert_authorities: TrustedCertAuthorities
    vdom_link: VdomLink
    vdom_resource: VdomResource
    vm_information: VmInformation

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...
