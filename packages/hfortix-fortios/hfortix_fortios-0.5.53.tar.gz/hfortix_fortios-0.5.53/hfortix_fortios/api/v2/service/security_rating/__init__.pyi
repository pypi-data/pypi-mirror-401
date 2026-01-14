"""Type stubs for SECURITY_RATING category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .recommendations import Recommendations, RecommendationsDictMode, RecommendationsObjectMode
    from .report import Report, ReportDictMode, ReportObjectMode

__all__ = [
    "Recommendations",
    "Report",
    "SecurityRatingDictMode",
    "SecurityRatingObjectMode",
]

class SecurityRatingDictMode:
    """SECURITY_RATING API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    recommendations: RecommendationsDictMode
    report: ReportDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_rating category with HTTP client."""
        ...


class SecurityRatingObjectMode:
    """SECURITY_RATING API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    recommendations: RecommendationsObjectMode
    report: ReportObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_rating category with HTTP client."""
        ...


# Base class for backwards compatibility
class SecurityRating:
    """SECURITY_RATING API category."""
    
    recommendations: Recommendations
    report: Report

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize security_rating category with HTTP client."""
        ...
