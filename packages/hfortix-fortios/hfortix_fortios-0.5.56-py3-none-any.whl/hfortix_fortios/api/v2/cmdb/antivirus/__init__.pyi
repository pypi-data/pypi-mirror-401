"""Type stubs for ANTIVIRUS category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .exempt_list import ExemptList, ExemptListDictMode, ExemptListObjectMode
    from .profile import Profile, ProfileDictMode, ProfileObjectMode
    from .quarantine import Quarantine, QuarantineDictMode, QuarantineObjectMode
    from .settings import Settings, SettingsDictMode, SettingsObjectMode

__all__ = [
    "ExemptList",
    "Profile",
    "Quarantine",
    "Settings",
    "AntivirusDictMode",
    "AntivirusObjectMode",
]

class AntivirusDictMode:
    """ANTIVIRUS API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    exempt_list: ExemptListDictMode
    profile: ProfileDictMode
    quarantine: QuarantineDictMode
    settings: SettingsDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize antivirus category with HTTP client."""
        ...


class AntivirusObjectMode:
    """ANTIVIRUS API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    exempt_list: ExemptListObjectMode
    profile: ProfileObjectMode
    quarantine: QuarantineObjectMode
    settings: SettingsObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize antivirus category with HTTP client."""
        ...


# Base class for backwards compatibility
class Antivirus:
    """ANTIVIRUS API category."""
    
    exempt_list: ExemptList
    profile: Profile
    quarantine: Quarantine
    settings: Settings

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize antivirus category with HTTP client."""
        ...
