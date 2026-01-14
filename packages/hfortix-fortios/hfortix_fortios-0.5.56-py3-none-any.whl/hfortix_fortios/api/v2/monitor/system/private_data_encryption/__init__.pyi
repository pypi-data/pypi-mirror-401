"""Type stubs for PRIVATE_DATA_ENCRYPTION category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .set import Set, SetDictMode, SetObjectMode

__all__ = [
    "Set",
    "PrivateDataEncryptionDictMode",
    "PrivateDataEncryptionObjectMode",
]

class PrivateDataEncryptionDictMode:
    """PRIVATE_DATA_ENCRYPTION API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    set: SetDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize private_data_encryption category with HTTP client."""
        ...


class PrivateDataEncryptionObjectMode:
    """PRIVATE_DATA_ENCRYPTION API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    set: SetObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize private_data_encryption category with HTTP client."""
        ...


# Base class for backwards compatibility
class PrivateDataEncryption:
    """PRIVATE_DATA_ENCRYPTION API category."""
    
    set: Set

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize private_data_encryption category with HTTP client."""
        ...
