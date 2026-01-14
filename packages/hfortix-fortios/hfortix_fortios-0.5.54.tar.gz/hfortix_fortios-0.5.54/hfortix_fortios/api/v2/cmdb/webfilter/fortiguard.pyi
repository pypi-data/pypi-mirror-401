from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class FortiguardPayload(TypedDict, total=False):
    """
    Type hints for webfilter/fortiguard payload fields.
    
    Configure FortiGuard Web Filter service.
    
    **Usage:**
        payload: FortiguardPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    cache_mode: Literal["ttl", "db-ver"]  # Cache entry expiration mode. | Default: ttl
    cache_prefix_match: Literal["enable", "disable"]  # Enable/disable prefix matching in the cache. | Default: enable
    cache_mem_permille: int  # Maximum permille of available memory allocated to | Default: 1 | Min: 1 | Max: 150
    ovrd_auth_port_http: int  # Port to use for FortiGuard Web Filter HTTP overrid | Default: 8008 | Min: 0 | Max: 65535
    ovrd_auth_port_https: int  # Port to use for FortiGuard Web Filter HTTPS overri | Default: 8010 | Min: 0 | Max: 65535
    ovrd_auth_port_https_flow: int  # Port to use for FortiGuard Web Filter HTTPS overri | Default: 8015 | Min: 0 | Max: 65535
    ovrd_auth_port_warning: int  # Port to use for FortiGuard Web Filter Warning over | Default: 8020 | Min: 0 | Max: 65535
    ovrd_auth_https: Literal["enable", "disable"]  # Enable/disable use of HTTPS for override authentic | Default: enable
    warn_auth_https: Literal["enable", "disable"]  # Enable/disable use of HTTPS for warning and authen | Default: enable
    close_ports: Literal["enable", "disable"]  # Close ports used for HTTP/HTTPS override authentic | Default: disable
    request_packet_size_limit: int  # Limit size of URL request packets sent to FortiGua | Default: 0 | Min: 576 | Max: 10000
    embed_image: Literal["enable", "disable"]  # Enable/disable embedding images into replacement m | Default: enable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class FortiguardResponse(TypedDict):
    """
    Type hints for webfilter/fortiguard API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    cache_mode: Literal["ttl", "db-ver"]  # Cache entry expiration mode. | Default: ttl
    cache_prefix_match: Literal["enable", "disable"]  # Enable/disable prefix matching in the cache. | Default: enable
    cache_mem_permille: int  # Maximum permille of available memory allocated to | Default: 1 | Min: 1 | Max: 150
    ovrd_auth_port_http: int  # Port to use for FortiGuard Web Filter HTTP overrid | Default: 8008 | Min: 0 | Max: 65535
    ovrd_auth_port_https: int  # Port to use for FortiGuard Web Filter HTTPS overri | Default: 8010 | Min: 0 | Max: 65535
    ovrd_auth_port_https_flow: int  # Port to use for FortiGuard Web Filter HTTPS overri | Default: 8015 | Min: 0 | Max: 65535
    ovrd_auth_port_warning: int  # Port to use for FortiGuard Web Filter Warning over | Default: 8020 | Min: 0 | Max: 65535
    ovrd_auth_https: Literal["enable", "disable"]  # Enable/disable use of HTTPS for override authentic | Default: enable
    warn_auth_https: Literal["enable", "disable"]  # Enable/disable use of HTTPS for warning and authen | Default: enable
    close_ports: Literal["enable", "disable"]  # Close ports used for HTTP/HTTPS override authentic | Default: disable
    request_packet_size_limit: int  # Limit size of URL request packets sent to FortiGua | Default: 0 | Min: 576 | Max: 10000
    embed_image: Literal["enable", "disable"]  # Enable/disable embedding images into replacement m | Default: enable


@final
class FortiguardObject:
    """Typed FortiObject for webfilter/fortiguard with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Cache entry expiration mode. | Default: ttl
    cache_mode: Literal["ttl", "db-ver"]
    # Enable/disable prefix matching in the cache. | Default: enable
    cache_prefix_match: Literal["enable", "disable"]
    # Maximum permille of available memory allocated to caching | Default: 1 | Min: 1 | Max: 150
    cache_mem_permille: int
    # Port to use for FortiGuard Web Filter HTTP override authenti | Default: 8008 | Min: 0 | Max: 65535
    ovrd_auth_port_http: int
    # Port to use for FortiGuard Web Filter HTTPS override authent | Default: 8010 | Min: 0 | Max: 65535
    ovrd_auth_port_https: int
    # Port to use for FortiGuard Web Filter HTTPS override authent | Default: 8015 | Min: 0 | Max: 65535
    ovrd_auth_port_https_flow: int
    # Port to use for FortiGuard Web Filter Warning override authe | Default: 8020 | Min: 0 | Max: 65535
    ovrd_auth_port_warning: int
    # Enable/disable use of HTTPS for override authentication. | Default: enable
    ovrd_auth_https: Literal["enable", "disable"]
    # Enable/disable use of HTTPS for warning and authentication. | Default: enable
    warn_auth_https: Literal["enable", "disable"]
    # Close ports used for HTTP/HTTPS override authentication and | Default: disable
    close_ports: Literal["enable", "disable"]
    # Limit size of URL request packets sent to FortiGuard server | Default: 0 | Min: 576 | Max: 10000
    request_packet_size_limit: int
    # Enable/disable embedding images into replacement messages | Default: enable
    embed_image: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> FortiguardPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Fortiguard:
    """
    Configure FortiGuard Web Filter service.
    
    Path: webfilter/fortiguard
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardObject: ...
    
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
    ) -> FortiguardObject: ...
    
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
    ) -> FortiguardObject: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortiguardObject: ...
    
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
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
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
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

class FortiguardDictMode:
    """Fortiguard endpoint for dict response mode (default for this client).
    
    By default returns FortiguardResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return FortiguardObject.
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
    ) -> FortiguardObject: ...
    
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
    ) -> FortiguardObject: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortiguardObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
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
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
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


class FortiguardObjectMode:
    """Fortiguard endpoint for object response mode (default for this client).
    
    By default returns FortiguardObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return FortiguardResponse (TypedDict).
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardResponse: ...
    
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
    ) -> FortiguardObject: ...
    
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
    ) -> FortiguardObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortiguardObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiguardObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
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
        payload_dict: FortiguardPayload | None = ...,
        cache_mode: Literal["ttl", "db-ver"] | None = ...,
        cache_prefix_match: Literal["enable", "disable"] | None = ...,
        cache_mem_permille: int | None = ...,
        ovrd_auth_port_http: int | None = ...,
        ovrd_auth_port_https: int | None = ...,
        ovrd_auth_port_https_flow: int | None = ...,
        ovrd_auth_port_warning: int | None = ...,
        ovrd_auth_https: Literal["enable", "disable"] | None = ...,
        warn_auth_https: Literal["enable", "disable"] | None = ...,
        close_ports: Literal["enable", "disable"] | None = ...,
        request_packet_size_limit: int | None = ...,
        embed_image: Literal["enable", "disable"] | None = ...,
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
    "Fortiguard",
    "FortiguardDictMode",
    "FortiguardObjectMode",
    "FortiguardPayload",
    "FortiguardObject",
]