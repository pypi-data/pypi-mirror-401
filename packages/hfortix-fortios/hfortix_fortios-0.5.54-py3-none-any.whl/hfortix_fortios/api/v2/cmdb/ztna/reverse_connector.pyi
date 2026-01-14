from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ReverseConnectorPayload(TypedDict, total=False):
    """
    Type hints for ztna/reverse_connector payload fields.
    
    Configure ZTNA Reverse-Connector.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.vpn.certificate.ca.CaEndpoint` (via: trusted-server-ca)
        - :class:`~.vpn.certificate.local.LocalEndpoint` (via: certificate)

    **Usage:**
        payload: ReverseConnectorPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Reverse-Connector name | MaxLen: 35
    status: Literal["enable", "disable"]  # Reverse-Connector status. | Default: enable
    address: str  # Connector service edge adress(IP or FQDN). | MaxLen: 255
    port: int  # Port number that traffic uses to connect to connec | Default: 0 | Min: 0 | Max: 65535
    health_check_interval: int  # Health check interval in seconds | Default: 60 | Min: 0 | Max: 600
    ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"]  # Highest TLS version acceptable from a server. | Default: tls-1.3
    certificate: str  # The name of the certificate to use for SSL handsha | MaxLen: 35
    trusted_server_ca: str  # Trusted Server CA certificate used by SSL connecti | MaxLen: 79

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class ReverseConnectorResponse(TypedDict):
    """
    Type hints for ztna/reverse_connector API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Reverse-Connector name | MaxLen: 35
    status: Literal["enable", "disable"]  # Reverse-Connector status. | Default: enable
    address: str  # Connector service edge adress(IP or FQDN). | MaxLen: 255
    port: int  # Port number that traffic uses to connect to connec | Default: 0 | Min: 0 | Max: 65535
    health_check_interval: int  # Health check interval in seconds | Default: 60 | Min: 0 | Max: 600
    ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"]  # Highest TLS version acceptable from a server. | Default: tls-1.3
    certificate: str  # The name of the certificate to use for SSL handsha | MaxLen: 35
    trusted_server_ca: str  # Trusted Server CA certificate used by SSL connecti | MaxLen: 79


@final
class ReverseConnectorObject:
    """Typed FortiObject for ztna/reverse_connector with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Reverse-Connector name | MaxLen: 35
    name: str
    # Reverse-Connector status. | Default: enable
    status: Literal["enable", "disable"]
    # Connector service edge adress(IP or FQDN). | MaxLen: 255
    address: str
    # Port number that traffic uses to connect to connector servic | Default: 0 | Min: 0 | Max: 65535
    port: int
    # Health check interval in seconds | Default: 60 | Min: 0 | Max: 600
    health_check_interval: int
    # Highest TLS version acceptable from a server. | Default: tls-1.3
    ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"]
    # The name of the certificate to use for SSL handshake. | MaxLen: 35
    certificate: str
    # Trusted Server CA certificate used by SSL connection. | MaxLen: 79
    trusted_server_ca: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ReverseConnectorPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class ReverseConnector:
    """
    Configure ZTNA Reverse-Connector.
    
    Path: ztna/reverse_connector
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
    ) -> ReverseConnectorResponse: ...
    
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
    ) -> ReverseConnectorResponse: ...
    
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
    ) -> list[ReverseConnectorResponse]: ...
    
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
    ) -> ReverseConnectorObject: ...
    
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
    ) -> ReverseConnectorObject: ...
    
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
    ) -> list[ReverseConnectorObject]: ...
    
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
    ) -> ReverseConnectorResponse: ...
    
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
    ) -> ReverseConnectorResponse: ...
    
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
    ) -> list[ReverseConnectorResponse]: ...
    
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
    ) -> ReverseConnectorObject | list[ReverseConnectorObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
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
    ) -> ReverseConnectorObject: ...
    
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
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
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

class ReverseConnectorDictMode:
    """ReverseConnector endpoint for dict response mode (default for this client).
    
    By default returns ReverseConnectorResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ReverseConnectorObject.
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
    ) -> ReverseConnectorObject: ...
    
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
    ) -> list[ReverseConnectorObject]: ...
    
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
    ) -> ReverseConnectorResponse: ...
    
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
    ) -> list[ReverseConnectorResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
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
    ) -> ReverseConnectorObject: ...
    
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
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
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


class ReverseConnectorObjectMode:
    """ReverseConnector endpoint for object response mode (default for this client).
    
    By default returns ReverseConnectorObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ReverseConnectorResponse (TypedDict).
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
    ) -> ReverseConnectorResponse: ...
    
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
    ) -> list[ReverseConnectorResponse]: ...
    
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
    ) -> ReverseConnectorObject: ...
    
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
    ) -> list[ReverseConnectorObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
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
    ) -> ReverseConnectorObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ReverseConnectorObject: ...
    
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
        payload_dict: ReverseConnectorPayload | None = ...,
        name: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        address: str | None = ...,
        port: int | None = ...,
        health_check_interval: int | None = ...,
        ssl_max_version: Literal["tls-1.1", "tls-1.2", "tls-1.3"] | None = ...,
        certificate: str | None = ...,
        trusted_server_ca: str | None = ...,
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
    "ReverseConnector",
    "ReverseConnectorDictMode",
    "ReverseConnectorObjectMode",
    "ReverseConnectorPayload",
    "ReverseConnectorObject",
]