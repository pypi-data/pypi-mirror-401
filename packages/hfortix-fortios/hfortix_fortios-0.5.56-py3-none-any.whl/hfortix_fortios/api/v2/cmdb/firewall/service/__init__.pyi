"""Type stubs for SERVICE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .category import Category, CategoryDictMode, CategoryObjectMode
    from .custom import Custom, CustomDictMode, CustomObjectMode
    from .group import Group, GroupDictMode, GroupObjectMode

__all__ = [
    "Category",
    "Custom",
    "Group",
    "ServiceDictMode",
    "ServiceObjectMode",
]

class ServiceDictMode:
    """SERVICE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    category: CategoryDictMode
    custom: CustomDictMode
    group: GroupDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize service category with HTTP client."""
        ...


class ServiceObjectMode:
    """SERVICE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    category: CategoryObjectMode
    custom: CustomObjectMode
    group: GroupObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize service category with HTTP client."""
        ...


# Base class for backwards compatibility
class Service:
    """SERVICE API category."""
    
    category: Category
    custom: Custom
    group: Group

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize service category with HTTP client."""
        ...
