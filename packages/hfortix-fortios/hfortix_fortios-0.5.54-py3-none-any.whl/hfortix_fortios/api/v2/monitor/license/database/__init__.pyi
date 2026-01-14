"""Type stubs for DATABASE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .upgrade import Upgrade, UpgradeDictMode, UpgradeObjectMode

__all__ = [
    "Upgrade",
    "DatabaseDictMode",
    "DatabaseObjectMode",
]

class DatabaseDictMode:
    """DATABASE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    upgrade: UpgradeDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize database category with HTTP client."""
        ...


class DatabaseObjectMode:
    """DATABASE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    upgrade: UpgradeObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize database category with HTTP client."""
        ...


# Base class for backwards compatibility
class Database:
    """DATABASE API category."""
    
    upgrade: Upgrade

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize database category with HTTP client."""
        ...
