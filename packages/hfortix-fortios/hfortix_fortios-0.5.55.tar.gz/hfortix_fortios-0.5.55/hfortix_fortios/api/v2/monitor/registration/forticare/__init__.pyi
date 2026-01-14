"""Type stubs for FORTICARE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .add_license import AddLicense, AddLicenseDictMode, AddLicenseObjectMode
    from .check_connectivity import CheckConnectivity, CheckConnectivityDictMode, CheckConnectivityObjectMode
    from .create import Create, CreateDictMode, CreateObjectMode
    from .deregister_device import DeregisterDevice, DeregisterDeviceDictMode, DeregisterDeviceObjectMode
    from .login import Login, LoginDictMode, LoginObjectMode
    from .transfer import Transfer, TransferDictMode, TransferObjectMode

__all__ = [
    "AddLicense",
    "CheckConnectivity",
    "Create",
    "DeregisterDevice",
    "Login",
    "Transfer",
    "ForticareDictMode",
    "ForticareObjectMode",
]

class ForticareDictMode:
    """FORTICARE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    add_license: AddLicenseDictMode
    check_connectivity: CheckConnectivityDictMode
    create: CreateDictMode
    deregister_device: DeregisterDeviceDictMode
    login: LoginDictMode
    transfer: TransferDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticare category with HTTP client."""
        ...


class ForticareObjectMode:
    """FORTICARE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    add_license: AddLicenseObjectMode
    check_connectivity: CheckConnectivityObjectMode
    create: CreateObjectMode
    deregister_device: DeregisterDeviceObjectMode
    login: LoginObjectMode
    transfer: TransferObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticare category with HTTP client."""
        ...


# Base class for backwards compatibility
class Forticare:
    """FORTICARE API category."""
    
    add_license: AddLicense
    check_connectivity: CheckConnectivity
    create: Create
    deregister_device: DeregisterDevice
    login: Login
    transfer: Transfer

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize forticare category with HTTP client."""
        ...
