"""Type stubs for SERVICE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .ldap import LdapDictMode, LdapObjectMode

__all__ = [
    "ServiceDictMode",
    "ServiceObjectMode",
]

class ServiceDictMode:
    """SERVICE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    ldap: LdapDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize service category with HTTP client."""
        ...


class ServiceObjectMode:
    """SERVICE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    ldap: LdapObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize service category with HTTP client."""
        ...


# Base class for backwards compatibility
class Service:
    """SERVICE API category."""
    
    ldap: Ldap

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize service category with HTTP client."""
        ...
