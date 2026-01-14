from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class VlanPolicyPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/vlan_policy payload fields.
    
    Configure VLAN policy to be applied on the managed FortiSwitch ports through dynamic-port-policy.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: fortilink, vlan)

    **Usage:**
        payload: VlanPolicyPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # VLAN policy name. | MaxLen: 63
    description: str  # Description for the VLAN policy. | MaxLen: 63
    fortilink: str  # FortiLink interface for which this VLAN policy bel | MaxLen: 15
    vlan: str  # Native VLAN to be applied when using this VLAN pol | MaxLen: 15
    allowed_vlans: list[dict[str, Any]]  # Allowed VLANs to be applied when using this VLAN p
    untagged_vlans: list[dict[str, Any]]  # Untagged VLANs to be applied when using this VLAN
    allowed_vlans_all: Literal["enable", "disable"]  # Enable/disable all defined VLANs when using this V | Default: disable
    discard_mode: Literal["none", "all-untagged", "all-tagged"]  # Discard mode to be applied when using this VLAN po | Default: none

# Nested TypedDicts for table field children (dict mode)

class VlanPolicyAllowedvlansItem(TypedDict):
    """Type hints for allowed-vlans table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    vlan_name: str  # VLAN name. | MaxLen: 79


class VlanPolicyUntaggedvlansItem(TypedDict):
    """Type hints for untagged-vlans table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    vlan_name: str  # VLAN name. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class VlanPolicyAllowedvlansObject:
    """Typed object for allowed-vlans table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # VLAN name. | MaxLen: 79
    vlan_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class VlanPolicyUntaggedvlansObject:
    """Typed object for untagged-vlans table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # VLAN name. | MaxLen: 79
    vlan_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class VlanPolicyResponse(TypedDict):
    """
    Type hints for switch_controller/vlan_policy API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # VLAN policy name. | MaxLen: 63
    description: str  # Description for the VLAN policy. | MaxLen: 63
    fortilink: str  # FortiLink interface for which this VLAN policy bel | MaxLen: 15
    vlan: str  # Native VLAN to be applied when using this VLAN pol | MaxLen: 15
    allowed_vlans: list[VlanPolicyAllowedvlansItem]  # Allowed VLANs to be applied when using this VLAN p
    untagged_vlans: list[VlanPolicyUntaggedvlansItem]  # Untagged VLANs to be applied when using this VLAN
    allowed_vlans_all: Literal["enable", "disable"]  # Enable/disable all defined VLANs when using this V | Default: disable
    discard_mode: Literal["none", "all-untagged", "all-tagged"]  # Discard mode to be applied when using this VLAN po | Default: none


@final
class VlanPolicyObject:
    """Typed FortiObject for switch_controller/vlan_policy with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # VLAN policy name. | MaxLen: 63
    name: str
    # Description for the VLAN policy. | MaxLen: 63
    description: str
    # FortiLink interface for which this VLAN policy belongs to. | MaxLen: 15
    fortilink: str
    # Native VLAN to be applied when using this VLAN policy. | MaxLen: 15
    vlan: str
    # Allowed VLANs to be applied when using this VLAN policy.
    allowed_vlans: list[VlanPolicyAllowedvlansObject]
    # Untagged VLANs to be applied when using this VLAN policy.
    untagged_vlans: list[VlanPolicyUntaggedvlansObject]
    # Enable/disable all defined VLANs when using this VLAN policy | Default: disable
    allowed_vlans_all: Literal["enable", "disable"]
    # Discard mode to be applied when using this VLAN policy. | Default: none
    discard_mode: Literal["none", "all-untagged", "all-tagged"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> VlanPolicyPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class VlanPolicy:
    """
    Configure VLAN policy to be applied on the managed FortiSwitch ports through dynamic-port-policy.
    
    Path: switch_controller/vlan_policy
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
    ) -> VlanPolicyResponse: ...
    
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
    ) -> VlanPolicyResponse: ...
    
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
    ) -> list[VlanPolicyResponse]: ...
    
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
    ) -> VlanPolicyObject: ...
    
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
    ) -> VlanPolicyObject: ...
    
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
    ) -> list[VlanPolicyObject]: ...
    
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
    ) -> VlanPolicyResponse: ...
    
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
    ) -> VlanPolicyResponse: ...
    
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
    ) -> list[VlanPolicyResponse]: ...
    
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
    ) -> VlanPolicyObject | list[VlanPolicyObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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
    ) -> VlanPolicyObject: ...
    
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
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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

class VlanPolicyDictMode:
    """VlanPolicy endpoint for dict response mode (default for this client).
    
    By default returns VlanPolicyResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return VlanPolicyObject.
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
    ) -> VlanPolicyObject: ...
    
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
    ) -> list[VlanPolicyObject]: ...
    
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
    ) -> VlanPolicyResponse: ...
    
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
    ) -> list[VlanPolicyResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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
    ) -> VlanPolicyObject: ...
    
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
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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


class VlanPolicyObjectMode:
    """VlanPolicy endpoint for object response mode (default for this client).
    
    By default returns VlanPolicyObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return VlanPolicyResponse (TypedDict).
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
    ) -> VlanPolicyResponse: ...
    
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
    ) -> list[VlanPolicyResponse]: ...
    
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
    ) -> VlanPolicyObject: ...
    
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
    ) -> list[VlanPolicyObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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
    ) -> VlanPolicyObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> VlanPolicyObject: ...
    
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
        payload_dict: VlanPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        fortilink: str | None = ...,
        vlan: str | None = ...,
        allowed_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        untagged_vlans: str | list[str] | list[dict[str, Any]] | None = ...,
        allowed_vlans_all: Literal["enable", "disable"] | None = ...,
        discard_mode: Literal["none", "all-untagged", "all-tagged"] | None = ...,
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
    "VlanPolicy",
    "VlanPolicyDictMode",
    "VlanPolicyObjectMode",
    "VlanPolicyPayload",
    "VlanPolicyObject",
]