"""Type stubs for FORTIGUARD category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .answers import Answers, AnswersDictMode, AnswersObjectMode
    from .redirect_portal import RedirectPortal, RedirectPortalDictMode, RedirectPortalObjectMode
    from .service_communication_stats import ServiceCommunicationStats, ServiceCommunicationStatsDictMode, ServiceCommunicationStatsObjectMode

__all__ = [
    "Answers",
    "RedirectPortal",
    "ServiceCommunicationStats",
    "FortiguardDictMode",
    "FortiguardObjectMode",
]

class FortiguardDictMode:
    """FORTIGUARD API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    answers: AnswersDictMode
    redirect_portal: RedirectPortalDictMode
    service_communication_stats: ServiceCommunicationStatsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


class FortiguardObjectMode:
    """FORTIGUARD API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    answers: AnswersObjectMode
    redirect_portal: RedirectPortalObjectMode
    service_communication_stats: ServiceCommunicationStatsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...


# Base class for backwards compatibility
class Fortiguard:
    """FORTIGUARD API category."""
    
    answers: Answers
    redirect_portal: RedirectPortal
    service_communication_stats: ServiceCommunicationStats

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize fortiguard category with HTTP client."""
        ...
