"""Type stubs for SCIM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .groups import Groups, GroupsDictMode, GroupsObjectMode
    from .users import Users, UsersDictMode, UsersObjectMode

__all__ = [
    "Groups",
    "Users",
    "ScimDictMode",
    "ScimObjectMode",
]

class ScimDictMode:
    """SCIM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    groups: GroupsDictMode
    users: UsersDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize scim category with HTTP client."""
        ...


class ScimObjectMode:
    """SCIM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    groups: GroupsObjectMode
    users: UsersObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize scim category with HTTP client."""
        ...


# Base class for backwards compatibility
class Scim:
    """SCIM API category."""
    
    groups: Groups
    users: Users

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize scim category with HTTP client."""
        ...
