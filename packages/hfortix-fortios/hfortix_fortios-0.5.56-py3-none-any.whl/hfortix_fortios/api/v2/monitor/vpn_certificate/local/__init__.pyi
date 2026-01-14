"""Type stubs for LOCAL category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .create import Create, CreateDictMode, CreateObjectMode
    from .import_ import Import, ImportDictMode, ImportObjectMode

__all__ = [
    "Create",
    "Import",
    "LocalDictMode",
    "LocalObjectMode",
]

class LocalDictMode:
    """LOCAL API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    create: CreateDictMode
    import_: ImportDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local category with HTTP client."""
        ...


class LocalObjectMode:
    """LOCAL API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    create: CreateObjectMode
    import_: ImportObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local category with HTTP client."""
        ...


# Base class for backwards compatibility
class Local:
    """LOCAL API category."""
    
    create: Create
    import_: Import

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize local category with HTTP client."""
        ...
