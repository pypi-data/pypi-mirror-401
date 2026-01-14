"""Type stubs for EXTENSION_CONTROLLER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .dataplan import Dataplan, DataplanDictMode, DataplanObjectMode
    from .extender import Extender, ExtenderDictMode, ExtenderObjectMode
    from .extender_profile import ExtenderProfile, ExtenderProfileDictMode, ExtenderProfileObjectMode
    from .extender_vap import ExtenderVap, ExtenderVapDictMode, ExtenderVapObjectMode
    from .fortigate import Fortigate, FortigateDictMode, FortigateObjectMode
    from .fortigate_profile import FortigateProfile, FortigateProfileDictMode, FortigateProfileObjectMode

__all__ = [
    "Dataplan",
    "Extender",
    "ExtenderProfile",
    "ExtenderVap",
    "Fortigate",
    "FortigateProfile",
    "ExtensionControllerDictMode",
    "ExtensionControllerObjectMode",
]

class ExtensionControllerDictMode:
    """EXTENSION_CONTROLLER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    dataplan: DataplanDictMode
    extender: ExtenderDictMode
    extender_profile: ExtenderProfileDictMode
    extender_vap: ExtenderVapDictMode
    fortigate: FortigateDictMode
    fortigate_profile: FortigateProfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extension_controller category with HTTP client."""
        ...


class ExtensionControllerObjectMode:
    """EXTENSION_CONTROLLER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    dataplan: DataplanObjectMode
    extender: ExtenderObjectMode
    extender_profile: ExtenderProfileObjectMode
    extender_vap: ExtenderVapObjectMode
    fortigate: FortigateObjectMode
    fortigate_profile: FortigateProfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extension_controller category with HTTP client."""
        ...


# Base class for backwards compatibility
class ExtensionController:
    """EXTENSION_CONTROLLER API category."""
    
    dataplan: Dataplan
    extender: Extender
    extender_profile: ExtenderProfile
    extender_vap: ExtenderVap
    fortigate: Fortigate
    fortigate_profile: FortigateProfile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize extension_controller category with HTTP client."""
        ...
