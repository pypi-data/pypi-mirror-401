"""Type stubs for LDAP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .query import Query, QueryDictMode, QueryObjectMode

__all__ = [
    "Query",
    "LdapDictMode",
    "LdapObjectMode",
]

class LdapDictMode:
    """LDAP API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    query: QueryDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ldap category with HTTP client."""
        ...


class LdapObjectMode:
    """LDAP API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    query: QueryObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ldap category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ldap:
    """LDAP API category."""
    
    query: Query

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ldap category with HTTP client."""
        ...
