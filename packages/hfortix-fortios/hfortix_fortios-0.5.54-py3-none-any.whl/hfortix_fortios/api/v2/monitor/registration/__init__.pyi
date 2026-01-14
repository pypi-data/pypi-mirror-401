"""Type stubs for REGISTRATION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .forticare import ForticareDictMode, ForticareObjectMode
    from .forticloud import ForticloudDictMode, ForticloudObjectMode
    from .vdom import VdomDictMode, VdomObjectMode

__all__ = [
    "RegistrationDictMode",
    "RegistrationObjectMode",
]

class RegistrationDictMode:
    """REGISTRATION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    forticare: ForticareDictMode
    forticloud: ForticloudDictMode
    vdom: VdomDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize registration category with HTTP client."""
        ...


class RegistrationObjectMode:
    """REGISTRATION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    forticare: ForticareObjectMode
    forticloud: ForticloudObjectMode
    vdom: VdomObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize registration category with HTTP client."""
        ...


# Base class for backwards compatibility
class Registration:
    """REGISTRATION API category."""
    
    forticare: Forticare
    forticloud: Forticloud
    vdom: Vdom

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize registration category with HTTP client."""
        ...
