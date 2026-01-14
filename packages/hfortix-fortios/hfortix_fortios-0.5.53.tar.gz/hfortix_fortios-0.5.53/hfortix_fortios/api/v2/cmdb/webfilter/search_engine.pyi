from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SearchEnginePayload(TypedDict, total=False):
    """
    Type hints for webfilter/search_engine payload fields.
    
    Configure web filter search engines.
    
    **Usage:**
        payload: SearchEnginePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Search engine name. | MaxLen: 35
    hostname: str  # Hostname (regular expression). | MaxLen: 127
    url: str  # URL (regular expression). | MaxLen: 127
    query: str  # Code used to prefix a query | MaxLen: 15
    safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"]  # Safe search method. You can disable safe search, a | Default: disable
    charset: Literal["utf-8", "gb2312"]  # Search engine charset. | Default: utf-8
    safesearch_str: str  # Safe search parameter used in the URL in URL mode. | MaxLen: 255

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class SearchEngineResponse(TypedDict):
    """
    Type hints for webfilter/search_engine API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Search engine name. | MaxLen: 35
    hostname: str  # Hostname (regular expression). | MaxLen: 127
    url: str  # URL (regular expression). | MaxLen: 127
    query: str  # Code used to prefix a query | MaxLen: 15
    safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"]  # Safe search method. You can disable safe search, a | Default: disable
    charset: Literal["utf-8", "gb2312"]  # Search engine charset. | Default: utf-8
    safesearch_str: str  # Safe search parameter used in the URL in URL mode. | MaxLen: 255


@final
class SearchEngineObject:
    """Typed FortiObject for webfilter/search_engine with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Search engine name. | MaxLen: 35
    name: str
    # Hostname (regular expression). | MaxLen: 127
    hostname: str
    # URL (regular expression). | MaxLen: 127
    url: str
    # Code used to prefix a query | MaxLen: 15
    query: str
    # Safe search method. You can disable safe search, add the saf | Default: disable
    safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"]
    # Search engine charset. | Default: utf-8
    charset: Literal["utf-8", "gb2312"]
    # Safe search parameter used in the URL in URL mode. In transl | MaxLen: 255
    safesearch_str: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SearchEnginePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class SearchEngine:
    """
    Configure web filter search engines.
    
    Path: webfilter/search_engine
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
    ) -> SearchEngineResponse: ...
    
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
    ) -> SearchEngineResponse: ...
    
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
    ) -> list[SearchEngineResponse]: ...
    
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
    ) -> SearchEngineObject: ...
    
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
    ) -> SearchEngineObject: ...
    
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
    ) -> list[SearchEngineObject]: ...
    
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
    ) -> SearchEngineResponse: ...
    
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
    ) -> SearchEngineResponse: ...
    
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
    ) -> list[SearchEngineResponse]: ...
    
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
    ) -> SearchEngineObject | list[SearchEngineObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
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
    ) -> SearchEngineObject: ...
    
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
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
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

class SearchEngineDictMode:
    """SearchEngine endpoint for dict response mode (default for this client).
    
    By default returns SearchEngineResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SearchEngineObject.
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
    ) -> SearchEngineObject: ...
    
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
    ) -> list[SearchEngineObject]: ...
    
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
    ) -> SearchEngineResponse: ...
    
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
    ) -> list[SearchEngineResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
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
    ) -> SearchEngineObject: ...
    
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
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
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


class SearchEngineObjectMode:
    """SearchEngine endpoint for object response mode (default for this client).
    
    By default returns SearchEngineObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SearchEngineResponse (TypedDict).
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
    ) -> SearchEngineResponse: ...
    
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
    ) -> list[SearchEngineResponse]: ...
    
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
    ) -> SearchEngineObject: ...
    
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
    ) -> list[SearchEngineObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
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
    ) -> SearchEngineObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SearchEngineObject: ...
    
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
        payload_dict: SearchEnginePayload | None = ...,
        name: str | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        query: str | None = ...,
        safesearch: Literal["disable", "url", "header", "translate", "yt-pattern", "yt-scan", "yt-video", "yt-channel"] | None = ...,
        charset: Literal["utf-8", "gb2312"] | None = ...,
        safesearch_str: str | None = ...,
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
    "SearchEngine",
    "SearchEngineDictMode",
    "SearchEngineObjectMode",
    "SearchEnginePayload",
    "SearchEngineObject",
]