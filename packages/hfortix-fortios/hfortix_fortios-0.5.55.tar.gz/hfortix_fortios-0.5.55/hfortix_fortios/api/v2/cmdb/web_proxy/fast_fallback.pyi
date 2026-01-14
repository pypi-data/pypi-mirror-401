from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class FastFallbackPayload(TypedDict, total=False):
    """
    Type hints for web_proxy/fast_fallback payload fields.
    
    Proxy destination connection fast-fallback.
    
    **Usage:**
        payload: FastFallbackPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Configure a name for the fast-fallback entry. | MaxLen: 63
    status: Literal["enable", "disable"]  # Enable/disable the fast-fallback entry. | Default: enable
    connection_mode: Literal["sequentially", "simultaneously"]  # Connection mode for multiple destinations. | Default: sequentially
    protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"]  # Connection protocols for multiple destinations. | Default: IPv4-first
    connection_timeout: int  # Number of milliseconds to wait before starting ano | Default: 200 | Min: 200 | Max: 1800000

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class FastFallbackResponse(TypedDict):
    """
    Type hints for web_proxy/fast_fallback API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Configure a name for the fast-fallback entry. | MaxLen: 63
    status: Literal["enable", "disable"]  # Enable/disable the fast-fallback entry. | Default: enable
    connection_mode: Literal["sequentially", "simultaneously"]  # Connection mode for multiple destinations. | Default: sequentially
    protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"]  # Connection protocols for multiple destinations. | Default: IPv4-first
    connection_timeout: int  # Number of milliseconds to wait before starting ano | Default: 200 | Min: 200 | Max: 1800000


@final
class FastFallbackObject:
    """Typed FortiObject for web_proxy/fast_fallback with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Configure a name for the fast-fallback entry. | MaxLen: 63
    name: str
    # Enable/disable the fast-fallback entry. | Default: enable
    status: Literal["enable", "disable"]
    # Connection mode for multiple destinations. | Default: sequentially
    connection_mode: Literal["sequentially", "simultaneously"]
    # Connection protocols for multiple destinations. | Default: IPv4-first
    protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"]
    # Number of milliseconds to wait before starting another conne | Default: 200 | Min: 200 | Max: 1800000
    connection_timeout: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> FastFallbackPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class FastFallback:
    """
    Proxy destination connection fast-fallback.
    
    Path: web_proxy/fast_fallback
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
    ) -> FastFallbackResponse: ...
    
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
    ) -> FastFallbackResponse: ...
    
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
    ) -> list[FastFallbackResponse]: ...
    
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
    ) -> FastFallbackObject: ...
    
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
    ) -> FastFallbackObject: ...
    
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
    ) -> list[FastFallbackObject]: ...
    
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
    ) -> FastFallbackResponse: ...
    
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
    ) -> FastFallbackResponse: ...
    
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
    ) -> list[FastFallbackResponse]: ...
    
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
    ) -> FastFallbackObject | list[FastFallbackObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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
    ) -> FastFallbackObject: ...
    
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
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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

class FastFallbackDictMode:
    """FastFallback endpoint for dict response mode (default for this client).
    
    By default returns FastFallbackResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return FastFallbackObject.
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
    ) -> FastFallbackObject: ...
    
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
    ) -> list[FastFallbackObject]: ...
    
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
    ) -> FastFallbackResponse: ...
    
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
    ) -> list[FastFallbackResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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
    ) -> FastFallbackObject: ...
    
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
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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


class FastFallbackObjectMode:
    """FastFallback endpoint for object response mode (default for this client).
    
    By default returns FastFallbackObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return FastFallbackResponse (TypedDict).
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
    ) -> FastFallbackResponse: ...
    
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
    ) -> list[FastFallbackResponse]: ...
    
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
    ) -> FastFallbackObject: ...
    
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
    ) -> list[FastFallbackObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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
    ) -> FastFallbackObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FastFallbackObject: ...
    
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
        payload_dict: FastFallbackPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        connection_mode: Literal["sequentially", "simultaneously"] | None = ...,
        protocol: Literal["IPv4-first", "IPv6-first", "IPv4-only", "IPv6-only"] | None = ...,
        connection_timeout: int | None = ...,
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
    "FastFallback",
    "FastFallbackDictMode",
    "FastFallbackObjectMode",
    "FastFallbackPayload",
    "FastFallbackObject",
]