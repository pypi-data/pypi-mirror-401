"""Type stubs for RECOMMENDATION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .pse_config import PseConfig, PseConfigDictMode, PseConfigObjectMode

__all__ = [
    "PseConfig",
    "RecommendationDictMode",
    "RecommendationObjectMode",
]

class RecommendationDictMode:
    """RECOMMENDATION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    pse_config: PseConfigDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize recommendation category with HTTP client."""
        ...


class RecommendationObjectMode:
    """RECOMMENDATION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    pse_config: PseConfigObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize recommendation category with HTTP client."""
        ...


# Base class for backwards compatibility
class Recommendation:
    """RECOMMENDATION API category."""
    
    pse_config: PseConfig

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize recommendation category with HTTP client."""
        ...
