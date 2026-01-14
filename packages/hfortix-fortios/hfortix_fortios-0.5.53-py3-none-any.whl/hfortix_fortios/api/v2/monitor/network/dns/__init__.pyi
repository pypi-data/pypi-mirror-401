"""Type stubs for DNS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .latency import Latency, LatencyDictMode, LatencyObjectMode

__all__ = [
    "Latency",
    "DnsDictMode",
    "DnsObjectMode",
]

class DnsDictMode:
    """DNS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    latency: LatencyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dns category with HTTP client."""
        ...


class DnsObjectMode:
    """DNS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    latency: LatencyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dns category with HTTP client."""
        ...


# Base class for backwards compatibility
class Dns:
    """DNS API category."""
    
    latency: Latency

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dns category with HTTP client."""
        ...
