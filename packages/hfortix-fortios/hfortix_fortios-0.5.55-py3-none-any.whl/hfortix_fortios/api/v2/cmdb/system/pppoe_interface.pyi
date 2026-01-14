from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class PppoeInterfacePayload(TypedDict, total=False):
    """
    Type hints for system/pppoe_interface payload fields.
    
    Configure the PPPoE interfaces.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: device)

    **Usage:**
        payload: PppoeInterfacePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name of the PPPoE interface. | MaxLen: 15
    dial_on_demand: Literal["enable", "disable"]  # Enable/disable dial on demand to dial the PPPoE in | Default: disable
    ipv6: Literal["enable", "disable"]  # Enable/disable IPv6 Control Protocol (IPv6CP). | Default: disable
    device: str  # Name for the physical interface. | MaxLen: 15
    username: str  # User name. | MaxLen: 64
    password: str  # Enter the password. | MaxLen: 128
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]  # CoS in VLAN tag for outgoing PPPoE/PPP packets. | Default: cos0
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]  # PPP authentication type to use. | Default: auto
    ipunnumbered: str  # PPPoE unnumbered IP. | Default: 0.0.0.0
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]  # Enable/disable PPPoE unnumbered negotiation. | Default: enable
    idle_timeout: int  # PPPoE auto disconnect after idle timeout | Default: 0 | Min: 0 | Max: 4294967295
    multilink: Literal["enable", "disable"]  # Enable/disable PPP multilink support. | Default: disable
    mrru: int  # PPP MRRU (296 - 65535, default = 1500). | Default: 1500 | Min: 296 | Max: 65535
    disc_retry_timeout: int  # PPPoE discovery init timeout value in | Default: 1 | Min: 0 | Max: 4294967295
    padt_retry_timeout: int  # PPPoE terminate timeout value in | Default: 1 | Min: 0 | Max: 4294967295
    service_name: str  # PPPoE service name. | MaxLen: 63
    ac_name: str  # PPPoE AC name. | MaxLen: 63
    lcp_echo_interval: int  # Time in seconds between PPPoE Link Control Protoco | Default: 5 | Min: 0 | Max: 32767
    lcp_max_echo_fails: int  # Maximum missed LCP echo messages before disconnect | Default: 3 | Min: 0 | Max: 32767

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class PppoeInterfaceResponse(TypedDict):
    """
    Type hints for system/pppoe_interface API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name of the PPPoE interface. | MaxLen: 15
    dial_on_demand: Literal["enable", "disable"]  # Enable/disable dial on demand to dial the PPPoE in | Default: disable
    ipv6: Literal["enable", "disable"]  # Enable/disable IPv6 Control Protocol (IPv6CP). | Default: disable
    device: str  # Name for the physical interface. | MaxLen: 15
    username: str  # User name. | MaxLen: 64
    password: str  # Enter the password. | MaxLen: 128
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]  # CoS in VLAN tag for outgoing PPPoE/PPP packets. | Default: cos0
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]  # PPP authentication type to use. | Default: auto
    ipunnumbered: str  # PPPoE unnumbered IP. | Default: 0.0.0.0
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]  # Enable/disable PPPoE unnumbered negotiation. | Default: enable
    idle_timeout: int  # PPPoE auto disconnect after idle timeout | Default: 0 | Min: 0 | Max: 4294967295
    multilink: Literal["enable", "disable"]  # Enable/disable PPP multilink support. | Default: disable
    mrru: int  # PPP MRRU (296 - 65535, default = 1500). | Default: 1500 | Min: 296 | Max: 65535
    disc_retry_timeout: int  # PPPoE discovery init timeout value in | Default: 1 | Min: 0 | Max: 4294967295
    padt_retry_timeout: int  # PPPoE terminate timeout value in | Default: 1 | Min: 0 | Max: 4294967295
    service_name: str  # PPPoE service name. | MaxLen: 63
    ac_name: str  # PPPoE AC name. | MaxLen: 63
    lcp_echo_interval: int  # Time in seconds between PPPoE Link Control Protoco | Default: 5 | Min: 0 | Max: 32767
    lcp_max_echo_fails: int  # Maximum missed LCP echo messages before disconnect | Default: 3 | Min: 0 | Max: 32767


@final
class PppoeInterfaceObject:
    """Typed FortiObject for system/pppoe_interface with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name of the PPPoE interface. | MaxLen: 15
    name: str
    # Enable/disable dial on demand to dial the PPPoE interface wh | Default: disable
    dial_on_demand: Literal["enable", "disable"]
    # Enable/disable IPv6 Control Protocol (IPv6CP). | Default: disable
    ipv6: Literal["enable", "disable"]
    # Name for the physical interface. | MaxLen: 15
    device: str
    # User name. | MaxLen: 64
    username: str
    # Enter the password. | MaxLen: 128
    password: str
    # CoS in VLAN tag for outgoing PPPoE/PPP packets. | Default: cos0
    pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]
    # PPP authentication type to use. | Default: auto
    auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]
    # PPPoE unnumbered IP. | Default: 0.0.0.0
    ipunnumbered: str
    # Enable/disable PPPoE unnumbered negotiation. | Default: enable
    pppoe_unnumbered_negotiate: Literal["enable", "disable"]
    # PPPoE auto disconnect after idle timeout (0-4294967295 sec). | Default: 0 | Min: 0 | Max: 4294967295
    idle_timeout: int
    # Enable/disable PPP multilink support. | Default: disable
    multilink: Literal["enable", "disable"]
    # PPP MRRU (296 - 65535, default = 1500). | Default: 1500 | Min: 296 | Max: 65535
    mrru: int
    # PPPoE discovery init timeout value in (0-4294967295 sec). | Default: 1 | Min: 0 | Max: 4294967295
    disc_retry_timeout: int
    # PPPoE terminate timeout value in (0-4294967295 sec). | Default: 1 | Min: 0 | Max: 4294967295
    padt_retry_timeout: int
    # PPPoE service name. | MaxLen: 63
    service_name: str
    # PPPoE AC name. | MaxLen: 63
    ac_name: str
    # Time in seconds between PPPoE Link Control Protocol (LCP) ec | Default: 5 | Min: 0 | Max: 32767
    lcp_echo_interval: int
    # Maximum missed LCP echo messages before disconnect. | Default: 3 | Min: 0 | Max: 32767
    lcp_max_echo_fails: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> PppoeInterfacePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class PppoeInterface:
    """
    Configure the PPPoE interfaces.
    
    Path: system/pppoe_interface
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
    ) -> PppoeInterfaceResponse: ...
    
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
    ) -> PppoeInterfaceResponse: ...
    
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
    ) -> list[PppoeInterfaceResponse]: ...
    
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
    ) -> PppoeInterfaceObject: ...
    
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
    ) -> PppoeInterfaceObject: ...
    
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
    ) -> list[PppoeInterfaceObject]: ...
    
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
    ) -> PppoeInterfaceResponse: ...
    
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
    ) -> PppoeInterfaceResponse: ...
    
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
    ) -> list[PppoeInterfaceResponse]: ...
    
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
    ) -> PppoeInterfaceObject | list[PppoeInterfaceObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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
    ) -> PppoeInterfaceObject: ...
    
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
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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

class PppoeInterfaceDictMode:
    """PppoeInterface endpoint for dict response mode (default for this client).
    
    By default returns PppoeInterfaceResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return PppoeInterfaceObject.
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
    ) -> PppoeInterfaceObject: ...
    
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
    ) -> list[PppoeInterfaceObject]: ...
    
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
    ) -> PppoeInterfaceResponse: ...
    
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
    ) -> list[PppoeInterfaceResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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
    ) -> PppoeInterfaceObject: ...
    
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
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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


class PppoeInterfaceObjectMode:
    """PppoeInterface endpoint for object response mode (default for this client).
    
    By default returns PppoeInterfaceObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return PppoeInterfaceResponse (TypedDict).
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
    ) -> PppoeInterfaceResponse: ...
    
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
    ) -> list[PppoeInterfaceResponse]: ...
    
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
    ) -> PppoeInterfaceObject: ...
    
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
    ) -> list[PppoeInterfaceObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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
    ) -> PppoeInterfaceObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PppoeInterfaceObject: ...
    
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
        payload_dict: PppoeInterfacePayload | None = ...,
        name: str | None = ...,
        dial_on_demand: Literal["enable", "disable"] | None = ...,
        ipv6: Literal["enable", "disable"] | None = ...,
        device: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pppoe_egress_cos: Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"] | None = ...,
        auth_type: Literal["auto", "pap", "chap", "mschapv1", "mschapv2"] | None = ...,
        ipunnumbered: str | None = ...,
        pppoe_unnumbered_negotiate: Literal["enable", "disable"] | None = ...,
        idle_timeout: int | None = ...,
        multilink: Literal["enable", "disable"] | None = ...,
        mrru: int | None = ...,
        disc_retry_timeout: int | None = ...,
        padt_retry_timeout: int | None = ...,
        service_name: str | None = ...,
        ac_name: str | None = ...,
        lcp_echo_interval: int | None = ...,
        lcp_max_echo_fails: int | None = ...,
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
    "PppoeInterface",
    "PppoeInterfaceDictMode",
    "PppoeInterfaceObjectMode",
    "PppoeInterfacePayload",
    "PppoeInterfaceObject",
]