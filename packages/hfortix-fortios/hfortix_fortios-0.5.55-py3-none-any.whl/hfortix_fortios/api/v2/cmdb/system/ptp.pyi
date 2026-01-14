from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class PtpPayload(TypedDict, total=False):
    """
    Type hints for system/ptp payload fields.
    
    Configure system PTP information.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: interface)

    **Usage:**
        payload: PtpPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    status: Literal["enable", "disable"]  # Enable/disable setting the FortiGate system time b | Default: disable
    mode: Literal["multicast", "hybrid"]  # Multicast transmission or hybrid transmission. | Default: multicast
    delay_mechanism: Literal["E2E", "P2P"]  # End to end delay detection or peer to peer delay d | Default: E2E
    request_interval: int  # The delay request value is the logarithmic mean in | Default: 1 | Min: 1 | Max: 6
    interface: str  # PTP client will reply through this interface. | MaxLen: 15
    server_mode: Literal["enable", "disable"]  # Enable/disable FortiGate PTP server mode. Your For | Default: disable
    server_interface: list[dict[str, Any]]  # FortiGate interface(s) with PTP server mode enable

# Nested TypedDicts for table field children (dict mode)

class PtpServerinterfaceItem(TypedDict):
    """Type hints for server-interface table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # ID. | Default: 0 | Min: 0 | Max: 4294967295
    server_interface_name: str  # Interface name. | MaxLen: 15
    delay_mechanism: Literal["E2E", "P2P"]  # End to end delay detection or peer to peer delay d | Default: E2E


# Nested classes for table field children (object mode)

@final
class PtpServerinterfaceObject:
    """Typed object for server-interface table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Interface name. | MaxLen: 15
    server_interface_name: str
    # End to end delay detection or peer to peer delay detection. | Default: E2E
    delay_mechanism: Literal["E2E", "P2P"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class PtpResponse(TypedDict):
    """
    Type hints for system/ptp API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    status: Literal["enable", "disable"]  # Enable/disable setting the FortiGate system time b | Default: disable
    mode: Literal["multicast", "hybrid"]  # Multicast transmission or hybrid transmission. | Default: multicast
    delay_mechanism: Literal["E2E", "P2P"]  # End to end delay detection or peer to peer delay d | Default: E2E
    request_interval: int  # The delay request value is the logarithmic mean in | Default: 1 | Min: 1 | Max: 6
    interface: str  # PTP client will reply through this interface. | MaxLen: 15
    server_mode: Literal["enable", "disable"]  # Enable/disable FortiGate PTP server mode. Your For | Default: disable
    server_interface: list[PtpServerinterfaceItem]  # FortiGate interface(s) with PTP server mode enable


@final
class PtpObject:
    """Typed FortiObject for system/ptp with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Enable/disable setting the FortiGate system time by synchron | Default: disable
    status: Literal["enable", "disable"]
    # Multicast transmission or hybrid transmission. | Default: multicast
    mode: Literal["multicast", "hybrid"]
    # End to end delay detection or peer to peer delay detection. | Default: E2E
    delay_mechanism: Literal["E2E", "P2P"]
    # The delay request value is the logarithmic mean interval in | Default: 1 | Min: 1 | Max: 6
    request_interval: int
    # PTP client will reply through this interface. | MaxLen: 15
    interface: str
    # Enable/disable FortiGate PTP server mode. Your FortiGate bec | Default: disable
    server_mode: Literal["enable", "disable"]
    # FortiGate interface(s) with PTP server mode enabled. Devices
    server_interface: list[PtpServerinterfaceObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> PtpPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Ptp:
    """
    Configure system PTP information.
    
    Path: system/ptp
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpObject: ...
    
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
    ) -> PtpObject: ...
    
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
    ) -> PtpObject: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PtpObject: ...
    
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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

class PtpDictMode:
    """Ptp endpoint for dict response mode (default for this client).
    
    By default returns PtpResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return PtpObject.
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
    ) -> PtpObject: ...
    
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
    ) -> PtpObject: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PtpObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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


class PtpObjectMode:
    """Ptp endpoint for object response mode (default for this client).
    
    By default returns PtpObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return PtpResponse (TypedDict).
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpResponse: ...
    
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
    ) -> PtpObject: ...
    
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
    ) -> PtpObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PtpObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PtpObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: PtpPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        mode: Literal["multicast", "hybrid"] | None = ...,
        delay_mechanism: Literal["E2E", "P2P"] | None = ...,
        request_interval: int | None = ...,
        interface: str | None = ...,
        server_mode: Literal["enable", "disable"] | None = ...,
        server_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "Ptp",
    "PtpDictMode",
    "PtpObjectMode",
    "PtpPayload",
    "PtpObject",
]