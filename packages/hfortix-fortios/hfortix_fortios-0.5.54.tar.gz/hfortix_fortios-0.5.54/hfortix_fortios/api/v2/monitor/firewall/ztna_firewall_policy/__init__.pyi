"""Type stubs for ZTNA_FIREWALL_POLICY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .clear_counters import ClearCounters, ClearCountersDictMode, ClearCountersObjectMode

__all__ = [
    "ClearCounters",
    "ZtnaFirewallPolicyDictMode",
    "ZtnaFirewallPolicyObjectMode",
]

class ZtnaFirewallPolicyDictMode:
    """ZTNA_FIREWALL_POLICY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    clear_counters: ClearCountersDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ztna_firewall_policy category with HTTP client."""
        ...


class ZtnaFirewallPolicyObjectMode:
    """ZTNA_FIREWALL_POLICY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    clear_counters: ClearCountersObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ztna_firewall_policy category with HTTP client."""
        ...


# Base class for backwards compatibility
class ZtnaFirewallPolicy:
    """ZTNA_FIREWALL_POLICY API category."""
    
    clear_counters: ClearCounters

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ztna_firewall_policy category with HTTP client."""
        ...
