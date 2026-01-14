"""Type stubs for NTP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status, StatusDictMode, StatusObjectMode

__all__ = [
    "Status",
    "NtpDictMode",
    "NtpObjectMode",
]

class NtpDictMode:
    """NTP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    status: StatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ntp category with HTTP client."""
        ...


class NtpObjectMode:
    """NTP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    status: StatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ntp category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ntp:
    """NTP API category."""
    
    status: Status

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ntp category with HTTP client."""
        ...
