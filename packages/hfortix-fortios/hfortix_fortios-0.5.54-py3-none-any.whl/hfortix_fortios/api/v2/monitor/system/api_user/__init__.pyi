"""Type stubs for API_USER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .generate_key import GenerateKey, GenerateKeyDictMode, GenerateKeyObjectMode

__all__ = [
    "GenerateKey",
    "ApiUserDictMode",
    "ApiUserObjectMode",
]

class ApiUserDictMode:
    """API_USER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    generate_key: GenerateKeyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize api_user category with HTTP client."""
        ...


class ApiUserObjectMode:
    """API_USER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    generate_key: GenerateKeyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize api_user category with HTTP client."""
        ...


# Base class for backwards compatibility
class ApiUser:
    """API_USER API category."""
    
    generate_key: GenerateKey

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize api_user category with HTTP client."""
        ...
