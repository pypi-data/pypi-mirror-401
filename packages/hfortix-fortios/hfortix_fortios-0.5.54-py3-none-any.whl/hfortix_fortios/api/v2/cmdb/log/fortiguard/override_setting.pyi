from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class OverrideSettingPayload(TypedDict, total=False):
    """
    Type hints for log/fortiguard/override_setting payload fields.
    
    Override global FortiCloud logging settings for this VDOM.
    
    **Usage:**
        payload: OverrideSettingPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    override: Literal["enable", "disable"]  # Overriding FortiCloud settings for this VDOM or us | Default: disable
    status: Literal["enable", "disable"]  # Enable/disable logging to FortiCloud. | Default: disable
    upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]  # Configure how log messages are sent to FortiCloud. | Default: 5-minute
    upload_interval: Literal["daily", "weekly", "monthly"]  # Frequency of uploading log files to FortiCloud. | Default: daily
    upload_day: str  # Day of week to roll logs.
    upload_time: str  # Time of day to roll logs (hh:mm).
    priority: Literal["default", "low"]  # Set log transmission priority. | Default: default
    max_log_rate: int  # FortiCloud maximum log rate in MBps | Default: 0 | Min: 0 | Max: 100000
    access_config: Literal["enable", "disable"]  # Enable/disable FortiCloud access to configuration | Default: enable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class OverrideSettingResponse(TypedDict):
    """
    Type hints for log/fortiguard/override_setting API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    override: Literal["enable", "disable"]  # Overriding FortiCloud settings for this VDOM or us | Default: disable
    status: Literal["enable", "disable"]  # Enable/disable logging to FortiCloud. | Default: disable
    upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]  # Configure how log messages are sent to FortiCloud. | Default: 5-minute
    upload_interval: Literal["daily", "weekly", "monthly"]  # Frequency of uploading log files to FortiCloud. | Default: daily
    upload_day: str  # Day of week to roll logs.
    upload_time: str  # Time of day to roll logs (hh:mm).
    priority: Literal["default", "low"]  # Set log transmission priority. | Default: default
    max_log_rate: int  # FortiCloud maximum log rate in MBps | Default: 0 | Min: 0 | Max: 100000
    access_config: Literal["enable", "disable"]  # Enable/disable FortiCloud access to configuration | Default: enable


@final
class OverrideSettingObject:
    """Typed FortiObject for log/fortiguard/override_setting with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Overriding FortiCloud settings for this VDOM or use global s | Default: disable
    override: Literal["enable", "disable"]
    # Enable/disable logging to FortiCloud. | Default: disable
    status: Literal["enable", "disable"]
    # Configure how log messages are sent to FortiCloud. | Default: 5-minute
    upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]
    # Frequency of uploading log files to FortiCloud. | Default: daily
    upload_interval: Literal["daily", "weekly", "monthly"]
    # Day of week to roll logs.
    upload_day: str
    # Time of day to roll logs (hh:mm).
    upload_time: str
    # Set log transmission priority. | Default: default
    priority: Literal["default", "low"]
    # FortiCloud maximum log rate in MBps (0 = unlimited). | Default: 0 | Min: 0 | Max: 100000
    max_log_rate: int
    # Enable/disable FortiCloud access to configuration and data. | Default: enable
    access_config: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> OverrideSettingPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class OverrideSetting:
    """
    Override global FortiCloud logging settings for this VDOM.
    
    Path: log/fortiguard/override_setting
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingObject: ...
    
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
    ) -> OverrideSettingObject: ...
    
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
    ) -> OverrideSettingObject: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideSettingObject: ...
    
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
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
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
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

class OverrideSettingDictMode:
    """OverrideSetting endpoint for dict response mode (default for this client).
    
    By default returns OverrideSettingResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return OverrideSettingObject.
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
    ) -> OverrideSettingObject: ...
    
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
    ) -> OverrideSettingObject: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideSettingObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
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
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
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


class OverrideSettingObjectMode:
    """OverrideSetting endpoint for object response mode (default for this client).
    
    By default returns OverrideSettingObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return OverrideSettingResponse (TypedDict).
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingResponse: ...
    
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
    ) -> OverrideSettingObject: ...
    
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
    ) -> OverrideSettingObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideSettingObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OverrideSettingObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
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
        payload_dict: OverrideSettingPayload | None = ...,
        override: Literal["enable", "disable"] | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        upload_option: Literal["store-and-upload", "realtime", "1-minute", "5-minute"] | None = ...,
        upload_interval: Literal["daily", "weekly", "monthly"] | None = ...,
        upload_day: str | None = ...,
        upload_time: str | None = ...,
        priority: Literal["default", "low"] | None = ...,
        max_log_rate: int | None = ...,
        access_config: Literal["enable", "disable"] | None = ...,
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
    "OverrideSetting",
    "OverrideSettingDictMode",
    "OverrideSettingObjectMode",
    "OverrideSettingPayload",
    "OverrideSettingObject",
]