"""Type stubs for CLEARPASS_ADDRESS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .add import Add, AddDictMode, AddObjectMode
    from .delete import Delete, DeleteDictMode, DeleteObjectMode

__all__ = [
    "Add",
    "Delete",
    "ClearpassAddressDictMode",
    "ClearpassAddressObjectMode",
]

class ClearpassAddressDictMode:
    """CLEARPASS_ADDRESS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    add: AddDictMode
    delete: DeleteDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize clearpass_address category with HTTP client."""
        ...


class ClearpassAddressObjectMode:
    """CLEARPASS_ADDRESS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    add: AddObjectMode
    delete: DeleteObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize clearpass_address category with HTTP client."""
        ...


# Base class for backwards compatibility
class ClearpassAddress:
    """CLEARPASS_ADDRESS API category."""
    
    add: Add
    delete: Delete

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize clearpass_address category with HTTP client."""
        ...
