"""Type stubs for WAF category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .main_class import MainClass, MainClassDictMode, MainClassObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .signature import Signature, SignatureDictMode, SignatureObjectMode

__all__ = [
    "MainClass",
    "Profile",
    "Signature",
    "WafDictMode",
    "WafObjectMode",
]

class WafDictMode:
    """WAF API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    main_class: MainClassDictMode
    profile: ProfileDictMode
    signature: SignatureDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize waf category with HTTP client."""
        ...


class WafObjectMode:
    """WAF API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    main_class: MainClassObjectMode
    profile: ProfileObjectMode
    signature: SignatureObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize waf category with HTTP client."""
        ...


# Base class for backwards compatibility
class Waf:
    """WAF API category."""
    
    main_class: MainClass
    profile: Profile
    signature: Signature

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize waf category with HTTP client."""
        ...
