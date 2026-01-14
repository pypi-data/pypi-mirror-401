"""Type stubs for USB_DEVICE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .eject import Eject, EjectDictMode, EjectObjectMode

__all__ = [
    "Eject",
    "UsbDeviceDictMode",
    "UsbDeviceObjectMode",
]

class UsbDeviceDictMode:
    """USB_DEVICE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    eject: EjectDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize usb_device category with HTTP client."""
        ...


class UsbDeviceObjectMode:
    """USB_DEVICE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    eject: EjectObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize usb_device category with HTTP client."""
        ...


# Base class for backwards compatibility
class UsbDevice:
    """USB_DEVICE API category."""
    
    eject: Eject

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize usb_device category with HTTP client."""
        ...
