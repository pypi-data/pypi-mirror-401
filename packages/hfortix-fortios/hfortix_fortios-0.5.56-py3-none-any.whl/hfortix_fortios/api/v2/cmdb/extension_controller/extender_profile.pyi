from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ExtenderProfilePayload(TypedDict, total=False):
    """
    Type hints for extension_controller/extender_profile payload fields.
    
    FortiExtender extender profile configuration.
    
    **Usage:**
        payload: ExtenderProfilePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # FortiExtender profile name. | MaxLen: 31
    id: int  # ID. | Default: 32 | Min: 0 | Max: 102400000
    model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]  # Model. | Default: FX201E
    extension: Literal["wan-extension", "lan-extension"]  # Extension option. | Default: wan-extension
    allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"]  # Control management access to the managed extender.
    login_password_change: Literal["yes", "default", "no"]  # Change or reset the administrator password of a ma | Default: no
    login_password: str  # Set the managed extender's administrator password. | MaxLen: 27
    enforce_bandwidth: Literal["enable", "disable"]  # Enable/disable enforcement of bandwidth on LAN ext | Default: disable
    bandwidth_limit: int  # FortiExtender LAN extension bandwidth limit (Mbps) | Default: 1024 | Min: 1 | Max: 16776000
    cellular: str  # FortiExtender cellular configuration.
    wifi: str  # FortiExtender Wi-Fi configuration.
    lan_extension: str  # FortiExtender LAN extension configuration.

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class ExtenderProfileResponse(TypedDict):
    """
    Type hints for extension_controller/extender_profile API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # FortiExtender profile name. | MaxLen: 31
    id: int  # ID. | Default: 32 | Min: 0 | Max: 102400000
    model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]  # Model. | Default: FX201E
    extension: Literal["wan-extension", "lan-extension"]  # Extension option. | Default: wan-extension
    allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"]  # Control management access to the managed extender.
    login_password_change: Literal["yes", "default", "no"]  # Change or reset the administrator password of a ma | Default: no
    login_password: str  # Set the managed extender's administrator password. | MaxLen: 27
    enforce_bandwidth: Literal["enable", "disable"]  # Enable/disable enforcement of bandwidth on LAN ext | Default: disable
    bandwidth_limit: int  # FortiExtender LAN extension bandwidth limit (Mbps) | Default: 1024 | Min: 1 | Max: 16776000
    cellular: str  # FortiExtender cellular configuration.
    wifi: str  # FortiExtender Wi-Fi configuration.
    lan_extension: str  # FortiExtender LAN extension configuration.


@final
class ExtenderProfileObject:
    """Typed FortiObject for extension_controller/extender_profile with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # FortiExtender profile name. | MaxLen: 31
    name: str
    # ID. | Default: 32 | Min: 0 | Max: 102400000
    id: int
    # Model. | Default: FX201E
    model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]
    # Extension option. | Default: wan-extension
    extension: Literal["wan-extension", "lan-extension"]
    # Control management access to the managed extender. Separate
    allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"]
    # Change or reset the administrator password of a managed exte | Default: no
    login_password_change: Literal["yes", "default", "no"]
    # Set the managed extender's administrator password. | MaxLen: 27
    login_password: str
    # Enable/disable enforcement of bandwidth on LAN extension int | Default: disable
    enforce_bandwidth: Literal["enable", "disable"]
    # FortiExtender LAN extension bandwidth limit (Mbps). | Default: 1024 | Min: 1 | Max: 16776000
    bandwidth_limit: int
    # FortiExtender cellular configuration.
    cellular: str
    # FortiExtender Wi-Fi configuration.
    wifi: str
    # FortiExtender LAN extension configuration.
    lan_extension: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ExtenderProfilePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class ExtenderProfile:
    """
    FortiExtender extender profile configuration.
    
    Path: extension_controller/extender_profile
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
    ) -> ExtenderProfileResponse: ...
    
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
    ) -> ExtenderProfileResponse: ...
    
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
    ) -> list[ExtenderProfileResponse]: ...
    
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
    ) -> ExtenderProfileObject: ...
    
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
    ) -> ExtenderProfileObject: ...
    
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
    ) -> list[ExtenderProfileObject]: ...
    
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
    ) -> ExtenderProfileResponse: ...
    
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
    ) -> ExtenderProfileResponse: ...
    
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
    ) -> list[ExtenderProfileResponse]: ...
    
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
    ) -> ExtenderProfileObject | list[ExtenderProfileObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
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
    ) -> ExtenderProfileObject: ...
    
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
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
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

class ExtenderProfileDictMode:
    """ExtenderProfile endpoint for dict response mode (default for this client).
    
    By default returns ExtenderProfileResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ExtenderProfileObject.
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
    ) -> ExtenderProfileObject: ...
    
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
    ) -> list[ExtenderProfileObject]: ...
    
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
    ) -> ExtenderProfileResponse: ...
    
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
    ) -> list[ExtenderProfileResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
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
    ) -> ExtenderProfileObject: ...
    
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
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
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


class ExtenderProfileObjectMode:
    """ExtenderProfile endpoint for object response mode (default for this client).
    
    By default returns ExtenderProfileObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ExtenderProfileResponse (TypedDict).
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
    ) -> ExtenderProfileResponse: ...
    
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
    ) -> list[ExtenderProfileResponse]: ...
    
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
    ) -> ExtenderProfileObject: ...
    
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
    ) -> list[ExtenderProfileObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
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
    ) -> ExtenderProfileObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ExtenderProfileObject: ...
    
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
        payload_dict: ExtenderProfilePayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        model: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"] | None = ...,
        extension: Literal["wan-extension", "lan-extension"] | None = ...,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = ...,
        login_password_change: Literal["yes", "default", "no"] | None = ...,
        login_password: str | None = ...,
        enforce_bandwidth: Literal["enable", "disable"] | None = ...,
        bandwidth_limit: int | None = ...,
        cellular: str | None = ...,
        wifi: str | None = ...,
        lan_extension: str | None = ...,
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
    "ExtenderProfile",
    "ExtenderProfileDictMode",
    "ExtenderProfileObjectMode",
    "ExtenderProfilePayload",
    "ExtenderProfileObject",
]