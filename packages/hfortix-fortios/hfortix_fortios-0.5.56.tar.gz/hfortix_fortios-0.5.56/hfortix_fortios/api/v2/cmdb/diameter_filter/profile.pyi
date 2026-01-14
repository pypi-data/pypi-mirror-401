from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ProfilePayload(TypedDict, total=False):
    """
    Type hints for diameter_filter/profile payload fields.
    
    Configure Diameter filter profiles.
    
    **Usage:**
        payload: ProfilePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Profile name. | MaxLen: 47
    comment: str  # Comment. | MaxLen: 255
    monitor_all_messages: Literal["disable", "enable"]  # Enable/disable logging for all User Name and Resul | Default: disable
    log_packet: Literal["disable", "enable"]  # Enable/disable packet log for triggered diameter s | Default: disable
    track_requests_answers: Literal["disable", "enable"]  # Enable/disable validation that each answer has a c | Default: enable
    missing_request_action: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for answers without correspondi | Default: block
    protocol_version_invalid: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for invalid protocol version. | Default: block
    message_length_invalid: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for invalid message length. | Default: block
    request_error_flag_set: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for request messages with error | Default: block
    cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for messages with cmd flag rese | Default: block
    command_code_invalid: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for messages with invalid comma | Default: block
    command_code_range: str  # Valid range for command codes (0-16777215).

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class ProfileResponse(TypedDict):
    """
    Type hints for diameter_filter/profile API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Profile name. | MaxLen: 47
    comment: str  # Comment. | MaxLen: 255
    monitor_all_messages: Literal["disable", "enable"]  # Enable/disable logging for all User Name and Resul | Default: disable
    log_packet: Literal["disable", "enable"]  # Enable/disable packet log for triggered diameter s | Default: disable
    track_requests_answers: Literal["disable", "enable"]  # Enable/disable validation that each answer has a c | Default: enable
    missing_request_action: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for answers without correspondi | Default: block
    protocol_version_invalid: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for invalid protocol version. | Default: block
    message_length_invalid: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for invalid message length. | Default: block
    request_error_flag_set: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for request messages with error | Default: block
    cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for messages with cmd flag rese | Default: block
    command_code_invalid: Literal["allow", "block", "reset", "monitor"]  # Action to be taken for messages with invalid comma | Default: block
    command_code_range: str  # Valid range for command codes (0-16777215).


@final
class ProfileObject:
    """Typed FortiObject for diameter_filter/profile with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Profile name. | MaxLen: 47
    name: str
    # Comment. | MaxLen: 255
    comment: str
    # Enable/disable logging for all User Name and Result Code AVP | Default: disable
    monitor_all_messages: Literal["disable", "enable"]
    # Enable/disable packet log for triggered diameter settings. | Default: disable
    log_packet: Literal["disable", "enable"]
    # Enable/disable validation that each answer has a correspondi | Default: enable
    track_requests_answers: Literal["disable", "enable"]
    # Action to be taken for answers without corresponding request | Default: block
    missing_request_action: Literal["allow", "block", "reset", "monitor"]
    # Action to be taken for invalid protocol version. | Default: block
    protocol_version_invalid: Literal["allow", "block", "reset", "monitor"]
    # Action to be taken for invalid message length. | Default: block
    message_length_invalid: Literal["allow", "block", "reset", "monitor"]
    # Action to be taken for request messages with error flag set. | Default: block
    request_error_flag_set: Literal["allow", "block", "reset", "monitor"]
    # Action to be taken for messages with cmd flag reserve bits s | Default: block
    cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"]
    # Action to be taken for messages with invalid command code. | Default: block
    command_code_invalid: Literal["allow", "block", "reset", "monitor"]
    # Valid range for command codes (0-16777215).
    command_code_range: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ProfilePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Profile:
    """
    Configure Diameter filter profiles.
    
    Path: diameter_filter/profile
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
    ) -> ProfileResponse: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject | list[ProfileObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
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
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
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

class ProfileDictMode:
    """Profile endpoint for dict response mode (default for this client).
    
    By default returns ProfileResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ProfileObject.
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...
    
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
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
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
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


class ProfileObjectMode:
    """Profile endpoint for object response mode (default for this client).
    
    By default returns ProfileObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ProfileResponse (TypedDict).
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
    ) -> ProfileResponse: ...
    
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
    ) -> list[ProfileResponse]: ...
    
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
    ) -> ProfileObject: ...
    
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
    ) -> list[ProfileObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
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
    ) -> ProfileObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ProfileObject: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        monitor_all_messages: Literal["disable", "enable"] | None = ...,
        log_packet: Literal["disable", "enable"] | None = ...,
        track_requests_answers: Literal["disable", "enable"] | None = ...,
        missing_request_action: Literal["allow", "block", "reset", "monitor"] | None = ...,
        protocol_version_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        message_length_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        request_error_flag_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        cmd_flags_reserve_set: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_invalid: Literal["allow", "block", "reset", "monitor"] | None = ...,
        command_code_range: str | None = ...,
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
    "Profile",
    "ProfileDictMode",
    "ProfileObjectMode",
    "ProfilePayload",
    "ProfileObject",
]