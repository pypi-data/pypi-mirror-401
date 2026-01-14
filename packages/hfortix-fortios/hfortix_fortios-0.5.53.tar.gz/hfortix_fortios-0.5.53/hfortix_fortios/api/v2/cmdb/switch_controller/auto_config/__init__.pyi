"""Type stubs for AUTO_CONFIG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .custom import Custom, CustomDictMode, CustomObjectMode
    from .default import Default, DefaultDictMode, DefaultObjectMode
    from .policy import Policy, PolicyDictMode, PolicyObjectMode

__all__ = [
    "Custom",
    "Default",
    "Policy",
    "AutoConfigDictMode",
    "AutoConfigObjectMode",
]

class AutoConfigDictMode:
    """AUTO_CONFIG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    custom: CustomDictMode
    default: DefaultDictMode
    policy: PolicyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize auto_config category with HTTP client."""
        ...


class AutoConfigObjectMode:
    """AUTO_CONFIG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    custom: CustomObjectMode
    default: DefaultObjectMode
    policy: PolicyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize auto_config category with HTTP client."""
        ...


# Base class for backwards compatibility
class AutoConfig:
    """AUTO_CONFIG API category."""
    
    custom: Custom
    default: Default
    policy: Policy

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize auto_config category with HTTP client."""
        ...
