from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ProxyAddressPayload(TypedDict, total=False):
    """
    Type hints for firewall/proxy_address payload fields.
    
    Configure web proxy address.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.firewall.address.AddressEndpoint` (via: host)
        - :class:`~.firewall.addrgrp.AddrgrpEndpoint` (via: host)
        - :class:`~.firewall.proxy-address.ProxyAddressEndpoint` (via: host)
        - :class:`~.firewall.vip.VipEndpoint` (via: host)
        - :class:`~.firewall.vipgrp.VipgrpEndpoint` (via: host)

    **Usage:**
        payload: ProxyAddressPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Address name. | MaxLen: 79
    uuid: str  # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]  # Proxy address type. | Default: url
    host: str  # Address object for the host. | MaxLen: 79
    host_regex: str  # Host name as a regular expression. | MaxLen: 255
    path: str  # URL path as a regular expression. | MaxLen: 255
    query: str  # Match the query part of the URL as a regular expre | MaxLen: 255
    referrer: Literal["enable", "disable"]  # Enable/disable use of referrer field in the HTTP h | Default: disable
    category: list[dict[str, Any]]  # FortiGuard category ID.
    method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"]  # HTTP request methods to be used.
    ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"]  # Names of browsers to be used as user agent.
    ua_min_ver: str  # Minimum version of the user agent specified in dot | MaxLen: 63
    ua_max_ver: str  # Maximum version of the user agent specified in dot | MaxLen: 63
    header_name: str  # Name of HTTP header. | MaxLen: 79
    header: str  # HTTP header name as a regular expression. | MaxLen: 255
    case_sensitivity: Literal["disable", "enable"]  # Enable to make the pattern case sensitive. | Default: disable
    header_group: list[dict[str, Any]]  # HTTP header group.
    color: int  # Integer value to determine the color of the icon i | Default: 0 | Min: 0 | Max: 32
    tagging: list[dict[str, Any]]  # Config object tagging.
    comment: str  # Optional comments. | MaxLen: 255
    application: list[dict[str, Any]]  # SaaS application.

# Nested TypedDicts for table field children (dict mode)

class ProxyAddressCategoryItem(TypedDict):
    """Type hints for category table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # FortiGuard category ID. | Default: 0 | Min: 0 | Max: 4294967295


class ProxyAddressHeadergroupItem(TypedDict):
    """Type hints for header-group table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # ID. | Default: 0 | Min: 0 | Max: 4294967295
    header_name: str  # HTTP header. | MaxLen: 79
    header: str  # HTTP header regular expression. | MaxLen: 255
    case_sensitivity: Literal["disable", "enable"]  # Case sensitivity in pattern. | Default: disable


class ProxyAddressTaggingItem(TypedDict):
    """Type hints for tagging table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Tagging entry name. | MaxLen: 63
    category: str  # Tag category. | MaxLen: 63
    tags: str  # Tags.


class ProxyAddressApplicationItem(TypedDict):
    """Type hints for application table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # SaaS application name. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class ProxyAddressCategoryObject:
    """Typed object for category table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # FortiGuard category ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class ProxyAddressHeadergroupObject:
    """Typed object for header-group table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # HTTP header. | MaxLen: 79
    header_name: str
    # HTTP header regular expression. | MaxLen: 255
    header: str
    # Case sensitivity in pattern. | Default: disable
    case_sensitivity: Literal["disable", "enable"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class ProxyAddressTaggingObject:
    """Typed object for tagging table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Tagging entry name. | MaxLen: 63
    name: str
    # Tag category. | MaxLen: 63
    category: str
    # Tags.
    tags: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class ProxyAddressApplicationObject:
    """Typed object for application table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # SaaS application name. | MaxLen: 79
    name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class ProxyAddressResponse(TypedDict):
    """
    Type hints for firewall/proxy_address API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Address name. | MaxLen: 79
    uuid: str  # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]  # Proxy address type. | Default: url
    host: str  # Address object for the host. | MaxLen: 79
    host_regex: str  # Host name as a regular expression. | MaxLen: 255
    path: str  # URL path as a regular expression. | MaxLen: 255
    query: str  # Match the query part of the URL as a regular expre | MaxLen: 255
    referrer: Literal["enable", "disable"]  # Enable/disable use of referrer field in the HTTP h | Default: disable
    category: list[ProxyAddressCategoryItem]  # FortiGuard category ID.
    method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"]  # HTTP request methods to be used.
    ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"]  # Names of browsers to be used as user agent.
    ua_min_ver: str  # Minimum version of the user agent specified in dot | MaxLen: 63
    ua_max_ver: str  # Maximum version of the user agent specified in dot | MaxLen: 63
    header_name: str  # Name of HTTP header. | MaxLen: 79
    header: str  # HTTP header name as a regular expression. | MaxLen: 255
    case_sensitivity: Literal["disable", "enable"]  # Enable to make the pattern case sensitive. | Default: disable
    header_group: list[ProxyAddressHeadergroupItem]  # HTTP header group.
    color: int  # Integer value to determine the color of the icon i | Default: 0 | Min: 0 | Max: 32
    tagging: list[ProxyAddressTaggingItem]  # Config object tagging.
    comment: str  # Optional comments. | MaxLen: 255
    application: list[ProxyAddressApplicationItem]  # SaaS application.


@final
class ProxyAddressObject:
    """Typed FortiObject for firewall/proxy_address with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Address name. | MaxLen: 79
    name: str
    # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    uuid: str
    # Proxy address type. | Default: url
    type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]
    # Address object for the host. | MaxLen: 79
    host: str
    # Host name as a regular expression. | MaxLen: 255
    host_regex: str
    # URL path as a regular expression. | MaxLen: 255
    path: str
    # Match the query part of the URL as a regular expression. | MaxLen: 255
    query: str
    # Enable/disable use of referrer field in the HTTP header to m | Default: disable
    referrer: Literal["enable", "disable"]
    # FortiGuard category ID.
    category: list[ProxyAddressCategoryObject]
    # HTTP request methods to be used.
    method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"]
    # Names of browsers to be used as user agent.
    ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"]
    # Minimum version of the user agent specified in dotted notati | MaxLen: 63
    ua_min_ver: str
    # Maximum version of the user agent specified in dotted notati | MaxLen: 63
    ua_max_ver: str
    # Name of HTTP header. | MaxLen: 79
    header_name: str
    # HTTP header name as a regular expression. | MaxLen: 255
    header: str
    # Enable to make the pattern case sensitive. | Default: disable
    case_sensitivity: Literal["disable", "enable"]
    # HTTP header group.
    header_group: list[ProxyAddressHeadergroupObject]
    # Integer value to determine the color of the icon in the GUI | Default: 0 | Min: 0 | Max: 32
    color: int
    # Config object tagging.
    tagging: list[ProxyAddressTaggingObject]
    # Optional comments. | MaxLen: 255
    comment: str
    # SaaS application.
    application: list[ProxyAddressApplicationObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ProxyAddressPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class ProxyAddress:
    """
    Configure web proxy address.
    
    Path: firewall/proxy_address
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
    ) -> ProxyAddressResponse: ...
    
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
    ) -> ProxyAddressResponse: ...
    
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
    ) -> list[ProxyAddressResponse]: ...
    
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
    ) -> ProxyAddressObject: ...
    
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
    ) -> ProxyAddressObject: ...
    
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
    ) -> list[ProxyAddressObject]: ...
    
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
    ) -> ProxyAddressResponse: ...
    
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
    ) -> ProxyAddressResponse: ...
    
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
    ) -> list[ProxyAddressResponse]: ...
    
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
    ) -> ProxyAddressObject | list[ProxyAddressObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ProxyAddressObject: ...
    
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
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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

class ProxyAddressDictMode:
    """ProxyAddress endpoint for dict response mode (default for this client).
    
    By default returns ProxyAddressResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ProxyAddressObject.
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
    ) -> ProxyAddressObject: ...
    
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
    ) -> list[ProxyAddressObject]: ...
    
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
    ) -> ProxyAddressResponse: ...
    
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
    ) -> list[ProxyAddressResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ProxyAddressObject: ...
    
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
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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


class ProxyAddressObjectMode:
    """ProxyAddress endpoint for object response mode (default for this client).
    
    By default returns ProxyAddressObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ProxyAddressResponse (TypedDict).
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
    ) -> ProxyAddressResponse: ...
    
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
    ) -> list[ProxyAddressResponse]: ...
    
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
    ) -> ProxyAddressObject: ...
    
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
    ) -> list[ProxyAddressObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ProxyAddressObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProxyAddressObject: ...
    
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
        payload_dict: ProxyAddressPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        type: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"] | None = ...,
        host: str | None = ...,
        host_regex: str | None = ...,
        path: str | None = ...,
        query: str | None = ...,
        referrer: Literal["enable", "disable"] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        method: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"] | list[str] | None = ...,
        ua: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"] | list[str] | None = ...,
        ua_min_ver: str | None = ...,
        ua_max_ver: str | None = ...,
        header_name: str | None = ...,
        header: str | None = ...,
        case_sensitivity: Literal["disable", "enable"] | None = ...,
        header_group: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "ProxyAddress",
    "ProxyAddressDictMode",
    "ProxyAddressObjectMode",
    "ProxyAddressPayload",
    "ProxyAddressObject",
]