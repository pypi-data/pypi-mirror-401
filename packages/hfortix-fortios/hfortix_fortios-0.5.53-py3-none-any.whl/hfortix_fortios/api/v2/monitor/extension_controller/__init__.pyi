"""Type stubs for EXTENSION_CONTROLLER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fortigate import Fortigate, FortigateDictMode, FortigateObjectMode
    from .lan_extension_vdom_status import LanExtensionVdomStatus, LanExtensionVdomStatusDictMode, LanExtensionVdomStatusObjectMode

__all__ = [
    "Fortigate",
    "LanExtensionVdomStatus",
    "ExtensionControllerDictMode",
    "ExtensionControllerObjectMode",
]

class ExtensionControllerDictMode:
    """EXTENSION_CONTROLLER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    fortigate: FortigateDictMode
    lan_extension_vdom_status: LanExtensionVdomStatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extension_controller category with HTTP client."""
        ...


class ExtensionControllerObjectMode:
    """EXTENSION_CONTROLLER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    fortigate: FortigateObjectMode
    lan_extension_vdom_status: LanExtensionVdomStatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extension_controller category with HTTP client."""
        ...


# Base class for backwards compatibility
class ExtensionController:
    """EXTENSION_CONTROLLER API category."""
    
    fortigate: Fortigate
    lan_extension_vdom_status: LanExtensionVdomStatus

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extension_controller category with HTTP client."""
        ...
