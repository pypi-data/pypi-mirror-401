from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class TrafficPolicyPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/traffic_policy payload fields.
    
    Configure FortiSwitch traffic policy.
    
    **Usage:**
        payload: TrafficPolicyPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Traffic policy name. | MaxLen: 63
    description: str  # Description of the traffic policy. | MaxLen: 63
    policer_status: Literal["enable", "disable"]  # Enable/disable policer config on the traffic polic | Default: enable
    guaranteed_bandwidth: int  # Guaranteed bandwidth in kbps | Default: 10000 | Min: 0 | Max: 524287000
    guaranteed_burst: int  # Guaranteed burst size in bytes | Default: 45000 | Min: 0 | Max: 4294967295
    maximum_burst: int  # Maximum burst size in bytes | Default: 67500 | Min: 0 | Max: 4294967295
    type: Literal["ingress", "egress"]  # Configure type of policy(ingress/egress). | Default: ingress
    cos_queue: int  # COS queue(0 - 7), or unset to disable. | Min: 0 | Max: 7

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class TrafficPolicyResponse(TypedDict):
    """
    Type hints for switch_controller/traffic_policy API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Traffic policy name. | MaxLen: 63
    description: str  # Description of the traffic policy. | MaxLen: 63
    policer_status: Literal["enable", "disable"]  # Enable/disable policer config on the traffic polic | Default: enable
    guaranteed_bandwidth: int  # Guaranteed bandwidth in kbps | Default: 10000 | Min: 0 | Max: 524287000
    guaranteed_burst: int  # Guaranteed burst size in bytes | Default: 45000 | Min: 0 | Max: 4294967295
    maximum_burst: int  # Maximum burst size in bytes | Default: 67500 | Min: 0 | Max: 4294967295
    type: Literal["ingress", "egress"]  # Configure type of policy(ingress/egress). | Default: ingress
    cos_queue: int  # COS queue(0 - 7), or unset to disable. | Min: 0 | Max: 7


@final
class TrafficPolicyObject:
    """Typed FortiObject for switch_controller/traffic_policy with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Traffic policy name. | MaxLen: 63
    name: str
    # Description of the traffic policy. | MaxLen: 63
    description: str
    # Enable/disable policer config on the traffic policy. | Default: enable
    policer_status: Literal["enable", "disable"]
    # Guaranteed bandwidth in kbps (max value = 524287000). | Default: 10000 | Min: 0 | Max: 524287000
    guaranteed_bandwidth: int
    # Guaranteed burst size in bytes (max value = 4294967295). | Default: 45000 | Min: 0 | Max: 4294967295
    guaranteed_burst: int
    # Maximum burst size in bytes (max value = 4294967295). | Default: 67500 | Min: 0 | Max: 4294967295
    maximum_burst: int
    # Configure type of policy(ingress/egress). | Default: ingress
    type: Literal["ingress", "egress"]
    # COS queue(0 - 7), or unset to disable. | Min: 0 | Max: 7
    cos_queue: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> TrafficPolicyPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class TrafficPolicy:
    """
    Configure FortiSwitch traffic policy.
    
    Path: switch_controller/traffic_policy
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
    ) -> TrafficPolicyResponse: ...
    
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
    ) -> TrafficPolicyResponse: ...
    
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
    ) -> list[TrafficPolicyResponse]: ...
    
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
    ) -> TrafficPolicyObject: ...
    
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
    ) -> TrafficPolicyObject: ...
    
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
    ) -> list[TrafficPolicyObject]: ...
    
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
    ) -> TrafficPolicyResponse: ...
    
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
    ) -> TrafficPolicyResponse: ...
    
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
    ) -> list[TrafficPolicyResponse]: ...
    
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
    ) -> TrafficPolicyObject | list[TrafficPolicyObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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
    ) -> TrafficPolicyObject: ...
    
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
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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

class TrafficPolicyDictMode:
    """TrafficPolicy endpoint for dict response mode (default for this client).
    
    By default returns TrafficPolicyResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return TrafficPolicyObject.
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
    ) -> TrafficPolicyObject: ...
    
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
    ) -> list[TrafficPolicyObject]: ...
    
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
    ) -> TrafficPolicyResponse: ...
    
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
    ) -> list[TrafficPolicyResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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
    ) -> TrafficPolicyObject: ...
    
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
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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


class TrafficPolicyObjectMode:
    """TrafficPolicy endpoint for object response mode (default for this client).
    
    By default returns TrafficPolicyObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return TrafficPolicyResponse (TypedDict).
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
    ) -> TrafficPolicyResponse: ...
    
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
    ) -> list[TrafficPolicyResponse]: ...
    
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
    ) -> TrafficPolicyObject: ...
    
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
    ) -> list[TrafficPolicyObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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
    ) -> TrafficPolicyObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficPolicyObject: ...
    
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
        payload_dict: TrafficPolicyPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        policer_status: Literal["enable", "disable"] | None = ...,
        guaranteed_bandwidth: int | None = ...,
        guaranteed_burst: int | None = ...,
        maximum_burst: int | None = ...,
        type: Literal["ingress", "egress"] | None = ...,
        cos_queue: int | None = ...,
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
    "TrafficPolicy",
    "TrafficPolicyDictMode",
    "TrafficPolicyObjectMode",
    "TrafficPolicyPayload",
    "TrafficPolicyObject",
]