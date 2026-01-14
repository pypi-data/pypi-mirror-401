"""Type stubs for INITIAL_CONFIG category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .template import Template, TemplateDictMode, TemplateObjectMode
    from .vlans import Vlans, VlansDictMode, VlansObjectMode

__all__ = [
    "Template",
    "Vlans",
    "InitialConfigDictMode",
    "InitialConfigObjectMode",
]

class InitialConfigDictMode:
    """INITIAL_CONFIG API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    template: TemplateDictMode
    vlans: VlansDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize initial_config category with HTTP client."""
        ...


class InitialConfigObjectMode:
    """INITIAL_CONFIG API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    template: TemplateObjectMode
    vlans: VlansObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize initial_config category with HTTP client."""
        ...


# Base class for backwards compatibility
class InitialConfig:
    """INITIAL_CONFIG API category."""
    
    template: Template
    vlans: Vlans

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize initial_config category with HTTP client."""
        ...
