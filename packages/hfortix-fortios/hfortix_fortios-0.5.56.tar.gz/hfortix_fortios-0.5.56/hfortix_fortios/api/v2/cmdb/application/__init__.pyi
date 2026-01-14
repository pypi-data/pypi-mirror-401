"""Type stubs for APPLICATION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom import Custom, CustomDictMode, CustomObjectMode
    from .group import Group, GroupDictMode, GroupObjectMode
    from .list import List, ListDictMode, ListObjectMode
    from .name import Name, NameDictMode, NameObjectMode
    from .rule_settings import RuleSettings, RuleSettingsDictMode, RuleSettingsObjectMode

__all__ = [
    "Custom",
    "Group",
    "List",
    "Name",
    "RuleSettings",
    "ApplicationDictMode",
    "ApplicationObjectMode",
]

class ApplicationDictMode:
    """APPLICATION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    custom: CustomDictMode
    group: GroupDictMode
    list: ListDictMode
    name: NameDictMode
    rule_settings: RuleSettingsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize application category with HTTP client."""
        ...


class ApplicationObjectMode:
    """APPLICATION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    custom: CustomObjectMode
    group: GroupObjectMode
    list: ListObjectMode
    name: NameObjectMode
    rule_settings: RuleSettingsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize application category with HTTP client."""
        ...


# Base class for backwards compatibility
class Application:
    """APPLICATION API category."""
    
    custom: Custom
    group: Group
    list: List
    name: Name
    rule_settings: RuleSettings

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize application category with HTTP client."""
        ...
