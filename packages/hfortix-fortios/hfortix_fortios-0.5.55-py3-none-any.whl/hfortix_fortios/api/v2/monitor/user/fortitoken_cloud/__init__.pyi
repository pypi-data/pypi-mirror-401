"""Type stubs for FORTITOKEN_CLOUD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status, StatusDictMode, StatusObjectMode
    from .trial import Trial, TrialDictMode, TrialObjectMode

__all__ = [
    "Status",
    "Trial",
    "FortitokenCloudDictMode",
    "FortitokenCloudObjectMode",
]

class FortitokenCloudDictMode:
    """FORTITOKEN_CLOUD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    status: StatusDictMode
    trial: TrialDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortitoken_cloud category with HTTP client."""
        ...


class FortitokenCloudObjectMode:
    """FORTITOKEN_CLOUD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    status: StatusObjectMode
    trial: TrialObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortitoken_cloud category with HTTP client."""
        ...


# Base class for backwards compatibility
class FortitokenCloud:
    """FORTITOKEN_CLOUD API category."""
    
    status: Status
    trial: Trial

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortitoken_cloud category with HTTP client."""
        ...
