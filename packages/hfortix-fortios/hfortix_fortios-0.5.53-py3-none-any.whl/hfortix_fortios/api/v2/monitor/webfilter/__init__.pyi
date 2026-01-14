"""Type stubs for WEBFILTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .fortiguard_categories import FortiguardCategories, FortiguardCategoriesDictMode, FortiguardCategoriesObjectMode
    from .trusted_urls import TrustedUrls, TrustedUrlsDictMode, TrustedUrlsObjectMode
    from .category_quota import CategoryQuota
    from .malicious_urls import MaliciousUrls
    from .override import Override

__all__ = [
    "FortiguardCategories",
    "TrustedUrls",
    "WebfilterDictMode",
    "WebfilterObjectMode",
]

class WebfilterDictMode:
    """WEBFILTER API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    category_quota: CategoryQuota
    malicious_urls: MaliciousUrls
    override: Override
    fortiguard_categories: FortiguardCategoriesDictMode
    trusted_urls: TrustedUrlsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webfilter category with HTTP client."""
        ...


class WebfilterObjectMode:
    """WEBFILTER API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    category_quota: CategoryQuota
    malicious_urls: MaliciousUrls
    override: Override
    fortiguard_categories: FortiguardCategoriesObjectMode
    trusted_urls: TrustedUrlsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webfilter category with HTTP client."""
        ...


# Base class for backwards compatibility
class Webfilter:
    """WEBFILTER API category."""
    
    category_quota: CategoryQuota
    malicious_urls: MaliciousUrls
    override: Override
    fortiguard_categories: FortiguardCategories
    trusted_urls: TrustedUrls

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize webfilter category with HTTP client."""
        ...
