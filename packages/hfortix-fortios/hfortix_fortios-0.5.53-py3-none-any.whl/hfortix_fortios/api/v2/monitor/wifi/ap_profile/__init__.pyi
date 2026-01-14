"""Type stubs for AP_PROFILE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .create_default import CreateDefault, CreateDefaultDictMode, CreateDefaultObjectMode

__all__ = [
    "CreateDefault",
    "ApProfileDictMode",
    "ApProfileObjectMode",
]

class ApProfileDictMode:
    """AP_PROFILE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    create_default: CreateDefaultDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ap_profile category with HTTP client."""
        ...


class ApProfileObjectMode:
    """AP_PROFILE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    create_default: CreateDefaultObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ap_profile category with HTTP client."""
        ...


# Base class for backwards compatibility
class ApProfile:
    """AP_PROFILE API category."""
    
    create_default: CreateDefault

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ap_profile category with HTTP client."""
        ...
