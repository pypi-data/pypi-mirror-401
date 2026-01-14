"""Type stubs for AUTHENTICATION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .rule import Rule, RuleDictMode, RuleObjectMode
    from .scheme import Scheme, SchemeDictMode, SchemeObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "Rule",
    "Scheme",
    "Setting",
    "AuthenticationDictMode",
    "AuthenticationObjectMode",
]

class AuthenticationDictMode:
    """AUTHENTICATION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    rule: RuleDictMode
    scheme: SchemeDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize authentication category with HTTP client."""
        ...


class AuthenticationObjectMode:
    """AUTHENTICATION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    rule: RuleObjectMode
    scheme: SchemeObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize authentication category with HTTP client."""
        ...


# Base class for backwards compatibility
class Authentication:
    """AUTHENTICATION API category."""
    
    rule: Rule
    scheme: Scheme
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize authentication category with HTTP client."""
        ...
