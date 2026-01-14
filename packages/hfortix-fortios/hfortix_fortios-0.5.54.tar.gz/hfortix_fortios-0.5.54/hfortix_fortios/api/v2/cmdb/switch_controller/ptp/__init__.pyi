"""Type stubs for PTP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .interface_policy import InterfacePolicy, InterfacePolicyDictMode, InterfacePolicyObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode

__all__ = [
    "InterfacePolicy",
    "Profile",
    "PtpDictMode",
    "PtpObjectMode",
]

class PtpDictMode:
    """PTP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    interface_policy: InterfacePolicyDictMode
    profile: ProfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ptp category with HTTP client."""
        ...


class PtpObjectMode:
    """PTP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    interface_policy: InterfacePolicyObjectMode
    profile: ProfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ptp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ptp:
    """PTP API category."""
    
    interface_policy: InterfacePolicy
    profile: Profile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ptp category with HTTP client."""
        ...
