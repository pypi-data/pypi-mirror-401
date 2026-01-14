from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class EventfilterPayload(TypedDict, total=False):
    """
    Type hints for log/eventfilter payload fields.
    
    Configure log event filters.
    
    **Usage:**
        payload: EventfilterPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    event: Literal["enable", "disable"]  # Enable/disable event logging. | Default: enable
    system: Literal["enable", "disable"]  # Enable/disable system event logging. | Default: enable
    vpn: Literal["enable", "disable"]  # Enable/disable VPN event logging. | Default: enable
    user: Literal["enable", "disable"]  # Enable/disable user authentication event logging. | Default: enable
    router: Literal["enable", "disable"]  # Enable/disable router event logging. | Default: enable
    wireless_activity: Literal["enable", "disable"]  # Enable/disable wireless event logging. | Default: enable
    wan_opt: Literal["enable", "disable"]  # Enable/disable WAN optimization event logging. | Default: enable
    endpoint: Literal["enable", "disable"]  # Enable/disable endpoint event logging. | Default: enable
    ha: Literal["enable", "disable"]  # Enable/disable ha event logging. | Default: enable
    security_rating: Literal["enable", "disable"]  # Enable/disable Security Rating result logging. | Default: enable
    fortiextender: Literal["enable", "disable"]  # Enable/disable FortiExtender logging. | Default: enable
    connector: Literal["enable", "disable"]  # Enable/disable SDN connector logging. | Default: enable
    sdwan: Literal["enable", "disable"]  # Enable/disable SD-WAN logging. | Default: enable
    cifs: Literal["enable", "disable"]  # Enable/disable CIFS logging. | Default: enable
    switch_controller: Literal["enable", "disable"]  # Enable/disable Switch-Controller logging. | Default: enable
    rest_api: Literal["enable", "disable"]  # Enable/disable REST API logging. | Default: enable
    web_svc: Literal["enable", "disable"]  # Enable/disable web-svc performance logging. | Default: enable
    webproxy: Literal["enable", "disable"]  # Enable/disable web proxy event logging. | Default: enable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class EventfilterResponse(TypedDict):
    """
    Type hints for log/eventfilter API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    event: Literal["enable", "disable"]  # Enable/disable event logging. | Default: enable
    system: Literal["enable", "disable"]  # Enable/disable system event logging. | Default: enable
    vpn: Literal["enable", "disable"]  # Enable/disable VPN event logging. | Default: enable
    user: Literal["enable", "disable"]  # Enable/disable user authentication event logging. | Default: enable
    router: Literal["enable", "disable"]  # Enable/disable router event logging. | Default: enable
    wireless_activity: Literal["enable", "disable"]  # Enable/disable wireless event logging. | Default: enable
    wan_opt: Literal["enable", "disable"]  # Enable/disable WAN optimization event logging. | Default: enable
    endpoint: Literal["enable", "disable"]  # Enable/disable endpoint event logging. | Default: enable
    ha: Literal["enable", "disable"]  # Enable/disable ha event logging. | Default: enable
    security_rating: Literal["enable", "disable"]  # Enable/disable Security Rating result logging. | Default: enable
    fortiextender: Literal["enable", "disable"]  # Enable/disable FortiExtender logging. | Default: enable
    connector: Literal["enable", "disable"]  # Enable/disable SDN connector logging. | Default: enable
    sdwan: Literal["enable", "disable"]  # Enable/disable SD-WAN logging. | Default: enable
    cifs: Literal["enable", "disable"]  # Enable/disable CIFS logging. | Default: enable
    switch_controller: Literal["enable", "disable"]  # Enable/disable Switch-Controller logging. | Default: enable
    rest_api: Literal["enable", "disable"]  # Enable/disable REST API logging. | Default: enable
    web_svc: Literal["enable", "disable"]  # Enable/disable web-svc performance logging. | Default: enable
    webproxy: Literal["enable", "disable"]  # Enable/disable web proxy event logging. | Default: enable


@final
class EventfilterObject:
    """Typed FortiObject for log/eventfilter with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Enable/disable event logging. | Default: enable
    event: Literal["enable", "disable"]
    # Enable/disable system event logging. | Default: enable
    system: Literal["enable", "disable"]
    # Enable/disable VPN event logging. | Default: enable
    vpn: Literal["enable", "disable"]
    # Enable/disable user authentication event logging. | Default: enable
    user: Literal["enable", "disable"]
    # Enable/disable router event logging. | Default: enable
    router: Literal["enable", "disable"]
    # Enable/disable wireless event logging. | Default: enable
    wireless_activity: Literal["enable", "disable"]
    # Enable/disable WAN optimization event logging. | Default: enable
    wan_opt: Literal["enable", "disable"]
    # Enable/disable endpoint event logging. | Default: enable
    endpoint: Literal["enable", "disable"]
    # Enable/disable ha event logging. | Default: enable
    ha: Literal["enable", "disable"]
    # Enable/disable Security Rating result logging. | Default: enable
    security_rating: Literal["enable", "disable"]
    # Enable/disable FortiExtender logging. | Default: enable
    fortiextender: Literal["enable", "disable"]
    # Enable/disable SDN connector logging. | Default: enable
    connector: Literal["enable", "disable"]
    # Enable/disable SD-WAN logging. | Default: enable
    sdwan: Literal["enable", "disable"]
    # Enable/disable CIFS logging. | Default: enable
    cifs: Literal["enable", "disable"]
    # Enable/disable Switch-Controller logging. | Default: enable
    switch_controller: Literal["enable", "disable"]
    # Enable/disable REST API logging. | Default: enable
    rest_api: Literal["enable", "disable"]
    # Enable/disable web-svc performance logging. | Default: enable
    web_svc: Literal["enable", "disable"]
    # Enable/disable web proxy event logging. | Default: enable
    webproxy: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> EventfilterPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Eventfilter:
    """
    Configure log event filters.
    
    Path: log/eventfilter
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterObject: ...
    
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
    ) -> EventfilterObject: ...
    
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
    ) -> EventfilterObject: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> EventfilterObject: ...
    
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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

class EventfilterDictMode:
    """Eventfilter endpoint for dict response mode (default for this client).
    
    By default returns EventfilterResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return EventfilterObject.
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
    ) -> EventfilterObject: ...
    
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
    ) -> EventfilterObject: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> EventfilterObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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


class EventfilterObjectMode:
    """Eventfilter endpoint for object response mode (default for this client).
    
    By default returns EventfilterObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return EventfilterResponse (TypedDict).
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterResponse: ...
    
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
    ) -> EventfilterObject: ...
    
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
    ) -> EventfilterObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> EventfilterObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> EventfilterObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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
        payload_dict: EventfilterPayload | None = ...,
        event: Literal["enable", "disable"] | None = ...,
        system: Literal["enable", "disable"] | None = ...,
        vpn: Literal["enable", "disable"] | None = ...,
        user: Literal["enable", "disable"] | None = ...,
        router: Literal["enable", "disable"] | None = ...,
        wireless_activity: Literal["enable", "disable"] | None = ...,
        wan_opt: Literal["enable", "disable"] | None = ...,
        endpoint: Literal["enable", "disable"] | None = ...,
        ha: Literal["enable", "disable"] | None = ...,
        security_rating: Literal["enable", "disable"] | None = ...,
        fortiextender: Literal["enable", "disable"] | None = ...,
        connector: Literal["enable", "disable"] | None = ...,
        sdwan: Literal["enable", "disable"] | None = ...,
        cifs: Literal["enable", "disable"] | None = ...,
        switch_controller: Literal["enable", "disable"] | None = ...,
        rest_api: Literal["enable", "disable"] | None = ...,
        web_svc: Literal["enable", "disable"] | None = ...,
        webproxy: Literal["enable", "disable"] | None = ...,
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
    "Eventfilter",
    "EventfilterDictMode",
    "EventfilterObjectMode",
    "EventfilterPayload",
    "EventfilterObject",
]