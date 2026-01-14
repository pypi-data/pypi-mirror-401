"""Type stubs for ISL_LOCKDOWN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .status import Status, StatusDictMode, StatusObjectMode
    from .update import Update, UpdateDictMode, UpdateObjectMode

__all__ = [
    "Status",
    "Update",
    "IslLockdownDictMode",
    "IslLockdownObjectMode",
]

class IslLockdownDictMode:
    """ISL_LOCKDOWN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    status: StatusDictMode
    update: UpdateDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize isl_lockdown category with HTTP client."""
        ...


class IslLockdownObjectMode:
    """ISL_LOCKDOWN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    status: StatusObjectMode
    update: UpdateObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize isl_lockdown category with HTTP client."""
        ...


# Base class for backwards compatibility
class IslLockdown:
    """ISL_LOCKDOWN API category."""
    
    status: Status
    update: Update

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize isl_lockdown category with HTTP client."""
        ...
