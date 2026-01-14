from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ForwardServerGroupPayload(TypedDict, total=False):
    """
    Type hints for web_proxy/forward_server_group payload fields.
    
    Configure a forward server group consisting or multiple forward servers. Supports failover and load balancing.
    
    **Usage:**
        payload: ForwardServerGroupPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Configure a forward server group consisting one or | MaxLen: 63
    affinity: Literal["enable", "disable"]  # Enable/disable affinity, attaching a source-ip's t | Default: enable
    ldb_method: Literal["weighted", "least-session", "active-passive"]  # Load balance method: weighted or least-session. | Default: weighted
    group_down_option: Literal["block", "pass"]  # Action to take when all of the servers in the forw | Default: block
    server_list: list[dict[str, Any]]  # Add web forward servers to a list to form a server

# Nested TypedDicts for table field children (dict mode)

class ForwardServerGroupServerlistItem(TypedDict):
    """Type hints for server-list table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Forward server name. | MaxLen: 63
    weight: int  # Optionally assign a weight of the forwarding serve | Default: 10 | Min: 1 | Max: 100


# Nested classes for table field children (object mode)

@final
class ForwardServerGroupServerlistObject:
    """Typed object for server-list table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Forward server name. | MaxLen: 63
    name: str
    # Optionally assign a weight of the forwarding server for weig | Default: 10 | Min: 1 | Max: 100
    weight: int
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class ForwardServerGroupResponse(TypedDict):
    """
    Type hints for web_proxy/forward_server_group API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Configure a forward server group consisting one or | MaxLen: 63
    affinity: Literal["enable", "disable"]  # Enable/disable affinity, attaching a source-ip's t | Default: enable
    ldb_method: Literal["weighted", "least-session", "active-passive"]  # Load balance method: weighted or least-session. | Default: weighted
    group_down_option: Literal["block", "pass"]  # Action to take when all of the servers in the forw | Default: block
    server_list: list[ForwardServerGroupServerlistItem]  # Add web forward servers to a list to form a server


@final
class ForwardServerGroupObject:
    """Typed FortiObject for web_proxy/forward_server_group with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Configure a forward server group consisting one or multiple | MaxLen: 63
    name: str
    # Enable/disable affinity, attaching a source-ip's traffic to | Default: enable
    affinity: Literal["enable", "disable"]
    # Load balance method: weighted or least-session. | Default: weighted
    ldb_method: Literal["weighted", "least-session", "active-passive"]
    # Action to take when all of the servers in the forward server | Default: block
    group_down_option: Literal["block", "pass"]
    # Add web forward servers to a list to form a server group. Op
    server_list: list[ForwardServerGroupServerlistObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ForwardServerGroupPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class ForwardServerGroup:
    """
    Configure a forward server group consisting or multiple forward servers. Supports failover and load balancing.
    
    Path: web_proxy/forward_server_group
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
    ) -> ForwardServerGroupResponse: ...
    
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
    ) -> ForwardServerGroupResponse: ...
    
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
    ) -> list[ForwardServerGroupResponse]: ...
    
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
    ) -> ForwardServerGroupObject: ...
    
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
    ) -> ForwardServerGroupObject: ...
    
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
    ) -> list[ForwardServerGroupObject]: ...
    
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
    ) -> ForwardServerGroupResponse: ...
    
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
    ) -> ForwardServerGroupResponse: ...
    
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
    ) -> list[ForwardServerGroupResponse]: ...
    
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
    ) -> ForwardServerGroupObject | list[ForwardServerGroupObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ForwardServerGroupObject: ...
    
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
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
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

class ForwardServerGroupDictMode:
    """ForwardServerGroup endpoint for dict response mode (default for this client).
    
    By default returns ForwardServerGroupResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ForwardServerGroupObject.
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
    ) -> ForwardServerGroupObject: ...
    
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
    ) -> list[ForwardServerGroupObject]: ...
    
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
    ) -> ForwardServerGroupResponse: ...
    
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
    ) -> list[ForwardServerGroupResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ForwardServerGroupObject: ...
    
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
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
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


class ForwardServerGroupObjectMode:
    """ForwardServerGroup endpoint for object response mode (default for this client).
    
    By default returns ForwardServerGroupObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ForwardServerGroupResponse (TypedDict).
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
    ) -> ForwardServerGroupResponse: ...
    
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
    ) -> list[ForwardServerGroupResponse]: ...
    
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
    ) -> ForwardServerGroupObject: ...
    
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
    ) -> list[ForwardServerGroupObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ForwardServerGroupObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ForwardServerGroupObject: ...
    
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
        payload_dict: ForwardServerGroupPayload | None = ...,
        name: str | None = ...,
        affinity: Literal["enable", "disable"] | None = ...,
        ldb_method: Literal["weighted", "least-session", "active-passive"] | None = ...,
        group_down_option: Literal["block", "pass"] | None = ...,
        server_list: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "ForwardServerGroup",
    "ForwardServerGroupDictMode",
    "ForwardServerGroupObjectMode",
    "ForwardServerGroupPayload",
    "ForwardServerGroupObject",
]