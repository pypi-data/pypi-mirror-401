from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SdnVpnPayload(TypedDict, total=False):
    """
    Type hints for system/sdn_vpn payload fields.
    
    Configure public cloud VPN service.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: internal-interface, tunnel-interface)
        - :class:`~.system.sdn-connector.SdnConnectorEndpoint` (via: sdn)

    **Usage:**
        payload: SdnVpnPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Public cloud VPN name. | MaxLen: 35
    sdn: str  # SDN connector name. | MaxLen: 35
    remote_type: Literal["vgw", "tgw"]  # Type of remote device. | Default: vgw
    routing_type: Literal["static", "dynamic"]  # Type of routing. | Default: dynamic
    vgw_id: str  # Virtual private gateway id. | MaxLen: 63
    tgw_id: str  # Transit gateway id. | MaxLen: 63
    subnet_id: str  # AWS subnet id for TGW route propagation. | MaxLen: 63
    bgp_as: int  # BGP Router AS number. | Default: 65000 | Min: 1 | Max: 4294967295
    cgw_gateway: str  # Public IP address of the customer gateway. | Default: 0.0.0.0
    nat_traversal: Literal["disable", "enable"]  # Enable/disable use for NAT traversal. Please enabl | Default: enable
    tunnel_interface: str  # Tunnel interface with public IP. | MaxLen: 15
    internal_interface: str  # Internal interface with local subnet. | MaxLen: 15
    local_cidr: str  # Local subnet address and subnet mask. | Default: 0.0.0.0 0.0.0.0
    remote_cidr: str  # Remote subnet address and subnet mask. | Default: 0.0.0.0 0.0.0.0
    cgw_name: str  # AWS customer gateway name to be created. | MaxLen: 35
    psksecret: str  # Pre-shared secret for PSK authentication. Auto-gen
    type: int  # SDN VPN type. | Default: 0 | Min: 0 | Max: 65535
    status: int  # SDN VPN status. | Default: 0 | Min: 0 | Max: 255
    code: int  # SDN VPN error code. | Default: 0 | Min: 0 | Max: 255

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class SdnVpnResponse(TypedDict):
    """
    Type hints for system/sdn_vpn API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Public cloud VPN name. | MaxLen: 35
    sdn: str  # SDN connector name. | MaxLen: 35
    remote_type: Literal["vgw", "tgw"]  # Type of remote device. | Default: vgw
    routing_type: Literal["static", "dynamic"]  # Type of routing. | Default: dynamic
    vgw_id: str  # Virtual private gateway id. | MaxLen: 63
    tgw_id: str  # Transit gateway id. | MaxLen: 63
    subnet_id: str  # AWS subnet id for TGW route propagation. | MaxLen: 63
    bgp_as: int  # BGP Router AS number. | Default: 65000 | Min: 1 | Max: 4294967295
    cgw_gateway: str  # Public IP address of the customer gateway. | Default: 0.0.0.0
    nat_traversal: Literal["disable", "enable"]  # Enable/disable use for NAT traversal. Please enabl | Default: enable
    tunnel_interface: str  # Tunnel interface with public IP. | MaxLen: 15
    internal_interface: str  # Internal interface with local subnet. | MaxLen: 15
    local_cidr: str  # Local subnet address and subnet mask. | Default: 0.0.0.0 0.0.0.0
    remote_cidr: str  # Remote subnet address and subnet mask. | Default: 0.0.0.0 0.0.0.0
    cgw_name: str  # AWS customer gateway name to be created. | MaxLen: 35
    psksecret: str  # Pre-shared secret for PSK authentication. Auto-gen
    type: int  # SDN VPN type. | Default: 0 | Min: 0 | Max: 65535
    status: int  # SDN VPN status. | Default: 0 | Min: 0 | Max: 255
    code: int  # SDN VPN error code. | Default: 0 | Min: 0 | Max: 255


@final
class SdnVpnObject:
    """Typed FortiObject for system/sdn_vpn with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Public cloud VPN name. | MaxLen: 35
    name: str
    # SDN connector name. | MaxLen: 35
    sdn: str
    # Type of remote device. | Default: vgw
    remote_type: Literal["vgw", "tgw"]
    # Type of routing. | Default: dynamic
    routing_type: Literal["static", "dynamic"]
    # Virtual private gateway id. | MaxLen: 63
    vgw_id: str
    # Transit gateway id. | MaxLen: 63
    tgw_id: str
    # AWS subnet id for TGW route propagation. | MaxLen: 63
    subnet_id: str
    # BGP Router AS number. | Default: 65000 | Min: 1 | Max: 4294967295
    bgp_as: int
    # Public IP address of the customer gateway. | Default: 0.0.0.0
    cgw_gateway: str
    # Enable/disable use for NAT traversal. Please enable if your | Default: enable
    nat_traversal: Literal["disable", "enable"]
    # Tunnel interface with public IP. | MaxLen: 15
    tunnel_interface: str
    # Internal interface with local subnet. | MaxLen: 15
    internal_interface: str
    # Local subnet address and subnet mask. | Default: 0.0.0.0 0.0.0.0
    local_cidr: str
    # Remote subnet address and subnet mask. | Default: 0.0.0.0 0.0.0.0
    remote_cidr: str
    # AWS customer gateway name to be created. | MaxLen: 35
    cgw_name: str
    # Pre-shared secret for PSK authentication. Auto-generated if
    psksecret: str
    # SDN VPN type. | Default: 0 | Min: 0 | Max: 65535
    type: int
    # SDN VPN status. | Default: 0 | Min: 0 | Max: 255
    status: int
    # SDN VPN error code. | Default: 0 | Min: 0 | Max: 255
    code: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SdnVpnPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class SdnVpn:
    """
    Configure public cloud VPN service.
    
    Path: system/sdn_vpn
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
    ) -> SdnVpnResponse: ...
    
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
    ) -> SdnVpnResponse: ...
    
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
    ) -> list[SdnVpnResponse]: ...
    
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
    ) -> SdnVpnObject: ...
    
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
    ) -> SdnVpnObject: ...
    
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
    ) -> list[SdnVpnObject]: ...
    
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
    ) -> SdnVpnResponse: ...
    
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
    ) -> SdnVpnResponse: ...
    
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
    ) -> list[SdnVpnResponse]: ...
    
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
    ) -> SdnVpnObject | list[SdnVpnObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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
    ) -> SdnVpnObject: ...
    
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
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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

class SdnVpnDictMode:
    """SdnVpn endpoint for dict response mode (default for this client).
    
    By default returns SdnVpnResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SdnVpnObject.
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
    ) -> SdnVpnObject: ...
    
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
    ) -> list[SdnVpnObject]: ...
    
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
    ) -> SdnVpnResponse: ...
    
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
    ) -> list[SdnVpnResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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
    ) -> SdnVpnObject: ...
    
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
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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


class SdnVpnObjectMode:
    """SdnVpn endpoint for object response mode (default for this client).
    
    By default returns SdnVpnObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SdnVpnResponse (TypedDict).
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
    ) -> SdnVpnResponse: ...
    
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
    ) -> list[SdnVpnResponse]: ...
    
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
    ) -> SdnVpnObject: ...
    
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
    ) -> list[SdnVpnObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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
    ) -> SdnVpnObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SdnVpnObject: ...
    
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
        payload_dict: SdnVpnPayload | None = ...,
        name: str | None = ...,
        sdn: str | None = ...,
        remote_type: Literal["vgw", "tgw"] | None = ...,
        routing_type: Literal["static", "dynamic"] | None = ...,
        vgw_id: str | None = ...,
        tgw_id: str | None = ...,
        subnet_id: str | None = ...,
        bgp_as: int | None = ...,
        cgw_gateway: str | None = ...,
        nat_traversal: Literal["disable", "enable"] | None = ...,
        tunnel_interface: str | None = ...,
        internal_interface: str | None = ...,
        local_cidr: str | None = ...,
        remote_cidr: str | None = ...,
        cgw_name: str | None = ...,
        psksecret: str | None = ...,
        type: int | None = ...,
        status: int | None = ...,
        code: int | None = ...,
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
    "SdnVpn",
    "SdnVpnDictMode",
    "SdnVpnObjectMode",
    "SdnVpnPayload",
    "SdnVpnObject",
]