"""Type stubs for MANAGED_SWITCH category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .bios import Bios, BiosDictMode, BiosObjectMode
    from .bounce_port import BouncePort, BouncePortDictMode, BouncePortObjectMode
    from .cable_status import CableStatus, CableStatusDictMode, CableStatusObjectMode
    from .dhcp_snooping import DhcpSnooping, DhcpSnoopingDictMode, DhcpSnoopingObjectMode
    from .faceplate_xml import FaceplateXml, FaceplateXmlDictMode, FaceplateXmlObjectMode
    from .factory_reset import FactoryReset, FactoryResetDictMode, FactoryResetObjectMode
    from .health_status import HealthStatus, HealthStatusDictMode, HealthStatusObjectMode
    from .models import Models, ModelsDictMode, ModelsObjectMode
    from .poe_reset import PoeReset, PoeResetDictMode, PoeResetObjectMode
    from .port_health import PortHealth, PortHealthDictMode, PortHealthObjectMode
    from .port_stats import PortStats, PortStatsDictMode, PortStatsObjectMode
    from .port_stats_reset import PortStatsReset, PortStatsResetDictMode, PortStatsResetObjectMode
    from .restart import Restart, RestartDictMode, RestartObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode
    from .transceivers import Transceivers, TransceiversDictMode, TransceiversObjectMode
    from .tx_rx import TxRx, TxRxDictMode, TxRxObjectMode
    from .update import Update, UpdateDictMode, UpdateObjectMode

__all__ = [
    "Bios",
    "BouncePort",
    "CableStatus",
    "DhcpSnooping",
    "FaceplateXml",
    "FactoryReset",
    "HealthStatus",
    "Models",
    "PoeReset",
    "PortHealth",
    "PortStats",
    "PortStatsReset",
    "Restart",
    "Status",
    "Transceivers",
    "TxRx",
    "Update",
    "ManagedSwitchDictMode",
    "ManagedSwitchObjectMode",
]

class ManagedSwitchDictMode:
    """MANAGED_SWITCH API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    bios: BiosDictMode
    bounce_port: BouncePortDictMode
    cable_status: CableStatusDictMode
    dhcp_snooping: DhcpSnoopingDictMode
    faceplate_xml: FaceplateXmlDictMode
    factory_reset: FactoryResetDictMode
    health_status: HealthStatusDictMode
    models: ModelsDictMode
    poe_reset: PoeResetDictMode
    port_health: PortHealthDictMode
    port_stats: PortStatsDictMode
    port_stats_reset: PortStatsResetDictMode
    restart: RestartDictMode
    status: StatusDictMode
    transceivers: TransceiversDictMode
    tx_rx: TxRxDictMode
    update: UpdateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize managed_switch category with HTTP client."""
        ...


class ManagedSwitchObjectMode:
    """MANAGED_SWITCH API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    bios: BiosObjectMode
    bounce_port: BouncePortObjectMode
    cable_status: CableStatusObjectMode
    dhcp_snooping: DhcpSnoopingObjectMode
    faceplate_xml: FaceplateXmlObjectMode
    factory_reset: FactoryResetObjectMode
    health_status: HealthStatusObjectMode
    models: ModelsObjectMode
    poe_reset: PoeResetObjectMode
    port_health: PortHealthObjectMode
    port_stats: PortStatsObjectMode
    port_stats_reset: PortStatsResetObjectMode
    restart: RestartObjectMode
    status: StatusObjectMode
    transceivers: TransceiversObjectMode
    tx_rx: TxRxObjectMode
    update: UpdateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize managed_switch category with HTTP client."""
        ...


# Base class for backwards compatibility
class ManagedSwitch:
    """MANAGED_SWITCH API category."""
    
    bios: Bios
    bounce_port: BouncePort
    cable_status: CableStatus
    dhcp_snooping: DhcpSnooping
    faceplate_xml: FaceplateXml
    factory_reset: FactoryReset
    health_status: HealthStatus
    models: Models
    poe_reset: PoeReset
    port_health: PortHealth
    port_stats: PortStats
    port_stats_reset: PortStatsReset
    restart: Restart
    status: Status
    transceivers: Transceivers
    tx_rx: TxRx
    update: Update

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize managed_switch category with HTTP client."""
        ...
