"""Type stubs for INFO category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .query import Query, QueryDictMode, QueryObjectMode
    from .thumbnail import Thumbnail, ThumbnailDictMode, ThumbnailObjectMode
    from .thumbnail_file import ThumbnailFile, ThumbnailFileDictMode, ThumbnailFileObjectMode

__all__ = [
    "Query",
    "Thumbnail",
    "ThumbnailFile",
    "InfoDictMode",
    "InfoObjectMode",
]

class InfoDictMode:
    """INFO API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    query: QueryDictMode
    thumbnail: ThumbnailDictMode
    thumbnail_file: ThumbnailFileDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize info category with HTTP client."""
        ...


class InfoObjectMode:
    """INFO API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    query: QueryObjectMode
    thumbnail: ThumbnailObjectMode
    thumbnail_file: ThumbnailFileObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize info category with HTTP client."""
        ...


# Base class for backwards compatibility
class Info:
    """INFO API category."""
    
    query: Query
    thumbnail: Thumbnail
    thumbnail_file: ThumbnailFile

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize info category with HTTP client."""
        ...
