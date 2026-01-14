from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SwitchInterfacePayload(TypedDict, total=False):
    """
    Type hints for system/switch_interface payload fields.
    
    Configure software switch interfaces by grouping physical and WiFi interfaces.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: span-dest-port)
        - :class:`~.system.vdom.VdomEndpoint` (via: vdom)

    **Usage:**
        payload: SwitchInterfacePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Interface name | MaxLen: 15
    vdom: str  # VDOM that the software switch belongs to. | MaxLen: 31
    span_dest_port: str  # SPAN destination port name. All traffic on the SPA | MaxLen: 15
    span_source_port: list[dict[str, Any]]  # Physical interface name. Port spanning echoes all
    member: list[dict[str, Any]]  # Names of the interfaces that belong to the virtual
    type: Literal["switch", "hub"]  # Type of switch based on functionality: switch for | Default: switch
    intra_switch_policy: Literal["implicit", "explicit"]  # Allow any traffic between switch interfaces or req | Default: implicit
    mac_ttl: int  # Duration for which MAC addresses are held in the A | Default: 300 | Min: 300 | Max: 8640000
    span: Literal["disable", "enable"]  # Enable/disable port spanning. Port spanning echoes | Default: disable
    span_direction: Literal["rx", "tx", "both"]  # The direction in which the SPAN port operates, eit | Default: both

# Nested TypedDicts for table field children (dict mode)

class SwitchInterfaceSpansourceportItem(TypedDict):
    """Type hints for span-source-port table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    interface_name: str  # Physical interface name. | MaxLen: 79


class SwitchInterfaceMemberItem(TypedDict):
    """Type hints for member table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    interface_name: str  # Interface name. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class SwitchInterfaceSpansourceportObject:
    """Typed object for span-source-port table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Physical interface name. | MaxLen: 79
    interface_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class SwitchInterfaceMemberObject:
    """Typed object for member table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Interface name. | MaxLen: 79
    interface_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class SwitchInterfaceResponse(TypedDict):
    """
    Type hints for system/switch_interface API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Interface name | MaxLen: 15
    vdom: str  # VDOM that the software switch belongs to. | MaxLen: 31
    span_dest_port: str  # SPAN destination port name. All traffic on the SPA | MaxLen: 15
    span_source_port: list[SwitchInterfaceSpansourceportItem]  # Physical interface name. Port spanning echoes all
    member: list[SwitchInterfaceMemberItem]  # Names of the interfaces that belong to the virtual
    type: Literal["switch", "hub"]  # Type of switch based on functionality: switch for | Default: switch
    intra_switch_policy: Literal["implicit", "explicit"]  # Allow any traffic between switch interfaces or req | Default: implicit
    mac_ttl: int  # Duration for which MAC addresses are held in the A | Default: 300 | Min: 300 | Max: 8640000
    span: Literal["disable", "enable"]  # Enable/disable port spanning. Port spanning echoes | Default: disable
    span_direction: Literal["rx", "tx", "both"]  # The direction in which the SPAN port operates, eit | Default: both


@final
class SwitchInterfaceObject:
    """Typed FortiObject for system/switch_interface with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Interface name | MaxLen: 15
    name: str
    # VDOM that the software switch belongs to. | MaxLen: 31
    vdom: str
    # SPAN destination port name. All traffic on the SPAN source p | MaxLen: 15
    span_dest_port: str
    # Physical interface name. Port spanning echoes all traffic on
    span_source_port: list[SwitchInterfaceSpansourceportObject]
    # Names of the interfaces that belong to the virtual switch.
    member: list[SwitchInterfaceMemberObject]
    # Type of switch based on functionality: switch for normal fun | Default: switch
    type: Literal["switch", "hub"]
    # Allow any traffic between switch interfaces or require firew | Default: implicit
    intra_switch_policy: Literal["implicit", "explicit"]
    # Duration for which MAC addresses are held in the ARP table | Default: 300 | Min: 300 | Max: 8640000
    mac_ttl: int
    # Enable/disable port spanning. Port spanning echoes traffic r | Default: disable
    span: Literal["disable", "enable"]
    # The direction in which the SPAN port operates, either: rx, t | Default: both
    span_direction: Literal["rx", "tx", "both"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SwitchInterfacePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class SwitchInterface:
    """
    Configure software switch interfaces by grouping physical and WiFi interfaces.
    
    Path: system/switch_interface
    Category: cmdb
    Primary Key: name
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
    ) -> SwitchInterfaceResponse: ...
    
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
    ) -> SwitchInterfaceResponse: ...
    
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
    ) -> list[SwitchInterfaceResponse]: ...
    
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
    ) -> SwitchInterfaceObject: ...
    
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
    ) -> SwitchInterfaceObject: ...
    
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
    ) -> list[SwitchInterfaceObject]: ...
    
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
    ) -> SwitchInterfaceResponse: ...
    
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
    ) -> SwitchInterfaceResponse: ...
    
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
    ) -> list[SwitchInterfaceResponse]: ...
    
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
    ) -> Union[dict[str, Any], list[dict[str, Any]], FortiObject, list[FortiObject]]: ...
    
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
    ) -> SwitchInterfaceObject | list[SwitchInterfaceObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
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

class SwitchInterfaceDictMode:
    """SwitchInterface endpoint for dict response mode (default for this client).
    
    By default returns SwitchInterfaceResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SwitchInterfaceObject.
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
    ) -> SwitchInterfaceObject: ...
    
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
    ) -> list[SwitchInterfaceObject]: ...
    
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
    ) -> SwitchInterfaceResponse: ...
    
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
    ) -> list[SwitchInterfaceResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        name: str,
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
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
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


class SwitchInterfaceObjectMode:
    """SwitchInterface endpoint for object response mode (default for this client).
    
    By default returns SwitchInterfaceObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SwitchInterfaceResponse (TypedDict).
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
    ) -> SwitchInterfaceResponse: ...
    
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
    ) -> list[SwitchInterfaceResponse]: ...
    
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
    ) -> SwitchInterfaceObject: ...
    
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
    ) -> list[SwitchInterfaceObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SwitchInterfaceObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        name: str,
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
        payload_dict: SwitchInterfacePayload | None = ...,
        name: str | None = ...,
        span_dest_port: str | None = ...,
        span_source_port: str | list[str] | list[dict[str, Any]] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        type: Literal["switch", "hub"] | None = ...,
        intra_switch_policy: Literal["implicit", "explicit"] | None = ...,
        mac_ttl: int | None = ...,
        span: Literal["disable", "enable"] | None = ...,
        span_direction: Literal["rx", "tx", "both"] | None = ...,
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
    "SwitchInterface",
    "SwitchInterfaceDictMode",
    "SwitchInterfaceObjectMode",
    "SwitchInterfacePayload",
    "SwitchInterfaceObject",
]