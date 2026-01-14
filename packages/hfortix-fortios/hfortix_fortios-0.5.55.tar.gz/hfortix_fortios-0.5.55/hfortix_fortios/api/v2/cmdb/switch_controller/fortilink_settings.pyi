from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class FortilinkSettingsPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/fortilink_settings payload fields.
    
    Configure integrated FortiLink settings for FortiSwitch.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: fortilink)

    **Usage:**
        payload: FortilinkSettingsPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # FortiLink settings name. | MaxLen: 35
    fortilink: str  # FortiLink interface to which this fortilink-settin | MaxLen: 15
    inactive_timer: int  # Time interval(minutes) to be included in the inact | Default: 15 | Min: 1 | Max: 1440
    link_down_flush: Literal["disable", "enable"]  # Clear NAC and dynamic devices on switch ports on l | Default: enable
    access_vlan_mode: Literal["legacy", "fail-open", "fail-close"]  # Intra VLAN traffic behavior with loss of connectio | Default: legacy
    nac_ports: str  # NAC specific configuration.

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class FortilinkSettingsResponse(TypedDict):
    """
    Type hints for switch_controller/fortilink_settings API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # FortiLink settings name. | MaxLen: 35
    fortilink: str  # FortiLink interface to which this fortilink-settin | MaxLen: 15
    inactive_timer: int  # Time interval(minutes) to be included in the inact | Default: 15 | Min: 1 | Max: 1440
    link_down_flush: Literal["disable", "enable"]  # Clear NAC and dynamic devices on switch ports on l | Default: enable
    access_vlan_mode: Literal["legacy", "fail-open", "fail-close"]  # Intra VLAN traffic behavior with loss of connectio | Default: legacy
    nac_ports: str  # NAC specific configuration.


@final
class FortilinkSettingsObject:
    """Typed FortiObject for switch_controller/fortilink_settings with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # FortiLink settings name. | MaxLen: 35
    name: str
    # FortiLink interface to which this fortilink-setting belongs. | MaxLen: 15
    fortilink: str
    # Time interval(minutes) to be included in the inactive device | Default: 15 | Min: 1 | Max: 1440
    inactive_timer: int
    # Clear NAC and dynamic devices on switch ports on link down e | Default: enable
    link_down_flush: Literal["disable", "enable"]
    # Intra VLAN traffic behavior with loss of connection to the F | Default: legacy
    access_vlan_mode: Literal["legacy", "fail-open", "fail-close"]
    # NAC specific configuration.
    nac_ports: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> FortilinkSettingsPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class FortilinkSettings:
    """
    Configure integrated FortiLink settings for FortiSwitch.
    
    Path: switch_controller/fortilink_settings
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
    ) -> FortilinkSettingsResponse: ...
    
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
    ) -> FortilinkSettingsResponse: ...
    
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
    ) -> list[FortilinkSettingsResponse]: ...
    
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
    ) -> FortilinkSettingsObject: ...
    
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
    ) -> FortilinkSettingsObject: ...
    
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
    ) -> list[FortilinkSettingsObject]: ...
    
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
    ) -> FortilinkSettingsResponse: ...
    
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
    ) -> FortilinkSettingsResponse: ...
    
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
    ) -> list[FortilinkSettingsResponse]: ...
    
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
    ) -> FortilinkSettingsObject | list[FortilinkSettingsObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
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
    ) -> FortilinkSettingsObject: ...
    
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
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
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

class FortilinkSettingsDictMode:
    """FortilinkSettings endpoint for dict response mode (default for this client).
    
    By default returns FortilinkSettingsResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return FortilinkSettingsObject.
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
    ) -> FortilinkSettingsObject: ...
    
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
    ) -> list[FortilinkSettingsObject]: ...
    
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
    ) -> FortilinkSettingsResponse: ...
    
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
    ) -> list[FortilinkSettingsResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
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
    ) -> FortilinkSettingsObject: ...
    
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
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
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


class FortilinkSettingsObjectMode:
    """FortilinkSettings endpoint for object response mode (default for this client).
    
    By default returns FortilinkSettingsObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return FortilinkSettingsResponse (TypedDict).
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
    ) -> FortilinkSettingsResponse: ...
    
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
    ) -> list[FortilinkSettingsResponse]: ...
    
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
    ) -> FortilinkSettingsObject: ...
    
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
    ) -> list[FortilinkSettingsObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
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
    ) -> FortilinkSettingsObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortilinkSettingsObject: ...
    
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
        payload_dict: FortilinkSettingsPayload | None = ...,
        name: str | None = ...,
        fortilink: str | None = ...,
        inactive_timer: int | None = ...,
        link_down_flush: Literal["disable", "enable"] | None = ...,
        access_vlan_mode: Literal["legacy", "fail-open", "fail-close"] | None = ...,
        nac_ports: str | None = ...,
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
    "FortilinkSettings",
    "FortilinkSettingsDictMode",
    "FortilinkSettingsObjectMode",
    "FortilinkSettingsPayload",
    "FortilinkSettingsObject",
]