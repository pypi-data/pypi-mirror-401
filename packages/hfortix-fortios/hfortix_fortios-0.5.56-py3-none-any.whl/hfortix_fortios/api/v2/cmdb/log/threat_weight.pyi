from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ThreatWeightPayload(TypedDict, total=False):
    """
    Type hints for log/threat_weight payload fields.
    
    Configure threat weight settings.
    
    **Usage:**
        payload: ThreatWeightPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    status: Literal["enable", "disable"]  # Enable/disable the threat weight feature. | Default: enable
    level: str  # Score mapping for threat weight levels.
    blocked_connection: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for blocked connections. | Default: high
    failed_connection: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for failed connections. | Default: low
    url_block_detected: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for URL blocking. | Default: high
    botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for detected botnet connection | Default: critical
    malware: str  # Anti-virus malware threat weight settings.
    ips: str  # IPS threat weight settings.
    web: list[dict[str, Any]]  # Web filtering threat weight settings.
    geolocation: list[dict[str, Any]]  # Geolocation-based threat weight settings.
    application: list[dict[str, Any]]  # Application-control threat weight settings.

# Nested TypedDicts for table field children (dict mode)

class ThreatWeightWebItem(TypedDict):
    """Type hints for web table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Entry ID. | Default: 0 | Min: 0 | Max: 255
    category: int  # Threat weight score for web category filtering mat | Default: 0 | Min: 0 | Max: 255
    level: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for web category filtering mat | Default: low


class ThreatWeightGeolocationItem(TypedDict):
    """Type hints for geolocation table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Entry ID. | Default: 0 | Min: 0 | Max: 255
    country: str  # Country code. | MaxLen: 2
    level: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for Geolocation-based events. | Default: low


class ThreatWeightApplicationItem(TypedDict):
    """Type hints for application table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Entry ID. | Default: 0 | Min: 0 | Max: 255
    category: int  # Application category. | Default: 0 | Min: 0 | Max: 65535
    level: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for Application events. | Default: low


# Nested classes for table field children (object mode)

@final
class ThreatWeightWebObject:
    """Typed object for web table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Entry ID. | Default: 0 | Min: 0 | Max: 255
    id: int
    # Threat weight score for web category filtering matches. | Default: 0 | Min: 0 | Max: 255
    category: int
    # Threat weight score for web category filtering matches. | Default: low
    level: Literal["disable", "low", "medium", "high", "critical"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class ThreatWeightGeolocationObject:
    """Typed object for geolocation table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Entry ID. | Default: 0 | Min: 0 | Max: 255
    id: int
    # Country code. | MaxLen: 2
    country: str
    # Threat weight score for Geolocation-based events. | Default: low
    level: Literal["disable", "low", "medium", "high", "critical"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class ThreatWeightApplicationObject:
    """Typed object for application table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Entry ID. | Default: 0 | Min: 0 | Max: 255
    id: int
    # Application category. | Default: 0 | Min: 0 | Max: 65535
    category: int
    # Threat weight score for Application events. | Default: low
    level: Literal["disable", "low", "medium", "high", "critical"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class ThreatWeightResponse(TypedDict):
    """
    Type hints for log/threat_weight API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    status: Literal["enable", "disable"]  # Enable/disable the threat weight feature. | Default: enable
    level: str  # Score mapping for threat weight levels.
    blocked_connection: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for blocked connections. | Default: high
    failed_connection: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for failed connections. | Default: low
    url_block_detected: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for URL blocking. | Default: high
    botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"]  # Threat weight score for detected botnet connection | Default: critical
    malware: str  # Anti-virus malware threat weight settings.
    ips: str  # IPS threat weight settings.
    web: list[ThreatWeightWebItem]  # Web filtering threat weight settings.
    geolocation: list[ThreatWeightGeolocationItem]  # Geolocation-based threat weight settings.
    application: list[ThreatWeightApplicationItem]  # Application-control threat weight settings.


@final
class ThreatWeightObject:
    """Typed FortiObject for log/threat_weight with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Enable/disable the threat weight feature. | Default: enable
    status: Literal["enable", "disable"]
    # Score mapping for threat weight levels.
    level: str
    # Threat weight score for blocked connections. | Default: high
    blocked_connection: Literal["disable", "low", "medium", "high", "critical"]
    # Threat weight score for failed connections. | Default: low
    failed_connection: Literal["disable", "low", "medium", "high", "critical"]
    # Threat weight score for URL blocking. | Default: high
    url_block_detected: Literal["disable", "low", "medium", "high", "critical"]
    # Threat weight score for detected botnet connections. | Default: critical
    botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"]
    # Anti-virus malware threat weight settings.
    malware: str
    # IPS threat weight settings.
    ips: str
    # Web filtering threat weight settings.
    web: list[ThreatWeightWebObject]
    # Geolocation-based threat weight settings.
    geolocation: list[ThreatWeightGeolocationObject]
    # Application-control threat weight settings.
    application: list[ThreatWeightApplicationObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ThreatWeightPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class ThreatWeight:
    """
    Configure threat weight settings.
    
    Path: log/threat_weight
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightObject: ...
    
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
    ) -> ThreatWeightObject: ...
    
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
    ) -> ThreatWeightObject: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ThreatWeightObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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

class ThreatWeightDictMode:
    """ThreatWeight endpoint for dict response mode (default for this client).
    
    By default returns ThreatWeightResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ThreatWeightObject.
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
    ) -> ThreatWeightObject: ...
    
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
    ) -> ThreatWeightObject: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ThreatWeightObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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


class ThreatWeightObjectMode:
    """ThreatWeight endpoint for object response mode (default for this client).
    
    By default returns ThreatWeightObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ThreatWeightResponse (TypedDict).
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightResponse: ...
    
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
    ) -> ThreatWeightObject: ...
    
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
    ) -> ThreatWeightObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ThreatWeightObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ThreatWeightObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: ThreatWeightPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        level: str | None = ...,
        blocked_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        failed_connection: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        url_block_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        botnet_connection_detected: Literal["disable", "low", "medium", "high", "critical"] | None = ...,
        malware: str | None = ...,
        ips: str | None = ...,
        web: str | list[str] | list[dict[str, Any]] | None = ...,
        geolocation: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "ThreatWeight",
    "ThreatWeightDictMode",
    "ThreatWeightObjectMode",
    "ThreatWeightPayload",
    "ThreatWeightObject",
]