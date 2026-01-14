"""Type stubs for LLDP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .network_policy import NetworkPolicy, NetworkPolicyDictMode, NetworkPolicyObjectMode

__all__ = [
    "NetworkPolicy",
    "LldpDictMode",
    "LldpObjectMode",
]

class LldpDictMode:
    """LLDP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    network_policy: NetworkPolicyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lldp category with HTTP client."""
        ...


class LldpObjectMode:
    """LLDP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    network_policy: NetworkPolicyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lldp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Lldp:
    """LLDP API category."""
    
    network_policy: NetworkPolicy

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lldp category with HTTP client."""
        ...
