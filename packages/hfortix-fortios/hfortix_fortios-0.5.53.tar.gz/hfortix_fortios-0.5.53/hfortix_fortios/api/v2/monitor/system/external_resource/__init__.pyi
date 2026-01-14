"""Type stubs for EXTERNAL_RESOURCE category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .dynamic import Dynamic, DynamicDictMode, DynamicObjectMode
    from .entry_list import EntryList, EntryListDictMode, EntryListObjectMode
    from .generic_address import GenericAddress, GenericAddressDictMode, GenericAddressObjectMode
    from .refresh import Refresh, RefreshDictMode, RefreshObjectMode
    from .validate_jsonpath import ValidateJsonpath, ValidateJsonpathDictMode, ValidateJsonpathObjectMode

__all__ = [
    "Dynamic",
    "EntryList",
    "GenericAddress",
    "Refresh",
    "ValidateJsonpath",
    "ExternalResourceDictMode",
    "ExternalResourceObjectMode",
]

class ExternalResourceDictMode:
    """EXTERNAL_RESOURCE API category for dict response mode.
    
    This class is returned when the client is instantiated with response_mode="dict" (default).
    All endpoints return dict/TypedDict responses by default.
    """
    
    dynamic: DynamicDictMode
    entry_list: EntryListDictMode
    generic_address: GenericAddressDictMode
    refresh: RefreshDictMode
    validate_jsonpath: ValidateJsonpathDictMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize external_resource category with HTTP client."""
        ...


class ExternalResourceObjectMode:
    """EXTERNAL_RESOURCE API category for object response mode.
    
    This class is returned when the client is instantiated with response_mode="object".
    All endpoints return FortiObject responses by default.
    """
    
    dynamic: DynamicObjectMode
    entry_list: EntryListObjectMode
    generic_address: GenericAddressObjectMode
    refresh: RefreshObjectMode
    validate_jsonpath: ValidateJsonpathObjectMode

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize external_resource category with HTTP client."""
        ...


# Base class for backwards compatibility
class ExternalResource:
    """EXTERNAL_RESOURCE API category."""
    
    dynamic: Dynamic
    entry_list: EntryList
    generic_address: GenericAddress
    refresh: Refresh
    validate_jsonpath: ValidateJsonpath

    def __init__(self, client: IHTTPClient, vdom: str | None = None) -> None:
        """Initialize external_resource category with HTTP client."""
        ...
