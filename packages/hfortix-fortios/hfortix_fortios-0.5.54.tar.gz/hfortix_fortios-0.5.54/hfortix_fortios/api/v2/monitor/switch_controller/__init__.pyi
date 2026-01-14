"""Type stubs for SWITCH_CONTROLLER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .detected_device import DetectedDevice, DetectedDeviceDictMode, DetectedDeviceObjectMode
    from .known_nac_device_criteria_list import KnownNacDeviceCriteriaList, KnownNacDeviceCriteriaListDictMode, KnownNacDeviceCriteriaListObjectMode
    from .matched_devices import MatchedDevices, MatchedDevicesDictMode, MatchedDevicesObjectMode
    from .fsw_firmware import FswFirmware
    from .isl_lockdown import IslLockdown
    from .managed_switch import ManagedSwitch
    from .mclag_icl import MclagIcl
    from .nac_device import NacDevice
    from .recommendation import RecommendationDictMode, RecommendationObjectMode

__all__ = [
    "DetectedDevice",
    "KnownNacDeviceCriteriaList",
    "MatchedDevices",
    "SwitchControllerDictMode",
    "SwitchControllerObjectMode",
]

class SwitchControllerDictMode:
    """SWITCH_CONTROLLER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    fsw_firmware: FswFirmware
    isl_lockdown: IslLockdown
    managed_switch: ManagedSwitch
    mclag_icl: MclagIcl
    nac_device: NacDevice
    recommendation: RecommendationDictMode
    detected_device: DetectedDeviceDictMode
    known_nac_device_criteria_list: KnownNacDeviceCriteriaListDictMode
    matched_devices: MatchedDevicesDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize switch_controller category with HTTP client."""
        ...


class SwitchControllerObjectMode:
    """SWITCH_CONTROLLER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    fsw_firmware: FswFirmware
    isl_lockdown: IslLockdown
    managed_switch: ManagedSwitch
    mclag_icl: MclagIcl
    nac_device: NacDevice
    recommendation: RecommendationObjectMode
    detected_device: DetectedDeviceObjectMode
    known_nac_device_criteria_list: KnownNacDeviceCriteriaListObjectMode
    matched_devices: MatchedDevicesObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize switch_controller category with HTTP client."""
        ...


# Base class for backwards compatibility
class SwitchController:
    """SWITCH_CONTROLLER API category."""
    
    fsw_firmware: FswFirmware
    isl_lockdown: IslLockdown
    managed_switch: ManagedSwitch
    mclag_icl: MclagIcl
    nac_device: NacDevice
    recommendation: Recommendation
    detected_device: DetectedDevice
    known_nac_device_criteria_list: KnownNacDeviceCriteriaList
    matched_devices: MatchedDevices

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize switch_controller category with HTTP client."""
        ...
