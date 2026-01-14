"""Type stubs for SYSTEM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fabric_admin_lockout_exists_on_firmware_update import FabricAdminLockoutExistsOnFirmwareUpdate, FabricAdminLockoutExistsOnFirmwareUpdateDictMode, FabricAdminLockoutExistsOnFirmwareUpdateObjectMode
    from .fabric_time_in_sync import FabricTimeInSync, FabricTimeInSyncDictMode, FabricTimeInSyncObjectMode
    from .psirt_vulnerabilities import PsirtVulnerabilities, PsirtVulnerabilitiesDictMode, PsirtVulnerabilitiesObjectMode

__all__ = [
    "FabricAdminLockoutExistsOnFirmwareUpdate",
    "FabricTimeInSync",
    "PsirtVulnerabilities",
    "SystemDictMode",
    "SystemObjectMode",
]

class SystemDictMode:
    """SYSTEM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    fabric_admin_lockout_exists_on_firmware_update: FabricAdminLockoutExistsOnFirmwareUpdateDictMode
    fabric_time_in_sync: FabricTimeInSyncDictMode
    psirt_vulnerabilities: PsirtVulnerabilitiesDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...


class SystemObjectMode:
    """SYSTEM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    fabric_admin_lockout_exists_on_firmware_update: FabricAdminLockoutExistsOnFirmwareUpdateObjectMode
    fabric_time_in_sync: FabricTimeInSyncObjectMode
    psirt_vulnerabilities: PsirtVulnerabilitiesObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...


# Base class for backwards compatibility
class System:
    """SYSTEM API category."""
    
    fabric_admin_lockout_exists_on_firmware_update: FabricAdminLockoutExistsOnFirmwareUpdate
    fabric_time_in_sync: FabricTimeInSync
    psirt_vulnerabilities: PsirtVulnerabilities

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize system category with HTTP client."""
        ...
