"""Type stubs for WEBFILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .content import Content, ContentDictMode, ContentObjectMode
    from .content_header import ContentHeader, ContentHeaderDictMode, ContentHeaderObjectMode
    from .fortiguard import Fortiguard, FortiguardDictMode, FortiguardObjectMode
    from .ftgd_local_cat import FtgdLocalCat, FtgdLocalCatDictMode, FtgdLocalCatObjectMode
    from .ftgd_local_rating import FtgdLocalRating, FtgdLocalRatingDictMode, FtgdLocalRatingObjectMode
    from .ftgd_local_risk import FtgdLocalRisk, FtgdLocalRiskDictMode, FtgdLocalRiskObjectMode
    from .ftgd_risk_level import FtgdRiskLevel, FtgdRiskLevelDictMode, FtgdRiskLevelObjectMode
    from .ips_urlfilter_cache_setting import IpsUrlfilterCacheSetting, IpsUrlfilterCacheSettingDictMode, IpsUrlfilterCacheSettingObjectMode
    from .ips_urlfilter_setting import IpsUrlfilterSetting, IpsUrlfilterSettingDictMode, IpsUrlfilterSettingObjectMode
    from .ips_urlfilter_setting6 import IpsUrlfilterSetting6, IpsUrlfilterSetting6DictMode, IpsUrlfilterSetting6ObjectMode
    from .override import Override, OverrideDictMode, OverrideObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .search_engine import SearchEngine, SearchEngineDictMode, SearchEngineObjectMode
    from .urlfilter import Urlfilter, UrlfilterDictMode, UrlfilterObjectMode

__all__ = [
    "Content",
    "ContentHeader",
    "Fortiguard",
    "FtgdLocalCat",
    "FtgdLocalRating",
    "FtgdLocalRisk",
    "FtgdRiskLevel",
    "IpsUrlfilterCacheSetting",
    "IpsUrlfilterSetting",
    "IpsUrlfilterSetting6",
    "Override",
    "Profile",
    "SearchEngine",
    "Urlfilter",
    "WebfilterDictMode",
    "WebfilterObjectMode",
]

class WebfilterDictMode:
    """WEBFILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    content: ContentDictMode
    content_header: ContentHeaderDictMode
    fortiguard: FortiguardDictMode
    ftgd_local_cat: FtgdLocalCatDictMode
    ftgd_local_rating: FtgdLocalRatingDictMode
    ftgd_local_risk: FtgdLocalRiskDictMode
    ftgd_risk_level: FtgdRiskLevelDictMode
    ips_urlfilter_cache_setting: IpsUrlfilterCacheSettingDictMode
    ips_urlfilter_setting: IpsUrlfilterSettingDictMode
    ips_urlfilter_setting6: IpsUrlfilterSetting6DictMode
    override: OverrideDictMode
    profile: ProfileDictMode
    search_engine: SearchEngineDictMode
    urlfilter: UrlfilterDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webfilter category with HTTP client."""
        ...


class WebfilterObjectMode:
    """WEBFILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    content: ContentObjectMode
    content_header: ContentHeaderObjectMode
    fortiguard: FortiguardObjectMode
    ftgd_local_cat: FtgdLocalCatObjectMode
    ftgd_local_rating: FtgdLocalRatingObjectMode
    ftgd_local_risk: FtgdLocalRiskObjectMode
    ftgd_risk_level: FtgdRiskLevelObjectMode
    ips_urlfilter_cache_setting: IpsUrlfilterCacheSettingObjectMode
    ips_urlfilter_setting: IpsUrlfilterSettingObjectMode
    ips_urlfilter_setting6: IpsUrlfilterSetting6ObjectMode
    override: OverrideObjectMode
    profile: ProfileObjectMode
    search_engine: SearchEngineObjectMode
    urlfilter: UrlfilterObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webfilter category with HTTP client."""
        ...


# Base class for backwards compatibility
class Webfilter:
    """WEBFILTER API category."""
    
    content: Content
    content_header: ContentHeader
    fortiguard: Fortiguard
    ftgd_local_cat: FtgdLocalCat
    ftgd_local_rating: FtgdLocalRating
    ftgd_local_risk: FtgdLocalRisk
    ftgd_risk_level: FtgdRiskLevel
    ips_urlfilter_cache_setting: IpsUrlfilterCacheSetting
    ips_urlfilter_setting: IpsUrlfilterSetting
    ips_urlfilter_setting6: IpsUrlfilterSetting6
    override: Override
    profile: Profile
    search_engine: SearchEngine
    urlfilter: Urlfilter

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webfilter category with HTTP client."""
        ...
