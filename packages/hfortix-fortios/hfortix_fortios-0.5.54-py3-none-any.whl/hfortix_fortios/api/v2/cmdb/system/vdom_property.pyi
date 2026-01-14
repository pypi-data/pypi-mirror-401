from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class VdomPropertyPayload(TypedDict, total=False):
    """
    Type hints for system/vdom_property payload fields.
    
    Configure VDOM property.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.vdom.VdomEndpoint` (via: name)

    **Usage:**
        payload: VdomPropertyPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # VDOM name. | MaxLen: 31
    description: str  # Description. | MaxLen: 127
    snmp_index: int  # Permanent SNMP Index of the virtual domain | Default: 0 | Min: 1 | Max: 2147483647
    session: list[dict[str, Any]]  # Maximum guaranteed number of sessions.
    ipsec_phase1: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase 1 tun
    ipsec_phase2: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase 2 tun
    ipsec_phase1_interface: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase1 inte
    ipsec_phase2_interface: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase2 inte
    dialup_tunnel: list[dict[str, Any]]  # Maximum guaranteed number of dial-up tunnels.
    firewall_policy: list[dict[str, Any]]  # Maximum guaranteed number of firewall policies
    firewall_address: list[dict[str, Any]]  # Maximum guaranteed number of firewall addresses
    firewall_addrgrp: list[dict[str, Any]]  # Maximum guaranteed number of firewall address grou
    custom_service: list[dict[str, Any]]  # Maximum guaranteed number of firewall custom servi
    service_group: list[dict[str, Any]]  # Maximum guaranteed number of firewall service grou
    onetime_schedule: list[dict[str, Any]]  # Maximum guaranteed number of firewall one-time sch
    recurring_schedule: list[dict[str, Any]]  # Maximum guaranteed number of firewall recurring sc
    user: list[dict[str, Any]]  # Maximum guaranteed number of local users.
    user_group: list[dict[str, Any]]  # Maximum guaranteed number of user groups.
    sslvpn: list[dict[str, Any]]  # Maximum guaranteed number of Agentless VPNs.
    proxy: list[dict[str, Any]]  # Maximum guaranteed number of concurrent proxy user
    log_disk_quota: list[dict[str, Any]]  # Log disk quota in megabytes (MB). Range depends on

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class VdomPropertyResponse(TypedDict):
    """
    Type hints for system/vdom_property API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # VDOM name. | MaxLen: 31
    description: str  # Description. | MaxLen: 127
    snmp_index: int  # Permanent SNMP Index of the virtual domain | Default: 0 | Min: 1 | Max: 2147483647
    session: list[dict[str, Any]]  # Maximum guaranteed number of sessions.
    ipsec_phase1: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase 1 tun
    ipsec_phase2: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase 2 tun
    ipsec_phase1_interface: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase1 inte
    ipsec_phase2_interface: list[dict[str, Any]]  # Maximum guaranteed number of VPN IPsec phase2 inte
    dialup_tunnel: list[dict[str, Any]]  # Maximum guaranteed number of dial-up tunnels.
    firewall_policy: list[dict[str, Any]]  # Maximum guaranteed number of firewall policies
    firewall_address: list[dict[str, Any]]  # Maximum guaranteed number of firewall addresses
    firewall_addrgrp: list[dict[str, Any]]  # Maximum guaranteed number of firewall address grou
    custom_service: list[dict[str, Any]]  # Maximum guaranteed number of firewall custom servi
    service_group: list[dict[str, Any]]  # Maximum guaranteed number of firewall service grou
    onetime_schedule: list[dict[str, Any]]  # Maximum guaranteed number of firewall one-time sch
    recurring_schedule: list[dict[str, Any]]  # Maximum guaranteed number of firewall recurring sc
    user: list[dict[str, Any]]  # Maximum guaranteed number of local users.
    user_group: list[dict[str, Any]]  # Maximum guaranteed number of user groups.
    sslvpn: list[dict[str, Any]]  # Maximum guaranteed number of Agentless VPNs.
    proxy: list[dict[str, Any]]  # Maximum guaranteed number of concurrent proxy user
    log_disk_quota: list[dict[str, Any]]  # Log disk quota in megabytes (MB). Range depends on


@final
class VdomPropertyObject:
    """Typed FortiObject for system/vdom_property with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # VDOM name. | MaxLen: 31
    name: str
    # Description. | MaxLen: 127
    description: str
    # Permanent SNMP Index of the virtual domain (1 - 2147483647). | Default: 0 | Min: 1 | Max: 2147483647
    snmp_index: int
    # Maximum guaranteed number of sessions.
    session: list[dict[str, Any]]
    # Maximum guaranteed number of VPN IPsec phase 1 tunnels.
    ipsec_phase1: list[dict[str, Any]]
    # Maximum guaranteed number of VPN IPsec phase 2 tunnels.
    ipsec_phase2: list[dict[str, Any]]
    # Maximum guaranteed number of VPN IPsec phase1 interface tunn
    ipsec_phase1_interface: list[dict[str, Any]]
    # Maximum guaranteed number of VPN IPsec phase2 interface tunn
    ipsec_phase2_interface: list[dict[str, Any]]
    # Maximum guaranteed number of dial-up tunnels.
    dialup_tunnel: list[dict[str, Any]]
    # Maximum guaranteed number of firewall policies
    firewall_policy: list[dict[str, Any]]
    # Maximum guaranteed number of firewall addresses
    firewall_address: list[dict[str, Any]]
    # Maximum guaranteed number of firewall address groups
    firewall_addrgrp: list[dict[str, Any]]
    # Maximum guaranteed number of firewall custom services.
    custom_service: list[dict[str, Any]]
    # Maximum guaranteed number of firewall service groups.
    service_group: list[dict[str, Any]]
    # Maximum guaranteed number of firewall one-time schedules..
    onetime_schedule: list[dict[str, Any]]
    # Maximum guaranteed number of firewall recurring schedules.
    recurring_schedule: list[dict[str, Any]]
    # Maximum guaranteed number of local users.
    user: list[dict[str, Any]]
    # Maximum guaranteed number of user groups.
    user_group: list[dict[str, Any]]
    # Maximum guaranteed number of Agentless VPNs.
    sslvpn: list[dict[str, Any]]
    # Maximum guaranteed number of concurrent proxy users.
    proxy: list[dict[str, Any]]
    # Log disk quota in megabytes (MB). Range depends on how much
    log_disk_quota: list[dict[str, Any]]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> VdomPropertyPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class VdomProperty:
    """
    Configure VDOM property.
    
    Path: system/vdom_property
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
    ) -> VdomPropertyResponse: ...
    
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
    ) -> VdomPropertyResponse: ...
    
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
    ) -> list[VdomPropertyResponse]: ...
    
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
    ) -> VdomPropertyObject: ...
    
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
    ) -> VdomPropertyObject: ...
    
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
    ) -> list[VdomPropertyObject]: ...
    
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
    ) -> VdomPropertyResponse: ...
    
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
    ) -> VdomPropertyResponse: ...
    
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
    ) -> list[VdomPropertyResponse]: ...
    
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
    ) -> VdomPropertyObject | list[VdomPropertyObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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
    ) -> VdomPropertyObject: ...
    
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
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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

class VdomPropertyDictMode:
    """VdomProperty endpoint for dict response mode (default for this client).
    
    By default returns VdomPropertyResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return VdomPropertyObject.
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
    ) -> VdomPropertyObject: ...
    
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
    ) -> list[VdomPropertyObject]: ...
    
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
    ) -> VdomPropertyResponse: ...
    
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
    ) -> list[VdomPropertyResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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
    ) -> VdomPropertyObject: ...
    
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
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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


class VdomPropertyObjectMode:
    """VdomProperty endpoint for object response mode (default for this client).
    
    By default returns VdomPropertyObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return VdomPropertyResponse (TypedDict).
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
    ) -> VdomPropertyResponse: ...
    
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
    ) -> list[VdomPropertyResponse]: ...
    
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
    ) -> VdomPropertyObject: ...
    
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
    ) -> list[VdomPropertyObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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
    ) -> VdomPropertyObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> VdomPropertyObject: ...
    
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
        payload_dict: VdomPropertyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        snmp_index: int | None = ...,
        session: str | list[str] | None = ...,
        ipsec_phase1: str | list[str] | None = ...,
        ipsec_phase2: str | list[str] | None = ...,
        ipsec_phase1_interface: str | list[str] | None = ...,
        ipsec_phase2_interface: str | list[str] | None = ...,
        dialup_tunnel: str | list[str] | None = ...,
        firewall_policy: str | list[str] | None = ...,
        firewall_address: str | list[str] | None = ...,
        firewall_addrgrp: str | list[str] | None = ...,
        custom_service: str | list[str] | None = ...,
        service_group: str | list[str] | None = ...,
        onetime_schedule: str | list[str] | None = ...,
        recurring_schedule: str | list[str] | None = ...,
        user: str | list[str] | None = ...,
        user_group: str | list[str] | None = ...,
        sslvpn: str | list[str] | None = ...,
        proxy: str | list[str] | None = ...,
        log_disk_quota: str | list[str] | None = ...,
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
    "VdomProperty",
    "VdomPropertyDictMode",
    "VdomPropertyObjectMode",
    "VdomPropertyPayload",
    "VdomPropertyObject",
]