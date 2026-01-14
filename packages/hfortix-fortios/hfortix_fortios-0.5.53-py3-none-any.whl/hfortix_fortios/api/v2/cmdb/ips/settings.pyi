from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SettingsPayload(TypedDict, total=False):
    """
    Type hints for ips/settings payload fields.
    
    Configure IPS VDOM parameter.
    
    **Usage:**
        payload: SettingsPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    packet_log_history: int  # Number of packets to capture before and including | Default: 1 | Min: 1 | Max: 255
    packet_log_post_attack: int  # Number of packets to log after the IPS signature i | Default: 0 | Min: 0 | Max: 255
    packet_log_memory: int  # Maximum memory can be used by packet log | Default: 256 | Min: 64 | Max: 8192
    ips_packet_quota: int  # Maximum amount of disk space in MB for logged pack | Default: 0 | Min: 0 | Max: 4294967295
    proxy_inline_ips: Literal["disable", "enable"]  # Enable/disable proxy-mode policy inline IPS suppor | Default: enable
    ha_session_pickup: Literal["connectivity", "security"]  # IPS HA failover session pickup preference. | Default: connectivity

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class SettingsResponse(TypedDict):
    """
    Type hints for ips/settings API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    packet_log_history: int  # Number of packets to capture before and including | Default: 1 | Min: 1 | Max: 255
    packet_log_post_attack: int  # Number of packets to log after the IPS signature i | Default: 0 | Min: 0 | Max: 255
    packet_log_memory: int  # Maximum memory can be used by packet log | Default: 256 | Min: 64 | Max: 8192
    ips_packet_quota: int  # Maximum amount of disk space in MB for logged pack | Default: 0 | Min: 0 | Max: 4294967295
    proxy_inline_ips: Literal["disable", "enable"]  # Enable/disable proxy-mode policy inline IPS suppor | Default: enable
    ha_session_pickup: Literal["connectivity", "security"]  # IPS HA failover session pickup preference. | Default: connectivity


@final
class SettingsObject:
    """Typed FortiObject for ips/settings with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Number of packets to capture before and including the one in | Default: 1 | Min: 1 | Max: 255
    packet_log_history: int
    # Number of packets to log after the IPS signature is detected | Default: 0 | Min: 0 | Max: 255
    packet_log_post_attack: int
    # Maximum memory can be used by packet log (64 - 8192 kB). | Default: 256 | Min: 64 | Max: 8192
    packet_log_memory: int
    # Maximum amount of disk space in MB for logged packets when l | Default: 0 | Min: 0 | Max: 4294967295
    ips_packet_quota: int
    # Enable/disable proxy-mode policy inline IPS support. | Default: enable
    proxy_inline_ips: Literal["disable", "enable"]
    # IPS HA failover session pickup preference. | Default: connectivity
    ha_session_pickup: Literal["connectivity", "security"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SettingsPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Settings:
    """
    Configure IPS VDOM parameter.
    
    Path: ips/settings
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsObject: ...
    
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
    ) -> SettingsObject: ...
    
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
    ) -> SettingsObject: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SettingsObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
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
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
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

class SettingsDictMode:
    """Settings endpoint for dict response mode (default for this client).
    
    By default returns SettingsResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SettingsObject.
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
    ) -> SettingsObject: ...
    
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
    ) -> SettingsObject: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SettingsObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
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
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
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


class SettingsObjectMode:
    """Settings endpoint for object response mode (default for this client).
    
    By default returns SettingsObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SettingsResponse (TypedDict).
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsResponse: ...
    
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
    ) -> SettingsObject: ...
    
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
    ) -> SettingsObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SettingsObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SettingsObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
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
        payload_dict: SettingsPayload | None = ...,
        packet_log_history: int | None = ...,
        packet_log_post_attack: int | None = ...,
        packet_log_memory: int | None = ...,
        ips_packet_quota: int | None = ...,
        proxy_inline_ips: Literal["disable", "enable"] | None = ...,
        ha_session_pickup: Literal["connectivity", "security"] | None = ...,
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
    "Settings",
    "SettingsDictMode",
    "SettingsObjectMode",
    "SettingsPayload",
    "SettingsObject",
]