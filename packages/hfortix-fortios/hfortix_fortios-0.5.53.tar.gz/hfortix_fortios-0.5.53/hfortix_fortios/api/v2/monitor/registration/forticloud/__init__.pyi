"""Type stubs for FORTICLOUD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .device_status import DeviceStatus, DeviceStatusDictMode, DeviceStatusObjectMode
    from .disclaimer import Disclaimer, DisclaimerDictMode, DisclaimerObjectMode
    from .domains import Domains, DomainsDictMode, DomainsObjectMode
    from .login import Login, LoginDictMode, LoginObjectMode
    from .logout import Logout, LogoutDictMode, LogoutObjectMode
    from .migrate import Migrate, MigrateDictMode, MigrateObjectMode
    from .register_device import RegisterDevice, RegisterDeviceDictMode, RegisterDeviceObjectMode

__all__ = [
    "DeviceStatus",
    "Disclaimer",
    "Domains",
    "Login",
    "Logout",
    "Migrate",
    "RegisterDevice",
    "ForticloudDictMode",
    "ForticloudObjectMode",
]

class ForticloudDictMode:
    """FORTICLOUD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    device_status: DeviceStatusDictMode
    disclaimer: DisclaimerDictMode
    domains: DomainsDictMode
    login: LoginDictMode
    logout: LogoutDictMode
    migrate: MigrateDictMode
    register_device: RegisterDeviceDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticloud category with HTTP client."""
        ...


class ForticloudObjectMode:
    """FORTICLOUD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    device_status: DeviceStatusObjectMode
    disclaimer: DisclaimerObjectMode
    domains: DomainsObjectMode
    login: LoginObjectMode
    logout: LogoutObjectMode
    migrate: MigrateObjectMode
    register_device: RegisterDeviceObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticloud category with HTTP client."""
        ...


# Base class for backwards compatibility
class Forticloud:
    """FORTICLOUD API category."""
    
    device_status: DeviceStatus
    disclaimer: Disclaimer
    domains: Domains
    login: Login
    logout: Logout
    migrate: Migrate
    register_device: RegisterDevice

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticloud category with HTTP client."""
        ...
