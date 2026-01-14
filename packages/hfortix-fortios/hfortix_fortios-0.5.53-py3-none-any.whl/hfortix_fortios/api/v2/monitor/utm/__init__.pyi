"""Type stubs for UTM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .app_lookup import AppLookup, AppLookupDictMode, AppLookupObjectMode
    from .application_categories import ApplicationCategories, ApplicationCategoriesDictMode, ApplicationCategoriesObjectMode
    from .antivirus import AntivirusDictMode, AntivirusObjectMode
    from .blacklisted_certificates import BlacklistedCertificates
    from .rating_lookup import RatingLookup

__all__ = [
    "AppLookup",
    "ApplicationCategories",
    "UtmDictMode",
    "UtmObjectMode",
]

class UtmDictMode:
    """UTM API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    antivirus: AntivirusDictMode
    blacklisted_certificates: BlacklistedCertificates
    rating_lookup: RatingLookup
    app_lookup: AppLookupDictMode
    application_categories: ApplicationCategoriesDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize utm category with HTTP client."""
        ...


class UtmObjectMode:
    """UTM API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    antivirus: AntivirusObjectMode
    blacklisted_certificates: BlacklistedCertificates
    rating_lookup: RatingLookup
    app_lookup: AppLookupObjectMode
    application_categories: ApplicationCategoriesObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize utm category with HTTP client."""
        ...


# Base class for backwards compatibility
class Utm:
    """UTM API category."""
    
    antivirus: Antivirus
    blacklisted_certificates: BlacklistedCertificates
    rating_lookup: RatingLookup
    app_lookup: AppLookup
    application_categories: ApplicationCategories

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize utm category with HTTP client."""
        ...
