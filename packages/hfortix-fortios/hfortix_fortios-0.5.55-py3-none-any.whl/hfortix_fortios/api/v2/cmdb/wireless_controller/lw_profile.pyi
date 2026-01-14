from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class LwProfilePayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/lw_profile payload fields.
    
    Configure LoRaWAN profile.
    
    **Usage:**
        payload: LwProfilePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # LoRaWAN profile name. | MaxLen: 35
    comment: str  # Comment. | MaxLen: 63
    lw_protocol: Literal["basics-station", "packet-forwarder"]  # Configure LoRaWAN protocol | Default: basics-station
    cups_server: str  # CUPS (Configuration and Update Server) domain name | MaxLen: 255
    cups_server_port: int  # CUPS Port value of LoRaWAN device. | Default: 0 | Min: 0 | Max: 65535
    cups_api_key: str  # CUPS API key of LoRaWAN device. | MaxLen: 128
    tc_server: str  # TC (Traffic Controller) domain name or IP address | MaxLen: 255
    tc_server_port: int  # TC Port value of LoRaWAN device. | Default: 0 | Min: 0 | Max: 65535
    tc_api_key: str  # TC API key of LoRaWAN device. | MaxLen: 128

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class LwProfileResponse(TypedDict):
    """
    Type hints for wireless_controller/lw_profile API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # LoRaWAN profile name. | MaxLen: 35
    comment: str  # Comment. | MaxLen: 63
    lw_protocol: Literal["basics-station", "packet-forwarder"]  # Configure LoRaWAN protocol | Default: basics-station
    cups_server: str  # CUPS (Configuration and Update Server) domain name | MaxLen: 255
    cups_server_port: int  # CUPS Port value of LoRaWAN device. | Default: 0 | Min: 0 | Max: 65535
    cups_api_key: str  # CUPS API key of LoRaWAN device. | MaxLen: 128
    tc_server: str  # TC (Traffic Controller) domain name or IP address | MaxLen: 255
    tc_server_port: int  # TC Port value of LoRaWAN device. | Default: 0 | Min: 0 | Max: 65535
    tc_api_key: str  # TC API key of LoRaWAN device. | MaxLen: 128


@final
class LwProfileObject:
    """Typed FortiObject for wireless_controller/lw_profile with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # LoRaWAN profile name. | MaxLen: 35
    name: str
    # Comment. | MaxLen: 63
    comment: str
    # Configure LoRaWAN protocol (default = basics-station) | Default: basics-station
    lw_protocol: Literal["basics-station", "packet-forwarder"]
    # CUPS (Configuration and Update Server) domain name or IP add | MaxLen: 255
    cups_server: str
    # CUPS Port value of LoRaWAN device. | Default: 0 | Min: 0 | Max: 65535
    cups_server_port: int
    # CUPS API key of LoRaWAN device. | MaxLen: 128
    cups_api_key: str
    # TC (Traffic Controller) domain name or IP address of LoRaWAN | MaxLen: 255
    tc_server: str
    # TC Port value of LoRaWAN device. | Default: 0 | Min: 0 | Max: 65535
    tc_server_port: int
    # TC API key of LoRaWAN device. | MaxLen: 128
    tc_api_key: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> LwProfilePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class LwProfile:
    """
    Configure LoRaWAN profile.
    
    Path: wireless_controller/lw_profile
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
    ) -> LwProfileResponse: ...
    
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
    ) -> LwProfileResponse: ...
    
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
    ) -> list[LwProfileResponse]: ...
    
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
    ) -> LwProfileObject: ...
    
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
    ) -> LwProfileObject: ...
    
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
    ) -> list[LwProfileObject]: ...
    
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
    ) -> LwProfileResponse: ...
    
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
    ) -> LwProfileResponse: ...
    
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
    ) -> list[LwProfileResponse]: ...
    
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
    ) -> LwProfileObject | list[LwProfileObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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
    ) -> LwProfileObject: ...
    
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
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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

class LwProfileDictMode:
    """LwProfile endpoint for dict response mode (default for this client).
    
    By default returns LwProfileResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return LwProfileObject.
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
    ) -> LwProfileObject: ...
    
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
    ) -> list[LwProfileObject]: ...
    
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
    ) -> LwProfileResponse: ...
    
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
    ) -> list[LwProfileResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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
    ) -> LwProfileObject: ...
    
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
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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


class LwProfileObjectMode:
    """LwProfile endpoint for object response mode (default for this client).
    
    By default returns LwProfileObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return LwProfileResponse (TypedDict).
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
    ) -> LwProfileResponse: ...
    
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
    ) -> list[LwProfileResponse]: ...
    
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
    ) -> LwProfileObject: ...
    
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
    ) -> list[LwProfileObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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
    ) -> LwProfileObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LwProfileObject: ...
    
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
        payload_dict: LwProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        lw_protocol: Literal["basics-station", "packet-forwarder"] | None = ...,
        cups_server: str | None = ...,
        cups_server_port: int | None = ...,
        cups_api_key: str | None = ...,
        tc_server: str | None = ...,
        tc_server_port: int | None = ...,
        tc_api_key: str | None = ...,
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
    "LwProfile",
    "LwProfileDictMode",
    "LwProfileObjectMode",
    "LwProfilePayload",
    "LwProfileObject",
]