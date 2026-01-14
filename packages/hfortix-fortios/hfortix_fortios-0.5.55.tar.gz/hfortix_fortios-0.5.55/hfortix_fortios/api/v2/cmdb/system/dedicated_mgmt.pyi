from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class DedicatedMgmtPayload(TypedDict, total=False):
    """
    Type hints for system/dedicated_mgmt payload fields.
    
    Configure dedicated management.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: interface)

    **Usage:**
        payload: DedicatedMgmtPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    status: Literal["enable", "disable"]  # Enable/disable dedicated management. | Default: disable
    interface: str  # Dedicated management interface. | MaxLen: 15
    default_gateway: str  # Default gateway for dedicated management interface | Default: 0.0.0.0
    dhcp_server: Literal["enable", "disable"]  # Enable/disable DHCP server on management interface | Default: disable
    dhcp_netmask: str  # DHCP netmask. | Default: 0.0.0.0
    dhcp_start_ip: str  # DHCP start IP for dedicated management. | Default: 0.0.0.0
    dhcp_end_ip: str  # DHCP end IP for dedicated management. | Default: 0.0.0.0

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class DedicatedMgmtResponse(TypedDict):
    """
    Type hints for system/dedicated_mgmt API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    status: Literal["enable", "disable"]  # Enable/disable dedicated management. | Default: disable
    interface: str  # Dedicated management interface. | MaxLen: 15
    default_gateway: str  # Default gateway for dedicated management interface | Default: 0.0.0.0
    dhcp_server: Literal["enable", "disable"]  # Enable/disable DHCP server on management interface | Default: disable
    dhcp_netmask: str  # DHCP netmask. | Default: 0.0.0.0
    dhcp_start_ip: str  # DHCP start IP for dedicated management. | Default: 0.0.0.0
    dhcp_end_ip: str  # DHCP end IP for dedicated management. | Default: 0.0.0.0


@final
class DedicatedMgmtObject:
    """Typed FortiObject for system/dedicated_mgmt with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Enable/disable dedicated management. | Default: disable
    status: Literal["enable", "disable"]
    # Dedicated management interface. | MaxLen: 15
    interface: str
    # Default gateway for dedicated management interface. | Default: 0.0.0.0
    default_gateway: str
    # Enable/disable DHCP server on management interface. | Default: disable
    dhcp_server: Literal["enable", "disable"]
    # DHCP netmask. | Default: 0.0.0.0
    dhcp_netmask: str
    # DHCP start IP for dedicated management. | Default: 0.0.0.0
    dhcp_start_ip: str
    # DHCP end IP for dedicated management. | Default: 0.0.0.0
    dhcp_end_ip: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> DedicatedMgmtPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class DedicatedMgmt:
    """
    Configure dedicated management.
    
    Path: system/dedicated_mgmt
    Category: cmdb
    """
    
    # ================================================================
    # DEFAULT MODE OVERLOADS (no response_mode) - MUST BE FIRST
    # These match when response_mode is NOT passed (client default is "dict")
    # Pylance matches overloads top-to-bottom, so these must come first!
    # ================================================================
    
    # Default mode: mkey as positional arg -> returns typed dict
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> DedicatedMgmtResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> DedicatedMgmtResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        name: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> DedicatedMgmtResponse: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # Object mode: no mkey -> returns list of objects
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        name: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Dict mode with mkey provided as positional arg (single dict)
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...
    
    # Dict mode - list of dicts (no mkey/name provided) - keyword-only signature
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        name: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> dict[str, Any] | FortiObject: ...
    
    def get(
        self,
        name: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: str | None = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> Union[list[str], list[dict[str, Any]]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> dict[str, Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> dict[str, Any]: ...
    
    @staticmethod
    def schema() -> dict[str, Any]: ...


# ================================================================
# MODE-SPECIFIC CLASSES FOR CLIENT-LEVEL response_mode SUPPORT
# ================================================================

class DedicatedMgmtDictMode:
    """DedicatedMgmt endpoint for dict response mode (default for this client).
    
    By default returns DedicatedMgmtResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return DedicatedMgmtObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        name: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Object mode override with mkey (single item)
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        name: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        name: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...


    # Helper methods (inherited from base class)
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> Union[list[str], list[dict[str, Any]]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> dict[str, Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> dict[str, Any]: ...
    
    @staticmethod
    def schema() -> dict[str, Any]: ...


class DedicatedMgmtObjectMode:
    """DedicatedMgmt endpoint for object response mode (default for this client).
    
    By default returns DedicatedMgmtObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return DedicatedMgmtResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        name: str | None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Dict mode override with mkey (single item)
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        name: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> DedicatedMgmtResponse: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        name: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["object"] | None = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        name: None = ...,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["object"] | None = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DedicatedMgmtObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...


    # Helper methods (inherited from base class)
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DedicatedMgmtPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        interface: str | None = ...,
        default_gateway: str | None = ...,
        dhcp_server: Literal["enable", "disable"] | None = ...,
        dhcp_netmask: str | None = ...,
        dhcp_start_ip: str | None = ...,
        dhcp_end_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> Union[list[str], list[dict[str, Any]]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> dict[str, Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> dict[str, Any]: ...
    
    @staticmethod
    def schema() -> dict[str, Any]: ...


__all__ = [
    "DedicatedMgmt",
    "DedicatedMgmtDictMode",
    "DedicatedMgmtObjectMode",
    "DedicatedMgmtPayload",
    "DedicatedMgmtObject",
]