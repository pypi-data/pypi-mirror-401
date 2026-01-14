"""Type stubs for SECURITY_POLICY category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .local_access import LocalAccess, LocalAccessDictMode, LocalAccessObjectMode
    from .x802_1x import X8021x, X8021xDictMode, X8021xObjectMode

__all__ = [
    "LocalAccess",
    "X8021x",
    "SecurityPolicyDictMode",
    "SecurityPolicyObjectMode",
]

class SecurityPolicyDictMode:
    """SECURITY_POLICY API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    local_access: LocalAccessDictMode
    x802_1x: X8021xDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_policy category with HTTP client."""
        ...


class SecurityPolicyObjectMode:
    """SECURITY_POLICY API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    local_access: LocalAccessObjectMode
    x802_1x: X8021xObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_policy category with HTTP client."""
        ...


# Base class for backwards compatibility
class SecurityPolicy:
    """SECURITY_POLICY API category."""
    
    local_access: LocalAccess
    x802_1x: X8021x

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_policy category with HTTP client."""
        ...
