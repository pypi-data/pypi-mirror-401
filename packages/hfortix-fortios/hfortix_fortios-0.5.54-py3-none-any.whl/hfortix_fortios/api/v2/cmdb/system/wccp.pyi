from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class WccpPayload(TypedDict, total=False):
    """
    Type hints for system/wccp payload fields.
    
    Configure WCCP.
    
    **Usage:**
        payload: WccpPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    service_id: str  # Service ID. | MaxLen: 3
    router_id: str  # IP address known to all cache engines. If all cach | Default: 0.0.0.0
    cache_id: str  # IP address known to all routers. If the addresses | Default: 0.0.0.0
    group_address: str  # IP multicast address used by the cache routers. Fo | Default: 0.0.0.0
    server_list: list[dict[str, Any]]  # IP addresses and netmasks for up to four cache ser
    router_list: list[dict[str, Any]]  # IP addresses of one or more WCCP routers.
    ports_defined: Literal["source", "destination"]  # Match method.
    server_type: Literal["forward", "proxy"]  # Cache server type. | Default: forward
    ports: list[dict[str, Any]]  # Service ports.
    authentication: Literal["enable", "disable"]  # Enable/disable MD5 authentication. | Default: disable
    password: str  # Password for MD5 authentication. | MaxLen: 128
    forward_method: Literal["GRE", "L2", "any"]  # Method used to forward traffic to the cache server | Default: GRE
    cache_engine_method: Literal["GRE", "L2"]  # Method used to forward traffic to the routers or t | Default: GRE
    service_type: Literal["auto", "standard", "dynamic"]  # WCCP service type used by the cache server for log | Default: auto
    primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"]  # Hash method. | Default: dst-ip
    priority: int  # Service priority. | Default: 0 | Min: 0 | Max: 255
    protocol: int  # Service protocol. | Default: 0 | Min: 0 | Max: 255
    assignment_weight: int  # Assignment of hash weight/ratio for the WCCP cache | Default: 0 | Min: 0 | Max: 255
    assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"]  # Assignment bucket format for the WCCP cache engine | Default: cisco-implementation
    return_method: Literal["GRE", "L2", "any"]  # Method used to decline a redirected packet and ret | Default: GRE
    assignment_method: Literal["HASH", "MASK", "any"]  # Hash key assignment preference. | Default: HASH
    assignment_srcaddr_mask: str  # Assignment source address mask. | Default: 0.0.23.65
    assignment_dstaddr_mask: str  # Assignment destination address mask. | Default: 0.0.0.0

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class WccpResponse(TypedDict):
    """
    Type hints for system/wccp API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    service_id: str  # Service ID. | MaxLen: 3
    router_id: str  # IP address known to all cache engines. If all cach | Default: 0.0.0.0
    cache_id: str  # IP address known to all routers. If the addresses | Default: 0.0.0.0
    group_address: str  # IP multicast address used by the cache routers. Fo | Default: 0.0.0.0
    server_list: list[dict[str, Any]]  # IP addresses and netmasks for up to four cache ser
    router_list: list[dict[str, Any]]  # IP addresses of one or more WCCP routers.
    ports_defined: Literal["source", "destination"]  # Match method.
    server_type: Literal["forward", "proxy"]  # Cache server type. | Default: forward
    ports: list[dict[str, Any]]  # Service ports.
    authentication: Literal["enable", "disable"]  # Enable/disable MD5 authentication. | Default: disable
    password: str  # Password for MD5 authentication. | MaxLen: 128
    forward_method: Literal["GRE", "L2", "any"]  # Method used to forward traffic to the cache server | Default: GRE
    cache_engine_method: Literal["GRE", "L2"]  # Method used to forward traffic to the routers or t | Default: GRE
    service_type: Literal["auto", "standard", "dynamic"]  # WCCP service type used by the cache server for log | Default: auto
    primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"]  # Hash method. | Default: dst-ip
    priority: int  # Service priority. | Default: 0 | Min: 0 | Max: 255
    protocol: int  # Service protocol. | Default: 0 | Min: 0 | Max: 255
    assignment_weight: int  # Assignment of hash weight/ratio for the WCCP cache | Default: 0 | Min: 0 | Max: 255
    assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"]  # Assignment bucket format for the WCCP cache engine | Default: cisco-implementation
    return_method: Literal["GRE", "L2", "any"]  # Method used to decline a redirected packet and ret | Default: GRE
    assignment_method: Literal["HASH", "MASK", "any"]  # Hash key assignment preference. | Default: HASH
    assignment_srcaddr_mask: str  # Assignment source address mask. | Default: 0.0.23.65
    assignment_dstaddr_mask: str  # Assignment destination address mask. | Default: 0.0.0.0


@final
class WccpObject:
    """Typed FortiObject for system/wccp with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Service ID. | MaxLen: 3
    service_id: str
    # IP address known to all cache engines. If all cache engines | Default: 0.0.0.0
    router_id: str
    # IP address known to all routers. If the addresses are the sa | Default: 0.0.0.0
    cache_id: str
    # IP multicast address used by the cache routers. For the Fort | Default: 0.0.0.0
    group_address: str
    # IP addresses and netmasks for up to four cache servers.
    server_list: list[dict[str, Any]]
    # IP addresses of one or more WCCP routers.
    router_list: list[dict[str, Any]]
    # Match method.
    ports_defined: Literal["source", "destination"]
    # Cache server type. | Default: forward
    server_type: Literal["forward", "proxy"]
    # Service ports.
    ports: list[dict[str, Any]]
    # Enable/disable MD5 authentication. | Default: disable
    authentication: Literal["enable", "disable"]
    # Password for MD5 authentication. | MaxLen: 128
    password: str
    # Method used to forward traffic to the cache servers. | Default: GRE
    forward_method: Literal["GRE", "L2", "any"]
    # Method used to forward traffic to the routers or to return t | Default: GRE
    cache_engine_method: Literal["GRE", "L2"]
    # WCCP service type used by the cache server for logical inter | Default: auto
    service_type: Literal["auto", "standard", "dynamic"]
    # Hash method. | Default: dst-ip
    primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"]
    # Service priority. | Default: 0 | Min: 0 | Max: 255
    priority: int
    # Service protocol. | Default: 0 | Min: 0 | Max: 255
    protocol: int
    # Assignment of hash weight/ratio for the WCCP cache engine. | Default: 0 | Min: 0 | Max: 255
    assignment_weight: int
    # Assignment bucket format for the WCCP cache engine. | Default: cisco-implementation
    assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"]
    # Method used to decline a redirected packet and return it to | Default: GRE
    return_method: Literal["GRE", "L2", "any"]
    # Hash key assignment preference. | Default: HASH
    assignment_method: Literal["HASH", "MASK", "any"]
    # Assignment source address mask. | Default: 0.0.23.65
    assignment_srcaddr_mask: str
    # Assignment destination address mask. | Default: 0.0.0.0
    assignment_dstaddr_mask: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> WccpPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Wccp:
    """
    Configure WCCP.
    
    Path: system/wccp
    Category: cmdb
    Primary Key: service-id
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
        service_id: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> WccpResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        service_id: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> WccpResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        service_id: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[WccpResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        service_id: str,
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
    ) -> WccpObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        service_id: str,
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
    ) -> WccpObject: ...
    
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
    ) -> list[WccpObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        service_id: str | None = ...,
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
        service_id: str,
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
    ) -> WccpResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        service_id: str,
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
    ) -> WccpResponse: ...
    
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
    ) -> list[WccpResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        service_id: str | None = ...,
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
        service_id: str | None = ...,
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
    ) -> WccpObject | list[WccpObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        service_id: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    @overload
    def delete(
        self,
        service_id: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        service_id: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        service_id: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        service_id: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
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

class WccpDictMode:
    """Wccp endpoint for dict response mode (default for this client).
    
    By default returns WccpResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return WccpObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        service_id: str | None = ...,
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
        service_id: str,
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
    ) -> WccpObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        service_id: None = ...,
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
    ) -> list[WccpObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        service_id: str,
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
    ) -> WccpResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        service_id: None = ...,
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
    ) -> list[WccpResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
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


class WccpObjectMode:
    """Wccp endpoint for object response mode (default for this client).
    
    By default returns WccpObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return WccpResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        service_id: str | None = ...,
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
        service_id: str,
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
    ) -> WccpResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        service_id: None = ...,
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
    ) -> list[WccpResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        service_id: str,
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
    ) -> WccpObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        service_id: None = ...,
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
    ) -> list[WccpObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WccpObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        service_id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: WccpPayload | None = ...,
        service_id: str | None = ...,
        router_id: str | None = ...,
        cache_id: str | None = ...,
        group_address: str | None = ...,
        server_list: str | list[str] | None = ...,
        router_list: str | list[str] | None = ...,
        ports_defined: Literal["source", "destination"] | None = ...,
        server_type: Literal["forward", "proxy"] | None = ...,
        ports: str | list[str] | None = ...,
        authentication: Literal["enable", "disable"] | None = ...,
        password: str | None = ...,
        forward_method: Literal["GRE", "L2", "any"] | None = ...,
        cache_engine_method: Literal["GRE", "L2"] | None = ...,
        service_type: Literal["auto", "standard", "dynamic"] | None = ...,
        primary_hash: Literal["src-ip", "dst-ip", "src-port", "dst-port"] | list[str] | None = ...,
        priority: int | None = ...,
        protocol: int | None = ...,
        assignment_weight: int | None = ...,
        assignment_bucket_format: Literal["wccp-v2", "cisco-implementation"] | None = ...,
        return_method: Literal["GRE", "L2", "any"] | None = ...,
        assignment_method: Literal["HASH", "MASK", "any"] | None = ...,
        assignment_srcaddr_mask: str | None = ...,
        assignment_dstaddr_mask: str | None = ...,
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
    "Wccp",
    "WccpDictMode",
    "WccpObjectMode",
    "WccpPayload",
    "WccpObject",
]