from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class CaPayload(TypedDict, total=False):
    """
    Type hints for certificate/ca payload fields.
    
    CA certificate.
    
    **Usage:**
        payload: CaPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 79
    ca: str  # CA certificate as a PEM file.
    range: Literal["global", "vdom"]  # Either global or VDOM IP address range for the CA | Default: global
    source: Literal["factory", "user", "bundle"]  # CA certificate source type. | Default: user
    ssl_inspection_trusted: Literal["enable", "disable"]  # Enable/disable this CA as a trusted CA for SSL ins | Default: enable
    scep_url: str  # URL of the SCEP server. | MaxLen: 255
    est_url: str  # URL of the EST server. | MaxLen: 255
    auto_update_days: int  # Number of days to wait before requesting an update | Default: 0 | Min: 0 | Max: 4294967295
    auto_update_days_warning: int  # Number of days before an expiry-warning message is | Default: 0 | Min: 0 | Max: 4294967295
    source_ip: str  # Source IP address for communications to the SCEP s | Default: 0.0.0.0
    ca_identifier: str  # CA identifier of the SCEP server. | MaxLen: 255
    obsolete: Literal["disable", "enable"]  # Enable/disable this CA as obsoleted. | Default: disable
    fabric_ca: Literal["disable", "enable"]  # Enable/disable synchronization of CA across Securi | Default: disable
    details: str  # Print CA certificate detailed information.

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class CaResponse(TypedDict):
    """
    Type hints for certificate/ca API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 79
    ca: str  # CA certificate as a PEM file.
    range: Literal["global", "vdom"]  # Either global or VDOM IP address range for the CA | Default: global
    source: Literal["factory", "user", "bundle"]  # CA certificate source type. | Default: user
    ssl_inspection_trusted: Literal["enable", "disable"]  # Enable/disable this CA as a trusted CA for SSL ins | Default: enable
    scep_url: str  # URL of the SCEP server. | MaxLen: 255
    est_url: str  # URL of the EST server. | MaxLen: 255
    auto_update_days: int  # Number of days to wait before requesting an update | Default: 0 | Min: 0 | Max: 4294967295
    auto_update_days_warning: int  # Number of days before an expiry-warning message is | Default: 0 | Min: 0 | Max: 4294967295
    source_ip: str  # Source IP address for communications to the SCEP s | Default: 0.0.0.0
    ca_identifier: str  # CA identifier of the SCEP server. | MaxLen: 255
    obsolete: Literal["disable", "enable"]  # Enable/disable this CA as obsoleted. | Default: disable
    fabric_ca: Literal["disable", "enable"]  # Enable/disable synchronization of CA across Securi | Default: disable
    details: str  # Print CA certificate detailed information.


@final
class CaObject:
    """Typed FortiObject for certificate/ca with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 79
    name: str
    # CA certificate as a PEM file.
    ca: str
    # Either global or VDOM IP address range for the CA certificat | Default: global
    range: Literal["global", "vdom"]
    # CA certificate source type. | Default: user
    source: Literal["factory", "user", "bundle"]
    # Enable/disable this CA as a trusted CA for SSL inspection. | Default: enable
    ssl_inspection_trusted: Literal["enable", "disable"]
    # URL of the SCEP server. | MaxLen: 255
    scep_url: str
    # URL of the EST server. | MaxLen: 255
    est_url: str
    # Number of days to wait before requesting an updated CA certi | Default: 0 | Min: 0 | Max: 4294967295
    auto_update_days: int
    # Number of days before an expiry-warning message is generated | Default: 0 | Min: 0 | Max: 4294967295
    auto_update_days_warning: int
    # Source IP address for communications to the SCEP server. | Default: 0.0.0.0
    source_ip: str
    # CA identifier of the SCEP server. | MaxLen: 255
    ca_identifier: str
    # Enable/disable this CA as obsoleted. | Default: disable
    obsolete: Literal["disable", "enable"]
    # Enable/disable synchronization of CA across Security Fabric. | Default: disable
    fabric_ca: Literal["disable", "enable"]
    # Print CA certificate detailed information.
    details: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> CaPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Ca:
    """
    CA certificate.
    
    Path: certificate/ca
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
    ) -> CaResponse: ...
    
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
    ) -> CaResponse: ...
    
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
    ) -> list[CaResponse]: ...
    
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
    ) -> CaObject: ...
    
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
    ) -> CaObject: ...
    
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
    ) -> list[CaObject]: ...
    
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
    ) -> CaResponse: ...
    
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
    ) -> CaResponse: ...
    
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
    ) -> list[CaResponse]: ...
    
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
    ) -> CaObject | list[CaObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CaObject: ...
    
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
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
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
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

class CaDictMode:
    """Ca endpoint for dict response mode (default for this client).
    
    By default returns CaResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return CaObject.
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
    ) -> CaObject: ...
    
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
    ) -> list[CaObject]: ...
    
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
    ) -> CaResponse: ...
    
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
    ) -> list[CaResponse]: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CaObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
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
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
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


class CaObjectMode:
    """Ca endpoint for object response mode (default for this client).
    
    By default returns CaObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return CaResponse (TypedDict).
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
    ) -> CaResponse: ...
    
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
    ) -> list[CaResponse]: ...
    
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
    ) -> CaObject: ...
    
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
    ) -> list[CaObject]: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CaObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> CaObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
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
        payload_dict: CaPayload | None = ...,
        name: str | None = ...,
        ca: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        ssl_inspection_trusted: Literal["enable", "disable"] | None = ...,
        scep_url: str | None = ...,
        est_url: str | None = ...,
        auto_update_days: int | None = ...,
        auto_update_days_warning: int | None = ...,
        source_ip: str | None = ...,
        ca_identifier: str | None = ...,
        obsolete: Literal["disable", "enable"] | None = ...,
        fabric_ca: Literal["disable", "enable"] | None = ...,
        details: str | None = ...,
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
    "Ca",
    "CaDictMode",
    "CaObjectMode",
    "CaPayload",
    "CaObject",
]