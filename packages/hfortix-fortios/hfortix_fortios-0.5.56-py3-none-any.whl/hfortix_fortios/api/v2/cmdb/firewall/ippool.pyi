from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class IppoolPayload(TypedDict, total=False):
    """
    Type hints for firewall/ippool payload fields.
    
    Configure IPv4 IP pools.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: arp-intf, associated-interface)

    **Usage:**
        payload: IppoolPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # IP pool name. | MaxLen: 79
    type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]  # IP pool type: overload, one-to-one, fixed-port-ran | Default: overload
    startip: str  # First IPv4 address (inclusive) in the range for th | Default: 0.0.0.0
    endip: str  # Final IPv4 address (inclusive) in the range for th | Default: 0.0.0.0
    startport: int  # First port number (inclusive) in the range for the | Default: 5117 | Min: 1024 | Max: 65535
    endport: int  # Final port number (inclusive) in the range for the | Default: 65533 | Min: 1024 | Max: 65535
    source_startip: str  # First IPv4 address (inclusive) in the range of the | Default: 0.0.0.0
    source_endip: str  # Final IPv4 address (inclusive) in the range of the | Default: 0.0.0.0
    block_size: int  # Number of addresses in a block | Default: 128 | Min: 64 | Max: 4096
    port_per_user: int  # Number of port for each user | Default: 0 | Min: 32 | Max: 60417
    num_blocks_per_user: int  # Number of addresses blocks that can be used by a u | Default: 8 | Min: 1 | Max: 128
    pba_timeout: int  # Port block allocation timeout (seconds). | Default: 30 | Min: 3 | Max: 86400
    pba_interim_log: int  # Port block allocation interim logging interval | Default: 0 | Min: 600 | Max: 86400
    permit_any_host: Literal["disable", "enable"]  # Enable/disable fullcone NAT. Accept UDP packets fr | Default: disable
    arp_reply: Literal["disable", "enable"]  # Enable/disable replying to ARP requests when an IP | Default: enable
    arp_intf: str  # Select an interface from available options that wi | MaxLen: 15
    associated_interface: str  # Associated interface name. | MaxLen: 15
    comments: str  # Comment. | MaxLen: 255
    nat64: Literal["disable", "enable"]  # Enable/disable NAT64. | Default: disable
    add_nat64_route: Literal["disable", "enable"]  # Enable/disable adding NAT64 route. | Default: enable
    source_prefix6: str  # Source IPv6 network to be translated | Default: ::/0
    client_prefix_length: int  # Subnet length of a single deterministic NAT64 clie | Default: 64 | Min: 1 | Max: 128
    tcp_session_quota: int  # Maximum number of concurrent TCP sessions allowed | Default: 0 | Min: 0 | Max: 2097000
    udp_session_quota: int  # Maximum number of concurrent UDP sessions allowed | Default: 0 | Min: 0 | Max: 2097000
    icmp_session_quota: int  # Maximum number of concurrent ICMP sessions allowed | Default: 0 | Min: 0 | Max: 2097000
    privileged_port_use_pba: Literal["disable", "enable"]  # Enable/disable selection of the external port from | Default: disable
    subnet_broadcast_in_ippool: Literal["disable"]  # Enable/disable inclusion of the subnetwork address

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class IppoolResponse(TypedDict):
    """
    Type hints for firewall/ippool API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # IP pool name. | MaxLen: 79
    type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]  # IP pool type: overload, one-to-one, fixed-port-ran | Default: overload
    startip: str  # First IPv4 address (inclusive) in the range for th | Default: 0.0.0.0
    endip: str  # Final IPv4 address (inclusive) in the range for th | Default: 0.0.0.0
    startport: int  # First port number (inclusive) in the range for the | Default: 5117 | Min: 1024 | Max: 65535
    endport: int  # Final port number (inclusive) in the range for the | Default: 65533 | Min: 1024 | Max: 65535
    source_startip: str  # First IPv4 address (inclusive) in the range of the | Default: 0.0.0.0
    source_endip: str  # Final IPv4 address (inclusive) in the range of the | Default: 0.0.0.0
    block_size: int  # Number of addresses in a block | Default: 128 | Min: 64 | Max: 4096
    port_per_user: int  # Number of port for each user | Default: 0 | Min: 32 | Max: 60417
    num_blocks_per_user: int  # Number of addresses blocks that can be used by a u | Default: 8 | Min: 1 | Max: 128
    pba_timeout: int  # Port block allocation timeout (seconds). | Default: 30 | Min: 3 | Max: 86400
    pba_interim_log: int  # Port block allocation interim logging interval | Default: 0 | Min: 600 | Max: 86400
    permit_any_host: Literal["disable", "enable"]  # Enable/disable fullcone NAT. Accept UDP packets fr | Default: disable
    arp_reply: Literal["disable", "enable"]  # Enable/disable replying to ARP requests when an IP | Default: enable
    arp_intf: str  # Select an interface from available options that wi | MaxLen: 15
    associated_interface: str  # Associated interface name. | MaxLen: 15
    comments: str  # Comment. | MaxLen: 255
    nat64: Literal["disable", "enable"]  # Enable/disable NAT64. | Default: disable
    add_nat64_route: Literal["disable", "enable"]  # Enable/disable adding NAT64 route. | Default: enable
    source_prefix6: str  # Source IPv6 network to be translated | Default: ::/0
    client_prefix_length: int  # Subnet length of a single deterministic NAT64 clie | Default: 64 | Min: 1 | Max: 128
    tcp_session_quota: int  # Maximum number of concurrent TCP sessions allowed | Default: 0 | Min: 0 | Max: 2097000
    udp_session_quota: int  # Maximum number of concurrent UDP sessions allowed | Default: 0 | Min: 0 | Max: 2097000
    icmp_session_quota: int  # Maximum number of concurrent ICMP sessions allowed | Default: 0 | Min: 0 | Max: 2097000
    privileged_port_use_pba: Literal["disable", "enable"]  # Enable/disable selection of the external port from | Default: disable
    subnet_broadcast_in_ippool: Literal["disable"]  # Enable/disable inclusion of the subnetwork address


@final
class IppoolObject:
    """Typed FortiObject for firewall/ippool with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # IP pool name. | MaxLen: 79
    name: str
    # IP pool type: overload, one-to-one, fixed-port-range, port-b | Default: overload
    type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"]
    # First IPv4 address (inclusive) in the range for the address | Default: 0.0.0.0
    startip: str
    # Final IPv4 address (inclusive) in the range for the address | Default: 0.0.0.0
    endip: str
    # First port number (inclusive) in the range for the address p | Default: 5117 | Min: 1024 | Max: 65535
    startport: int
    # Final port number (inclusive) in the range for the address p | Default: 65533 | Min: 1024 | Max: 65535
    endport: int
    # First IPv4 address (inclusive) in the range of the source ad | Default: 0.0.0.0
    source_startip: str
    # Final IPv4 address (inclusive) in the range of the source ad | Default: 0.0.0.0
    source_endip: str
    # Number of addresses in a block (64 - 4096, default = 128). | Default: 128 | Min: 64 | Max: 4096
    block_size: int
    # Number of port for each user | Default: 0 | Min: 32 | Max: 60417
    port_per_user: int
    # Number of addresses blocks that can be used by a user | Default: 8 | Min: 1 | Max: 128
    num_blocks_per_user: int
    # Port block allocation timeout (seconds). | Default: 30 | Min: 3 | Max: 86400
    pba_timeout: int
    # Port block allocation interim logging interval | Default: 0 | Min: 600 | Max: 86400
    pba_interim_log: int
    # Enable/disable fullcone NAT. Accept UDP packets from any hos | Default: disable
    permit_any_host: Literal["disable", "enable"]
    # Enable/disable replying to ARP requests when an IP Pool is a | Default: enable
    arp_reply: Literal["disable", "enable"]
    # Select an interface from available options that will reply t | MaxLen: 15
    arp_intf: str
    # Associated interface name. | MaxLen: 15
    associated_interface: str
    # Comment. | MaxLen: 255
    comments: str
    # Enable/disable NAT64. | Default: disable
    nat64: Literal["disable", "enable"]
    # Enable/disable adding NAT64 route. | Default: enable
    add_nat64_route: Literal["disable", "enable"]
    # Source IPv6 network to be translated | Default: ::/0
    source_prefix6: str
    # Subnet length of a single deterministic NAT64 client | Default: 64 | Min: 1 | Max: 128
    client_prefix_length: int
    # Maximum number of concurrent TCP sessions allowed per client | Default: 0 | Min: 0 | Max: 2097000
    tcp_session_quota: int
    # Maximum number of concurrent UDP sessions allowed per client | Default: 0 | Min: 0 | Max: 2097000
    udp_session_quota: int
    # Maximum number of concurrent ICMP sessions allowed per clien | Default: 0 | Min: 0 | Max: 2097000
    icmp_session_quota: int
    # Enable/disable selection of the external port from the port | Default: disable
    privileged_port_use_pba: Literal["disable", "enable"]
    # Enable/disable inclusion of the subnetwork address and broad
    subnet_broadcast_in_ippool: Literal["disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> IppoolPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Ippool:
    """
    Configure IPv4 IP pools.
    
    Path: firewall/ippool
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
    ) -> IppoolResponse: ...
    
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
    ) -> IppoolResponse: ...
    
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
    ) -> list[IppoolResponse]: ...
    
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
    ) -> IppoolObject: ...
    
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
    ) -> IppoolObject: ...
    
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
    ) -> list[IppoolObject]: ...
    
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
    ) -> IppoolResponse: ...
    
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
    ) -> IppoolResponse: ...
    
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
    ) -> list[IppoolResponse]: ...
    
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
    ) -> IppoolObject | list[IppoolObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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
    ) -> IppoolObject: ...
    
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
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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

class IppoolDictMode:
    """Ippool endpoint for dict response mode (default for this client).
    
    By default returns IppoolResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return IppoolObject.
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
    ) -> IppoolObject: ...
    
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
    ) -> list[IppoolObject]: ...
    
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
    ) -> IppoolResponse: ...
    
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
    ) -> list[IppoolResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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
    ) -> IppoolObject: ...
    
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
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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


class IppoolObjectMode:
    """Ippool endpoint for object response mode (default for this client).
    
    By default returns IppoolObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return IppoolResponse (TypedDict).
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
    ) -> IppoolResponse: ...
    
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
    ) -> list[IppoolResponse]: ...
    
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
    ) -> IppoolObject: ...
    
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
    ) -> list[IppoolObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> IppoolObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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
    ) -> IppoolObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> IppoolObject: ...
    
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
        payload_dict: IppoolPayload | None = ...,
        name: str | None = ...,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = ...,
        startip: str | None = ...,
        endip: str | None = ...,
        startport: int | None = ...,
        endport: int | None = ...,
        source_startip: str | None = ...,
        source_endip: str | None = ...,
        block_size: int | None = ...,
        port_per_user: int | None = ...,
        num_blocks_per_user: int | None = ...,
        pba_timeout: int | None = ...,
        pba_interim_log: int | None = ...,
        permit_any_host: Literal["disable", "enable"] | None = ...,
        arp_reply: Literal["disable", "enable"] | None = ...,
        arp_intf: str | None = ...,
        associated_interface: str | None = ...,
        comments: str | None = ...,
        nat64: Literal["disable", "enable"] | None = ...,
        add_nat64_route: Literal["disable", "enable"] | None = ...,
        source_prefix6: str | None = ...,
        client_prefix_length: int | None = ...,
        tcp_session_quota: int | None = ...,
        udp_session_quota: int | None = ...,
        icmp_session_quota: int | None = ...,
        privileged_port_use_pba: Literal["disable", "enable"] | None = ...,
        subnet_broadcast_in_ippool: Literal["disable"] | None = ...,
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
    "Ippool",
    "IppoolDictMode",
    "IppoolObjectMode",
    "IppoolPayload",
    "IppoolObject",
]