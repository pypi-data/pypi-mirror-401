from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ProfilePayload(TypedDict, total=False):
    """
    Type hints for web_proxy/profile payload fields.
    
    Configure web proxy profiles.
    
    **Usage:**
        payload: ProfilePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Profile name. | MaxLen: 63
    header_client_ip: Literal["pass", "add", "remove"]  # Action to take on the HTTP client-IP header in for | Default: pass
    header_via_request: Literal["pass", "add", "remove"]  # Action to take on the HTTP via header in forwarded | Default: pass
    header_via_response: Literal["pass", "add", "remove"]  # Action to take on the HTTP via header in forwarded | Default: pass
    header_client_cert: Literal["pass", "add", "remove"]  # Action to take on the HTTP Client-Cert/Client-Cert | Default: pass
    header_x_forwarded_for: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-forwarded-for header | Default: pass
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-forwarded-client-cert | Default: pass
    header_front_end_https: Literal["pass", "add", "remove"]  # Action to take on the HTTP front-end-HTTPS header | Default: pass
    header_x_authenticated_user: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-authenticated-user he | Default: pass
    header_x_authenticated_groups: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-authenticated-groups | Default: pass
    strip_encoding: Literal["enable", "disable"]  # Enable/disable stripping unsupported encoding from | Default: disable
    log_header_change: Literal["enable", "disable"]  # Enable/disable logging HTTP header changes. | Default: disable
    headers: list[dict[str, Any]]  # Configure HTTP forwarded requests headers.

# Nested TypedDicts for table field children (dict mode)

class ProfileHeadersItem(TypedDict):
    """Type hints for headers table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # HTTP forwarded header id. | Default: 0 | Min: 0 | Max: 4294967295
    name: str  # HTTP forwarded header name. | MaxLen: 79
    dstaddr: str  # Destination address and address group names.
    dstaddr6: str  # Destination address and address group names (IPv6)
    action: Literal["add-to-request", "add-to-response", "remove-from-request", "remove-from-response", "monitor-request", "monitor-response"]  # Configure adding, removing, or logging of the HTTP | Default: add-to-request
    content: str  # HTTP header content (max length: 3999 characters). | MaxLen: 3999
    base64_encoding: Literal["disable", "enable"]  # Enable/disable use of base64 encoding of HTTP cont | Default: disable
    add_option: Literal["append", "new-on-not-found", "new", "replace", "replace-when-match"]  # Configure options to append content to existing HT | Default: new
    protocol: Literal["https", "http"]  # Configure protocol(s) to take add-option action on | Default: https http


# Nested classes for table field children (object mode)

@final
class ProfileHeadersObject:
    """Typed object for headers table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # HTTP forwarded header id. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # HTTP forwarded header name. | MaxLen: 79
    name: str
    # Destination address and address group names.
    dstaddr: str
    # Destination address and address group names (IPv6).
    dstaddr6: str
    # Configure adding, removing, or logging of the HTTP header en | Default: add-to-request
    action: Literal["add-to-request", "add-to-response", "remove-from-request", "remove-from-response", "monitor-request", "monitor-response"]
    # HTTP header content (max length: 3999 characters). | MaxLen: 3999
    content: str
    # Enable/disable use of base64 encoding of HTTP content. | Default: disable
    base64_encoding: Literal["disable", "enable"]
    # Configure options to append content to existing HTTP header | Default: new
    add_option: Literal["append", "new-on-not-found", "new", "replace", "replace-when-match"]
    # Configure protocol(s) to take add-option action on | Default: https http
    protocol: Literal["https", "http"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class ProfileResponse(TypedDict):
    """
    Type hints for web_proxy/profile API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Profile name. | MaxLen: 63
    header_client_ip: Literal["pass", "add", "remove"]  # Action to take on the HTTP client-IP header in for | Default: pass
    header_via_request: Literal["pass", "add", "remove"]  # Action to take on the HTTP via header in forwarded | Default: pass
    header_via_response: Literal["pass", "add", "remove"]  # Action to take on the HTTP via header in forwarded | Default: pass
    header_client_cert: Literal["pass", "add", "remove"]  # Action to take on the HTTP Client-Cert/Client-Cert | Default: pass
    header_x_forwarded_for: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-forwarded-for header | Default: pass
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-forwarded-client-cert | Default: pass
    header_front_end_https: Literal["pass", "add", "remove"]  # Action to take on the HTTP front-end-HTTPS header | Default: pass
    header_x_authenticated_user: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-authenticated-user he | Default: pass
    header_x_authenticated_groups: Literal["pass", "add", "remove"]  # Action to take on the HTTP x-authenticated-groups | Default: pass
    strip_encoding: Literal["enable", "disable"]  # Enable/disable stripping unsupported encoding from | Default: disable
    log_header_change: Literal["enable", "disable"]  # Enable/disable logging HTTP header changes. | Default: disable
    headers: list[ProfileHeadersItem]  # Configure HTTP forwarded requests headers.


@final
class ProfileObject:
    """Typed FortiObject for web_proxy/profile with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Profile name. | MaxLen: 63
    name: str
    # Action to take on the HTTP client-IP header in forwarded req | Default: pass
    header_client_ip: Literal["pass", "add", "remove"]
    # Action to take on the HTTP via header in forwarded requests: | Default: pass
    header_via_request: Literal["pass", "add", "remove"]
    # Action to take on the HTTP via header in forwarded responses | Default: pass
    header_via_response: Literal["pass", "add", "remove"]
    # Action to take on the HTTP Client-Cert/Client-Cert-Chain hea | Default: pass
    header_client_cert: Literal["pass", "add", "remove"]
    # Action to take on the HTTP x-forwarded-for header in forward | Default: pass
    header_x_forwarded_for: Literal["pass", "add", "remove"]
    # Action to take on the HTTP x-forwarded-client-cert header in | Default: pass
    header_x_forwarded_client_cert: Literal["pass", "add", "remove"]
    # Action to take on the HTTP front-end-HTTPS header in forward | Default: pass
    header_front_end_https: Literal["pass", "add", "remove"]
    # Action to take on the HTTP x-authenticated-user header in fo | Default: pass
    header_x_authenticated_user: Literal["pass", "add", "remove"]
    # Action to take on the HTTP x-authenticated-groups header in | Default: pass
    header_x_authenticated_groups: Literal["pass", "add", "remove"]
    # Enable/disable stripping unsupported encoding from the reque | Default: disable
    strip_encoding: Literal["enable", "disable"]
    # Enable/disable logging HTTP header changes. | Default: disable
    log_header_change: Literal["enable", "disable"]
    # Configure HTTP forwarded requests headers.
    headers: list[ProfileHeadersObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ProfilePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Profile:
    """
    Configure web proxy profiles.
    
    Path: web_proxy/profile
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
    ) -> ProfileResponse: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject | list[ProfileObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
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

class ProfileDictMode:
    """Profile endpoint for dict response mode (default for this client).
    
    By default returns ProfileResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ProfileObject.
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
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


class ProfileObjectMode:
    """Profile endpoint for object response mode (default for this client).
    
    By default returns ProfileObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ProfileResponse (TypedDict).
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ProfileObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        header_client_ip: Literal["pass", "add", "remove"] | None = ...,
        header_via_request: Literal["pass", "add", "remove"] | None = ...,
        header_via_response: Literal["pass", "add", "remove"] | None = ...,
        header_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_for: Literal["pass", "add", "remove"] | None = ...,
        header_x_forwarded_client_cert: Literal["pass", "add", "remove"] | None = ...,
        header_front_end_https: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_user: Literal["pass", "add", "remove"] | None = ...,
        header_x_authenticated_groups: Literal["pass", "add", "remove"] | None = ...,
        strip_encoding: Literal["enable", "disable"] | None = ...,
        log_header_change: Literal["enable", "disable"] | None = ...,
        headers: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "Profile",
    "ProfileDictMode",
    "ProfileObjectMode",
    "ProfilePayload",
    "ProfileObject",
]