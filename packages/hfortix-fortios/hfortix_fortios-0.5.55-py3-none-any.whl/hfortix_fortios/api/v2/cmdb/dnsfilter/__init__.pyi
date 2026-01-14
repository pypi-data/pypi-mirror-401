"""Type stubs for DNSFILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .domain_filter import DomainFilter, DomainFilterDictMode, DomainFilterObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode

__all__ = [
    "DomainFilter",
    "Profile",
    "DnsfilterDictMode",
    "DnsfilterObjectMode",
]

class DnsfilterDictMode:
    """DNSFILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    domain_filter: DomainFilterDictMode
    profile: ProfileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dnsfilter category with HTTP client."""
        ...


class DnsfilterObjectMode:
    """DNSFILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    domain_filter: DomainFilterObjectMode
    profile: ProfileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dnsfilter category with HTTP client."""
        ...


# Base class for backwards compatibility
class Dnsfilter:
    """DNSFILTER API category."""
    
    domain_filter: DomainFilter
    profile: Profile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize dnsfilter category with HTTP client."""
        ...
