"""Type stubs for AUTOMATION_STITCH category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .stats import Stats, StatsDictMode, StatsObjectMode
    from .test import Test, TestDictMode, TestObjectMode
    from .webhook import Webhook, WebhookDictMode, WebhookObjectMode

__all__ = [
    "Stats",
    "Test",
    "Webhook",
    "AutomationStitchDictMode",
    "AutomationStitchObjectMode",
]

class AutomationStitchDictMode:
    """AUTOMATION_STITCH API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    stats: StatsDictMode
    test: TestDictMode
    webhook: WebhookDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize automation_stitch category with HTTP client."""
        ...


class AutomationStitchObjectMode:
    """AUTOMATION_STITCH API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    stats: StatsObjectMode
    test: TestObjectMode
    webhook: WebhookObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize automation_stitch category with HTTP client."""
        ...


# Base class for backwards compatibility
class AutomationStitch:
    """AUTOMATION_STITCH API category."""
    
    stats: Stats
    test: Test
    webhook: Webhook

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize automation_stitch category with HTTP client."""
        ...
