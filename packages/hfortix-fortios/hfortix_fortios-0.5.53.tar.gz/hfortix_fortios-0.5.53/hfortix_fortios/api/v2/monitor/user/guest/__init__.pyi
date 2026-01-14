"""Type stubs for GUEST category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .email import Email, EmailDictMode, EmailObjectMode
    from .sms import Sms, SmsDictMode, SmsObjectMode

__all__ = [
    "Email",
    "Sms",
    "GuestDictMode",
    "GuestObjectMode",
]

class GuestDictMode:
    """GUEST API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    email: EmailDictMode
    sms: SmsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize guest category with HTTP client."""
        ...


class GuestObjectMode:
    """GUEST API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    email: EmailObjectMode
    sms: SmsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize guest category with HTTP client."""
        ...


# Base class for backwards compatibility
class Guest:
    """GUEST API category."""
    
    email: Email
    sms: Sms

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize guest category with HTTP client."""
        ...
