"""Type stubs for SDN_CONNECTOR category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .nsx_security_tags import NsxSecurityTags, NsxSecurityTagsDictMode, NsxSecurityTagsObjectMode
    from .status import Status, StatusDictMode, StatusObjectMode
    from .update import Update, UpdateDictMode, UpdateObjectMode
    from .validate_gcp_key import ValidateGcpKey, ValidateGcpKeyDictMode, ValidateGcpKeyObjectMode

__all__ = [
    "NsxSecurityTags",
    "Status",
    "Update",
    "ValidateGcpKey",
    "SdnConnectorDictMode",
    "SdnConnectorObjectMode",
]

class SdnConnectorDictMode:
    """SDN_CONNECTOR API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    nsx_security_tags: NsxSecurityTagsDictMode
    status: StatusDictMode
    update: UpdateDictMode
    validate_gcp_key: ValidateGcpKeyDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdn_connector category with HTTP client."""
        ...


class SdnConnectorObjectMode:
    """SDN_CONNECTOR API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    nsx_security_tags: NsxSecurityTagsObjectMode
    status: StatusObjectMode
    update: UpdateObjectMode
    validate_gcp_key: ValidateGcpKeyObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdn_connector category with HTTP client."""
        ...


# Base class for backwards compatibility
class SdnConnector:
    """SDN_CONNECTOR API category."""
    
    nsx_security_tags: NsxSecurityTags
    status: Status
    update: Update
    validate_gcp_key: ValidateGcpKey

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize sdn_connector category with HTTP client."""
        ...
