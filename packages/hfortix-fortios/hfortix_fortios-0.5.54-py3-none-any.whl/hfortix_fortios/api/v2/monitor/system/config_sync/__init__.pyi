"""Type stubs for CONFIG_SYNC category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status, StatusDictMode, StatusObjectMode

__all__ = [
    "Status",
    "ConfigSyncDictMode",
    "ConfigSyncObjectMode",
]

class ConfigSyncDictMode:
    """CONFIG_SYNC API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    status: StatusDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize config_sync category with HTTP client."""
        ...


class ConfigSyncObjectMode:
    """CONFIG_SYNC API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    status: StatusObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize config_sync category with HTTP client."""
        ...


# Base class for backwards compatibility
class ConfigSync:
    """CONFIG_SYNC API category."""
    
    status: Status

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize config_sync category with HTTP client."""
        ...
