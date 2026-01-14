"""Type stubs for SSID category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .generate_keys import GenerateKeys, GenerateKeysDictMode, GenerateKeysObjectMode

__all__ = [
    "GenerateKeys",
    "SsidDictMode",
    "SsidObjectMode",
]

class SsidDictMode:
    """SSID API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    generate_keys: GenerateKeysDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ssid category with HTTP client."""
        ...


class SsidObjectMode:
    """SSID API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    generate_keys: GenerateKeysObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ssid category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ssid:
    """SSID API category."""
    
    generate_keys: GenerateKeys

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ssid category with HTTP client."""
        ...
