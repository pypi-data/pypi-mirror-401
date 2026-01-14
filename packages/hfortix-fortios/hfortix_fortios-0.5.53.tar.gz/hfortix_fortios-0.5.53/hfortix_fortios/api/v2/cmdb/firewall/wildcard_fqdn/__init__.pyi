"""Type stubs for WILDCARD_FQDN category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom import Custom, CustomDictMode, CustomObjectMode
    from .group import Group, GroupDictMode, GroupObjectMode

__all__ = [
    "Custom",
    "Group",
    "WildcardFqdnDictMode",
    "WildcardFqdnObjectMode",
]

class WildcardFqdnDictMode:
    """WILDCARD_FQDN API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    custom: CustomDictMode
    group: GroupDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wildcard_fqdn category with HTTP client."""
        ...


class WildcardFqdnObjectMode:
    """WILDCARD_FQDN API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    custom: CustomObjectMode
    group: GroupObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wildcard_fqdn category with HTTP client."""
        ...


# Base class for backwards compatibility
class WildcardFqdn:
    """WILDCARD_FQDN API category."""
    
    custom: Custom
    group: Group

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize wildcard_fqdn category with HTTP client."""
        ...
