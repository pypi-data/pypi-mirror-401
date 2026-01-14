from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class UtmProfilePayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/utm_profile payload fields.
    
    Configure UTM (Unified Threat Management) profile.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.antivirus.profile.ProfileEndpoint` (via: antivirus-profile)
        - :class:`~.application.list.ListEndpoint` (via: application-list)
        - :class:`~.ips.sensor.SensorEndpoint` (via: ips-sensor)
        - :class:`~.webfilter.profile.ProfileEndpoint` (via: webfilter-profile)

    **Usage:**
        payload: UtmProfilePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # UTM profile name. | MaxLen: 35
    comment: str  # Comment. | MaxLen: 63
    utm_log: Literal["enable", "disable"]  # Enable/disable UTM logging. | Default: enable
    ips_sensor: str  # IPS sensor name. | MaxLen: 47
    application_list: str  # Application control list name. | MaxLen: 47
    antivirus_profile: str  # AntiVirus profile name. | MaxLen: 47
    webfilter_profile: str  # WebFilter profile name. | MaxLen: 47
    scan_botnet_connections: Literal["disable", "monitor", "block"]  # Block or monitor connections to Botnet servers or | Default: monitor

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class UtmProfileResponse(TypedDict):
    """
    Type hints for wireless_controller/utm_profile API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # UTM profile name. | MaxLen: 35
    comment: str  # Comment. | MaxLen: 63
    utm_log: Literal["enable", "disable"]  # Enable/disable UTM logging. | Default: enable
    ips_sensor: str  # IPS sensor name. | MaxLen: 47
    application_list: str  # Application control list name. | MaxLen: 47
    antivirus_profile: str  # AntiVirus profile name. | MaxLen: 47
    webfilter_profile: str  # WebFilter profile name. | MaxLen: 47
    scan_botnet_connections: Literal["disable", "monitor", "block"]  # Block or monitor connections to Botnet servers or | Default: monitor


@final
class UtmProfileObject:
    """Typed FortiObject for wireless_controller/utm_profile with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # UTM profile name. | MaxLen: 35
    name: str
    # Comment. | MaxLen: 63
    comment: str
    # Enable/disable UTM logging. | Default: enable
    utm_log: Literal["enable", "disable"]
    # IPS sensor name. | MaxLen: 47
    ips_sensor: str
    # Application control list name. | MaxLen: 47
    application_list: str
    # AntiVirus profile name. | MaxLen: 47
    antivirus_profile: str
    # WebFilter profile name. | MaxLen: 47
    webfilter_profile: str
    # Block or monitor connections to Botnet servers or disable Bo | Default: monitor
    scan_botnet_connections: Literal["disable", "monitor", "block"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> UtmProfilePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class UtmProfile:
    """
    Configure UTM (Unified Threat Management) profile.
    
    Path: wireless_controller/utm_profile
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
    ) -> UtmProfileResponse: ...
    
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
    ) -> UtmProfileResponse: ...
    
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
    ) -> list[UtmProfileResponse]: ...
    
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
    ) -> UtmProfileObject: ...
    
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
    ) -> UtmProfileObject: ...
    
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
    ) -> list[UtmProfileObject]: ...
    
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
    ) -> UtmProfileResponse: ...
    
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
    ) -> UtmProfileResponse: ...
    
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
    ) -> list[UtmProfileResponse]: ...
    
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
    ) -> UtmProfileObject | list[UtmProfileObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
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
    ) -> UtmProfileObject: ...
    
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
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
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

class UtmProfileDictMode:
    """UtmProfile endpoint for dict response mode (default for this client).
    
    By default returns UtmProfileResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return UtmProfileObject.
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
    ) -> UtmProfileObject: ...
    
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
    ) -> list[UtmProfileObject]: ...
    
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
    ) -> UtmProfileResponse: ...
    
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
    ) -> list[UtmProfileResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
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
    ) -> UtmProfileObject: ...
    
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
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
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


class UtmProfileObjectMode:
    """UtmProfile endpoint for object response mode (default for this client).
    
    By default returns UtmProfileObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return UtmProfileResponse (TypedDict).
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
    ) -> UtmProfileResponse: ...
    
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
    ) -> list[UtmProfileResponse]: ...
    
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
    ) -> UtmProfileObject: ...
    
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
    ) -> list[UtmProfileObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
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
    ) -> UtmProfileObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> UtmProfileObject: ...
    
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
        payload_dict: UtmProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        utm_log: Literal["enable", "disable"] | None = ...,
        ips_sensor: str | None = ...,
        application_list: str | None = ...,
        antivirus_profile: str | None = ...,
        webfilter_profile: str | None = ...,
        scan_botnet_connections: Literal["disable", "monitor", "block"] | None = ...,
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
    "UtmProfile",
    "UtmProfileDictMode",
    "UtmProfileObjectMode",
    "UtmProfilePayload",
    "UtmProfileObject",
]