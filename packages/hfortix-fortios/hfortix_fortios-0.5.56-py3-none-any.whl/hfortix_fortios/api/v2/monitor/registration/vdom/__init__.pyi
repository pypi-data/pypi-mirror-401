"""Type stubs for VDOM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .add_license import AddLicense, AddLicenseDictMode, AddLicenseObjectMode

__all__ = [
    "AddLicense",
    "VdomDictMode",
    "VdomObjectMode",
]

class VdomDictMode:
    """VDOM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    add_license: AddLicenseDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vdom category with HTTP client."""
        ...


class VdomObjectMode:
    """VDOM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    add_license: AddLicenseObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vdom category with HTTP client."""
        ...


# Base class for backwards compatibility
class Vdom:
    """VDOM API category."""
    
    add_license: AddLicense

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize vdom category with HTTP client."""
        ...
