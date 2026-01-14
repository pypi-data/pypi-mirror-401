from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class IpamPayload(TypedDict, total=False):
    """
    Type hints for system/ipam payload fields.
    
    Configure IP address management services.
    
    **Usage:**
        payload: IpamPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    status: Literal["enable", "disable"]  # Enable/disable IP address management services. | Default: disable
    server_type: Literal["fabric-root"]  # Configure the type of IPAM server to use. | Default: fabric-root
    automatic_conflict_resolution: Literal["disable", "enable"]  # Enable/disable automatic conflict resolution. | Default: disable
    require_subnet_size_match: Literal["disable", "enable"]  # Enable/disable reassignment of subnets to make req | Default: enable
    manage_lan_addresses: Literal["disable", "enable"]  # Enable/disable default management of LAN interface | Default: enable
    manage_lan_extension_addresses: Literal["disable", "enable"]  # Enable/disable default management of FortiExtender | Default: enable
    manage_ssid_addresses: Literal["disable", "enable"]  # Enable/disable default management of FortiAP SSID | Default: enable
    pools: list[dict[str, Any]]  # Configure IPAM pools.
    rules: list[dict[str, Any]]  # Configure IPAM allocation rules.

# Nested TypedDicts for table field children (dict mode)

class IpamPoolsItem(TypedDict):
    """Type hints for pools table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # IPAM pool name. | MaxLen: 79
    description: str  # Description. | MaxLen: 127
    subnet: str  # Configure IPAM pool subnet, Class A - Class B subn | Default: 0.0.0.0 0.0.0.0
    exclude: str  # Configure pool exclude subnets.


class IpamRulesItem(TypedDict):
    """Type hints for rules table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # IPAM rule name. | MaxLen: 79
    description: str  # Description. | MaxLen: 127
    device: str  # Configure serial number or wildcard of FortiGate t
    interface: str  # Configure name or wildcard of interface to match.
    role: Literal["any", "lan", "wan", "dmz", "undefined"]  # Configure role of interface to match. | Default: any
    pool: str  # Configure name of IPAM pool to use.
    dhcp: Literal["enable", "disable"]  # Enable/disable DHCP server for matching IPAM inter | Default: disable


# Nested classes for table field children (object mode)

@final
class IpamPoolsObject:
    """Typed object for pools table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # IPAM pool name. | MaxLen: 79
    name: str
    # Description. | MaxLen: 127
    description: str
    # Configure IPAM pool subnet, Class A - Class B subnet. | Default: 0.0.0.0 0.0.0.0
    subnet: str
    # Configure pool exclude subnets.
    exclude: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class IpamRulesObject:
    """Typed object for rules table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # IPAM rule name. | MaxLen: 79
    name: str
    # Description. | MaxLen: 127
    description: str
    # Configure serial number or wildcard of FortiGate to match.
    device: str
    # Configure name or wildcard of interface to match.
    interface: str
    # Configure role of interface to match. | Default: any
    role: Literal["any", "lan", "wan", "dmz", "undefined"]
    # Configure name of IPAM pool to use.
    pool: str
    # Enable/disable DHCP server for matching IPAM interfaces. | Default: disable
    dhcp: Literal["enable", "disable"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class IpamResponse(TypedDict):
    """
    Type hints for system/ipam API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    status: Literal["enable", "disable"]  # Enable/disable IP address management services. | Default: disable
    server_type: Literal["fabric-root"]  # Configure the type of IPAM server to use. | Default: fabric-root
    automatic_conflict_resolution: Literal["disable", "enable"]  # Enable/disable automatic conflict resolution. | Default: disable
    require_subnet_size_match: Literal["disable", "enable"]  # Enable/disable reassignment of subnets to make req | Default: enable
    manage_lan_addresses: Literal["disable", "enable"]  # Enable/disable default management of LAN interface | Default: enable
    manage_lan_extension_addresses: Literal["disable", "enable"]  # Enable/disable default management of FortiExtender | Default: enable
    manage_ssid_addresses: Literal["disable", "enable"]  # Enable/disable default management of FortiAP SSID | Default: enable
    pools: list[IpamPoolsItem]  # Configure IPAM pools.
    rules: list[IpamRulesItem]  # Configure IPAM allocation rules.


@final
class IpamObject:
    """Typed FortiObject for system/ipam with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Enable/disable IP address management services. | Default: disable
    status: Literal["enable", "disable"]
    # Configure the type of IPAM server to use. | Default: fabric-root
    server_type: Literal["fabric-root"]
    # Enable/disable automatic conflict resolution. | Default: disable
    automatic_conflict_resolution: Literal["disable", "enable"]
    # Enable/disable reassignment of subnets to make requested and | Default: enable
    require_subnet_size_match: Literal["disable", "enable"]
    # Enable/disable default management of LAN interface addresses | Default: enable
    manage_lan_addresses: Literal["disable", "enable"]
    # Enable/disable default management of FortiExtender LAN exten | Default: enable
    manage_lan_extension_addresses: Literal["disable", "enable"]
    # Enable/disable default management of FortiAP SSID addresses. | Default: enable
    manage_ssid_addresses: Literal["disable", "enable"]
    # Configure IPAM pools.
    pools: list[IpamPoolsObject]
    # Configure IPAM allocation rules.
    rules: list[IpamRulesObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> IpamPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Ipam:
    """
    Configure IP address management services.
    
    Path: system/ipam
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamObject: ...
    
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
    ) -> IpamObject: ...
    
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
    ) -> IpamObject: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IpamObject: ...
    
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
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

class IpamDictMode:
    """Ipam endpoint for dict response mode (default for this client).
    
    By default returns IpamResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return IpamObject.
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
    ) -> IpamObject: ...
    
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
    ) -> IpamObject: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IpamObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
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


class IpamObjectMode:
    """Ipam endpoint for object response mode (default for this client).
    
    By default returns IpamObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return IpamResponse (TypedDict).
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamResponse: ...
    
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
    ) -> IpamObject: ...
    
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
    ) -> IpamObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> IpamObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> IpamObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: IpamPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        server_type: Literal["fabric-root"] | None = ...,
        automatic_conflict_resolution: Literal["disable", "enable"] | None = ...,
        require_subnet_size_match: Literal["disable", "enable"] | None = ...,
        manage_lan_addresses: Literal["disable", "enable"] | None = ...,
        manage_lan_extension_addresses: Literal["disable", "enable"] | None = ...,
        manage_ssid_addresses: Literal["disable", "enable"] | None = ...,
        pools: str | list[str] | list[dict[str, Any]] | None = ...,
        rules: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "Ipam",
    "IpamDictMode",
    "IpamObjectMode",
    "IpamPayload",
    "IpamObject",
]