from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class LabelPayload(TypedDict, total=False):
    """
    Type hints for dlp/label payload fields.
    
    Configure labels used by DLP blocking.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.sdn-connector.SdnConnectorEndpoint` (via: connector)

    **Usage:**
        payload: LabelPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name of table containing the label. | MaxLen: 35
    type: Literal["mpip", "fortidata"]  # Label type. | Default: mpip
    mpip_type: Literal["remote", "local"]  # MPIP label type. | Default: remote
    connector: str  # Name of SDN connector. | MaxLen: 35
    comment: str  # Optional comments. | MaxLen: 255
    entries: list[dict[str, Any]]  # DLP label entries.

# Nested TypedDicts for table field children (dict mode)

class LabelEntriesItem(TypedDict):
    """Type hints for entries table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # ID. | Default: 0 | Min: 1 | Max: 32
    fortidata_label_name: str  # Name of FortiData label | MaxLen: 127
    mpip_label_name: str  # Name of MPIP label. | MaxLen: 127
    guid: str  # MPIP label guid. | MaxLen: 36


# Nested classes for table field children (object mode)

@final
class LabelEntriesObject:
    """Typed object for entries table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # ID. | Default: 0 | Min: 1 | Max: 32
    id: int
    # Name of FortiData label | MaxLen: 127
    fortidata_label_name: str
    # Name of MPIP label. | MaxLen: 127
    mpip_label_name: str
    # MPIP label guid. | MaxLen: 36
    guid: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class LabelResponse(TypedDict):
    """
    Type hints for dlp/label API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name of table containing the label. | MaxLen: 35
    type: Literal["mpip", "fortidata"]  # Label type. | Default: mpip
    mpip_type: Literal["remote", "local"]  # MPIP label type. | Default: remote
    connector: str  # Name of SDN connector. | MaxLen: 35
    comment: str  # Optional comments. | MaxLen: 255
    entries: list[LabelEntriesItem]  # DLP label entries.


@final
class LabelObject:
    """Typed FortiObject for dlp/label with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name of table containing the label. | MaxLen: 35
    name: str
    # Label type. | Default: mpip
    type: Literal["mpip", "fortidata"]
    # MPIP label type. | Default: remote
    mpip_type: Literal["remote", "local"]
    # Name of SDN connector. | MaxLen: 35
    connector: str
    # Optional comments. | MaxLen: 255
    comment: str
    # DLP label entries.
    entries: list[LabelEntriesObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> LabelPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Label:
    """
    Configure labels used by DLP blocking.
    
    Path: dlp/label
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
    ) -> LabelResponse: ...
    
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
    ) -> LabelResponse: ...
    
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
    ) -> list[LabelResponse]: ...
    
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
    ) -> LabelObject: ...
    
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
    ) -> LabelObject: ...
    
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
    ) -> list[LabelObject]: ...
    
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
    ) -> LabelResponse: ...
    
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
    ) -> LabelResponse: ...
    
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
    ) -> list[LabelResponse]: ...
    
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
    ) -> LabelObject | list[LabelObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LabelObject: ...
    
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LabelObject: ...
    
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> LabelObject: ...
    
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
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
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

class LabelDictMode:
    """Label endpoint for dict response mode (default for this client).
    
    By default returns LabelResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return LabelObject.
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
    ) -> LabelObject: ...
    
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
    ) -> list[LabelObject]: ...
    
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
    ) -> LabelResponse: ...
    
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
    ) -> list[LabelResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LabelObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LabelObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> LabelObject: ...
    
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
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
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


class LabelObjectMode:
    """Label endpoint for object response mode (default for this client).
    
    By default returns LabelObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return LabelResponse (TypedDict).
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
    ) -> LabelResponse: ...
    
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
    ) -> list[LabelResponse]: ...
    
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
    ) -> LabelObject: ...
    
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
    ) -> list[LabelObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LabelObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LabelObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LabelObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LabelObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> LabelObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LabelObject: ...
    
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
        payload_dict: LabelPayload | None = ...,
        name: str | None = ...,
        type: Literal["mpip", "fortidata"] | None = ...,
        mpip_type: Literal["remote", "local"] | None = ...,
        connector: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "Label",
    "LabelDictMode",
    "LabelObjectMode",
    "LabelPayload",
    "LabelObject",
]