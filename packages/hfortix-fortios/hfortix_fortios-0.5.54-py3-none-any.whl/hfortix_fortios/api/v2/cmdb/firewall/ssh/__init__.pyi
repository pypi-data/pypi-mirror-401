"""Type stubs for SSH category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .host_key import HostKey, HostKeyDictMode, HostKeyObjectMode
    from .local_ca import LocalCa, LocalCaDictMode, LocalCaObjectMode
    from .local_key import LocalKey, LocalKeyDictMode, LocalKeyObjectMode
    from .setting import Setting, SettingDictMode, SettingObjectMode

__all__ = [
    "HostKey",
    "LocalCa",
    "LocalKey",
    "Setting",
    "SshDictMode",
    "SshObjectMode",
]

class SshDictMode:
    """SSH API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    host_key: HostKeyDictMode
    local_ca: LocalCaDictMode
    local_key: LocalKeyDictMode
    setting: SettingDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ssh category with HTTP client."""
        ...


class SshObjectMode:
    """SSH API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    host_key: HostKeyObjectMode
    local_ca: LocalCaObjectMode
    local_key: LocalKeyObjectMode
    setting: SettingObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ssh category with HTTP client."""
        ...


# Base class for backwards compatibility
class Ssh:
    """SSH API category."""
    
    host_key: HostKey
    local_ca: LocalCa
    local_key: LocalKey
    setting: Setting

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize ssh category with HTTP client."""
        ...
