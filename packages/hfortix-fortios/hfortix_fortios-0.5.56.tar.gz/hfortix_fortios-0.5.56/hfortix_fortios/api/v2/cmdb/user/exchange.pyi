from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ExchangePayload(TypedDict, total=False):
    """
    Type hints for user/exchange payload fields.
    
    Configure MS Exchange server entries.
    
    **Usage:**
        payload: ExchangePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # MS Exchange server entry name. | MaxLen: 35
    server_name: str  # MS Exchange server hostname. | MaxLen: 63
    domain_name: str  # MS Exchange server fully qualified domain name. | MaxLen: 79
    username: str  # User name used to sign in to the server. Must have | MaxLen: 64
    password: str  # Password for the specified username. | MaxLen: 128
    ip: str  # Server IPv4 address. | Default: 0.0.0.0
    connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"]  # Connection protocol used to connect to MS Exchange | Default: rpc-over-https
    validate_server_certificate: Literal["disable", "enable"]  # Enable/disable exchange server certificate validat | Default: disable
    auth_type: Literal["spnego", "ntlm", "kerberos"]  # Authentication security type used for the RPC prot | Default: kerberos
    auth_level: Literal["connect", "call", "packet", "integrity", "privacy"]  # Authentication security level used for the RPC pro | Default: privacy
    http_auth_type: Literal["basic", "ntlm"]  # Authentication security type used for the HTTP tra | Default: ntlm
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]  # Minimum SSL/TLS protocol version for HTTPS transpo | Default: default
    auto_discover_kdc: Literal["enable", "disable"]  # Enable/disable automatic discovery of KDC IP addre | Default: enable
    kdc_ip: list[dict[str, Any]]  # KDC IPv4 addresses for Kerberos authentication.

# Nested TypedDicts for table field children (dict mode)

class ExchangeKdcipItem(TypedDict):
    """Type hints for kdc-ip table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    ipv4: str  # KDC IPv4 addresses for Kerberos authentication. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class ExchangeKdcipObject:
    """Typed object for kdc-ip table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # KDC IPv4 addresses for Kerberos authentication. | MaxLen: 79
    ipv4: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class ExchangeResponse(TypedDict):
    """
    Type hints for user/exchange API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # MS Exchange server entry name. | MaxLen: 35
    server_name: str  # MS Exchange server hostname. | MaxLen: 63
    domain_name: str  # MS Exchange server fully qualified domain name. | MaxLen: 79
    username: str  # User name used to sign in to the server. Must have | MaxLen: 64
    password: str  # Password for the specified username. | MaxLen: 128
    ip: str  # Server IPv4 address. | Default: 0.0.0.0
    connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"]  # Connection protocol used to connect to MS Exchange | Default: rpc-over-https
    validate_server_certificate: Literal["disable", "enable"]  # Enable/disable exchange server certificate validat | Default: disable
    auth_type: Literal["spnego", "ntlm", "kerberos"]  # Authentication security type used for the RPC prot | Default: kerberos
    auth_level: Literal["connect", "call", "packet", "integrity", "privacy"]  # Authentication security level used for the RPC pro | Default: privacy
    http_auth_type: Literal["basic", "ntlm"]  # Authentication security type used for the HTTP tra | Default: ntlm
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]  # Minimum SSL/TLS protocol version for HTTPS transpo | Default: default
    auto_discover_kdc: Literal["enable", "disable"]  # Enable/disable automatic discovery of KDC IP addre | Default: enable
    kdc_ip: list[ExchangeKdcipItem]  # KDC IPv4 addresses for Kerberos authentication.


@final
class ExchangeObject:
    """Typed FortiObject for user/exchange with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # MS Exchange server entry name. | MaxLen: 35
    name: str
    # MS Exchange server hostname. | MaxLen: 63
    server_name: str
    # MS Exchange server fully qualified domain name. | MaxLen: 79
    domain_name: str
    # User name used to sign in to the server. Must have proper pe | MaxLen: 64
    username: str
    # Password for the specified username. | MaxLen: 128
    password: str
    # Server IPv4 address. | Default: 0.0.0.0
    ip: str
    # Connection protocol used to connect to MS Exchange service. | Default: rpc-over-https
    connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"]
    # Enable/disable exchange server certificate validation. | Default: disable
    validate_server_certificate: Literal["disable", "enable"]
    # Authentication security type used for the RPC protocol layer | Default: kerberos
    auth_type: Literal["spnego", "ntlm", "kerberos"]
    # Authentication security level used for the RPC protocol laye | Default: privacy
    auth_level: Literal["connect", "call", "packet", "integrity", "privacy"]
    # Authentication security type used for the HTTP transport. | Default: ntlm
    http_auth_type: Literal["basic", "ntlm"]
    # Minimum SSL/TLS protocol version for HTTPS transport | Default: default
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    # Enable/disable automatic discovery of KDC IP addresses. | Default: enable
    auto_discover_kdc: Literal["enable", "disable"]
    # KDC IPv4 addresses for Kerberos authentication.
    kdc_ip: list[ExchangeKdcipObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ExchangePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Exchange:
    """
    Configure MS Exchange server entries.
    
    Path: user/exchange
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
    ) -> ExchangeResponse: ...
    
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
    ) -> ExchangeResponse: ...
    
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
    ) -> list[ExchangeResponse]: ...
    
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
    ) -> ExchangeObject: ...
    
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
    ) -> ExchangeObject: ...
    
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
    ) -> list[ExchangeObject]: ...
    
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
    ) -> ExchangeResponse: ...
    
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
    ) -> ExchangeResponse: ...
    
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
    ) -> list[ExchangeResponse]: ...
    
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
    ) -> ExchangeObject | list[ExchangeObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ExchangeObject: ...
    
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
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
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

class ExchangeDictMode:
    """Exchange endpoint for dict response mode (default for this client).
    
    By default returns ExchangeResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ExchangeObject.
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
    ) -> ExchangeObject: ...
    
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
    ) -> list[ExchangeObject]: ...
    
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
    ) -> ExchangeResponse: ...
    
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
    ) -> list[ExchangeResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ExchangeObject: ...
    
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
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
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


class ExchangeObjectMode:
    """Exchange endpoint for object response mode (default for this client).
    
    By default returns ExchangeObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ExchangeResponse (TypedDict).
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
    ) -> ExchangeResponse: ...
    
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
    ) -> list[ExchangeResponse]: ...
    
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
    ) -> ExchangeObject: ...
    
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
    ) -> list[ExchangeObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> ExchangeObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ExchangeObject: ...
    
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
        payload_dict: ExchangePayload | None = ...,
        name: str | None = ...,
        server_name: str | None = ...,
        domain_name: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        ip: str | None = ...,
        connect_protocol: Literal["rpc-over-tcp", "rpc-over-http", "rpc-over-https"] | None = ...,
        validate_server_certificate: Literal["disable", "enable"] | None = ...,
        auth_type: Literal["spnego", "ntlm", "kerberos"] | None = ...,
        auth_level: Literal["connect", "call", "packet", "integrity", "privacy"] | None = ...,
        http_auth_type: Literal["basic", "ntlm"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        auto_discover_kdc: Literal["enable", "disable"] | None = ...,
        kdc_ip: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "Exchange",
    "ExchangeDictMode",
    "ExchangeObjectMode",
    "ExchangePayload",
    "ExchangeObject",
]