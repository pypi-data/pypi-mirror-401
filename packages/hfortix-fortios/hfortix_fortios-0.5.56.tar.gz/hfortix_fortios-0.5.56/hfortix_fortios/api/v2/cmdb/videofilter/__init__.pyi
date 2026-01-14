"""Type stubs for VIDEOFILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .keyword import Keyword, KeywordDictMode, KeywordObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .youtube_key import YoutubeKey, YoutubeKeyDictMode, YoutubeKeyObjectMode

__all__ = [
    "Keyword",
    "Profile",
    "YoutubeKey",
    "VideofilterDictMode",
    "VideofilterObjectMode",
]

class VideofilterDictMode:
    """VIDEOFILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    keyword: KeywordDictMode
    profile: ProfileDictMode
    youtube_key: YoutubeKeyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize videofilter category with HTTP client."""
        ...


class VideofilterObjectMode:
    """VIDEOFILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    keyword: KeywordObjectMode
    profile: ProfileObjectMode
    youtube_key: YoutubeKeyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize videofilter category with HTTP client."""
        ...


# Base class for backwards compatibility
class Videofilter:
    """VIDEOFILTER API category."""
    
    keyword: Keyword
    profile: Profile
    youtube_key: YoutubeKey

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize videofilter category with HTTP client."""
        ...
