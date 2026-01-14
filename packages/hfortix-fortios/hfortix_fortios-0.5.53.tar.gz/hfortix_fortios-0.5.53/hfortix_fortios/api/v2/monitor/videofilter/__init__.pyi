"""Type stubs for VIDEOFILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fortiguard_categories import FortiguardCategories, FortiguardCategoriesDictMode, FortiguardCategoriesObjectMode

__all__ = [
    "FortiguardCategories",
    "VideofilterDictMode",
    "VideofilterObjectMode",
]

class VideofilterDictMode:
    """VIDEOFILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    fortiguard_categories: FortiguardCategoriesDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize videofilter category with HTTP client."""
        ...


class VideofilterObjectMode:
    """VIDEOFILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    fortiguard_categories: FortiguardCategoriesObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize videofilter category with HTTP client."""
        ...


# Base class for backwards compatibility
class Videofilter:
    """VIDEOFILTER API category."""
    
    fortiguard_categories: FortiguardCategories

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize videofilter category with HTTP client."""
        ...
