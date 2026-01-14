from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class InternetServicePayload(TypedDict, total=False):
    """
    Type hints for firewall/internet_service payload fields.
    
    Show Internet Service application.
    
    **Usage:**
        payload: InternetServicePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    id: int  # Internet Service ID. | Default: 0 | Min: 0 | Max: 4294967295
    name: str  # Internet Service name. | MaxLen: 63
    icon_id: int  # Icon ID of Internet Service. | Default: 0 | Min: 0 | Max: 4294967295
    direction: Literal["src", "dst", "both"]  # How this service may be used in a firewall policy | Default: both
    database: Literal["isdb", "irdb"]  # Database name this Internet Service belongs to. | Default: isdb
    ip_range_number: int  # Number of IPv4 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    extra_ip_range_number: int  # Extra number of IPv4 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    ip_number: int  # Total number of IPv4 addresses. | Default: 0 | Min: 0 | Max: 4294967295
    ip6_range_number: int  # Number of IPv6 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    extra_ip6_range_number: int  # Extra number of IPv6 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    singularity: int  # Singular level of the Internet Service. | Default: 0 | Min: 0 | Max: 65535
    obsolete: int  # Indicates whether the Internet Service can be used | Default: 0 | Min: 0 | Max: 255

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class InternetServiceResponse(TypedDict):
    """
    Type hints for firewall/internet_service API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    id: int  # Internet Service ID. | Default: 0 | Min: 0 | Max: 4294967295
    name: str  # Internet Service name. | MaxLen: 63
    icon_id: int  # Icon ID of Internet Service. | Default: 0 | Min: 0 | Max: 4294967295
    direction: Literal["src", "dst", "both"]  # How this service may be used in a firewall policy | Default: both
    database: Literal["isdb", "irdb"]  # Database name this Internet Service belongs to. | Default: isdb
    ip_range_number: int  # Number of IPv4 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    extra_ip_range_number: int  # Extra number of IPv4 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    ip_number: int  # Total number of IPv4 addresses. | Default: 0 | Min: 0 | Max: 4294967295
    ip6_range_number: int  # Number of IPv6 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    extra_ip6_range_number: int  # Extra number of IPv6 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    singularity: int  # Singular level of the Internet Service. | Default: 0 | Min: 0 | Max: 65535
    obsolete: int  # Indicates whether the Internet Service can be used | Default: 0 | Min: 0 | Max: 255


@final
class InternetServiceObject:
    """Typed FortiObject for firewall/internet_service with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Internet Service ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Internet Service name. | MaxLen: 63
    name: str
    # Icon ID of Internet Service. | Default: 0 | Min: 0 | Max: 4294967295
    icon_id: int
    # How this service may be used in a firewall policy | Default: both
    direction: Literal["src", "dst", "both"]
    # Database name this Internet Service belongs to. | Default: isdb
    database: Literal["isdb", "irdb"]
    # Number of IPv4 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    ip_range_number: int
    # Extra number of IPv4 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    extra_ip_range_number: int
    # Total number of IPv4 addresses. | Default: 0 | Min: 0 | Max: 4294967295
    ip_number: int
    # Number of IPv6 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    ip6_range_number: int
    # Extra number of IPv6 ranges. | Default: 0 | Min: 0 | Max: 4294967295
    extra_ip6_range_number: int
    # Singular level of the Internet Service. | Default: 0 | Min: 0 | Max: 65535
    singularity: int
    # Indicates whether the Internet Service can be used. | Default: 0 | Min: 0 | Max: 255
    obsolete: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> InternetServicePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class InternetService:
    """
    Show Internet Service application.
    
    Path: firewall/internet_service
    Category: cmdb
    Primary Key: id
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
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> InternetServiceResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> InternetServiceResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        id: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[InternetServiceResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        id: int,
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
    ) -> InternetServiceObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        id: int,
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
    ) -> InternetServiceObject: ...
    
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
    ) -> list[InternetServiceObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> InternetServiceResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        id: int,
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
    ) -> InternetServiceResponse: ...
    
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
    ) -> list[InternetServiceResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int | None = ...,
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
    ) -> InternetServiceObject | list[InternetServiceObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
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

class InternetServiceDictMode:
    """InternetService endpoint for dict response mode (default for this client).
    
    By default returns InternetServiceResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return InternetServiceObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> InternetServiceObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[InternetServiceObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
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
    ) -> InternetServiceResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[InternetServiceResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
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


class InternetServiceObjectMode:
    """InternetService endpoint for object response mode (default for this client).
    
    By default returns InternetServiceObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return InternetServiceResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> InternetServiceResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[InternetServiceResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
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
    ) -> InternetServiceObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[InternetServiceObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> InternetServiceObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: InternetServicePayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        icon_id: int | None = ...,
        direction: Literal["src", "dst", "both"] | None = ...,
        database: Literal["isdb", "irdb"] | None = ...,
        ip_range_number: int | None = ...,
        extra_ip_range_number: int | None = ...,
        ip_number: int | None = ...,
        ip6_range_number: int | None = ...,
        extra_ip6_range_number: int | None = ...,
        singularity: int | None = ...,
        obsolete: int | None = ...,
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
    "InternetService",
    "InternetServiceDictMode",
    "InternetServiceObjectMode",
    "InternetServicePayload",
    "InternetServiceObject",
]