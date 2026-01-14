"""Type stubs for DIAMETER_FILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .profile import Profile, ProfileDictMode, ProfileObjectMode

__all__ = [
    "Profile",
    "DiameterFilterDictMode",
    "DiameterFilterObjectMode",
]

class DiameterFilterDictMode:
    """DIAMETER_FILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    profile: ProfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize diameter_filter category with HTTP client."""
        ...


class DiameterFilterObjectMode:
    """DIAMETER_FILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    profile: ProfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize diameter_filter category with HTTP client."""
        ...


# Base class for backwards compatibility
class DiameterFilter:
    """DIAMETER_FILTER API category."""
    
    profile: Profile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize diameter_filter category with HTTP client."""
        ...
