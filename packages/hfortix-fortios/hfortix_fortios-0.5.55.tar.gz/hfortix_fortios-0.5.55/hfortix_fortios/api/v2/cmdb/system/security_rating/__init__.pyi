"""Type stubs for SECURITY_RATING category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .controls import Controls, ControlsDictMode, ControlsObjectMode
    from .settings import Settings, SettingsDictMode, SettingsObjectMode

__all__ = [
    "Controls",
    "Settings",
    "SecurityRatingDictMode",
    "SecurityRatingObjectMode",
]

class SecurityRatingDictMode:
    """SECURITY_RATING API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    controls: ControlsDictMode
    settings: SettingsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_rating category with HTTP client."""
        ...


class SecurityRatingObjectMode:
    """SECURITY_RATING API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    controls: ControlsObjectMode
    settings: SettingsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_rating category with HTTP client."""
        ...


# Base class for backwards compatibility
class SecurityRating:
    """SECURITY_RATING API category."""
    
    controls: Controls
    settings: Settings

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_rating category with HTTP client."""
        ...
