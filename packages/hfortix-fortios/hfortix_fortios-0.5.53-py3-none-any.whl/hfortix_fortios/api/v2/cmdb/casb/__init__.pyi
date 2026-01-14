"""Type stubs for CASB category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .attribute_match import AttributeMatch, AttributeMatchDictMode, AttributeMatchObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .saas_application import SaasApplication, SaasApplicationDictMode, SaasApplicationObjectMode
    from .user_activity import UserActivity, UserActivityDictMode, UserActivityObjectMode

__all__ = [
    "AttributeMatch",
    "Profile",
    "SaasApplication",
    "UserActivity",
    "CasbDictMode",
    "CasbObjectMode",
]

class CasbDictMode:
    """CASB API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    attribute_match: AttributeMatchDictMode
    profile: ProfileDictMode
    saas_application: SaasApplicationDictMode
    user_activity: UserActivityDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize casb category with HTTP client."""
        ...


class CasbObjectMode:
    """CASB API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    attribute_match: AttributeMatchObjectMode
    profile: ProfileObjectMode
    saas_application: SaasApplicationObjectMode
    user_activity: UserActivityObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize casb category with HTTP client."""
        ...


# Base class for backwards compatibility
class Casb:
    """CASB API category."""
    
    attribute_match: AttributeMatch
    profile: Profile
    saas_application: SaasApplication
    user_activity: UserActivity

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize casb category with HTTP client."""
        ...
