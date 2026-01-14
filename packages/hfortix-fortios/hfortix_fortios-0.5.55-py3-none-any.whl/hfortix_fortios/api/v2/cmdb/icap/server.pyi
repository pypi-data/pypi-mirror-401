from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ServerPayload(TypedDict, total=False):
    """
    Type hints for icap/server payload fields.
    
    Configure ICAP servers.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.certificate.ca.CaEndpoint` (via: ssl-cert)

    **Usage:**
        payload: ServerPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Server name. | MaxLen: 63
    addr_type: Literal["ip4", "ip6", "fqdn"]  # Address type of the remote ICAP server: IPv4, IPv6 | Default: ip4
    ip_address: str  # IPv4 address of the ICAP server. | Default: 0.0.0.0
    ip6_address: str  # IPv6 address of the ICAP server. | Default: ::
    fqdn: str  # ICAP remote server Fully Qualified Domain Name | MaxLen: 255
    port: int  # ICAP server port. | Default: 1344 | Min: 1 | Max: 65535
    max_connections: int  # Maximum number of concurrent connections to ICAP s | Default: 100 | Min: 0 | Max: 4294967295
    secure: Literal["disable", "enable"]  # Enable/disable secure connection to ICAP server. | Default: disable
    ssl_cert: str  # CA certificate name. | MaxLen: 79
    healthcheck: Literal["disable", "enable"]  # Enable/disable ICAP remote server health checking. | Default: disable
    healthcheck_service: str  # ICAP Service name to use for health checks. | MaxLen: 127

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class ServerResponse(TypedDict):
    """
    Type hints for icap/server API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Server name. | MaxLen: 63
    addr_type: Literal["ip4", "ip6", "fqdn"]  # Address type of the remote ICAP server: IPv4, IPv6 | Default: ip4
    ip_address: str  # IPv4 address of the ICAP server. | Default: 0.0.0.0
    ip6_address: str  # IPv6 address of the ICAP server. | Default: ::
    fqdn: str  # ICAP remote server Fully Qualified Domain Name | MaxLen: 255
    port: int  # ICAP server port. | Default: 1344 | Min: 1 | Max: 65535
    max_connections: int  # Maximum number of concurrent connections to ICAP s | Default: 100 | Min: 0 | Max: 4294967295
    secure: Literal["disable", "enable"]  # Enable/disable secure connection to ICAP server. | Default: disable
    ssl_cert: str  # CA certificate name. | MaxLen: 79
    healthcheck: Literal["disable", "enable"]  # Enable/disable ICAP remote server health checking. | Default: disable
    healthcheck_service: str  # ICAP Service name to use for health checks. | MaxLen: 127


@final
class ServerObject:
    """Typed FortiObject for icap/server with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Server name. | MaxLen: 63
    name: str
    # Address type of the remote ICAP server: IPv4, IPv6 or FQDN. | Default: ip4
    addr_type: Literal["ip4", "ip6", "fqdn"]
    # IPv4 address of the ICAP server. | Default: 0.0.0.0
    ip_address: str
    # IPv6 address of the ICAP server. | Default: ::
    ip6_address: str
    # ICAP remote server Fully Qualified Domain Name (FQDN). | MaxLen: 255
    fqdn: str
    # ICAP server port. | Default: 1344 | Min: 1 | Max: 65535
    port: int
    # Maximum number of concurrent connections to ICAP server | Default: 100 | Min: 0 | Max: 4294967295
    max_connections: int
    # Enable/disable secure connection to ICAP server. | Default: disable
    secure: Literal["disable", "enable"]
    # CA certificate name. | MaxLen: 79
    ssl_cert: str
    # Enable/disable ICAP remote server health checking. Attempts | Default: disable
    healthcheck: Literal["disable", "enable"]
    # ICAP Service name to use for health checks. | MaxLen: 127
    healthcheck_service: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ServerPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Server:
    """
    Configure ICAP servers.
    
    Path: icap/server
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
    ) -> ServerResponse: ...
    
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
    ) -> ServerResponse: ...
    
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
    ) -> list[ServerResponse]: ...
    
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
    ) -> ServerObject: ...
    
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
    ) -> ServerObject: ...
    
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
    ) -> list[ServerObject]: ...
    
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
    ) -> ServerResponse: ...
    
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
    ) -> ServerResponse: ...
    
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
    ) -> list[ServerResponse]: ...
    
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
    ) -> ServerObject | list[ServerObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ServerObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ServerObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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
    ) -> ServerObject: ...
    
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
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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

class ServerDictMode:
    """Server endpoint for dict response mode (default for this client).
    
    By default returns ServerResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ServerObject.
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
    ) -> ServerObject: ...
    
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
    ) -> list[ServerObject]: ...
    
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
    ) -> ServerResponse: ...
    
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
    ) -> list[ServerResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ServerObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ServerObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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
    ) -> ServerObject: ...
    
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
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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


class ServerObjectMode:
    """Server endpoint for object response mode (default for this client).
    
    By default returns ServerObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ServerResponse (TypedDict).
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
    ) -> ServerResponse: ...
    
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
    ) -> list[ServerResponse]: ...
    
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
    ) -> ServerObject: ...
    
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
    ) -> list[ServerObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ServerObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ServerObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ServerObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ServerObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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
    ) -> ServerObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ServerObject: ...
    
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
        payload_dict: ServerPayload | None = ...,
        name: str | None = ...,
        addr_type: Literal["ip4", "ip6", "fqdn"] | None = ...,
        ip_address: str | None = ...,
        ip6_address: str | None = ...,
        fqdn: str | None = ...,
        port: int | None = ...,
        max_connections: int | None = ...,
        secure: Literal["disable", "enable"] | None = ...,
        ssl_cert: str | None = ...,
        healthcheck: Literal["disable", "enable"] | None = ...,
        healthcheck_service: str | None = ...,
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
    "Server",
    "ServerDictMode",
    "ServerObjectMode",
    "ServerPayload",
    "ServerObject",
]