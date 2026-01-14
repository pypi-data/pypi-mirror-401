from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class LldpSettingsPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/lldp_settings payload fields.
    
    Configure FortiSwitch LLDP settings.
    
    **Usage:**
        payload: LldpSettingsPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    tx_hold: int  # Number of tx-intervals before local LLDP data expi | Default: 4 | Min: 1 | Max: 16
    tx_interval: int  # Frequency of LLDP PDU transmission from FortiSwitc | Default: 30 | Min: 5 | Max: 4095
    fast_start_interval: int  # Frequency of LLDP PDU transmission from FortiSwitc | Default: 2 | Min: 0 | Max: 255
    management_interface: Literal["internal", "mgmt"]  # Primary management interface to be advertised in L | Default: internal
    device_detection: Literal["disable", "enable"]  # Enable/disable dynamic detection of LLDP neighbor | Default: enable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class LldpSettingsResponse(TypedDict):
    """
    Type hints for switch_controller/lldp_settings API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    tx_hold: int  # Number of tx-intervals before local LLDP data expi | Default: 4 | Min: 1 | Max: 16
    tx_interval: int  # Frequency of LLDP PDU transmission from FortiSwitc | Default: 30 | Min: 5 | Max: 4095
    fast_start_interval: int  # Frequency of LLDP PDU transmission from FortiSwitc | Default: 2 | Min: 0 | Max: 255
    management_interface: Literal["internal", "mgmt"]  # Primary management interface to be advertised in L | Default: internal
    device_detection: Literal["disable", "enable"]  # Enable/disable dynamic detection of LLDP neighbor | Default: enable


@final
class LldpSettingsObject:
    """Typed FortiObject for switch_controller/lldp_settings with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Number of tx-intervals before local LLDP data expires | Default: 4 | Min: 1 | Max: 16
    tx_hold: int
    # Frequency of LLDP PDU transmission from FortiSwitch | Default: 30 | Min: 5 | Max: 4095
    tx_interval: int
    # Frequency of LLDP PDU transmission from FortiSwitch for the | Default: 2 | Min: 0 | Max: 255
    fast_start_interval: int
    # Primary management interface to be advertised in LLDP and CD | Default: internal
    management_interface: Literal["internal", "mgmt"]
    # Enable/disable dynamic detection of LLDP neighbor devices fo | Default: enable
    device_detection: Literal["disable", "enable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> LldpSettingsPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class LldpSettings:
    """
    Configure FortiSwitch LLDP settings.
    
    Path: switch_controller/lldp_settings
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsObject: ...
    
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
    ) -> LldpSettingsObject: ...
    
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
    ) -> LldpSettingsObject: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LldpSettingsObject: ...
    
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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

class LldpSettingsDictMode:
    """LldpSettings endpoint for dict response mode (default for this client).
    
    By default returns LldpSettingsResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return LldpSettingsObject.
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
    ) -> LldpSettingsObject: ...
    
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
    ) -> LldpSettingsObject: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LldpSettingsObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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


class LldpSettingsObjectMode:
    """LldpSettings endpoint for object response mode (default for this client).
    
    By default returns LldpSettingsObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return LldpSettingsResponse (TypedDict).
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsResponse: ...
    
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
    ) -> LldpSettingsObject: ...
    
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
    ) -> LldpSettingsObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LldpSettingsObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LldpSettingsObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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
        payload_dict: LldpSettingsPayload | None = ...,
        tx_hold: int | None = ...,
        tx_interval: int | None = ...,
        fast_start_interval: int | None = ...,
        management_interface: Literal["internal", "mgmt"] | None = ...,
        device_detection: Literal["disable", "enable"] | None = ...,
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
    "LldpSettings",
    "LldpSettingsDictMode",
    "LldpSettingsObjectMode",
    "LldpSettingsPayload",
    "LldpSettingsObject",
]