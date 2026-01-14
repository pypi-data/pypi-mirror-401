"""Type stubs for LTE_MODEM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status, StatusDictMode, StatusObjectMode
    from .upgrade import Upgrade, UpgradeDictMode, UpgradeObjectMode
    from .upload import Upload, UploadDictMode, UploadObjectMode

__all__ = [
    "Status",
    "Upgrade",
    "Upload",
    "LteModemDictMode",
    "LteModemObjectMode",
]

class LteModemDictMode:
    """LTE_MODEM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    status: StatusDictMode
    upgrade: UpgradeDictMode
    upload: UploadDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lte_modem category with HTTP client."""
        ...


class LteModemObjectMode:
    """LTE_MODEM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    status: StatusObjectMode
    upgrade: UpgradeObjectMode
    upload: UploadObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lte_modem category with HTTP client."""
        ...


# Base class for backwards compatibility
class LteModem:
    """LTE_MODEM API category."""
    
    status: Status
    upgrade: Upgrade
    upload: Upload

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize lte_modem category with HTTP client."""
        ...
