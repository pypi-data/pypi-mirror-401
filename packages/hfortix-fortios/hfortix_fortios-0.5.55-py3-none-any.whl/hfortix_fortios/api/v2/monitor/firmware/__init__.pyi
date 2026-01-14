"""Type stubs for FIRMWARE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .extension_device import ExtensionDevice, ExtensionDeviceDictMode, ExtensionDeviceObjectMode

__all__ = [
    "ExtensionDevice",
    "FirmwareDictMode",
    "FirmwareObjectMode",
]

class FirmwareDictMode:
    """FIRMWARE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    extension_device: ExtensionDeviceDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firmware category with HTTP client."""
        ...


class FirmwareObjectMode:
    """FIRMWARE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    extension_device: ExtensionDeviceObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firmware category with HTTP client."""
        ...


# Base class for backwards compatibility
class Firmware:
    """FIRMWARE API category."""
    
    extension_device: ExtensionDevice

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize firmware category with HTTP client."""
        ...
