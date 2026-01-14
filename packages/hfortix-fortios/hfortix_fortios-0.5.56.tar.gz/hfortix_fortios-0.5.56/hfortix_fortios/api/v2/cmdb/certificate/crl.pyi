from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class CrlPayload(TypedDict, total=False):
    """
    Type hints for certificate/crl payload fields.
    
    Certificate Revocation List as a PEM file.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.certificate.local.LocalEndpoint` (via: scep-cert)
        - :class:`~.system.vdom.VdomEndpoint` (via: update-vdom)

    **Usage:**
        payload: CrlPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 35
    crl: str  # Certificate Revocation List as a PEM file.
    range: Literal["global", "vdom"]  # Either global or VDOM IP address range for the cer | Default: global
    source: Literal["factory", "user", "bundle"]  # Certificate source type. | Default: user
    update_vdom: str  # VDOM for CRL update. | Default: root | MaxLen: 31
    ldap_server: str  # LDAP server name for CRL auto-update. | MaxLen: 35
    ldap_username: str  # LDAP server user name. | MaxLen: 63
    ldap_password: str  # LDAP server user password. | MaxLen: 128
    http_url: str  # HTTP server URL for CRL auto-update. | MaxLen: 255
    scep_url: str  # SCEP server URL for CRL auto-update. | MaxLen: 255
    scep_cert: str  # Local certificate for SCEP communication for CRL a | Default: Fortinet_CA_SSL | MaxLen: 35
    update_interval: int  # Time in seconds before the FortiGate checks for an | Default: 0 | Min: 0 | Max: 4294967295
    source_ip: str  # Source IP address for communications to a HTTP or | Default: 0.0.0.0

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class CrlResponse(TypedDict):
    """
    Type hints for certificate/crl API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 35
    crl: str  # Certificate Revocation List as a PEM file.
    range: Literal["global", "vdom"]  # Either global or VDOM IP address range for the cer | Default: global
    source: Literal["factory", "user", "bundle"]  # Certificate source type. | Default: user
    update_vdom: str  # VDOM for CRL update. | Default: root | MaxLen: 31
    ldap_server: str  # LDAP server name for CRL auto-update. | MaxLen: 35
    ldap_username: str  # LDAP server user name. | MaxLen: 63
    ldap_password: str  # LDAP server user password. | MaxLen: 128
    http_url: str  # HTTP server URL for CRL auto-update. | MaxLen: 255
    scep_url: str  # SCEP server URL for CRL auto-update. | MaxLen: 255
    scep_cert: str  # Local certificate for SCEP communication for CRL a | Default: Fortinet_CA_SSL | MaxLen: 35
    update_interval: int  # Time in seconds before the FortiGate checks for an | Default: 0 | Min: 0 | Max: 4294967295
    source_ip: str  # Source IP address for communications to a HTTP or | Default: 0.0.0.0


@final
class CrlObject:
    """Typed FortiObject for certificate/crl with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 35
    name: str
    # Certificate Revocation List as a PEM file.
    crl: str
    # Either global or VDOM IP address range for the certificate. | Default: global
    range: Literal["global", "vdom"]
    # Certificate source type. | Default: user
    source: Literal["factory", "user", "bundle"]
    # VDOM for CRL update. | Default: root | MaxLen: 31
    update_vdom: str
    # LDAP server name for CRL auto-update. | MaxLen: 35
    ldap_server: str
    # LDAP server user name. | MaxLen: 63
    ldap_username: str
    # LDAP server user password. | MaxLen: 128
    ldap_password: str
    # HTTP server URL for CRL auto-update. | MaxLen: 255
    http_url: str
    # SCEP server URL for CRL auto-update. | MaxLen: 255
    scep_url: str
    # Local certificate for SCEP communication for CRL auto-update | Default: Fortinet_CA_SSL | MaxLen: 35
    scep_cert: str
    # Time in seconds before the FortiGate checks for an updated C | Default: 0 | Min: 0 | Max: 4294967295
    update_interval: int
    # Source IP address for communications to a HTTP or SCEP CA se | Default: 0.0.0.0
    source_ip: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> CrlPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Crl:
    """
    Certificate Revocation List as a PEM file.
    
    Path: certificate/crl
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
    ) -> CrlResponse: ...
    
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
    ) -> CrlResponse: ...
    
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
    ) -> list[CrlResponse]: ...
    
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
    ) -> CrlObject: ...
    
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
    ) -> CrlObject: ...
    
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
    ) -> list[CrlObject]: ...
    
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
    ) -> CrlResponse: ...
    
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
    ) -> CrlResponse: ...
    
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
    ) -> list[CrlResponse]: ...
    
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
    ) -> CrlObject | list[CrlObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CrlObject: ...
    
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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

class CrlDictMode:
    """Crl endpoint for dict response mode (default for this client).
    
    By default returns CrlResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return CrlObject.
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
    ) -> CrlObject: ...
    
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
    ) -> list[CrlObject]: ...
    
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
    ) -> CrlResponse: ...
    
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
    ) -> list[CrlResponse]: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CrlObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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


class CrlObjectMode:
    """Crl endpoint for object response mode (default for this client).
    
    By default returns CrlObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return CrlResponse (TypedDict).
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
    ) -> CrlResponse: ...
    
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
    ) -> list[CrlResponse]: ...
    
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
    ) -> CrlObject: ...
    
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
    ) -> list[CrlObject]: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CrlObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> CrlObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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
        payload_dict: CrlPayload | None = ...,
        name: str | None = ...,
        crl: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        update_vdom: str | None = ...,
        ldap_server: str | None = ...,
        ldap_username: str | None = ...,
        ldap_password: str | None = ...,
        http_url: str | None = ...,
        scep_url: str | None = ...,
        scep_cert: str | None = ...,
        update_interval: int | None = ...,
        source_ip: str | None = ...,
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
    "Crl",
    "CrlDictMode",
    "CrlObjectMode",
    "CrlPayload",
    "CrlObject",
]