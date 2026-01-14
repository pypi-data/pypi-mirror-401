"""Type stubs for ENDPOINT_CONTROL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fctems import Fctems, FctemsDictMode, FctemsObjectMode
    from .fctems_override import FctemsOverride, FctemsOverrideDictMode, FctemsOverrideObjectMode
    from .settings import Settings, SettingsDictMode, SettingsObjectMode

__all__ = [
    "Fctems",
    "FctemsOverride",
    "Settings",
    "EndpointControlDictMode",
    "EndpointControlObjectMode",
]

class EndpointControlDictMode:
    """ENDPOINT_CONTROL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    fctems: FctemsDictMode
    fctems_override: FctemsOverrideDictMode
    settings: SettingsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize endpoint_control category with HTTP client."""
        ...


class EndpointControlObjectMode:
    """ENDPOINT_CONTROL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    fctems: FctemsObjectMode
    fctems_override: FctemsOverrideObjectMode
    settings: SettingsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize endpoint_control category with HTTP client."""
        ...


# Base class for backwards compatibility
class EndpointControl:
    """ENDPOINT_CONTROL API category."""
    
    fctems: Fctems
    fctems_override: FctemsOverride
    settings: Settings

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize endpoint_control category with HTTP client."""
        ...
