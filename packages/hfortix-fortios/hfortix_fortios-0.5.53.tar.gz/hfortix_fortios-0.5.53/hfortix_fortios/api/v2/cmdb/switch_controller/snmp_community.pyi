from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SnmpCommunityPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/snmp_community payload fields.
    
    Configure FortiSwitch SNMP v1/v2c communities globally.
    
    **Usage:**
        payload: SnmpCommunityPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    id: int  # SNMP community ID. | Default: 0 | Min: 0 | Max: 4294967295
    name: str  # SNMP community name. | MaxLen: 35
    status: Literal["disable", "enable"]  # Enable/disable this SNMP community. | Default: enable
    hosts: list[dict[str, Any]]  # Configure IPv4 SNMP managers (hosts).
    query_v1_status: Literal["disable", "enable"]  # Enable/disable SNMP v1 queries. | Default: enable
    query_v1_port: int  # SNMP v1 query port (default = 161). | Default: 161 | Min: 0 | Max: 65535
    query_v2c_status: Literal["disable", "enable"]  # Enable/disable SNMP v2c queries. | Default: enable
    query_v2c_port: int  # SNMP v2c query port (default = 161). | Default: 161 | Min: 0 | Max: 65535
    trap_v1_status: Literal["disable", "enable"]  # Enable/disable SNMP v1 traps. | Default: enable
    trap_v1_lport: int  # SNMP v2c trap local port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v1_rport: int  # SNMP v2c trap remote port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v2c_status: Literal["disable", "enable"]  # Enable/disable SNMP v2c traps. | Default: enable
    trap_v2c_lport: int  # SNMP v2c trap local port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v2c_rport: int  # SNMP v2c trap remote port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"]  # SNMP notifications (traps) to send. | Default: cpu-high mem-low log-full intf-ip ent-conf-change l2mac

# Nested TypedDicts for table field children (dict mode)

class SnmpCommunityHostsItem(TypedDict):
    """Type hints for hosts table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Host entry ID. | Default: 0 | Min: 0 | Max: 4294967295
    ip: str  # IPv4 address of the SNMP manager (host).


# Nested classes for table field children (object mode)

@final
class SnmpCommunityHostsObject:
    """Typed object for hosts table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Host entry ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # IPv4 address of the SNMP manager (host).
    ip: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class SnmpCommunityResponse(TypedDict):
    """
    Type hints for switch_controller/snmp_community API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    id: int  # SNMP community ID. | Default: 0 | Min: 0 | Max: 4294967295
    name: str  # SNMP community name. | MaxLen: 35
    status: Literal["disable", "enable"]  # Enable/disable this SNMP community. | Default: enable
    hosts: list[SnmpCommunityHostsItem]  # Configure IPv4 SNMP managers (hosts).
    query_v1_status: Literal["disable", "enable"]  # Enable/disable SNMP v1 queries. | Default: enable
    query_v1_port: int  # SNMP v1 query port (default = 161). | Default: 161 | Min: 0 | Max: 65535
    query_v2c_status: Literal["disable", "enable"]  # Enable/disable SNMP v2c queries. | Default: enable
    query_v2c_port: int  # SNMP v2c query port (default = 161). | Default: 161 | Min: 0 | Max: 65535
    trap_v1_status: Literal["disable", "enable"]  # Enable/disable SNMP v1 traps. | Default: enable
    trap_v1_lport: int  # SNMP v2c trap local port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v1_rport: int  # SNMP v2c trap remote port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v2c_status: Literal["disable", "enable"]  # Enable/disable SNMP v2c traps. | Default: enable
    trap_v2c_lport: int  # SNMP v2c trap local port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v2c_rport: int  # SNMP v2c trap remote port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"]  # SNMP notifications (traps) to send. | Default: cpu-high mem-low log-full intf-ip ent-conf-change l2mac


@final
class SnmpCommunityObject:
    """Typed FortiObject for switch_controller/snmp_community with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # SNMP community ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # SNMP community name. | MaxLen: 35
    name: str
    # Enable/disable this SNMP community. | Default: enable
    status: Literal["disable", "enable"]
    # Configure IPv4 SNMP managers (hosts).
    hosts: list[SnmpCommunityHostsObject]
    # Enable/disable SNMP v1 queries. | Default: enable
    query_v1_status: Literal["disable", "enable"]
    # SNMP v1 query port (default = 161). | Default: 161 | Min: 0 | Max: 65535
    query_v1_port: int
    # Enable/disable SNMP v2c queries. | Default: enable
    query_v2c_status: Literal["disable", "enable"]
    # SNMP v2c query port (default = 161). | Default: 161 | Min: 0 | Max: 65535
    query_v2c_port: int
    # Enable/disable SNMP v1 traps. | Default: enable
    trap_v1_status: Literal["disable", "enable"]
    # SNMP v2c trap local port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v1_lport: int
    # SNMP v2c trap remote port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v1_rport: int
    # Enable/disable SNMP v2c traps. | Default: enable
    trap_v2c_status: Literal["disable", "enable"]
    # SNMP v2c trap local port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v2c_lport: int
    # SNMP v2c trap remote port (default = 162). | Default: 162 | Min: 0 | Max: 65535
    trap_v2c_rport: int
    # SNMP notifications (traps) to send. | Default: cpu-high mem-low log-full intf-ip ent-conf-change l2mac
    events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SnmpCommunityPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class SnmpCommunity:
    """
    Configure FortiSwitch SNMP v1/v2c communities globally.
    
    Path: switch_controller/snmp_community
    Category: cmdb
    Primary Key: id
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
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> SnmpCommunityResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> SnmpCommunityResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        id: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[SnmpCommunityResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        id: int,
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
    ) -> SnmpCommunityObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        id: int,
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
    ) -> SnmpCommunityObject: ...
    
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
    ) -> list[SnmpCommunityObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> SnmpCommunityResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        id: int,
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
    ) -> SnmpCommunityResponse: ...
    
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
    ) -> list[SnmpCommunityResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int | None = ...,
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
    ) -> SnmpCommunityObject | list[SnmpCommunityObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
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

class SnmpCommunityDictMode:
    """SnmpCommunity endpoint for dict response mode (default for this client).
    
    By default returns SnmpCommunityResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SnmpCommunityObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> SnmpCommunityObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[SnmpCommunityObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
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
    ) -> SnmpCommunityResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[SnmpCommunityResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
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


class SnmpCommunityObjectMode:
    """SnmpCommunity endpoint for object response mode (default for this client).
    
    By default returns SnmpCommunityObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SnmpCommunityResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> SnmpCommunityResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[SnmpCommunityResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
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
    ) -> SnmpCommunityObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[SnmpCommunityObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SnmpCommunityObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SnmpCommunityPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        status: Literal["disable", "enable"] | None = ...,
        hosts: str | list[str] | list[dict[str, Any]] | None = ...,
        query_v1_status: Literal["disable", "enable"] | None = ...,
        query_v1_port: int | None = ...,
        query_v2c_status: Literal["disable", "enable"] | None = ...,
        query_v2c_port: int | None = ...,
        trap_v1_status: Literal["disable", "enable"] | None = ...,
        trap_v1_lport: int | None = ...,
        trap_v1_rport: int | None = ...,
        trap_v2c_status: Literal["disable", "enable"] | None = ...,
        trap_v2c_lport: int | None = ...,
        trap_v2c_rport: int | None = ...,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"] | list[str] | None = ...,
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
    "SnmpCommunity",
    "SnmpCommunityDictMode",
    "SnmpCommunityObjectMode",
    "SnmpCommunityPayload",
    "SnmpCommunityObject",
]