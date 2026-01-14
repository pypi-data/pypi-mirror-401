from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class TrafficSnifferPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/traffic_sniffer payload fields.
    
    Configure FortiSwitch RSPAN/ERSPAN traffic sniffing parameters.
    
    **Usage:**
        payload: TrafficSnifferPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    mode: Literal["erspan-auto", "rspan", "none"]  # Configure traffic sniffer mode. | Default: erspan-auto
    erspan_ip: str  # Configure ERSPAN collector IP address. | Default: 0.0.0.0
    target_mac: list[dict[str, Any]]  # Sniffer MACs to filter.
    target_ip: list[dict[str, Any]]  # Sniffer IPs to filter.
    target_port: list[dict[str, Any]]  # Sniffer ports to filter.

# Nested TypedDicts for table field children (dict mode)

class TrafficSnifferTargetmacItem(TypedDict):
    """Type hints for target-mac table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    mac: str  # Sniffer MAC. | Default: 00:00:00:00:00:00
    description: str  # Description for the sniffer MAC. | MaxLen: 63


class TrafficSnifferTargetipItem(TypedDict):
    """Type hints for target-ip table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    ip: str  # Sniffer IP. | Default: 0.0.0.0
    description: str  # Description for the sniffer IP. | MaxLen: 63


class TrafficSnifferTargetportItem(TypedDict):
    """Type hints for target-port table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    switch_id: str  # Managed-switch ID. | MaxLen: 35
    description: str  # Description for the sniffer port entry. | MaxLen: 63
    in_ports: str  # Configure source ingress port interfaces.
    out_ports: str  # Configure source egress port interfaces.


# Nested classes for table field children (object mode)

@final
class TrafficSnifferTargetmacObject:
    """Typed object for target-mac table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Sniffer MAC. | Default: 00:00:00:00:00:00
    mac: str
    # Description for the sniffer MAC. | MaxLen: 63
    description: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class TrafficSnifferTargetipObject:
    """Typed object for target-ip table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Sniffer IP. | Default: 0.0.0.0
    ip: str
    # Description for the sniffer IP. | MaxLen: 63
    description: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class TrafficSnifferTargetportObject:
    """Typed object for target-port table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Managed-switch ID. | MaxLen: 35
    switch_id: str
    # Description for the sniffer port entry. | MaxLen: 63
    description: str
    # Configure source ingress port interfaces.
    in_ports: str
    # Configure source egress port interfaces.
    out_ports: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class TrafficSnifferResponse(TypedDict):
    """
    Type hints for switch_controller/traffic_sniffer API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    mode: Literal["erspan-auto", "rspan", "none"]  # Configure traffic sniffer mode. | Default: erspan-auto
    erspan_ip: str  # Configure ERSPAN collector IP address. | Default: 0.0.0.0
    target_mac: list[TrafficSnifferTargetmacItem]  # Sniffer MACs to filter.
    target_ip: list[TrafficSnifferTargetipItem]  # Sniffer IPs to filter.
    target_port: list[TrafficSnifferTargetportItem]  # Sniffer ports to filter.


@final
class TrafficSnifferObject:
    """Typed FortiObject for switch_controller/traffic_sniffer with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Configure traffic sniffer mode. | Default: erspan-auto
    mode: Literal["erspan-auto", "rspan", "none"]
    # Configure ERSPAN collector IP address. | Default: 0.0.0.0
    erspan_ip: str
    # Sniffer MACs to filter.
    target_mac: list[TrafficSnifferTargetmacObject]
    # Sniffer IPs to filter.
    target_ip: list[TrafficSnifferTargetipObject]
    # Sniffer ports to filter.
    target_port: list[TrafficSnifferTargetportObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> TrafficSnifferPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class TrafficSniffer:
    """
    Configure FortiSwitch RSPAN/ERSPAN traffic sniffing parameters.
    
    Path: switch_controller/traffic_sniffer
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferObject: ...
    
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
    ) -> TrafficSnifferObject: ...
    
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
    ) -> TrafficSnifferObject: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficSnifferObject: ...
    
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
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

class TrafficSnifferDictMode:
    """TrafficSniffer endpoint for dict response mode (default for this client).
    
    By default returns TrafficSnifferResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return TrafficSnifferObject.
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
    ) -> TrafficSnifferObject: ...
    
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
    ) -> TrafficSnifferObject: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficSnifferObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
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


class TrafficSnifferObjectMode:
    """TrafficSniffer endpoint for object response mode (default for this client).
    
    By default returns TrafficSnifferObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return TrafficSnifferResponse (TypedDict).
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferResponse: ...
    
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
    ) -> TrafficSnifferObject: ...
    
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
    ) -> TrafficSnifferObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficSnifferObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficSnifferObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: TrafficSnifferPayload | None = ...,
        mode: Literal["erspan-auto", "rspan", "none"] | None = ...,
        erspan_ip: str | None = ...,
        target_mac: str | list[str] | list[dict[str, Any]] | None = ...,
        target_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        target_port: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "TrafficSniffer",
    "TrafficSnifferDictMode",
    "TrafficSnifferObjectMode",
    "TrafficSnifferPayload",
    "TrafficSnifferObject",
]