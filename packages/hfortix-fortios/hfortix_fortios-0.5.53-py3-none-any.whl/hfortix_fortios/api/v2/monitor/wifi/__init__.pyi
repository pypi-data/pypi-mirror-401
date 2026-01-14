"""Type stubs for WIFI category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .ap_channels import ApChannels, ApChannelsDictMode, ApChannelsObjectMode
    from .ap_names import ApNames, ApNamesDictMode, ApNamesObjectMode
    from .ap_status import ApStatus, ApStatusDictMode, ApStatusObjectMode
    from .interfering_ap import InterferingAp, InterferingApDictMode, InterferingApObjectMode
    from .matched_devices import MatchedDevices, MatchedDevicesDictMode, MatchedDevicesObjectMode
    from .meta import Meta, MetaDictMode, MetaObjectMode
    from .station_capability import StationCapability, StationCapabilityDictMode, StationCapabilityObjectMode
    from .statistics import Statistics, StatisticsDictMode, StatisticsObjectMode
    from .unassociated_devices import UnassociatedDevices, UnassociatedDevicesDictMode, UnassociatedDevicesObjectMode
    from .ap_profile import ApProfile
    from .client_ns import Client
    from .euclid import Euclid
    from .firmware import Firmware
    from .managed_ap import ManagedAp
    from .nac_device import NacDevice
    from .network import NetworkDictMode, NetworkObjectMode
    from .region_image import RegionImage
    from .rogue_ap import RogueAp
    from .spectrum import Spectrum
    from .ssid import SsidDictMode, SsidObjectMode
    from .vlan_probe import VlanProbe

__all__ = [
    "ApChannels",
    "ApNames",
    "ApStatus",
    "InterferingAp",
    "MatchedDevices",
    "Meta",
    "StationCapability",
    "Statistics",
    "UnassociatedDevices",
    "WifiDictMode",
    "WifiObjectMode",
]

class WifiDictMode:
    """WIFI API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ap_profile: ApProfile
    client: Client
    euclid: Euclid
    firmware: Firmware
    managed_ap: ManagedAp
    nac_device: NacDevice
    network: NetworkDictMode
    region_image: RegionImage
    rogue_ap: RogueAp
    spectrum: Spectrum
    ssid: SsidDictMode
    vlan_probe: VlanProbe
    ap_channels: ApChannelsDictMode
    ap_names: ApNamesDictMode
    ap_status: ApStatusDictMode
    interfering_ap: InterferingApDictMode
    matched_devices: MatchedDevicesDictMode
    meta: MetaDictMode
    station_capability: StationCapabilityDictMode
    statistics: StatisticsDictMode
    unassociated_devices: UnassociatedDevicesDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wifi category with HTTP client."""
        ...


class WifiObjectMode:
    """WIFI API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ap_profile: ApProfile
    client: Client
    euclid: Euclid
    firmware: Firmware
    managed_ap: ManagedAp
    nac_device: NacDevice
    network: NetworkObjectMode
    region_image: RegionImage
    rogue_ap: RogueAp
    spectrum: Spectrum
    ssid: SsidObjectMode
    vlan_probe: VlanProbe
    ap_channels: ApChannelsObjectMode
    ap_names: ApNamesObjectMode
    ap_status: ApStatusObjectMode
    interfering_ap: InterferingApObjectMode
    matched_devices: MatchedDevicesObjectMode
    meta: MetaObjectMode
    station_capability: StationCapabilityObjectMode
    statistics: StatisticsObjectMode
    unassociated_devices: UnassociatedDevicesObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wifi category with HTTP client."""
        ...


# Base class for backwards compatibility
class Wifi:
    """WIFI API category."""
    
    ap_profile: ApProfile
    client: Client
    euclid: Euclid
    firmware: Firmware
    managed_ap: ManagedAp
    nac_device: NacDevice
    network: Network
    region_image: RegionImage
    rogue_ap: RogueAp
    spectrum: Spectrum
    ssid: Ssid
    vlan_probe: VlanProbe
    ap_channels: ApChannels
    ap_names: ApNames
    ap_status: ApStatus
    interfering_ap: InterferingAp
    matched_devices: MatchedDevices
    meta: Meta
    station_capability: StationCapability
    statistics: Statistics
    unassociated_devices: UnassociatedDevices

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wifi category with HTTP client."""
        ...
